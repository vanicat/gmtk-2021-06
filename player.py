from libs import length
from ursina import Sprite, Vec2, time, held_keys, distance2d
from constant import *

class Player(Sprite):
    def __init__(self, texture, position, control = True):
        super().__init__(texture=texture, position = position, scale=(SCALE, SCALE), collider = 'box')
        self.velocity = Vec2(0, 0)
        self.width = texture.width * SCALE / 100
        self.height = texture.height * SCALE / 64
        #self.collider.visible = True
        self.control = control
        self.other = None
        self.length = .5
        self.capacities = set()
        self.claw = False
        self.touching = True


    def input(self, key):
        if self.control:
            if key == 'space' and self.touching :
                for direction in self.touching:
                    self.velocity += SAUT[direction]
            if key == 'control':
                if self.touching and Capacity.CLAW in self.capacities and not self.claw:
                    self.claw = True
                else:
                    self.claw = False
        if key == 'tab':
            self.control = not self.control
        
    def update(self):
        touching = set()

        direction = self.down
        hits_info = self.cast(direction)
        if hits_info.hit:
            if hits_info.entity.tile.get('intangible'):
                hits_info.entity.collide()
            else:
                touching.add('down')

        direction = self.up
        hits_info = self.cast(direction)
        if hits_info.hit:
            if hits_info.entity.tile.get('intangible'):
                hits_info.entity.collide()
            else:
                touching.add('up')

        direction = self.left
        hits_info = self.cast(direction)
        if hits_info.hit:
            if hits_info.entity.tile.get('intangible'):
                hits_info.entity.collide()
            else:
                touching.add('left')

        direction = self.right
        hits_info = self.cast(direction)
        if hits_info.hit:
            if hits_info.entity.tile.get('intangible'):
                hits_info.entity.collide()
            else:
                touching.add('right')

        if not self.touching and touching and not self.claw:
            sounds['bang'].play()

        self.touching = touching

        if self.claw:
            self.velocity = Vec2(0, 0)
            return

        # update velocity
        self.velocity *= .9 ** time.dt
        self.velocity += GRAVITY * time.dt
        if self.control:
            if touching:
                speed = WALKING_SPEED
            else:
                speed = COMMAND_SPEED
            self.velocity.x += (held_keys['right arrow'] - held_keys['left arrow']) * time.dt * speed

        too_long = False

        dist = distance2d(self, self.other)
        if dist >= self.length:
            too_long = True
            vec = self.other.position - self.position
            vec = vec.normalized()
            k = sum(vec * self.velocity)
            if dist > self.length:
                k = k*1.10
            vec *= max(-k, 0)
            self.velocity += (vec.x, vec.y)

        if 'down' in touching:
            self.velocity.y = max(self.velocity.y, 0)
        if 'up' in touching:
            self.velocity.y = min(self.velocity.y, 0)
        if 'left' in touching:
            self.velocity.x = max(self.velocity.x, 0)
        if 'right' in touching:
            self.velocity.x = min(self.velocity.x, 0)
        
        self.position += self.velocity * time.dt

        new_dist = distance2d(self, self.other)
        if too_long and new_dist > self.length * 1.03:
            self.position += -self.velocity * time.dt
            self.velocity = Vec2(0, 0)  


    def cast(self, direction:Vec2):
        direction = direction.normalized()
        self.position += direction * (max(length(self.velocity), 0.05) * time.dt)
        hits_info = self.intersects()
        self.position -= direction * (max(length(self.velocity), 0.05) * time.dt)
        
        """ raycast(self.position + direction * self.width / 2, 
            direction = direction,
            distance = ,
            #thickness = self.width/2,
            ignore = (self,),
            debug = True
        ) """
        
        return hits_info

