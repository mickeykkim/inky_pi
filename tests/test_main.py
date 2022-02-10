#!/usr/bin/env python
"""Tests for inky_pi.main"""
# pylint: disable=redefined-outer-name

from typing import Any, Dict, Generator
from unittest.mock import Mock, patch

import pytest

from inky_pi.helper import TrainModel, TrainObject, train_model_factory
from inky_pi.train.huxley2 import Huxley2  # type: ignore
from inky_pi.train.open_live import OpenLive  # type: ignore
from inky_pi.train.train_base import TrainBase  # type: ignore


# pylint: disable=possibly-unused-variable
@pytest.fixture
def _setup_vars() -> Generator[Dict[str, Any], None, None]:
    station_from: str = "MZH"
    station_to: str = "LBG"
    number: int = 3
    url: str = "http://url.url"
    token: str = "key"
    yield locals()


@patch("inky_pi.train.open_live.HistoryPlugin")
@patch("inky_pi.train.open_live.xsd.Element")
@patch("inky_pi.train.open_live.Client")
def test_instantiate_train_open_live(
    zeep_client_mock: Mock,
    zeep_xsd_mock: Mock,
    zeep_history_mock: Mock,
    _setup_vars: Dict[str, Any],
) -> None:
    """Test for creating OpenLDBWS instanced object"""
    train_object = TrainObject(
        model=TrainModel.OPEN_LIVE,
        station_from=_setup_vars["station_from"],
        station_to=_setup_vars["station_to"],
        number=_setup_vars["number"],
        url=_setup_vars["url"],
        token=_setup_vars["token"],
    )
    ret: TrainBase = train_model_factory(train_object)
    zeep_history_mock.assert_called_once()
    zeep_client_mock.assert_called_once()
    zeep_xsd_mock.assert_called()
    assert isinstance(ret, OpenLive)


@patch("inky_pi.train.huxley2.requests.get")
def test_instantiate_train_huxley2(
    requests_get_mock: Mock, _setup_vars: Dict[str, Any]
) -> None:
    """Test for creating Huxley2 OpenLDBWS instanced object"""
    train_object = TrainObject(
        model=TrainModel.HUXLEY2,
        station_from=_setup_vars["station_from"],
        station_to=_setup_vars["station_to"],
        number=_setup_vars["number"],
    )
    ret: TrainBase = train_model_factory(train_object)
    requests_get_mock.assert_called_once()
    assert isinstance(ret, Huxley2)


def test_instantiate_openldbws_error(_setup_vars: Dict[str, Any]) -> None:
    """Test for invalid OpenLDBWS object creation"""
    train_object = TrainObject(
        model=TrainModel.OPEN_LIVE,
        station_from=_setup_vars["station_from"],
        station_to=_setup_vars["station_to"],
        number=_setup_vars["number"],
    )
    with pytest.raises(ValueError):
        train_model_factory(train_object)
