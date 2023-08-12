from perlin import Perlin
from ursina import *
from random import random
from swirl_engine import SwirlEngine
from mining_system import *
from building_system import *
from config import six_cube_dirs, minerals, mins
from tree_system import *

class MeshTerrain:
    def __init__(self,_sub,_cam):
        
        self.subject = _sub
        self.camera = _cam

        self.block = load_model('block.obj',use_deepcopy=True)
        self.textureAtlas = 'texture_atlas_3.png'
        self.numVertices = len(self.block.vertices)

        self.subsets = []
        self.numSubsets = 1024
        
        self.subWidth = 6 
        self.swirlEngine = SwirlEngine(self.subWidth)
        self.currentSubset = 0

        self.td = {}

        self.vd = {}

        self.perlin = Perlin()

        
        self.setup_subsets()

    def plantTree(self,_x,_y,_z):
        ent=TreeSystem.genTree(_x,_z)
        if ent==0: return
        # Trunk.
        for i in range(int(ent*10)):
            self.genBlock(_x,_y+i,_z,
                blockType='concrete',layingTerrain=False)
        # Crown.
        for t in range(-2,3):
            for tt in range(4):
                for ttt in range(-2,3):
                    self.genBlock(_x+t,_y+(ent*10)+tt,_z+ttt, blockType='ice')


    def setup_subsets(self):
        for i in range(0,self.numSubsets):
            e = Entity( model=Mesh(), texture=self.textureAtlas)
            e.texture_scale*=64/e.texture.width
            self.subsets.append(e)

    def do_mining(self):
        epi = mine( self.td,self.vd,self.subsets,self.textureAtlas,self.subject)
        if (epi != None and epi[2] != 'concrete' and epi[2] != 'ice'):
            self.genWalls(epi[0],epi[1])
            self.subsets[epi[1]].model.generate()

    
    def update(self):
        highlight(  self.subject.position,
                    self.subject.height,
                    self.camera,self.td)
        
        if bte.visible==True and mouse.locked==True:
            if held_keys['shift'] and held_keys['left mouse']:
                self.do_mining()

    def input(self,key):
        if key=='left mouse up' and bte.visible==True and mouse.locked==True:
            self.do_mining()
        
        if self.subject.blockType is None: return
        if key=='right mouse up' and bte.visible==True and mouse.locked==True:
            bsite = checkBuild( bte.position,self.td,
                                self.camera.forward,
                                self.subject.position+Vec3(0,self.subject.height,0))
            if bsite!=None:
                self.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),subset=0,blockType=self.subject.blockType)
                gapShell(self.td,bsite)
                self.subsets[0].model.generate()
    
    def genWalls(self,epi,subset):
        
        if epi==None: return
        
        for i in range(0,6):
            np = epi + six_cube_dirs[i]
            if self.td.get( (floor(np.x),
                            floor(np.y),
                            floor(np.z)))==None:
                self.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')


    def genBlock(self,x,y,z,subset=-1,gap=True,blockType='grass',layingTerrain=False):
        if subset==-1: subset=self.currentSubset

        model = self.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                self.block.vertices])

        if layingTerrain:
            
            if random() > 0.86:
                blockType='stone'
            
            if y > 2:
                blockType='snow'

        if len(minerals[blockType])>2:
            c = random()-0.5
            ce=minerals[blockType][2]
            model.colors.extend(    (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)*self.numVertices)
        else:
            c = random()-0.5
            model.colors.extend(    (Vec4(1-c,1-c,1-c,1),)*self.numVertices)

        uu=minerals[blockType][0]
        uv=minerals[blockType][1]

        model.uvs.extend([Vec2(uu,uv) + u for u in self.block.uvs])

        self.td[(floor(x),floor(y),floor(z))] = blockType

        if gap==True:
            key=((floor(x),floor(y+1),floor(z)))
            if self.td.get(key)==None:
                self.td[key]='g'

        vob = (subset, len(model.vertices)-self.numVertices-1)
        self.vd[(floor(x),
                floor(y),
                floor(z))] = vob

    def genTerrain(self):

        x = floor(self.swirlEngine.pos.x)
        z = floor(self.swirlEngine.pos.y)

        d = int(self.subWidth*0.5)
        
        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(self.perlin.getHeight(x+k,z+j))
                if self.td.get( (floor(x+k),
                                floor(y),
                                floor(z+j)))==None:
                    self.genBlock(x+k,y,z+j,blockType='grass',layingTerrain=True)
                    self.plantTree(x+k,y+1,z+j)

        self.subsets[self.currentSubset].model.generate()
        if self.currentSubset<self.numSubsets-1:
            self.currentSubset+=1
        else: self.currentSubset=0
        self.swirlEngine.move()