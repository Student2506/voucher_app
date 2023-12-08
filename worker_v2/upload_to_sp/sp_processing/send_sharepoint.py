"""Main logic to work with sharepint."""

from pathlib import Path
from typing import Any

from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind

from settings.config import get_logger, settings

logger = get_logger(__name__)


class SharePoint:
    def __init__(self) -> None:
        self.conn = ClientContext(str(settings.sharepoint_site)).with_credentials(
            ClientCredential(settings.sharepoint_client_id, settings.sharepoint_secret),
        )

    def create_folder(self, folder_name: str) -> Any:
        """Create Folder at Exchange Folder."""
        target_folder_url_path = (
            Path('/sites')
            / settings.sharepoint_site_name
            / settings.sharepoint_doc_library
        )
        root_folder = self.conn.web.get_folder_by_server_relative_url(
            target_folder_url_path.as_posix()
        )
        target_folder = root_folder.folders.add(folder_name).execute_query()
        logger.debug(f'Created {target_folder}')
        return target_folder

    def upload_file(self, file_name: str, folder_name: str, content: Any) -> str:
        """Upload file to specific folder."""
        target_folder_url_path = (
            Path('/sites')
            / settings.sharepoint_site_name
            / settings.sharepoint_doc_library
            / folder_name
        )
        target_folder = self.conn.web.get_folder_by_server_relative_path(
            target_folder_url_path.as_posix()
        )
        # target_folder.upload_file(file_name, content).execute_query()
        target_folder.files.create_upload_session(
            content, chunk_size=100_000_000
        ).execute_query()
        return f'{settings.sharepoint_site}/{settings.sharepoint_doc_library}/{folder_name}/{file_name}'

    def get_share_link(self, file_path: str) -> Any:
        logger.debug(file_path)
        vouchers = self.conn.web.get_file_by_server_relative_url(file_path)
        logger.debug(vouchers)
        result = vouchers.share_link(SharingLinkKind.OrganizationView).execute_query()
        logger.debug(result)
        guest_url = result.value.sharingLinkInfo.Url
        shared_file = self.conn.web.get_file_by_guest_url(guest_url).execute_query()
        return shared_file
