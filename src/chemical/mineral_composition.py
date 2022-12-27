class MineralComp(object):
    def __init__(self, mineral, init_volume_fraction, reaction_type, radius=None, reactive_surface_area=None, unit=None):
        self.mineral = mineral
        self.init_volume_fraction = init_volume_fraction
        self.reaction_type = reaction_type
        self.radius = radius
        self.reactive_surface_area = reactive_surface_area
        self.unit = unit