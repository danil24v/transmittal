from ..utils.validate import *


def update_apar_info(apar_id, checkboxes, closing_code, json_fields) -> str:
    apar = db.session.query(Apar).get(apar_id)
    apar.legal_checklist = checkboxes
    apar.closing_code = closing_code
    new_dict = apar.json_data.copy()
    new_dict.update(json_fields)
    apar.json_data = new_dict
    print('JSON FIELDS UP', apar.json_data)
    db.session.commit()
    return None


def update_trans_fields(trans_id, ticket: str = None, apar_number: str = None) -> str:
    trans = db.session.query(Transmittal).get(trans_id)
    if ticket is not None:
        if ticket != '':
            check_apar = db.session.query(Transmittal). \
                filter(Transmittal.id != trans.id). \
                filter(Transmittal.apar_number == apar_number). \
                filter(Transmittal.prd_id == trans.prd_id).first()
            if check_apar:
                return f'Jira ticket should be unique. It is already assigned to another transmittal (ID:{check_apar.id})'
        trans.ticket = ticket
    if apar_number:
        if db.session.query(Transmittal). \
                filter(Transmittal.id != trans.id). \
                filter(Transmittal.apar_number == apar_number).\
                filter(Transmittal.prd_id == trans.prd_id).first():
            return f'APAR number should be unique.'
        trans.apar_number = apar_number
    db.session.commit()
    return None


def update_trans_json_data(trans_id, json_record):
    trans = db.session.query(Transmittal).get(trans_id)
    if not trans.json_data:
        trans.json_data = {}
    new_dict = trans.json_data.copy()
    new_dict.update(json_record)
    trans.json_data = new_dict
    db.session.commit()

def update_hold_text(hold_id, text):
    hold = db.session.query(Hold).get(hold_id)
    hold.text = text
    db.session.commit()

