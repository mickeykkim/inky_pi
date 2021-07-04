#!/usr/bin/env python
"""Tests for inky_pi.main"""
# pylint: disable=redefined-outer-name

from typing import Any, Dict, Generator
from unittest.mock import Mock, patch

import pytest

from inky_pi.main import _train_model_factory
from inky_pi.train.huxley2_openldbws import HuxleyOpenLDBWS  # type: ignore
from inky_pi.train.openldbws import OpenLDBWS  # type: ignore
from inky_pi.train.train_base import TrainBase  # type: ignore


# pylint: disable=possibly-unused-variable
@pytest.fixture
def _setup_vars() -> Generator[Dict[str, Any], None, None]:
    t_station_from: str = "MZH"
    t_station_to: str = "LBG"
    t_num: int = 3
    t_wsdl: str = 'http://url.url'
    t_ldb_token: str = 'key'
    yield locals()


@patch('inky_pi.train.openldbws.HistoryPlugin')
@patch('inky_pi.train.openldbws.xsd.Element')
@patch('inky_pi.train.openldbws.Client')
def test_instantiate_train_openldbws(zeep_client_mock: Mock,
                                     zeep_xsd_mock: Mock,
                                     zeep_history_mock: Mock,
                                     _setup_vars: Dict[str, Any]) -> None:
    """Test for creating OpenLDBWS instanced object"""
    ret: TrainBase = _train_model_factory('openldbws',
                                          _setup_vars['t_station_from'],
                                          _setup_vars['t_station_to'],
                                          _setup_vars['t_num'],
                                          _setup_vars['t_wsdl'],
                                          _setup_vars['t_ldb_token'])
    zeep_history_mock.assert_called_once()
    zeep_client_mock.assert_called_once()
    zeep_xsd_mock.assert_called()
    assert isinstance(ret, OpenLDBWS)


@patch('inky_pi.train.huxley2_openldbws.requests.get')
def test_instantiate_train_huxley2(requests_get_mock: Mock,
                                   _setup_vars: Dict[str, Any]) -> None:
    """Test for creating Huxley2 OpenLDBWS instanced object"""
    ret: TrainBase = _train_model_factory('huxley2',
                                          _setup_vars['t_station_from'],
                                          _setup_vars['t_station_to'],
                                          _setup_vars['t_num'])
    requests_get_mock.assert_called_once()
    assert isinstance(ret, HuxleyOpenLDBWS)


def test_instantiate_openldbws_error(_setup_vars: Dict[str, Any]) -> None:
    """Test for invalid OpenLDBWS object creation"""
    with pytest.raises(ValueError):
        _train_model_factory('openldbws', _setup_vars['t_station_from'],
                             _setup_vars['t_station_to'], _setup_vars['t_num'],
                             _setup_vars['t_wsdl'])
