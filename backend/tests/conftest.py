import os
import sys

os.environ["DATABASE_URL"] = "sqlite://"  # in-memory; must be set before database.py is imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
