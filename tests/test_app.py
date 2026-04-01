from unittest.mock import patch

import pytest

from container_app_job_playground.app import create_parser, main, parse_duration, run_logging


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


@pytest.mark.parametrize(
    "argv,expected",
    [
        (["--duration", "5s"], "5s"),
        (["-d", "1m"], "1m"),
    ],
)
def test_create_parser_parses_duration(argv, expected):
    parser = create_parser()
    args = parser.parse_args(argv)
    assert args.duration == expected


def test_create_parser_requires_duration():
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


@pytest.mark.parametrize("seconds", [1, 5, 10])
def test_run_logging(seconds):
    """Test run_logging logs 'tikk' exactly 'seconds' times."""
    with (
        patch("container_app_job_playground.app.time.sleep") as mock_sleep,
        patch("container_app_job_playground.app.logger") as mock_logger,
    ):
        run_logging(seconds)

        assert mock_logger.info.call_count == seconds + 1

        assert mock_sleep.call_count == seconds


def test_main_runs_logging_when_duration_is_valid():
    with (
        patch("container_app_job_playground.app.logging.basicConfig") as mock_basic_config,
        patch("container_app_job_playground.app.create_parser") as mock_create_parser,
        patch("container_app_job_playground.app.parse_duration", return_value=5) as mock_parse_duration,
        patch("container_app_job_playground.app.run_logging") as mock_run_logging,
    ):
        mock_parser = mock_create_parser.return_value
        mock_parser.parse_args.return_value.duration = "5s"

        main()

        mock_basic_config.assert_called_once()
        mock_parse_duration.assert_called_once_with("5s")
        mock_run_logging.assert_called_once_with(5)


def test_main_calls_parser_error_when_duration_is_invalid():
    with (
        patch("container_app_job_playground.app.create_parser") as mock_create_parser,
        patch("container_app_job_playground.app.parse_duration", return_value=None),
        patch("container_app_job_playground.app.run_logging") as mock_run_logging,
    ):
        mock_parser = mock_create_parser.return_value
        mock_parser.parse_args.return_value.duration = "invalid"
        mock_parser.error.side_effect = SystemExit(2)

        with pytest.raises(SystemExit):
            main()

        mock_parser.error.assert_called_once_with(
            "Could not parse duration. Use formats like '3m', '5h', '1h30m', or '3m6h'."
        )
        mock_run_logging.assert_not_called()
