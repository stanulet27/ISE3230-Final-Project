import cvxpy as cp
import numpy as np
import csv

#the total expected demand for these vehicles
totalExpectedSales = 696067

#emissions per car
emissions = []
#profits per car
profits = []
# number of units sold in 2022 per car
sales = []

with open('HondaEmissions.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emissions.append(row['g/mi'])
        profits.append(row['Estimated Profit'])

with open('HondaSales.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sales.append(row['min cars'])


x = cp.Variable(len(emissions), integer = True)


obj_func = cp.sum([profits[i]*x[i] for i in range(len(profits))])

constraints = []

#Adding the emission constraint
constraints.append(np.multiply(np.array(emissions).astype(float) - 307.0,x) <= 0)

#Adding the sales constraint
constraints.append(x[0] + x[1] + x[2] + x[3] >= sales[0]) #all civics
constraints.append(x[4] + x[5] >= sales[1])#all accords

#all other cars are single
for i in range(len(sales) -2):
    constraints.append(x[i+6] >= sales[i+2])

# bound total sales to expected number
constraints.append(cp.sum([x[i] for i in range(len(profits))]) <= totalExpectedSales)

#Adding non-negative constraints
for i in range(len(emissions)):   
    constraints.append(x[i] >= 0)

            
problem = cp.Problem(cp.Maximize(obj_func), constraints)
problem.solve(solver=cp.GUROBI, verbose = True)

print("obj_func =")
print(obj_func.value)
print("x = ")
print(x.value)