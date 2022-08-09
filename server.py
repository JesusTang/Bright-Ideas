from flask_app.controllers import users
from flask_app.controllers import ideas
from flask_app.controllers import comments
from flask_app.controllers import topics
from flask_app import app

if __name__=="__main__":
    app.run(debug=True)