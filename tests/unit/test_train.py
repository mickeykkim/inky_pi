"""Tests for train module"""
from typing import Generator, Mapping, Union
from unittest.mock import Mock, patch

import pytest

from inky_pi.train.huxley2 import Huxley2
from inky_pi.train.open_live import OpenLive
from inky_pi.train.train_base import TrainBase, abbreviate_stn_name
from inky_pi.util import TrainModel, TrainObject, train_model_factory


# pylint: disable=possibly-unused-variable
@pytest.fixture
def _setup_train_vars() -> Generator[Mapping[str, Union[int, float, str]], None, None]:
    station_from: str = "MZH"
    station_to: str = "LBG"
    number: int = 3
    url: str = "http://url.url"
    token: str = "key"
    yield locals()


@patch("inky_pi.train.open_live.HistoryPlugin")
@patch("inky_pi.train.open_live.xsd.Element")
@patch("inky_pi.train.open_live.Client")
def test_can_successfully_instantiate_train_open_live(
    zeep_client_mock: Mock,
    zeep_xsd_mock: Mock,
    zeep_history_mock: Mock,
    _setup_train_vars: Mapping,
) -> None:
    """Test for creating OpenLDBWS instanced object"""
    train_object = TrainObject(
        model=TrainModel.OPEN_LIVE,
        station_from=_setup_train_vars["station_from"],
        station_to=_setup_train_vars["station_to"],
        number=_setup_train_vars["number"],
        url=_setup_train_vars["url"],
        token=_setup_train_vars["token"],
    )
    ret: TrainBase = train_model_factory(train_object)
    zeep_history_mock.assert_called_once()
    zeep_client_mock.assert_called_once()
    assert zeep_xsd_mock.call_count == 2
    assert isinstance(ret, OpenLive)


@patch("inky_pi.train.huxley2.requests.get")
def test_can_successfully_instantiate_train_huxley2(
    requests_get_mock: Mock, _setup_train_vars: Mapping
) -> None:
    """Test for creating Huxley2 OpenLDBWS instanced object"""
    train_object = TrainObject(
        model=TrainModel.HUXLEY2,
        station_from=_setup_train_vars["station_from"],
        station_to=_setup_train_vars["station_to"],
        number=_setup_train_vars["number"],
    )
    ret: TrainBase = train_model_factory(train_object)
    requests_get_mock.assert_called_once()
    assert isinstance(ret, Huxley2)


def test_instantiate_openldbws_without_url_and_token_raises_error(
    _setup_train_vars: Mapping,
) -> None:
    """Test for invalid OpenLDBWS object creation
    Due to the fact that OpenLDBWS requires a URL and a token, this test will raise an
    error.
    """
    train_object = TrainObject(
        model=TrainModel.OPEN_LIVE,
        station_from=_setup_train_vars["station_from"],
        station_to=_setup_train_vars["station_to"],
        number=_setup_train_vars["number"],
    )
    with pytest.raises(ValueError):
        train_model_factory(train_object)


def test_abbreviate_station_name() -> None:
    """Test for abbreviating station names"""
    assert abbreviate_stn_name("London Cannon Street") == "London Cannon St"
    assert abbreviate_stn_name("Clapham South") == "Clapham S"
    assert (
        abbreviate_stn_name("West Hampstead City Thameslink") == "W Hampstead City TL"
    )
