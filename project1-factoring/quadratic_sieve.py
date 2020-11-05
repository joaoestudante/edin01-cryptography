import math
import os
import time

def prime_factorization(n): # TODO: use something homemade
    factorized = []
    while n % 2 == 0:
        n = n / 2
        factorized.append(2)

    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3, int(math.sqrt(n)) + 1, 2):

        # while i divides n , print i ad divide n
        while n % i == 0:
            factorized.append(i)
            n = n / i

    if n > 2:
        factorized.append(n)

    return factorized


def generate_factor_base_list(factor_base):
    """
    Creates a list of primes with size factor_base.
    """

    primes = []
    with open("prim_2_24.txt", "r") as primes:
        # Primes are organized in lists of 10 primes, so the following list
        # comprehension returns all the lists of 10 primes until the list that
        # contains the factor_base prime.
        factor_base_list = [next(primes).split() for x in range(math.ceil(factor_base / 10))]
        flattened = [int(prime) for factor_base_sublist in factor_base_list for prime in factor_base_sublist]
        return flattened[:factor_base]


def generate_matrix_row(factorization, factor_base_list):
    new_row = []
    for prime in factor_base_list:
        if prime in factorization:
            new_row.append(factorization.count(prime)%2)
        else:
            new_row.append(0)
    return new_row

def gaussian_elimination(matrix):
    """
    Writes matrix to a file to be used as input to the provided program,
    returns all the solutions
    """
    m = len(matrix)
    n = len(matrix[0])
    with open("matrix_input.txt", "w") as file:
        file.write("{} {}\n".format(m, n))
        for row in matrix:
            stringed_row = [str(i) for i in row]
            file.write(" ".join(stringed_row))
            file.write("\n")
    
    os.system("GaussBin.exe matrix_input.txt result.txt")

    with open("result.txt", "r") as output:
        raw_result = output.readlines()[1:]

    separated = [result.split() for result in raw_result]
    final_result = []
    for solution in separated:
        final_result.append([int(x) for x in solution])
    return final_result


def quadratic_sieve(given_number):
    factor_base = 1000
    factor_base_list = generate_factor_base_list(factor_base)
    print("Generated primes list.")
    r_values = []
    matrix = []
    factorizations = {}
    r_values_seen = []
    # Generate r values
    k = 2
    j = 2
    print("Starting r_numbers generation...")
    while k < factor_base + 2:
        #print("(k: {}, j:{}".format(k,j))
        if j > k:
            j = 1
            k += 1

        r = math.floor(math.sqrt(k * given_number)) + j

        if r ** 2 % given_number > 1 and r ** 2 % given_number not in r_values_seen:
            r_values_seen.append(r)
            factorization = prime_factorization(r ** 2 % given_number)
            if factorization[-1] <= factor_base_list[-1]:
                new_row = generate_matrix_row(factorization, factor_base_list)
                if new_row not in matrix:
                    matrix.append(new_row)
                    r_values.append((r, factorization))
                    print(r)
                    j += 1
                    continue
        j += 1

    print("Finding solutions...")
    solutions = gaussian_elimination(matrix)
    for solution in solutions:
        x = 1
        y = 1
        for equation, i in enumerate(solution):
            if i == 1:
                x *= r_values[equation][0]
                for k in r_values[equation][1]:
                    y *= k

        x = x % given_number
        y = int(math.sqrt(y)) % given_number
        gcd = math.gcd(max([x,y]) - min([x,y]), given_number)
        if gcd != 1:
            return gcd, int(given_number/gcd)


# TESTS #
test = False
if test:
    print("Tests for quadratic sieve have started.")
    in_values = [323, 307561, 31741649, 3205837387, 392742364277][:-1]
    expected = [(17,19), (457, 673), (4621, 6869), (46819, 68473), (534571, 734687)][:-1]

    for index, value in enumerate(in_values):
        print("Running for input {}".format(value))
        start = time.clock()
        print("Got: {}, expected: {}".format(quadratic_sieve(value), expected[index]))
        print("Execution time: {} seconds.".format(time.clock()))
        print("\n")

print(quadratic_sieve(323))
# quadratic_sieve(235616869893895625763911) # Group 12 (me) input