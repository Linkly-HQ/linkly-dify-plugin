"""Minimal client for the Linkly REST API (https://api.linklyhq.com)."""

from typing import Any

import requests

BASE_URL = "https://api.linklyhq.com"
USER_AGENT = "linkly-dify-plugin/0.1.0 (+https://github.com/Linkly-HQ/linkly-dify-plugin)"
TIMEOUT = 30


class LinklyError(Exception):
    """Raised when the Linkly API returns an error or cannot be reached."""


class LinklyClient:
    def __init__(self, api_key: str, workspace_id: str | int | None = None):
        if not api_key:
            raise LinklyError("A Linkly API key is required.")
        self._api_key = api_key
        self._workspace_id = str(workspace_id).strip() if workspace_id not in (None, "") else None
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "User-Agent": USER_AGENT,
            }
        )

    # -- helpers -----------------------------------------------------------

    def request(self, method: str, path: str, params: dict | None = None, json: dict | None = None) -> Any:
        try:
            response = self._session.request(
                method,
                f"{BASE_URL}{path}",
                params={k: v for k, v in (params or {}).items() if v not in (None, "")},
                json=json,
                timeout=TIMEOUT,
            )
        except requests.RequestException as exc:  # network / TLS / timeout
            raise LinklyError(f"Could not reach the Linkly API: {exc}") from exc

        if response.status_code == 401:
            raise LinklyError("Linkly rejected the API key (HTTP 401). Check the key at https://app.linklyhq.com/app/user/api")
        if response.status_code == 403:
            raise LinklyError("This API key does not have access to that workspace or resource (HTTP 403).")
        if response.status_code == 404:
            raise LinklyError("Linkly returned 404: the link, domain or workspace was not found.")
        if response.status_code >= 400:
            detail = ""
            try:
                body = response.json()
                detail = body.get("error") or body.get("errors") or body.get("message") or body
            except ValueError:
                detail = response.text[:300]
            raise LinklyError(f"Linkly API error (HTTP {response.status_code}): {detail}")

        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError:
            return {"raw": response.text}

    def workspace_id(self) -> str:
        """Return the configured workspace id, or discover the first workspace the key can access."""
        if self._workspace_id:
            return self._workspace_id
        workspaces = self.request("GET", "/api/v1/workspaces")
        if not isinstance(workspaces, list) or not workspaces:
            raise LinklyError("No Linkly workspace is available to this API key.")
        self._workspace_id = str(workspaces[0]["id"])
        return self._workspace_id

    # -- endpoints ---------------------------------------------------------

    def list_workspaces(self) -> list[dict]:
        return self.request("GET", "/api/v1/workspaces")

    def create_link(self, **fields: Any) -> dict:
        payload = {k: v for k, v in fields.items() if v not in (None, "")}
        payload["workspace_id"] = int(self.workspace_id())
        return self.request("POST", "/api/v1/link", json=payload)

    def get_link(self, link_id: str | int) -> dict:
        return self.request("GET", f"/api/v1/link/{link_id}", params={"workspace_id": self.workspace_id()})

    def list_links(self, **params: Any) -> dict:
        return self.request("GET", f"/api/v1/workspace/{self.workspace_id()}/list_links", params=params)

    def get_clicks(self, **params: Any) -> dict:
        return self.request("GET", f"/api/v1/workspace/{self.workspace_id()}/clicks", params=params)

    def click_counters(self, counter: str, **params: Any) -> dict:
        return self.request("GET", f"/api/v1/workspace/{self.workspace_id()}/clicks/counters/{counter}", params=params)

    def list_domains(self) -> dict:
        return self.request("GET", f"/api/v1/workspace/{self.workspace_id()}/domains")

    def delete_link(self, link_id: str | int) -> dict:
        return self.request("DELETE", f"/api/v1/workspace/{self.workspace_id()}/links/{link_id}")


def client_from_credentials(credentials: dict[str, Any]) -> LinklyClient:
    return LinklyClient(api_key=credentials.get("api_key", ""), workspace_id=credentials.get("workspace_id"))
