import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

import pytest
from app import app as flask_app
from pathlib import Path

test_results_path = Path("data/test_survey.ndjson")

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })

    from storage import RESULTS_PATH
    original_path = RESULTS_PATH
    RESULTS_PATH.unlink(missing_ok=True)

    RESULTS_PATH = test_results_path

    yield flask_app

    if test_results_path.exists():
        test_results_path.unlink() 

    RESULTS_PATH = original_path

@pytest.fixture()
def client(app):
    return app.test_client()