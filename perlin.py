from perlin_module import PerlinNoise

class Perlin:
    def __init__(self):
        
        self.seed = ord('y')+ord('o')
        self.octaves = 8
        self.freq = 256
        self.amp = 18    

        self.pNoise_continental = PerlinNoise( seed=self.seed,
                                    octaves=1)
        self.pNoise_details = PerlinNoise(  seed=self.seed,
                                    octaves=self.octaves)

    def getHeight(self,x,z):
        from math import sin
        y = 0
        y = self.pNoise_continental([x/512,z/512])*128
        y += self.pNoise_details([x/self.freq,z/self.freq])*self.amp

        sAmp=0.33
        y+=sin(z)*sAmp
        y+=sin(x*0.5)*sAmp
        return y