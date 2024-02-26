from . import db
from sqlalchemy.dialects.postgresql import JSON


def duplicate_object(old_obj):
    # SQLAlchemy related data class?

    mapper = db.inspect(type(old_obj))
    new_obj = type(old_obj)()

    for name, col in mapper.columns.items():
        # no PrimaryKey not Unique
        if not col.primary_key and not col.unique:
            setattr(new_obj, name, getattr(old_obj, name))

    return new_obj


def as_dict(object: db.Model):
    return {c.name: getattr(object, c.name) for c in object.__table__.columns}


class Transmittal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prd_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    type = db.Column(db.Integer, db.ForeignKey('product.type'))
    ticket = db.Column(db.String(15), unique=False)
    date = db.Column(db.Date, nullable=False)
    creator = db.Column(db.String(15), nullable=False)
    apar_number = db.Column(db.String(7))
    apars = db.relationship('Apar', cascade='all, delete')
    holds = db.relationship('Hold', cascade='all, delete')
    mcs = db.relationship('MCS', cascade='all, delete')
    valid_issues = db.Column(db.String(24), nullable=False)
    json_data = db.Column(JSON)


class Apar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transmittal_id = db.Column(db.Integer, db.ForeignKey('transmittal.id'))
    apar_number = db.Column(db.String(7), nullable=False)
    closing_code = db.Column(db.String(3))
    json_data = db.Column(JSON)
    legal_checklist = db.Column(db.String(24), nullable=False)


class MCS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transmittal_id = db.Column(db.Integer, db.ForeignKey('transmittal.id'))
    mcs = db.Column(db.String(40), nullable=False)


class HoldFields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(6), nullable=False)  # ROCKET or IBM
    name = db.Column(db.String(16), nullable=False, unique=True)
    regexp = db.Column(db.String(36))
    linelen = db.Column(db.Integer, nullable=False)
    maxsize = db.Column(db.Integer, nullable=False)
    allowfew = db.Column(db.Boolean, nullable=False, default=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(6))  # ROCKET or IBM
    fmid = db.Column(db.String(8), unique=True)
    qual = db.Column(db.String(3), unique=True)
    family = db.Column(db.String(10))
    description = db.Column(db.String(35))


class JenkinsFields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    name = db.Column(db.String(27))
    value = db.Column(db.String(48))


class ClosingCodeField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3))
    name = db.Column(db.String(20))
    regexp = db.Column(db.String(36))
    linelen = db.Column(db.Integer, nullable=False)
    maxsize = db.Column(db.Integer, nullable=False)
    is_urgent = db.Column(db.Boolean, nullable=False, default=False)


class Hold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transmittal_id = db.Column(db.Integer, db.ForeignKey('transmittal.id'))
    type = db.Column(db.String(8))
    text = db.Column(db.Text)
