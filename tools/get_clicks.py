from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._common import LinklyMixin, as_bool
from utils.linkly_client import LinklyClient


class GetClicksTool(LinklyMixin, Tool):
    def _run(self, client: LinklyClient, p: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        params = {
            "link_id": p.get("link_id"),
            "start": p.get("start"),
            "end": p.get("end"),
            "frequency": p.get("frequency") or "day",
            "timezone": p.get("timezone"),
            "format": "json",
        }
        if as_bool(p.get("unique"), False):
            params["unique"] = "true"
        if not as_bool(p.get("bots"), True):
            params["bots"] = "false"
        data = client.get_clicks(**params)
        traffic = data.get("traffic", data)
        total = 0
        if isinstance(traffic, list):
            for row in traffic:
                if isinstance(row, dict):
                    for k, v in row.items():
                        if k not in ("date", "datetime", "time", "t") and isinstance(v, (int, float)):
                            total += v
        yield self.create_text_message(f"{len(traffic) if isinstance(traffic, list) else 0} {params['frequency']} buckets, {total} clicks in range")
        yield self.create_json_message({"traffic": traffic})
