import pygame as pg
import object as obj
import vector_space as vecs
import math
import numpy as np

screen_width = 800
screen_height = 600

screen = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

centerX = screen_width/2
centerY = screen_height/2

def init():
    global screen
    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height))

def render(cameraPlane):
    global screen
    screen.fill((0, 0, 0))
    square = obj.Object(pg.Vector3(0, 0, 0), [pg.Vector3(1, 1, 0), pg.Vector3(-1, 1, 0), pg.Vector3(1, -1, 0), pg.Vector3(-1, -1, 0), pg.Vector3(1, 1, 1), pg.Vector3(-1, 1, 1), pg.Vector3(1, -1, 1), pg.Vector3(-1, -1, 1)], [[0, 1], [0, 2], [1, 3], [2, 3], [0, 4], [1, 5], [2, 6], [3, 7], [4, 6], [4, 5], [5, 7], [6, 7]])
    for connection in square.connections:
        v1_proj = orthogonal_projection(cameraPlane, square.components[connection[0]])
        v2_proj = orthogonal_projection(cameraPlane, square.components[connection[1]])

        vec_1_2d = toTwoDim(cameraPlane, v1_proj)
        vec_2_2d = toTwoDim(cameraPlane, v2_proj)
        pg.draw.line(screen, WHITE, vec_1_2d, vec_2_2d)
    pg.display.update()

def toTwoDim(vecs: vecs.VectorSpace, vec: pg.Vector3, scale = 100):
    global centerX, centerY
    normalVector = crossProduct(vecs.spanVectors[0], vecs.spanVectors[1])/vectorNorm(crossProduct(vecs.spanVectors[0], vecs.spanVectors[1]), 3)
    p0 = vecs.spanVectors[0] + vecs.spanVectors[1]
    r = vec - p0
    rotationMatrix = np.array([
    [vecs.spanVectors[0].x, vecs.spanVectors[0].y, vecs.spanVectors[0].z],
    [vecs.spanVectors[1].x, vecs.spanVectors[1].y, vecs.spanVectors[1].z],
    [normalVector.x,        normalVector.y,        normalVector.z]
    ])
    rNumPy = np.array([r.x, r.y, r.z])
    rotatedVector = rotationMatrix.T.dot(rNumPy)

    sx = rotatedVector[0] * scale + centerX
    sy = -rotatedVector[1] * scale + centerY

    return pg.Vector2(sx, sy)

def orthogonal_projection(vecs_destination: vecs.VectorSpace, vecInOrigin: pg.Vector3):
    projectedVector = pg.Vector3(0, 0, 0)
    for i in range(vecs_destination.dimensions):
        projectedVector += vecs_destination.spanVectors[i] * scalarProduct(vecs_destination.spanVectors[i], vecInOrigin, 3)
    return projectedVector

def vectorNorm(vec, dimensions):
    if(dimensions == 3):
        return math.sqrt(math.pow(vec.x, 2)+math.pow(vec.y, 2)+math.pow(vec.z, 2))
    else:
        return math.sqrt(math.pow(vec.x, 2)+math.pow(vec.y, 2))
    
def crossProduct(vec1, vec2):
    return pg.Vector3(
        vec1.y * vec2.z - vec1.z * vec2.y,
        vec1.z * vec2.x - vec1.x * vec2.z,
        vec1.x * vec2.y - vec1.y * vec2.x
    )


def scalarProduct(vec1, vec2, dimensions):
    product = vec1.x * vec2.x + vec1.y * vec2.y
    if(dimensions > 2):
        product += vec1.z * vec2.z
    return product

def ThreeDRotation(angle, vector, fixed):
    fixed = fixed.lower()
    rotationMatrix = None
    if(fixed == "x"):
        rotationMatrix = np.array([
        [1, 0, 0],
        [0, math.cos(angle), math.sin(angle)],
        [0, -math.sin(angle), math.cos(angle)]
        ])
    elif(fixed == "y"):
        rotationMatrix = np.array([
        [math.cos(angle), 0, -math.sin(angle)],
        [0, 1, 0],
        [math.sin(angle), 0, math.cos(angle)]
        ])
    elif(fixed == "z"):
        rotationMatrix = np.array([
        [math.cos(angle), math.sin(angle), 0],
        [-math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
        ])
    else:
        return vector
    npVector = np.array([vector.x, vector.y, vector.z])
    rotatedVector = rotationMatrix.dot(npVector)
    return pg.Vector3(rotatedVector[0], rotatedVector[1], rotatedVector[2])

init()
running = True
clock = pg.time.Clock()
i = 0
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    angle = i * 0.01
    spanVec1 = ThreeDRotation(angle, ThreeDRotation(angle, pg.Vector3(1, 0, 1), "x"), "y")
    spanVec2 = ThreeDRotation(angle,ThreeDRotation(angle, pg.Vector3(1, 1, 0), "x"), "y")
    twoDPlane = vecs.VectorSpace([spanVec1, spanVec2])
    render(twoDPlane)
    clock.tick(60)
    i = i+1
pg.quit()