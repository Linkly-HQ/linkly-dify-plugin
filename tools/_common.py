"""Shared helpers for the Linkly tools."""

from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from utils.linkly_client import LinklyClient, LinklyError, client_from_credentials


class LinklyMixin:
    """Mixin for the tool classes: builds the API client from provider credentials and normalises errors.

    Deliberately not a Tool subclass - Dify's loader requires exactly one Tool subclass per tool module.
    """

    def _client(self) -> LinklyClient:
        return client_from_credentials(self.runtime.credentials or {})

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        try:
            yield from self._run(self._client(), tool_parameters)
        except LinklyError as exc:
            yield self.create_text_message(f"Linkly error: {exc}")
            yield self.create_json_message({"error": str(exc)})

    def _run(self, client: LinklyClient, p: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:  # pragma: no cover
        raise NotImplementedError


def as_int(value: Any, default: int | None = None) -> int | None:
    if value in (None, ""):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def as_bool(value: Any, default: bool) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def link_summary(link: dict) -> dict:
    keys = ("id", "full_url", "url", "name", "slug", "domain", "note", "enabled", "clicks_total", "clicks_today",
            "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "inserted_at", "updated_at")
    return {k: link[k] for k in keys if k in link}
