# Directed Graph Data Structure
# Jacob Mosiman
# Personal Project June 2024

from ds_library import Stack, Queue, PriorityQueue


class Vertex:
    """
    Object representing a vertex in a graph.

    :param identifier:      Unique identifier for the vertex. Used to store in Graph vertices dictionary.
    :param value:           Value that the vertex will hold.
    :param adj_vert:        List containing identifiers of adjacent vertices. Default to None / empty list.
    """

    def __init__(self, identifier: str, value: object, adj_vert: dict = None):
        self.id = identifier
        self.value = value
        self.adj_dict = {} if adj_vert is None else adj_vert


class GraphException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DirectedGraph:
    """
    Directed Graph data structure. Can support weighted or unweighted edges.

    :param weighted:        Bool indicating if edges of graph are weighted. Defaults to False.
    """

    def __init__(self, weighted=False):
        self._vertices = {}
        self._size = 0
        self._weighted = weighted

    def add_vertex(self, identifier: str, value: object) -> None:
        """
        Creates a new vertex and adds it to the graph. If a vertex with that identifier already exists in the graph,
        its value is replaced. If replacing an existing vertex value, adjacent vertices will not be changed.

        :param identifier:      String representing the unique identifier of the new vertex.
        :param value:           Value that the new vertex will hold.

        :return:                None.
        """
        # If identifier already exists in graph, replace value.
        if identifier in self._vertices:
            old_vert = self._vertices[identifier]
            self._vertices[identifier] = Vertex(identifier, value, old_vert.adj_dict)
            return

        # Otherwise, add new vertex and increment size
        self._vertices[identifier] = Vertex(identifier, value)
        self._size += 1

    def remove_vertex(self, identifier: str) -> None:
        """
        Removes the vertex with the given identifier and any inbound edges.

        :param identifier:      String representing the identifier of the vertex to be removed.

        :return:                None.
        """
        # If vertex does not exist, raise exception
        if identifier not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided identifier.")

        # Remove any inbound edges
        for vertex_id in self._vertices:
            vertex = self._vertices[vertex_id]
            if identifier in vertex.adj_dict:
                del vertex.adj_dict[identifier]

        # Delete the vertex and decrement graph size
        del self._vertices[identifier]
        self._size -= 1

    def add_edge(self, source_id: str, dest_id: str, weight: int = None) -> None:
        """
        Creates a new edge between two vertices in the graph. If graph is weighted, weight must be supplied. If graph
        is not weighted, weight value will be ignored. If either of the vertices do not exist, raises exception. If edge
        already exists, does nothing.

        :param source_id:       String representing the identifier of the vertex where the edge begins.
        :param dest_id:         String representing the identifier of the vertex where the edge ends.
        :param weight:          Integer representing the weight of the edge. Applies to weighted graphs only.

        :return:                None.
        """
        # Raise exception if either vertex is not in the graph
        if source_id not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided source identifier.")
        elif dest_id not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided destination identifier.")

        source_vert = self._vertices[source_id]

        # If edge does not already exist
        if dest_id not in source_vert.adj_dict:
            # If graph is weighted and no weight was supplied, raise exception
            if self._weighted and not weight:
                raise GraphException("Error: Graph is weighted - all edges must be supplied with a weight.")
            # Otherwise, add edge - ignore weight if graph not weighted
            source_vert.adj_dict[dest_id] = weight if self._weighted else None

    def remove_edge(self, source_id: str, dest_id: str) -> None:
        """
        Removes the edge from source to destination vertices. If edge does not exist, raises exception.

        :param source_id:       String representing the identifier of the vertex where the edge begins.
        :param dest_id:         String representing the identifier of the vertex where the edge ends.

        :return:                None.
        """
        # If the edge exists, remove it
        if source_id in self._vertices:
            source_list = self._vertices[source_id].adj_dict
            if dest_id in source_list:
                del source_list[dest_id]
                return
        # Otherwise, raise exception
        raise GraphException("Error: No edge exists between the source vertex and destination vertex.")

    def edge_exists(self, source_id: str, dest_id: str) -> bool:
        """
        Returns True if the edge exists in the graph, False otherwise.

        :param source_id:       String representing the identifier of the vertex where the edge begins.
        :param dest_id:         String representing the identifier of the vertex where the edge ends.

        :return:                Boolean. True if edge exists, False otherwise.
        """
        # If outbound vert exists, check if inbound vert in adjacency list (y--> True n--> False)
        if source_id in self._vertices:
            source_vert = self._vertices[source_id]
            if dest_id in source_vert.adj_dict:
                return True

        return False

    def vertex_exists(self, identifier: str) -> bool:
        """
        Returns True if the vertex exists in the graph, False otherwise.

        :param identifier:      String representing the identifier of the vertex we are checking for.
        :return:                Boolean. True of vertex with given identifier exists, False otherwise.
        """
        if identifier in self._vertices:
            return True

        return False

    def get_adjacent_vertices(self, identifier: str) -> list | None:
        """
        Returns a list of identifiers of the adjacent vertices for the vertex assigned to the given identifier or None
        if no adjacent vertices exist. If the vertex does not exist, raises exception.

        :param identifier:      String representing the identifier of the vertex we are getting adjacent vertices of.

        :return:                List of adjacent vertices, or None if no adjacent vertices.
        """
        if identifier not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided identifier.")

        adj_vertex = self._vertices[identifier].adj_dict
        if len(adj_vertex) == 0:
            return

        return [key for key in adj_vertex]

    def depth_first_search(self, source_id: str, target_id: str) -> bool:
        """
        Uses DFS to return True if target_id node is reachable from source_id node. False if unreachable.

        :param source_id:       String representing the identifier of the vertex we are searching FROM.
        :param target_id:       String representing the identifier of the vertex we are searching FOR.

        :return:                Boolean. True if target reachable from source, False otherwise.
        """
        if source_id not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided source identifier.")
        elif target_id not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided target identifier.")

        # Init empty set (visited vertices) and stack, then push source vertex to stack
        visited_vert = set()
        stack = Stack()
        stack.push(source_id)

        # While stack is not empty, pop top vertex id
        while not stack.is_empty():
            vert_id = stack.pop()
            # If vertex hasn't been visited, add to visited list and process. If == target, return success.
            if vert_id not in visited_vert:
                visited_vert.add(vert_id)
                if vert_id == target_id:
                    return True
                # Push each adjacent vertex to the stack
                for vertex in self._vertices[vert_id].adj_dict:
                    stack.push(vertex)

        # If target vertex not found, no path exists
        return False

    def breadth_first_search(self, source_id: str, target_id: str = None) -> tuple | list:
        """
        Uses BFS to return a list of the vertices reachable from the source vertex. If a target_id is specified, will
        return a tuple containing a Boolean indicating if target is reachable and the list of all vertices reachable
        from the source vertex.

        :param source_id:       String representing the identifier of the vertex we are searching FROM.
        :param target_id:       String representing the identifier of the vertex we are searching FOR. Optional value,
                                if none supplied, will exclusively return list of all vertices reachable.

        :return:                If target_id supplied, will return tuple of (Boolean indicating target reachable, list
                                of reachable vertices). Otherwise, will exclusively return list of reachable vertices.
        """
        if source_id not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided source identifier.")
        elif target_id and target_id not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided target identifier.")

        # Init empty set (visited vertices) and queue, then enqueue source vertex
        visited_vert = set()
        q = Queue()
        q.enqueue(source_id)
        target_found = False        # Used if target_id supplied

        while not q.is_empty():
            vert_id = q.dequeue()
            # If target_id supplied and current vertex matches, flag target found as True
            if target_id and vert_id == target_id:
                target_found = True
            # Add current vertex to set of visited vertices
            visited_vert.add(vert_id)
            # For each vertex adjacent to current vertex, add to queue if not yet visited
            for vertex in self._vertices[vert_id].adj_dict:
                if vertex not in visited_vert:
                    q.enqueue(vertex)

        # Create a list of the visited vertices
        reachable_vert = [vert for vert in visited_vert]
        # If searching for a target, return tuple. Otherwise, return list.
        if target_id:
            return target_found, reachable_vert
        return reachable_vert

    def min_path(self, source_id: str) -> tuple:
        """
        Calculates the minimum distance from vertex of supplied source_id to all other reachable vertices in the graph.
        Returns a dictionary containing a list of vertices from nearest to farthest, and a dictionary containing each
        vertex and its associated distance.

        :param source_id:   String representing the identifier of the vertex we are searching from.

        :return:            Tuple containing a list of vertices ordered from the smallest distance to the largest, and a
                            dictionary containing each vertex and its associated distance as key-value pairs.
        """
        # If graph not weighted, raise exception
        if not self._weighted:
            raise GraphException("Error: min_path() requires a weighted graph. Current graph unweighted.")
        elif source_id not in self._vertices:
            raise GraphException("Error: There is no vertex in the graph with the provided identifier.")

        # Init dictionary of visited vertices and priority queue of vertices to check. Add source vertex to priority q.
        visited_vert = {}
        p_queue = PriorityQueue()
        p_queue.enqueue(0, source_id)

        # While the priority queue is not empty, dequeue and assign vertex's distance and ID to variables
        while not p_queue.is_empty():
            distance, vertex = p_queue.dequeue()
            # If vertex hasn't been visited, add to visited_vert and enqueue adjacent vertices
            if vertex not in visited_vert:
                visited_vert[vertex] = distance
                adj_vert = self._vertices[vertex].adj_dict
                for vert in adj_vert:
                    # Set adjacent vertex's priority (distance) to dequeued vertex's distance + distance of adj edge
                    vert_priority = distance + adj_vert[vert]
                    p_queue.enqueue(vert_priority, vert)
