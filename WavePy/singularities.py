class Singularity:
    def __init__(self, pos, Nb, Nc, Nb_, Nc_):
        self.pos = pos
        self.Nb = Nb
        self.Nc = Nc
        self.Nb_ = Nb_
        self.Nc_ = Nc_

class Fix(Singularity):
    def __init__(self, pos):
        self.pos = pos
        self.Nb = 1
        self.Nc = 2

class Free(Singularity):
    def __init__(self, pos):
        self.pos = pos
        self.Nb = -1
        self.Nc = 0

class Double(Singularity):
    def __init__(self, pos):
        self.pos = pos
        self.Nb = 1/3
        self.Nc = 4/3
        self.Nb_ = -1/3
        self.Nc_ = 2/3

class Half(Singularity):
    def __init__(self, pos):
        self.pos = pos
        self.Nb = -1/3
        self.Nc = 2/3
        self.Nb_ = 1/3
        self.Nc_ = 4/3