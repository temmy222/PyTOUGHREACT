class Grid(object):
    def __init__(self, unit_system, numxblocks, numyblocks, numzblocks, xLength, yLength, zLength, depth, originX,
                 originY, originZ,
                 equalSpacing=True):
        self.unit_system = unit_system
        if self.unit_system.lower() == 'si':
            self.depth = depth
            self.zLength = zLength
            self.yLength = yLength
            self.xLength = xLength
            self.originZ = originZ
            self.originX = originX
            self.originY = originY
        else:
            self.depth = self.convertToMetric(depth)
            self.zLength = self.convertToMetric(zLength)
            self.yLength = self.convertToMetric(yLength)
            self.xLength = self.convertToMetric(xLength)
            self.originZ = self.convertToMetric(originZ)
            self.originX = self.convertToMetric(originX)
            self.originY = self.convertToMetric(originY)
        self.equalSpacing = equalSpacing
        self.numzblocks = numzblocks
        self.numyblocks = numyblocks
        self.numxblocks = numxblocks
        if self.equalSpacing:
            self.get_spacing(numxblocks, numyblocks, numzblocks, xLength, yLength, zLength)

    def get_spacing(self, numxblocks, numyblocks, numzblocks, xLength, yLength, zLength):
        xspacing = xLength / numxblocks
        yspacing = yLength / numyblocks
        zspacing = zLength / numzblocks
        return [xspacing, yspacing, zspacing]

    def dimensionSpacing(self, numxblocks, numyblocks, numzblocks, xspacing, yspacing, zspacing):
        dx = [xspacing] * numxblocks
        dy = [yspacing] * numyblocks
        dz = [zspacing] * numzblocks
        return [dx, dy, dz]

    def convertToMetric(self, value):
        answer = value * 0.3048
        return answer
