import cvxpy as cp
import numpy as np
import csv

emissions = []
profits = []
with open('HondaEmissions.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emissions.append(row['g/mi'])
        profits.append(row['Estimated Profit'])

sales = []

with open('HondaSales.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emissions.append(row['units sold in 2022'])


x = cp.Variable(len(emissions), integer = True)

#obj_func = profits[0]*x[0]+profits[1]*x[1]+profits[2]*x[2]+profits[3]*x[3]+profits[4]*x[4]+profits[5]*x[5]+profits[6]*x[6]+profits[7]*x[7]+profits[8]*x[8]+profits[9]*x[9]+profits[10]*x[10]+profits[11]*x[11]+profits[12]*x[12]+profits[13]*x[13]+profits[14]*x[14]
obj_func = cp.sum([profits[i]*x[i] for i in range(len(profits))])
print(obj_func)
constraints = []


#Adding the emission constraint
constraints.append(np.multiply(np.array(emissions).astype(float) - 307.0,x) <= 307)
#constraints.append(cp.sum([(emissions[i]-307)*x[i] for i in range(len(emissions))]) <= 307)
#Adding the sales constraint



#Adding non-negative constraints
for i in range(15):   
    constraints.append(x[i] >= 0)

            
problem = cp.Problem(cp.Maximize(obj_func), constraints)
problem.solve(solver=cp.GUROBI, verbose = True)

print("obj_func =")
print(obj_func.value)
print("x = ")
print(x.value)