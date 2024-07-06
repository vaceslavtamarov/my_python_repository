import csv
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO)

def read_file(filename: str) -> list[dict]:
    """Читает данные из CSV файла и преобразует их в список словарей.

    :param filename: Название файла, содержащего данные.
    :return: Список словарей с данными о домах.
    """
    with open(filename, newline="", encoding="utf-8") as input_file:
        reader = list(csv.DictReader(input_file))

        for row in reader:
            row["floor_count"] = int(row["floor_count"])
            row["heating_value"] = float(row["heating_value"])
            row["area_residential"] = float(row["area_residential"])
            row["population"] = int(row["population"])

    return reader


def classify_house(floor_count: int) -> str:
    """Классифицирует дом на основе количества этажей.

    Проверяет, является ли количество этажей целым числом и положительным значением.
    Возвращает категорию дома в зависимости от количества этажей.

    :param floor_count: Количество этажей в доме.
    :return: Категория дома в виде строки: "Малоэтажный",
                                           "Среднеэтажный" или "Многоэтажный".
    """
    if not isinstance(floor_count, int):
        type_error = "Количество этажей должно быть целым числом."
        raise TypeError(type_error)

    if floor_count <= 0:
        value_error = "Количество этажей должно быть положительным числом."
        raise ValueError(value_error)

    low_rise = 5
    middle_rise = 16
    if 1 <= floor_count <= low_rise:
        return "Малоэтажный"
    if low_rise < floor_count <= middle_rise:
        return "Среднеэтажный"

    return "Многоэтажный"


def get_classify_houses(houses: list[dict]) -> list[str]:
    """Классифицирует дома на основе количества этажей.

    :param houses: Список словарей с данными о домах.
    :return: Список категорий домов.
    """
    return [classify_house(glossary["floor_count"]) for glossary in houses]


def get_count_house_categories(categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество домов в каждой категории.

    :param categories: Список категорий домов.
    :return: Словарь с количеством домов в каждой категории.
    """
    return dict(Counter(categories))


def min_area_residential(houses: list[dict]) -> str:
    """Находит адрес дома с наименьшим средним количеством квадратных метров.

    :param houses: Список словарей с данными о домах.
    :return: Адрес дома с наименьшим средним количеством
                квадратных метров жилой площади на одного жильца.
    """
    house_with_min_area = min(
        houses, key=lambda house: house["area_residential"] / house["population"],
    )
    return house_with_min_area["house_address"]


if __name__ == "__main__":
    data_houses = read_file("housing_data.csv")

    house_categories = get_classify_houses(houses=data_houses)

    count_categories = get_count_house_categories(house_categories)
    logging.info(count_categories)

    coordinate_min_area = min_area_residential(data_houses)
    logging.info(coordinate_min_area)
