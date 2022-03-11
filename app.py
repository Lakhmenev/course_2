from flask import Flask
from main.main import main


app = Flask(__name__)
app.register_blueprint(main)


if __name__ == '__main__':
    app.debug = True
    app.config['JSON_AS_ASCII'] = False
    app.run(host="127.0.0.1", port=5000)
