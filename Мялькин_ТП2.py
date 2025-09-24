import random
import pandas as pd
import matplotlib.pyplot as plt

L = 30
T = 30
vmax = 5
p = 0.00
Nc = 4
STEP_SECONDS = 1
SEED = 42

CAR_IDS = list(range(1, Nc + 1))
INIT_POS = [1, 6, 12, 20]
assert len(INIT_POS) == Nc

random.seed(SEED)

def gap_ahead(pos_i, all_pos, L):
    best = None
    for pj in all_pos:
        if pj == pos_i:
            continue
        d = (pj - pos_i) % L
        if d > 0 and (best is None or d < best):
            best = d
    if best is None:
        return L - 1
    return best - 1

def step_nasch(pos, spd, L, vmax, p):
    N = len(pos)
    spd_new = [min(v + 1, vmax) for v in spd]
    for i in range(N):
        g = gap_ahead(pos[i], pos, L)
        if spd_new[i] > g:
            spd_new[i] = g
        if spd_new[i] < 0:
            spd_new[i] = 0

    for i in range(N):
        if spd_new[i] > 0 and random.random() < p:
            spd_new[i] -= 1

    pos_new = [None]*N
    crossed_zero = []
    for i in range(N):
        old = pos[i]
        new = (pos[i] + spd_new[i]) % L
        pos_new[i] = new
        if spd_new[i] > 0 and new < old:
            crossed_zero.append(i)
    return pos_new, spd_new, crossed_zero

pos = INIT_POS[:]
spd = [0]*Nc

columns = (
    ["step"]
    + [f"pos_{cid}" for cid in CAR_IDS]
    + [f"v_{cid}" for cid in CAR_IDS]
    + ["crossings", "avg_speed"]
)
rows = []

rows.append([0] + pos[:] + spd[:] + [0, sum(spd)/Nc])

total_cross = 0
avg_speeds = []

for t in range(1, T+1):
    pos, spd, crossed = step_nasch(pos, spd, L, vmax, p)
    c = len(crossed)
    total_cross += c
    v_avg = sum(spd)/Nc
    avg_speeds.append(v_avg)
    rows.append([t] + pos[:] + spd[:] + [c, v_avg])

df = pd.DataFrame(rows, columns=columns)
df.to_csv("nasch_result.csv", index=False, encoding="utf-8-sig")

rho = Nc / L
q_per_step = total_cross / T
q_per_hour = q_per_step * (3600.0 / STEP_SECONDS)

print("=== ИТОГ ===")
print(f"Плотность ρ = {Nc}/{L} = {rho:.3f} авт/клетку")
print(f"Средний поток q = {q_per_step:.3f} авт/шаг  ->  {q_per_hour:.1f} авт/ч")
print(f"Средняя скорость по шагам: {sum(avg_speeds)/len(avg_speeds):.3f} клет/шаг")
print("Таблица сохранена: nasch_result.csv")

plt.figure(figsize=(6,4))
plt.plot(df["step"], df["avg_speed"], marker="o")
plt.xlabel("Шаг")
plt.ylabel("Средняя скорость (клет/шаг)")
plt.title("Средняя скорость по времени")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

plt.figure(figsize=(5,4))
plt.scatter([rho], [q_per_hour], s=90, c="tab:red", label=f"ρ={rho:.2f}, q={q_per_hour:.0f} авт/ч")
plt.xlabel("Плотность ρ (авт/клетку)")
plt.ylabel("Интенсивность q (авт/ч)")
plt.title("Фундаментальная диаграмма (результат эксперимента)")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
