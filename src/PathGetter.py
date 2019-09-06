class PathGetter:
    def __init__(self, basePath):
        self.basePath = basePath

    def getRec(self, path):
        return f'{self.basePath}rec/{path}'

    def getScript(self, path):
        return f'{self.basePath}scripts/{path}'

    def getPage(self, path):
        return f'{self.basePath}{path}'