"""Subject terrain collisions through walls etc."""

from ursina import Vec3, held_keys, time, lerp

def collisionWall(subject,terrain):
    blockFound=False
    step = 2
    jumpHeight = 3
    height = subject.height
    x = round(subject.x)
    z = round(subject.z)
    y = round(subject.y)

    def checkcollision(inF):
        for i in range(1,step+1):
            whatT=terrain.td.get(  (round(inF.x), round(inF.y+i),round(inF.z)))
            if whatT!=None and whatT!='g':
                return True
        return False

    howClose=0.55
    rPos=Vec3(x,y,z)
    subFor=subject.forward
    subFor.y=0
    bDir=rPos+subFor*howClose
    if (checkcollision(bDir) or
        checkcollision(bDir+subject.left*howClose*0.5) or
        checkcollision(bDir+subject.right*howClose*0.5)):
        held_keys['w'] = 0
    
    bDir=rPos-subFor*howClose
    if (checkcollision(bDir) or
        checkcollision(bDir+subject.left*howClose*0.5) or
        checkcollision(bDir+subject.right*howClose*0.5)):
        held_keys['s'] = 0
    
    subFor=subject.left
    subFor.y=0
    bDir=rPos+subFor*howClose
    if (checkcollision(bDir) or
        checkcollision(bDir+subject.forward*howClose*0.5) or
        checkcollision(bDir+subject.back*howClose*0.5)):
        held_keys['a'] = 0
    
    bDir=rPos-subFor*howClose
    if (checkcollision(bDir) or
        checkcollision(bDir+subject.forward*howClose*0.5) or
        checkcollision(bDir+subject.back*howClose*0.5)):
        held_keys['d'] = 0

    for i in range(-2,step):
        whatT1=terrain.td.get((x,y+i,z))
        if whatT1!=None and whatT1!='g':
            whatT2=terrain.td.get((x,y+i+1,z))
            if whatT2!=None and whatT2!='g':
                
                target = y+i+height+1
                blockFound=True
                break
            
            whatT3=terrain.td.get((x,y+i+2,z))
            if whatT3!=None and whatT3!='g':
                target = y+i+height+2
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        subject.y = lerp(subject.y, target, 6 * time.dt)
        
        if subject.frog is True:
            subject.frog=False
            subject.y+=jumpHeight
    else:
        subject.y -= 9.8 * time.dt