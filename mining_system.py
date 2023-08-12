from ursina import Entity, color, floor, Vec3
from collectible_system import *

bte = Entity(model='block.obj',color=color.rgba(1,1,0,0.4))
bte.scale=1.1
bte.origin_y+=0.05

def highlight(pos,sub_H,cam,td):
    for i in range(1,32):
        wp=pos+Vec3(0,sub_H,0)+cam.forward*(i*0.5)

        x = round(wp.x)
        y = floor(wp.y)
        z = round(wp.z)
        bte.x = x
        bte.y = y
        bte.z = z
        whatT=td.get((x,y,z))
        if whatT!=None and whatT!='g':
            bte.visible = True
            break
        else:
            bte.visible = False

def mine(td,vd,subsets,_texture,_sub):
    if not bte.visible: 
        return
    wv=vd.get((floor(bte.x),floor(bte.y),floor(bte.z)))
    
    if wv==None: 
        return
    
    for i in range(wv[1]+1,wv[1]+37):
        subsets[wv[0]].model.vertices[i][1]+=999

    blockType=td.get((floor(bte.x),floor(bte.y),floor(bte.z)))
    Collectible(blockType,bte.position,_texture,_sub)

    subsets[wv[0]].model.generate()

    td[ (floor(bte.x),floor(bte.y),floor(bte.z))]='g'
    vd[ (floor(bte.x),floor(bte.y),floor(bte.z))] = None
    
    return (bte.position, wv[0], blockType)