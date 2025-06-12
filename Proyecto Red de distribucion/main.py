from grafo import Grafo
from simulador import sugerir_rutas_por_distancia, nodos_sin_suministro_por_bfs
from visualizador import visualizar_red

#Ejemplos:
#1 T2-T3   T3
#2 SE0-SC   SC
#3 SE0-SC   CE3

def mostrar_menu():
    print("\n=== SIMULADOR RED ELECTRICA ===")
    print("1. Cargar grafo desde JSON")
    print("2. Mostrar red")
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
    fallas_nodos = set()
    fallas_conex = set()
    subestaciones = []

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción [1-10]: ").strip()

        if opcion == "1":
            # ----------------------------
            # 1) Cargar red desde JSON
            # ----------------------------
            archivo = input("Ruta del JSON (por defecto 'datos.json'): ").strip()
            if archivo == "":
                archivo = "datos.json"
            try:
                red.cargar_desde_json(archivo)
                print(f"Red cargada correctamente desde '{archivo}'.")
                # Detecta subestaciones
                subestaciones = [
                    n for n, a in red.atributos.items()
                    if a["tipo"].startswith("subestacion") or a["tipo"].startswith("central")
                ]
                print(f"  → Subestaciones detectadas: {subestaciones}")
                # reiniciamos fallas
                fallas_nodos.clear()
                fallas_conex.clear()
            except Exception as e:
                print(f"Error al cargar JSON: {e}")

        elif opcion == "2":
            # -------------------------------
            # 2) Mostrar red 
            # -------------------------------
            if red.grafo:
                red.imprimir_red()
            else:
                print("Primero debes cargar la red (opción 1).")

        elif opcion == "3":
            # -------------------------------
            # 3) Marcar falla en un nodo
            # -------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opción 1).")
            else:
                nodo = input("Nombre del nodo a fallar: ").strip()
                if nodo in red.grafo:
                    fallas_nodos.add(nodo)
                    print(f"  -> Nodo '{nodo}' marcado como falla.")
                else:
                    print(f"   El nodo '{nodo}' no existe en la red.")

        elif opcion == "4":
            # ------------------------------------------
            # 4) Marcar falla en una conexión (arista)
            # ------------------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                a = input("Nodo A de la conexion a fallar: ").strip()
                b = input("Nodo B de la conexion a fallar: ").strip()
                # Verificamos que exista la arista en grafo.grafo
                existe = False
                for (v, _) in red.grafo.get(a, []):
                    if v == b:
                        existe = True
                        break
                if existe:
                    fallas_conex.add(frozenset((a, b)))
                    print(f"  → Conexion '{a} ↔ {b}' marcada como falla.")
                else:
                    print(" La arista indicada no existe o ya esta caida.")

        elif opcion == "5":
            # -----------------------------------
            # 5) Reparar nodo (quitar falla)
            # -----------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                nodo = input("Nombre del nodo a reparar: ").strip()
                if nodo in fallas_nodos:
                    fallas_nodos.remove(nodo)
                    print(f"  → Nodo '{nodo}' reparado (ya no esta en falla).")
                else:
                    print(f" El nodo '{nodo}' no esta marcado como falla.")

        elif opcion == "6":
            # ------------------------------------------
            # 6) Reparar conexion (quitar falla de arista)
            # ------------------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                a = input("Nodo A de la conexión a reparar: ").strip()
                b = input("Nodo B de la conexión a reparar: ").strip()
                clave = frozenset((a, b))
                if clave in fallas_conex:
                    fallas_conex.remove(clave)
                    print(f"  → Conexion '{a} ↔ {b}' reparada.")
                else:
                    print(" Esa conexion no estaba marcada como falla.")

        elif opcion == "7":
            # -----------------------------------
            # 7) Mostrar nodos sin suministro
            # -----------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                aislados = nodos_sin_suministro_por_bfs(
                    red.grafo, fallas_nodos, fallas_conex, subestaciones
                )
                if aislados:
                    print("\nNodos SIN suministro:")
                    for n in sorted(aislados):
                        print(f"  - {n}")
                else:
                    print("Todos los nodos estan recibiendo suministro.")

        elif opcion == "8":
            # -----------------------------------
            # 8) Se obtiene la ruta mas corta
            # -----------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                #Calculamos rutas pre-falla y post-falla
                sugerencias = sugerir_rutas_por_distancia(
                    red.grafo, fallas_nodos, fallas_conex, red.atributos
                )

                print("\n--- Sugerencias de reconexion (menor distancia) ---")
                for (nodo, d_pre, camino_pre, d_post, camino_post) in sugerencias:
                    if d_pre == float('inf') and d_post < float('inf'):
                        print(
                            f"  → Nodo '{nodo}' antes inalcanzable, "
                            f"ahora usar ruta: {camino_post} (dist={d_post})"
                        )

                    elif d_post == float('inf'):
                        if d_pre < float('inf'):
                            print(
                                f"  → Nodo '{nodo}' perdio su ruta anterior "
                                f"{camino_pre} (dist={d_pre}) y no tiene alternativa."
                            )
                        else:
                            print(f"  → Nodo '{nodo}' sigue inalcanzable.")

                    elif d_pre < float('inf') and d_post > d_pre + 1e-9:
                        print(
                            f"  → Nodo '{nodo}' antes: {camino_pre} (dist={d_pre}), "
                            f"ahora: {camino_post} (dist={d_post})"
                        )


        elif opcion == "9":
            # -------------------------------
            # 9) Visualizar grafo
            # -------------------------------
            if not red.grafo:
                print("Primero debes cargar la red (opcion 1).")
            else:
                #rutas afectadas 
                sugerencias_completas = sugerir_rutas_por_distancia(
                    red.grafo, fallas_nodos, fallas_conex, red.atributos
                )

                rutas_a_dibujar = []
                for (_nodo, _d_pre, _cam_pre, d_post, cam_post) in sugerencias_completas:
                    if d_post < float('inf') and cam_post:
                        for i in range(len(cam_post) - 1):
                            u = cam_post[i]
                            v = cam_post[i + 1]
                            rutas_a_dibujar.append((u, v))

                #Llamamos a visualizar_red, pasando rutas_a_dibujar 
                visualizar_red(
                    red.grafo,
                    red.atributos,
                    fallas_nodos=fallas_nodos,
                    fallas_conex=fallas_conex,
                    sugerencias=rutas_a_dibujar
                )

        elif opcion == "10":
            print("Saliendo...")
            break

        else:
            print("Opcion invalida")

if __name__ == "__main__":
    main()
