from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._common import LinklyMixin, as_int, link_summary
from utils.linkly_client import LinklyClient, LinklyError


class GetLinkTool(LinklyMixin, Tool):
    def _run(self, client: LinklyClient, p: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        link_id = as_int(p.get("id"))
        if link_id is None:
            raise LinklyError("A numeric link ID is required.")
        link = client.get_link(link_id)
        summary = link_summary(link)
        yield self.create_text_message(
            f"Link {summary.get('id')}: {summary.get('full_url')} -> {summary.get('url')} "
            f"({summary.get('clicks_total', 0)} clicks total)"
        )
        yield self.create_json_message(link)
