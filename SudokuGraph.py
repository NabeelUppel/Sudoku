from Graph import Graph
import numpy as np


class SudokuGraph:
    def __init__(self):
        self.graph = Graph()
        self.rows = 9
        self.cols = 9
        self.blocks = self.rows * self.cols
        self.__generateGraph()
        self.connectEdges()

    def __generateGraph(self):
        for b in range(1, self.blocks + 1):
            _ = self.graph.addNodes(b)

    def connectEdges(self):
        m = self.connectByMatrix()
        # NEED TO CHANGE INDICES TO SOLVE OTHER SIZES
        indices = [1, 4, 7]
        for r in range(self.rows):
            for c in range(self.cols):
                head = m[r][c]
                self.connectToRows(m, head, r)
                self.connectToColumns(head)
                if r in indices and c in indices:
                    self.miniMatrixUtility(head)

    def connectToRows(self, matrix, head, r):
        row = matrix[r]
        for x in row:
            if x != head:
                self.graph.addEdge(head, x, 1)

    def connectToColumns(self, head):
        x = head + 9
        while self.cols < x <= self.blocks:
            self.graph.addEdge(head, x, 1)
            x += 9

    def miniMatrixUtility(self, v):
        m = self.connectByMatrix()

        dx = [-1, 1, 1, -1, 0, 0, -1, 1]
        dy = [1, -1, 1, -1, 1, -1, 0, 0]
        for i in range(0, 8):
            r = np.where(m == v)[0][0] + dx[i]
            c = np.where(m == v)[1][0] + dy[i]
            if self.isValid(r, c):
                coord = m[r][c]
                node = self.graph.allNodes[coord]
                if v not in node.getNeighbours():
                    self.graph.addEdge(v, node.id, 0)

    def isValid(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return True
        return False

    def connectByMatrix(self):
        matrix = np.arange(1, self.blocks + 1).reshape(self.rows, self.cols)
        return matrix
