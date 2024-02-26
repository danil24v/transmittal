from website.forms.forms import Form, FormField
from .validators import RegexpValidator
from .. import app, db
from ..const import *
from ..models import *
from ..utils.delete import delete_obj
from ..utils.update import update_trans_fields, update_trans_json_data
from flask import flash


class MainTransForm(Form):

    def __init__(self, trans_id, request: dict) -> None:
        self.trans_id = trans_id
        fields = [
            FormField('inptJirat', RegexpValidator(REGEXP_TICKET, allow_empty=True), 'Invalid Jira ticket.')
        ]
        super().__init__(request, fields, )

    @Form.process
    def process(self):
        if self.is_clicked('btnSave'):
            input_ticket = self.get_value('inptJirat')
            error = update_trans_fields(self.trans_id, ticket=input_ticket)
            if error:
                flash(error, 'warning')

            input_ds = self.get_value('inptDs')
            if not input_ds:
                input_ds = ''
            new_record = {'ibm_ds': input_ds}
            update_trans_json_data(self.trans_id, new_record)

            flash('Saved!', 'success')
        pass
