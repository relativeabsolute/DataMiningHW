import math

def dot(first, second):
    if len(first) != len(second):
        raise IndexError
    return sum(first[i] * second[i] for i in range(len(first)))

def norm(vector):
    return math.sqrt(sum(item * item for item in vector))

def cosine(first, second):
    return dot(first, second) / (norm(first) * norm(second))

# used to measure similarity of asymmetric binary data
def jaccard_similarity_coefficient(first, second):
    if len(first) != len(second):
        raise IndexError
    return float(sum(1 if first[i] and second[i] else 0 for i in range(len(first)))) / sum(1 if first[i] or second[i] else 0 for i in range(len(first)))

# used to measure similarity of symmetric binary data or categorical data
def simple_matching_coefficient(first, second):
    if len(first) != len(second):
        raise IndexError
    return float(sum(1 if first[i] == second[i] else 0 for i in range(len(first)))) / len(first)

def min_max_normalize(vector):
    min_item = min(vector)
    max_item = max(vector)
    delta = max_item - min_item
    return [(x - min_item) / delta for x in vector]

def ordinal_normalize(vector, order):
    order_dict = {item[1] : item[0] for item in enumerate(order)}
    return [order_dict[item] / float(len(order) - 1) for item in vector]

def euclidean_distance(first, second):
    return normalized_euclidean_distance(first, second, [1.0 for _ in first])

def normalized_euclidean_distance(first, second, weights):
    if len(first) != len(second) or len(first) != len(weights):
        raise IndexError
    return math.sqrt(sum(weights[i] * (first[i] - second[i]) ** 2 for i in range(len(first)))) / math.sqrt(sum(weights))
