import random
import os
import pygame
from pygame.locals import *
from pygame import mixer

mixer.init()
pygame.init()

clockobject = pygame.time.Clock()
fps = 60
screen_width = 1000
screen_height = 700
start_game = True
pass_game = False

counter = pygame.time.get_ticks()
update_time = pygame.time.get_ticks()
update_time1 = pygame.time.get_ticks()
score_time = pygame.time.get_ticks()
game_start_time = pygame.time.get_ticks()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle City Remastered')

#define game variables
tile_size = 50
player_list = []  # contains player characters
enemy_list = []   # contains enemy characters
char_list = []    # contains all characters

player_list_detial = []  # contains player characters detial
enemy_list_detial = []   # contains enemy characters detial
char_list_detial = []    # contains all characters detial

enemy_pastaway = []
tank_pastaway = []
player_pastaway = []

p1_point = []
p2_point = []
p3_point = []
p4_point = []

p1_TP = []
p2_TP = []
p3_TP = []
p4_TP = []

powerUP_count = [5, 10, 15]
enemy_levelUP = [6, 11, 16]
enemy_count = [int(i) for i in range(-5,16)]
current_level = 1

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

#load images
bg_img = pygame.image.load('./resources/images/grassbg2.png')
bg_img = pygame.transform.scale(bg_img, (1000, 700))
rocket_img = pygame.image.load(f'./resources/images/rocket/1.png')
detial_img = pygame.image.load('./resources/images/detials.png')
bc_img = pygame.image.load('./resources/images/intro/bc.png')
ps_img = pygame.image.load('./resources/images/intro/ps.png')
co_img = pygame.image.load('./resources/images/intro/co.png')
control_img = pygame.image.load('./resources/images/intro/control.png')
pause_img = pygame.image.load('./resources/images/intro/pause.png')
re_img = pygame.image.load('./resources/images/intro/resume.png')
qg_img = pygame.image.load('./resources/images/intro/qg.png')
rest_img = pygame.image.load('./resources/images/intro/rest.png')
score_img = pygame.image.load('./resources/images/intro/score.png')
pl_img = []
for i in range(1,3):
    img = pygame.image.load(f'./resources/images/player1/lv1/right/{i}.png')
    pl_img.append(img)

#load sounds
# tank move sound
tank_move = mixer.Sound('./resources/sound/move.ogg')
tank_move.set_volume(0.0)
tank_move.play(-1)

# bonus sound
bonus = pygame.mixer.Sound('./resources/sound/bonus.ogg')
bonus.set_volume(0.9)

# tank blast sound
tank_blast = pygame.mixer.Sound('./resources/sound/explosion.ogg')
tank_blast.set_volume(0.9)

# tank fire sound
tank_fire = pygame.mixer.Sound('./resources/sound/fire.ogg')
tank_fire.set_volume(0.9)

# brick sound
brick = pygame.mixer.Sound('./resources/sound/brick.ogg')
brick.set_volume(0.9)

# gamestart sound
gamestart = pygame.mixer.Sound('./resources/sound/gamestart.ogg')
gamestart.set_volume(0.9)

# gameover sound
gameover = pygame.mixer.Sound('./resources/sound/gameover.ogg')
gameover.set_volume(0.9)

# score sound
score = pygame.mixer.Sound('./resources/sound/score.ogg')
score.set_volume(0.9)

# steel sound
steel = pygame.mixer.Sound('./resources/sound/steel.ogg')
steel.set_volume(0.9)

# rocket_blast sound
rblast = pygame.mixer.Sound('./resources/sound/rblast.wav')
rblast.set_volume(0.9)

# high score sound
hg = pygame.mixer.Sound('./resources/sound/hg.mp3')
hg.set_volume(0.9)

def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

def rl():
    while True: 
        a = random.randint(0, 6)
        if a != 1:
            break
    return a

############################################################## TANK #######################################################

class Tank(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, direction, level, health, speed):
        pygame.sprite.Sprite.__init__(self)
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.shoot = False
        self.alive = True
        self.level = level
        self.fire_power = 1
        self.skit = False
        self.char_type = char_type
        self.speed_o = self.speed = speed
        self.shoot_cooldown = 0
        self.health = health
        self.lifes = 3
        self.count = 0
        self.max_health = self.health
        self.direction = direction
        self.action = 0
        if char_type != "player1" and char_type != "player2" and char_type != "player3" and char_type != "player4":
            self.action = 1
            self.direction = -2
            self.lifes = 1
        self.frame_index = 0
        self.frame_index_blast = 0
        self.frame_spawn_index = 0
        self.frame_shiled_index = 0
        self.animation_list = []
        self.blast = 0
        self.born = 0
        self.blink_count = 1
        self.born_ = True
        self.timer = False
        self.shiled_active = False
        self.update_time = pygame.time.get_ticks()
        self.spawn_time = pygame.time.get_ticks()
        self.shiled_time = pygame.time.get_ticks()
        self.shiled_time_end = pygame.time.get_ticks()
        self.cooldown_timer = pygame.time.get_ticks()
        self.blink = pygame.time.get_ticks()

        # load tank blast images
        self.tank_blast = []
        for i in range(1, len(os.listdir(f'./resources/images/tank_blast'))+1):
            img = pygame.image.load(f"./resources/images/tank_blast/{i}.png")
            self.tank_blast.append(img)
        self.image_blast = self.tank_blast[0]

        # load tank shiled images
        self.tank_shiled = []
        for i in range(1, len(os.listdir(f'./resources/images/shiled'))+1):
            img = pygame.image.load(f"./resources/images/shiled/{i}.png")
            self.tank_shiled.append(img)
        self.image_shiled = self.tank_shiled[0]

        # load tank spawn images
        self.tank_spawn = []
        for i in range(1, len(os.listdir(f'./resources/images/tank_spawn'))+1):
            img = pygame.image.load(f"./resources/images/tank_spawn/{i}.png")
            self.tank_spawn.append(img)
        self.image_spawn = self.tank_spawn[0]

        # load all images for the players
        animation_types = ['up', 'down', 'right', 'left']
        for animation_index in range(1,5):
            temp_list_lv = []
            for animation in animation_types:
                #reset temporary list of images
                temp_list = []
                #count number of files in the folder
                if char_type != "player1" and char_type != "player2" and char_type != "player3" and char_type != "player4":
                    num_of_frames = len(os.listdir(f'./resources/images/enemy/{"lv"+str(animation_index)}/{animation}'))
                else:
                    num_of_frames = len(os.listdir(f'./resources/images/{self.char_type}/{"lv"+str(animation_index)}/{animation}'))
                for i in range(1,num_of_frames+1):
                    if char_type != "player1" and char_type != "player2" and char_type != "player3" and char_type != "player4":
                        img = pygame.image.load(f"./resources/images/enemy/{'lv'+str(animation_index)}/{animation}/{i}.png")
                    else:
                        img = pygame.image.load(f"./resources/images/{self.char_type}/{'lv'+str(animation_index)}/{animation}/{i}.png")
                    temp_list.append(img)
                temp_list_lv.append(temp_list)
            self.animation_list.append(temp_list_lv)


        self.image = self.animation_list[self.level - 1][self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.spawn_x = self.rect.x = x
        self.spawn_y = self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.space= False
        self.collusion = False

        #AI variables
        self.ran_move = 1
        self.movement_count = 0
        self.vision = pygame.Rect(0, 0, 300, 20)
        self.angle = 0

    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
    def move(self):
        dx = 0
        dy = 0

        if self.moving_up:
            self.skit = True
            dy -= self.speed
            self.direction = 2
    
        elif self.moving_down:
            self.skit = True
            dy += self.speed
            self.direction = -2
        
        elif self.moving_left:
            self.skit = True
            dx -= self.speed
            self.direction = -1
        
        elif self.moving_right:
            self.skit = True
            dx += self.speed
            self.direction = 1
        
        if self.direction == 1:
            self.angle = 270
        elif self.direction == -1:
            self.angle = 90
        elif self.direction == 2:
            self.angle = 0
        elif self.direction == -2:
            self.angle = 180

        self.char_collusionx = False
        self.char_collusiony = False
        #check for tank collision
        index = char_list.index(self.char_type) ; j = 0
        for i in char_list_detial:
            if i.alive:
                #x-axis
                if i.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and j != index:
                    self.char_collusionx = True
                    if self.direction == 1:
                        self.ran_move = random.choice([1,2,4])
                        self.movement_count = 0
                    elif self.direction == -1:
                        self.ran_move = random.choice([1,2,3])
                        self.movement_count = 0
                    dx=0
                
                #y-axis
                elif i.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) and j != index:
                    self.char_collusiony = True
                    if self.direction == 2:
                        self.ran_move = random.choice([1,3,4])
                        self.movement_count = 0
                    elif self.direction == -2:
                        self.ran_move = random.choice([2,3,4])
                        self.movement_count = 0
                    dy=0
            j += 1
        

        #check for wall collision
        self.speed = self.speed_o
        for tile in world.tile_list:
            if tile[2] == 'sp':
                if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    if self.skit:
                        #if self.direction == 1 or self.direction == -1 or self.direction == -2 or self.direction == 2:
                        self.speed = self.speed_o + 1
                        if self.direction == -1 and self.moving_left == False:
                            self.count += 1
                            dx -= 1
                        elif self.direction == 1 and self.moving_right == False:
                            self.count += 1
                            dx += 1
                        elif self.direction == -2 and self.moving_down == False:
                            self.count += 1
                            dy += 1
                        elif self.direction == 2 and self.moving_up == False:
                            self.count += 1
                            dy -= 1

                        if self.count >= 40:
                            self.skit = False
                            self.count = 0

            if tile[2]=='s' or tile[2]=='e' or tile[2]=='default' or tile[2]=='b' or tile[2]=='w':
                #x-axis
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    if self.direction == 1:
                        self.ran_move = random.choice([1,2,4])
                        self.movement_count = 0
                    elif self.direction == -1:
                        self.ran_move = random.choice([1,2,3])
                        self.movement_count = 0

                    y=str(self.rect.y)
                    if len(y)==1:
                        y="00"+y
                    elif len(y)==2:
                        y="0"+y

                    if int(y[1:])>=40 and int(y[1:])<=60:
                        self.rect.y=int(y[0]+"50")
                    if int(y[1:])>=90:
                        self.rect.y=int(y[0]+"00")+100
                    if int(y[1:])<=10:
                        self.rect.y=int(y[0]+"00")
                    dx=0
                    break

                #y-axis
                elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.direction == 2:
                        self.ran_move = random.choice([1,3,4])
                        self.movement_count = 0
                    elif self.direction == -2:
                        self.ran_move = random.choice([2,3,4])
                        self.movement_count = 0

                    x=str(self.rect.x)
                    if len(x)==1:
                        x="00"+x
                    elif len(x)==2:
                        x="0"+x

                    if int(x[1:])>=40 and int(x[1:])<=60:
                        self.rect.x=int(x[0]+"50")
                    if int(x[1:])>=90:
                        self.rect.x=int(x[0]+"00")+100
                    if int(x[1:])<=10:
                        self.rect.x=int(x[0]+"00")
                    dy=0
                    break

        if self.char_collusionx:
            dx = 0
        if self.char_collusiony:
            dy = 0

        #update player coordinates
        if self.timer == False and self.born_ == False and self.health >= 0:
            self.rect.x += dx
            self.rect.y += dy


        #boarder check
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0
            self.ran_move = random.choice([2,3,4])
            self.movement_count = 0
        if self.rect.top < 0:
            self.rect.top = 0
            dy = 0
            self.ran_move = random.choice([1,3,4])
            self.movement_count = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            dx = 0
            self.ran_move = random.choice([1,2,4])
            self.movement_count = 0
        if self.rect.left < 0:
            self.rect.left = 0
            dx = 0
            self.ran_move = random.choice([1,2,3])
            self.movement_count = 0
 
    def AI(self):
        if self.alive:
            self.movement_count += 1
            if self.movement_count < 50:
                if self.ran_move == 1:
                    self.action = 0
                    self.moving_down = self.moving_right = self.moving_left = False
                    self.moving_up = True
                    self.direction = 2
                    self.vision = pygame.Rect(0, 0, 20, 300)
                    self.vision.center = (self.rect.centerx, self.rect.centery - 150)
                elif self.ran_move == 2:
                    self.action = 1
                    self.moving_up = self.moving_right = self.moving_left = False
                    self.moving_down = True
                    self.direction = -2
                    self.vision = pygame.Rect(0, 0, 20, 300)
                    self.vision.center = (self.rect.centerx, self.rect.centery + 150)
                elif self.ran_move == 3:
                    self.action = 2
                    self.moving_up = self.moving_down = self.moving_left = False
                    self.moving_right = True
                    self.direction = 1
                    self.vision = pygame.Rect(0, 0, 300, 20)
                    self.vision.center = (self.rect.centerx + 150, self.rect.centery)
                elif self.ran_move == 4:
                    self.action = 3
                    self.moving_right = self.moving_up = self.moving_down = False
                    self.moving_left = True
                    self.direction = -1
                    self.vision = pygame.Rect(0, 0, 300, 20)
                    self.vision.center = (self.rect.centerx - 150, self.rect.centery)
                    
            if self.movement_count >= 100:
                self.ran_move = random.randint(1,4)
                self.movement_count = 0

            # vision of AI
            for tile in world.tile_list:
                if self.vision.colliderect(tile[1]):
                    if tile[2]=='b':
                        self.enemy_shoot()
                    if (tile[2]=='s' and self.fire_power >= 2):
                        self.enemy_shoot()
                    if tile[2]=='e' and (self.char_type != "player1" or self.char_type != "player2" or self.char_type != "player3" or self.char_type != "player4"):
                        if tile[3]!=1:
                            self.enemy_shoot()
                            
            if self.char_type == "player1" or self.char_type == "player2" or self.char_type == "player3" or self.char_type == "player4":         
                self.check_list = enemy_list_detial
            else:
                self.check_list = player_list_detial
            for pl in self.check_list:
                if pl.alive:
                    if self.vision.colliderect(pl.rect):
                        self.enemy_shoot()

    def shoot_rocket(self):
        if self.born_ == False and self.timer == False and self.shoot == True:
            if self.fire_power <= 2 and self.shoot_cooldown == 0:
                self.shoot_cooldown = 80
                tank_fire.play()
                rocket = Rocket(self.rect.x, self.rect.y, self.direction, self.char_type, self.fire_power)
                rocket_group.add(rocket)
            elif self.fire_power == 3 and (self.shoot_cooldown == 0 or self.shoot_cooldown == 8):
                if self.shoot_cooldown == 0:
                    self.shoot_cooldown = 50
                tank_fire.play()
                rocket = Rocket(self.rect.x, self.rect.y, self.direction, self.char_type, self.fire_power)
                rocket_group.add(rocket)

    def enemy_shoot(self):
        if self.born_ == False and self.timer == False:
            if self.fire_power <= 2 and self.shoot_cooldown == 0:
                self.shoot_cooldown = 80
                tank_fire.play()
                rocket = Rocket(self.rect.x, self.rect.y, self.direction, self.char_type, self.fire_power)
                rocket_group.add(rocket)
            elif self.fire_power == 3 and (self.shoot_cooldown == 0 or self.shoot_cooldown == 8):
                if self.shoot_cooldown == 0:
                    self.shoot_cooldown = 50
                tank_fire.play()
                rocket = Rocket(self.rect.x, self.rect.y, self.direction, self.char_type, self.fire_power)
                rocket_group.add(rocket)

    def shiled_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 200
        #update image depending on current frame
        self.image_shiled = self.tank_shiled[self.frame_shiled_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.shiled_time > ANIMATION_COOLDOWN:
            self.shiled_time = pygame.time.get_ticks()
            self.frame_shiled_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_shiled_index >= len(self.tank_shiled):
            self.frame_shiled_index = 0
        if pygame.time.get_ticks() - self.shiled_time_end > 30000:
            self.shiled_active = False
            self.health = self.level*5

    def timer_cooldown(self):
        if pygame.time.get_ticks() - self.cooldown_timer > 15000:
            self.timer = False
        #update image depending on current frame
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.cooldown_timer > 10000 and pygame.time.get_ticks() - self.cooldown_timer < 15000:
            if pygame.time.get_ticks() - self.blink > 300:
                self.blink = pygame.time.get_ticks()
                if self.blink_count%2 == 0:
                    self.image = pygame.transform.scale(world.img_, (0, 0))
                else:
                    self.image = self.animation_list[self.level - 1][self.action][0]
            self.blink_count += 1

    def update_animation(self):
        if self.health >= 0 and self.timer == False:
            #update animation
            ANIMATION_COOLDOWN = 100
            #update image depending on current frame
            self.image = self.animation_list[self.level - 1][self.action][self.frame_index]
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN and (self.moving_up or self.moving_down or self.moving_left or self.moving_right or self.speed != self.speed_o):
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #if the animation has run out the reset back to the start
            if self.frame_index >= len(self.animation_list[self.level - 1][self.action]):
                self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action  and self.timer == False:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #tank spawn animation
    def tank_born(self):
        #update animation
        ANIMATION_COOLDOWN = 180
        #update image depending on current frame
        self.image_spawn = self.tank_spawn[self.frame_spawn_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.spawn_time > ANIMATION_COOLDOWN:
            self.spawn_time = pygame.time.get_ticks()
            if self.frame_spawn_index >= 0:
                self.frame_spawn_index += 1
            else:
                self.frame_spawn_index -= 1
        #if the animation has run out the reset back to the start
        if self.frame_spawn_index >= len(self.tank_spawn):
            self.born += 1
            self.frame_spawn_index = -2
        elif self.frame_spawn_index < -4:
            self.born += 1
            self.frame_spawn_index = 1
        if self.born >= 2:
            self.born_ = False

    def check_alive(self):
        if self.shiled_active == False:
             self.shiled_time_end = pygame.time.get_ticks()

        if self.timer == False:
            self.cooldown_timer = pygame.time.get_ticks()
            self.blink = pygame.time.get_ticks()

        if self.health <= 0:
            self.speed = 0
            self.frame_index = 0
            self.moving_right = False
            self.moving_left = False
            self.moving_up = False
            self.moving_down = False
            
            if self.blast >= 3:
                #self.alive = False
                if self.lifes > 0:
                    self.lifes -= 1

                if self.lifes < 1:
                    self.alive = False
                    self.frame_index_blast = 0
                    self.kill()
                
                else:
                    self.born_ = True
                    self.born = 0
                    self.rect.x = self.spawn_x
                    self.rect.y = self.spawn_y
                    self.health = 5
                    self.level = 1
                    self.fire_power = 1
                    self.blast = 0
                    self.direction = 2
                    self.action = 0
        
            #blast animation
            ANIMATION_COOLDOWN = 150
            #update image depending on current frame
            self.image_blast = self.tank_blast[self.frame_index_blast]
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.blast += 1
                self.update_time = pygame.time.get_ticks()
                self.frame_index_blast += 1
            #if the animation has run out the reset back to the start
            if self.frame_index_blast >= len(self.tank_blast):
                self.frame_index_blast = 0
 
    def draw(self):
        if self.born_:
            self.tank_born()
            screen.blit(self.image_spawn, self.rect)
        else:
            screen.blit(self.image, self.rect)
        if self.shiled_active:
            self.shiled_animation()
            screen.blit(self.image_shiled, self.rect)
        if self.timer:
            self.timer_cooldown()
        #pygame.draw.rect(screen, (255,255,255), self.rect, 1)

    def draw_blast(self):
        if self.health <= 0:
            screen.blit(self.image_blast, self.rect)

############################################################ ROCKET #####################################################

class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, char, fire_power):
        pygame.sprite.Sprite.__init__(self)
        self.blast = 0
        self.rocket_collusion = False
        self.char_type = char
        self.direction = direction
        self.fire_power = fire_power
        self.angle = 0
        self.blastx = 0
        self.blasty = 0
        self.tile_remove = []
        if self.direction == 1:
            self.angle = 270
        elif self.direction == -1:
            self.angle = 90
        elif self.direction == -2:
            self.angle = 180

        self.image = pygame.transform.rotate(rocket_img, self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if self.direction == 2 or self.direction == -2:
            self.rect.x = x+19
            if self.direction == -2:
                self.rect.y = y+55#50
            if self.direction == 2: #r
                self.rect.y = y-25#16
        elif self.direction == 1 or self.direction == -1:
            self.rect.y = y+19
            if self.direction == 1:
                self.rect.x = x+55#50
            if self.direction == -1:
                self.rect.x = x-25#16
        self.update_time = pygame.time.get_ticks()

    def update(self):
        dx = 0
        dy = 0

        
        if self.direction == 1:
            dx += 4
        elif self.direction == -1:
            dx -= 4
        elif self.direction == 2:
            dy -= 4
        elif self.direction == -2:
            dy += 4

        #update rocket coordinates
        self.rect.x += dx
        self.rect.y += dy
        
       
        #check if rocket has gone off screen
        if self.rect.bottom > screen_height:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.left < -1:
            self.kill()

        #check for wall collision
        for tile in world.tile_list:

            if tile[1].colliderect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()) and (tile[2]=='s' or tile[2]=='e' or tile[2]=='default' or tile[2]=='b'):
                if self.direction == 1:
                    self.blastx = tile[1].left-22
                    self.blasty = self.rect.y-20
                elif self.direction == -1:
                    self.blastx = tile[1].left+50
                    self.blasty = self.rect.y-20
                elif self.direction == 2:
                    self.blasty = tile[1].top+50
                    self.blastx = self.rect.x-20
                elif self.direction == -2:
                    self.blasty = tile[1].top-22
                    self.blastx = self.rect.x-20

                if tile[2] == 'b':
                    brick.play()

                if tile[2] == 's':
                    steel.play()

                if tile[2] == 'default':
                    self.kill()

                elif tile[2] != 'default':
                    if tile[3]//5 > 1:
                        if tile[2] == 's' and self.fire_power >= 2:
                            tile[0] =  world.stell_wall[5 - (tile[3]//5)]
                        elif tile[2] == 'b':
                            tile[0] =  world.brick_wall[5 - (tile[3]//5)]
                        elif tile[2] == 'e':
                            tile[0] =  world.eagle[1]
                            if tile[3] != 1:
                                world.eagle_blast = True
                            tile[3] = 1

                    if tile[2] == 's' and self.fire_power >= 2:
                        tile[3] -= 5
                    elif tile[2] == 'b':
                        if self.fire_power == 1:
                            tile[3] -= 5
                        else:
                            tile[3] -= 10
                    
                    if tile[3] <= 0:
                        self.tile_remove.append(tile)

                    wall_bst = Wall_blast(self.blastx, self.blasty, self.direction, self.tile_remove)
                    wall_blast_group.add(wall_bst)
                    self.kill()
                

        #check collision with char
        if self.char_type == "player1" or self.char_type == "player2" or self.char_type == "player3" or self.char_type == "player4":         
            self.check_list = enemy_list_detial
        else:
            self.check_list = player_list_detial
        for i in self.check_list:
            if i.born_ == False :
                if i.rect.colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()):
                    if i.alive:
                        steel.play()
                        if self.fire_power == 1:
                            i.health -= 5
                        elif self.fire_power >= 2:
                            i.health -= 10
                        if i.health <= 0:
                            tank_blast.play()
                            if self.char_type == "player1":
                                p1_point.append(i.level)
                            elif self.char_type == "player2":
                                p2_point.append(i.level)
                            elif self.char_type == "player3":
                                p3_point.append(i.level)
                            elif self.char_type == "player4":
                                p4_point.append(i.level)

                        self.kill()

        #check for rocket and rocket collision
        for i in rocket_group:
            if i.rect.colliderect(self.rect.x, self.rect.y + dy, self.image.get_width(), self.image.get_height()) and i.char_type != self.char_type:
                rblast.play(0, 500)
                rblast.set_volume(0.7)
                self.kill()
                i.kill()
                rocket_bst = Rocket_blast(self.rect.x+self.image.get_width()//2, self.rect.y+self.image.get_height()//2)
                rocket_blast_group.add(rocket_bst)

#################################################### ROCKET BLAST #######################################################

class Rocket_blast(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.update_time = pygame.time.get_ticks()
        self.frame_index_blast = 0
        
        # load tank blast images
        self.tank_blast = []
        for i in range(1, len(os.listdir(f'./resources/images/tank_blast'))+1):
            img = pygame.image.load(f"./resources/images/tank_blast/{i}.png")
            self.tank_blast.append(img)
        self.image = self.tank_blast[0]
        self.rect = self.image.get_rect()
        image_w = self.image.get_width()//2
        image_h = self.image.get_height()//2
        self.rect.x = x-image_w
        self.rect.y = y-image_h
        
    def update(self):
        #blast animation
        ANIMATION_COOLDOWN = 150
        #update image depending on current frame
        self.image = self.tank_blast[self.frame_index_blast]
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index_blast += 1
        #if the animation has run out the reset back to the start
        if self.frame_index_blast == len(self.tank_blast):
            self.kill()
    
####################################################### WALL BLAST #######################################################

class Wall_blast(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, tile_remove):
        pygame.sprite.Sprite.__init__(self)
        
        self.update_time = pygame.time.get_ticks()
        self.tile_remove = tile_remove
        self.frame_index_blast = 0
        self.direction = direction
        if self.direction == 1:
            self.angle = 270
        elif self.direction == -1:
            self.angle = 90
        elif self.direction == 2:
            self.angle = 0
        elif self.direction == -2:
            self.angle = 180
        
        #load all images for the rocket_boom
        self.rocket_boom = []
        for i in range(len(os.listdir("./resources/images/rocket_boom"))):
            img = pygame.image.load(f"./resources/images/rocket_boom/{i}.png")
            self.rocket_boom.append(img)
        self.image = pygame.transform.rotate(self.rocket_boom[0], self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        #blast animation
        ANIMATION_COOLDOWN = 55
        #update image depending on current frame

        self.image = pygame.transform.rotate(self.rocket_boom[self.frame_index_blast], self.angle)
        
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index_blast += 1
        #if the animation has run out the reset back to the start
        if self.frame_index_blast == len(self.rocket_boom):
            if len(self.tile_remove) != 0:
                for tile in self.tile_remove:
                    if tile[3] <= 0:
                        try:
                            world.tile_list.remove(tile)
                            self.tile_remove.remove(tile)
                        except:
                            pass
            self.kill()
  
######################################################### POWERUP #########################################################

class Power_up(pygame.sprite.Sprite):
    def __init__(self, data):
        pygame.sprite.Sprite.__init__(self)
        self.data = data
        self.spawn_location = None
        self.run = True
        self.show_image = False
        self.update_time = pygame.time.get_ticks()
        self.remove_time = pygame.time.get_ticks()
        self.animation_count = 1
        self.index = 0

        self.powerUP = []
        self.powerUP_index = 0
        for i in os.listdir("./resources/images/powerup"):
            img = pygame.image.load(f"./resources/images/powerup/{i}")
            self.powerUP.append(img)

        # rendering images
        self.powerUP_lst = ['boom', 'eagle_shiled', 'levelup', 'lifes', 'rocket_powerup', 'shiled', 'timer']
        while self.run:
            self.spawn_r = random.randint(2, 12)
            self.spawn_c = random.randint(1, 15)
            row_count = 0
            for row in self.data:
                col_count = 0
                if self.run == False:
                    break
                for tile in row:
                    if self.run == False:
                        break
                    if tile == 0 and row_count == self.spawn_r and col_count == self.spawn_c:
                        self.idx_org = self.powerUP_index = random.randint(0, 6)
                        self.image = pygame.transform.scale(self.powerUP[self.powerUP_index], (tile_size, tile_size))
                        self.rect = img.get_rect()
                        self.rect.x = col_count * tile_size
                        self.rect.y = row_count * tile_size
                        self.spawn_location = [self.image, self.rect, self.powerUP_lst[self.powerUP_index]]
                        self.run = False
                    col_count += 1
                row_count += 1

    def blink(self):
        #update animation
        ANIMATION_COOLDOWN = 250
        #update image depending on current frame
        if self.index == 7:
            self.image = pygame.transform.scale(self.powerUP[self.index], (0, 0))
        else:
            self.image = pygame.transform.scale(self.powerUP[self.idx_org], (tile_size, tile_size))
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.index = 7
            self.update_time = pygame.time.get_ticks()
            self.animation_count += 1
        #if the animation has run out the reset back to the start
        if self.animation_count >= 3:
            self.animation_count = 1
            self.index = self.idx_org

    # remove powerup after 30 seconds
    def remove_power_up(self):
        #update animation
        ANIMATION_COOLDOWN = 30000
        #update image depending on current frame
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.remove_time > ANIMATION_COOLDOWN:
            self.kill()

    def update(self):
        self.rect.x
        self.rect.y

        #check if character catched the powerup
        for i in char_list_detial:
            if i.born_ == False and i.alive:
                if i.rect.colliderect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()):
                    index = char_list_detial.index(i)
                    bonus.play()

                    if self.powerUP_lst[self.powerUP_index] == 'boom':
                        tank_blast.play()
                        # check if player catch boom
                        if char_list[index] == "player1" or char_list[index] == "player2" or char_list[index] == "player3" or char_list[index] == "player4":
                            for i in enemy_list_detial:
                                index_ = char_list_detial.index(i)
                                i.health = -5
                                if char_list[index_] not in enemy_pastaway:
                                    enemy_pastaway.append(char_list[index_])
                                """if i.alive == False and index_ not in tank_pastaway:
                                    tank_pastaway.append(index_)"""
                        # check if enemy catch boom
                        else:
                            for i in player_list_detial:
                                #index_ = char_list_detial.index(i)
                                i.health = -5
                                """if i.alive == False and index_ not in tank_pastaway:
                                    tank_pastaway.append(index_)"""
                               
                    elif self.powerUP_lst[self.powerUP_index] == 'eagle_shiled':
                        self.lst = []
                        for item in world.eagle_wall_co:
                            for i in world.tile_list:
                                if (item[1] == i[1]) and (item[4] == 'es'):
                                    self.lst.append(item)
                        for item in world.eagle_wall_co:
                            if item not in self.lst:
                                world.tile_list.append(item)

                        world.eagle_wall_change = True
                        for tile in world.tile_list:
                            if char_list[index] == "player1" or char_list[index] == "player2" or char_list[index] == "player3" or char_list[index] == "player4":
                                world.player = True
                                if tile[4] == 'es':
                                    tile[0] = world.stell_wall[0]
                                    tile[2] = world.s
                                    tile[3] = world.wall_health

                            else:
                                world.player = False
                                if tile[4] == 'es':
                                    tile[0] = pygame.transform.scale(world.brick_wall[0], (0, 0))
                                    tile[2] = world.g

                    elif self.powerUP_lst[self.powerUP_index] == 'levelup':
                        if i.level < 4:
                            i.level += 1

                        if i.level == 2:
                            i.health = 10
                        elif i.level == 3:
                            i.health = 15
                            i.speed = 2
                            i.speed_o = 2
                        elif i.level == 4:
                            i.health = 20
                            i.speed = 1
                            i.speed_o = 1

                    elif self.powerUP_lst[self.powerUP_index] == 'lifes':
                        if char_list[index] == "player1" or char_list[index] == "player2" or char_list[index] == "player3" or char_list[index] == "player4":
                            i.lifes += 1

                    elif self.powerUP_lst[self.powerUP_index] == 'rocket_powerup':
                        if i.fire_power < 3:
                            i.fire_power += 1

                    elif self.powerUP_lst[self.powerUP_index] == 'shiled':
                        i.health = 100
                        i.shiled_active = True

                    elif self.powerUP_lst[self.powerUP_index] == 'timer':
                        # check if player catch timer
                        if char_list[index] == "player1" or char_list[index] == "player2" or char_list[index] == "player3" or char_list[index] == "player4":
                            for i in enemy_list_detial:
                                i.timer = True
                        # check if enemy catch timer
                        else:
                            for i in player_list_detial:
                                i.timer = True

                    self.kill()

########################################################## WORLD ##########################################################

class World():
    def __init__(self, data):
        self.tile_list = []
        self.s = 's'
        self.b = 'b'
        self.g = 'g'
        self.w = 'w'
        self.e = 'e'
        self.sp = 'sp'
        self.es = 'es'
        self.default = 'default'
        self.data = data
        self.water_position = []
        self.wall_health = 20
        self.eagle_wall_change = False
        self.eagle_wall_co = []
        self.update_time = pygame.time.get_ticks()
        self.restore_time = pygame.time.get_ticks()
        self.eagle_blast_time = pygame.time.get_ticks()
        self.player = None
        self.eagle_blast = False
        self.blink_count = 1

        #map images load
        self.img_ = pygame.image.load(f"./resources/images/powerup/zzz.png")
        self.boarder = pygame.image.load('./resources/images/boarder.png')
        self.grass=pygame.image.load("./resources/images/grass/1.png")
        self.speed_tiled=pygame.image.load("./resources/images/speed_tiled/1.png")

        self.stell_wall = []
        self.stell_wall_index = 0
        for i in range(1, len(os.listdir("./resources/images/stell_wall"))+1):
            img = pygame.image.load(f"./resources/images/stell_wall/{i}.png")
            self.stell_wall.append(img)

        self.brick_wall = []
        self.brick_wall_index = 0
        for i in range(1, len(os.listdir("./resources/images/brick_wall"))+1):
            img = pygame.image.load(f"./resources/images/brick_wall/{i}.png")
            self.brick_wall.append(img)

        self.water = []
        self.water_index = 0
        for i in range(1, len(os.listdir("./resources/images/water"))+1):
            img = pygame.image.load(f"./resources/images/water/{i}.png")
            self.water.append(img)

        self.eagle = []
        self.eagle_index = 0
        for i in range(1, len(os.listdir("./resources/images/eagle"))+1):
            img = pygame.image.load(f"./resources/images/eagle/{i}.png")
            self.eagle.append(img)

        self.eagle_boom = []
        self.eagle_boom_index = 0
        for i in range(1, len(os.listdir("./resources/images/boom"))+1):
            img = pygame.image.load(f"./resources/images/boom/{i}.png")
            self.eagle_boom.append(img)

        self.map_tile_lst = [self.boarder, self.grass, self.speed_tiled, self.stell_wall[self.stell_wall_index],
                            self.brick_wall[self.brick_wall_index], self.water[self.water_index], self.eagle[self.eagle_index]]
        # rendering images
        ep = 'en'
        row_count = 0
        for row in self.data:
            col_count = 0
            for tile in row:
                tile = tile - 1
                if tile != -1:
                    if tile == 7:
                        img = pygame.transform.scale(self.map_tile_lst[4], (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        self.eagle_wall_co.append([img, img_rect, self.b, self.wall_health, 'es'])
                        self.tile_list.append([img, img_rect, self.b, self.wall_health, 'es'])

                    if tile != 7:
                        img = pygame.transform.scale(self.map_tile_lst[tile], (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size

                        if tile == 1:
                            tile = [img, img_rect, self.g, self.wall_health, ep]   # grass
                        elif tile == 2:
                            tile = [img, img_rect, self.sp, self.wall_health, ep]  # speed_tiled
                        elif tile == 5:
                            tile = [img, img_rect, self.w, self.wall_health, ep]   # water
                            self.water_position.append(img_rect)
                        elif tile == 3:
                            tile = [img, img_rect, self.s, self.wall_health, ep]   # stell_wall
                        elif tile == 4:
                            tile = [img, img_rect, self.b, self.wall_health, ep]   # brick_wall
                        elif tile == 6:
                            tile = [img, img_rect, self.e, self.wall_health, ep]   # eagle
                            self.ex, self.ey = img_rect.x+25, img_rect.y+25
                        else:
                            tile = [img, img_rect, self.default, self.wall_health, ep]
                        self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def water_effect(self):
        #update animation
        ANIMATION_COOLDOWN = 550
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.water_index += 1
        #if the animation has run out the reset back to the start
        if self.water_index >= len(self.water):
            self.water_index = 0
        if self.eagle_wall_change == False:
            self.restore_time = pygame.time.get_ticks()
            self.blink = pygame.time.get_ticks()

    def eagle_blast_effect(self):
        #update animation
        ANIMATION_COOLDOWN = 180
        #update image depending on current frame
        if self.eagle_boom_index < len(self.eagle_boom):
            self.image_blast = self.eagle_boom[self.eagle_boom_index]
        image_w = self.image_blast.get_width()//2
        image_h = self.image_blast.get_height()//2
        if self.eagle_boom_index == 0:
            tank_blast.play()
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.eagle_blast_time  > ANIMATION_COOLDOWN:
            self.eagle_blast_time  = pygame.time.get_ticks()
            self.eagle_boom_index += 1
        #if the animation has run out the reset back to the start
        if self.eagle_boom_index >= len(self.eagle_boom):
            self.image_blast = self.eagle_boom[0]
            
        screen.blit(self.image_blast, (self.ex-image_w, self.ey-image_h))

    def restore_ewall(self):
        #update animation
        if self.eagle_wall_change:
            #update image depending on current frame
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.restore_time > 40000 and pygame.time.get_ticks() - self.restore_time < 50000:
                if pygame.time.get_ticks() - self.blink > 1000:
                    self.blink = pygame.time.get_ticks()
                    for tile in self.tile_list:
                        if tile[4] == 'es':
                            if self.player:
                                if self.blink_count%2 == 0:
                                    tile[0] = self.stell_wall[0]
                                    tile[2] = self.b
                                    tile[3] = self.wall_health
                                else:
                                    tile[0] = self.brick_wall[0]
                            else: 
                                if self.blink_count%2 == 0:
                                    tile[0] = pygame.transform.scale(self.img_, (0, 0))
                                else:
                                    tile[0] = self.brick_wall[0]
                    self.blink_count += 1

                    

            ANIMATION_COOLDOWN = 50000
            if pygame.time.get_ticks() - self.restore_time > ANIMATION_COOLDOWN:
                self.restore_time = pygame.time.get_ticks()
                for tile in self.tile_list:
                    if tile[4] == 'es':
                        tile[0] = self.brick_wall[0]
                        tile[2] = self.b
                        tile[3] = self.wall_health
                
                self.eagle_wall_change = False
         
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

            # water effect
            self.water_effect()
            for k in self.water_position:
                if tile[1] == k:
                    screen.blit(self.water[self.water_index], k)
    
    def draw_grass(self):
        for tile in self.tile_list:
            if tile[2] == self.g:
                screen.blit(tile[0], tile[1])

#################################################### DETIALS TO DISPLAY ###################################################

class Detials():
    def __init__(self):
        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)
        self.maroon = (128, 0, 0)
        self.navy = (0, 0, 128)
        self.silver = (192, 192, 192)
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.font = pygame.font.Font('freesansbold.ttf', 50)
        self.score_font = pygame.font.Font('freesansbold.ttf', 65)
        self.scoreT_font = pygame.font.Font('freesansbold.ttf', 45)
        self.update_time = pygame.time.get_ticks()
        self.update_time1 = pygame.time.get_ticks()
        self.count = 0

        self.high_sc = []
        self.high_sc_index = 0
        for i in range(1, len(os.listdir("./resources/images/intro/hs"))+1):
            img = pygame.image.load(f"./resources/images/intro/hs/{i}.png")
            self.high_sc.append(img)

        self.high_no = []
        self.high_no_index = 0
        for i in range(0, len(os.listdir("./resources/images/intro/no"))):
            img = pygame.image.load(f"./resources/images/intro/no/{i}.png")
            self.high_no.append(img)

        self.high_no1 = []
        self.high_no_index1 = 0
        for i in range(0, len(os.listdir("./resources/images/intro/no1"))):
            img1 = pygame.image.load(f"./resources/images/intro/no1/{i}.png")
            self.high_no1.append(img1)
        
        self.no_image = self.high_no[0]
        self.no_lst = self.high_no[:]

        self.pl_image_lst = []
        self.pl_image_index = 0
        for i in range(1, 5):
            self.temp_lst = []
            for j in range(1, 3):
                self.pl_img = pygame.image.load(f"./resources/images/player{i}/lv1/up/{j}.png")
                self.temp_lst.append(self.pl_img)
            self.pl_image_lst.append(self.temp_lst)
        self.pl_image = self.pl_image_lst[0][0]

        self.score_img = pygame.image.load('./resources/images/intro/score.png')
        self.score_txt_img = pygame.image.load('./resources/images/intro/sc.png')
        self.score_time = pygame.time.get_ticks()
        self.score_time_add = 0

        self.total1 = 0
        self.total2 = 0
        self.total3 = 0
        self.total4 = 0

        self.total1_count = 0
        self.total2_count = 0
        self.total3_count = 0
        self.total4_count = 0

        self.width_add = 0
        self.width_add1 = 0
        self.height_addT = 0

    def enemy_count(self):
        text = self.font.render(f'{20-enemy_counter}', True, self.silver)
        textRect = text.get_rect()
        textRect.center = (screen_width-50, 75)
        screen.blit(text, textRect)

    def player1_lives(self):
        text = self.font.render(f'{player_list_detial[0].lifes}', True, self.yellow)
        textRect = text.get_rect()
        textRect.center = (screen_width-50, 183)
        screen.blit(text, textRect)

    def player2_lives(self):
        text = self.font.render(f'{player_list_detial[1].lifes}', True, self.green)
        textRect = text.get_rect()
        textRect.center = (screen_width-50, 285)
        screen.blit(text, textRect)

    def player3_lives(self):
        text = self.font.render(f'{player_list_detial[2].lifes}', True, self.red)
        textRect = text.get_rect()
        textRect.center = (screen_width-50, 387)
        screen.blit(text, textRect)

    def player4_lives(self):
        text = self.font.render(f'{player_list_detial[3].lifes}', True, self.blue)
        textRect = text.get_rect()
        textRect.center = (screen_width-50, 488)
        screen.blit(text, textRect)

    def current_level(self):
        font = pygame.font.Font('freesansbold.ttf', 40)
        text = font.render(f'{current_level}', True, self.maroon)
        textRect = text.get_rect()
        textRect.center = (screen_width-95, 600)
        screen.blit(text, textRect)

    def p1_score(self, score):
        score1 = score.count(1)
        text = self.score_font.render(f'{score1}', True, self.yellow)
        textRect = text.get_rect()
        textRect.center = (170, 140)
        screen.blit(text, textRect)

        score2 = score.count(2)
        text = self.score_font.render(f'{score2}', True, self.yellow)
        textRect = text.get_rect()
        textRect.center = (358, 140)
        screen.blit(text, textRect)

        score3 = score.count(3)
        text = self.score_font.render(f'{score3}', True, self.yellow)
        textRect = text.get_rect()
        textRect.center = (543, 140)
        screen.blit(text, textRect)

        score4 = score.count(4)
        text = self.score_font.render(f'{score4}', True, self.yellow)
        textRect = text.get_rect()
        textRect.center = (725, 140)
        screen.blit(text, textRect)

        self.total1 = score1*100 + score2*200 + score3*300 + score4*400
        self.total1_count += 1
        if self.total1_count == 1:
            p1_TP.append(self.total1)
        self.total1 = str(self.total1)
        if self.total1[-3:] == "000":
            self.total1 = self.total1[:-3] + 'k' 
        text = self.scoreT_font.render(f'{self.total1}', True, self.yellow)
        textRect = text.get_rect()
        textRect.center = (845, 140)
        screen.blit(text, textRect)

    def p2_score(self, score):
        score1 = score.count(1)
        text = self.score_font.render(f'{score1}', True, self.green)
        textRect = text.get_rect()
        textRect.center = (170, 275)
        screen.blit(text, textRect)

        score2 = score.count(2)
        text = self.score_font.render(f'{score2}', True, self.green)
        textRect = text.get_rect()
        textRect.center = (358, 275)
        screen.blit(text, textRect)

        score3 = score.count(3)
        text = self.score_font.render(f'{score3}', True, self.green)
        textRect = text.get_rect()
        textRect.center = (543, 275)
        screen.blit(text, textRect)

        score4 = score.count(4)
        text = self.score_font.render(f'{score4}', True, self.green)
        textRect = text.get_rect()
        textRect.center = (725, 275)
        screen.blit(text, textRect)

        self.total2 = score1*100 + score2*200 + score3*300 + score4*400
        self.total2_count += 1
        if self.total2_count == 1:
            p2_TP.append(self.total2)
        self.total2 = str(self.total2)
        if self.total2[-3:] == "000":
            self.total2 = self.total2[:-3] + 'k' 
        text = self.scoreT_font.render(f'{self.total2}', True, self.green)
        textRect = text.get_rect()
        textRect.center = (845, 275)
        screen.blit(text, textRect)

    def p3_score(self, score):
        score1 = score.count(1)
        text = self.score_font.render(f'{score1}', True, self.red)
        textRect = text.get_rect()
        textRect.center = (170, 419)
        screen.blit(text, textRect)

        score2 = score.count(2)
        text = self.score_font.render(f'{score2}', True, self.red)
        textRect = text.get_rect()
        textRect.center = (358, 419)
        screen.blit(text, textRect)

        score3 = score.count(3)
        text = self.score_font.render(f'{score3}', True, self.red)
        textRect = text.get_rect()
        textRect.center = (543, 419)
        screen.blit(text, textRect)

        score4 = score.count(4)
        text = self.score_font.render(f'{score4}', True, self.red)
        textRect = text.get_rect()
        textRect.center = (725, 419)
        screen.blit(text, textRect)

        self.total3 = score1*100 + score2*200 + score3*300 + score4*400
        self.total3_count += 1
        if self.total3_count == 1:
            p3_TP.append(self.total3)
        self.total3 = str(self.total3)
        if self.total3[-3:] == "000":
            self.total3 = self.total3[:-3] + 'k' 
        text = self.scoreT_font.render(f'{self.total3}', True, self.red)
        textRect = text.get_rect()
        textRect.center = (845, 419)
        screen.blit(text, textRect)

    def p4_score(self, score):
        score1 = score.count(1)
        text = self.score_font.render(f'{score1}', True, self.blue)
        textRect = text.get_rect()
        textRect.center = (170, 571)
        screen.blit(text, textRect)

        score2 = score.count(2)
        text = self.score_font.render(f'{score2}', True, self.blue)
        textRect = text.get_rect()
        textRect.center = (358, 571)
        screen.blit(text, textRect)

        score3 = score.count(3)
        text = self.score_font.render(f'{score3}', True, self.blue)
        textRect = text.get_rect()
        textRect.center = (543, 571)
        screen.blit(text, textRect)

        score4 = score.count(4)
        text = self.score_font.render(f'{score4}', True, self.blue)
        textRect = text.get_rect()
        textRect.center = (725, 571)
        screen.blit(text, textRect)

        self.total4 = score1*100 + score2*200 + score3*300 + score4*400
        self.total4_count += 1
        if self.total4_count == 1:
            p4_TP.append(self.total4)
        self.total4 = str(self.total4)
        if self.total4[-3:] == "000":
            self.total4 = self.total4[:-3] + 'k' 
        text = self.scoreT_font.render(f'{self.total4}', True, self.blue)
        textRect = text.get_rect()
        textRect.center = (845, 571)
        screen.blit(text, textRect)

    def high_score(self):
        pygame.draw.rect(screen, BLACK, (0, 0, 1000, 700))
        self.score_img = pygame.transform.scale(self.score_img, (900, 500))
        screen.blit(self.score_img, (50, 100))

        self.score_time_add = (2000*player_spawn_counter)+4000
        if player_spawn_counter >= 1:
            if pygame.time.get_ticks() - self.score_time > 2000:
                if pygame.time.get_ticks() - self.score_time > 2000 and pygame.time.get_ticks() - self.score_time < 2020:
                    score.play()
                detials.p1_score(p1_point)
        if player_spawn_counter >= 2:
            if pygame.time.get_ticks() - self.score_time > 4000:
                if pygame.time.get_ticks() - self.score_time > 2000 and pygame.time.get_ticks() - self.score_time < 4020:
                    score.play()
                detials.p2_score(p2_point)
        if player_spawn_counter >= 3:
            if pygame.time.get_ticks() - self.score_time > 6000:
                if pygame.time.get_ticks() - self.score_time > 6000 and pygame.time.get_ticks() - self.score_time < 6020:
                    score.play()
                detials.p3_score(p3_point)
        if player_spawn_counter >= 4:
            if pygame.time.get_ticks() - self.score_time > 8000:
                if pygame.time.get_ticks() - self.score_time > 8000 and pygame.time.get_ticks() - self.score_time < 8020:
                    score.play()
                detials.p4_score(p4_point)

        if player_spawn_counter == 1:
            pygame.draw.rect(screen, BLACK, (0, 200, 1000, 700))
        elif player_spawn_counter == 2:
            pygame.draw.rect(screen, BLACK, (0, 300, 1000, 700))
        elif player_spawn_counter == 3:
            pygame.draw.rect(screen, BLACK, (0, 500, 1000, 700))

        if pygame.time.get_ticks() - self.score_time > self.score_time_add:
            if pygame.time.get_ticks() - self.score_time < self.score_time_add + 20:
                hg.play()
            screen.blit(bg_img, (0, 0))

            p1_FS = sum(p1_TP)
            p2_FS = sum(p2_TP)
            p3_FS = sum(p3_TP)
            p4_FS = sum(p4_TP)

            score_lst = [p1_FS, p2_FS, p3_FS, p4_FS][0:player_spawn_counter]
            res = dict(zip([0, 1, 2, 3][0:player_spawn_counter], score_lst))
            sortdict = dict(sorted(res.items(), key=lambda x:x[1], reverse=True))

            max_score = max(score_lst)

            max_score_pl = score_lst.index(max_score)

            max_score_pl_str = str(max_score)
            for i in max_score_pl_str:
                self.no_image = pygame.transform.scale(self.no_lst[int(i)], (70, 84))
                screen.blit(self.no_image, (55 + self.width_add, 120))
                self.width_add += 48
                if self.width_add >= len(max_score_pl_str)*48:
                    self.width_add = 0

            if player_spawn_counter > 1:
                screen.blit(pygame.transform.scale(self.score_txt_img, (350, 90)), (30, 270))

            for i in sortdict.items():
                if i[0] != max_score_pl:

                    for j in str(i[1]):
                        self.no_image1 = pygame.transform.scale(self.high_no[int(j)], (55, 70))
                        screen.blit(self.no_image1, (160 + self.width_add1, 385 + self.height_addT))
                        self.width_add1 += 35
                        if self.width_add1 >= len(str(i[1]))*35:
                            self.width_add1 = 0

                    self.pl_image1 = pygame.transform.scale(self.pl_image_lst[i[0]][self.pl_image_index], (70, 70))
                    screen.blit(self.pl_image1, (70, 380 + self.height_addT))
                    self.height_addT += 100
                    if self.height_addT >= (player_spawn_counter-1)*100:
                        self.height_addT = 0

            #update image depending on current frame
            self.hs_image = self.high_sc[self.high_sc_index]
            self.pl_image = pygame.transform.scale(self.pl_image_lst[max_score_pl][self.pl_image_index], (80, 80))
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > 500:
                self.no_lst = self.high_no1[:]
                self.update_time = pygame.time.get_ticks()
                self.high_sc_index += 1
                self.pl_image_index += 1
            #if the animation has run out the reset back to the start
            if self.high_sc_index >= len(self.high_sc):
                self.no_lst = self.high_no[:]
                self.high_sc_index = 0
                self.pl_image_index = 0
            
            
            screen.blit(self.pl_image, (50, 33))
            screen.blit(self.hs_image, (150, 38))
            
            self.count += 1
            if self.count == 1:
                self.update_time1 = pygame.time.get_ticks()

            if pygame.time.get_ticks() - self.update_time1 > 4500:
                return True
            else:
                return False

######################################################## SCREEN FADE ######################################################

class ScreenFade():
    def __init__(self, direction, colour, speed, width):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
        self.width = width

    def fade(self):
        global run
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:#whole screen fade
            pygame.draw.circle(screen, BLACK, [screen_width // 2, screen_height // 2], self.fade_counter, self.width)
        if self.direction == 2:#vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, screen_width, 0 + self.fade_counter))
        if self.fade_counter >= screen_width:
            fade_complete = True

        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

        return fade_complete

######################################################## GAME OVER #######################################################

class Game_over():
    def __init__(self):
        self.go_img = pygame.image.load('./resources/images/intro/go.png')
        self.speed = 1
        self.fade_counter = 0
        self.update_time = pygame.time.get_ticks()
        self.finish = False

    def display(self):
        if self.fade_counter == 2:
            gameover.play()

        if self.fade_counter <= 240:
            self.go_img = pygame.transform.scale(self.go_img, (300, 150))
            screen.blit(self.go_img, (((screen_width-150-self.go_img.get_width())//2), (500-self.fade_counter))) #((screen_height-self.go_img.get_height())//2)+(screen_height//2-self.fade_counter))

            if pygame.time.get_ticks() - self.update_time > 15:
                self.update_time = pygame.time.get_ticks()
                self.fade_counter += 2
            detials.score_time = pygame.time.get_ticks()

        elif self.fade_counter > 240:
            self.go_img = pygame.transform.scale(self.go_img, (300, 150))
            screen.blit(self.go_img, (((screen_width-150-self.go_img.get_width())//2), ((screen_height-self.go_img.get_height())//2)+(screen_height//2-self.fade_counter)))
            self.finish = True

    def reset_all(self):
        # reset variables
        global next_enemy, enemy_index, speed_limit, enemy_counter, player_spawn_counter, start_game, world, level_no, current_level, next_level, data

        next_enemy = 1
        enemy_index = 0
        speed_limit = 1
        enemy_counter = 0
        player_spawn_counter = 1
        start_game = True
        level_no = 1
        current_level = 1
        next_level = False
        self.finish = False

        detials.total1_count = 0
        detials.total2_count = 0
        detials.total3_count = 0
        detials.total4_count = 0

        # clear all list
        p1_point.clear()
        p2_point.clear()
        p3_point.clear()
        p4_point.clear()

        p1_TP.clear()
        p2_TP.clear()
        p3_TP.clear()
        p4_TP.clear()

        player_list.clear()
        enemy_list.clear()
        char_list.clear()

        player_list_detial.clear()
        enemy_list_detial.clear()
        char_list_detial.clear()

        enemy_pastaway.clear()
        tank_pastaway.clear()
        player_pastaway.clear()

        powerUP_count.clear()
        enemy_count.clear()
        enemy_levelUP.clear()
        for i in [5, 10, 15]:
            powerUP_count.append(i)
        for i in range(-5,16):
            enemy_count.append(i)
        for i in [6, 11, 16]:
            enemy_levelUP.append(i) 


        # empty all groups
        rocket_group.empty()
        powerUP_group.empty()
        rocket_blast_group.empty()
        wall_blast_group.empty()

        data = world_create()
        world = World(data)

        fade1.fade_counter = 0

def world_create():
    world_data = [
    [   0,    0, rl(), rl(), rl(), rl(), rl(), rl(),    0,    0, rl(), rl(), rl(), rl(), rl(),    0,    0, 1, 1, 1], 
    [   0,    0,    0, rl(), rl(), rl(), rl(),    0,    0, rl(), rl(), rl(), rl(), rl(),    0,    0,    0, 1, 1, 1], 
    [rl(), rl(),    0, rl(), rl(), rl(), rl(),    0, rl(), rl(), rl(), rl(),    0,    0,    0, rl(), rl(), 1, 1, 1], 
    [rl(), rl(),    0, rl(), rl(),    0,    0,    0,    0, rl(), rl(), rl(),    0, rl(), rl(), rl(), rl(), 1, 1, 1], 
    [   0,    0,    0, rl(), rl(),    0, rl(), rl(),    0, rl(), rl(), rl(),    0, rl(), rl(), rl(), rl(), 1, 1, 1], 
    [rl(), rl(),    0, rl(), rl(), rl(), rl(), rl(),    0,    0,    0, rl(),    0, rl(), rl(), rl(), rl(), 1, 1, 1], 
    [rl(), rl(), rl(), rl(), rl(),    0, rl(), rl(), rl(), rl(),    0,    0, rl(), rl(), rl(), rl(), rl(), 1, 1, 1], 
    [rl(), rl(),    0, rl(), rl(), rl(),    0,    0, rl(), rl(), rl(), rl(),    0,    0,    0, rl(), rl(), 1, 1, 1], 
    [rl(), rl(), rl(),    0, rl(), rl(), rl(), rl(), rl(), rl(),    0,    0,    0, rl(),    0, rl(), rl(), 1, 1, 1], 
    [rl(), rl(), rl(),rl(),  rl(),    0,    0,    0, rl(), rl(),    0, rl(), rl(), rl(), rl(), rl(), rl(), 1, 1, 1], 
    [rl(), rl(), rl(),    0,    0, rl(), rl(), rl(), rl(), rl(),    0, rl(), rl(), rl(),    0, rl(), rl(), 1, 1, 1], 
    [rl(), rl(), rl(), rl(), rl(),    0, rl(), rl(), rl(), rl(), rl(), rl(), rl(), rl(),    0, rl(), rl(), 1, 1, 1], 
    [rl(), rl(), rl(), rl(), rl(),    0, rl(),    8,    8,    8,    0, rl(),    0,    0, rl(), rl(), rl(), 1, 1, 1], 
    [rl(), rl(), rl(), rl(),    0,    0,    0,    8,    7,    8,    0,    0,    0, rl(), rl(), rl(), rl(), 1, 1, 1]
    ]                                                   # 
                                                     #centre
    
    return world_data

data = world_create()
world = World(data)
detials = Detials()
ga_ov = Game_over()

#create screen fades
fade1 = ScreenFade(1, BLACK, 4, 0)

#create sprite groups
rocket_group = pygame.sprite.Group()
powerUP_group = pygame.sprite.Group()
rocket_blast_group = pygame.sprite.Group()
wall_blast_group = pygame.sprite.Group()

# creating enemys
enemy_group_list = ["enemy1", "enemy2", "enemy3", "enemy4", "enemy5", "enemy6", "enemy7", "enemy8", 
                    "enemy9", "enemy10", "enemy11", "enemy12", "enemy13", "enemy14", "enemy15", 
                    "enemy16", "enemy17", "enemy18", "enemy19", "enemy20"]

# creating players
player_group_list = ["player1", "player2", "player3", "player4"]

# key assign
key_list = [(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RCTRL), 
            (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_TAB), 
            (pygame.K_KP4, pygame.K_KP6, pygame.K_KP8, pygame.K_KP2, pygame.K_KP5), 
            (pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k, pygame.K_SPACE)]


next_enemy = 1
enemy_index = 0
run = True
level_no = 1
speed_limit = 1
enemy_counter = 0
frame_index = 0
select_tank_pos = 0
select_tank_pos1 = 0
player_spawn_counter = 1
option_select = None
next_level = False
control = False

def control_menu():
    global pl_image, re_img, frame_index, update_time, control_img

    control_img = pygame.transform.scale(control_img, (1000, 700))
    screen.blit(control_img, (0, 0))

    re_img = pygame.transform.scale(re_img, (200, 80))
    screen.blit(re_img, ((screen_width-re_img.get_width())//2, ((screen_height-re_img.get_height())//2)+275))


    #update image depending on current frame
    pl_image = pl_img[frame_index]
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - update_time > 130:
        update_time = pygame.time.get_ticks()
        frame_index += 1
    #if the animation has run out the reset back to the start
    if frame_index >= len(pl_img):
        frame_index = 0

    pl_image = pygame.transform.scale(pl_image, (50, 50))
    screen.blit(pl_image, (((screen_width-pl_image.get_width())//2)-140, ((screen_height-pl_image.get_height())//2)+274))

while run:

    clockobject.tick(fps)
    screen.blit(bg_img, (0, 0))

    if start_game:
        detials.count = 0
        bc_img = pygame.transform.scale(bc_img, (700, 200))
        screen.blit(bc_img, ((screen_width-bc_img.get_width())//2, ((screen_height-bc_img.get_height())//2)-200))

        ps_img = pygame.transform.scale(ps_img, (257, 320))
        screen.blit(ps_img, ((screen_width-ps_img.get_width())//2, ((screen_height-ps_img.get_height())//2)+137))

        #update image depending on current frame
        pl_image = pl_img[frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - update_time > 130:
            update_time = pygame.time.get_ticks()
            frame_index += 1
        #if the animation has run out the reset back to the start
        if frame_index >= len(pl_img):
            frame_index = 0

        pl_image = pygame.transform.scale(pl_image, (40, 40))
        screen.blit(pl_image, (((screen_width-pl_image.get_width())//2)-160, ((screen_height-pl_image.get_height())//2)+select_tank_pos))
        
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    steel.play()
                    if select_tank_pos > 0:
                        select_tank_pos -= 69
                if event.key == pygame.K_DOWN:
                    steel.play()
                    if select_tank_pos < 276:
                        select_tank_pos += 69
                if event.key == pygame.K_RETURN:
                    steel.play()
                    pl_sl = [0, 69, 138, 207, 276]
                    player_spawn_counter = pl_sl.index(select_tank_pos)+1
                    if player_spawn_counter == 5:
                        control = True
                        start_game = False
                    else:
                        for i in player_group_list[0:player_spawn_counter]:
                            char_list.append(i)
                            player_list.append(i)
                            if i == "player1":
                                i = Tank(i, 200, 800, 2, 1, 5, 1)
                            elif i == "player2":
                                i = Tank(i, 300, 800, 2, 1, 5, 1)
                            elif i == "player3":
                                i = Tank(i, 500, 800, 2, 1, 5, 1)
                            elif i == "player4":
                                i = Tank(i, 600, 800, 2, 1, 5, 1)

                            player_list_detial.append(i)
                            char_list_detial.append(i)
                        start_game = False
                        ga_ov.fade_counter = 0
                        gamestart.play()
                        game_start_time = pygame.time.get_ticks()

    elif control:
        control_menu()
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    steel.play()
                    if pass_game != True:
                        start_game = True
                    control = False

    elif pass_game:
        tank_move.set_volume(0.0)
        pause_img = pygame.transform.scale(pause_img, (300, 100))
        screen.blit(pause_img, ((screen_width-pause_img.get_width())//2, ((screen_height-pause_img.get_height())//2)-200))
        
        re_img = pygame.transform.scale(re_img, (200, 80))
        screen.blit(re_img, ((screen_width-re_img.get_width())//2, ((screen_height-re_img.get_height())//2)))
 
        co_img = pygame.transform.scale(co_img, (247, 80))
        screen.blit(co_img, (((screen_width-co_img.get_width())//2)+20, ((screen_height-co_img.get_height())//2)+100))

        qg_img = pygame.transform.scale(qg_img, (200, 80))
        screen.blit(qg_img, ((screen_width-qg_img.get_width())//2, ((screen_height-qg_img.get_height())//2)+200))
 
        #update image depending on current frame
        pl_image = pl_img[frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - update_time > 130:
            update_time = pygame.time.get_ticks()
            frame_index += 1
        #if the animation has run out the reset back to the start
        if frame_index >= len(pl_img):
            frame_index = 0

        pl_image = pygame.transform.scale(pl_image, (50, 50))
        screen.blit(pl_image, (((screen_width-pl_image.get_width())//2)-140, ((screen_height-pl_image.get_height())//2)+select_tank_pos1))
        
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    tank_move.set_volume(0.6)
                    pass_game = False
                if event.key == pygame.K_UP:
                    steel.play()
                    if select_tank_pos1 > 0:
                        select_tank_pos1 -= 100
                if event.key == pygame.K_DOWN:
                    steel.play()
                    if select_tank_pos1 < 200:
                        select_tank_pos1 += 100
                if event.key == pygame.K_RETURN:
                    steel.play()
                    pl_sl = [0, 100, 200]
                    option_select = pl_sl.index(select_tank_pos1)+1
                    if option_select == 1:
                        tank_move.set_volume(0.6)
                        pass_game = False
                    elif option_select == 2:
                        control = True
                    elif option_select == 3:
                        run = False

    elif next_level:
        pygame.draw.rect(screen, BLACK, (0, 0, 1000, 700))
        score_img = pygame.transform.scale(score_img, (900, 500))
        screen.blit(score_img, (50, 100))

        score_time_add = (2000*player_spawn_counter)+4000
        if player_spawn_counter >= 1:
            if pygame.time.get_ticks() - score_time > 2000:
                if pygame.time.get_ticks() - score_time > 2000 and pygame.time.get_ticks() - score_time < 2020:
                    score.play()
                detials.p1_score(p1_point)
                player_list_detial[0].rect.x = 200
                player_list_detial[0].rect.y = 800
        if player_spawn_counter >= 2:
            if pygame.time.get_ticks() - score_time > 4000:
                if pygame.time.get_ticks() - score_time > 4000 and pygame.time.get_ticks() - score_time < 4020:
                    score.play()
                detials.p2_score(p2_point)
                player_list_detial[1].rect.x = 300
                player_list_detial[1].rect.y = 800
        if player_spawn_counter >= 3:
            if pygame.time.get_ticks() - score_time > 6000:
                if pygame.time.get_ticks() - score_time > 6000 and pygame.time.get_ticks() - score_time < 6020:
                    score.play()
                detials.p3_score(p3_point)
                player_list_detial[2].rect.x = 500
                player_list_detial[2].rect.y = 800
        if player_spawn_counter >= 4:
            if pygame.time.get_ticks() - score_time > 8000:
                if pygame.time.get_ticks() - score_time > 8000 and pygame.time.get_ticks() - score_time < 8020:
                    score.play()
                detials.p4_score(p4_point)
                player_list_detial[3].rect.x = 600
                player_list_detial[3].rect.y = 800

        if player_spawn_counter == 1:
            pygame.draw.rect(screen, BLACK, (0, 200, 1000, 700))
        elif player_spawn_counter == 2:
            pygame.draw.rect(screen, BLACK, (0, 300, 1000, 700))
        elif player_spawn_counter == 3:
            pygame.draw.rect(screen, BLACK, (0, 500, 1000, 700))

        if pygame.time.get_ticks() - score_time > score_time_add:
            # claer previous level score
            p1_point.clear()
            p2_point.clear()
            p3_point.clear()
            p4_point.clear()

            enemy_pastaway.clear()

            detials.total1_count = 0
            detials.total2_count = 0
            detials.total3_count = 0
            detials.total4_count = 0

            for i in player_list_detial:
                i.shoot = False
                i.update_action(0)
                i.born_ = True
                i.born = 0
                i.moving_left = False
                i.moving_right = False
                i.moving_up = False
                i.moving_down = False

            score_time = pygame.time.get_ticks()
            current_level += 1
            next_level = False

            gamestart.play()
            game_start_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pass_game = True
                if event.key == pygame.K_ESCAPE:
                    pass_game = True

    else:
        if len(enemy_pastaway) == 20:
            tank_move.set_volume(0.0)
            if fade1.fade():
                next_enemy = 1
                enemy_index = 0
                speed_limit = 1
                enemy_counter = 0
                level_no = 1


                # clear all list
                for i in enemy_list:
                    char_list.remove(i)
                enemy_list.clear()

                for i in enemy_list_detial:
                    char_list_detial.remove(i)
                enemy_list_detial.clear()

                tank_pastaway.clear()

                powerUP_count.clear()
                enemy_count.clear()
                enemy_levelUP.clear()
                for i in [5, 10, 15]:
                    powerUP_count.append(i)
                for i in range(-5,16):
                    enemy_count.append(i)
                enemy_levelUP = [6, 11, 16]


                # empty all groups
                rocket_group.empty()
                powerUP_group.empty()
                rocket_blast_group.empty()
                wall_blast_group.empty()

                data = world_create()
                world = World(data)

                fade1.fade_counter = 0
                score_time = pygame.time.get_ticks()
                next_level = True
       
        elif ga_ov.finish:
            tank_move.set_volume(0.0)
            if detials.high_score():
                ga_ov.reset_all()
            
            for event in pygame.event.get():
            #quit game
                if event.type == pygame.QUIT:
                    run = False

        else:
            if pygame.time.get_ticks() - game_start_time > 2000:
                tank_move.set_volume(0.6)

            world.draw()
            if world.eagle_wall_change:
                world.restore_ewall()

            screen.blit(detial_img, (850, 0))
            if player_spawn_counter == 1:
                pygame.draw.rect(screen, (98,99,98), pygame.Rect(850, 210, 150, 310))
            elif player_spawn_counter == 2:
                pygame.draw.rect(screen, (98,99,98), pygame.Rect(850, 310, 150, 210))
            elif player_spawn_counter == 3:
                pygame.draw.rect(screen, (98,99,98), pygame.Rect(850, 410, 150, 110))

            detials.enemy_count()
            if player_spawn_counter >= 1:
                detials.player1_lives()
            if player_spawn_counter >= 2:
                detials.player2_lives()
            if player_spawn_counter >= 3:
                detials.player3_lives()
            if player_spawn_counter >= 4:
                detials.player4_lives()
            detials.current_level()
        
            
            for i in enemy_count:
                if pygame.time.get_ticks() - counter > 2000:
                    counter = pygame.time.get_ticks()
                    if len(enemy_pastaway) > i and enemy_index <= 19:
                        enemy_counter += 1
                        for j in enemy_levelUP:
                            if enemy_counter >= j:
                                level_no += 1
                                if level_no == 3:
                                    speed_limit = 2
                                elif level_no == 4:
                                    speed_limit = 1
                                enemy_levelUP.remove(j)

                        update_index = enemy_group_list[enemy_index]
                        char_list.append(update_index)
                        enemy_list.append(update_index)
                        if next_enemy == 1:
                            update_index = Tank(update_index, 0, 0, -2, level_no, level_no*3, speed_limit)
                        elif next_enemy == 2:
                            update_index = Tank(update_index, 400, 0, -2, level_no, level_no*3, speed_limit)
                        elif next_enemy == 3:
                            update_index = Tank(update_index, 800, 0, -2, level_no, level_no*3, speed_limit)
                        next_enemy += 1
                        if next_enemy > 3:
                            next_enemy = 1
                        enemy_index += 1
                        enemy_list_detial.append(update_index)
                        char_list_detial.append(update_index)
                        enemy_count.remove(i)
                        

            # draw power_up
            for i in powerUP_count:
                if len(enemy_pastaway) >= i:
                    power_up = Power_up(data)
                    powerUP_group.add(power_up)
                    powerUP_count.remove(i)

            #update and draw groups
            powerUP_group.update()
            for i in powerUP_group:
                i.blink()
                i.remove_power_up()
            powerUP_group.draw(screen)

            #draw_grid()

            #update player actions
            for i in player_list_detial:
                index = char_list_detial.index(i)
                if i.alive:
                    i.update()
                    i.draw()
                    i.move()
                    i.shoot_rocket()
                    #i.AI()
                elif i.alive == False and index not in player_pastaway: 
                    player_pastaway.append(index)
            
            #update enemy actions
            for i in enemy_list_detial:
                index = char_list_detial.index(i)
                if i.alive:
                    i.update()
                    i.draw()
                    i.move()
                    i.shoot_rocket()
                    i.AI()
                elif i.alive == False and char_list[index] not in enemy_pastaway:
                    enemy_pastaway.append(char_list[index])

            rocket_group.update()
            rocket_group.draw(screen)
            
            world.draw_grass()
                
            for i in char_list_detial:
                if i.blast < 3:
                    i.draw_blast()

            rocket_blast_group.update()
            rocket_blast_group.draw(screen)

            wall_blast_group.update()
            wall_blast_group.draw(screen)
            
            if len(player_pastaway) == player_spawn_counter and world.eagle_blast != True:
                ga_ov.display()

            if world.eagle_blast:
                world.eagle_blast_effect()
                if len(player_pastaway) != player_spawn_counter:
                    ga_ov.display()

            for event in pygame.event.get():
                #quit game
                if event.type == pygame.QUIT:
                    run = False

                for i in player_list_detial[0:player_spawn_counter]:
                    if i == player_list_detial[0]:
                        player_index = 0
                    elif i == player_list_detial[1]:
                        player_index = 1
                    elif i == player_list_detial[2]:
                        player_index = 2
                    elif i == player_list_detial[3]:
                        player_index = 3

                    #keyboard presses
                    if event.type == pygame.KEYDOWN and i.alive:
                        if event.key == key_list[player_index][0]:
                            i.update_action(3)
                            i.moving_left = True
                            i.moving_right = i.moving_up = i.moving_down = False
                        elif event.key == key_list[player_index][1]:
                            i.update_action(2)
                            i.moving_right = True
                            i.moving_left = i.moving_up = i.moving_down = False
                        elif event.key == key_list[player_index][2]:
                            i.update_action(0)
                            i.moving_up = True
                            i.moving_left = i.moving_right = i.moving_down = False
                        elif event.key == key_list[player_index][3]:
                            i.update_action(1)
                            i.moving_down = True
                            i.moving_left = i.moving_right = i.moving_up = False
                        if event.key == key_list[player_index][4]:
                            i.shoot = True
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                            pass_game = True

                    #keyboard button released
                    if event.type == pygame.KEYUP:
                        if event.key == key_list[player_index][0]:
                            i.moving_left = False
                        if event.key == key_list[player_index][1]:
                            i.moving_right = False
                        if event.key == key_list[player_index][2]:
                            i.moving_up = False
                        if event.key == key_list[player_index][3]:
                            i.moving_down = False
                        if event.key == key_list[player_index][4]:
                            i.shoot = False
 
    pygame.display.update()

pygame.quit()