import json
import requests
from requests_oauthlib import OAuth2Session

import logging
import os

# hack against InsecureTransportError: (insecure_transport) OAuth 2 MUST utilize https
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


authorization_base_url = " https://api.mcs3.miele.com/thirdparty/login/"
token_url = "https://api.mcs3.miele.com/thirdparty/token"
scope = ["write:devices", "read:devices"]

config = json.load(open("config.json"))


client_id = config["client_id"]
client_secret = config["client_secret"]
agent = config["agent"]

# TODO idea from : https://github.com/docbobo/home-assistant-miele/blob/master/miele/miele_at_home.py
cache_path = "./tmp_cache"


def _get_cached_token(cache_path):
    token = None
    if cache_path:
        try:
            f = open(cache_path)
            token_info_string = f.read()
            f.close()
            token = json.loads(token_info_string)

        except IOError:
            pass

    return token


def _save_token(cache_path, token):
    if cache_path:
        try:
            f = open(cache_path, "w")
            f.write(json.dumps(token))
            f.close()
        except IOError:
            log.warning(f"Could not write token to cache file {cache_path}")
            pass


local_redirect = "http://localhost:5000/choco_auth"

token = _get_cached_token(cache_path)


miele = OAuth2Session(
    client_id,
    redirect_uri=local_redirect,
    auto_refresh_url=token_url,
    token=token,
    token_updater=_save_token,
    scope=scope,
)

if not miele.authorized:
    print(f" session is authorized: {miele.authorized}")
    print("-----------now getting new token---------------------------------")

    authorization_url, state = miele.authorization_url(authorization_base_url)
    print(f"Please go to {authorization_url} and authorize access.")

    code = input("Please enter the code: ")

    print("-----------now fetching token---------------------------------")
    token = miele.fetch_token(
        token_url,
        code=code,
        client_secret=client_secret,
        vg="de_DE",
        client_id=client_id,
        include_client_id=True,
    )
    _save_token(cache_path, token)

log.info(f"token: {token}")
print(f" session is authorized: {miele.authorized}")
url_devices = "https://api.mcs3.miele.com/v1/devices"

test = miele.get(url_devices)

print(f"test status: {test.status_code}")
print(f"test text: {test.text}")
print("-----------")
print(f"test json: {test.json()}")
