from collections.abc import Generator
from typing import Any

from dify_plugin.entities.tool import ToolInvokeMessage

from tools._common import LinklyTool, as_int, link_summary
from utils.linkly_client import LinklyClient


class ListLinksTool(LinklyTool):
    def _run(self, client: LinklyClient, p: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        page_size = max(1, min(as_int(p.get("page_size"), 20) or 20, 100))
        data = client.list_links(
            search=p.get("search"),
            page=as_int(p.get("page"), 1),
            page_size=page_size,
            sort_by=p.get("sort_by"),
            sort_dir=p.get("sort_dir"),
        )
        links = [link_summary(l) for l in data.get("links", [])]
        lines = [f"- {l.get('full_url')} -> {l.get('url')} (ID {l.get('id')}, {l.get('clicks_total', 0)} clicks)" for l in links]
        header = f"{data.get('total_entries', len(links))} links in workspace, page {data.get('page_number', 1)} of {data.get('total_pages', 1)}"
        yield self.create_text_message(header + ("\n" + "\n".join(lines) if lines else ""))
        yield self.create_json_message({
            "links": links,
            "page_number": data.get("page_number"),
            "page_size": data.get("page_size"),
            "total_entries": data.get("total_entries"),
            "total_pages": data.get("total_pages"),
        })
