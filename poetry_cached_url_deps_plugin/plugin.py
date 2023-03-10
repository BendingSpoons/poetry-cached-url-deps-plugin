import functools
import os
import tempfile
import urllib.parse
from pathlib import Path

from poetry.console.application import Application
from poetry.core.packages.package import Package
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.puzzle.provider import Provider
from poetry.utils.authenticator import Authenticator
from poetry.utils.helpers import download_file, get_file_hash


def mock_get_package_from_url(cls, url: str, session: Authenticator) -> Package:
    file_name = os.path.basename(urllib.parse.urlparse(url).path)
    with tempfile.TemporaryDirectory() as temp_dir:
        dest = Path(temp_dir) / file_name
        download_file(url, dest, session=session, chunk_size=1024 * 1024 * 10)
        package = cls.get_package_from_file(dest)

        package.files = [{"file": file_name, "hash": "sha256:" + get_file_hash(dest)}]

    package._source_type = "url"
    package._source_url = url

    return package


class PoetryCachedUrlDepsPlugin(ApplicationPlugin):
    def __init__(self) -> None:
        super().__init__()
        self._session = Authenticator(cache_id="_url")

    def activate(self, application: Application) -> None:
        mocked = classmethod(functools.partial(mock_get_package_from_url, session=self._session))
        Provider.get_package_from_url = mocked  # type: ignore
