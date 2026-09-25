from flask import Flask

app = Flask(__name__)

from app.sources.registry import registry
registry.discover()

from app import routes