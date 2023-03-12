"""Open Live Departure Boards Web Service (OpenLDBWS) API
"""
from typing import Any

import zeep
from loguru import logger

from inky_pi.train.train_base import TrainBase, TrainObject, abbreviate_stn_name


class OpenLive(TrainBase):
    """Fetch and manage train data"""

    def retrieve_data(self, protocol: Any, train_object: TrainObject) -> None:
        """Requests train data from OpenLDBWS train arrivals API endpoint

        API description: http://lite.realtime.nationalrail.co.uk/openldbws/

        Args:
            protocol (Any): Zeep object for SOAP requests
            train_object (TrainObject): Train object
        """
        history: Any = protocol.plugins.HistoryPlugin()
        client: Any = protocol.Client(wsdl=train_object.url, plugins=[history])
        header: Any = protocol.xsd.Element(
            "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken",
            protocol.xsd.ComplexType(
                [
                    protocol.xsd.Element(
                        "{http://thalesgroup.com/RTTI/2013-11-28/Token/types}"
                        + "TokenValue",
                        protocol.xsd.String(),
                    ),
                ]
            ),
        )
        header_value = header(TokenValue=train_object.token)
        self._num = train_object.number
        try:
            self._data = client.service.GetDepartureBoard(
                numRows=train_object.number,
                crs=train_object.station_from,
                filterCrs=train_object.station_to,
                filterType="to",
                _soapheaders=[header_value],
            )
            self.origin = abbreviate_stn_name(self._data.locationName)
            self.destination = abbreviate_stn_name(self._data.filterLocationName)
        except protocol.exceptions.Fault as exc:
            logger.error("Error retrieving train data (check stations?).")
            raise ValueError(f"Invalid train data request: {train_object}") from exc

    def _handle_error(self, num: int) -> str:
        """Log error and raise exception

        Args:
            num (int): Train number

        Raises:
            Exception: Exception to raise
        """
        if not self._data:
            raise ValueError("No train data available.")

        try:
            # pylint: disable=protected-access
            error_msg = str(self._data.nrccMessages.message[0]._value_1)[1:]
            return TrainBase.format_error_msg(error_msg, num)
        except (AttributeError, TypeError, KeyError, IndexError):
            error_msg = f"No trains to {self.destination} from {self.origin}."
            return TrainBase.format_error_msg(error_msg, num)

    def fetch_train(self, num: int) -> str:
        """Generate next train string

        String is returned in format:
            [hh:mm] | [Platform #] to [Final Destination Station] - [Status]

        Args:
            num (int): Next train departing number starting from 0

        Returns:
            str: Formatted string or error message
        """
        self._validate_number(num)
        if not self._data:
            raise ValueError("No train data available.")

        try:
            service: Any = self._data.trainServices.service[num]
            platform: str = service.platform[0:2]
            arrival_t: str = service.std
            dest_stn: str = service.destination.location[0].locationName
            status: str = service.etd
            return TrainBase.format_train_string(arrival_t, platform, dest_stn, status)
        except (AttributeError, TypeError, KeyError, IndexError):
            return self._handle_error(num)


def instantiate_open_live(train_object: TrainObject) -> OpenLive:
    """Open Live object creator

    Args:
        train_object (TrainObject): train object containing model

    Returns:
        OpenLive: OpenLive object
    """
    train_base = OpenLive()
    train_base.retrieve_data(zeep, train_object)
    return train_base
