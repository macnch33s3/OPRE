from scipy.optimize import linprog


def main():
    c = [-8, -5]

    A = [[2, 1], [3, 4], [1, 1], [1, -1]]

    b = [1000, 2400, 800, 350]

    x0_bounds = (0, None)
    x1_bounds = (0, None)
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method="highs")

    print(res.message)
    print(f"Objective value:\t{res.fun}")
    print(f"Results:\t\t\t{res.x}")


if __name__ == "__main__":
    main()

