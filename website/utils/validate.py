import re
from ..const import *
from ..models import *


def edit_validation(transmittal, tag, is_good):
    issues = transmittal.valid_issues
    if tag not in issues and not is_good:
        issues += ',' + tag
        db.session.commit()
    elif tag in issues and is_good:
        issues = issues.replace(f',{tag}', '')
        issues = issues.replace(f'{tag}', '')

    if transmittal.valid_issues != issues:
        transmittal.valid_issues = issues
        db.session.commit()
        print("Validation updated")
    else:
        print("Validation left as it is")


def validate_multi_line(plain_text: str, max_size: int, max_linelen: int, regexp: str, allow_empty: bool):
    text_len = len(plain_text)
    if not allow_empty and text_len == 0:
        return f'Field is empty.'
    if text_len > max_size:
        return f'Max size exceed by {text_len - max_size} symbols.'
    for line in plain_text.split('/n'):
        line_len = len(line)
        if regexp:
            if not re.match(regexp, line):
                return f'Line do not match regexp: {line}'
        if line_len > max_linelen:
            return f'Max line length exceed by {line_len - max_linelen} symbols: {line}'

    return None


''' 
=============================================
            APAR VALIDATION
=============================================
'''


def check_apar_issues(apar) -> str:
    # Validating closing text
    closing_code = apar.closing_code
    fields = None
    try:
        fields = CLOSING_CODES[closing_code]
    except KeyError:
        return f'closing_text, unexpected closing code.'

    apar_ctext = apar.json_data
    if not apar_ctext:
        apar_ctext = {}

    if not fields:
        return f'No filled closing fields.'

    for field in fields:
        try:
            closing_text = None
            try:
                closing_text = apar_ctext[field.name]
            except KeyError:
                if field.is_urgent:
                    return f'closing_text, field is urgent: {field.name}'
                else:
                    continue
            regexp = field.regexp
            max_linelen = field.linelen
            max_size = field.maxsize
            text_len = len(closing_text)
            if text_len == 0 and field.is_urgent:
                return f'closing_text, field is urgent: {field.name}'
            error = validate_multi_line(closing_text, max_size, max_linelen, regexp, allow_empty=True)
            if error:
                return f'closing_text, {error}'
        except Exception as e:
            return f'closing_text, unexpected error: {e}'
        print(f'{field.name} passed validation')
    # Validate legal checklist
    legal_list = apar.legal_checklist
    answers = legal_list.split(',')
    for question in LEGAL_CHECKLIST:
        if question['must']:
            qid = question['id']
            if qid not in answers:
                return f'legal_checklist, question {qid} must be checked.'

    return ''


def validate_apar(apar_id, trans: Transmittal = None):
    apar = db.session.query(Apar).get(apar_id)
    apar_issues = ''
    apar_issues = check_apar_issues(apar)
    if not trans:
        trans = db.session.query(Transmittal).get(apar.transmittal_id)
    apar_number = apar.apar_number
    edit_validation(trans, f'#apar:{apar_number}', is_good=(apar_issues == ''))
    print(f'Issues with {apar_number}, issues: {apar_issues}')


def validate_apars(transmittal):
    for apar in transmittal.apars:
        validate_apar(apar)


''' 
=============================================
            MAIN PAGE VALIDATION
=============================================
'''


def validate_ticket(transmittal):
    is_good = re.match(REGEXP_TICKET, transmittal.jiraticket)
    edit_validation(transmittal, '#tran', is_good)


''' 
=============================================
            HOLDS VALIDATION
=============================================
'''


def check_hold_issues(prd_type, hold):
    hold_restr = HOLD_FIELDS[prd_type][hold.type]
    error = validate_multi_line(hold.text, hold_restr.maxsize,
                                hold_restr.linelen, hold_restr.regexp, allow_empty=True)
    if error:
        return f'validate_hold, {error}'
    return None


def validate_holds(trans_id):
    trans = db.session.query(Transmittal).get(trans_id)
    is_good = True
    for hold in trans.holds:
        error = check_hold_issues(trans.type, hold)
        if error:
            is_good = False
    print('is good', is_good)
    edit_validation(trans, '#hld', is_good)
