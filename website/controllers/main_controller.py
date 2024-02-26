from flask import render_template, request, flash, jsonify, send_file, redirect
from sqlalchemy import desc, JSON
from .. import app, db
import json
import re
from ..const import *
from ..models import *
from ..user import *
from ..forms.form_modal_create_trans import CreateTrasmittalModal


# ====================================================
#                   LIST OF PRODUCTS (MAIN PAGE)
# =====================================================
@app.route('/', methods=['GET', 'POST'])
@login_required
def main_page_products():
    filter_arg = request.args.get('filter_by')
    desc_arg = request.args.get('desc')
    order = '.asc()'
    if desc_arg != None:
        order = '.desc()'
        print()
    # prods = db.session.query(Product).order_by(Product.type).order_by(Product.qual).all()
    base_request = 'db.session.query(Product)'
    if filter_arg == 'name':
        base_request += f'.order_by(Product.description{order})'
    elif filter_arg == 'fmid':
        base_request += f'.order_by(Product.fmid{order})'
    elif filter_arg == 'family':
        base_request += f'.order_by(Product.family{order})'
    else:
        base_request += f'.order_by(Product.type{order}).order_by(Product.qual{order})'
    base_request += '.all()'
    prods = eval(base_request)
    return render_template("main.html", products=prods, page='main', prod=None)


# =======================================================
#                   LIST OF TRANSMITTALS
# =======================================================
@app.route('/transmittals/<product_id>', methods=['GET', 'POST'])
@login_required
def main_page_transmittals(product_id):
    prod = db.session.get(Product, product_id)
    form = CreateTrasmittalModal(product_id, prod.type, request)

    filter_arg = request.args.get('filter_by')
    desc_arg = request.args.get('desc')
    order = '.asc()'
    if desc_arg is not None:
        order = '.desc()'
        print()

    base_request = 'db.session.query(Transmittal).filter(Transmittal.prd_id == product_id)'
    if filter_arg == 'ticket':
        base_request += f'.order_by(Transmittal.ticket{order})'
    elif filter_arg == 'apar':
        base_request += f'.order_by(Transmittal.apar_number{order})'
    elif filter_arg == 'creator':
        base_request += f'.order_by(Transmittal.creator{order})'
    else:
        if desc_arg is not None:
            order = '.asc()'
        base_request += f'.order_by(Transmittal.date{order})'
    base_request += '.all()'

    # transmittals = db.session.query(Transmittal).filter(Transmittal.prd_id == product_id).order_by(
    #    desc(Transmittal.date))
    transmittals = eval(base_request)
    return render_template("main.html", page='transmittals',
                           prod=prod,
                           transmittals=transmittals)
