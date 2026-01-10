import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.products = []
        self.id_map = {}

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        return DAO.obtain_category()

    def build_graph(self,category,date1,date2):
        self.G.clear()
        self.products = DAO.get_all_products_by_category(category)

        for p in self.products:
            self.id_map[p.id] = p

        self.G.add_nodes_from(self.products)

        all_edges = DAO.get_edges(category,date1,date2,self.id_map)
        for e in all_edges:
            self.G.add_edge(e[0],e[1], weight=e[2])

    def get_graph_details(self):
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def get_best_prodotti(self):
        best_prodotti = []
        for n in self.G.nodes():
            score = 0
            for e_out in self.G.edges(n, data=True):
                score += e_out[2]['weight']
            for e_in in self.G.edges(n, data=True):
                score += e_in[2]['weight']

            best_prodotti.append((n,score))

        best_prodotti = sorted(best_prodotti, key=lambda x: x[1], reverse=True)
        return best_prodotti[0:5]

    def get_all_nodes(self):
        nodes = list(self.G.nodes())
        nodes.sort(key=lambda x: x.product_name)
        return nodes