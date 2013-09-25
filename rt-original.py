#!/usr/bin/python

from math import sqrt, ceil
import random
import sys

G = [247570,280596,280600,249748,18578,18577,231184,16,16]

def R():
    return random.random()

def T(o, d, t, n):
    """ The intersection test for line [o, v] """
    t = 1e9
    m = 0
    p = -o.z/d.z

    if .01 < p:
        t = p
        n = v(0, 0, 1)
        m = 1

    for k in range(18, -1, -1):
        for j in range(8, -1, -1):
            if G[j] & 1 << k:
                p = o + v(-k, 0, -j-4)
                b = p % d
                c = p % p - 1
                q = b*b-c

                if q > 0:
                    s = -b-sqrt(q)

                    if s < t and s > 0.01: ## XXX rewrite 
                        t = s
                        n = -(p+d*t)
                        m = 2

    return m, t, n

def S(o, d):
    t = 0.0
    n = v()

    m, t, n = T(o, d, t, n)

    if not m:
        return v(.7,.6, 1) * ((1-d.z) ** 4)

    # A sphere was maybe hit
    h = o+d*t
    l = -(v(9+R(), 9+R(), 16) + h * -1)
    r = d + n * (n%d*-2)

    # lambertian factor
    b = l % n

    # illumination factor
    if b < 0 or T(h, l, t, n)[0]:
        b = 0

    # calculate the color 'p' 
    p = (l % r * (1 if b > 0 else 0))**99

    if m %2 == 1:
        h = h * .2
        if (ceil(h.x)+ceil(h.y)) % 2 == 1:
            x = v(3, 1, 1)
        else:
            x = v(3, 3, 3)
        return x*(b*.2+.1)

    # m == 2 sphere was hit
    return v(p, p, p) + S(h, r) * .5

class v(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, r): # +
        return v(self.x+r.x, self.y+r.y, self.z+r.z)

    def __mul__(self, f): # *
        return v(self.x*f, self.y*f, self.z*f)

    def __mod__(self, r): # %
        return self.x * r.x + self.y * r.y + self.z * r.z

    def __xor__(self, r): # ^
        return v(self.y*r.z-self.z*r.y,
                      self.z*r.x-self.x*r.z,
                      self.x*r.y-self.y*r.x)

    def __neg__(self): # -
        return self * (1.0/sqrt(self % self))

def main():
    sys.stdout.write("P6 512 512 255 ")

    g = -v(-6, -16, 0)  # camera direction
    a = -(v(0,0,1)^g)*.002
    b = -(g^a) * 0.002
    c = (a+b)*-256+g

    raycount = 64

    for y in range(511, -1, -1):
        for x in range(511, -1, -1):
            p = v(13, 13, 13)
            for r in range(raycount-1, -1, -1):
                t = a*(R()-.5)*99+b*(R()-.5)*99
                p = S(v(17, 16, 8)+t,
                           -(t*-1+(a*(R()+x)+b*(y+R())+c)*16)
                          )*3.5+p

            sys.stdout.write("%s%s%s" % (chr(int(p.x)), chr(int(p.y)), chr(int(p.z))))

if __name__ == '__main__':
    main()
