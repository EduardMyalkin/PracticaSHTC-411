import math


def calculate_distance_haversine(lat1, lon1, lat2, lon2):

    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def calculate_distance_spherical_law_of_cosines(lat1, lon1, lat2, lon2):

    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    distance = R * math.acos(math.sin(lat1_rad) * math.sin(lat2_rad) +
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad))

    return distance


def calculate_distance_flat_pythagoras(lat1, lon1, lat2, lon2):

    mid_lat = math.radians((lat1 + lat2) / 2)

    km_per_degree_lat = 111.0
    km_per_degree_lon = 111.0 * math.cos(mid_lat)

    dx = (lon2 - lon1) * km_per_degree_lon
    dy = (lat2 - lat1) * km_per_degree_lat

    return math.sqrt(dx ** 2 + dy ** 2)


def test_all_methods(lat1, lon1, lat2, lon2, description):

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


test_all_methods(
    55.78736, 37.609144,  # среднее А
    58.522365, 31.269338,  # среднее Б
    "Среднее точки:")

test_all_methods(
    55.857725, 37.422192,  # близко А
    55.857907, 37.420414,  # близко Б
    "Малое расстояние:")

test_all_methods(
    55.984722, 122.645172,  # большое А
    66.093328,  -171.079442,  # большое Б
    "Большое расстояние:")

