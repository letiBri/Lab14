import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDDNodi = None

    def fillDDStore(self):
        store = self._model.getStore()
        for s in store:
            self._view._ddStore.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view._ddNode.options.clear()
        storeId = self._view._ddStore.value
        if storeId == "" or storeId is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: selezionare uno store!", color="red"))
            self._view.update_page()
            return
        storeIdInt = int(storeId)

        kMax = self._view._txtIntK.value
        if kMax is None or kMax == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: inserire un numero massimo di giorni!", color="red"))
            self._view.update_page()
            return
        try:
            kInt = int(kMax)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: inserire un numero intero positivo di giorni!", color="red"))
            self._view.update_page()
            return
        if kInt < 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione: inserire un numero intero positivo di giorni!", color="red"))
            self._view.update_page()
            return
        # se sono qui ho superato tutti i controlli
        self._model.buildGraph(storeIdInt, kInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {a}"))
        self.fillDDNodi(list(self._model._graph.nodes()))
        self._view._btnRicorsione.disabled = False
        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view.update_page()

    def handleCerca(self, e):
        if self._choiceDDNodi is None:
            self._view.txt_result.controls.append(ft.Text("Attenzione: selezionare il nodo di partenza!", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {self._choiceDDNodi.order_id}"))
        self._view.update_page()
        path = self._model.getCamminoMax(self._choiceDDNodi)
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p.order_id))
        self._view.update_page()


    def handleRicorsione(self, e):
        pass

    def fillDDNodi(self, listOfNodes):
        for n in listOfNodes:
            self._view._ddNode.options.append(ft.dropdown.Option(key=n.order_id, data=n, on_click=self.getSelectedNode))
        self._view.update_page()


    def getSelectedNode(self, e):
        if e.control.data is None:
            print("error in reading DD Nodes")
            self._choiceDDNodi = None
        self._choiceDDNodi = e.control.data
