import platform
from enum import Enum
from pathlib import Path
from typing import Optional, Self, Union
from dataclasses import dataclass
from . import common


class GetOptionsError(Enum):
    Platform = 1
    SteamType = 2
    CustomTypeNoPathOverride = 3
    SavePath = 4


@dataclass
class Options:
    platform: common.Platforms
    steam_type: common.SteamTypes
    steam_path: Path
    save_path: Path

    @classmethod
    def get_defaults(
        cls: type[Self],
        platform_override: Optional[common.Platforms] = None,
        steam_type_override: Optional[common.SteamTypes] = None,
        steam_path_override: Optional[Path] = None,
        save_path_override: Optional[Path] = None,
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
            steam_path = common.steam_paths.get(steam_type)
            if steam_path is None:
                return GetOptionsError.CustomTypeNoPathOverride

        save_path = None
        if save_path_override is not None:
            save_path = save_path_override
        else:
            if user_platform == common.Platforms.Windows:
                save_path = Path.home() / "AppData/Local/CrabChampions/Saved/SaveGames"
            elif user_platform == common.Platforms.Linux:
                save_path = (
                    steam_path
                    / "steamapps/compatdata/774801/pfx/drive_c/users/steamuser/AppData/Local/CrabChampions/Saved/SaveGames"
                )

            if save_path is None or not save_path.exists():
                return GetOptionsError.SavePath

        return cls(user_platform, steam_type, steam_path, save_path)
