from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database.db import get_connection
from app.database.init_db import main as init_db_main
from app.logging.tracer import reset_trace_file


@pytest.fixture(autouse=True)
def fresh_test_environment():
    """
    Prepare a clean local test environment before each test.
    """
    init_db_main()

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM notifications")
        connection.commit()

    reset_trace_file()
    yield