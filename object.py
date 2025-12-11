import pygame as pg
import math

class Object():
    def __init__(self, startPos, components, connections, color = (255, 255, 255)):
        nullVector = startPos
        relativeComps = []
        for comp in components:
            relativeComps.append(comp + nullVector)
        self.components = relativeComps
        self.center = nullVector
        self.connections = connections
        self.color = color

    @staticmethod
    def getSquare(size):
        comps = [pg.Vector3(1, 1, -1), pg.Vector3(-1, 1, -1), pg.Vector3(1, -1, -1), pg.Vector3(-1, -1, -1), pg.Vector3(1, 1, 1), pg.Vector3(-1, 1, 1), pg.Vector3(1, -1, 1), pg.Vector3(-1, -1, 1)]
        connections = [[0, 1], [0, 2], [1, 3], [2, 3], [0, 4], [1, 5], [2, 6], [3, 7], [4, 6], [4, 5], [5, 7], [6, 7]]
        
        for i in range(len(comps)):
            comps[i] *= size
        return [comps, connections]
    
    @staticmethod
    def getRectangle(width, length, height):
        comps = [pg.Vector3(width, length, -height), pg.Vector3(-width, length, -height), pg.Vector3(width, -length, -height), pg.Vector3(-width, -length, -height), pg.Vector3(width, length, height), pg.Vector3(-width, length, height), pg.Vector3(width, -length, height), pg.Vector3(-width, -length, height)]
        connections = [[0, 1], [0, 2], [1, 3], [2, 3], [0, 4], [1, 5], [2, 6], [3, 7], [4, 6], [4, 5], [5, 7], [6, 7]]
        return [comps, connections]
    
    @staticmethod
    def getSphere(radius, rings=12, segments=24):
        comps = []
        connections = []

        for i in range(rings + 1):
            theta = math.pi * i / rings
            for j in range(segments):
                phi = 2 * math.pi * j / segments 
                x = radius * math.sin(theta) * math.cos(phi)
                y = radius * math.sin(theta) * math.sin(phi)
                z = radius * math.cos(theta)
                comps.append(pg.Vector3(x, y, z))
        for i in range(rings + 1):
            for j in range(segments):
                index = i * segments + j
                next_index = i * segments + (j + 1) % segments
                connections.append([index, next_index])
        for i in range(rings):
            for j in range(segments):
                index = i * segments + j
                below_index = (i + 1) * segments + j
                connections.append([index, below_index])
        return [comps, connections]

