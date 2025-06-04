from grafo import Grafo

def menu():
    print("\n=== SIMULADOR RED ELECTRICA ===")
    print("1. Cargar grafo desde JSON")
    print("2. Mostrar red (lista ponderada y atributos)")
    print("3. Marcar falla en un nodo")
    print("4. Marcar falla en una conexion (arista)")
    print("5. Reparar nodo")
    print("6. Reparar conexion")
    print("7. Mostrar nodos sin suministro")
    print("8. Sugerir ruta alterna (menor distancia)")
    print("9. Visualizar grafo")
    print("10. Salir")
    print("=========================")

def main():
    red = Grafo()

    while True:
        menu()
        opcion = input("Selecciona una opción [1-10]: ").strip()

        if opcion == "1":
            # ----------------------------
            # 1) Cargar red desde JSON
            # ----------------------------
            archivo = input("Ruta del JSON (por defecto 'datos.json'): ").strip()
            if archivo == "":
                archivo = "datos.json"
            try:

        elif opcion == "2":
            # -------------------------------
            # 2) Mostrar red (ponderada)
            # -------------------------------
            else:
                print("Primero debes cargar la red (opción 1).")

        elif opcion == "3":
            # -------------------------------
            # 3) Marcar falla en un nodo
            # -------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opción 1).")
            else:

        elif opcion == "4":
            # ------------------------------------------
            # 4) Marcar falla en una conexión (arista)
            # ------------------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:

        elif opcion == "5":
            # -----------------------------------
            # 5) Reparar nodo (quitar falla)
            # -----------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                

        elif opcion == "6":
            # ------------------------------------------
            # 6) Reparar conexión (quitar falla de arista)
            # ------------------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                

        elif opcion == "7":
            # -----------------------------------
            # 7) Mostrar nodos sin suministro
            # -----------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:

        elif opcion == "8":
            # -----------------------------------
            # 8) Se obtiene la ruta mas corta
            # -----------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                
        elif opcion == "9":
            # -------------------------------
            # 9) Visualizar grafo
            # -------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                

        elif opcion == "10":
            print("Saliendo...")
            break

        else:
            print("Opcion invalida. Elige un numero del 1 al 10.")

if __name__ == "__main__":
    main()
