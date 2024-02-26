from werkzeug.datastructures import ImmutableMultiDict
from collections import namedtuple

from website.forms.validators import FormValidator
from website.forms.defaults import default_form_on_error
from website.utils.exceptions import WrongHttpMethod, FormValidationError

FormField = namedtuple('FormField', ['name', 'validator', 'error'])


class Form:

    def __init__(self, request: ImmutableMultiDict, fields: list, error_callback=default_form_on_error) -> None:
        self.request = request
        self.form = request.form
        self.fields = fields
        self.error_callback = error_callback
        if self.request.method == "POST":
            if not self.validate():
                return
            self.process()

    def is_clicked(self, component_name: str) -> bool:
        if component_name in self.form:
            return True
        return False

    def get_list(self, list_tag: str) -> list:
        return self.form.getlist(list_tag)

    def get_fields_by_namepart(self, name_part: str, remove_namepart=True) -> dict:
        ret_dict = {}
        for key in self.form.keys():
            if name_part in key:
                new_key = key
                if remove_namepart:
                    new_key = new_key.replace(name_part, '').strip()
                ret_dict.update({new_key: self.form.get(key)})

        return ret_dict

    def get_value(self, component_name: str) -> str:
        if component_name in self.form:
            return self.form.get(component_name)
        return None

    def validate_field(self, component_name: str, validator: FormValidator) -> bool:
        value = self.get_value(component_name)
        print('Value', value)
        if not value:
            value = ''
        return validator.validate(value)

    def validate(self):
        if self.request.method != "POST":
            raise WrongHttpMethod('Only POST allowed to perform validation operation.')
        for field in self.fields:
            print('validating', field)
            if not self.validate_field(field.name, field.validator):
                if not self.error_callback:
                    raise FormValidationError(field.error)
                self.error_callback(field.error)
                return False
        return True

    def process(custom_process_funct):
        def process_wrapper(self):
            if self.request.method != "POST":
                raise WrongHttpMethod('Only POST allowed to perform process operation.')
            custom_process_funct(self)

        return process_wrapper

        pass
