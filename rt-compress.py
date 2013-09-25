#!/usr/bin/python
from math import sqrt, ceil
import random,sys
R,f,i,e,w,G=random.random,float,int,range,sys.stdout.write,[247570,280596,280600,249748,18578,18577,231184,16,16]
def T(o,d,t,n):
 t,m,p=1e9,0,-o.z/d.z
 if .01<p:t,n,m=p,v(0,0,1),1
 for k in e(18, -1, -1):
  for j in e(8, -1, -1):
   if G[j]&1<<k:
    p=o+v(-k,0,-j-4)
    b,c=p%d,p%p-1
    q=b*b-c
    if q>0:
     s=-b-sqrt(q)
     if .01<s<t: t,n,m=s,-(p+d*s),2
 return m,t,n
def S(o,d):
 t,n=0.,v()
 m,t,n=T(o,d,t,n)
 if not m:return v(.7,.6,1)*((1-d.z)**4)
 h=o+d*t
 l,r=-(v(9+R(),9+R(),16)+h*-1),d+n*(n%d*-2)
 b=l%n
 if b<0 or T(h,l,t,n)[0]:b=0
 p=(l%r*(b>0))**99
 if m%2:
  h=h*.2
  if(ceil(h.x)+ceil(h.y))%2:
   x=v(3,1,1)
  else:
   x=v(3,3,3)
  return x*(b*.2+.1)
 return v(p,p,p)+S(h,r)*.5
class v(object):
 def __init__(s,x=0.,y=0.,z=0.):s.x,s.y,s.z=f(x),f(y),f(z)
 def __add__(s,r):return v(s.x+r.x,s.y+r.y,s.z+r.z)
 def __mul__(s,f):return v(s.x*f,s.y*f,s.z*f)
 def __mod__(s,r):return s.x*r.x+s.y*r.y+s.z*r.z
 def __xor__(s,r):return v(s.y*r.z-s.z*r.y,s.z*r.x-s.x*r.z,s.x*r.y-s.y*r.x)
 def __neg__(s):return s*(1./sqrt(s%s))
w("P6 512 512 255 ")
g=-v(-6,-16,0)
a=-(v(0,0,1)^g)*.002
b=-(g^a)*.002
c=(a+b)*-256+g
for y in e(511, -1, -1):
 for x in e(511, -1, -1):
  p=v(13,13,13)
  for r in e(63,-1,-1):
   t=a*(R()-.5)*99+b*(R()-.5)*99
   p=S(v(17,16,8)+t,-(t*-1+(a*(R()+x)+b*(y+R())+c)*16))*3.5+p
  w("%c%c%c"%(i(p.x),i(p.y),i(p.z)))
