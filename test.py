from pulp import *
period = [str(i) for i in range(0, 24)]
power = 210  # default value
cost_list = []
for j in period:
    i = int(j)
    cost_list.append(
        0.4 if (i >= 23) or (i < 7) else
        1.5 if (i >= 8) and (i <= 11) else
        1.5 if (i >= 20) and (i <= 22) else 1.0)
# print i, cost_list[i]
costs = dict(zip(period, cost_list))
prob = LpProblem(name="Power-Cost consumtion problem", sense=LpMinimize)
time = LpVariable.dicts("time", period, 0, 2, LpInteger)
prob += lpSum([costs[i] * time[i] * power for i in period]
              ), "Total Cost of Energy"
prob += lpSum([power * time[i] for i in period]) <= 7000, "Max Power"
prob += lpSum([power * time[i] for i in period]) >= 6500, "Min Power"
prob.writeLP("PowerModel.lp")
prob.solve()
print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", int(v.varValue))
print("Total Cost of Power = ", value(prob.objective))
