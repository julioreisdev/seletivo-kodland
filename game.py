import math

WIDTH = 800
HEIGHT = 600
GRAVITY = 0.5
BOTTOM_LEVEL = HEIGHT // 2 + 120 

music.play('theme')
game_state = 'menu'
sound_on = True
start_screen_hero_time = 0
game_screen_fly_time = 0

general_background = Actor('general_background', topleft=(0, 0))
menu_background = Actor('menu_background', center=(WIDTH - 300, HEIGHT // 2))
logo = Actor('logo', center=(WIDTH - 300, HEIGHT -  400))

class Character:
    global game_state
    def __init__(self, images, pos, normal_images=None):
        self.images = images
        self.normal_images = normal_images or [images[0]]
        self.actor = Actor(self.normal_images[0], pos)
        self.frame = 0
        self.y_velocity = 0

    def animate(self, moving=False):
        if moving:
            self.frame += 0.2
            if self.frame >= len(self.images):
                self.frame = 0
            self.actor.image = self.images[int(self.frame)]
        else:
            if game_state == 'playing':
                self.frame += 0.02
                if self.frame >= len(self.normal_images):
                    self.frame = 0
                self.actor.image = self.normal_images[int(self.frame)]
            else:
                self.actor.image = self.normal_images[1]

    def draw(self):
        self.actor.draw()

    def set_pos(self, pos):
        self.actor.pos = pos

    @property
    def x(self):
        return self.actor.x

    @x.setter
    def x(self, value):
        self.actor.x = value

    @property
    def y(self):
        return self.actor.y

    @y.setter
    def y(self, value):
        self.actor.y = value

    @property
    def left(self):
        return self.actor.left

    @left.setter
    def left(self, value):
        self.actor.left = value

    @property
    def right(self):
        return self.actor.right

    @right.setter
    def right(self, value):
        self.actor.right = value

    @property
    def bottom(self):
        return self.actor.bottom

    @bottom.setter
    def bottom(self, value):
        self.actor.bottom = value

    @property
    def height(self):
        return self.actor.height

    def colliderect(self, other):
        return self.actor.colliderect(other.actor)

class Bee(Character):
    def __init__(self, pos):
        images = ['bee_a', 'bee_b', 'bee_b', 'bee_c', 'bee_c']
        super().__init__(images, pos)

    def update(self):
        self.x -= 2
        self.frame += 0.1
        if self.frame >= len(self.images):
            self.frame = 0
        self.actor.image = self.images[int(self.frame)]
        if self.actor.right < 0:
            self.actor.left = WIDTH

class Fly(Character):
    def __init__(self, pos):
        images = ['fly_a', 'fly_b', 'fly_b', 'fly_rest', 'fly_rest']
        super().__init__(images, pos)
        self.fly_time = 0

    def update(self):
        self.x -= 3
        self.frame += 0.1
        if self.frame >= len(self.images):
            self.frame = 0
        self.actor.image = self.images[int(self.frame)]
        if self.actor.right < 0:
            self.actor.left = WIDTH

        self.fly_time += 0.05
        amplitude = 60
        self.y = HEIGHT // 2 + math.sin(self.fly_time) * amplitude

class Hero(Character):
    def __init__(self, pos):
        walk_images = ['walk_b', 'walk_c', 'walk_d']
        normal_images = ['back', 'walk_a']
        super().__init__(walk_images, pos, normal_images)
        self.y_velocity = 0

    def update(self, keys, sound_on):
        moving = False
        if keys.right:
            self.x += 7
            moving = True
        elif keys.left:
            self.x -= 7
            moving = True

        self.animate(moving)

        self.y_velocity += GRAVITY
        self.y += self.y_velocity
        if self.bottom > BOTTOM_LEVEL:
            self.bottom = BOTTOM_LEVEL
            self.y_velocity = 0

        if keys.up and self.bottom == BOTTOM_LEVEL:
            if sound_on:
                sounds.up.play()
            self.y_velocity = -15

        if self.left > WIDTH:
            self.right = 0
        if self.right < 0:
            self.left = WIDTH

hero = Hero((WIDTH // 6, HEIGHT // 2))
bee = Bee((WIDTH - 25, BOTTOM_LEVEL - 50))
fly = Fly((WIDTH - 25, BOTTOM_LEVEL - 50))

button_start = Actor('button_start', (WIDTH - 300, HEIGHT - 200))
button_sound = Actor('button_sound_off', (WIDTH - 300, HEIGHT - 275))
button_exit = Actor('button_exit', (WIDTH - 150, HEIGHT - 400))
button_menu = Actor('button_menu', (WIDTH - 50, 50))

def draw():
    screen.fill((68,71,90))
    general_background.draw()
    hero.draw()

    if game_state == 'menu':
        draw_menu()
    elif game_state == 'playing':
        draw_playing()

def draw_playing(): 
    button_menu.draw()
    bee.draw()
    fly.draw()
    
def draw_menu():
    hero.set_pos((WIDTH // 6, HEIGHT // 2))
    menu_background.draw()
    logo.draw()
    button_start.draw()
    button_exit.draw()
    
    if sound_on:
        button_sound.image = 'button_sound_off'
    else:
        button_sound.image = 'button_sound_on'
    button_sound.draw()

def update():
    global start_screen_hero_time, game_state
    if game_state == 'menu':
        start_screen_hero_time += 0.05
        top = 20
        hero.y = HEIGHT // 2 + math.sin(start_screen_hero_time) * top
        hero.animate(False)
    elif game_state == 'playing':
        if hero.colliderect(bee) or hero.colliderect(fly):
            if sound_on:
                sounds.game_over.play()
            game_state = 'menu'

        hero.update(keyboard, sound_on)
        bee.update()
        fly.update()

def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == 'menu':
        if button_start.collidepoint(pos):
            if sound_on:
                sounds.click.play()
                music.play('bee_music')
            hero.set_pos((100, BOTTOM_LEVEL - (hero.height / 2)))
            bee.set_pos((WIDTH - 25, BOTTOM_LEVEL - 50))
            fly.set_pos((WIDTH - 25, BOTTOM_LEVEL - 50))
            game_state = 'playing'

        if button_sound.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                sounds.click.play()
                music.set_volume(1.0)
            else:
                music.set_volume(0.0)

        if button_exit.collidepoint(pos):
            if sound_on:
                sounds.click.play()
            quit()
    elif game_state == 'playing':
        if button_menu.collidepoint(pos):
            if sound_on:
                sounds.click.play()
                music.play('theme')
            game_state = 'menu'
