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
def get_trans_edit_template(transmittal_id, active_tab, current_edit_apar=None,
                            transmittal_obj=None,
                            load_holds=False, closing_fields=[], cl_codes=[], apar_ctext=[]):
    transmittal = transmittal_obj
    if not transmittal_obj:
        transmittal = db.session.get(Transmittal, transmittal_id)
    hold_fields = []
    if load_holds:
        hold_fields = db.session.query(HoldFields).all()
    if transmittal is None:
        return jsonify({'msg': f'{transmittal_id} unknown transmittal!'})

    return render_template("transmittal.html", tid=transmittal_id,
                           tab=active_tab,
                           trans=transmittal,
                           edit_apar=current_edit_apar,
                           hold_types=hold_fields,
                           closing_fields=closing_fields,
                           cl_codes=cl_codes,
                           apar_ctext=apar_ctext,
                           legal_checklist=LEGAL_CHECKLIST)


# ===============================================
#                   TRANSMITTAL EDIT
# ===============================================
@app.route('/edit/<transmittal_id>/', methods=['GET', 'POST'])
@login_required
def edit_main(transmittal_id):
    trans = db.session.get(Transmittal, transmittal_id)
    form = None
    if trans.type == "IBM":
        form = MainTransForm(transmittal_id, request)
    else:
        form = MainTransFormRocket(transmittal_id, request)
    return get_trans_edit_template(transmittal_id, 'transmittal', transmittal_obj=trans)


# ===============================================
#                   HOLDS EDIT
# ===============================================
@app.route('/edit/<transmittal_id>/holds', methods=['GET', 'POST'])
@login_required
def edit_holds(transmittal_id):
    active_tab = 'holds'
    form = HoldsForm(transmittal_id, request)

    return get_trans_edit_template(transmittal_id, active_tab, load_holds=True)


# ===============================================
#                   RELS EDIT
# ===============================================
@app.route('/edit/<transmittal_id>/rels', methods=['GET', 'POST'])
@login_required
def edit_rels(transmittal_id):
    active_tab = 'rels'

    form = RelsForm(transmittal_id, request)

    return get_trans_edit_template(transmittal_id, active_tab)


# ===============================================
#                   APAR EDIT
# ===============================================
@app.route('/edit/<transmittal_id>/apars', methods=['GET', 'POST'])
@login_required
def edit_apars(transmittal_id):
    active_tab = 'apars'
    form = AparsForm(transmittal_id, request)
    return get_trans_edit_template(transmittal_id, active_tab)


@app.route('/edit/<transmittal_id>/apars/<apar_id>', methods=['GET', 'POST'])
@login_required
def edit_apar_data(transmittal_id, apar_id):
    active_tab = 'apars'
    form = AparEditForm(apar_id, request)

    trans = db.session.get(Transmittal, transmittal_id)
    apar = db.session.get(Apar, apar_id)

    apar_ctext = apar.json_data

    cl_codes = []
    main_apar_number = trans.apar_number
    closing_fields = db.session.query(ClosingCodeField)
    if apar.closing_code:
        cl_codes.append(apar.closing_code)
    for field in closing_fields:
        cl_codes.append(field.code)
    cl_codes = list(dict.fromkeys(cl_codes))

    return get_trans_edit_template(transmittal_id, active_tab, current_edit_apar=apar,
                       closing_fields=closing_fields, cl_codes=cl_codes, apar_ctext=apar_ctext)
