from scipy.optimize import linprog

def main():
     c = [-1, -1]

     A = [[800, 400],
          [ -1,   0],
          [  0,  -1],
          [  2,  -1]]

     b = [200000,
          -100,
          -200,
               0]

     x0_bounds = (0, None)
     x1_bounds = (0, None)
     res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')

     print(res.message)
     print(f"Objective value:\t{res.fun}")
     print(f"Results:\t\t\t{res.x}")


if __name__ == "__main__":
    main()