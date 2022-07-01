from qd.cae.dyna import KeyFile


class ModelHandler:
    """Helper class for loading adjusting the model"""
    def __init__(self, filename):
        self.file = KeyFile(filename, parse_mesh=True)

    def get_parts(self):
        
