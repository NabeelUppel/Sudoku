class Node:
    def __init__(self, idx, data=0):
        self.id = idx
        self.data = data
        self.neighbours = dict()

    def addNeighbour(self, n, weight=0):
        if n.id not in self.neighbours.keys():
            self.neighbours[n.id] = weight

    def setData(self, data):
        self.data = data

    def getNeighbours(self):
        return self.neighbours.keys()

    def getId(self):
        return self.id

    def getData(self):
        return self.data

    def getWeight(self, n):
        return self.neighbours[n.id]

    def __str__(self):
        return str(self.data) + " Connected to : " + \
               str([x.data for x in self.neighbours])


class Graph:
    totalV = 0

    def __init__(self):
        self.allNodes = dict()

    def addNodes(self, idx):
        if idx in self.allNodes:
            return None

        Graph.totalV += 1
        node = Node(idx)
        self.allNodes[idx] = node
        return node

    def addNodeData(self, idx, data):
        if idx in self.allNodes:
            node = self.allNodes[idx]
            node.setData(data)
        else:
            print("No ID to add this data")

    def addEdge(self, src, dest, wt=0):
        self.allNodes[src].addNeighbour(self.allNodes[dest], wt)
        self.allNodes[dest].addNeighbour(self.allNodes[src], wt)

    def isNeighbour(self, u, v):
        if 1 <= u <= 81 and 1 <= v <= 81 and u != v:
            if v in self.allNodes[u].getNeighbours():
                return True

        return False

    def printEdges(self):
        for idx in self.allNodes:
            node = self.allNodes[idx]
            for n in node.getNeighbours():
                print(node.getId(), "-->", self.allNodes[n].getId())

    def getNode(self, idx):
        if idx in self.allNodes:
            return self.allNodes[idx]
        return None

    def getAllNodesIDs(self):
        return self.allNodes.keys()

    def dfs(self, start):
        visited = [False] * self.totalV
        if start in self.allNodes.keys():
            self.__dfsUtility(start, visited)
        else:
            print("Start Node not found")

    def bfs(self, start):
        visited = [False] * self.totalV
        if start in self.allNodes.keys():
            self.__bfsUtility(start, visited)
        else:
            print("Start Node not found")

    def __bfsUtility(self, node_id, visited):
        queue = []
        visited = self.__setVisited(visited, node_id)
        queue.append(node_id)

        while queue:
            x = queue.pop(0)
            print(self.allNodes[x].getId())

            for i in self.allNodes[x].getNeighbours():
                idx = self.allNodes[i].getId()
                if not visited[idx]:
                    queue.append(idx)
                    visited = self.__setVisited(visited, idx)

    def __dfsUtility(self, node_id, visited):
        visited = self.__setVisited(visited, node_id)
        print(self.allNodes[node_id].getId())

        for i in self.allNodes[node_id].getNeighbours():
            if not visited[self.allNodes[i].getId()]:
                self.__dfsUtility(self.allNodes[i].getId(), visited)

    def __setVisited(self, visited, node_id):
        visited[node_id] = True
        return visited
