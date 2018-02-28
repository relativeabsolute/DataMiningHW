from vectors import *

data = [["Name", "Gender", "Fav Color", "Blood Type", "General Health", "Test1", "Cough", "High Blood Pressure"],
        ["Susan", "F", "Blue", "O-", "Excellent", 75, "N", "N"],
        ["Jim", "M", "Red", "O+", "Good", 65, "N", "N"],
        ["Joe", "M", "Red", "AB-", "Fair", 64, "N", "Y"],
        ["Jane", "F", "Green", "A+", "Poor", 83, "Y", "Y"],
        ["Sam", "M", "Blue", "A-", "Good", 71, "N", "N"],
        ["Michelle", "F", "Blue", "O-", "Good", 90, "N", "N"]]

def flip_matrix(matrix):
    return [[1 - item for item in row] for row in matrix]
    
def sum_matrices(matrices):
    return [[sum([matrices[i][row][index] for i in range(len(matrices))]) for index in range(len(matrices[0][row]))] for row in range(len(matrices[0]))]

def scale_matrix(matrix, scalar):
    return [[scalar * item for item in row] for row in matrix] 

def print_matrix(matrix):
    for row in matrix:
        print('[', end='')
        for item in row:
            print(' {} '.format(item), end='')
        print(']')

if __name__ == "__main__":
    rows = data[1:]
    names = get_columns(rows, [0])
    print("Names = {}".format(str(names)))
    symmetric = get_columns_lambda(rows, [1], lambda item: 1 if item == 'M' else 0)
    symmetric_matrix = [[simple_matching_coefficient([symmetric[i]], [symmetric[j]]) for i in range(len(symmetric))]
        for j in range(len(symmetric))]
    print("Symmetric = {}".format(str(symmetric)))
    print("Symmetric similarity matrix = ")
    print_matrix(symmetric_matrix)
    nominal = get_columns(rows, [2, 3])
    nominal_matrix = [[simple_matching_coefficient(nominal[i], nominal[j]) for i in range(len(nominal))]
        for j in range(len(nominal))]
    print("Nominal = {}".format(str(nominal)))
    print("Nominal similarity matrix = ")
    print_matrix(nominal_matrix)
    order = ["Poor", "Fair", "Good", "Excellent"]
    ordinal = get_columns_lambda(rows, [4], lambda item: ordinal_normalize_num(item, order))
    ordinal_matrix = [[euclidean_distance(ordinal[i], ordinal[j]) for i in range(len(ordinal))]
        for j in range(len(ordinal))]
    print("Ordinal = {}".format(str(ordinal)))
    print("Ordinal difference matrix = ")
    print_matrix(ordinal_matrix)
    numeric = min_max_normalize_v(get_columns(rows, [5]))
    numeric_matrix = [[euclidean_distance([numeric[i]], [numeric[j]]) for i in range(len(numeric))]
        for j in range(len(numeric))]
    print("Numeric = {}".format(str(numeric)))
    print("Numeric difference matrix = ")
    print_matrix(numeric_matrix)
    asymmetric = [[1 if item == 'Y' else 0 for item in vector] for vector in get_columns(rows, [6, 7])]
    print("Asymmetric = {}".format(str(asymmetric)))
    asymmetric_matrix = [[jaccard_similarity_coefficient(asymmetric[i], asymmetric[j])
        for i in range(len(asymmetric))] for j in range(len(asymmetric))]
    for i in range(len(asymmetric_matrix)):
        for j in range(len(asymmetric_matrix)):
            if i == j:
                asymmetric_matrix[i][j] = 1.0 # needed because NaN != NaN
    print("Asymmetric similarity matrix = ")
    print_matrix(asymmetric_matrix)

    matrices = [symmetric_matrix, scale_matrix(nominal_matrix, 2.0), flip_matrix(ordinal_matrix),
        scale_matrix(flip_matrix(numeric_matrix), 2.0), asymmetric_matrix]
    matrix_sum = scale_matrix(sum_matrices(matrices), 1.0 / 7.0)
    print("Result = ")
    print_matrix(matrix_sum)
