def nodosbfs(grafo, fallas_nodos, fallas_conex, subestaciones):
    
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
                v not in fallas_nodos):
                visitados.add(v)
                cola.append(v)

    return set(grafo.keys()) - visitados



def dijkstra(grafo, fallas_nodos, fallas_conex, fuentes):
    
     # dist: distancia minima desde la fuente mas cercana a cada nodo.
     # padre: nodo predecesor en esa ruta optima
    
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
            if v in fallas_nodos:
                continue
            nd = distancia_u + peso_uv
            if nd < dist[v]:
                dist[v] = nd
                padre[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, padre    