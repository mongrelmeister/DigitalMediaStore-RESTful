import os

from app import create_app
from app.config import app_config

env = os.environ["APP_CONFIG_ENV"]
app = create_app(app_config[env], instance_relative_config=True)

if __name__ == "__main__":
    app.run()
