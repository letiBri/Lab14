import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapOrders = {}


    def getStore(self):
        return DAO.getStore()

    def buildGraph(self, storeId, kInt):
        self._graph.clear()
        self._idMapOrders = {}
        nodes = DAO.getOrders(storeId)
        for n in nodes:
            self._idMapOrders[n.order_id] = n
        self._graph.add_nodes_from(nodes)

        edges = DAO.getEdges(storeId, kInt)
        for e in edges:
            # print(e.ordine1, e.ordine2, e.peso)
            self._graph.add_edge(self._idMapOrders[e.ordine1], self._idMapOrders[e.ordine2], weight=e.peso)


    def getGraphDetails(self):
        print("Num nodi:", len(self._graph.nodes), "Num archi:", len(self._graph.edges))
        return len(self._graph.nodes), len(self._graph.edges)

    def getCamminoMax(self, source):
        cammino = list(nx.bfs_tree(self._graph, source))
        cammino.remove(source)
        return cammino
