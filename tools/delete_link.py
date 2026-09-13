from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._common import LinklyMixin, as_int
from utils.linkly_client import LinklyClient, LinklyError


class DeleteLinkTool(LinklyMixin, Tool):
    def _run(self, client: LinklyClient, p: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        link_id = as_int(p.get("id"))
        if link_id is None:
            raise LinklyError("A numeric link ID is required.")
        data = client.delete_link(link_id)
        yield self.create_text_message(f"Deleted link {link_id}." if data is not None else f"Delete request sent for link {link_id}.")
        yield self.create_json_message({"id": link_id, "deleted": True, "response": data})
