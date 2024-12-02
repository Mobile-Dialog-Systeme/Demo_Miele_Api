import requests
import logging
from oauth_client import OAuthClient, OAuth2Session

log = logging.getLogger(__name__)


class MieleAPI:
    def __init__(self, oauth_client: OAuthClient):

        self.client = oauth_client
        self.session: OAuth2Session = oauth_client.session
        self.base_url = "https://api.mcs3.miele.com/v1"
        self.devices = {
            # Default Device ist eigentlich ein Hack.
            # Die ID wurde per Hand aus dem  Ergebnis von get_devices() genommen.
            "default": "000184392486",
            # Add other devices here
        }
        self.default_device = self.devices.get("default")

    def get_devices(self) -> dict:
        url = f"{self.base_url}/devices"
        response: requests.Response = self.session.get(url)

        log.info(f"Devices response: {response.json()}")

        return response.json()

    def start_program(self, device_name, program_id) -> requests.Response:
        device_id = self.devices.get(device_name, self.default_device)
        url = f"{self.base_url}/devices/{device_id}/programs"
        data = {"programId": program_id}
        response: requests.Response = self.session.put(url, json=data)
        log.info(f"Start program response: {response.status_code}")

        return response

    def turn_device_on(self, device_name="default", power_on=True) -> requests.Response:
        """
        Turns on the specified device.
        """
        device_id = self.devices.get(device_name, self.default_device)
        log.info(f"Turning on device {device_id}...")
        url = f"{self.base_url}/devices/{device_id}/actions"
        data = {"powerOn": power_on}

        response: requests.Response = self.session.put(url, json=data)

        if response.status_code == 204:
            log.info(f"Device {device_id} is now turned on!")
        else:
            log.error(f"Error Code: {response.status_code}")
            log.error(f"Response: {response.text}")
            log.error(f"Couldn't turn on the device {device_id}.")
        return response

    def mach_schoko(self, device_name="default") -> requests.Response:
        """
        Starts the chocolate program on the specified device.
        """
        log.info(f"Sending command to the device to make chocolate.")
        response: requests.Response = self.start_program(device_name, 24018)

        if response.status_code == 204:
            log.info("Chocolate program started successfully!")
        else:
            log.error("Failed to start the chocolate program.")
        return response
