from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from tools._common import LinklyTool, link_summary
from utils.linkly_client import LinklyClient, LinklyError


class CreateLinkTool(LinklyTool):
    def _run(self, client: LinklyClient, p: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        url = (p.get("url") or "").strip()
        if not url:
            raise LinklyError("A destination URL is required.")
        if not url.lower().startswith(("http://", "https://")):
            url = "https://" + url
        link = client.create_link(
            url=url,
            name=p.get("name"),
            slug=p.get("slug"),
            domain=p.get("domain"),
            note=p.get("note"),
            utm_source=p.get("utm_source"),
            utm_medium=p.get("utm_medium"),
            utm_campaign=p.get("utm_campaign"),
            utm_content=p.get("utm_content"),
            utm_term=p.get("utm_term"),
        )
        summary = link_summary(link)
        short = summary.get("full_url", "")
        yield self.create_text_message(f"Created Linkly short link {short} (ID {summary.get('id')}) -> {summary.get('url', url)}")
        yield self.create_json_message(summary)
        if short:
            yield self.create_variable_message("short_url", short)
            yield self.create_variable_message("link_id", summary.get("id"))
