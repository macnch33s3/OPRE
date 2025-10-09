from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np

def main():
     # reference see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
     c = [1, 1, 1, 1, 1, 1]

     A = [[-1,-1, 0, 0, 0, 0],
          [-1,-1, 0, 0, 0,-1],
          [ 0, 0,-1,-1, 0, 0],
          [ 0, 0,-1,-1,-1, 0],
          [ 0, 0, 0,-1,-1,-1],
          [ 0,-1, 0, 0,-1,-1]]

     b = [-1,-1,-1,-1,-1,-1]

     # 0 : Continuous, 1 : Integer, 2 : Semi-continuous, 3 : Semi-integer variable
     integrality = [1, 1, 1, 1, 1, 1]
     bounds = Bounds(lb=[0, 0, 0, 0, 0, 0],
                    ub=[1, 1, 1, 1, 1, 1])
     b_l = np.full_like(b, -np.inf, dtype=float)
     constraints = LinearConstraint(A=A, lb=b_l, ub=b)
     options = {'disp': False, 'time_limit': 1000}
     res = milp(c=c, integrality=integrality, bounds=bounds, constraints=constraints, options=options)

     print(res.message)
     print(f"Objective value:\t{res.fun}")
     print(f"Results:\t\t\t{res.x}")

if __name__ == "__main__":
    main()
    