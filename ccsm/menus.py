from .common import Platforms, SteamTypes
from ui_forge import items
from collections import OrderedDict

yes_no = OrderedDict(
    {"Yes": items.OptionItem(value=True), "No": items.OptionItem(value=False)}
)

platform_select = OrderedDict(
    {
        "Windows": items.OptionItem(value=Platforms.Windows),
        "Linux": items.OptionItem(value=Platforms.Linux),
    }
)

linux_steam_version_select = OrderedDict(
    {
        "Native": items.OptionItem(value=SteamTypes.LinuxNative),
        "Flatpak": items.OptionItem(value=SteamTypes.LinuxFlatpak),
    }
)
