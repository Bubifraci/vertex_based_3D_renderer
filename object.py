import pygame as pg
import math

class Object():
    def __init__(self, startPos, components, connections):
        nullVector = startPos
        relativeComps = []
        for comp in components:
            relativeComps.append(comp + nullVector)
        self.components = relativeComps
        self.center = nullVector
        self.connections = connections

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

    @staticmethod
    def getRomanBust(size=1.0):
        """
        Returns a simple bust-like wireframe:
        - pedestal
        - upper torso / shoulders
        - neck
        - stylized head (rings)
        All scaled by `size`.
        """
        comps = []
        connections = []

        s = float(size)

        # ---------- PEDESTAL (simple box) ----------
        base_width  = 0.6 * s
        base_depth  = 0.4 * s
        y_base_bot  = -0.5 * s
        y_base_top  = -0.3 * s

        # 0–3: bottom rectangle (pedestal)
        comps.extend([
            pg.Vector3( base_width, y_base_bot, -base_depth),  # 0
            pg.Vector3(-base_width, y_base_bot, -base_depth),  # 1
            pg.Vector3( base_width, y_base_bot,  base_depth),  # 2
            pg.Vector3(-base_width, y_base_bot,  base_depth),  # 3
        ])
        # 4–7: top rectangle (pedestal)
        comps.extend([
            pg.Vector3( base_width, y_base_top, -base_depth),  # 4
            pg.Vector3(-base_width, y_base_top, -base_depth),  # 5
            pg.Vector3( base_width, y_base_top,  base_depth),  # 6
            pg.Vector3(-base_width, y_base_top,  base_depth),  # 7
        ])

        # Pedestal edges
        connections += [
            [0, 1], [0, 2], [1, 3], [2, 3],  # bottom
            [4, 5], [4, 6], [5, 7], [6, 7],  # top
            [0, 4], [1, 5], [2, 6], [3, 7],  # verticals
        ]

        # ---------- TORSO / SHOULDERS (trapezoid block) ----------
        chest_width    = 0.7 * s * 0.5  # half width
        shoulder_width = 0.9 * s * 0.5
        torso_depth    = 0.35 * s
        y_chest        = -0.1 * s
        y_shoulder     =  0.1 * s

        # 8–11: chest layer
        comps.extend([
            pg.Vector3( chest_width, y_chest, -torso_depth),  # 8
            pg.Vector3(-chest_width, y_chest, -torso_depth),  # 9
            pg.Vector3( chest_width, y_chest,  torso_depth),  # 10
            pg.Vector3(-chest_width, y_chest,  torso_depth),  # 11
        ])

        # 12–15: shoulders layer (wider)
        comps.extend([
            pg.Vector3( shoulder_width, y_shoulder, -torso_depth),  # 12
            pg.Vector3(-shoulder_width, y_shoulder, -torso_depth),  # 13
            pg.Vector3( shoulder_width, y_shoulder,  torso_depth),  # 14
            pg.Vector3(-shoulder_width, y_shoulder,  torso_depth),  # 15
        ])

        # Torso edges: chest & shoulders loops + verticals
        connections += [
            # chest loop
            [8, 9], [8,10], [9,11], [10,11],
            # shoulders loop
            [12,13], [12,14], [13,15], [14,15],
            # verticals chest -> shoulders
            [8,12], [9,13], [10,14], [11,15],
            # connect pedestal to chest center-ish
            [4,8], [5,9], [6,10], [7,11],
        ]

        # ---------- NECK (cylindrical ring) ----------
        neck_radius     = 0.18 * s
        y_neck_base     = 0.2 * s
        y_neck_top      = 0.32 * s
        neck_segments   = 8

        neck_base_start = len(comps)
        for k in range(neck_segments):
            angle = 2.0 * math.pi * k / neck_segments
            x = neck_radius * math.cos(angle)
            z = neck_radius * math.sin(angle)
            comps.append(pg.Vector3(x, y_neck_base, z))

        neck_top_start = len(comps)
        for k in range(neck_segments):
            angle = 2.0 * math.pi * k / neck_segments
            x = neck_radius * math.cos(angle)
            z = neck_radius * math.sin(angle)
            comps.append(pg.Vector3(x, y_neck_top, z))

        # Neck ring connections
        for k in range(neck_segments):
            k_next = (k + 1) % neck_segments
            # bottom ring
            connections.append([neck_base_start + k, neck_base_start + k_next])
            # top ring
            connections.append([neck_top_start + k, neck_top_start + k_next])
            # vertical between base and top
            connections.append([neck_base_start + k, neck_top_start + k])

        # Connect neck base to shoulders center area (roughly)
        # use shoulder midpoints: average of 12 & 13 for back, 14 & 15 for front
        shoulder_mid_back  = (12, 13)
        shoulder_mid_front = (14, 15)
        # pick a couple of neck base points to connect
        connections.append([neck_base_start + 0, shoulder_mid_back[0]])
        connections.append([neck_base_start + neck_segments//2, shoulder_mid_front[0]])

        # ---------- HEAD (two rings: mid + top) ----------
        head_radius       = 0.32 * s
        head_top_radius   = 0.18 * s
        y_head_mid        = 0.50 * s
        y_head_top        = 0.68 * s
        head_segments     = 8

        head_mid_start = len(comps)
        for k in range(head_segments):
            angle = 2.0 * math.pi * k / head_segments
            x = head_radius * math.cos(angle)
            z = head_radius * math.sin(angle)
            comps.append(pg.Vector3(x, y_head_mid, z))

        head_top_start = len(comps)
        for k in range(head_segments):
            angle = 2.0 * math.pi * k / head_segments
            x = head_top_radius * math.cos(angle)
            z = head_top_radius * math.sin(angle)
            comps.append(pg.Vector3(x, y_head_top, z))

        # Head ring connections
        for k in range(head_segments):
            k_next = (k + 1) % head_segments
            # mid head ring
            connections.append([head_mid_start + k, head_mid_start + k_next])
            # top head ring
            connections.append([head_top_start + k, head_top_start + k_next])
            # verticals
            connections.append([head_mid_start + k, head_top_start + k])

        # Connect head to neck top (simple center line)
        neck_center_top_index = neck_top_start  # any point, they’re all around (0, y, 0)
        head_center_mid_index = head_mid_start  # likewise
        connections.append([neck_center_top_index, head_center_mid_index])

        return [comps, connections]
