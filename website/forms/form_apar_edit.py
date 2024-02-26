from flask import flash

from website.forms.forms import Form, FormField
from .validators import RegexpValidator
from ..const import *
from ..utils.update import update_apar_info
from ..utils.validate import validate_apar


class AparEditForm(Form):

    def __init__(self, apar_id, request: dict) -> None:
        self.apar_id = apar_id
        fields = [
            FormField('selCode', RegexpValidator(REGEXP_CLCODE), 'Unexpected closing code.'),
        ]
        super().__init__(request, fields)

    def process(self):
        if self.is_clicked('btnSave'):
            closing_code = self.get_value('selCode')
            checkboxes_list = []
            checkboxes_list.extend(self.get_list('cbQuestion'))
            checkboxes_list.extend(self.get_list('cbAdd'))
            checkboxes = ','.join(checkboxes_list)

            cl_fields_key = 'clField'
            list_fields = self.get_fields_by_namepart(cl_fields_key)
            json_cfields = {}
            for key in list_fields.keys():
                code, title = key.split(':')
                if code != closing_code.strip():
                    continue
                field_val = self.get_value(f'{cl_fields_key} {key}')
                json_cfields.update({title: field_val})

            error = update_apar_info(self.apar_id, checkboxes, closing_code, json_cfields)
            if error:
                flash(error, 'warning')

            validate_apar(self.apar_id)
            flash('Saved!', 'success')
        pass
