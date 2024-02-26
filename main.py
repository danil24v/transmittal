from website import create_app
from website.utils import delete, validate
from website.controllers import edit_controller, main_controller, login_controller, rest_contoller
from website.utils import create, delete, validate, update

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)