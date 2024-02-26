from flask import flash

from website.forms.forms import Form
from ..models import *
from ..utils.create import create_hold
from ..utils.delete import delete_obj
from ..utils.update import update_hold_text
from ..utils.validate import validate_holds


class HoldsForm(Form):

    def __init__(self, trans_id, request: dict) -> None:
        self.trans_id = trans_id
        fields = [

        ]
        super().__init__(request, fields)

    def process(self):
        if self.is_clicked('btnHoldAdd'):
            sel_type = self.get_value('selHold')
            if sel_type:
                error = create_hold(self.trans_id, sel_type, '')
                if error:
                    flash(error, 'warning')

        if self.is_clicked('btnDel'):
            del_list = self.get_list('btnDel')
            if del_list:
                for id in del_list:
                    delete_obj(Hold, int(id), trans_id=self.trans_id)
            validate_holds(self.trans_id)

        if self.is_clicked('btnSave'):
            hold_field_name = 'hlField'
            list_fields = self.get_fields_by_namepart(hold_field_name)
            for hold_id in list_fields.keys():
                print('Checking', hold_id)
                field_val = self.get_value(f'{hold_field_name} {hold_id}')
                update_hold_text(hold_id, field_val)
                print('Holds:', field_val)
            validate_holds(self.trans_id)
            flash('Saved!', 'success')

        pass
