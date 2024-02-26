from flask import Blueprint, render_template, request, flash, jsonify
from sqlalchemy.orm import make_transient

from ..models import *
from .. import app, db
import json
import re
from ..const import *
import json
from ..utils.delete import *
from flask_login import login_required


@app.route('/delete/apar/<apar_id>', methods=['DELETE'])
@login_required
def del_apar(apar_id):
    try:
        delete_apar(apar_id)
    except Exception as e:
        return str(e), 400
    return "OK", 200


@app.route('/delete/transmittal/<trans_id>', methods=['DELETE'])
@login_required
def del_trans(trans_id):
    error = delete_obj(Transmittal, trans_id)
    if error:
        return error, 400
    return "OK", 200


@app.route('/get/transmittal/<trans_id>', methods=['GET'])
@login_required
def get_trans_as_json(trans_id):
    def objs_to_list(objects) -> list:
        ret_list = []
        for obj in objects:
            tmp_obj = as_dict(obj)
            ret_list.append(tmp_obj)
        return ret_list

    trans = db.session.query(Transmittal).get(trans_id)
    d_trans = as_dict(trans)

    d_trans.update({'mcs': objs_to_list(trans.mcs)})
    d_trans.update({'holds': objs_to_list(trans.holds)})
    d_trans.update({'apars': objs_to_list(trans.apars)})

    return jsonify(d_trans)


@app.route('/copy/<trans_id>', methods=['GET'])
@login_required
def copy(trans_id):
    trans = db.session.query(Transmittal).get(trans_id)
    new_obj = duplicate_object(trans)
    new_obj.apar_number = 'ZZ12345'
    db.session.add(new_obj)
    db.session.commit()
    return "OK"

@app.route('/testvideo/', methods=['GET'])
def test():
    return render_template("test.html")
