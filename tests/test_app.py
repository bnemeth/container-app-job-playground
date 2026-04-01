from unittest.mock import patch

import pytest

from container_app_job_playground.app import parse_duration, run_logging


@pytest.mark.parametrize(
    "duration_str,expected",
    [
        ("5s", 5),
        ("1m", 60),
        ("2m30s", 150),
        ("1h", 3600),
        ("1h5m30s", 3930),
        ("3m", 180),
        ("invalid", None),
    ],
)
def test_parse_duration(duration_str, expected):
    result = parse_duration(duration_str)
    assert result == expected


@pytest.mark.parametrize("seconds", [1, 5, 10])
def test_run_logging(seconds):
    """Test run_logging logs 'tikk' exactly 'seconds' times."""
    with (
        patch("container_app_job_playground.app.time.sleep") as mock_sleep,
        patch("container_app_job_playground.app.logger") as mock_logger,
    ):
        run_logging(seconds)

        # Ellenőrizni hogy pontosan 'seconds' alkalommal hívták meg az info-t
        # +1 az intro üzenetért ("Logging for X seconds...")
        assert mock_logger.info.call_count == seconds + 1

        # Ellenőrizni hogy sleep hívták meg
        assert mock_sleep.call_count == seconds
