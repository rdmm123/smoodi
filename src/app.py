from flask import Flask

from backend import auth, frontend, api, commands

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.register_blueprint(auth.bp)
    app.register_blueprint(frontend.bp)
    app.register_blueprint(commands.bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", debug=True)