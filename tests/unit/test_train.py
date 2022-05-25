"""Tests for train module"""
import json
from pathlib import Path
from typing import Generator, Mapping, Union
from unittest.mock import Mock, patch

import pytest

from inky_pi.train.huxley2 import Huxley2
from inky_pi.train.open_live import OpenLive
from inky_pi.train.train_base import (
    TrainBase,
    TrainModel,
    TrainObject,
    abbreviate_stn_name,
)
from inky_pi.util import train_model_factory
from tests.unit.resources.fakes import FakeRequests

TEST_DIR = Path(__file__).parent
RESOURCES_DIR = TEST_DIR.joinpath("resources")
HUXLEY2_TRAIN_DATA = RESOURCES_DIR.joinpath("train_data.json")
OPEN_LIVE_TRAIN_DATA = RESOURCES_DIR.joinpath("train_data_zeep.pickle")
INVALID_OPEN_LIVE_DATA = RESOURCES_DIR.joinpath("trains_unavailable_zeep.pickle")


# pylint: disable=possibly-unused-variable
@pytest.fixture
def _setup_train_vars() -> Generator[Mapping[str, Union[int, float, str]], None, None]:
    station_from: str = "MZH"
    station_to: str = "LBG"
    number: int = 3
    url: str = "http://url.url"
    token: str = "key"
    yield locals()


@pytest.fixture
def _setup_train_object_open_live(
    _setup_train_vars: Mapping,
) -> Generator[TrainObject, None, None]:
    open_live_train_object = TrainObject(
        model=TrainModel.OPEN_LIVE,
        station_from=_setup_train_vars["station_from"],
        station_to=_setup_train_vars["station_to"],
        number=_setup_train_vars["number"],
        url=_setup_train_vars["url"],
        token=_setup_train_vars["token"],
    )
    yield open_live_train_object


@pytest.fixture
def _setup_train_object_huxley2(
    _setup_train_vars: Mapping,
) -> Generator[TrainObject, None, None]:
    huxley2_train_object = TrainObject(
        model=TrainModel.HUXLEY2,
        station_from=_setup_train_vars["station_from"],
        station_to=_setup_train_vars["station_to"],
        number=_setup_train_vars["number"],
    )
    yield huxley2_train_object


@pytest.fixture
def _setup_huxley2_fake_data(
    _setup_train_object_huxley2: TrainObject,
) -> Generator[Huxley2, None, None]:
    requests = FakeRequests()
    with open(HUXLEY2_TRAIN_DATA, "r", encoding="utf-8") as file:
        train_data = json.load(file)
        requests.add_response(train_data, 200)

    train_base = Huxley2()
    train_base.retrieve_data(requests, _setup_train_object_huxley2)
    yield train_base


@pytest.mark.parametrize(
    "name, expected_abbreviation",
    [
        ("London Cannon Street", "London Cannon St"),
        ("Clapham South", "Clapham S"),
        ("West Hampstead City Thameslink", "W Hampstead City TL"),
    ],
)
def test_abbreviate_station_name(name: str, expected_abbreviation: str) -> None:
    """Test for abbreviating station names

    Args:
        name (str): The name of the station
        expected_abbreviation (str): The expected abbreviation of the station
    """
    assert abbreviate_stn_name(name) == expected_abbreviation


def test_format_train_string() -> None:
    """Test for formatting train string"""
    arrival_t = "12:00"
    platform = "1"
    dest_stn = "London Cannon Street"
    status = "On time"
    assert TrainBase.format_train_string(arrival_t, platform, dest_stn, status) == (
        "12:00 | P1 to London Cannon St - On time"
    )


@pytest.mark.parametrize(
    "error_msg, num, expected",
    [
        ("Error message", 0, "Error message"),
        (
            "There are no train services at this station",
            0,
            "There are no train services at this st",
        ),
        ("Error message", 1, ""),
        (
            "There are no train services at station London Bridge",
            1,
            "London Bridge",
        ),
    ],
)
def test_format_train_error_string(error_msg: str, num: int, expected: str) -> None:
    """Test for formatting train error string

    Args:
        error_msg (str): The error message
        num (int): The number of trains
        expected (str): The expected string
    """
    assert TrainBase.format_error_msg(error_msg, num) == expected


@patch("inky_pi.train.open_live.zeep.plugins.HistoryPlugin")
@patch("inky_pi.train.open_live.zeep.xsd.Element")
@patch("inky_pi.train.open_live.zeep.Client")
def test_can_successfully_instantiate_train_open_live(
    zeep_client_mock: Mock,
    zeep_xsd_mock: Mock,
    zeep_history_mock: Mock,
    _setup_train_object_open_live: TrainObject,
) -> None:
    """Test for creating OpenLDBWS instanced object

    Args:
        zeep_client_mock (Mock): Mock for Client class
        zeep_xsd_mock (Mock): Mock for xsd.Element class
        zeep_history_mock (Mock): Mock for HistoryPlugin class
        _setup_train_object_open_live (TrainObject): Open Live TrainObject
    """
    ret: TrainBase = train_model_factory(_setup_train_object_open_live)
    zeep_history_mock.assert_called_once()
    zeep_client_mock.assert_called_once()
    assert zeep_xsd_mock.call_count == 2
    assert isinstance(ret, OpenLive)


@patch("inky_pi.train.huxley2.requests.get")
def test_can_successfully_instantiate_train_huxley2(
    requests_get_mock: Mock, _setup_train_object_huxley2: TrainObject
) -> None:
    """Test for creating Huxley2 OpenLDBWS instanced object

    Args:
        requests_get_mock (Mock): Mock for requests.get class
        _setup_train_object_huxley2 (TrainObject): Huxley2 TrainObject
    """
    ret: TrainBase = train_model_factory(_setup_train_object_huxley2)
    requests_get_mock.assert_called_once()
    assert isinstance(ret, Huxley2)


@patch("inky_pi.util.sys.exit")
def test_instantiate_open_live_without_url_and_token_raises_error(
    sys_exit_mock: Mock, _setup_train_vars: Mapping
) -> None:
    """Test for invalid OpenLDBWS object creation
    Due to the fact OpenLDBWS requires URL and token, test will trigger error

    Args:
        _setup_train_vars (Mapping): Mapping of variables to be used in the test
    """
    train_object = TrainObject(
        model=TrainModel.OPEN_LIVE,
        station_from=_setup_train_vars["station_from"],
        station_to=_setup_train_vars["station_to"],
        number=_setup_train_vars["number"],
    )
    with pytest.raises(ValueError):
        train_model_factory(train_object)
        sys_exit_mock.assert_called_once()


@pytest.mark.parametrize(
    "num, expected",
    [
        (0, "18:11 | P2 to Slade Green - On time"),
        (1, "18:14 | P1 to Luton - On time"),
        (2, "18:21 | P2 to Slade Green - On time"),
    ],
)
def test_can_successfully_fetch_train_string_huxley2(
    num: int, expected: str, _setup_huxley2_fake_data: Huxley2
) -> None:
    """Test for fetching train string from Huxley2 fake data

    Args:
        num (int): The number of trains to be fetched
        expected (str): The expected string
        _setup_huxley2_fake_data (Huxley2): Huxley2 fake data
    """
    assert _setup_huxley2_fake_data.fetch_train(num) == expected


@pytest.mark.parametrize(
    "num",
    [-1, 10],
)
def test_fetch_train_string_huxley2_invalid_num_raises_error(
    num: int,
    _setup_huxley2_fake_data: Huxley2,
) -> None:
    """Test invalid train number for Huxley2

    Args:
        num (int): The number of trains to be fetched
        _setup_huxley2_fake_data (Huxley2): Huxley2 fake data
    """
    with pytest.raises(ValueError):
        _setup_huxley2_fake_data.fetch_train(num)
