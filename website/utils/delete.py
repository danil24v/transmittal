from ..models import *


def delete_obj(object_type, obj_id, trans_id=None):
    '''
    if trans_id:
        trans = db.session.query(Transmittal).get(trans_id)
        if not db.session.query(object_type).filter(object_type.id == obj_id)\
                .filter(object_type.transmittal_id == trans_id).one():
            raise Exception(f'{object_type}({obj_id}) not found within Transmittal{trans_id}')
        print(obj_id, 'found')
    '''
    obj = db.session.query(object_type).get(obj_id)
    db.session.delete(obj)
    db.session.commit()


def delete_apar(apar_id):
    apar = db.session.query(Apar).get(apar_id)
    trans = db.session.query(Transmittal).get(apar.transmittal_id)
    if trans.apar_number == apar.apar_number:
        raise Exception("Deletion of main APAR is prohibited.")
    delete_obj(Apar, apar_id)
    return None


def delete_hold(hold_id):
    delete_obj(Hold, hold_id)
    return None


def delete_transmittal(trans_id):
    trans = db.session.query(Transmittal).get(trans_id)
    delete_obj(Transmittal, trans_id)
    return None

