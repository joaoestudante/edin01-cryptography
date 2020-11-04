import math

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
    prime_index = 0
    target_number_rows = len(matrix) - len(matrix[0])
    while prime_index < 10:
        for row in matrix:
            if row[prime_index] == 1:
                for row2 in matrix:
                    if row2 != row:
                        for i in range(len(row)):
                            if row2[prime_index] == 1:
                                row2[i] = (row2[i] + row[i]) % 2
                matrix.remove(row)
        prime_index += 1


def quadratic_sieve(given_number):
    factor_base = 10
    factor_base_list = generate_factor_base_list(factor_base)
    r_values = []
    matrix = []
    # Generate r values
    k = 2
    j = 2
    while len(r_values) < factor_base + 2:
        r = math.floor(math.sqrt(k * given_number)) + j

        if j > k:
            j = 1
            k += 1

        factorization = prime_factorization(r ** 2 % given_number)
        if factorization[-1] <= factor_base_list[-1]:
            new_row = generate_matrix_row(factorization, factor_base_list)
            if new_row not in matrix:
                matrix.append(new_row)
                r_values.append((r, factorization))
                j += 1
                continue
        j += 1
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    gaussian_elimination(matrix)
    print("#####################################")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    print(len(matrix))



quadratic_sieve(16637)  # should return (17, 19)
