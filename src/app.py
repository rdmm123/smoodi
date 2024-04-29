from flask import Flask
from flask_cors import CORS

from backend import auth, frontend, api, commands

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_prefixed_env()
    CORS(app, supports_credentials=True, resources={
        r'/api/*': {'origins': f'http://{app.config['FRONTEND_SERVER_NAME']}'}
    })
    app.register_blueprint(auth.bp)
    app.register_blueprint(frontend.bp)
    app.register_blueprint(commands.bp)
    app.register_blueprint(api.bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0")