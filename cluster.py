from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering


def kmeans_clustering(pair_tuple_list, num_clusters, model='all-MiniLM-L6-v2'):
    """
    pair_tuple_list: [(a1, b1), (a2, b2), (a3, b3), ...]
        ax is for clustering, bx is for showing in the result.
    """
    corpus_list = [temp_tuple[0] for temp_tuple in pair_tuple_list]
    show_list = [temp_tuple[1] for temp_tuple in pair_tuple_list]
    embedder = SentenceTransformer(model)
    corpus_embeddings = embedder.encode(corpus_list)

    clustering_model = KMeans(n_clusters=num_clusters)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_
    clustered_sentences = {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        if cluster_id not in clustered_sentences:
            clustered_sentences[cluster_id] = []
        clustered_sentences[cluster_id].append(show_list[sentence_id])

    clustered_sentences = dict(sorted(clustered_sentences.items(), key=lambda x: x[0]))

    for i, cluster in clustered_sentences.items():
        print("#" * 50 + " Cluster ", i + 1, "#" * 50)
        for c in cluster:
            print(c)
        print("")


def agglomerative_clustering(pair_tuple_list, threshold, model='all-MiniLM-L6-v2'):
    """
    pair_tuple_list: [(a1, b1), (a2, b2), (a3, b3), ...]
    ax is for clustering, bx is for showing in the result.
    """
    corpus_list = [temp_tuple[0] for temp_tuple in pair_tuple_list]
    show_list = [temp_tuple[1] for temp_tuple in pair_tuple_list]
    embedder = SentenceTransformer(model)
    corpus_embeddings = embedder.encode(corpus_list)
    clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=threshold)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        if cluster_id not in clustered_sentences:
            clustered_sentences[cluster_id] = []
        clustered_sentences[cluster_id].append(show_list[sentence_id])

    clustered_sentences = dict(sorted(clustered_sentences.items(), key=lambda x: x[0]))

    for i, cluster in clustered_sentences.items():
        print("#" * 50 + " Cluster ", i + 1, "#" * 50)
        for c in cluster:
            print(c)
        print("")