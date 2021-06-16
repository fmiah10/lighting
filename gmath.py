import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 3

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    iAmbient = calculate_ambient(ambient, areflect)
    iDiffuse = calculate_diffuse(light, dreflect, normal)
    iSpecular = calculate_specular(light, sreflect, view, normal)
    i = [0, 0, 0]
    for k in range(len(i)):
        i[k] = int(iAmbient[k]) + int(iDiffuse[k]) + int(iSpecular[k])
    return limit_color(i)

def calculate_ambient(alight, areflect):
    if type(alight) != list and type(areflect) != list:
        return alight * areflect
    iAmbient = [0, 0, 0]
    for i in range(len(alight)):
        iAmbient[i] = alight[i] * areflect[i]
    return iAmbient

def calculate_diffuse(light, dreflect, normal):
    lightVector = light[LOCATION]
    lightColor = light[COLOR]
    normalize(lightVector)
    normalize(normal)
    prod = dot_product(normal, lightVector)
    iDiffuse = [0, 0, 0]
    for i in range(len(iDiffuse)):
        iDiffuse[i] = lightColor[i] * dreflect[i] * prod
    return iDiffuse

def calculate_specular(light, sreflect, view, normal):
    lightVector = light[LOCATION]
    lightColor = light[COLOR]
    normalize(lightVector)
    normalize(normal)
    normalize(view)
    r = [0, 0, 0]
    for i in range(len(r)):
        r[i] = ( 2 * normal[i] * (dot_product(normal, lightVector)) ) - lightVector[i]
    iSpecular = [0, 0, 0]
    for i in range(len(iSpecular)):
        iSpecular[i] = ( lightColor[i] * sreflect[i] * ((dot_product(r, view)) ** SPECULAR_EXP) )
    return iSpecular

def limit_color(color):
    for i in range(len(color)):
        if color[i] < 0:
            color[i] = 0
        elif color[i] > 255:
            color[i] = 255
        else:
            color[i] = int(color[i])
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
