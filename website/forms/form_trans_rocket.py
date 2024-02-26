from website.forms.forms import Form, FormField
from .validators import RegexpValidator, MutliLineValidator
from .. import app, db
from ..const import *
from ..models import *
from ..utils.delete import delete_obj
from ..utils.update import update_trans_fields, update_trans_json_data
from flask import flash


class MainTransFormRocket(Form):

    def __init__(self, trans_id, request: dict) -> None:
        self.trans_id = trans_id
        self.type = type
        fields = [
            FormField('inptJirat', RegexpValidator(REGEXP_TICKET), 'Invalid Jira ticket.'),
            FormField('inptComp', RegexpValidator(REGEXP_RKT_COMPONENT),
                      'Invalid Component.'),
            FormField('selType', RegexpValidator(REGEXP_RKT_TYPE),
                      'Invalid Type.'),
            FormField('inptDesc', RegexpValidator(REGEXP_MULTI_DESC),
                      'Invalid Description.')
        ]
        super().__init__(request, fields)
        print("ROCKET EDIT")

    def process(self):
        if self.is_clicked('btnSave'):
            error = None
            input_ticket = self.get_value('inptJirat')
            input_comp = self.get_value('inptComp')
            sel_type = self.get_value('selType')
            input_desc = self.get_value('inptDesc')
            if input_ticket:
                error = update_trans_fields(self.trans_id, ticket=input_ticket, apar_number=input_ticket)
                if error:
                    flash(error, 'warning')
            if not input_desc:
                input_desc = ''

            new_record = {'rkt_desc': input_desc,
                          'rkt_comp': input_comp,
                          'rkt_type': sel_type}
            update_trans_json_data(self.trans_id, new_record)
            flash('Saved!', 'success')
        pass
