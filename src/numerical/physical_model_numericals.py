class PhysicalNumericals(object):
    def __init__(self) -> None:
        pass

    def timesteps(self, maximum_time_step=999, stop_time=1e7, time_step=500):
        self.maximum_time_step = maximum_time_step
        self.stop_time = stop_time
        self.time_step = time_step

    def toughMOPS(self):
        self.MOPS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]