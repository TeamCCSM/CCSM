import platform
from enum import Enum
from pathlib import Path
from typing import Optional, Self, Union
from dataclasses import dataclass
from . import common

savegamepath = "compatdata/774801/pfx/drive_c/Users/steamuser/AppData/Local/CrabChampions/Saved/SaveGames"

steam_paths = {
    common.SteamTypes.Windows: Path("C:/Program Files (x86)/Steam"),
    common.SteamTypes.LinuxNative: Path.home()
    / ".local/share/Steam",
    common.SteamTypes.LinuxFlatpak: Path.home()
    / ".var/app/com.valvesoftware.Steam/data/Steam",
}


class GetOptionsError(Enum):
    Platform = 1
    SteamType = 2
    CustomTypeNoPathOverride = 3


@dataclass
class Options:
    platform: common.Platforms
    steam_type: common.SteamTypes
    steam_path: Path

    @classmethod
    def get_defaults(
        cls: type[Self],
        platform_override: Optional[common.Platforms] = None,
        steam_type_override: Optional[common.SteamTypes] = None,
        steam_path_override: Optional[Path] = None
    ) -> Union[GetOptionsError, Self]:
        user_platform = None
        if platform_override is not None:
            user_platform = platform_override
        else:
            user_platform = common.Platforms.get(platform.system())
            if user_platform is None:
                return GetOptionsError.Platform

        steam_type = None
        if steam_type_override is not None:
            steam_type = steam_type_override
        else:
            steam_type = common.SteamTypes.get(user_platform)
            if steam_type is None:
                return GetOptionsError.SteamType

        steam_path = None
        if steam_path_override is not None:
            steam_path = steam_path_override
        else:
            steam_path = steam_paths.get(steam_type)
            if steam_path is None:
                return GetOptionsError.CustomTypeNoPathOverride
        return cls(user_platform, steam_type, steam_path)
