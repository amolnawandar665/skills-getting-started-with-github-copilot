from fastapi.testclient import TestClient
import pytest
from copy import deepcopy
import sys
from pathlib import Path

# Ensure project root is on sys.path so tests can import src.app
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import src.app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as c:
        yield c


@pytest.fixture(autouse=True)
def activities_state():
    """Snapshot and restore `activities` around each test to keep tests isolated."""
    original = deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)
