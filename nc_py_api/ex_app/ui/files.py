"""Nextcloud API for working with drop-down file's menu."""
import os
import typing
from datetime import datetime, timezone

from pydantic import BaseModel

from ..._exceptions import NextcloudExceptionNotFound
from ..._misc import require_capabilities
from ..._session import NcSessionApp
from ...files import FilePermissions, FsNode

ENDPOINT_SUFFIX = "files/actions/menu"


class UiActionFileInfo(BaseModel):
    """File Information Nextcloud sends to the External Application."""

    fileId: int
    """FileID without Nextcloud instance ID"""
    name: str
    """Name of the file/directory"""
    directory: str
    """Directory relative to the user's home directory"""
    etag: str
    mime: str
    fileType: str
    """**file** or **dir**"""
    size: int
    """size of file/directory"""
    favorite: str
    """**true** or **false**"""
    permissions: int
    """Combination of :py:class:`~nc_py_api.files.FilePermissions` values"""
    mtime: int
    """Last modified time"""
    userId: str
    """The ID of the user performing the action."""
    shareOwner: typing.Optional[str]
    """If the object is shared, this is a display name of the share owner."""
    shareOwnerId: typing.Optional[str]
    """If the object is shared, this is the owner ID of the share."""

    def to_fs_node(self) -> FsNode:
        """Returns created ``FsNode`` from the file info given.

        .. note:: :py:attr:`~nc_py_api.files.FsNode.file_id` in this case is ``without`` **instance_id**
            and equal to :py:attr:`~nc_py_api.files.FsNodeInfo.fileid`.
        """
        user_path = os.path.join(self.directory, self.name).rstrip("/")
        is_dir = bool(self.fileType.lower() == "dir")
        if is_dir:
            user_path += "/"
        full_path = os.path.join(f"files/{self.userId}", user_path.lstrip("/"))

        permissions = "S" if self.shareOwnerId else ""
        if self.permissions & FilePermissions.PERMISSION_SHARE:
            permissions += "R"
        if self.permissions & FilePermissions.PERMISSION_READ:
            permissions += "G"
        if self.permissions & FilePermissions.PERMISSION_DELETE:
            permissions += "D"
        if self.permissions & FilePermissions.PERMISSION_UPDATE:
            permissions += "NV" if is_dir else "NVW"
        if is_dir and self.permissions & FilePermissions.PERMISSION_CREATE:
            permissions += "CK"
        return FsNode(
            full_path,
            etag=self.etag,
            size=self.size,
            content_length=0 if is_dir else self.size,
            permissions=permissions,
            favorite=bool(self.favorite.lower() == "true"),
            file_id=self.fileId,
            fileid=self.fileId,
            last_modified=datetime.utcfromtimestamp(self.mtime).replace(tzinfo=timezone.utc),
        )


class UiFileActionHandlerInfo(BaseModel):
    """Action information Nextcloud sends to the External Application."""

    actionName: str
    """Name of the action, useful when App registers multiple actions for one handler."""
    actionHandler: str
    """Callback url, which was called with this information."""
    actionFile: UiActionFileInfo
    """Information about the file on which the action run."""


class _UiFilesActionsAPI:
    """API for the drop-down menu in Nextcloud **Files app**."""

    def __init__(self, session: NcSessionApp):
        self._session = session

    def register(self, name: str, display_name: str, callback_url: str, **kwargs) -> None:
        """Registers the files a dropdown menu element."""
        require_capabilities("app_ecosystem_v2", self._session.capabilities)
        params = {
            "fileActionMenuParams": {
                "name": name,
                "display_name": display_name,
                "mime": kwargs.get("mime", "file"),
                "permissions": kwargs.get("permissions", 31),
                "order": kwargs.get("order", 0),
                "icon": kwargs.get("icon", ""),
                "icon_class": kwargs.get("icon_class", "icon-app-ecosystem-v2"),
                "action_handler": callback_url,
            },
        }
        self._session.ocs(method="POST", path=f"{self._session.ae_url}/{ENDPOINT_SUFFIX}", json=params)

    def unregister(self, name: str, not_fail=True) -> None:
        """Removes files dropdown menu element."""
        require_capabilities("app_ecosystem_v2", self._session.capabilities)
        params = {"fileActionMenuName": name}
        try:
            self._session.ocs(method="DELETE", path=f"{self._session.ae_url}/{ENDPOINT_SUFFIX}", json=params)
        except NextcloudExceptionNotFound as e:
            if not not_fail:
                raise e from None
