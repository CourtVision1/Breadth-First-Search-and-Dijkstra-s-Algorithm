from collections import defaultdict, deque

# read all the files and get the data into a flat list
vertices = open('vertices.txt')
vertexList = []
for line in vertices.readlines():
    result = [x.rstrip("\n") for x in line.split(",")]
    x = vertexList.append(result)
vertices.close()

# Get vertexList into a flat list instead of a list of lists
vertexList = [x for list in vertexList for x in list]

edges = open('edges.txt', 'r')
edgeList = []
for line in edges.readlines():
    result = [x.rstrip("\n") for x in line.split(",")]
    x = edgeList.append(result)
edges.close()


# Graph class to hold everything
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}
        self.distances2 = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance, distance2):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        # Undirected so i just did it normal and in inverse. At some point
        # I realized I only had half the distances and I didn't want
        # to break everything I already had. I just update the 2 together in
        # the functions its needed in
        self.distances[(from_node, to_node)] = distance
        self.distances2[(to_node, from_node)] = distance2


# Function for Breadth First Search
def bfs(graph, start, end):
    # Made the first key None but from then the key will be the city going from
    parents = {start: None}

    # Queue to hold adjacent cities
    queue = deque([start])

    while queue:

        # Deletes already visited cities
        city = queue.popleft()

        # Finding the neighboring cities
        for neighbor in graph[city]:
            if neighbor not in parents:
                parents[neighbor] = city
                queue.append(neighbor)
                if city == end:
                    break

    # Getting the correct path from the parents dictionary by finding the key
    path = [end]
    while parents[end] is not None:
        path.insert(0, parents[end])
        end = parents[end]

    return path


# Function for Dijkstra's
def dijkstra(graph, start):
    visited = {start: 0}
    path = {}

    cities = set(graph.nodes)

    complete_distance = graph.distances.copy()
    complete_distance.update(graph.distances2)

    # This will change source_city to the node the algorithm is looking from
    while cities:
        source_city = None
        for city in cities:
            if city in visited:
                if source_city is None:
                    source_city = city
                elif visited[city] < visited[source_city]:
                    source_city = city

        if source_city is None:
            break

        # Removes the last source_city
        cities.remove(source_city)
        current_weight = visited[source_city]

        # Gets the current closest neighbor and adds the weight
        for neighbor in graph.edges[source_city]:
            weight = current_weight + complete_distance[(source_city, neighbor)]

            # "or weight < visited[neighbor]" will separate the results from bfs
            if neighbor not in visited or weight < visited[neighbor]:
                visited[neighbor] = weight
                path[neighbor] = source_city

    return visited, path


def shortest_path(graph, start, end):
    # visited is a dictionary starting at the origin city going out to
    # all other cities with their weights using dijkstra's.
    # city_list is a dictionary with all the paths dijkstra's took.
    visited, city_list = dijkstra(graph, start)

    path = []
    current_city = end

    # Works back from the end city to find the origin
    while current_city is not None:
        path.append(current_city)
        if current_city == start:
            break
        current_city = city_list[current_city]

    # Gets the final weight from the key of the visited cities
    weight = (visited[end])

    # Path is backwards
    path.reverse()

    return path, weight


# Some functions to print the paths
def bfs_print_path(start, finish):
    nice_list = bfs(graph.edges, start, finish)
    print("The bfs path from {} to {} is:".format(start, finish, ))
    print(*nice_list, sep=" -> ")


def dijkstra_print_path(start, finish):
    nice_list, total_distance = (shortest_path(graph, start, finish))
    print("With dijkstra's algorithm the path from {} to {} is:".format(start, finish, ))
    print(*nice_list, sep=" -> ")
    print("With a total distance of: ", total_distance)


def menu():
    while 1:
        print("""\nWant to do look up anything else with the program?
        1 - Reprint the Adjacency List
        2 - Breadth First Search
        3 - Dijkstra’s Algorithm
        4 - Prim's Algorithm
        5 - Quit Program""")

        x = int(input("Enter option: "))
        while (x < 1) or (x > 5):
            print("Must be 1-5")
            x = int(input("Enter option: "))

        if x == 1:
            for node in graph.edges:
                print(node, "->", [ed for ed in graph.edges[node]])

        # I just used try and excepts instead of validating the responses
        elif x == 2:
            print("***Print cities exactly as their shown on the map!***")
            print("(If you are looking for Rimnicu Vilcea enter it as one word.)")
            start = input("Where do you want to start at? ")
            finish = input("Where is your destination? ")
            try:
                bfs_print_path(start, finish)
            except:
                print("Oops! You made a typo. Just try again.")

        elif x == 3:
            print("***Print cities exactly as their shown on the map!***")
            print("(If you are looking for Rimnicu Vilcea enter it as one word.)")
            start = input("Where do you want to start at? ")
            finish = input("Where is your destination? ")
            print(start, finish)
            try:
                dijkstra_print_path(start, finish)
            except:
                print("Oops! You made a typo. Just try again.")

        elif x == 4:
            start = input("Where do you want the minimum spanning tree to start? ")
            try:
                prim_list = prims(graph, start)

                print("Here's the mst with prim's:\n", sorted(prim_list.items(),
                                                              key=lambda x: x[1]))
            except:
                print("Oops! You made a typo. Just try again.")

        elif x == 5:
            exit()


if __name__ == '__main__':
    # Making the graph class
    graph = Graph()
    for i in vertexList:
        graph.add_node(i)
    for x, y, z in edgeList:
        graph.add_edge(x, y, int(z), int(z))

    # This is all just the required tests in the project doc
    print("Here is the unweighted undirected adjacency list: \n{}".format('-' * 50))
    for node in graph.edges:
        print(node, "->", [i for i in graph.edges[node]])

    print("\nBreadth First Search tests:\n{}".format('-' * 50))
    bfs_print_path("Arad", "Sibiu")
    print("")
    bfs_print_path("Arad", "Craiova")
    print("")
    bfs_print_path("Arad", "Bucharest")

    print("\nDijkstra’s Algorithm test:\n{}".format('-' * 50))
    dijkstra_print_path("Arad", "Bucharest")
    print("\n{}".format('-' * 50))

    print("Required tests complete\n{}".format('-' * 50))

    # Starts a menu if specific cities want to be searched to and from
    menu()
