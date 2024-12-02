import json
import os
import logging
from requests_oauthlib import OAuth2Session

log = logging.getLogger(__name__)


class OAuthClient:
    def __init__(
        self,
        agent,
        client_id,
        client_secret,
        token_url,
        authorization_base_url,
        scope,
        cache_path,
    ):
        self.agent = agent
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.authorization_base_url = authorization_base_url
        self.scope = scope
        self.cache_path = cache_path
        self.token = self._get_cached_token()
        self.session = OAuth2Session(
            client_id,
            redirect_uri="http://localhost:5000/choco_auth",
            auto_refresh_url=token_url,
            token=self.token,
            token_updater=self._save_token,
            scope=scope,
        )
        self.session.headers["User-Agent"] = agent

    def _get_cached_token(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r") as f:
                log.debug("Loading token from cache")
                return json.load(f)
        return None

    def _save_token(self, token):
        with open(self.cache_path, "w") as f:
            log.debug("Saving token to cache")
            json.dump(token, f)

    def fetch_token(self, code, state):
        self.token = self.session.fetch_token(
            self.token_url,
            code=code,
            client_secret=self.client_secret,
            state=state,
            include_client_id=True,
        )
        log.info(f" fetched token: {self.token}")
        self._save_token(self.token)

    def get_authorization_url(self):
        return self.session.authorization_url(self.authorization_base_url)

    def is_authorized(self):
        return self.session.authorized
