import json

import src.const.ps_constants as const
from src.utils.ps_utils import get_type_chart, get_movedex, get_items, get_pokedex, get_learn_sets, get_abilities, \
    save_to_files


def test_print_get_type_chart():
    print(json.dumps(get_type_chart(), indent=4))


def test_print_get_movedex():
    print(json.dumps(get_movedex(), indent=4))


def test_print_get_items():
    print(json.dumps(get_items(), indent=4))


def test_print_get_pokedex():
    print(json.dumps(get_pokedex(), indent=4))


def test_print_get_learn_sets():
    print(json.dumps(get_learn_sets(), indent=4))


def test_print_get_abilities():
    print(json.dumps(get_abilities(), indent=4))


def test_save_to_files(static_data_path):
    pokedex = get_pokedex()
    movedex = get_movedex()
    learn_sets = get_learn_sets()
    abilities = get_abilities()
    type_chart = get_type_chart()
    # items = get_items()

    save_to_files(f'{static_data_path}/replays/static_data/pokedex.json', const.JSON, pokedex)
    save_to_files(f'{static_data_path}/replays/static_data/movedex.json', const.JSON, movedex)
    save_to_files(f'{static_data_path}/replays/static_data/learn_sets.json', const.JSON, learn_sets)
    save_to_files(f'{static_data_path}/replays/static_data/abilities.json', const.JSON, abilities)
    save_to_files(f'{static_data_path}/replays/static_data/type_chart.json', const.JSON, type_chart)
    # save_to_files(f'{static_data_path}/replays/static_data/items.json', const.JSON, items)


def main():
    # test_print_get_pokedex()
    # test_print_get_learn_sets()
    # test_print_get_items()
    # test_print_get_type_chart()
    # test_print_get_movedex()
    # test_print_get_abilities()

    # save static data to files:
    test_save_to_files(
        "/Users/viethnguyen/Documents/CEU_BA_MSc/Data_Engineering_1_ECBS5146/CEU_MSc_BA_ECBS5146_Data_Engineering_1/Term1")


if __name__ == '__main__':
    main()
