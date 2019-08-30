

def make_matrix():
    matrix = []
    try:
        num_var = int(input("Enter the number of variables: "))
    except ValueError:
        print("Please enter numbers only.")
        exit(0)

    for i in range(1,num_var+1):
        eq_coeffs = []
        for j in range(1,num_var+1):
            try:
                eq_coeffs.append(int(input("Enter the coefficient of variable "+str(j)+" in equation " + str(i)+": ")))
            except ValueError:
                print("Please enter numbers only.")
                exit(0)
        try:
            eq_coeffs.append(int(input("Enter the value of the constant in equation "+str(i)+": ")))
        except ValueError:
            print("Please enter numbers only.")
            exit(0)
        matrix.append(eq_coeffs)
    return matrix


def row_op(mat):
    for i in range(1,len(mat)):                 # For each equation, start with second eq
        first_coeff = mat[i-1][i-1]             # Get coeff of first var
        for j in range(i, len(mat)):                    # Scale all other equations
            coeff_to_cancel = mat[j][i - 1]
            if coeff_to_cancel == 0:
                continue
            elim_n = (-1 * first_coeff) / coeff_to_cancel
            for k in range(len(mat[j])):                            # Scale and cancel all coeffs in each equation
                mat[j][k] = (mat[j][k] * elim_n) + mat[i-1][k]
    return mat


def solve_for(i, nums):
    const = nums[-1]
    ind_of_var = i
    sum = 0
    for n in range(ind_of_var+1, len(nums) - 1):
        sum += nums[n]
    var = (const - sum) / nums[ind_of_var]
    return var


def solve_mat(mat):
    solution = []
    last_var = mat[-1][-2]
    last_const = mat[-1][-1]
    if last_var == 0 and last_const != 0:
        print("\nNo solution.")
        exit(0)
    if last_var == 0 and last_const == 0:
        print("\nMultiple solutions.")
        exit(0)
    solution.append(last_const / last_var)  # Final var value used to find others
    row_len = len(mat[0])
    for i in range(len(mat)-1,0, -1):           # Bottom up
        for j in range(1,len(solution)):      # Fill in all known vars
            mat[i-1][row_len-j-1] *= solution[j]
        solution.insert(0, solve_for(row_len - len(solution)-1, mat[i]))
    return solution


def display_solution(sol):
    print("\n")
    for i in range(len(sol)):
        print("\nThe value of x", i+1, " is: ", round(sol[i], 5), sep='')


def main():
    matr = make_matrix()
    display_solution(solve_mat(row_op(matr)))


if __name__ == '__main__':
    main()
