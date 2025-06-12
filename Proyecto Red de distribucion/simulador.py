from collections import deque
import heapq

def componentes_conexas(grafo, fallas_nodos, fallas_conex):
    
    #Encuentra todas las componentes conexas del grafo, ignorando nodos y aristas en falla.
    #Usa una búsqueda en profundidad/anchura (DFS/BFS) para agrupar nodos conectados.
    
    visitados = set()
    componentes = []

    for nodo in grafo:
        if nodo in visitados or nodo in fallas_nodos:
            continue
        cola = [nodo]
        comp = set()
        while cola:
            u = cola.pop()
            if u in visitados or u in fallas_nodos:
                continue
            visitados.add(u)
            comp.add(u)
            for (v, _) in grafo[u]:
                if (v not in visitados and
                    v not in fallas_nodos and
                    frozenset((u, v)) not in fallas_conex):
                    cola.append(v)
        if comp:
            componentes.append(comp)
    return componentes

def nodos_sin_suministro_por_bfs(grafo, fallas_nodos, fallas_conex, subestaciones):
    
    #Retorna el conjunto de nodos que no estan conectados a ninguna subestacion viva.
    #Parte simultaneamente de todas las subestaciones.
    
    visitados = set()
    cola = deque()
    for s in subestaciones:
        if s not in fallas_nodos:
            visitados.add(s)
            cola.append(s)

    while cola:
        u = cola.popleft()
        for (v, _) in grafo[u]:
            if (v not in visitados and
                v not in fallas_nodos and
                frozenset((u, v)) not in fallas_conex):
                visitados.add(v)
                cola.append(v)

    return set(grafo.keys()) - visitados

def dijkstra_multi_fuente(grafo, fallas_nodos, fallas_conex, fuentes):
    
    #Ejecuta Dijkstra con múltiples fuentes simultaneas.
    #Ignora nodos y aristas en falla. Devuelve:
     # - dist: distancia mínima desde la fuente más cercana a cada nodo.
     # - padre: nodo predecesor en esa ruta optima.
    
    dist = {nodo: float('inf') for nodo in grafo}
    padre = {nodo: None for nodo in grafo}
    pq = []

    for s in fuentes:
        if s in grafo and s not in fallas_nodos:
            dist[s] = 0
            heapq.heappush(pq, (0, s))

    while pq:
        distancia_u, u = heapq.heappop(pq)
        if distancia_u > dist[u] or u in fallas_nodos:
            continue
        for (v, peso_uv) in grafo[u]:
            if v in fallas_nodos or frozenset((u, v)) in fallas_conex:
                continue
            nd = distancia_u + peso_uv
            if nd < dist[v]:
                dist[v] = nd
                padre[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, padre

def reconstruir_camino(padre, dist, nodo_destino):
    
    #Reconstruye el camino de menor distancia hasta nodo_destino usando el diccionario 'padre'.
    #Si dist[nodo_destino] es infinito, devuelve lista vacía.
    
    if dist.get(nodo_destino, float('inf')) == float('inf'):
        return []
    ruta = []
    u = nodo_destino
    while u is not None:
        ruta.append(u)
        u = padre[u]
    return list(reversed(ruta))

def sugerir_rutas_por_distancia(grafo, fallas_nodos, fallas_conex, atributos):
  
    subestaciones_todas = [
        n for n, a in atributos.items()
        if a["tipo"].startswith("subestacion") or a["tipo"].startswith("central")
    ]
    dist_pre, padre_pre = dijkstra_multi_fuente(
        grafo, set(), set(), subestaciones_todas
    )
    subestaciones_vivas = [
        n for n in subestaciones_todas if n not in fallas_nodos
    ]
    dist_post, padre_post = dijkstra_multi_fuente(
        grafo, fallas_nodos, fallas_conex, subestaciones_vivas
    )

    sugerencias = []
    for nodo in grafo.keys():
        if nodo in subestaciones_todas:
            continue
        d_pre = dist_pre.get(nodo, float('inf'))
        d_post = dist_post.get(nodo, float('inf'))
        camino_pre = reconstruir_camino(padre_pre, dist_pre, nodo) if d_pre < float('inf') else []
        camino_post = reconstruir_camino(padre_post, dist_post, nodo) if d_post < float('inf') else []

        # Antes alcanzable, ahora inalcanzable
        if d_post == float('inf') and d_pre < float('inf'):
            sugerencias.append((nodo, d_pre, camino_pre, d_post, []))
        # Antes inalcanzable, ahora alcanzable
        elif d_pre == float('inf') and d_post < float('inf'):
            sugerencias.append((nodo, float('inf'), [], d_post, camino_post))
        # Ambos alcanzables, pero distancia aumentó
        elif d_pre < float('inf') and d_post > d_pre + 1e-9:
            sugerencias.append((nodo, d_pre, camino_pre, d_post, camino_post))
        # Ambos alcanzables, misma distancia, pero caminos distintos
        elif (d_pre < float('inf') and d_post < float('inf')
              and abs(d_post - d_pre) < 1e-9 and camino_pre != camino_post):
            sugerencias.append((nodo, d_pre, camino_pre, d_post, camino_post))

    return sugerencias
