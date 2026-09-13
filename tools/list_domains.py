from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from tools._common import LinklyTool
from utils.linkly_client import LinklyClient


class ListDomainsTool(LinklyTool):
    def _run(self, client: LinklyClient, p: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        data = client.list_domains()
        domains = data.get("domains", data if isinstance(data, list) else [])
        names = [d.get("name") or d.get("domain") if isinstance(d, dict) else str(d) for d in domains]
        yield self.create_text_message(("Domains: " + ", ".join(n for n in names if n)) if names else "No custom domains in this workspace.")
        yield self.create_json_message({"domains": domains})
