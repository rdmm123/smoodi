from flask import Flask

from routes import api, catch_all

app = Flask(__name__)
app.config.from_prefixed_env()

if __name__ == '__main__':
    app.register_blueprint(api.bp)
    app.register_blueprint(catch_all.bp)
    app.run(host="0.0.0.0", debug=True)