"""
Our building system 
"""
from ursina import Vec3, floor
from config import six_cube_dirs

def checkBuild(_bsite,_td,_camF,_pos): 

    dist = _bsite - _pos
    mouseInWorld = _pos + _camF * dist.length()
    mouseInWorld -= _camF * 0.75
    x = round(mouseInWorld.x)
    y = floor(mouseInWorld.y)
    z = round(mouseInWorld.z)

    if _bsite == Vec3(x,y,z):
        y+=1

    if _td.get((x,y,z))!='g' and _td.get((x,y,z))!=None:
        print("Cant build block present!!") 
        return None
    return Vec3(x,y,z)

def gapShell(_td,_bsite):
    
    for i in range(6):
        p = _bsite + six_cube_dirs[i]
        if _td.get((floor(p.x),floor(p.y),floor(p.z)))==None:
            _td[(floor(p.x),floor(p.y),floor(p.z))]='g'