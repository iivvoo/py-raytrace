#!/usr/bin/python

# http://webcache.googleusercontent.com/search?newwindow=1&client=ubuntu&hs=WH3&channel=fs&biw=1573&bih=804&sclient=psy-ab&q=cache%3Ahttp%3A%2F%2Ffabiensanglard.net%2FrayTracing_back_of_business_card%2Findex.php&oq=cache%3Ahttp%3A%2F%2Ffabiensanglard.net%2FrayTracing_back_of_business_card%2Findex.php&gs_l=serp.3..0l4.14543.18574.1.19003.45.16.9.6.6.7.207.1233.8j5j1.14.0....2...1c.1.27.psy-ab..61.23.641.0fjXozWL1vM&pbx=1

from math import sqrt, ceil
import random

G = [247570,280596,280600,249748,18578,18577,231184,16,16]

def Random():
    return random.random()

R = Random

def Trace(o, d, t, n):
    """ The intersection test for line [o, v] """
    t = 1e9
    m = 0
    p = -o.z/d.z

    for k in range(18, -1, -1):
        for j in range(8, -1, -1):
            if G[j] & 1 << k:
                p = o.add(vector(-k, 0, -j-4))
                b = p.dot(d)
                c = p.dot(p)-1
                q = b*b-c

                if q > 0:
                    s = -b-sqrt(q)

                    if s < t and s > 0.1: ## XXX rewrite 
                        t = s
                        n = p.add(d.scale(t)).normalize()
                        m = 2

    return m, t, n

T = Trace

def Sample(o, d):
    t = 0.0
    n = vector()

    m, t, n = Trace(o, d, t, n)

    if not m:
        ## pow(1-d.z, 4) XXX
        return vector(.7,.6, 1).scale(1-d.z ** 4)

    # A sphere was maybe hit
    h = o.add(d).scale(t)
    l = vector(9+R(), 9+R(), 16).add(h).scale(-1).normalize()
    ## not sure about % * precedence
    r = d.add(n.scale(n.dot(d.scale(-2))))

    # lambertian factor
    b = l.dot(n)

    # illumination factor
    if b < 0 or Trace(h, l, t, n)[0]:
        b = 0

    # calculate the color 'p' 
    p = l.dot(r.scale(1 if b > 0 else 0))**99

    if m == 1:
        h = h.scale(.2)
        if int(ceil(h.x)+ceil(h.y) == 1):
            x = vector(3, 1, 1)
        else:
            x = vector(3,3,3)
        return x.scale(b.scale(.2).add(.1))

    # m == 2 sphere was hit
    return vector(p, p, p).add(Sample(h, r).scale(.5))

S = Sample

class vector(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

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

    __ixor__ = cross

    def normalize(self): # !
        # print "!", self.x, self.y, self.z
        return self.scale(1/sqrt(self.dot(self)))
   
    __not__ = normalize

    def __str__(self):
        print "Vector(%f, %f, %f)" % (self.x, self.y, self.z)

def main():
    print "P6 512 512 255",

    ## ! has precedence over * ?
    g = vector(-6, 16, 0).normalize()  # camera direction
    a = vector(0, 0, 1).cross(g).normalize().scale(0.002) # camera up vec
    b = g.cross(a).normalize().scale(0.002) # right vector
    c = a.add(b).scale(-256).add(g) # ??

    for y in range(511, -1, -1):
        for x in range(511, -1, -1):
            p = vector(13, 13, 13)
            for r in range(63, -1, -1):
                t = a.scale(R()-.5).scale(99).add(b.scale(R()-.5).scale(99))

                p = Sample(vector(17, 16, 8).add(t),
                           t.scale(-1).add(a.scale(R()+x).add(b.scale(y+R()).add(c))).scale(16)).scale(3.5).add(p)

            print p
            print "%s%s%s" % (chr(int(p.x)), chr(int(p.y)), chr(int(p.z)))

if __name__ == '__main__':
    main()
