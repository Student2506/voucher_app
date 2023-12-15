"""Main logic to work with sharepint."""

from os import walk
from pathlib import Path
from shutil import copyfile

from settings.config import get_logger, settings

logger = get_logger(__name__)


class LocalStorage:
    def create_folder(self, folder_name: str) -> Path:
        """Create Folder at Exchange Folder."""
        full_path = Path(settings.folder_to_store) / folder_name
        if not full_path.exists():
            full_path.mkdir()
            logger.debug('Created new folder %s', str(full_path))
        else:
            for root, dirs, files in walk(full_path, topdown=False):
                for name in files:
                    (Path(root) / name).unlink()
                for name in dirs:
                    (Path(root) / name).rmdir()
            logger.debug("Folder %s was cleaned up", str(full_path))
        return full_path

    def upload_file(self, file_name: str, folder_name: str) -> str:
        """Upload file to specific folder."""
        logger.debug(file_name)
        logger.debug(folder_name)
        copyfile(file_name, Path(folder_name) / Path(file_name).name)

        return (
            f'scp://{settings.react_app_myip}'
            f'{Path(settings.folder_for_client) / Path(folder_name).name / Path(file_name).name}'
        )
