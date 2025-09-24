import random
import math
import pandas as pd
import matplotlib.pyplot as plt

L = 30
T = 30
vmax = 5
p = 0.10
Nc = 13
STEP_SECONDS = 1
SEED = 42

CAR_IDS = list(range(1, Nc + 1))
INIT_POS = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 25]
assert len(INIT_POS) == Nc, "Число стартовых позиций должно совпадать с Nc"

random.seed(SEED)

pos = INIT_POS[:]
spd = [0] * Nc

def distance_ahead(pos_i, pos_all):

    best = None
    for pj in pos_all:
        if pj == pos_i:
            continue
        d = (pj - pos_i) % L
        if d > 0:
            if best is None or d < best:
                best = d
    if best is None:
        return L - 1
    return best - 1

def step_nasch(pos, spd):

    N = len(pos)
    spd_new = [min(v + 1, vmax) for v in spd]

    for i in range(N):
        gap = distance_ahead(pos[i], pos)
        if spd_new[i] > gap:
            spd_new[i] = gap
        if spd_new[i] < 0:
            spd_new[i] = 0

    for i in range(N):
        if spd_new[i] > 0 and random.random() < p:
            spd_new[i] -= 1

    pos_new = [None] * N
    crossed_zero = []
    for i in range(N):
        old = pos[i]
        new = (pos[i] + spd_new[i]) % L
        pos_new[i] = new

        if spd_new[i] > 0 and new < old:
            crossed_zero.append(i)

    return pos_new, spd_new, crossed_zero

columns = ["step"] + [f"pos_{cid}" for cid in CAR_IDS] + [f"v_{cid}" for cid in CAR_IDS] + ["crossings"]
rows = []

row0 = [0] + pos[:] + spd[:] + [0]
rows.append(row0)

total_crossings = 0
avg_speeds_time = []

for t in range(1, T + 1):
    pos, spd, crossed = step_nasch(pos, spd)
    crossings_this_step = len(crossed)
    total_crossings += crossings_this_step
    avg_speed = sum(spd) / Nc
    avg_speeds_time.append(avg_speed)

    # строка таблицы
    row = [t] + pos[:] + spd[:] + [crossings_this_step]
    rows.append(row)

df = pd.DataFrame(rows, columns=columns)

q_per_step = total_crossings / T
q_per_hour = q_per_step * (3600.0 / STEP_SECONDS)

rho = Nc / L

print("=== ИТОГО ===")
print(f"Плотность rho = {Nc}/{L} = {rho:.3f} (авт./клетку)")
print(f"Средний поток q = {q_per_step:.3f} авт./шаг  ->  {q_per_hour:.1f} авт./ч (при {STEP_SECONDS}s/шаг)")
print(f"Средняя скорость по шагам: {sum(avg_speeds_time)/len(avg_speeds_time):.3f} (клеток/шаг)")

df.to_csv("nasch_log.csv", index=False, encoding="utf-8-sig")
print("Таблица сохранена в nasch_log.csv")

plt.figure(figsize=(5, 4))
plt.scatter([rho], [q_per_hour], s=80, c="tab:red", label=f"ρ={rho:.2f}, q={q_per_hour:.0f} авт./ч")
plt.xlabel("Плотность, ρ (авт./клетку)")
plt.ylabel("Интенсивность, q (авт./ч)")
plt.title("Фундаментальная диаграмма (точка по данным симуляции)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
