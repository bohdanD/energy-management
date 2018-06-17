from pulp import *
# constants
T_Max = 23
T_Min = 19
e_koef = 0.9
K_koef = 0.0094

T_outside = [0, 1, 2, 2, 2, 2, 0, -1, -1, -2, -3, -4, -5, -5, -5, -6, -6, -5, -5, -2, -2, -1, 0, 0]
T_inside = [21]
power = []
temp_lose_list = []
multiplyer = 1.5

def calculate_temp(power_arg, temp_lose, temp):
    return temp + temp_lose + power_arg * e_koef

def check_bounds(power_arg, temp_arg, current_temp, temp_lose):
    if temp_arg > T_Max:
        power_arg = power_arg / multiplyer
        temp_arg = calculate_temp(power_arg, temp_lose, current_temp)
        return check_bounds(power_arg, temp_arg, current_temp, temp_lose)
    else:
        return power_arg, temp_arg

def calculate_power_bound(temp_indicator):
    power_sum = 0
    for i in range(0, 23):
        lose = K_koef * (T_outside[i] - temp_indicator)
        current_power = abs(lose / e_koef)
        power_sum += current_power
    return power_sum

min_power = int(calculate_power_bound(T_Min) * 1000)
max_power = int(calculate_power_bound(T_Max) * 1000)

print(f'min power:{min_power}')
print(f'max_power:{max_power}')


for i in range(0, 23):
    temprature_lose = K_koef * (T_outside[i] - T_inside[i])
    current_power = abs(temprature_lose / e_koef * multiplyer) #make it hoter
    current_temp = calculate_temp(current_power, temprature_lose, T_inside[i])
    result = check_bounds(current_power, current_temp, T_inside[i], temprature_lose)
    current_power = result[0]
    current_temp = result[1]
    T_inside.append(current_temp)
    power.append(int(current_power * 1000))
    temp_lose_list.append(abs(temprature_lose))

power.append(power[0])

print('temp diference')
for i in range(0, 23):
    print(T_outside[i])

period = [str(i) for i in range(0, 24)]

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
prob += lpSum([power_dict[i] * time[i] for i in period]) <= max_power, "Max Power"
prob += lpSum([power_dict[i] * time[i] for i in period]) >= min_power, "Min Power"

prob.writeLP("PowerModel.lp")
prob.solve()
print("Status", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", int(v.varValue))

print("Total Cost of Power = ", value(prob.objective))
