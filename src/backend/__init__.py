from flask import Flask

from src.core.client.spotify.spotify_client import SpotifyClient
from src.core.client.spotify.models import SpotifyUser
from src.core.storage.cache_storage import CacheStorage
from src.core.repositories.user_repository import UserRepository

storage = CacheStorage()
client = SpotifyClient(storage=storage)
user_repository = UserRepository(user_cls=SpotifyUser, storage=storage)

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_prefixed_env()

    from src.backend import auth, frontend, api, commands
    app.register_blueprint(auth.bp)
    app.register_blueprint(frontend.bp)
    app.register_blueprint(commands.bp)
    app.register_blueprint(api.bp)

    if app.config['ENV'] == 'development':
        from flask_cors import CORS
        CORS(app, supports_credentials=True, resources={
            r'/api/*': {'origins': f"http://{app.config['FRONTEND_SERVER_NAME']}"}
        })
    
    return app
