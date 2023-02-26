import pygame
from pygame.locals import *
import sys
import random
import framework as fw

pygame.init()
resolution = (1280, 720)
pygame.display.set_caption('Lost in Mind')
screen = pygame.display.set_mode(resolution, FULLSCREEN)
display_res = [resolution[0] / 3, resolution[1] / 3]
display = pygame.Surface(display_res)
pygame.mixer.pre_init(44100, -16, 2, 512)
fps_clock = pygame.time.Clock()

# game variables ------------------- #
fade = fw.CrossFade(display, display_res[0], display_res[1])
fade_sprite = pygame.sprite.Group(fade)
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
death_counter = 0
true_scroll = [0, 0]
fall_weight = [0.45, 0.50, 0.60, 0.75]
fall_weight_multiplier = 0


# sounds -------------------------- #
def load_sound(path):
    sound = pygame.mixer.Sound('data/music/sfx/' + path)
    return sound


jump = load_sound('jump.wav')
death = load_sound('death.wav')
potion_pickup = [load_sound('potion_effect_1.wav'),
                 load_sound('potion_effect_2.wav'),
                 load_sound('potion_effect_3.wav')]

pygame.mixer.music.load('data/music/Space+Ambience+-+320bit.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
jump.set_volume(0.3)


# images -------------------------- #
def load_img(path):
    img = pygame.image.load('data/images/' + path)
    img.set_colorkey((0, 0, 0))
    return img


d_1 = load_img('tiles_0/a_0.png')
d_2 = load_img('tiles_0/a_1.png')
d_3 = load_img('tiles_0/a_2.png')

p_1 = load_img('collectables/potions/potion_of_healing.png')

o_1 = load_img('obstacles/spinner/o_1.png')
o_2 = load_img('obstacles/spinner/o_2.png')
o_fall = load_img('obstacles/o_4.png')

# font --------------------------- #
font = pygame.font.Font('data/font/kongtext.regular.ttf', 9)


# map loader ---------------------- #
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    lvl = []
    for row in data:
        lvl.append(list(row))
    return lvl


lvl_1 = load_map('data/game_map/tut_1')


# animation work ---------------------- #
animation_frames = {}


def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((0, 0, 0))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame
        

animation_database = {'run': load_animation('data/images/player_animations/run', [7, 7, 7, 3]),
                      'idle': load_animation('data/images/player_animations/idle', [20, 20]),
                      'jump': load_animation('data/images/player_animations/jump', [20])}

player_action = 'idle'
player_frame = 0
player_flip = False
player_rect = pygame.Rect(100, 100, 14, 22)


# object ----------------------------- #
class Obj(object):
    def __init__(self, loc, img):
        self.loc = loc
        self.img = img

    def render(self, surface, scr):
        surface.blit(self.img, (self.loc[0] - scr[0], self.loc[1] - scr[1]))

    def rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], self.img.get_width(), self.img.get_height())

    def collide(self, c_rect):
        obj_rect = self.rect()
        return obj_rect.colliderect(c_rect)


potions = [Obj((540, 75), p_1)]
obstacles = [Obj((160, 314), o_1),
             Obj((392, 330), o_2)]
falling_lvl_1 = [Obj([240, 272], o_fall),
                 Obj([265, 224], o_fall),
                 Obj([290, 192], o_fall)]

# game loop -------------------------- #
while True:
    display.fill((20, 20, 20))

    # print(player_rect.x, player_rect.y)

    # camera
    true_scroll[0] += (player_rect.x - true_scroll[0] - display_res[0] / 2) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - display_res[1] / 2) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    if scroll[0] <= 0:
        scroll[0] = 0
    elif scroll[0] >= 262:
        scroll[0] = 262
    if scroll[1] < 10:
        scroll[1] = 10

    # falling rocks
    falling_lvl_1[0].render(display, scroll)
    falling_lvl_1[0].loc[1] += random.choice(fall_weight)
    if falling_lvl_1[0].loc[1] > 350:
        falling_lvl_1[0].loc[1] = 272
    if falling_lvl_1[0].collide(player_rect):
        death.play()
        player_rect.x = 70
        player_rect.y = 90
        death_counter += 1
    falling_lvl_1[1].render(display, scroll)
    falling_lvl_1[1].loc[1] += random.choice(fall_weight)
    if falling_lvl_1[1].loc[1] > 350:
        falling_lvl_1[1].loc[1] = 272
    if falling_lvl_1[1].collide(player_rect):
        death.play()
        player_rect.x = 70
        player_rect.y = 90
        death_counter += 1
    falling_lvl_1[2].render(display, scroll)
    falling_lvl_1[2].loc[1] += random.choice(fall_weight)
    if falling_lvl_1[2].loc[1] > 370:
        falling_lvl_1[2].loc[1] = 272
    if falling_lvl_1[2].collide(player_rect):
        death.play()
        player_rect.x = 70
        player_rect.y = 90
        death_counter += 1

    # initializing game_map
    tile_rect = []
    y = 0
    for layer in lvl_1:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(d_1, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '2':
                display.blit(d_2, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '3':
                display.blit(d_3, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile != '0':
                tile_rect.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    # player movement
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    # implementing animations
    if player_movement[0] == 0:
        if air_timer > 6:
            player_action, player_frame = change_action(player_action, player_frame, 'jump')
        else:
            player_action, player_frame = change_action(player_action, player_frame, 'idle')
    if player_movement[0] > 0:
        if air_timer > 6:
            player_flip = False
            player_action, player_frame = change_action(player_action, player_frame, 'jump')
        else:
            player_flip = False
            player_action, player_frame = change_action(player_action, player_frame, 'run')
    if player_movement[0] < 0:
        if air_timer > 6:
            player_flip = True
            player_action, player_frame = change_action(player_action, player_frame, 'jump')
        else:
            player_flip = True
            player_action, player_frame = change_action(player_action, player_frame, 'run')

    player_rect, collisions = fw.move(player_rect, player_movement, tile_rect)

    # avoiding multiple jumps
    if collisions['bottom']:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    # avoiding sticking to the top tiles
    if collisions['top']:
        vertical_momentum += 2

    # player facing left/right and animation loop
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img, player_flip, False),
                 (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    # potions
    for potion in potions:
        potion.render(display, scroll)
        if potion.collide(player_rect):
            potions.remove(potion)
            random.choice(potion_pickup).play()

    # obstacles
    for obs in obstacles:
        obs.render(display, scroll)
        if obs.collide(player_rect):
        	death.play()
        	player_rect.x = 100
        	player_rect.y = 100
        	death_counter += 1

    ### print(player_rect.x, player_rect.y)

    death_text = font.render('Deaths: ' + str(death_counter), False, (255, 255, 255))
    display.blit(death_text, (5, 5))

    # event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_SPACE:
                if air_timer < 6:
                    jump.play()
                    vertical_momentum = -4.5

        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False

    fade_sprite.update()
    fade_sprite.draw(display)
        
    screen.blit(pygame.transform.scale(display, resolution), (0, 0))
    pygame.display.update()
    fps_clock.tick(60)
