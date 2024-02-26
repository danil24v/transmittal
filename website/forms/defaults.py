from flask import flash


def default_form_on_error(error):
    flash(error, 'warning')