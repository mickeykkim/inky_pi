from unittest.mock import Mock, patch

import pytest

from inky_pi.__main__ import main


@pytest.mark.integration
@patch("inky_pi.__main__.import_display")
def test_can_successfully_run_main(display_mock: Mock) -> None:
    """Test for running main"""
    args = Mock()
    args.option = "weather"
    args.output = "inky"
    with patch("inky_pi.__main__._parse_args", return_value=args):
        main()
        display_mock.assert_called_once()
