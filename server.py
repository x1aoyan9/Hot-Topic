from flask_app import app
from flask_app.controllers import users #other controllers belong here
if __name__ == "__main__":
app.run(debug=True)