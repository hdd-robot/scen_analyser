from nltk.corpus import wordnet as wn
import matplotlib
import networkx as nx

def travers(graph, start, node):
    graph.depth[node.name()] = node.shortest_path_distance(start)
    for child in node.hyponyms():
        graph.add_edge(node.name(), child.name())
        travers(graph, start, child)

def hyponym_graph(start):
    G = nx.Graph()
    G.depth = {}
    travers(G, start, start)
    return G

def graph_draw(graph):
    nx.draw(graph, node_size=[5 * graph.degree(n) for n in graph], node_color=[graph.depth[n] for n in graph],
    with_labels=True)
    matplotlib.pyplot.show()


computer = wn.synset('eating_utensil.n.01')
graph = hyponym_graph(computer)
graph_draw(graph)
