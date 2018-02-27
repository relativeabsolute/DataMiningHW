from vectors import *
if __name__ == "__main__":
    data = [["Name", "Gender", "Fav Color", "Blood Type", "General Health", "Test1", "Cough", "High Blood Pressure"],
        ["Susan", "F", "Blue", "O-", "Excellent", 75, "N", "N"],
        ["Jim", "M", "Red", "O+", "Good", 65, "N", "N"],
        ["Joe", "M", "Red", "AB-", "Fair", 64, "N", "Y"],
        ["Jane", "F", "Green", "A+", "Poor", 83, "Y", "Y"],
        ["Sam", "M", "Blue", "A-", "Good", 71, "N", "N"],
        ["Michelle", "F", "Blue", "O-", "Good", 90, "N", "N"]]
    rows = data[1:]
    names = get_columns(rows, [0])[0]
    print("Names = {}".format(str(names)))
    symmetric = [1 if item == 'M' else 0 for item in get_columns(rows, [1])[0]]
    print("Symmetric = {}".format(str(symmetric)))
    nominal = get_columns(rows, [2, 3])
    print("Nominal = {}".format(str(nominal)))
    ordinal = ordinal_normalize(get_columns(rows, [4])[0], ["Poor", "Fair", "Good", "Excellent"])
    print("Ordinal = {}".format(str(ordinal)))
    numeric = min_max_normalize(get_columns(rows, [5])[0])
    print("Numeric = {}".format(str(numeric)))
    asymmetric = [[1 if item == 'Y' else 0 for item in vector] for vector in get_columns(rows, [6, 7])]
    print("Asymmetric = {}".format(str(asymmetric)))
    
