from typing import Dict, Any, List, Optional
import copy
from pathlib import Path
from ccsm.sav_ops import loader
from SavConverter import json_to_sav
import json

key_conversion = {
    "Save": "AutoSave",
    "Skin": "CrabSkin",
    "SelectedWeapon": "WeaponDA",
    "SelectedAbility": "AbilityDA",
    "SelectedMelee": "MeleeDA",
}


def find_index_from_name(base: List[Dict[Any, Any]], name: str) -> Optional[int]:
    for i, item in enumerate(base):
        if name in key_conversion.keys():
            name = key_conversion[name]
        if item.get("name") == name:
            return i


def generate_gvas_ranked_weapons(
    neocrab: Dict[str, Dict[str, str]]
) -> List[List[Dict[str, str]]]:
    gvas_ranked_weapons = []
    for cat, ranked in neocrab.items():
        for item, rank in ranked.items():
            gvas_ranked_weapons.append(
                [
                    {
                        "type": "ObjectProperty",
                        "name": "Weapon",
                        "value": f"/Game/Blueprint/Weapon/{item}/DA_{cat}_{item}.DA_{cat}_{item}",
                    },
                    {
                        "type": "EnumProperty",
                        "name": "Rank",
                        "enum": "ECrabRank",
                        "value": f"ECrabRank::{rank}",
                    },
                    {"type": "NoneProperty"},
                ]
            )
    return gvas_ranked_weapons


def merge_challenges(neocrab: Dict[Any, Any], base: List[Any]):
    for challenge in base:
        if neocrab_data := neocrab.get(challenge[0]["value"][4:]):
            challenge[1]["value"] = neocrab_data["Description"]
            challenge[2]["value"] = neocrab_data["Progress"]
            challenge[3]["value"] = neocrab_data["Goal"]
            challenge[4]["value"] = neocrab_data["Completed"]
            challenge[5]["value"][0]["value"] = neocrab_data["Reward"]["Type"]
            name = neocrab_data["Reward"]["Name"]
            challenge[5]["value"][1]["value"] = name
            challenge[5]["value"][2][
                "value"
            ] = f"/Game/UI/Thumbnail/T_Thumbnail_{name}.T_Thumbnail_{name}"
            challenge[5]["value"][3][
                "value"
            ] = f"/Game/Character/Crab/Texture/Default/MI_Crab_{name}.MI_Crab_{name}"


def generate_unlocked_weapons(weapons: List[str]) -> List[str]:
    unlocked_weapons = []
    for weapon in weapons:
        unlocked_weapons.append(
            f"/Game/Blueprint/Weapon/{weapon}/DA_Weapon_{weapon}.DA_Weapon_{weapon}"
        )
    return unlocked_weapons


def generate_unlocked_abilities(abilities: List[str]) -> List[str]:
    unlocked_abilities = []
    for ability in abilities:
        unlocked_abilities.append(
            f"/Game/Blueprint/Weapon/{ability}/DA_Weapon_{ability}.DA_Weapon_{ability}"
        )
    return unlocked_abilities


def generate_unlocked_melees(melees: List[str]) -> List[str]:
    unlocked_melees = []
    for weapon in melees:
        unlocked_melees.append(
            f"/Game/Blueprint/Weapon/{weapon}/DA_Weapon_{weapon}.DA_Weapon_{weapon}"
        )
    return unlocked_melees


def generate_unlocked_weapon_mods(mods: Dict[str, str]) -> List[str]:
    unlocked_weapon_mods = []
    for mod, rarity in mods.items():
        unlocked_weapon_mods.append(
            f"/Game/Blueprint/Pickup/WeaponMod/{rarity}/DA_WeaponMod_{mod}.DA_WeaponMod_{mod}"
        )
    return unlocked_weapon_mods


def generate_unlocked_ability_mods(mods: Dict[str, str]) -> List[str]:
    unlocked_ability_mods = []
    for mod, rarity in mods.items():
        unlocked_ability_mods.append(
            f"/Game/Blueprint/Pickup/AbilityMod/{rarity}/DA_AbilityMod_{mod}.DA_AbilityMod_{mod}"
        )
    return unlocked_ability_mods


def generate_unlocked_melee_mods(mods: Dict[str, str]) -> List[str]:
    unlocked_melee_mods = []
    for mod, rarity in mods.items():
        unlocked_melee_mods.append(
            f"/Game/Blueprint/Pickup/MeleeMod/{rarity}/DA_MeleeMod_{mod}.DA_MeleeMod_{mod}"
        )
    return unlocked_melee_mods


def generate_unlocked_perks(perks: Dict[str, str]) -> List[str]:
    unlocked_perks = []
    for mod, rarity in perks.items():
        unlocked_perks.append(
            f"/Game/Blueprint/Pickup/Perk/{rarity}/DA_Perk_{mod}.DA_Perk_{mod}"
        )
    return unlocked_perks


def generate_unlocked_relics(relics: Dict[str, str]) -> List[str]:
    unlocked_relics = []
    for mod, rarity in relics.items():
        unlocked_relics.append(
            f"/Game/Blueprint/Pickup/Relic/{rarity}/DA_Relic_{mod}.DA_Relic_{mod}"
        )
    return unlocked_relics


def merge_next_island_info(neocrab: Dict[str, Any], base: List[Dict[Any, Any]]):
    base[0]["value"] = f"ECrabBiome::{neocrab["Biome"]}"
    base[1]["value"] = neocrab["CurrentIsland"]
    base[2]["value"] = neocrab["IslandName"]
    base[3]["value"] = f"ECrabIslandType::{neocrab["IslandType"]}"


def generate_health_info(neocrab: Dict[str, Any]) -> List[Dict[Any, Any]]:
    return [
        {
            "type": "IntProperty",
            "name": "CurrentArmorPlates",
            "value": neocrab["CurrentArmorPlates"],
        },
        {
            "type": "FloatProperty",
            "name": "CurrentArmorPlateHealth",
            "value": neocrab["CurrentArmorPlateHealth"],
        },
        {
            "type": "FloatProperty",
            "name": "PreviousArmorPlateHealth",
            "value": neocrab["PreviousArmorPlateHealth"],
        },
        {
            "type": "FloatProperty",
            "name": "CurrentHealth",
            "value": neocrab["CurrentHealth"],
        },
        {
            "type": "FloatProperty",
            "name": "CurrentMaxHealth",
            "value": neocrab["CurrentMaxHealth"],
        },
        {
            "type": "FloatProperty",
            "name": "PreviousHealth",
            "value": neocrab["PreviousHealth"],
        },
        {
            "type": "FloatProperty",
            "name": "PreviousMaxHealth",
            "value": neocrab["PreviousMaxHealth"],
        },
        {"type": "NoneProperty"},
    ]


def parse_enhancements(neocrab: List[str]) -> List[str]:
    enhancements = []
    for enhancement in neocrab:
        enhancements.append(f"ECrabEnhancementType::{enhancement}")
    return enhancements


def generate_weapon_mods(
    neocrab: Dict[str, Dict[str, Any]], unlocked_weapon_mods: Dict[str, str]
) -> List[List[Dict[Any, Any]]]:
    weapon_mods = []
    for mod, values in neocrab.items():
        weapon_mods.append(
            [
                {
                    "type": "ObjectProperty",
                    "name": "WeaponModDA",
                    "value": f"/Game/Blueprint/Pickup/WeaponMod/{unlocked_weapon_mods[mod]}/DA_WeaponMod_{mod}.DA_WeaponMod_{mod}",
                },
                {
                    "type": "StructProperty",
                    "name": "InventoryInfo",
                    "subtype": "CrabInventoryInfo",
                    "value": [
                        {
                            "type": "ByteProperty",
                            "name": "Level",
                            "subtype": "None",
                            "value": values["Level"],
                        },
                        {
                            "type": "ArrayProperty",
                            "name": "Enhancements",
                            "subtype": "EnumProperty",
                            "value": parse_enhancements(values["Enhancements"]),
                        },
                        {
                            "type": "FloatProperty",
                            "name": "AccumulatedBuff",
                            "value": values["AccumulatedBuff"],
                        },
                        {"type": "NoneProperty"},
                    ],
                },
                {"type": "NoneProperty"},
            ]
        )
    return weapon_mods


def generate_ability_mods(
    neocrab: Dict[str, Dict[str, Any]], unlocked_ability_mods: Dict[str, str]
) -> List[List[Dict[Any, Any]]]:
    ability_mods = []
    for mod, values in neocrab.items():
        ability_mods.append(
            [
                {
                    "type": "ObjectProperty",
                    "name": "AbilityModDA",
                    "value": f"/Game/Blueprint/Pickup/AbilityMod/{unlocked_ability_mods[mod]}/DA_AbilityMod_{mod}.DA_AbilityMod_{mod}",
                },
                {
                    "type": "StructProperty",
                    "name": "InventoryInfo",
                    "subtype": "CrabInventoryInfo",
                    "value": [
                        {
                            "type": "ByteProperty",
                            "name": "Level",
                            "subtype": "None",
                            "value": values["Level"],
                        },
                        {
                            "type": "ArrayProperty",
                            "name": "Enhancements",
                            "subtype": "EnumProperty",
                            "value": parse_enhancements(values["Enhancements"]),
                        },
                        {
                            "type": "FloatProperty",
                            "name": "AccumulatedBuff",
                            "value": values["AccumulatedBuff"],
                        },
                        {"type": "NoneProperty"},
                    ],
                },
                {"type": "NoneProperty"},
            ]
        )
    return ability_mods


def generate_melee_mods(
    neocrab: Dict[str, Dict[str, Any]], unlocked_melee_mods: Dict[str, str]
) -> List[List[Dict[Any, Any]]]:
    melee_mods = []
    for mod, values in neocrab.items():
        melee_mods.append(
            [
                {
                    "type": "ObjectProperty",
                    "name": "MeleeModDA",
                    "value": f"/Game/Blueprint/Pickup/MeleeMod/{unlocked_melee_mods[mod]}/DA_MeleeMod_{mod}.DA_MeleeMod_{mod}",
                },
                {
                    "type": "StructProperty",
                    "name": "InventoryInfo",
                    "subtype": "CrabInventoryInfo",
                    "value": [
                        {
                            "type": "ByteProperty",
                            "name": "Level",
                            "subtype": "None",
                            "value": values["Level"],
                        },
                        {
                            "type": "ArrayProperty",
                            "name": "Enhancements",
                            "subtype": "EnumProperty",
                            "value": parse_enhancements(values["Enhancements"]),
                        },
                        {
                            "type": "FloatProperty",
                            "name": "AccumulatedBuff",
                            "value": values["AccumulatedBuff"],
                        },
                        {"type": "NoneProperty"},
                    ],
                },
                {"type": "NoneProperty"},
            ]
        )
    return melee_mods


def generate_perks(
    neocrab: Dict[str, Dict[str, Any]], unlocked_perks: Dict[str, str]
) -> List[List[Dict[Any, Any]]]:
    perks = []
    for mod, values in neocrab.items():
        perks.append(
            [
                {
                    "type": "ObjectProperty",
                    "name": "PerkDA",
                    "value": f"/Game/Blueprint/Pickup/Perk/{unlocked_perks[mod]}/DA_Perk_{mod}.DA_Perk_{mod}",
                },
                {
                    "type": "StructProperty",
                    "name": "InventoryInfo",
                    "subtype": "CrabInventoryInfo",
                    "value": [
                        {
                            "type": "ByteProperty",
                            "name": "Level",
                            "subtype": "None",
                            "value": values["Level"],
                        },
                        {
                            "type": "ArrayProperty",
                            "name": "Enhancements",
                            "subtype": "EnumProperty",
                            "value": parse_enhancements(values["Enhancements"]),
                        },
                        {
                            "type": "FloatProperty",
                            "name": "AccumulatedBuff",
                            "value": values["AccumulatedBuff"],
                        },
                        {"type": "NoneProperty"},
                    ],
                },
                {"type": "NoneProperty"},
            ]
        )
    return perks


def merge_autosave(
    neocrab: Dict[str, Any],
    base: List[Dict[Any, Any]],
    unlocked_weapon_mods: Dict[str, str],
    unlocked_ability_mods: Dict[str, str],
    unlocked_melee_mods: Dict[str, str],
    unlocked_perks: Dict[str, str],
):
    for key, value in neocrab.items():
        if index := find_index_from_name(base, key):
            if key == "NextIslandInfo":
                merge_next_island_info(value, base[index]["value"])
            elif key == "HealthInfo":
                base[index]["value"] = generate_health_info(value)
            elif key == "WeaponMods":
                base[index]["value"] = generate_weapon_mods(value, unlocked_weapon_mods)
            elif key == "AbilityMods":
                base[index]["value"] = generate_ability_mods(
                    value, unlocked_ability_mods
                )
            elif key == "MeleeMods":
                base[index]["value"] = generate_melee_mods(value, unlocked_melee_mods)
            elif key == "Perks":
                base[index]["value"] = generate_perks(value, unlocked_perks)
            else:
                base[index]["value"] = value


def neocrab_to_save(
    neocrab: Dict[str, Any], base: List[Dict[Any, Any]]
) -> List[Dict[Any, Any]]:
    base = copy.deepcopy(base)
    for key, value in neocrab.items():
        if index := find_index_from_name(base, key):
            if key == "RankedWeapons":
                base[index]["value"] = generate_gvas_ranked_weapons(value)
            elif key == "Skin":
                base[index][
                    "value"
                ] = f"/Game/Character/Crab/Texture/SkinPrototype/MI_{value}.MI_{value}"
            elif key == "SelectedWeapon":
                base[index][
                    "value"
                ] = f"/Game/Blueprint/Weapon/{value}/DA_Weapon_{value}.DA_Weapon_{value}"
            elif key == "SelectedAbility":
                base[index][
                    "value"
                ] = f"/Game/Blueprint/Ability/DA_Ability_{value}.DA_Ability_{value}"
            elif key == "SelectedMelee":
                base[index][
                    "value"
                ] = f"/Game/Blueprint/Melee/DA_Melee_{value}.DA_Melee_{value}"
            elif key == "Challenges":
                merge_challenges(value, base[index]["value"])
            elif key == "UnlockedWeapons":
                base[index]["value"] = generate_unlocked_weapons(value)
            elif key == "UnlockedAbilities":
                base[index]["value"] = generate_unlocked_abilities(value)
            elif key == "UnlockedMeleeWeapons":
                base[index]["value"] = generate_unlocked_melees(value)
            elif key == "UnlockedWeaponMods":
                base[index]["value"] = generate_unlocked_weapon_mods(value)
            elif key == "UnlockedAbilityMods":
                base[index]["value"] = generate_unlocked_ability_mods(value)
            elif key == "UnlockedMeleeMods":
                base[index]["value"] = generate_unlocked_melee_mods(value)
            elif key == "UnlockedPerks":
                base[index]["value"] = generate_unlocked_perks(value)
            elif key == "UnlockedRelics":
                base[index]["value"] = generate_unlocked_relics(value)
            elif key == "Save":
                merge_autosave(
                    value,
                    base[index]["value"],
                    neocrab["UnlockedWeaponMods"],
                    neocrab["UnlockedAbilityMods"],
                    neocrab["UnlockedMeleeMods"],
                    neocrab["UnlockedPerks"],
                )
            else:
                base[index]["value"] = value
    return base


sav_path = Path(
    "/home/cj/.local/share/Steam/steamapps/compatdata/774801/pfx/drive_c/users/steamuser/AppData/Local/CrabChampions/Saved/SaveGames/SaveSlot.sav"
)
sav = loader.load(sav_path)
base = json.loads(Path("./testing.json").read_text())
neocrab = json.loads(Path("./testing_.json").read_text())

gvas = neocrab_to_save(neocrab, base)

Path("testing__.json").write_text(json.dumps(gvas, indent=2))
# sav_path.write_bytes(json_to_sav(gvas))
