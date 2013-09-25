#!/usr/bin/python

from math import sqrt, ceil
import random
import sys

# Define a vector class with constructor and operator: 'v'
class v(object):
    # Vector has three float attributes.
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, r): # +, vector add
        return v(self.x+r.x, self.y+r.y, self.z+r.z)

    def __mul__(self, f): # *, vector scaling
        return v(self.x*f, self.y*f, self.z*f)

    def __mod__(self, r): # %, vector dot product
        return self.x * r.x + self.y * r.y + self.z * r.z

    def __xor__(self, r): # ^, vector cross product
        return v(self.y*r.z-self.z*r.y,
                      self.z*r.x-self.x*r.z,
                      self.x*r.y-self.y*r.x)

    def __neg__(self): # -, Used later for normalizing the vector. 'not' cannot be used
        return self * (1.0/sqrt(self % self))

# The set of sphere positions describing the world.
# Those integers are in fact bit vectors.
G = [247570,280596,280600,249748,18578,18577,231184,16,16]

def R():
    return random.random()

def T(o, d, t, n):
    """
       The intersection test for line [o,v].
       Return 2 if a hit was found (and also return distance t and bouncing ray n).
       Return 0 if no hit was found but ray goes upward
       Return 1 if no hit was found but ray goes downward
    """
    t = 1e9
    m = 0
    p = -o.z/d.z

    if .01 < p:
        t = p
        n = v(0, 0, 1)
        m = 1

    # The world is encoded in G, with 9 lines and 19 columns
    for k in range(18, -1, -1): # For each columns of objects
        for j in range(8, -1, -1): # For each line on that columns
            if G[j] & 1 << k: # For this line j, is there a sphere at column i ?
                # There is a sphere but does the ray hit it ?
                p = o + v(-k, 0, -j-4)
                b = p % d
                c = p % p - 1
                q = b*b-c

                # Does the ray hit the sphere ?
                if q > 0:
                    # It does, compute the distance camera-sphere
                    s = -b-sqrt(q)

                    if 0.01 < s < t:
                        # So far this is the minimum distance, save it. And also compute the bouncing ray vector into 'n'
                        t = s
                        n = -(p+d*t)
                        m = 2

    return m, t, n

def S(o, d):
    """
        (S)ample the world and return the pixel color for
         a ray passing by point o (Origin) and d (Direction)
    """
    t = 0.0
    n = v()

    # Search for an intersection ray Vs World.
    m, t, n = T(o, d, t, n)

    if not m: # m == 0
        # No sphere found and the ray goes upward: Generate a sky color
        return v(.7,.6, 1) * ((1-d.z) ** 4)

    # A sphere was maybe hit

    h = o+d*t # h = intersection coordinate
    l = -(v(9+R(), 9+R(), 16) + h * -1) # 'l' = direction to light (with random delta for soft-shadows).
    r = d + n * (n%d*-2) # r = The half-vector

    # lambertian factor
    b = l % n

    # illumination factor (lambertian coefficient > 0 or in shadow)?
    if b < 0 or T(h, l, t, n)[0]:
        b = 0

    # calculate the color 'p' with diffuse and specular component
    p = (l % r * (1 if b > 0 else 0))**99

    if m %2 == 1: # m -- 1
        h = h * .2 # No sphere was hit and the ray was going downward: Generate a floor color
        return(v(3,1,1)if(ceil(h.x)+ceil(h.y))%2 else v(3,3,3))*(b*.2+.1)

    # m == 2 sphere was hit. Cast an ray bouncing from the sphere surface.
    return v(p, p, p) + S(h, r) * .5 # Attenuate color by 50% since it is bouncing (* .5)


if __name__ == '__main__':
    # The main function. It generates a PPM image to stdout.
    # Usage of the program is hence: pypy rt.py > erk.ppm
    sys.stdout.write("P6 512 512 255 ")

    # the - is for normalizing each vector with '-' operator
    g = -v(-6, -16, 0)  # camera direction
    a = -(v(0,0,1)^g)*.002 # Camera up vector...Seem Z is pointing up :/ WTF !
    b = -(g^a) * 0.002 # The right vector, obtained via traditional cross-product
    c = (a+b)*-256+g # WTF ? See https://news.ycombinator.com/item?id=6425965 for more.

    for y in range(511, -1, -1):
        for x in range(511, -1, -1):
            # reuse the vector class to store not XYZ but a RGB pixel color
            p = v(13, 13, 13)

            # cast 64 rays per pixel (For blur (stochastic sampling) and soft-shadows.
            for r in range(63, -1, -1):
                # The delta to apply to the origin of the view (For Depth of View blur).
                t = a*(R()-.5)*99+b*(R()-.5)*99
                # Set the camera focal point v(17,16,8) and Cast the ray
                # Accumulate the color returned in the p variable
                p = S(v(17, 16, 8)+t,
                           -(t*-1+(a*(R()+x)+b*(y+R())+c)*16) # Ray Direction with random deltas
                                                              # for stochastic sampling
                          )*3.5+p # +p for color accumulation

            sys.stdout.write("%c%c%c" % (int(p.x), int(p.y), int(p.z)))
