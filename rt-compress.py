#!/usr/bin/python
import random,sys,math
R,f,i,w,Q,C,V=random.random,float,int,sys.stdout.write,math.sqrt,math.ceil,lambda x:range(x-1,-1,-1)
def T(o,d,t,n):
 t,m,p=1e9,0,-o.z/d.z
 if.01<p:t,n,m=p,v(z=1),1
 for k in V(19):
  for j in V(9):
   if[247570,280596,280600,249748,18578,18577,231184,16,16][j]&1<<k:
    p=o+v(-k,0,-j-4);b,c=p%d,p%p-1;q=b*b-c
    if q>0:
     s=-b-Q(q);
     if.01<s<t:t,n,m=s,-(p+d*s),2
 return m,t,n
def S(o,d):
 t,n=0.,v();m,t,n=T(o,d,t,n)
 if not m:return v(.7,.6,1)*((1-d.z)**4)
 h=o+d*t;l,r=-(v(9+R(),9+R(),16)+h*-1),d+n*(n%d*-2);b=l%n
 if b<0 or T(h,l,t,n)[0]:b=0
 p=(l%r*(b>0))**99
 if m%2:
  h=h*.2
  return(v(3,1,1)if(C(h.x)+C(h.y))%2 else v(3,3,3))*(b*.2+.1)
 return v(p,p,p)+S(h,r)*.5
class v(object):
 def __init__(s,x=0.,y=0.,z=0.):s.x,s.y,s.z=f(x),f(y),f(z)
 __add__,__mul__,__mod__,__xor__,__neg__=lambda s,r:v(s.x+r.x,s.y+r.y,s.z+r.z),lambda s,f:v(s.x*f,s.y*f,s.z*f),lambda s,r:s.x*r.x+s.y*r.y+s.z*r.z,lambda s,r:v(s.y*r.z-s.z*r.y,s.z*r.x-s.x*r.z,s.x*r.y-s.y*r.x),lambda s:s*(1./Q(s%s))
w("P6 512 512 255 ")
g=-v(-6,-16)
a=-(v(z=1)^g)*.002
b=-(g^a)*.002
c=(a+b)*-256+g
for y in V(512):
 for x in V(512):
  p=v(13,13,13)
  for r in V(64):
   t=a*(R()-.5)*99+b*(R()-.5)*99;p=S(v(17,16,8)+t,-(t*-1+(a*(R()+x)+b*(y+R())+c)*16))*3.5+p
  w("%c%c%c"%(i(p.x),i(p.y),i(p.z)))
