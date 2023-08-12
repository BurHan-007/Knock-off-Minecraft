"""
To collect the blocks
"""

from ursina import Entity, Vec2, Vec4, load_model, Audio, destroy
from config import minerals
from math import sin, floor
from random import random
from inventory_system import Item

pop_audio = Audio('pop.mp3',autoplay=False,loop=False)
pickup_audio = Audio('pickup.mp3',autoplay=False,loop=False)

class Collectible(Entity):
    def __init__(self,_blockType,_pos,_tex,_sub):
        super().__init__()
        self.model=load_model('block.obj',use_deepcopy=True)
        self.texture=_tex
        self.scale=0.33
        self.position=_pos

        self.numVertices=len(self.model.vertices)
        self.blockType=_blockType
        self.subject=_sub
    
        self.o_position=self.position

        self.y+=0.5-(self.scale_y*0.5)
        self.original_y=self.y

        self.texture_scale*=64/self.texture.width

        if len(minerals[self.blockType])>2:
            c = random()-0.5
            ce=minerals[self.blockType][2]

            self.model.colors = (   (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)*
                                    self.numVertices)
        else:
            c = random()-0.5
            self.model.colors = (   (Vec4(1-c,1-c,1-c,1),)*
                                    self.numVertices)

        uu=minerals.get(_blockType)[0]
        uv=minerals.get(_blockType)[1]
        self.model.uvs=([Vec2(uu,uv) + u for u in self.model.uvs])

        pop_audio.play()
        self.model.generate()
        destroy(self, 7)

    def update(self):
        self.checkPickUp()
        self.bounce()

    def checkPickUp(self):
        x=round(self.subject.position.x)
        y=floor(self.subject.position.y)
        z=round(self.subject.position.z)
        if ((x,y,z)==self.o_position):
            pickup_audio.play()
            Item.new_item(self.blockType)
            self.disable()

    def bounce(self):
        self.rotation_y+=2
        self.y = ( self.original_y + 
                sin(self.rotation_y*0.05)*self.scale_y)