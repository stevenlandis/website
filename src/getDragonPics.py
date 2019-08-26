import bld
import os

def getDragonPics(folder):
    pics = folder.getDir('fractalPics')
    picsSrc = bld.DiskDir('C:/Users/StevenLandis/Google Drive/core/Programming/cppFractal/pics/color path')
    for f in picsSrc.files:
        if f.type != 'bmp': continue
        ConvertRule(f, pics.getFile(f'{f.title}.jpg'))


class ConvertRule(bld.Rule):
    def __init__(self, inFile, outFile):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
    def run(self):
        [inFile] = self.inputs
        [outFile] = self.outputs

        cmd = f'magick convert "{inFile.path}" "{outFile.path}"'
        print(cmd)
        os.system(cmd)
        # sub.run([cmd], shell=True)
