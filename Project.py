import cvxpy as cp
import csv

emissions = [280.02516,
304.16526,
299.33724,
268.75978,
358.88282,
273.5878,
188.29278,
185.0741,
57.93624,
291.29054,
289.6812,
426.4751,
428.08444,
399.11632,
432.91246]

profits = [943.907,
1192.968,
1259.77,
1312.37,
2356.217,
1467.277,
1711.867,
1354.976,
1810.229,
1267.66,
1551.7,
2203.94,
1950.934,
1990.384,
2040.88]

import cvxpy as cp

x = cp.Variable(15, integer = True)

obj_func = profits[0]*x[0]+profits[1]*x[1]+profits[2]*x[2]+profits[3]*x[3]+profits[4]*x[4]+profits[5]*x[5]+profits[6]*x[6]+profits[7]*x[7]+profits[8]*x[8]+profits[9]*x[9]+profits[10]*x[10]+profits[11]*x[11]+profits[12]*x[12]+profits[13]*x[13]+profits[14]*x[14]

constraints = []

#Adding the emission constraint

constraints.append(x[0]*(emissions[0]-307)+x[1]*(emissions[1]-307)+x[2]*(emissions[2]-307)+x[3]*(emissions[3]-307)+x[4]*(emissions[4]-307)+x[5]*(emissions[5]-307)+x[6]*(emissions[6]-307)+x[7]*(emissions[7]-307)+x[8]*(emissions[8]-307)+x[9]*(emissions[9]-307)+x[10]*(emissions[10]-307)+x[11]*(emissions[11]-307)+x[12]*(emissions[12]-307)+x[13]*(emissions[13]-307)+x[14]*(emissions[14]-307) <= 307)


#Adding non-negative constraints
for i in range(15):   
    constraints.append(x[i] >= 0)

            
problem = cp.Problem(cp.Maximize(obj_func), constraints)
problem.solve(solver=cp.GUROBI, verbose = True)

print("obj_func =")
print(obj_func.value)
print("x = ")
print(x.value)