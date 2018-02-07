import argparse
import random
import vectors

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='csv file containing vector data')
    parser.add_argument('num_clusters', help='number of clusters to find.', type=int)
    options = vars(parser.parse_args())

    return options

# assign data to clusters based on which cluster has the closest means
# data is a list of vectors
# means is a list of vectors to be treated as means
# distance_calc is a callable that takes two vectors and returns a floating point
#   calculation of the distance between the vectors
def assign_clusters(data, means, distance_calc):
    clusters = [[] for _ in range(len(means))]
    sim = [[distance_calc(data[j], mean) for mean in means] for j in range(len(data))]
    print("Sim = ")
    print(str(sim))
    for i in range(len(sim)):
        clusters[min(enumerate(sim[i]), key = lambda x : x[1])[0]].append(data[i])
    for i in range(len(clusters)):
        if not clusters[i]:
            clusters[i].append(random.choice(data))
    return clusters

def get_means(clusters):
    return [[sum(x) / len(cluster) for x in zip(*cluster)] if len(cluster) > 1 else cluster[0] for cluster in clusters]

# there are definitely more exact ways to calculate this but this should be good enough
# clusters must be sorted by length for correct results!
def has_converged(prev_clusters, clusters):
    return len(prev_clusters) == len(clusters) and all(len(prev_clusters[i]) == len(clusters[i]) for i in range(len(clusters)))

def do_kmeans(data, k, distance_calc):
    means = random.sample(data, k)
    prev_clusters = means
    clusters = [[] for _ in range(len(means))]
    while not has_converged(prev_clusters, clusters):
        prev_clusters = clusters
        clusters = sorted(assign_clusters(data, means, distance_calc), key=len)
        print("Clusters:")
        print(str(clusters))
        means = get_means(clusters)
        print("Means:")
        print(means)
    return clusters
    

def run(args):
    with open(args['data_file'], newline='') as input_csv:
        reader = csv.reader(input_csv, delimiter=',')
        # TODO: handle data input
    

def main():
    run(handle_args())

if __name__ == "__main__":
    main()
