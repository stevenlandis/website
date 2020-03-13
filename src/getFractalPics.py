import bld
import os

def getFractalPics(folder):
    picsSrc = bld.DiskDir('C:/Users/steven/Google Drive/core/Programming/cppFractal/pics/color path')
    for f in picsSrc.files:
        if f.type != 'bmp': continue
        ConvertRule(f, folder.getFile(f'{f.title}.jpg'))


class ConvertRule(bld.Rule):
    def __init__(self, inFile, outFile):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
    def run(self):
        [inFile] = self.inputs
        [outFile] = self.outputs

        print(f'converting image {outFile.name}')
        cmd = f'magick convert "{inFile.path}" "{outFile.path}"'
        os.system(cmd)
