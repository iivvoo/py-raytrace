#!/usr/bin/python

from math import sqrt, ceil
from random import random
import sys

world = [
"0000000000000010000",  # "              1    ",
"0000000000000010000",  # "              1    ",
"0111000011100010000",  # " 111    111   1    ",
"0000100100010010001",  # "    1  1   1  1   1",
"0000100100010010010",  # "    1  1   1  1  1 ",
"0111100111110010100",  # " 1111  11111  1 1  ",
"1000100100000011000",  # "1   1  1      11   ",
"1000100100000010100",  # "1   1  1      1 1  ",
"0111100011100010010",  # " 1111   111   1  1 ",
]

ivo_world = [
"1111000000000000000",
"0110000000000000000",
"0110000000000000000",
"0110000000000000000",
"0110110000110011100",
"0110011001100110110",
"0110011001101100011",
"0110001111000110110",
"1111000110000011100",
]

# G describes a 19 column 9 row "world" containing spheres, where a 1-bit is a sphere
G = [int(l, 2) for l in reversed(world)]

def Trace(o, d, t, n):
    """ The intersection test for line [o, v] """
    t = 1e9
    m = 0
    p = -o.z/d.z

    if .01 < p:
        t = p
        n = vector(0, 0, 1)
        m = 1

    for k in range(18, -1, -1): # 19 columns of possible spheres
        for j in range(8, -1, -1): # 9 rows of possible spheres
            if G[j] & 1 << k: # is the specific bit set? Draw a sphere
                p = o + vector(-k, 0, -j-4)
                b = p % d
                c = p % p - 1
                q = b*b-c

                # .. only if the current ray hits it
                if q > 0:
                    s = -b-sqrt(q)

                    if 0.01 < s < t:
                        t = s
                        n = -(p+d*t)
                        m = 2

    return m, t, n

def Sample(o, d):
    t = 0.0
    n = vector()

    m, t, n = Trace(o, d, t, n)

    if not m:
        return vector(.7,.6, 1) * ((1-d.z) ** 4)

    # A sphere was maybe hit
    h = o+d*t
    l = -(vector(9+random(), 9+random(), 16) + h * -1)
    r = d + n * (n%d*-2)

    # lambertian factor
    b = l % n

    # illumination factor
    if b < 0 or Trace(h, l, t, n)[0]:
        b = 0

    # calculate the color 'p' 
    p = (l % r * (1 if b > 0 else 0))**99

    if m %2 == 1:
        h = h * .2
        # red or white tile
        if (ceil(h.x)+ceil(h.y)) % 2 == 1:
            x = vector(3, 1, 1)
        else:
            x = vector(3, 3, 3)
        return x*(b*.2+.1)

    # m == 2 sphere was hit
    return vector(p, p, p) + Sample(h, r) * .5

class vector(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, v): # +, add vector
        return vector(self.x+v.x, self.y+v.y, self.z+v.z)

    def __mul__(self, f): # *, scale vector
        return vector(self.x*f, self.y*f, self.z*f)

    def __mod__(self, v): # %, dot product
        return self.x * v.x + self.y * v.y + self.z * v.z

    def __xor__(self, v): # ^, cross product
        return vector(self.y*v.z-self.z*v.y,
                      self.z*v.x-self.x*v.z,
                      self.x*v.y-self.y*v.x)

    def __neg__(self): # -, normalization
        return self * (1.0/sqrt(self % self))

    def __str__(self):
        return "Vector(%f, %f, %f)" % (self.x, self.y, self.z)

class color(vector):
    pass


def main():
    # print the ppm header (512x512 pixels, 255 colors)
    sys.stdout.write("P6 512 512 255 ")

    g = -vector(-6, -16, 0)  # camera direction
    a = -(vector(0,0,1)^g)*.002 # camera up vector. Things are a bit reversed
    b = -(g^a) * 0.002
    c = (a+b)*-256+g

    # where's the viewer located
    viewpoint = vector(17, 16, 8)

    # start with a nearly black color
    rr,gg,bb = 13, 13, 13
    for y in range(511, -1, -1): # rows
        for x in range(511, -1, -1): # colums
            p = color(rr, gg, bb)
            for r in range(63, -1, -1): # 64 rays per pixel
                t = a*(random()-.5)*99+b*(random()-.5)*99
                p = Sample(viewpoint+t,
                           -(t*-1+(a*(random()+x)+b*(y+random())+c)*16)
                          )*3.5+p

            sys.stdout.write("%c%c%c" % (int(p.x), int(p.y), int(p.z)))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
