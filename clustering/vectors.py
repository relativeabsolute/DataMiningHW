import math

def dot(first, second):
    if len(first) != len(second):
        raise IndexError
    return sum(first[i] * second[i] for i in range(len(first)))

def norm(vector):
    return math.sqrt(sum(item * item for item in vector))

def cosine(first, second):
    return dot(first, second) / (norm(first) * norm(second))
