from ursina import *

app = Ursina()

from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from flake import SnowFall
import random as ra
from bump_system import *
from save_load_system import saveMap, loadMap
from inventory_system import *

window.color = color.rgb(0,200,225)
window.fullscreen = True
window.exit_button.visible = False

subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=True
subject.cursor.color=color.white
subject.height=1.62
subject.camera_pivot.y=subject.height
subject.frog=False
subject.runSpeed=12
subject.walkSpeed=7
subject.blockType=None
camera.dash=10 

armTexture = load_texture("arm_texture.png") 
sky_texture = load_texture('skybox.png') 

arm = Entity(model = 'arm.obj') 
arm.parent = camera.ui 
arm.texture = armTexture 
arm.scale = 0.15 
arm.rotation = Vec3(150,-10,0) 
arm.position = Vec2(0.7,-0.6) 

sky = Entity(model = 'sphere') 
sky.parent = scene
sky.texture = sky_texture 
sky.scale = 15000 
sky.double_sided = True 

terrain = MeshTerrain(subject,camera)

generatingTerrain=True

for i in range(4):
    terrain.genTerrain()
# For loading in a large terrain at start.
#loadMap(subject,terrain)

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x 
pZ = subject.z

def input(key):
    global generatingTerrain
    terrain.input(key)
    # Jumping...
    if key=='space': subject.frog=True
    # Saving and loading...
    if key=='m': saveMap(subject.position,terrain.td)
    if key=='l': loadMap(subject,terrain)
    # Exit game.....
    if key == 'escape':
        quit()
    # Arm movement
    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.position = Vec2(0.65,-0.55)
    else:
        arm.position = Vec2(0.7,-0.6)

    # Inventory access.
    inv_input(key,subject,mouse)

count=0
earthcounter=0

def update():
    global count, pX, pZ, earthcounter

    # Highlight block for mining/building...
    terrain.update()

    # Panda Movement.
    mob_movement(panda, subject.position, terrain.td)

    count+=1
    if count >= 1:
        
        count=1
        
        if generatingTerrain:
            terrain.genTerrain()

    
    if abs(subject.x-pX)>1 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z 
        terrain.swirlEngine.reset(pX,pZ)
        
        if subject.y > 4:
            if snow_audio.playing==False:
                snow_audio.pitch=ra.random()+0.25
                snow_audio.play()
        elif grass_audio.playing==False:
            grass_audio.pitch=ra.random()+0.7
            grass_audio.play()

    collisionWall(subject,terrain)

    if held_keys['shift'] and held_keys['w']:
        subject.speed=subject.runSpeed
        if camera.fov<100:
            camera.fov+=camera.dash*time.dt
    else:
        subject.speed=subject.walkSpeed
        if camera.fov>90:
            camera.fov-=camera.dash*4*time.dt
            if camera.fov<90:camera.fov=90

from mob_system import *

app.run()