import json
import logging
import os
import webbrowser
from oauth_client import OAuthClient
from miele_api import MieleAPI
from local_server import TempServer
import time

logging.basicConfig(level=logging.INFO)
# use DEBUG to see the log messages from requests and oauthlib
# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def authorize_client(oauth_client: OAuthClient) -> OAuthClient:

    log.info("Authorization required.")
    local_server = TempServer()
    local_server.start()

    auth_url, state = oauth_client.get_authorization_url()
    print(f"Please go to {auth_url} and authorize access.")
    webbrowser.open(auth_url)
    code = local_server.get_auth_code()
    oauth_client.fetch_token(
        code=code,
        state=state,
    )
    local_server.stop()
    log.info("Authorization successful!")
    return oauth_client


def main():

    config = json.load(open("config.json"))
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    agent = config["agent"]

    cache_path = "./token_cache"

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    oauth_client = OAuthClient(
        agent=agent,
        client_id=client_id,
        client_secret=client_secret,
        token_url="https://api.mcs3.miele.com/thirdparty/token",
        authorization_base_url="https://api.mcs3.miele.com/thirdparty/login/",
        scope=["write:devices", "read:devices"],
        cache_path=cache_path,
    )

    if not oauth_client.is_authorized():
        oauth_client = authorize_client(oauth_client)

    log.info(f" session will use Headers: {oauth_client.session.headers}")

    miele_api = MieleAPI(oauth_client)

    # Finally you can do stuff with the API
    devices_info = miele_api.get_devices()
    # miele_api.turn_device_on()
    for _ in range(20):
        miele_api.turn_on_light()
        time.sleep(2)
        miele_api.turn_off_light()

    print(f" you have {len(devices_info)} devices")
    log.info(f"Devices: {devices_info}")


if __name__ == "__main__":
    main()
