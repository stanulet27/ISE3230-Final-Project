import cvxpy as cp
import numpy as np
import csv

#the total expected demand for these vehicles
totalExpectedSales = 969067

#emissions per car
emissions = []
#profits per car
profits = []
# 90% of units sold in 2022
minSales = []
# 200% of units sold in 2022
maxSales = []

with open('HondaEmissions.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emissions.append(row['g/mi'])
        profits.append(row['Estimated Profit'])

with open('HondaSales.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        minSales.append(row['min cars'])
        maxSales.append(row['max cars'])


x = cp.Variable(len(emissions), integer = True)


obj_func = cp.sum([profits[i]*x[i] for i in range(len(profits))])

constraints = []

#Adding the emission constraint
constraints.append(np.multiply(np.array(emissions).astype(float) - (307.0 * .925),x) <= 0)

#Adding the minSales constraint
constraints.append(x[0] + x[1] + x[2] + x[3] >= minSales[0]) #all civics
constraints.append(x[4] + x[5] >= minSales[1])#all accords

#all other cars are single
for i in range(len(minSales) -2):
    constraints.append(x[i+6] >= minSales[i+2])

# bound total minSales to expected number
constraints.append(cp.sum([x[i] for i in range(len(profits))]) <= totalExpectedSales)

#add constraint disallowing more than 2x in sales
constraints.append(x[0] + x[1] + x[2] + x[3] <=  maxSales[0]) #all civics
constraints.append(x[4] + x[5] <=  maxSales[1])#all accords

#all other cars are single
for i in range(len(maxSales) -2):
    constraints.append(x[i+6] <= maxSales[i+2])

#Adding non-negative constraints
for i in range(len(emissions)):   
    constraints.append(x[i] >= 0)

            
problem = cp.Problem(cp.Maximize(obj_func), constraints)
problem.solve(solver=cp.GUROBI, verbose = True)

print("obj_func =" , obj_func.value)
print("x = " , x.value)
