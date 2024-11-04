from enum import StrEnum
from typing import Optional
from pathlib import Path


class Platforms(StrEnum):
    Windows = "Windows"
    Linux = "Linux"

    @staticmethod
    def get(string: str) -> Optional["Platforms"]:
        if string == "Windows":
            return Platforms.Windows
        elif string == "Linux":
            return Platforms.Linux


class SteamTypes(StrEnum):
    Windows = "Windows"
    LinuxNative = "Native"
    LinuxFlatpak = "Flatpak"
    Custom = "Custom"

    @staticmethod
    def get_linux_steam_type() -> Optional["SteamTypes"]:
        if (Path.home() / ".local/share/Steam").exists():
            return SteamTypes.LinuxNative
        elif (Path.home() / ".var/app/com.valvesoftware.Steam").exists():
            return SteamTypes.LinuxFlatpak

    @staticmethod
    def get(platform: Platforms) -> Optional["SteamTypes"]:
        if platform == Platforms.Windows:
            return SteamTypes.Windows
        elif platform == Platforms.Linux:
            return SteamTypes.get_linux_steam_type()
