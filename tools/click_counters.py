from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._common import LinklyMixin, as_bool
from utils.linkly_client import LinklyClient, LinklyError

COUNTERS = {"country", "city", "region", "platform", "referer", "destination", "bot_name", "isp", "link_id",
            "ad_network", "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "top_params"}


class ClickCountersTool(LinklyMixin, Tool):
    def _run(self, client: LinklyClient, p: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        counter = (p.get("counter") or "country").strip()
        if counter not in COUNTERS:
            raise LinklyError(f"Unknown dimension '{counter}'. Choose one of: {', '.join(sorted(COUNTERS))}.")
        params = {
            "link_id": p.get("link_id"),
            "start": p.get("start"),
            "end": p.get("end"),
            "country": p.get("country"),
            "format": "json",
        }
        if as_bool(p.get("unique"), False):
            params["unique"] = "true"
        if not as_bool(p.get("bots"), True):
            params["bots"] = "false"
        data = client.click_counters(counter, **params)
        values = data.get("values", [])
        top = values[:10] if isinstance(values, list) else []
        lines = []
        for row in top:
            if isinstance(row, dict):
                label = row.get("value", row.get("name", row.get(counter, "")))
                lines.append(f"- {label}: {row.get('count', row.get('clicks', ''))}")
            else:
                lines.append(f"- {row}")
        yield self.create_text_message(f"Clicks by {counter}: {data.get('total', '?')} total" + ("\n" + "\n".join(lines) if lines else ""))
        yield self.create_json_message({"counter": counter, "total": data.get("total"), "values": values})
