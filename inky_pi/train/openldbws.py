"""Open Live Departure Boards Web Service (OpenLDBWS) API
"""
from zeep import Client, xsd  # type: ignore
from zeep.plugins import HistoryPlugin  # type: ignore

from .train_base import TrainBase  # type: ignore


class OpenLDBWS(TrainBase):
    """Fetch and manage train data"""
    def __init__(self, stn_from: str, stn_to: str, num_trains: int,
                 t_wsdl: str, t_ldb_token: str) -> None:
        """Requests train data from OpenLDBWS train arrivals API endpoint

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
        self._res = client.service.GetDepartureBoard(
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
        print("Trains at " + self._res.locationName)
        print("===================================================")

        services = self._res.trainServices.service

        for service in services:
            print(service.std + " to " +
                  service.destination.location[0].locationName + " - " +
                  service.etd)
