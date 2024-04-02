import json
import time

import pygame as pg
import pytmx

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE = 3.5

font = pg.font.Font(None, 40)

class Platforms(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super(Platforms, self).__init__()

        self.image = pg.transform.scale(image, (width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE



class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()

        self.load_animations()
        self.current_animation = self.idle_animation_right
        self.image = self.current_animation[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.center = (200, map_height - 400)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.tmx_map = pytmx.load_pygame("maps/level1.tmx")
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 200

        self.hp = 3
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000


    def load_animations(self):
        tile_size = 48
        tile_scale = 2

        self.idle_animation_right = []

        num_images = 4

        spritesheet = pg.image.load('Sprites/Idle (48 x 48).png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.idle_animation_right.append(image)

        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        self.move_animation_right = []

        num_images = 6

        spritesheet = pg.image.load('Sprites/Running (48 x 48).png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.move_animation_right.append(image)

        self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]


    def update(self, platforms):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()



        if keys[pg.K_a]:
            if self.current_animation != self.move_animation_left:
                self.current_animation = self.move_animation_left
                self.current_image = 0

            self.velocity_x = -10

        elif keys[pg.K_d]:
            if self.current_animation != self.move_animation_right:
                self.current_animation = self.move_animation_right
                self.current_image = 0

            self.velocity_x = 10
        else:
            if self.current_animation == self.move_animation_right:
                self.current_animation = self.idle_animation_right
                self.current_image = 0
            elif self.current_animation == self.move_animation_left:
                self.current_animation = self.idle_animation_left
                self.current_image = 0

            self.velocity_x = 0

        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y


        for layer in self.tmx_map:
            if layer.name == "ONE":
                for platform in platforms:

                    if platform.rect.collidepoint(self.rect.midbottom):
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.is_jumping = False


                    if platform.rect.collidepoint(self.rect.midtop):
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0

                    if platform.rect.collidepoint(self.rect.midright):
                        self.rect.right = platform.rect.left


                    if platform.rect.collidepoint(self.rect.midleft):
                        self.rect.left = platform.rect.right




        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

    def jump(self):
        self.velocity_y = -35
        self.is_jumping = True

    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()

# class Crab(pg.sprite.Sprite):
#     def __init__(self, map_width, map_height):
#         super(Crab, self).__init__()
#
#         self.load_animations()
#         self.current_animation = self.animation
#         self.image = self.current_animation[0]
#         self.current_image = 0
#
#         self.rect = self.image.get_rect()
#         self.rect.center = (100, 100)  # Начальное положение персонажа
#         self.left_edge = 150
#         self.right_edge = 500
#
#         # Начальная скорость и гравитация
#         self.velocity_x = 0
#         self.velocity_y = 0
#         self.gravity = 2
#         self.is_jumping = False
#         self.map_width = map_width * TILE_SCALE
#         self.map_height = map_height * TILE_SCALE
#
#         self.timer = pg.time.get_ticks()
#         self.interval = 300
#
#         self.direction = "right"
#
#
#     def load_animations(self):
#         tile_scale = 2
#         tile_size = 32
#         self.animation = []
#         image = pg.image.load("Sprites/Sprite Pack 2/9 - Snip Snap Crab/Movement_(Flip_image_back_and_forth) (32 x 32).png")
#         image = pg.transform.scale(image, (tile_size * tile_scale,tile_size * tile_scale))
#         self.animation.append(image)
#         self.animation.append(pg.transform.flip(image, True, False))
#
#     def update(self, platforms):
#
#         if self.direction == "right":
#             self.velocity_x = 5
#             if self.rect.right >= self.right_edge:
#                 self.direction = "left"
#
#         if self.direction == "left":
#             self.velocity_x = -5
#             if self.rect.left <= self.left_edge:
#                 self.direction = "right"
#
#
#         new_x = self.rect.x + self.velocity_x
#         if 0 <= new_x <= self.map_width - self.rect.width:
#             self.rect.x = new_x
#
#         self.velocity_y += self.gravity
#         self.rect.y += self.velocity_y
#
#         for platform in platforms:
#
#             if platform.rect.collidepoint(self.rect.midbottom):
#                 self.rect.bottom = platform.rect.top
#                 self.velocity_y = 0
#                 self.is_jumping = False
#
#
#             if platform.rect.collidepoint(self.rect.midtop):
#                 self.rect.top = platform.rect.bottom
#                 self.velocity_y = 0
#
#             if platform.rect.collidepoint(self.rect.midright):
#                 self.rect.right = platform.rect.left
#
#
#
#             if platform.rect.collidepoint(self.rect.midleft):
#                 self.rect.left = platform.rect.right
#         if pg.time.get_ticks() - self.timer > self.interval:
#             self.current_image += 1
#             if self.current_image >= len(self.current_animation):
#                 self.current_image = 0
#             self.image = self.current_animation[self.current_image]
#             self.timer = pg.time.get_ticks()

class Sceleton(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, start_pos, final_pos):
        super(Sceleton, self).__init__()

        self.load_animations()
        self.current_animation = self.move_animation_right
        self.image = self.current_animation[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.bottomleft = start_pos  # Начальное положение персонажа
        self.left_edge = start_pos[0]
        self.right_edge = final_pos[0] + self.image.get_width()

        self.tmx_map = pytmx.load_pygame("maps/level1.tmx")

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 300

        self.direction = "right"

    def load_animations(self):
        tile_size = 32
        tile_scale = 2

        self.move_animation_right = []

        num_images = 6

        spritesheet = pg.image.load('Sprites/Sprite Pack 6/3 - Skeleton/Limping_Movement (32 x 32).png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.move_animation_right.append(image)

        self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]

    def update(self, platforms):

        if self.direction == "right":
            self.velocity_x = 2
            if self.rect.right >= self.right_edge:
                self.current_animation = self.move_animation_left
                self.direction = "left"

        if self.direction == "left":
            self.velocity_x = -2
            if self.rect.left <= self.left_edge:
                self.current_animation = self.move_animation_right
                self.direction = "right"


        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        for platform in platforms:
            for layer in self.tmx_map:
                if layer.name == "ONE":


                    if platform.rect.collidepoint(self.rect.midbottom):
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.is_jumping = False

                    if platform.rect.collidepoint(self.rect.midtop):
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0

                    if platform.rect.collidepoint(self.rect.midright):
                        self.rect.right = platform.rect.left

                    if platform.rect.collidepoint(self.rect.midleft):
                        self.rect.left = platform.rect.right



        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

class Boss(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, start_pos, final_pos):
        super(Boss, self).__init__()

        self.load_animations()
        self.current_animation = self.move_animation_right
        self.image = self.current_animation[0]
        self.current_image = 0

        self.statusOfTheBoss = "normal"

        self.rect = self.image.get_rect()
        self.rect.bottomleft = start_pos  # Начальное положение персонажа
        self.left_edge = start_pos[0]
        self.right_edge = final_pos[0] + self.image.get_width()

        self.tmx_map = pytmx.load_pygame("maps/level1.tmx")

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 300

        self.boss_hp = 20
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000

        self.direction = "right"

    def load_animations(self):
        tile_size = 64
        tile_scale = 6

        self.move_animation_right = []

        num_images = 6

        spritesheet = pg.image.load('Sprites/Cacodaemon Sprite Sheet.png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.move_animation_right.append(image)

        self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]


    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.boss_hp -= 1
            self.damage_timer = pg.time.get_ticks()

        if self.boss_hp == 1:
            self.statusOfTheBoss = "badly"

    def update(self, platforms):

        if self.direction == "right":
            self.velocity_x = 2
            if self.rect.right >= self.right_edge:
                self.current_animation = self.move_animation_left
                self.direction = "left"

        if self.direction == "left":
            self.velocity_x = -2
            if self.rect.left <= self.left_edge:
                self.current_animation = self.move_animation_right
                self.direction = "right"


        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x



        for platform in platforms:
            for layer in self.tmx_map:
                if layer.name == "ONE":


                    if platform.rect.collidepoint(self.rect.midbottom):
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.is_jumping = False

                    if platform.rect.collidepoint(self.rect.midtop):
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0

                    if platform.rect.collidepoint(self.rect.midright):
                        self.rect.right = platform.rect.left

                    if platform.rect.collidepoint(self.rect.midleft):
                        self.rect.left = platform.rect.right



        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Ruby(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, star_pos, fina_pos):
        super(Ruby, self).__init__()

        self.load_animations()
        # self.current_animation = self.move_animation_right
        self.image = self.coin_images[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.bottomleft = star_pos  # Начальное положение персонажа
        self.up_edge = star_pos[1]
        self.rect.topright = fina_pos
        self.down_edge = fina_pos[1] + self.image.get_height()

        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.velocity_y = 0
        self.direction = "down"

    def load_animations(self):
        tile_size = 16
        tile_scale = 2

        self.coin_images = []

        num_images = 1

        spritesheet = pg.image.load('Sprites/Coin_gems/рубин.png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.coin_images.append(image)


    def update(self, platforms):

        if self.direction == "down":
            self.velocity_y = -2
            if self.rect.bottom <= self.down_edge:
                self.current_animation = self.coin_images
                self.direction = "left"

        if self.direction == "left":
            self.velocity_y = 2
            if self.rect.top >= self.up_edge:
                self.current_animation = self.coin_images
                self.direction = "down"


        new_y = self.rect.y + self.velocity_y
        if 0 <= new_y <= self.map_width - self.rect.width:
            self.rect.y = new_y

class Portal(pg.sprite.Sprite):
    def __init__(self, map_width, map_height,pos):
        super(Portal, self).__init__()

        self.load_animations()
        # self.current_animation = self.move_animation_right
        self.image = self.portal_images[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.topright = pos
        self.rect.midleft = pos

        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 150

    def load_animations(self):
        tile_size = 64
        tile_scale = 3

        self.portal_images = []

        num_images = 8

        spritesheet = pg.image.load('Sprites/GreenPortalSpriteSheetAnimation .png')

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.portal_images.append(image)


    def update(self, platforms):

        self.current_animation = self.portal_images

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()

        self.direction = direction
        self.speed = 20
        self.speed2 = 2

        self.ball_timer = pg.time.get_ticks()
        self.ball_interval = 750




        self.image = pg.image.load("Sprites/r.png")
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()

        if self.direction == "right":
            self.rect.x = player_rect.right
        else:
            self.rect.x = player_rect.left

        self.rect.y = player_rect.centery

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
            self.rect.y += self.speed2
        else:
            self.rect.x -= self.speed
            self.rect.y += self.speed2

class Bushes(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super(Bushes, self).__init__()

        self.image = pg.transform.scale(image, (width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE

class Eye(pg.sprite.Sprite):
    def __init__(self, boss_rect, direction_eye):
        super(Eye, self).__init__()

        self.speed = 20

        self.ball_timer = pg.time.get_ticks()
        self.ball_interval = 150

        self.diarection = direction_eye

        self.image = pg.image.load("Sprites/r.png")
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()


        self.rect.x = boss_rect.centerx
        self.rect.y = boss_rect.centery

    def update(self):
        if self.diarection == 1:
            self.rect.y += self.speed
        elif self.diarection == 2:
            self.rect.x += self.speed
            self.rect.y += self.speed
        else:
            self.rect.x -= self.speed
            self.rect.y += self.speed





class Game:
    def __init__(self):
        # Остальной код класса
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4
        self.level = 1
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.setup()


    #noinspection PyAttributeOutsideInit
    def setup(self):
        self.mode = "game"

        self.clock = pg.time.Clock()
        self.is_running = False

        self.collected_coins = 0

        self.background = pg.image.load("Background_1.png")
        self.background = pg.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.bushesx = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.boss_balls = pg.sprite.Group()
        self.bossgroup = pg.sprite.Group()

        self.ball_timer = pg.time.get_ticks()
        self.ball_interval = 1000



        self.eye_timer = pg.time.get_ticks()
        self.eye_interval = 500
        self.direction_eye = 1


        self.tmx_map = pytmx.load_pygame(f"maps/level{self.level}.tmx")

        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE

        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)





        # self.crab = Crab(self.map_pixel_width, self.map_pixel_height)
        # self.all_sprites.add(self.crab)

        # self.sceleton = Sceleton(self.map_pixel_width, self.map_pixel_height)
        # self.all_sprites.add(self.sceleton)

        # self.enemies.add(self.crab)
        # self.enemies.add(self.sceleton)

        for layer in self.tmx_map:
            for x, y, gid in layer:
                if layer.name == 'ONE':
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        platform = Platforms(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight,
                                             self.tmx_map.tilewidth,
                                             self.tmx_map.tileheight)
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)



                else:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    if tile:
                        bushe = Bushes(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight,
                                       self.tmx_map.tilewidth,
                                       self.tmx_map.tileheight)
                        self.all_sprites.add(bushe)
                        self.bushesx.add(bushe)



        with open(f"maps/level{self.level}_enemies.json", "r") as json_file:
            data = json.load(json_file)

        for enemy in data["enemies"]:
            if enemy["name"] == "Boss":
                x1 = enemy["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = enemy["start_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                x2 = enemy["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y2 = enemy["final_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                self.boss = Boss(self.map_pixel_width, self.map_pixel_height, [x1, y1], [x2, y2])

                self.all_sprites.add(self.boss)
                self.bossgroup.add(self.boss)


            elif enemy["name"] == "Sceleton":
                x1 = enemy["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = enemy["start_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                x2 = enemy["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y2 = enemy["final_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                self.sceleton = Sceleton(self.map_pixel_width, self.map_pixel_height, [x1, y1], [x2, y2])

                self.enemies.add(self.sceleton)
                self.all_sprites.add(self.sceleton)


        for coin in data["coins"]:
            if coin["name"] == "Ruby":
                x1 = coin["star_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = coin["star_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                x2 = coin["fina_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y2 = coin["fina_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                self.ruby = Ruby(self.map_pixel_width, self.map_pixel_height, [x1, y1], [x2, y2])

                self.coins.add(self.ruby)
                self.all_sprites.add(self.ruby)

        for portal in data["portals"]:
            if portal["name"] == "Green":
                x1 = portal["pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = portal["pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                self.portal = Portal(self.map_pixel_width, self.map_pixel_height, [x1, y1])

                self.portals.add(self.portal)
                self.all_sprites.add(self.portal)





        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(60)
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if pg.time.get_ticks() - self.ball_timer > self.ball_interval:

                        if self.player.current_animation in (self.player.idle_animation_right, self.player.move_animation_right):
                            direction = "right"
                        else:
                            direction = "left"
                        ball = Ball(self.player.rect, direction)
                        self.balls.add(ball)
                        self.all_sprites.add(ball)
                        self.ball_timer = pg.time.get_ticks()


            if self.mode == "game over":
                if event.type == pg.KEYDOWN:
                    self.setup()

            if self.mode == "game win":
                if event.type == pg.KEYDOWN:
                    self.level = 1
                    self.setup()

        if self.level == 3:
            if self.boss.boss_hp > 0:
                if pg.time.get_ticks() - self.eye_timer > self.eye_interval:
                    eye = Eye(self.boss.rect, self.direction_eye)
                    self.boss_balls.add(eye)
                    self.all_sprites.add(eye)
                    if self.direction_eye < 3:
                        self.direction_eye += 1
                    else:
                        self.direction_eye -= 2

                    print(self.direction_eye)

                    self.eye_timer = pg.time.get_ticks()




    def update(self):

        if self.player.hp <= 0 or self.player.map_height - 1500 < self.player.rect.y:
            self.mode = "game over"
            return


        if self.level == 3:
            if self.boss.boss_hp < 1:
                self.mode = "game win"

        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()

        for boss in self.bossgroup.sprites():
            if pg.sprite.collide_mask(self.player, boss):
                self.player.get_damage()
        for eye in self.boss_balls.sprites():
            if pg.sprite.collide_mask(self.player, eye):
                self.player.get_damage()

        if self.direction_eye > 3:
            self.direction_eye == 1


        for enemy in self.enemies.sprites():
            enemy.update(self.platforms)
        for boss in self.bossgroup.sprites():
            boss.update(self.platforms)
        self.balls.update()
        self.boss_balls.update()
        self.coins.update(self.platforms)
        self.portals.update(self.platforms)


        pg.sprite.groupcollide(self.balls, self.enemies, True, True)
        pg.sprite.groupcollide(self.balls, self.platforms, True, False)
        if self.level == 3:
            if self.boss.statusOfTheBoss == "normal":
                if pg.sprite.groupcollide(self.balls, self.bossgroup, True, False, pg.sprite.collide_mask):
                    self.boss.get_damage()
            else:
                if pg.sprite.groupcollide(self.balls, self.bossgroup, True, True,  pg.sprite.collide_mask):
                    self.boss.get_damage()





        hits = pg.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.collected_coins += 1

        hits = pg.sprite.spritecollide(self.player, self.portals, False, pg.sprite.collide_mask)
        for hit in hits:
            self.level += 1
            if self.level == 4:
                quit()
            self.setup()

        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2

        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))

        self.player.update(self.platforms)




    def draw(self):
        back = pg.image.load("Background_1.png")
        rect = back.get_rect()
        back = pg.transform.scale(back, (rect.width * TILE_SCALE, rect.height * TILE_SCALE))
        self.screen.blit(back, [0, 0])

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))

        pg.draw.rect(self.screen, pg.Color("red"), (20, 13, self.player.hp * 30 * 2, 10 * 2))
        with open("maps/level1_enemies.json", "r") as json_file:
            data = json.load(json_file)
        pg.draw.rect(self.screen, pg.Color("yellow"), (16, 51, self.collected_coins * 90 / len(data["coins"]) * 2, 20))

        if self.mode == "game over":
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
        if self.mode == "game win":
            text = font.render("GAME WIN", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        hpImage = pg.image.load('Sprites/hp.png')
        self.screen.blit(pg.transform.scale(hpImage, (212, 32)), [0, 7])
        rubyImage = pg.image.load('Sprites/монеты.png')
        self.screen.blit(pg.transform.scale(rubyImage, (212, 32)), [4, 45])

        if self.level == 3:
            pg.draw.rect(self.screen, pg.Color("#8B0000"), (250, 13, self.boss.boss_hp * 15, 20))
            if self.boss.boss_hp > 0:
                bossBarImage = pg.image.load('Sprites/BossBar1.png')
                self.screen.blit(pg.transform.scale(bossBarImage, (126 * 2.5, 32)), [247, 4])


        pg.display.flip()


if __name__ == "__main__":
    game = Game()
