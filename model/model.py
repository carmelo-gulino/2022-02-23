import copy
import datetime
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.best_sol = None
        self.cities = DAO.get_all_cities()
        self.graph = nx.DiGraph()

    def get_locali(self, city):
        return DAO.get_locali(city)

    def build_graph(self, business_id):
        self.graph.clear()
        reviews = DAO.get_reviews(business_id)
        self.graph.add_nodes_from(reviews)
        for u in self.graph:
            for v in self.graph:
                if u != v:
                    diff = (u.review_date - v.review_date).days
                    if diff > 0:
                        self.graph.add_edge(v, u, weight=abs(diff))
                    elif diff < 0:
                        self.graph.add_edge(u, v, weight=abs(diff))
        return self.graph

    def get_max_uscenti(self):
        sorted_successors = [(r, len(list(self.graph.successors(r)))) for r in self.graph.nodes]
        sorted_successors.sort(key=lambda x: x[1], reverse=True)
        result = [t for t in sorted_successors if t[1] == sorted_successors[0][1]]
        return result
    
    def get_percorso(self):
        self.best_sol = []
        sorted_nodes = sorted(self.graph.nodes, key=lambda review: review.stars)
        parziale = [sorted_nodes[0]]
        self.ricorsione(parziale)
        return self.best_sol

    def ricorsione(self, parziale):
        ultimo = parziale[-1]
        if len(parziale) > len(self.best_sol):
            self.best_sol = copy.deepcopy(parziale)
            print(len(parziale))
        sorted_successors = sorted(self.graph.successors(ultimo), key=lambda review: review.stars)
        for r in sorted_successors:
            if r not in parziale and r.stars >= ultimo.stars:
                parziale.append(r)
                self.ricorsione(parziale)
                parziale.pop()
            else:
                return

    def get_delta(self, g1, g2):
        return abs(g1.review_date - g2.review_date).days
