#!/usr/bin/python

# http://webcache.googleusercontent.com/search?newwindow=1&client=ubuntu&hs=WH3&channel=fs&biw=1573&bih=804&sclient=psy-ab&q=cache%3Ahttp%3A%2F%2Ffabiensanglard.net%2FrayTracing_back_of_business_card%2Findex.php&oq=cache%3Ahttp%3A%2F%2Ffabiensanglard.net%2FrayTracing_back_of_business_card%2Findex.php&gs_l=serp.3..0l4.14543.18574.1.19003.45.16.9.6.6.7.207.1233.8j5j1.14.0....2...1c.1.27.psy-ab..61.23.641.0fjXozWL1vM&pbx=1

from math import sqrt, ceil
import random
import sys

G = [247570,280596,280600,249748,18578,18577,231184,16,16]

def Random():
    return random.random()

R = Random

def Trace(o, d, t, n):
    """ The intersection test for line [o, v] """
    t = 1e9
    m = 0
    p = -o.z/d.z

    if .01 < p:
        t = p
        n = vector(0, 0, 1)
        m = 1

    for k in range(18, -1, -1):
        for j in range(8, -1, -1):
            if G[j] & 1 << k:
                p = o + vector(-k, 0, -j-4)
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

T = Trace

def Sample(o, d):
    t = 0.0
    n = vector()

    m, t, n = Trace(o, d, t, n)

    if not m:
        return vector(.7,.6, 1) * ((1-d.z) ** 4)

    # A sphere was maybe hit
    h = o+d*t
    l = -(vector(9+R(), 9+R(), 16) + h * -1)
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
        if (ceil(h.x)+ceil(h.y)) % 2 == 1:
            x = vector(3, 1, 1)
        else:
            x = vector(3, 3, 3)
        return x*(b*.2+.1)

    # m == 2 sphere was hit
    return vector(p, p, p) + Sample(h, r) * .5

S = Sample

class vector(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def add(self, v): # +
        return vector(self.x+v.x, self.y+v.y, self.z+v.z)

    __add__ = add

    def scale(self, f): # *
        return vector(self.x*f, self.y*f, self.z*f)

    __mul__ = scale

    def dot(self, v): # %
        return self.x * v.x + self.y * v.y + self.z * v.z

    __mod__ = dot

    def cross(self, v): # ^
        return vector(self.y*v.z-self.z*v.y,
                      self.z*v.x-self.x*v.z,
                      self.x*v.y-self.y*v.x)

    __xor__ = cross

    def normalize(self): # !
        return self * (1.0/sqrt(self % self))
   
    __neg__ = normalize

    def __str__(self):
        return "Vector(%f, %f, %f)" % (self.x, self.y, self.z)

def main():
    sys.stdout.write("P6 512 512 255 ")
    
    ## ! has precedence over * ?
    g = -vector(-6, -16, 0)  # camera direction
    a = -(vector(0,0,1)^g)*.002
    b = -(g^a) * 0.002
    c = (a+b)*-256+g

    raycount = 64

    rr,gg,bb = 13, 13, 13
    for y in range(511, -1, -1):
        for x in range(511, -1, -1):
            p = vector(rr, gg, bb)
            for r in range(raycount-1, -1, -1):
                t = a*(R()-.5)*99+b*(R()-.5)*99
                p = Sample(vector(17, 16, 8)+t,
                           -(t*-1+(a*(R()+x)+b*(y+R())+c)*16)
                          )*3.5+p

            sys.stdout.write("%s%s%s" % (chr(int(p.x)), chr(int(p.y)), chr(int(p.z))))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
