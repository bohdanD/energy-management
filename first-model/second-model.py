from pulp import *

period = [str(i) for i in range(0, 24)]

power = [250, 260, 260, 260, 270, 260, 260, 250, 250, 250,
        240, 230, 210, 200, 200, 210, 210, 210, 220, 220, 230, 230, 240, 240]

for j in period:
    i = int(j)
    print(power[i])
cost_list = []

for j in period:
    i = int(j)
    cost_list.append(\
        0.4 if (i >= 23) or (i < 7) else\
        1.5 if (i >= 8) and (i <= 11) else\
        1.5 if (i >= 20) and (i <= 22) else 1.0
    )
#print i, cost_list

costs = dict(zip(period, cost_list))
power_dict = dict(zip(period, power))

prob = LpProblem(name="Power-Cost consumption problem", sense=LpMinimize)
time = LpVariable.dicts("time", period, 0, 1, LpInteger)

prob += lpSum([costs[i] * time[i] * power_dict[i] for i in period]), "Total Cost of Energy"
prob += lpSum([power_dict[i] * time[i] for i in period]) <= 3500, "Max Power"
prob += lpSum([power_dict[i] * time[i] for i in period]) >= 3250, "Min Power"

prob.writeLP("PowerModel.lp")
prob.solve()
print("Status", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", int(v.varValue))

print("Total Cost of Power = ", value(prob.objective))
