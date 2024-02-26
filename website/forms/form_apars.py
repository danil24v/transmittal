from website.forms.forms import Form, FormField
from .validators import RegexpValidator
from .. import app, db
from ..const import *
from ..models import *
from ..utils.delete import delete_obj
from ..utils.create import create_apar
from flask import flash


class AparsForm(Form):

    def __init__(self, trans_id, request: dict) -> None:
        self.trans_id = trans_id
        fields = [
            FormField('inptAdda', RegexpValidator(REGEXP_APAR), 'Invalid APAR number.')
        ]
        super().__init__(request, fields)

    def process(self):
        if self.is_clicked('btnAparAdd'):
            input_apar = self.get_value('inptAdda')
            if input_apar:
                error = create_apar(self.trans_id, input_apar)
                if error:
                    flash(error, 'warning')
        pass
