import copy

import networkx as nx

from database.DAO import DAO
from model.retailer import Retailer


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._idMap={}
        self._bestPath=[]
        self._bestPeso=0
    def getYears(self):
        return DAO.getYears()

    def getCountry(self):
        return DAO.getCountry()

    def buildGraph(self,anno,nazione):
        self._grafo.clear()
        nodes=DAO.getNodiRetailers(nazione)
        self._grafo.add_nodes_from(nodes)
        for n in nodes:
            self._idMap[n.Retailer_code]=n
        archi=DAO.getArchiPesati(anno,nazione,self._idMap)
        for a in archi:
            self._grafo.add_edge(a[0],a[1],weight=a[2])

    def getNumNodes(self):
        return len(list(self._grafo.nodes))

    def calcolaVolumi(self):
        volumi=[]
        for n in self._grafo.nodes:
            incidenti=self._grafo.edges(n,data=True)
            volume=0
            for i in incidenti:
                volume+=i[2]['weight']
            volumi.append((n,volume))
        vol2=sorted(volumi,key=lambda x: x[1],reverse=True)
        return vol2

    def getNumEdges(self):
        return len(list(self._grafo.edges))


    def getBestCammino(self,lunghezza):
        self._bestPath = []
        self._bestPeso = 0
        parziale=[]
        for nodo in self._grafo.nodes:
            parziale.append(nodo)
            self._ricorsione(lunghezza,parziale)
            parziale.remove(nodo)

        return self._bestPeso,self._bestPath

    def _ricorsione(self,lunghezza,parziale: list[Retailer]):
        if len(parziale)==lunghezza+1:
            if self._bestPeso<self.calcolaPeso(parziale):
                self._bestPath=copy.deepcopy(parziale)
                self._bestPeso=self.calcolaPeso(parziale)
            return
        for nodo in self._grafo.neighbors(parziale[-1]):
            if nodo not in parziale or (nodo==parziale[0] and len(parziale)==lunghezza):
                parziale.append(nodo)
                self._ricorsione(lunghezza, parziale)
                parziale.remove(nodo)

    def calcolaPeso(self, cammino: list[Retailer]):
        peso = 0
        for i in range(len(cammino) - 1):
            peso += self._grafo[cammino[i]][cammino[i + 1]]['weight']

        # Aggiungi il peso tra ultimo e primo nodo se è un ciclo valido
        if self._grafo.has_edge(cammino[-1], cammino[0]):
            peso += self._grafo[cammino[-1]][cammino[0]]['weight']

        return peso

