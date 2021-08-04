"""Open Live Departure Boards Web Service (OpenLDBWS) API
"""
from typing import Any

from zeep import Client, xsd  # type: ignore
from zeep.plugins import HistoryPlugin  # type: ignore

from .train_base import TrainBase, abbreviate_stn_name  # type: ignore


class OpenLive(TrainBase):
    """Fetch and manage train data"""
    def __init__(self, stn_from: str, stn_to: str, num_trains: int,
                 t_wsdl: str, t_ldb_token: str) -> None:
        """Requests train data from OpenLDBWS train arrivals API endpoint

        API description: http://lite.realtime.nationalrail.co.uk/openldbws/

        Args:
            stn_from (str): From station
            stn_to (str): To station
            num_trains (int): Number of departing trains to request
            t_wsdl (str): WSDL address
            t_ldb_token: OpenLDBWS API Token
        """
        history: HistoryPlugin = HistoryPlugin()
        client: Client = Client(wsdl=t_wsdl, plugins=[history])
        header: xsd.Element = xsd.Element(
            '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
            xsd.ComplexType([
                xsd.Element(
                    '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}' +
                    'TokenValue', xsd.String()),
            ]))
        header_value = header(TokenValue=t_ldb_token)
        self._num: int = num_trains
        self._data = client.service.GetDepartureBoard(
            numRows=num_trains,
            crs=stn_from,
            filterCrs=stn_to,
            filterType='to',
            _soapheaders=[header_value])

    def fetch_train(self, num: int) -> str:
        """Generate next train string

        String is returned in format:
            [hh:mm] | [Platform #] to [Final Destination Station] - [Status]

        Args:
            num (int): Next train departing number

        Returns:
            str: Formatted string or error message
        """
        if num < 0 or num > self._num:
            raise ValueError(
                f"{num} is an invalid train request number (max: {self._num})")

        try:
            # Get all data
            service: Any = self._data.trainServices.service[num - 1]
            platform: str = service.platform[0:2]
            arrival_t: str = service.std
            dest_stn: str = service.destination.location[0].locationName
            dest_stn_abbr: str = abbreviate_stn_name(dest_stn)
            status: str = service.etd
            return f'{arrival_t} | P{platform} to {dest_stn_abbr} - {status}'
        except (AttributeError, TypeError, KeyError, IndexError):
            try:
                # Try to get the error message & line wrap over each line
                l_length: int = 41
                return str(
                    self._data.nrccMessages[0].value[(num - 1) * l_length:num *
                                                     l_length])
            except (AttributeError, TypeError, KeyError, IndexError):
                # Check if any trains are running
                if self._data.trainServices is None and num == 1:
                    dest: str = self._data.filterLocationName
                    return f"No train services to {dest}."
                # Otherwise return generic message on line 1
                msg: str = "Error retrieving train data." if num == 1 else ""
                return f"{msg}"
