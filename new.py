# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
accelerate = ""
add_rock = False
z = 0
x_rock =  random.randint(1, 10)
y_rock = random.randint(1, 10)
rock_list = dict()
rock_draw_list = list()
new_missile = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)


    def ship_rotate_cloclwise(self):
        self.angle_vel += .05

    def ship_rotate_counterclockwise(self):
        self.angle_vel -= .05

    def ship_rotate_stop(self):
        self.angle_vel = 0

    def ship_thrust(self, thrust):
        self.thrust_on = thrust
        if self.thrust_on:
            self.vel[0] = angle_to_vector(self.angle)[0]
            self.vel[1] = angle_to_vector(self.angle)[1]

    def ship_acc_keydown(self, acc):
        global accelerate
        self.acc = acc
        if self.acc:
            acc_constant = 1.03
            self.vel[0] *= acc_constant
            self.vel[1] *= acc_constant
            accelerate = 'on'
        else:
            accelerate = 'off'

    def update(self):
        # Angle rotation
        self.angle += self.angle_vel
        # Position of ship
        if accelerate == 'on':
            self.ship_acc_keydown(True)
            self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        if accelerate == 'off':
            self.ship_acc_keydown(False)
            self.pos[0] = (self.pos[0] + self.vel[0] * .3) % WIDTH
            self.pos[1] = (self.pos[1] + self.vel[1] * .3) %  HEIGHT

    def shoot(self):
        missile_direction = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * missile_direction[0], self.pos[1] + self.radius * missile_direction[1]]
        missile_vel = [self.vel[0]  +  10 * missile_direction[0], self.vel[1] + 10 * missile_direction[1]]
        n_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        return n_missile
        print 'SHOOT!!'
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self): 
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0] * .3) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1] * .3) %  HEIGHT
           
def draw(canvas):
    global time, x_rock, y_rock, add_rock, z
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_missile.draw(canvas)
    if new_missile:
        new_missile.draw(canvas)
        new_missile.update()

    # Add rock every 1 second
    rocks_movements(canvas)

    # update ship and sprites
    my_ship.update()
    a_missile.update()
    add_rock = False

    # Ship Acceleration
            

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

def keydown(key):
    global new_missile
    if key == simplegui.KEY_MAP['left']:
        my_ship.ship_rotate_counterclockwise()
    if key == simplegui.KEY_MAP['right']:
        my_ship.ship_rotate_cloclwise()
    if key == simplegui.KEY_MAP['up']:
        my_ship.ship_thrust(True)
        my_ship.ship_acc_keydown(True)
    if key == simplegui.KEY_MAP['space']:
        new_missile = my_ship.shoot()


def keyup(key):
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.ship_rotate_stop()
    if key == simplegui.KEY_MAP['up']:
        my_ship.ship_thrust(False)
        my_ship.ship_acc_keydown(False)

# timer handler that spawns a rock    
def rock_spawner():
    global add_rock, x_rock, y_rock, rock_list, z
    x_rock =  random.randrange(1, WIDTH)
    y_rock = random.randrange(1, HEIGHT) 
    n_rock =  Sprite([x_rock, y_rock], [random.random() * .3, random.random() * .3], 0, .009, asteroid_image, asteroid_info)
    rock_list[z] = n_rock
    add_rock = True

#Adding rock behaviour
def rocks_movements(canvas):
    global z
    if add_rock == True:
        for rock in rock_list:
            rock_draw_list.append(rock_list[rock])

    for rock in rock_draw_list:
        rock.draw(canvas)
        rock.update()

    if len(rock_draw_list) >= 20:
       del rock_draw_list[0]
    if z <= 20:
        z += 1
    else:
        z = 0

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)

# register event handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()