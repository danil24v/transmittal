from website.forms.forms import Form, FormField
from .validators import RegexpValidator
from .. import app, db
from ..const import *
from ..models import *
from ..utils.delete import delete_obj
from ..utils.create import create_transmittal
from flask import flash


class CreateTrasmittalModal(Form):

    def __init__(self, prod_id, prod_type, form: dict) -> None:
        self.prod_id = prod_id
        self.type = prod_type
        fields = [
            FormField('inptApar', RegexpValidator(REGEXP_APAR, allow_empty=True), 'Invalid APAR number.'),
        ]
        if self.type == 'ROCKET':
            fields = [
                FormField('inptApar', RegexpValidator(REGEXP_TICKET, allow_empty=True), 'Invalid Jira ticket.')
            ]
        super().__init__(form, fields)

    def process(self):
        if self.is_clicked('btnCreate'):
            input_apar = self.get_value('inptApar')
            if input_apar:
                error = create_transmittal(self.prod_id, input_apar, creator='me')
                if error:
                    flash(error, 'warning')
        pass
