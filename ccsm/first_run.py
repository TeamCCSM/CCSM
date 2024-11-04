import curses
import ui_forge
from typing import Union, Tuple
from pathlib import Path
from . import menus, common, options


def path_validator(path: str) -> bool:
    if not path:
        return False
    new_path = Path(path)
    return new_path.exists() and new_path.is_dir()


def platform_select(start_y: int = 0) -> common.Platforms:
    platform_win = curses.newwin(2, 27, start_y, 0)
    platform = ui_forge.selection_ui(platform_win, menus.platform_select)
    return platform


def linux_steam_path_select(current_type: common.SteamTypes, start_y: int = 0) -> Path:
    editor_win = curses.newwin(3, curses.COLS - 1, start_y, 0)
    return Path(
        ui_forge.editor_ui(
            editor_win,
            str(options.steam_paths[current_type]),
            path_validator,
            header="Please input the path of steam, ending with the directory named 'Steam' (Will reset your input if the path is invalid/doesn't exist).",
        )
    )


def save_path_select(start_y: int = 0) -> Path:
    editor_win = curses.newwin(3, curses.COLS - 1, start_y, 0)
    return Path(
        ui_forge.editor_ui(
            editor_win,
            validator=path_validator,
            header="Please input the path of your Crab Champions saves, ending with the directory named 'SaveGames' (Will reset your input if the path is invalid/doesn't exist).",
        )
    )


class Unhandlable:
    pass


def handle_get_options_error(
    options_instance: Union[options.Options, options.GetOptionsError]
) -> Union[Unhandlable, Tuple[options.Options, bool, bool]]:
    steam_path_overwritten = False
    save_path_overwritten = False

    overrides = {}

    while isinstance(options_instance, options.GetOptionsError):
        match options_instance:
            case options.GetOptionsError.Platform:
                header_win = curses.newwin(2, curses.COLS - 1)
                header_win.addstr(0, 0, "Failed to retrieve platform")
                header_win.addstr(1, 0, "Override?")
                header_win.refresh()
                yes_no_win = curses.newwin(2, 6, 2, 0)
                override = ui_forge.selection_ui(yes_no_win, menus.yes_no)
                if override:
                    overrides["platform_override"] = platform_select()
                else:
                    return Unhandlable()

            case options.GetOptionsError.SteamType:
                header_win = curses.newwin(2, curses.COLS - 1)
                header_win.addstr(0, 0, "Default steam path does not appear to exist.")
                header_win.addstr(1, 0, "Override?")
                header_win.refresh()
                yes_no_win = curses.newwin(2, 6, 2, 0)
                override = ui_forge.selection_ui(yes_no_win, menus.yes_no)
                if override:
                    overrides["steam_type_override"] = common.SteamTypes.Custom
                    overrides["steam_path_override"] = linux_steam_path_select(
                        common.SteamTypes.LinuxNative
                    )
                    steam_path_overwritten = True
                else:
                    return Unhandlable()

            case options.GetOptionsError.CustomTypeNoPathOverride:
                return Unhandlable()

            case options.GetOptionsError.SavePath:
                header_win = curses.newwin(2, curses.COLS - 1)
                header_win.addstr(
                    0, 0, "Default Crab Champions save path does not appear to exist."
                )
                header_win.addstr(1, 0, "Override?")
                header_win.refresh()
                yes_no_win = curses.newwin(2, 6, 2, 0)
                override = ui_forge.selection_ui(yes_no_win, menus.yes_no)
                if override:
                    overrides["save_path_override"] = save_path_select()
                    save_path_overwritten = True
                else:
                    return Unhandlable()

        options_instance = options.Options.get_defaults(**overrides)

    return (
        options_instance,
        steam_path_overwritten,
        save_path_overwritten,
    )


def main() -> Union[options.Options, Unhandlable]:
    steam_path_overwritten = False
    save_path_overwritten = False

    options_instance = options.Options.get_defaults()
    options_instance_and_data = handle_get_options_error(options_instance)
    if isinstance(options_instance_and_data, Unhandlable):
        return Unhandlable()
    (
        options_instance,
        steam_path_overwritten,
        save_path_overwritten,
    ) = options_instance_and_data

    if (
        options_instance.platform == common.Platforms.Linux
        and not steam_path_overwritten
    ):
        override_steam_path: bool
        header_win = curses.newwin(2, curses.COLS - 1)
        header_win.addstr(0, 0, f"Detected Steam Path: {options_instance.steam_path}")
        header_win.addstr(1, 0, "Override?")
        header_win.refresh()
        yes_no_win = curses.newwin(2, 6, 2, 0)
        override_steam_path = ui_forge.selection_ui(
            yes_no_win, menus.yes_no, start_line=1
        )

        header_win.clear()
        header_win.refresh()

        if override_steam_path:
            options_instance.steam_type = common.SteamTypes.Custom
            options_instance.steam_path = linux_steam_path_select(
                common.SteamTypes.LinuxNative
            )

    if not save_path_overwritten:
        override_save_path: bool
        header_win = curses.newwin(2, curses.COLS - 1)
        header_win.addstr(0, 0, f"Detected Save Path: {options_instance.save_path}")
        header_win.addstr(1, 0, "Override?")
        header_win.refresh()
        yes_no_win = curses.newwin(2, 6, 2, 0)
        override_save_path = ui_forge.selection_ui(
            yes_no_win, menus.yes_no, start_line=1
        )

        header_win.clear()
        header_win.refresh()

        if override_save_path:
            options_instance.save_path = save_path_select()

    return options_instance
