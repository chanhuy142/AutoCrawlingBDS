from flask import Flask
from api.routes import api_blueprint
from models import db
from flask_cors import CORS
#set port

app = Flask(__name__)



CORS(app)
app.register_blueprint(api_blueprint, url_prefix='/api')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/sampledb2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)