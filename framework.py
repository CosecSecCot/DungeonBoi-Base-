import pygame
import json


# collisions ----------------------------- #
def collision_test(rect, tiles):
    hit_list = []
    for t in tiles:
        if rect.colliderect(t):
            hit_list.append(t)
    return hit_list


# movement ------------------------------- #
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for t in hit_list:
        if movement[0] > 0:
            rect.right = t.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = t.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for t in hit_list:
        if movement[1] > 0:
            rect.bottom = t.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = t.bottom
            collision_types['top'] = True
    return rect, collision_types


# sprite sheet ---------------------------- #
class Sprite_sheet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.meta_data = self.file_name.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x = sprite["x"]
        y = sprite["y"]
        w = sprite["w"]
        h = sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image

# fade = CrossFade(screen, resolution[0], resolution[1])
# fade_sprite = pygame.sprite.Group(fade)
# while -----------------------------------
# if 'condition':
    # fade.fade_dir *= -1
# fade_sprite.update()
# fade_sprite.draw(screen)

class CrossFade(pygame.sprite.Sprite):
    def __init__(self, display, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image = self.image.convert() 
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = w / 2
        self.rect.centery = h / 2

        self.fade_dir = 1
        self.trans_value = 255
        self.fade_speed = 2
        self.delay = 1
        self.increment = 0
        self.image.set_alpha(self.trans_value)

    def update(self):
        self.image.set_alpha(self.trans_value)
        self.increment += 1

        if self.increment >= self.delay:
            self.increment = 0

        if self.fade_dir > 0:
            if self.trans_value - self.fade_speed < 0:
                self.trans_value = 0
            else:
                self.trans_value -= self.fade_speed

        elif self.fade_dir < 0:
            if self.trans_value + self.delay > 255:
                self.trans_value = 255
            else:
                self.trans_value += self.fade_speed
