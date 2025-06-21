import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapOrders = {}

        self.bestPath = []
        self.pesoMax = 0

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
        longest_path = []
        tree = nx.dfs_tree(self._graph, source)  # albero DFS a partire dal nodo source
        nodi = list(tree.nodes())  # tutti i nodi visitati nella DFS

        for node in nodi:
            tmp = [node]  # inizio un cammino che termina nel nodo attuale

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])  # Trova il predecessore di tmp[0]
                tmp.insert(0, pred[0])  # Aggiungi il predecessore all'inizio del cammino

            if len(tmp) > len(longest_path):  # Se il cammino corrente è più lungo del precedente massimo
                longest_path = copy.deepcopy(tmp)  # Salva il nuovo cammino più lungo

        return longest_path

    # per il punto2 con metodo ricorsivo
    def getBestPathPesoMax(self, source):
        self.bestPath = []
        self.pesoMax = 0
        parziale = [source]
        esplorabili = list(self._graph.successors(source))
        self._ricorsione(parziale, esplorabili)
        return self.bestPath, self.pesoMax

    def _ricorsione(self, parziale, esplorabili):
        if len(esplorabili) == 0:
            if self.getPeso(parziale) > self.pesoMax:
                self.bestPath = copy.deepcopy(parziale)
                self.pesoMax = self.getPeso(parziale)
        else:
            for n in esplorabili:
                if n not in parziale:
                    parziale.append(n)
                    nuovi_esplorabili = self.getEsplorabili(n, parziale)
                    self._ricorsione(parziale, nuovi_esplorabili)
                    parziale.pop()

    def getPeso(self, parziale):
        pesoTot = 0
        for i in range(0, len(parziale) - 1):
            pesoTot += self._graph[parziale[i]][parziale[i + 1]]['weight']
        return pesoTot

    def getEsplorabili(self, n, parziale):
        esplorabili = []
        for node in self._graph.successors(n):
            if node not in parziale and self._graph[parziale[-1]][node]['weight'] < self._graph[parziale[-2]][parziale[-1]]['weight']:
                esplorabili.append(node)
        return esplorabili

