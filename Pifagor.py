import math


def calculate_distance_haversine(lat1, lon1, lat2, lon2):
    """
    Рассчитывает расстояние между двумя точками на Земле
    по формуле гаверсинусов (самый точный и популярный метод).
    """
    R = 6371.0  # Радиус Земли в километрах

    # Конвертируем градусы в радианы
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Разница координат
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Формула Гаверсинусов
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def calculate_distance_spherical_law_of_cosines(lat1, lon1, lat2, lon2):
    """
    Рассчитывает расстояние между двумя точками на Земле
    по сферической теореме косинусов.
    """
    R = 6371.0  # Радиус Земли в километрах

    # Конвертируем градусы в радианы
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Сферическая теорема косинусов
    distance = R * math.acos(
        math.sin(lat1_rad) * math.sin(lat2_rad) +
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad)
    )

    return distance


def calculate_distance_flat_pythagoras(lat1, lon1, lat2, lon2):
    """
    Приближенный расчет по теореме Пифагора для плоской поверхности.
    Работает только для очень малых расстояний!
    """
    # Средняя широта для расчета долготы
    mid_lat = math.radians((lat1 + lat2) / 2)

    # Длина одного градуса в км
    km_per_degree_lat = 111.0  # Примерно постоянно для широты
    km_per_degree_lon = 111.0 * math.cos(mid_lat)  # Зависит от широты

    # Разница в координатах в километрах
    dx = (lon2 - lon1) * km_per_degree_lon
    dy = (lat2 - lat1) * km_per_degree_lat

    # Теорема Пифагора
    return math.sqrt(dx ** 2 + dy ** 2)


# Тестируем все три метода на разных расстояниях
def test_all_methods(lat1, lon1, lat2, lon2, description):
    """
    Тестирует все три метода расчета для заданных координат
    """
    print(f"\n{description}")
    print(f"Точка A: ({lat1}, {lon1})")
    print(f"Точка B: ({lat2}, {lon2})")

    try:
        dist_haversine = calculate_distance_haversine(lat1, lon1, lat2, lon2)
        dist_cosines = calculate_distance_spherical_law_of_cosines(lat1, lon1, lat2, lon2)
        dist_pythagoras = calculate_distance_flat_pythagoras(lat1, lon1, lat2, lon2)

        print(f"Формула Гаверсинуса:      {dist_haversine:.3f} км")
        print(f"Теорема косинусов:        {dist_cosines:.3f} км")
        print(f"Теорема Пифагора (плоск.): {dist_pythagoras:.3f} км")


    except ValueError as e:
        print(f"Ошибка в расчетах: {e}")
        print("(Может возникать из-за ошибок округления в теореме косинусов)")


# Пример 1: Близкие точки в пределах города
test_all_methods(
    55.78736, 37.609144,  # среднее А
    58.522365, 31.269338,  # среднее Б
    "Среднее точки:"
)

# Пример 2: Среднее расстояние (между городами)
test_all_methods(
    55.857725, 37.422192,  # близко А
    55.857907, 37.420414,  # близко Б
    "Малое расстояние:"
)

# Пример 3: Большое расстояние (между континентами)
test_all_methods(
    55.984722, 122.645172,  # большое А
    66.093328,  -171.079442,  # большое Б
    "Большое расстояние:"
)

