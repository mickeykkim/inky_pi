"""Open Live Departure Boards Web Service (OpenLDBWS) API
"""
from typing import Any, Optional

import zeep
from loguru import logger

from inky_pi.train.train_base import TrainBase, TrainObject, abbreviate_stn_name


class OpenLive(TrainBase):
    """Fetch and manage train data"""

    def __init__(self) -> None:
        self._num: int = 0
        self._data: Optional[Any] = None
        self._origin: str = ""
        self._destination: str = ""

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
            self._origin = abbreviate_stn_name(self._data.locationName)
            self._destination = abbreviate_stn_name(self._data.filterLocationName)
        except protocol.exceptions.Fault as exc:
            logger.error("Error retrieving train data (check stations?).")
            raise ValueError(f"Invalid train data request: {train_object}") from exc

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
            logger.error("Invalid fetch_train num", num)
            raise ValueError(
                f"{num} is an invalid train request number (max: {self._num})"
            )

        if not self._data:
            raise ValueError("No train data available")

        try:
            # Get all data
            service: Any = self._data.trainServices.service[num - 1]
            platform: str = service.platform[0:2]
            arrival_t: str = service.std
            dest_stn: str = service.destination.location[0].locationName
            dest_stn_abbr: str = abbreviate_stn_name(dest_stn)
            status: str = service.etd
            return f"{arrival_t} | P{platform} to {dest_stn_abbr} - {status}"
        except (AttributeError, TypeError, KeyError, IndexError):
            # Try to get the error message & line wrap over each line
            l_len: int = 38
            try:
                # pylint: disable=protected-access
                error_msg = str(self._data.nrccMessages.message[0]._value_1)[1:]
                if num == 1:
                    logger.warning(error_msg)
                return (error_msg[(num - 1) * l_len : num * l_len]).lstrip(" ")
            except (AttributeError, TypeError, KeyError, IndexError) as exc:
                logger.error("Could not get train error message", repr(exc))
                # Check if any trains are running
                error_msg = f"No trains to {self._destination} from {self._origin}."
                if num == 1:
                    logger.warning(error_msg)
                if self._data.trainServices is None:
                    return (error_msg[(num - 1) * l_len : num * l_len]).lstrip(" ")
                # Otherwise, return generic message on line 1
                msg: str = "Error retrieving train data." if num == 1 else ""
                return f"{msg}"


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
