# Linkly for Dify

**Author:** Linkly Ltd (linkly-hq)
**Version:** 0.1.0
**Type:** Tool plugin
**Source:** https://github.com/Linkly-HQ/linkly-dify-plugin
**Support:** support@linklyhq.com

[Linkly](https://linklyhq.com) is a URL shortener with click tracking: branded short links on your own domain, UTM tagging, retargeting pixels, link rotators and detailed click analytics. This plugin lets Dify agents, chatflows and workflows create and inspect Linkly links and read their analytics through the public [Linkly API](https://linklyhq.com/support/short-link-creation-api).

## Setup

1. Sign up at https://linklyhq.com (the free plan works with the API).
2. In the Linkly app open **Settings > API** (https://app.linklyhq.com/app/user/api) and copy your **API key**. Note the **workspace ID** shown on the same page.
3. In Dify go to **Plugins > Linkly > Authorize** and paste the API key. The workspace ID is optional; leave it blank to use the first workspace the key can access.

The plugin needs outbound HTTPS access to `api.linklyhq.com`.

## Tools

| Tool | What it does |
|------|--------------|
| `create_link` | Create a short link for a destination URL. Optional name, custom slug, branded domain, note and UTM parameters. Returns the short URL and link ID. |
| `get_link` | Fetch a link by ID: destination, short URL, settings and click totals. |
| `list_links` | List or search links in the workspace, with paging and sorting (for example by `clicks_total`). |
| `get_clicks` | Time-series click counts for the workspace or one link, by day or hour, optionally unique clicks only or excluding bots. |
| `click_counters` | Clicks grouped by one dimension: country, city, region, platform, referrer, destination, ISP, bot name, link, or any UTM tag. |
| `list_domains` | List the custom domains available for short links in the workspace. |
| `delete_link` | Permanently delete a link by ID. |

## Usage examples

- Agent: "Shorten https://example.com/spring-sale on our brand domain and tag it utm_source=newsletter" - the agent calls `create_link` and returns the short URL.
- Workflow: a `create_link` node after a content-generation node, so every generated post carries a tracked short link.
- Reporting: `click_counters` with `counter=country` for the last 30 days, fed into an LLM node for a summary.

## Notes

- Dates for the analytics tools use `YYYY-MM-DD` (or ISO 8601 with time).
- `delete_link` is permanent. Deleted links can only be restored from the Linkly app.
- The plugin is stateless and stores nothing; see [PRIVACY.md](PRIVACY.md).

## Development

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
dify plugin package ./ -o linkly-0.1.0.difypkg
```

Issues and pull requests: https://github.com/Linkly-HQ/linkly-dify-plugin

## License

MIT - Linkly Ltd
