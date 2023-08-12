from ursina import *

panda = FrameAnimation3d('panda_walk_',fps=1)

panda.texture='panda_texture'
panda.position = Vec3(0,-2.9,10)
panda.turnSpeed = 1
panda.speed = 1

def mob_movement(mob, subPos, _td):
    tempOR = mob.rotation_y
    mob.lookAt(subPos)
    mob.rotation = Vec3(0,mob.rotation.y+180,0)
    mob.rotation_y = lerp(tempOR,mob.rotation_y,mob.turnSpeed*time.dt)

    intimacyDist = 5
    dist = subPos-mob.position

    if dist.length() > intimacyDist:
        mob.position -= mob.forward * mob.speed * time.dt
        mob.resume() 
        mob.is_playing=True
    else:
        mob.pause()
        mob.is_playing=False

    terrain_walk(mob, _td)

def terrain_walk(mob, _td):
    if mob.y < -100:
        mob.y = 100
        print("Panda Fallen!")

    blockFound=False
    step = 4
    height = 1
    x = floor(mob.x+0.5)
    z = floor(mob.z+0.5)
    y = floor(mob.y+0.5)
    for i in range(-step,step):
        whatT1=_td.get((x,y+i,z))
        if whatT1!=None and whatT1!='g':
            whatT2=_td.get((x,y+i+1,z))
            if whatT2!=None and whatT2!='g':
                target = y+i+height+1
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        mob.y = lerp(mob.y, target, 6 * time.dt)
    else:
        mob.y -= 9.8 * time.dt
