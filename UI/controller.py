import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def popola_dropdown_ruolo(self):
        roles = self._model.get_roles()
        self._view.dd_ruolo.options = [ft.dropdown.Option(key=r, data=r) for r in roles]
        self._view.update()

    def choice_role(self, e):
        selected_key = e.control.value

        # recupero l’oggetto Category associato
        for opt in e.control.options:
            if opt.key == selected_key:
                self.dd_ruolo_value = opt.data
                break

    def handle_crea_grafo(self, e):
        self._model.build_graph(self.dd_ruolo_value)
        n_nodes, n_edges = self._model.graph_details()

        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(
            ft.Text(f'Nodi: {n_nodes} | Archi: {n_edges}')
        )
        self._view.update()

    def handle_classifica(self, e):
        classifica = self._model.classifica()
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(
            ft.Text(f'Artisti in ordine decrescente di influenza:')
        )
        for c in classifica:
            self._view.list_risultato.controls.append(
                ft.Text(f'{c[0]} -> Delta = {c[1]}')
            )
        self._view.update()


    def popola_dropdown_artista(self):
        artists = self._model.get_all_artists()
        self._view.dd_iniziale.options = [ft.dropdown.Option(key=a.name, data=a) for a in artists]
        self._view.update()

    def choice_iniziale(self, e):
        selected_key = e.control.value

        # recupero l’oggetto Category associato
        for opt in e.control.options:
            if opt.key == selected_key:
                self.dd_iniziale.value = opt.data
                break

    def handle_cerca_cammino(self, e):
        if self._view.txt_lunghezza_cammino.value == "":
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(" Inserire lunghezza del cammino"))
            self._view.update()
            return
        try:
            lun = int(self._view.txt_lunghezza_cammino.value)
        except ValueError:
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text("Valore inserito non numerico"))
            self._view.update()
            return

        path, score = self._model.get_best_path(lun, self.dd_art_start_value, self.dd_art_end_value)
        if len(path) == 0:
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text("Nessun cammino trovato"))
            self._view.update()
            return
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Cammino migliore:"))
        for p in path:
            self._view.txt_risultato.controls.append(ft.Text(f"{p}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Score: {score}"))
        self._view.update()