from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from utils.linkly_client import LinklyError, client_from_credentials


class LinklyProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        if not credentials.get("api_key"):
            raise ToolProviderCredentialValidationError("A Linkly API key is required.")
        workspace_id = credentials.get("workspace_id")
        if workspace_id not in (None, "") and not str(workspace_id).strip().isdigit():
            raise ToolProviderCredentialValidationError("Workspace ID must be a number (or left blank).")
        try:
            client = client_from_credentials(credentials)
            workspaces = client.list_workspaces()
            if workspace_id not in (None, ""):
                ids = {str(w.get("id")) for w in workspaces}
                if str(workspace_id).strip() not in ids:
                    raise ToolProviderCredentialValidationError(
                        f"Workspace {workspace_id} is not accessible with this API key. Available: {sorted(ids)}"
                    )
        except LinklyError as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
