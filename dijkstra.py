import math


class InvalidGraphItemError(Exception):
    pass


class NoGraphStartVertexError(Exception):
    pass


class NoGraphEndVertexError(Exception):
    pass


class NoPathExistsError(Exception):
    pass


class Vertex:
    def __init__(self, label, distance=math.inf, edges=None):
        self.label = str(label)
        self.distance = distance
        self.vertex_from = None
        self.edges = [] if edges is None else edges

    def add_edge(self, edge):
        self.edges.append(edge)

    def add(self, edge):
        self.add_edge(edge)

    def __repr__(self):
        return f'Vertex({self.label}, {self.distance}, {self.edges})'


class Edge:
    def __init__(self, vertex_from, vertex_to, weight):
        self.vertex_from = vertex_from
        self.vertex_to = vertex_to
        self.weight = weight

    def __repr__(self):
        return f'Edge({self.vertex_from}, {self.vertex_to}, {self.weight})'


class Path:
    def __init__(self, vertices=None):
        self._vertices = [] if vertices is None else vertices

    def prepend(self, item):
        self._vertices.insert(0, item)

    def append(self, item):
        self._vertices.append(item)

    @property
    def distance(self):
        return self._vertices[-1].distance

    @property
    def path(self):
        return [vertex.label for vertex in self._vertices]

    def __repr__(self):
        return f'Path({self._vertices})'


class Graph:
    def __init__(self):
        self.vertices = []
        self.start = None
        self.end = None

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, edge):
        vertex_from = edge.vertex_from
        vertex_to = edge.vertex_to
        vertex_from.add(edge)
        if vertex_from not in self.vertices:
            self.add_vertex(vertex_from)
        if vertex_to not in self.vertices:
            self.add_vertex(vertex_to)

    def add(self, item):
        if type(item) == Vertex:
            self.add_vertex(item)
        elif type(item) == Edge:
            self.add_edge(item)
        else:
            raise InvalidGraphItemError(
                'Only vertices and edges can be added to graphs.')

    def make_undirected(self, by=lambda w: w):
        for vertex in self.vertices:
            for edge in vertex.edges:
                new_edge = Edge(
                    edge.vertex_to, edge.vertex_from, by(edge.weight))
                self.add_edge(new_edge)

    def __repr__(self):
        return str(self.vertices)


class PriorityQueue:
    def __init__(self, items, sortkey):
        self._items = items
        self._sortkey = sortkey
        self.sort()

    def __len__(self):
        return len(self._items)

    def __getitem__(self, position):
        return self._items[position]

    def sort(self):
        self._items.sort(key=self._sortkey)

    def push(self, item):
        self._items.append(item)
        self.sort()

    def popmin(self):
        return self._items.pop(0)


def dijkstra(graph):
    if graph.start is None or graph.end is None:
        raise NoGraphStartVertexError('Graph start vertex not set.')
    if graph.end is None:
        raise NoGraphEndVertexError('Graph end vertex not set.')
    start = graph.start
    end = graph.end
    start.distance = 0
    toexplore = PriorityQueue([start], sortkey=lambda v: v.distance)
    path_found = False

    while len(toexplore) != 0:
        v = toexplore.popmin()

        if v is end:
            path_found = True
            break

        for edge in v.edges:
            w = edge.vertex_to
            dist_w = v.distance + edge.weight
            if dist_w < w.distance:
                w.distance = dist_w
                w.vertex_from = v
                if w in toexplore:
                    toexplore.sort()
                else:
                    toexplore.push(w)
    if not path_found:
        raise NoPathExistsError(
            'No path exists between the start and end vertices on this graph')

    current = end
    path = Path([current])
    while current is not start:
        path.prepend(current.vertex_from)
        current = current.vertex_from
    return path
