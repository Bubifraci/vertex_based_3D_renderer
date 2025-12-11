import pygame as pg

class VectorSpace:
    def __init__(self, spanVectors):
        self.spanVectors = spanVectors
        self.dimensions = len(spanVectors)