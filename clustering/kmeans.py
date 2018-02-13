import argparse
import random
import vectors
import csv

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

# optimization: don't need to calculate entire similarity matrix, only similarities between data and means
# given set of data, return a list of indices for each 
def assign_clusters(data, means, distance_calc):
    new_clusters = [[] for _ in range(len(means))]
    # sim[i] = [cos(data[i], mean[0]), cos(data[i], mean[1]), ... cos(data[i], mean[k])]
    sim = [[distance_calc(data[i], mean) for mean in means] for i in range(len(data))]
    print("Sim = ")
    print(str(sim))
    # result[i] = index of cluster data[i] belongs to
    return [max(enumerate(sim_item), key = lambda x : x[1])[0] for sim_item in sim]

# expects lists of data rows themselves
def get_means(clusters):
    return [[sum(x) / len(cluster) for x in zip(*cluster)] if len(cluster) > 1 else cluster[0] for cluster in clusters]

# use for lists of indices
# assumed that prev_clusters and clusters are each the same length
# since each item of data will be assigned to a cluster
def has_converged_exact(prev_clusters, clusters):
    return all(prev_clusters[i] == clusters[i] for i in range(len(clusters)))

def do_kmeans(data, k, distance_calc):
    mean_indices = random.sample(range(len(data)), k)
    means = [data[i] for i in mean_indices]
    prev_clusters = mean_indices
    clusters = [-1] * len(means)
    while not has_converged_exact(prev_clusters, clusters):
        prev_clusters = clusters
        clusters = assign_clusters(data, means, distance_calc)
        print("Clusters (Indices):")
        print(str(clusters))
        print("Clusters (Data):")
        cluster_data = [[data[i] for i in range(len(clusters)) if clusters[i] == index] for index in range(k)]
        print(str(cluster_data))
        means = get_means(cluster_data)
        print("Means:")
        print(means)
    return clusters
  
# returns a tuple containing the header row, the titles, and the votes themselves
def read_votes(file_name):
    with open(file_name, newline='') as input_csv:
        reader = csv.reader(input_csv)
        rows = [row for row in reader]
    return (rows[0], [row[0] for row in rows[1:]], [[int(row[i]) for row in rows[1:]] for i in range(1,len(rows[0]))])

def run(args):
    k = args['num_clusters']
    votes_header, votes_titles, votes_data = read_votes(args['data'])
    print("Header:")
    print(str(votes_header))
    print("Titles:")
    print(str(votes_titles))
    print("Data:")
    print(str(votes_data))
    result = do_kmeans(votes_data, args['num_clusters'], vectors.cosine)
    names = [[votes_header[1:][i] for i in range(len(result)) if result[i] == index] for index in range(k)]
    print("Result (Indices):")
    print(str(result))
    print("Result (Names):")
    print(str(names))

def main():
    run(handle_args())

if __name__ == "__main__":
    main()
