from flask import Flask

from routes import auth, frontend, api

def create_app()    
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.register_blueprint(auth.bp)
    app.register_blueprint(frontend.bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", debug=True)