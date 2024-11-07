from typing import Any, Dict, List


def _remove_colon_prefix(string: str) -> str:
    return string.split("::")[1]


def _remove_path_prefix(weapon_path: str) -> str:
    return weapon_path.split(".")[-1][3:]


def _parse_ranked_weapons(ranked_weapons: List[Any]) -> Dict[str, Any]:
    new_ranked_weapons = {}
    new_ranked_weapons["Weapon"] = {}
    new_ranked_weapons["Melee"] = {}
    new_ranked_weapons["Ability"] = {}
    for weapon in ranked_weapons:
        name_data = _remove_path_prefix(weapon[0]["value"]).split("_")
        type_data = name_data[0]
        name_data = name_data[1]
        rank_data = weapon[1]["value"]
        new_ranked_weapons[type_data][name_data] = _remove_colon_prefix(rank_data)

    return new_ranked_weapons


def _parse_reward(reward: List[Dict[str, str]]):
    type_data = _remove_colon_prefix(reward[0]["value"])
    name_data = reward[1]["value"]
    return {"Type": type_data, "Name": name_data}


def _parse_challenges(challenges: List[Any]) -> Dict[str, Any]:
    new_challenges = {}
    for challenge in challenges:
        id_data = challenge[0]["value"][4:]
        description_data = challenge[1]["value"]
        progress_data = challenge[2]["value"]
        goal_data = challenge[3]["value"]
        completed_data = challenge[4]["value"]
        reward_data = _parse_reward(challenge[5]["value"])
        new_challenges[id_data] = {
            "Description": description_data,
            "Progress": progress_data,
            "Goal": goal_data,
            "Completed": completed_data,
            "Reward": reward_data,
        }

    return new_challenges


def _parse_mods(mods: List[str]) -> Dict[str, str]:
    new_mods = {}
    for mod in mods:
        new_mods[_remove_path_prefix(mod).split("_")[1]] = mod.split("/")[5]
    return new_mods


def _parse_general_list(l: List[Any]) -> List[Any]:  # noqa: E741
    new_list = []
    for item in l:
        new_list.append(_remove_path_prefix(item).split("_")[1])
    return new_list


def _convert_next_island(next_island: List[Dict[Any, Any]]) -> Dict[str, Any]:
    new_next_island_dict = {}
    for item in next_island:
        if name := item.get("name"):
            value = item.get("value")
            if name == "Biome" or name == "IslandType":
                new_next_island_dict[name] = _remove_colon_prefix(str(value))
            else:
                new_next_island_dict[name] = value
    return new_next_island_dict


def _parse_enhancements(enhancements: List[str]) -> List[str]:
    new_enhancements = []
    for enhancement in enhancements:
        new_enhancements.append(_remove_colon_prefix(enhancement))
    return new_enhancements


def _convert_mods(mods: List[Dict[Any, Any]]) -> Dict[str, Any]:
    new_mods = {}
    for mod in mods:
        if mod[0]["value"] == "None":
            continue
        name_data = _remove_path_prefix(mod[0]["value"]).split("_")[1]
        inventory_data = mod[1]["value"]
        level_data = inventory_data[0]["value"]
        enhancements_data = _parse_enhancements(inventory_data[1]["value"])
        accumulated_buff_data = inventory_data[2]["value"]
        new_mods[name_data] = {
            "Level": level_data,
            "Enhancements": enhancements_data,
            "AccumulatedBuff": accumulated_buff_data,
        }
    return new_mods


def _convert_health_info(health_info: List[Dict[Any, Any]]) -> Dict[str, Any]:
    new_health_info = {}
    for info in health_info:
        if name := info.get("name"):
            value = info.get("value")
            new_health_info[name] = value
    return new_health_info


def _convert_auto_save(save: List[Dict[Any, Any]]) -> Dict[str, Any]:
    new_save_dict = {}
    for item in save:
        if name := item.get("name"):
            value = item.get("value")
            if isinstance(value, list):
                if name == "NextIslandInfo":
                    new_save_dict[name] = _convert_next_island(value)
                elif name == "HealthInfo":
                    new_save_dict[name] = _convert_health_info(value)
                elif (
                    name == "WeaponMods"
                    or name == "AbilityMods"
                    or name == "MeleeMods"
                    or name == "Perks"
                    or name == "Relics"
                ):
                    new_save_dict[name] = _convert_mods(value)
                else:
                    new_save_dict[name] = value
            else:
                if name == "Difficulty":
                    new_save_dict[name] = _remove_colon_prefix(str(value))
                elif name == "CrabSkin":
                    new_save_dict[name] = _remove_path_prefix(str(value)).split("_")[1]
                elif name == "WeaponDA":
                    new_save_dict["SelectedWeapon"] = _remove_path_prefix(
                        str(value)
                    ).split("Weapon_")[1]
                elif name == "AbilityDA":
                    new_save_dict["SelectedAbility"] = _remove_path_prefix(
                        str(value)
                    ).split("Ability_")[1]
                elif name == "MeleeDA":
                    new_save_dict["SelectedMelee"] = _remove_path_prefix(
                        str(value)
                    ).split("Melee_")[1]
                else:
                    new_save_dict[name] = value
    return new_save_dict


def to_neocrab(save: List[Dict[Any, Any]]) -> Dict[str, Any]:
    new_save_dict = {}
    for item in save:
        if name := item.get("name"):
            value = item.get("value")
            if isinstance(value, list):
                if name == "RankedWeapons":
                    new_save_dict[name] = _parse_ranked_weapons(value)
                elif name == "Challenges":
                    new_save_dict[name] = _parse_challenges(value)
                elif (
                    name == "UnlockedWeaponMods"
                    or name == "UnlockedAbilityMods"
                    or name == "UnlockedMeleeMods"
                    or name == "UnlockedPerks"
                    or name == "UnlockedRelics"
                ):
                    new_save_dict[name] = _parse_mods(value)
                elif name == "AutoSave":
                    new_save_dict[name] = _convert_auto_save(value)
                else:
                    new_save_dict[name] = _parse_general_list(value)
            else:
                if name == "Difficulty":
                    new_save_dict[name] = _remove_colon_prefix(str(value))
                elif name == "CrabSkin":
                    new_save_dict[name] = _remove_path_prefix(str(value))
                elif name == "WeaponDA":
                    new_save_dict["SelectedWeapon"] = _remove_path_prefix(
                        str(value)
                    ).split("Weapon_")[1]
                elif name == "AbilityDA":
                    new_save_dict["SelectedAbility"] = _remove_path_prefix(
                        str(value)
                    ).split("Ability_")[1]
                elif name == "MeleeDA":
                    new_save_dict["SelectedMelee"] = _remove_path_prefix(
                        str(value)
                    ).split("Melee_")[1]
                else:
                    new_save_dict[name] = value
    if new_save_dict.get("Difficulty") is None:
        new_save_dict["Difficulty"] = "Normal"
        if new_save_dict.get("Save"):
            new_save_dict["Save"]["Difficulty"] = "Normal"
    return new_save_dict
