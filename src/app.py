from flask import Flask

from routes import auth, frontend, api

app = Flask(__name__)
app.config.from_prefixed_env()

if __name__ == '__main__':
    app.register_blueprint(auth.bp)
    app.register_blueprint(frontend.bp)
    app.run(host="0.0.0.0", debug=True)