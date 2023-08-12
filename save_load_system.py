"""
Saving and loading a terrain 'map'.
"""

mapName='pre.map'

def saveMap(_subPos, _td):
    import os, sys, pickle

    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)

    with open(mapName, 'wb') as f:

        map_data = [_subPos, _td]

        pickle.dump(map_data, f)

        map_data.clear()

def loadMap(_subject,_terrain):
    import os, sys, pickle
    from ursina import destroy

    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open(mapName, 'rb') as f:
        map_data = pickle.load(f)

    for s in _terrain.subsets:
        destroy(s)
    _terrain.td={}
    _terrain.vd={}
    _terrain.subsets=[]
    _terrain.setup_subsets()
    _terrain.currentSubset=1
    _terrain.td=map_data[1]

    for key in _terrain.td:
        whatT=_terrain.td.get(key)
        if whatT!=None and whatT!='g':
            x = key[0]
            y = key[1]
            z = key[2]
            if i>=len(_terrain.subsets)-1:
                i=0
            _terrain.genBlock(x,y,z,subset=i,gap=False,blockType=whatT)
            i+=1

    _subject.position=map_data[0]
    _terrain.swirlEngine.reset( _subject.position.x, _subject.position.z)
    for s in _terrain.subsets:
        s.model.generate()