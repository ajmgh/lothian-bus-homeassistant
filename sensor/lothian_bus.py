import logging
import json
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_NAME)
from homeassistant.util import Throttle
import homeassistant.util.dt as dt_util
from homeassistant.components.sensor.rest import RestData

REQUEST_URL = "https://tfeapp.com/api/Unified.3.0/"
API_KEY = "LCHITUA68JXLBH61DP2YS63J7{}"
DEPARTURE_BOARD = "departure_boards.php"

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Data provided by Transport for Edinburgh"

DEFAULT_NAME = 'Lothian-Buses'

CONF_STOP_CODE = 'stop_code'
CONF_SERVICE_NUMBER = 'service_number'

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_STOP_CODE): cv.positive_int,
    vol.Required(CONF_SERVICE_NUMBER): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    stop_code = config.get(CONF_STOP_CODE)
    service_number = config.get(CONF_SERVICE_NUMBER)

    add_entities([LothianBusSensor(name, stop_code, service_number)])

class LothianBusSensor(Entity):
    def __init__(self, name, stop_code, service_number):
        self._name = name
        self._stop_code = stop_code
        self._service_number = service_number
        self._data = None
        self._lothian_api = LothianBusAPI()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return "minutes"

    @property
    def state(self):
        """Return the state of the device."""
        try:
            return self._data[2]
        except:
            return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:bus'

    @property
    def device_state_attributes(self):
        data = {
            ATTR_ATTRIBUTION: ATTRIBUTION
        }
        if self._data is not None:
            data['destination'] = self._data[0]
            data['real_time'] = self._data[1]

        return data

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data from the DWD-Weather-Warnings API."""
        data = self._lothian_api.GetDepartureData(self._stop_code, self._service_number)
        if data is not None:
            self._data = data

class LothianBusAPI:
    def GetDepartureData(self, stop_code, service_number):
        try:
            departure_resource = "{}{}?key={}&stops={}".format(
                 REQUEST_URL,
                 DEPARTURE_BOARD,
                 "73367e9efb0028ebed0669c9061fcec2",
                 stop_code)
            departure_rest = RestData('GET', departure_resource, None, None, None, True)
            departure_rest.update()
            json_string = departure_rest.data
            json_obj = json.loads(json_string)
            ourService = None
            services = json_obj[0]["services"]
            for service in services:
                if service["service_name"] == service_number:
                    ourService = service
                    break
            destination = ourService["departures"][0]["destination"]
            real_time = ourService["departures"][0]["real_time"]
            minutes = ourService["departures"][0]["minutes"]
        except:
            return None
        return destination, real_time, minutes
