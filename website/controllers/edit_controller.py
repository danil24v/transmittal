import sys

from flask import render_template, request, flash, jsonify, send_file, redirect
from sqlalchemy import desc
from .. import app, db
import json
import re
from ..const import *
from ..forms.form_trans_rocket import MainTransFormRocket
from ..models import *
from ..user import *
from ..forms.form_rels import RelsForm
from ..forms.form_holds import HoldsForm
from ..forms.form_apars import AparsForm
from ..forms.form_apar_edit import AparEditForm
from ..forms.form_trans import MainTransForm


# ================== HANDLE EDIT PAGE =====================
def get_trans_edit_template(transmittal, active_tab, current_edit_apar=None,
                            load_holds=True, closing_fields=[], cl_codes=[], apar_ctext=[],
                            html='transmittal.html'):
    hold_fields = []
    if transmittal is None:
        return jsonify({'msg': f'{transmittal_id} unknown transmittal!'})

    hold_fields = HOLD_FIELDS[transmittal.type.upper()]
    holds_fields_json = json.dumps(hold_fields)

    return render_template(html,
                           tab=active_tab,
                           trans=transmittal,
                           edit_apar=current_edit_apar,
                           hold_fields=hold_fields,
                           holds_fields_json=hold_fields,
                           closing_fields=closing_fields,
                           cl_codes=cl_codes,
                           apar_ctext=apar_ctext,
                           legal_checklist=LEGAL_CHECKLIST)

# ===============================================
#                   TRANSMITTAL EDIT
# ===============================================
@app.route('/edit/<transmittal_id>/', methods=['GET', 'POST'])
@login_required
def main_transmittal_router(transmittal_id):
    try:
        int(transmittal_id)
    except:
        return 'Why are you doing that?'

    trans = db.session.get(Transmittal, transmittal_id)
    print('sizeof trans:', sys.getsizeof(trans), sys.getsizeof(trans.apars))
    current_tab = request.form.get('current-tab')
    if not current_tab:
        current_tab = 'nav-trans-tab'
    if current_tab == 'nav-trans-tab':
        if trans.type == 'IBM':
            MainTransForm(transmittal_id, request)
        else:
            MainTransFormRocket(transmittal_id, request)
    elif current_tab == 'nav-apars-tab':
        AparsForm(transmittal_id, request)
    elif 'nav-apar-' in current_tab:
        AparsForm(transmittal_id, request)
    elif current_tab == 'nav-holds-tab':
        HoldsForm(transmittal_id, request)
    elif current_tab == 'nav-rels-tab':
        RelsForm(transmittal_id, request)
    return get_trans_edit_template(trans, current_tab)


@app.route('/edit/<transmittal_id>/apars/<apar_id>', methods=['GET', 'POST'])
@login_required
def edit_apar_data(transmittal_id, apar_id):
    AparEditForm(apar_id, request)
    trans = db.session.get(Transmittal, transmittal_id)
    apar = db.session.get(Apar, apar_id)

    apar_ctext = apar.json_data

    cl_codes = []
    main_apar_number = trans.apar_number
    restrictions_json = []
    closing_fields = CLOSING_CODES
    if apar.closing_code:
        cl_codes.append(apar.closing_code)
    for code in closing_fields.keys():
        cl_codes.append(code)
    cl_codes = list(dict.fromkeys(cl_codes))

    return render_template('apar.html',
                           trans=trans,
                           edit_apar=apar,
                           closing_fields=closing_fields,
                           cl_codes=cl_codes,
                           apar_ctext=apar_ctext,
                           closing_restrs=CLOSING_CODES,
                           legal_checklist=LEGAL_CHECKLIST)
