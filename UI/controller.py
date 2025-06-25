import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        allYears=self._model.getYears()
        for y in allYears:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

        allCountries = self._model.getCountry()
        for c in allCountries:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        anno=self._view.ddyear.value
        nazione=self._view.ddcountry.value
        self._model.buildGraph(anno,nazione)
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodes()} Numero di archi: {self._model.getNumEdges()}"))
        self._view.update_page()


    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        volumi=self._model.calcolaVolumi()
        for v in volumi:
            self._view.txtOut2.controls.append(ft.Text(f"{v[0]} --> {v[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        lunghezza=self._view.txtN.value
        self._view.txtOut3.controls.clear()

        if lunghezza=="":
            self._view.txtOut3.controls.append(ft.Text("Inserire un numero intero.",color="red"))
            self._view.update_page()
            return

        try:
            lInt=int(lunghezza)
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text("Il valore inserito non è un numero", color="red"))
            self._view.update_page()
            return

        pesoTot,bestCammino=self._model.getBestCammino(lInt)
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {pesoTot}"))
        for arco in bestCammino:
            self._view.txtOut3.controls.append(ft.Text(f"{arco[0]} --> {arco[1]}: {arco[2]['weight']}"))
        self._view.update_page()




