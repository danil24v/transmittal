from website.forms.forms import Form, FormField
from .validators import RegexpValidator
from .. import app, db
from ..const import *
from ..models import *
from ..utils.delete import delete_obj
from ..utils.create import create_req, create_if_req, create_del, create_mcs


class RelsForm(Form):

    def __init__(self, trans_id, request: dict) -> None:
        self.trans_id = trans_id
        fields = [
            FormField('inptReq', RegexpValidator(REGEXP_SYSMOD, allow_empty=True), 'Invalid SYSMOD ID input.'),
            FormField('inptIfrFmid', RegexpValidator(REGEXP_FMID, allow_empty=True), 'Invalid FMID input.'),
            FormField('inptIfrSysmod', RegexpValidator(REGEXP_SYSMOD, allow_empty=True), 'Invalid SYSMOD ID input.'),
            FormField('inptDel', RegexpValidator(REGEXP_MODNAMES, allow_empty=True),
                      'Invalid input. Example: MOD1NAME1,MODNAME2 or MODNAME0'),
            FormField('inptDelMod', RegexpValidator(REGEXP_MODNAMES, allow_empty=True),
                      'Invalid input. Example: MOD1NAME1,MODNAME2 or MODNAME0'),
            FormField('inptCust', RegexpValidator(REGEXP_CUST, allow_empty=True),
                      'Bad Custom statement.')
        ]
        super().__init__(request, fields)

    def process(self):
        if self.is_clicked('btnAddReq'):
            input_mod = self.get_value('inptReq')
            if input_mod:
                create_req(self.trans_id, input_mod)

        if self.is_clicked('btnAddIfr'):
            input_fmid = self.get_value('inptIfrFmid')
            input_mod = self.get_value('inptIfrSysmod')
            if input_fmid and input_mod:
                create_if_req(self.trans_id, input_fmid, input_mod)

        if self.is_clicked('btnAddDel'):
            input_mods = self.get_value('inptDel')
            print('Field:', input_mods)
            if input_mods:
                create_del(self.trans_id, input_mods, is_mod_del=False)

        if self.is_clicked('btnAddDelMod'):
            input_mods = self.get_value('inptDelMod')
            if input_mods:
                create_del(self.trans_id, input_mods, is_mod_del=True)

        if self.is_clicked('btnAddCust'):
            input_cust = self.get_value('inptCust')
            if input_cust:
                create_mcs(self.trans_id, input_cust)

        if self.is_clicked('btnDelMcs'):
            del_list = self.get_list('mcs')
            if del_list:
                for id in del_list:
                    delete_obj(MCS, int(id))
        pass
