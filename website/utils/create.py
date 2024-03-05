from datetime import date

from ..utils.validate import *


def create_apar(trans_id, apar_number) -> str:
    print('CREATE APAR')

    if db.session.query(Apar). \
            filter(Apar.transmittal_id == trans_id). \
            filter(Apar.apar_number == apar_number).first():
        return f'{apar_number} already exists within this transmittal.'

    apar = Apar(transmittal_id=trans_id, apar_number=apar_number,
                closing_code='', json_data={}, legal_checklist='')
    db.session.add(apar)
    db.session.commit()

    validate_apar(apar.id)

    return None


def create_transmittal(prod_id, apar_number, creator) -> str:
    print('CREATE OBJECT')
    prod = db.session.get(Product, prod_id)
    if db.session.query(Transmittal).filter(Transmittal.prd_id == prod.id).filter(
            Transmittal.apar_number == apar_number).all():
        return "Transmittal already exists."

    current_date = date.today()
    trans = Transmittal(prd_id=prod.id, ticket='', apar_number=apar_number,
                        type=prod.type,
                        date=current_date, creator=creator, valid_issues='',
                        json_data={})
    db.session.add(trans)
    db.session.commit()

    if prod.type is not 'ROCKET':
        create_apar(trans.id, apar_number)
    return None


def create_hold(trans_id, type, text) -> str:
    trans = db.session.get(Transmittal, trans_id)
    prd_type = trans.type.upper()
    hold_settings = HOLD_FIELDS[prd_type][type]
    if not hold_settings.allowfew:
        ex_holds = db.session.query(Hold).filter(Hold.transmittal_id == trans_id).filter(Hold.type == type).all()
        if len(ex_holds) > 0:
            return f'HOLD {type} is not allowed to be added twice!'
    hold = Hold(transmittal_id=trans_id, type=type, text=text)
    db.session.add(hold)
    db.session.commit()

    return None


def create_mcs(trans_id, mcs_st) -> int:
    mcs = MCS(transmittal_id=trans_id, mcs=mcs_st)
    db.session.add(mcs)
    db.session.commit()
    return mcs.id


def create_req(trans_id, mod):
    mcs_st = f'++REQ({mod.strip()}) .'
    create_mcs(trans_id, mcs_st)


def create_if_req(trans_id, fmid, mod):
    mcs_st = f'++IF FMID({fmid.strip()}) THEN REQ({mod.strip()}) .'
    create_mcs(trans_id, mcs_st)


def create_del(trans_id, mods_list, is_mod_del):
    split = mods_list.split(',')
    mods = list(filter(lambda m: (len(m) > 1), split))
    for mod in mods:
        mcs_st = None
        if not is_mod_del:
            mcs_st = f'++DELETE({mod.strip()}) .'
        else:
            mcs_st = f'++MOD({mod.strip()}) DELETE .'
        create_mcs(trans_id, mcs_st)

