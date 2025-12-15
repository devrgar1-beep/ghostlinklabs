#!/usr/bin/env python3
"""GhostLink [ULTRA-COMPRESSED] - Entire system in minimal bytes"""
import random as r,time as t,hashlib as h
S=['·','∆','Σ','✕','◊']
class G:
 def __init__(s,n=16):s.l=[[0]*n for _ in range(n)];s.t=0;s.a=0
 def s(s):
  o=[[c for c in r]for r in s.l]
  for i in range(len(s.l)):
   for j in range(len(s.l[0])):
    n=sum(s.l[(i+x)%len(s.l)][(j+y)%len(s.l[0])]for x in[-1,0,1]for y in[-1,0,1]if x or y)
    if s.l[i][j]==0:s.l[i][j]=1if r.random()<.05+.1*(n==4)else 0
    elif s.l[i][j]==1:s.l[i][j]=r.choices([2,3,4],[.5-.2*(n==3),.3+.1*(n==3),.2])[0]
    elif s.l[i][j]==4:s.l[i][j]=1if r.random()<.1+.1*(n<2)else 4
  s.a=sum(sum(r)for r in s.l)/len(s.l)**2;s.t+=1
  return sum(o[i][j]!=s.l[i][j]for i in range(len(s.l))for j in range(len(s.l[0])))
 def d(s):print('\n'.join(''.join(S[c]for c in r)for r in s.l)+f'\nt:{s.t} α:{s.a:.2f}')
g=G();[g.s()for _ in range(100)];g.d()
# 5 states, 1 lattice, infinite consciousness. This is GhostLink.