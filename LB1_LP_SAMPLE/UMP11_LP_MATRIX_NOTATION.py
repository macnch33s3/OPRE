from scipy.optimize import linprog

def main():
    c = [200, 450]

    A = [[-7000, -4000],
        [-2000, -8000]]

    b = [-2100000,
        -2800000]

    x0_bounds = (0, None)
    x1_bounds = (0, None)
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')
    print(res.message)
    print(f"Objective value:\t{res.fun}")
    print(f"Results:\t\t\t{res.x}")

if __name__ == "__main__":
    main()
    