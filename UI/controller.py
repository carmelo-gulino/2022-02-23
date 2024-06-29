import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_city(self):
        for c in self.model.cities:
            self.view.dd_city.options.append(ft.dropdown.Option(c))

    def fill_dd_locale(self, e):
        self.view.dd_locale.options.clear()
        city = self.view.dd_city.value
        for t in self.model.get_locali(city):
            self.view.dd_locale.options.append(ft.dropdown.Option(key=t[0], text=t[1]))
        self.view.btn_grafo.disabled = False
        self.view.update_page()

    def handle_crea_grafo(self, e):
        business_id = self.view.dd_locale.value
        if business_id is None:
            self.view.create_alert("Selezionare un locale")
            return
        graph = self.model.build_graph(business_id)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {len(graph.nodes)} Numero di archi {len(graph.edges)}"))
        nodi_max = self.model.get_max_uscenti()
        self.view.txt_result.controls.append(ft.Text(f"I nodi con più archi uscenti sono:"))
        for n in nodi_max:
            self.view.txt_result.controls.append(ft.Text(f"{n[0]}: {n[1]} archi"))
        self.view.btn_percorso.disabled = False
        self.view.update_page()

    def handle_percorso(self, e):
        path = self.model.get_percorso()
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Percorso di lunghezza {len(path)} trovato:"))
        self.view.txt_result.controls.append(
            ft.Text(f"Tra il primo e l'ultimo nodo passano {self.model.get_delta(path[0], path[1])} giorni"))
        for p in path:
            self.view.txt_result.controls.append(ft.Text(f"{p}"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
