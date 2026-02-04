import networkx as nx
from database.dao import DAO
import copy

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.artists = [] #nodes
        self.id_map = {}

    def get_authorship(self):
        self.authorships = DAO.get_authorship()

    def get_roles(self):
        return DAO.get_all_roles()

    def build_graph(self, role: str):
        self.artists = DAO.get_artist_for_role(role)

        self.G.clear()

        for a in self.artists:
            self.id_map[a.artist_id] = a

        self.G.add_nodes_from(self.artists)

        all_edges = DAO.get_edges(role, self.id_map)
        for e in all_edges:
            self.G.add_edge(e[0], e[1], weight=e[2])


    def graph_details(self):
        return self.G.number_of_nodes(), self.G.number_of_edges()


    def classifica(self):
        classifica = []
        for n in self.G.nodes():
            in_edges = self.G.in_edges(n)
            out_edges = self.G.out_edges(n)
            somma_in = 0
            somma_out = 0
            for e in in_edges:
                somma_in += e[1]['weight']
            for e in out_edges:
                somma_out += e[1]['weight']
            delta = somma_out - somma_in
            classifica.append(n, delta)

        classifica.sort(key= lambda x:x[1], reverse=True)
        return classifica

    def get_all_artists(self):
        return self.artists

    def get_best_path(self, lungh, start, end):
        self.best_path = []
        self.best_score = 0
        parziale = [start]
        self._ricorsione(parziale, lungh, start, end)
        return self.best_path, self.best_score

    def _ricorsione(self, parziale, lungh, start, end):
        if len(parziale) == lungh:
            if parziale[-1] == end and self._get_score(parziale) > self.best_score:
                self.best_score = self._get_score(parziale)
                self.best_path = copy.deepcopy(parziale)
            return

        for n in self.G.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lungh, start, end)
                parziale.pop()

    def _get_score(self, parziale):
        score = 0
        for i in range(1, len(parziale)):
            score += self.G[parziale[i - 1]][parziale[i]]["weight"]
        return score