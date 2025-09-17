import math

def distances(lat1, lon1, lat2, lon2):
    # Перевод в радианы
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    R = 6371.0088
    dlat, dlon = lat2 - lat1, lon2 - lon1

    # Пифагор
    dx = R * math.cos((lat1 + lat2) / 2) * dlon
    dy = R * dlat
    d_pif = math.sqrt(dx**2 + dy**2)

    # Косинусы
    cos_d = (math.sin(lat1) * math.sin(lat2) +
             math.cos(lat1) * math.cos(lat2) * math.cos(dlon))
    d_cos = R * math.acos(cos_d)

    # Haversine
    hav = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    d_hav = R * 2 * math.asin(math.sqrt(hav))

    return d_pif, d_cos, d_hav


# --- Координаты ---
pairs = [
    (55.787386, 37.609144, 58.522365, 31.269338),
    (55.851725, 37.422192, 55.857907, 37.420114),
    (55.984722, 122.645172, 66.093328, -171.079442)]

for i, (lat1, lon1, lat2, lon2) in enumerate(pairs, 1):
    d_pif, d_cos, d_hav = distances(lat1, lon1, lat2, lon2)
    print(f"\nКоордината {i}:")
    print(f"  По Пифагору   = {d_pif:.3f} км")
    print(f"  По косинусам  = {d_cos:.3f} км")
    print(f"  Haversine     = {d_hav:.3f} км")