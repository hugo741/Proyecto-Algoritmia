import json

class Grafo:
    def __init__(self):
        #Sera un diccionario
        self.grafo = {}
        # guardara por cada nodo sus atributos
        self.atributos = {}

    def cargar_desde_json(self, archivo_json):

        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        # Guarda los atributos de cada nodo
        self.atributos = datos.get("nodos", {})

        # Inicializa el grafo con lista vacia para cada nodo
        self.grafo = { nodo: [] for nodo in self.atributos }

        # Recorrer las conexiones y añadirlas con su distancia
        for conexion in datos.get("conexiones", []):
            origen  = conexion["origen"]
            destino = conexion["destino"]
            dist    = conexion.get("distancia", 1)  # si no viene, asumimos 1

            if origen not in self.grafo or destino not in self.grafo:
                raise ValueError(f"Conexion invalida: {origen} ↔ {destino}")

            self.grafo[origen].append((destino, dist))
            self.grafo[destino].append((origen, dist))

    def imprimir_red(self):
        
        #Muestra los atributos de cada nodo y la lista de adyacencia ponderada.
        print("---- ATRIBUTOS DE CADA NODO ----")
        for nodo, attrs in self.atributos.items():
            print(f"  {nodo}: {attrs}")

        print("\n---- GRAFO (lista de adyacencia) ----")
        for nodo, vecinos in self.grafo.items():
            lista_str = ", ".join(f"{v}({d})" for v, d in vecinos)
            print(f"  {nodo} → [{lista_str}]")
