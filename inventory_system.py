
from ursina import *
import random as ra
from config import mins,minerals
import numpy as np

itemspots=[]
items=[]

import sys
window.fullscreen=False
if window.fullscreen==False and sys.platform.lower()=='darwin':
    camera.ui.scale_x*=0.05*1/window.aspect_ratio
    camera.ui.scale_y*=0.05

itembar = Entity(model='quad',parent=camera.ui)

item_cols=9
item_wid=1/16 
hb_wid=item_wid*item_cols 
itembar.scale=Vec3(hb_wid,item_wid,0)

itembar.y=(-0.45 + (itembar.scale_y*0.5))
itembar.color=color.dark_gray
itembar.z=0

iPan = Entity(model='quad',parent=camera.ui)

iPan.rows=3
iPan.scale_y=itembar.scale_y * iPan.rows
iPan.scale_x=itembar.scale_x
iPan.basePosY=itembar.y+(itembar.scale_y*0.5)+(iPan.scale_y*0.5)
iPan.gap=itembar.scale_y
iPan.y=iPan.basePosY+iPan.gap

iPan.color=color.light_gray

iPan.z=0
iPan.visible=False

class itemspot(Entity):
    scalar=itembar.scale_y*0.9
    rowFit=9
    def __init__(self):
        super().__init__()
        self.model=load_model('quad',use_deepcopy=True)
        self.parent=camera.ui
        self.scale_y=itemspot.scalar
        self.scale_x=self.scale_y
        self.color=color.white
        self.texture='white_box'
        
        self.z=-1

        self.onitembar=False
        self.visible=False
        self.occupied=False
        self.item=None
        self.stack=0
        self.t = Text("",scale=1.5)
    
    @staticmethod
    def toggle():
        if iPan.visible:
            iPan.visible=False
        else:
            iPan.visible=True  
        for h in itemspots:
            if not h.visible and not h.onitembar:
                h.visible=True
                h.t.visible=True
                if h.item:
                    h.item.visible=True
            elif not h.onitembar:
                h.visible=False
                h.t.visible=False
                if h.item:
                    h.item.visible=False

class Item(Draggable):
    def __init__(self,_blockType):
        super().__init__()
        self.model=load_model('quad',use_deepcopy=True)
        self.scale_x=itemspot.scalar*0.9
        self.scale_y=self.scale_x
        self.color=color.white
        self.texture='texture_atlas_3.png'
        self.texture_scale*=64/self.texture.width
        self.z=-2

        if _blockType==None:
            self.blockType=mins[ra.randint(0,len(mins)-1)]
        else:
            self.blockType=_blockType

        self.onitembar=False
        self.visible=False
        self.currentSpot=None

        self.set_texture()
        self.set_colour()
    
    def set_texture(self):
        uu=minerals[self.blockType][0]
        uv=minerals[self.blockType][1]

        basemod=load_model('block.obj',use_deepcopy=True)
        e=Empty(model=basemod)
        cb=copy(e.model.uvs)
        del cb[:-33]
        self.model.uvs = [Vec2(uu,uv) + u for u in cb]
        self.model.generate()
        self.rotation_z=180

    def set_colour(self):
        if len(minerals[self.blockType]) > 2:
            self.color=minerals[self.blockType][2]
    
    def fixPos(self):
        closest=-1
        closestitemty=None
        for h in itemspots:
            if h.occupied and h.item!=self: continue
            
            dist=h.position-self.position
            dist=np.linalg.norm(dist)
            if dist < closest or closest == -1:
                closestitemty=h
                closest=dist

        if closestitemty is not None:
            self.position=closestitemty.position

            closestitemty.occupied=True
            closestitemty.item=self
            closestitemty.stack=self.currentSpot.stack
            
            if self.currentSpot!=closestitemty:
                self.currentSpot.stack=0
                self.currentSpot.t.text = "     "
                self.currentSpot.occupied=False
                self.currentSpot.item=None
                self.currentSpot=closestitemty

        elif self.currentSpot:
            self.position=self.currentSpot.position

    def update_stack_text(self):
        stackNum = self.currentSpot.stack
        myText="<white><bold>"+str(stackNum)
        self.currentSpot.t.text = myText
        self.currentSpot.t.origin=(0,0)
        self.currentSpot.t.z=-3
        self.currentSpot.t.x=self.currentSpot.x
        self.currentSpot.t.y=self.currentSpot.y

    def drop(self):
        self.fixPos()
        self.update_stack_text()

    @staticmethod
    def stack_check(_blockType):
        for h in itemspots:
            if h.onitembar==False: continue
            if h.occupied==False: continue

            if h.item.blockType==_blockType:
                h.stack+=1
                h.item.update_stack_text()
                return True
        return False

    @staticmethod
    def new_item(_blockType):
        aStack = Item.stack_check(_blockType)
        if aStack==False:
            for h in itemspots:
                if not h.onitembar or h.occupied: continue
                else:
                    h.stack=1
                    b=Item(_blockType)
                    b.currentSpot=h
                    items.append(b)
                    
                    h.item=b
                    h.occupied=True
                    b.onitembar=True
                    b.visible=True
                    b.x = h.x
                    b.y = h.y
                    b.update_stack_text()
                    break
                    

for i in range(itemspot.rowFit):
    bud=itemspot()
    bud.onitembar=True
    bud.visible=True
    bud.y=itembar.y
    padding=(itembar.scale_x-bud.scale_x*itemspot.rowFit)*0.5
    bud.x=  (   itembar.x-itembar.scale_x*0.5 +
                itemspot.scalar*0.5 + 
                padding +
                i*bud.scale_x
            )
    itemspots.append(bud)

for i in range(itemspot.rowFit):
    for j in range(iPan.rows):
        bud=itemspot()
        bud.onitembar=False
        bud.visible=False
        
        padding_x=(iPan.scale_x-itemspot.scalar*itemspot.rowFit)*0.5
        padding_y=(iPan.scale_y-itemspot.scalar*iPan.rows)*0.5
        bud.y=  (   iPan.y+iPan.scale_y*0.5 -
                    itemspot.scalar*0.5 -
                    padding_y -
                    itemspot.scalar * j
                )
        bud.x=  (   iPan.x-iPan.scale_x*0.5 +
                    itemspot.scalar*0.5 +
                    padding_x +
                    i*itemspot.scalar
                )
        itemspots.append(bud)

itemspot.toggle()
itemspot.toggle()    

def inv_input(key,subject,mouse):
    try:
        wnum = int(key)
        if wnum > 0 and wnum < 10:
            
            for h in itemspots:
                h.color=color.white
            
            wnum-=1
            itemspots[wnum].color=color.black
            
            if itemspots[wnum].occupied:
            
                subject.blockType=itemspots[wnum].item.blockType
                
    except:
        pass

    if key=='e' and subject.enabled:
        itemspot.toggle()
        subject.disable()
        mouse.locked=False
    elif key=='e' and not subject.enabled:
        itemspot.toggle()
        subject.enable()
        mouse.locked=True