class Pulse:
    def __init__(self, pos, mag, target, targetid, vel, t1):
        self.pos = pos
        self.mag = mag
        self.target = target
        self.targetid = targetid
        self.vel = vel
        self.t1 = t1
        self.reached = False
        self.alive = True

    def has_reached(self):
        if self.reached:
            return False
        if self.vel > 0 and self.pos >= self.target.pos:
            self.reached = True
            return True
        elif self.vel < 0 and self.pos <= self.target.pos:
            self.reached = True
            return True
        else:
            return False

    def has_passed(self):
        if self.vel > 0 and self.pos >= self.target.pos + self.vel*self.t1:
            self.alive = False
        elif self.vel < 0 and self.pos <= self.target.pos + self.vel*self.t1:
            self.alive = False
