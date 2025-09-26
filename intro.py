import csv
import random

WIDTH = 1120
HEIGHT = 640
tile_size = 16

class Hero:
    def __init__(self, x, y):
        self.actor = Actor("herochar_idle_anim_1", (x, y))
        self.lifes = 3
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.direction = "right"  # "right" ou "left"
        self.current_frame = 0
        self.frame_timer = 0
        self.state = "idle"  # idle, run, jump, dead

        # Carregando os frames das animações
        self.idle_frames = [f"herochar_idle_anim_{i}" for i in range(1, 5)]
        self.idle_frames_left = [f"herochar_idle_anim_left_{i}" for i in range(1, 5)]
        
        self.run_frames = [f"herochar_run_anim_{i}" for i in range(1, 7)]
        self.run_frames_left = [f"herochar_run_anim_left_{i}" for i in range(1, 7)] 

        self.jump_up_frames = [f"herochar_jump_up_anim_{i}" for i in range(1, 4)]
        self.jump_up_frames_left = [f"herochar_jump_up_anim_left_{i}" for i in range(1, 4)]

        self.jump_down_frames = [f"herochar_jump_down_anim_{i}" for i in range(1, 4)]
        self.jump_down_frames_left = [f"herochar_jump_down_anim_left_{i}" for i in range(1, 4)]

        self.jump_double_frames = [f"herochar_jump_double_anim_{i}" for i in range(1, 4)]
        self.jump_double_frames_left = [f"herochar_jump_double_anim_{i}" for i in range(1, 4)]

        self.dead_frames = [f"herochar_death_anim_{i}" for i in range(1, 9)]
        self.dead_frames_left = [f"herochar_death_anim_left_{i}" for i in range(1, 9)]

    def update(self):
        if self.state == "dead":
            self.animate()
            if self.current_frame == len(self.dead_frames) - 1 and self.frame_timer == 0:
                self.respawn()
            return
        
        self.vx = 0
        if keyboard.left:
            self.vx = -4
            self.direction = "left"
        elif keyboard.right:
            self.vx = 4
            self.direction = "right"
        if keyboard.up and self.on_ground:
            self.vy = -12
            self.on_ground = False
            self.on_jumping = True
            if music_on:
                sounds.jump_1.play()

        # Gravidade
        self.vy += 0.5
        if self.vy > 10:
            self.vy = 10

        # Aplicar movimento
        self.actor.x += self.vx
        self.actor.y += self.vy


        # Atualizar estado
        previous_state = self.state
        if not self.on_ground:
            if self.vy < 0:
                self.state = "jump_up"
            else:
                self.state = "jump_down"
        elif self.vx != 0:
            self.state = "run"
        else:
            self.state = "idle"

        # Resetar frame se mudou de estado
        if self.state != previous_state:
            self.current_frame = 0
            self.frame_timer = 0

        # Colisão com o solo
        self.check_collision()
        # Atualizar animação
        self.animate()


    def check_collision(self):
        self.on_ground = False
        for tile in tiles:
            if self.actor.colliderect(tile):
                # Colisão por baixo (chão)
                if self.vy > 0 and self.actor.bottom >= tile.top and self.actor.bottom - self.vy <= tile.top:
                    self.actor.bottom = tile.top
                    self.vy = 0
                    self.on_ground = True
                # Colisão por cima (teto)
                elif self.vy < 0 and self.actor.top <= tile.bottom and self.actor.top - self.vy >= tile.bottom:
                    self.actor.top = tile.bottom
                    self.vy = 0
                # Colisão pela esquerda
                elif self.vx < 0 and self.actor.left <= tile.right and self.actor.left - self.vx >= tile.right:
                    self.actor.left = tile.right
                    self.vx = 0
                # Colisão pela direita
                elif self.vx > 0 and self.actor.right >= tile.left and self.actor.right - self.vx <= tile.left:
                    self.actor.right = tile.left
                    self.vx = 0
        enemies = [slime_1, slime_2, slime_3]
        if not all(getattr(e, "killed", False) for e in enemies) and self.actor.colliderect(VICTORY_ZONE):
            print("kill the enemies first!")
            self.actor.left = VICTORY_ZONE.right
            self.vx = 0

    def respawn(self):
        if self.lifes > 1:
            self.lifes -= 1
            self.actor.topleft = (40, 500)
            self.vx = 0
            self.vy = 0
            self.on_ground = True
            self.state = "idle"
            self.current_frame = 0
            self.frame_timer = 0
            self.actor.image = self.idle_frames[0] if self.direction == "right" else self.idle_frames_left[0]
            #print(f"Lifes remaining: {self.lifes}")
        else:
            print("Game Over")
            global game_state
            game_state = "game_over"

    def restart(self):
        self.lifes = 3
        self.actor.topleft = (40, 500)
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.state = "idle"
        self.current_frame = 0
        self.frame_timer = 0

    def animate(self):
        if self.state == "jump_up":
            self.frame_timer += 1
            if self.frame_timer >= 4:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.jump_up_frames)
            if self.direction == "left":
                self.actor.image = self.jump_up_frames_left[self.current_frame]
            else:
                self.actor.image = self.jump_up_frames[self.current_frame]
        elif self.state == "jump_down":
            self.frame_timer += 1
            if self.frame_timer >= 4:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.jump_down_frames)
            if self.direction == "left":
                self.actor.image = self.jump_down_frames_left[self.current_frame]
            else:
                self.actor.image = self.jump_down_frames[self.current_frame]
        elif self.state == "idle":
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            if self.direction == "left":
                self.actor.image = self.idle_frames_left[self.current_frame]
            else:
                self.actor.image = self.idle_frames[self.current_frame]
        elif self.state == "run":
            self.frame_timer += 1
            if self.frame_timer >= 4:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
            if self.direction == "left":
                self.actor.image = self.run_frames_left[self.current_frame]
            else:
                self.actor.image = self.run_frames[self.current_frame]
        elif self.state == "dead":
            self.frame_timer += 1
            if self.frame_timer >= 7:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.dead_frames)
            if self.direction == "left":
                self.actor.image = self.dead_frames_left[self.current_frame]
            else:
                self.actor.image = self.dead_frames[self.current_frame]
    
    def draw(self):
        self.actor.draw()

class Enemy:
    def __init__(self, x, y):
        self.actor = Actor("slime_idle_anim_1", (x, y))
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.direction = "right"  # "right" ou "left"
        self.current_frame = 0
        self.frame_timer = 0
        self.state = "idle"
        self.timer = 0

        self.idle_frames = [f"slime_idle_anim_{i}" for i in range(1, 6)]
        self.idle_frames_left = [f"slime_idle_anim_left_{i}" for i in range(1, 6)]

        self.run_frames = [f"slime_walk_anim_{i}" for i in range(1, 16)]
        self.run_frames_left = [f"slime_walk_anim_left_{i}" for i in range(1, 16)]

        self.dead_frames = [f"slime_death_anim_{i}" for i in range(1, 7)]
        self.dead_frames_left = [f"slime_death_anim_left_{i}" for i in range(1, 7)]

        self.speed = 2
        self.patrol_min = x - 80
        self.patrol_max = x + 80

        self.change_interval = random.randint(180, 320)
        self.killed = False
    def update(self):
        if self.state == "dead":
            self.animate()
            if self.current_frame == len(self.dead_frames) - 1 and self.frame_timer == 0:
                self.actor.topleft = (-1000, 1000)
                return
        # Gravidade
        self.vy += 0.5
        if self.vy > 10:
            self.vy = 10


        # Aplicar movimento
        self.actor.x += self.vx
        self.actor.y += self.vy

        self.check_collision()
        self.animate()
        self.random_state()
        self.check_player_collision(player)

    def check_collision(self):
        self.on_ground = False
        for tile in tiles:
            if self.actor.colliderect(tile):
                # Colisão por baixo (chão)
                if self.vy > 0 and self.actor.bottom >= tile.top and self.actor.bottom - self.vy <= tile.top:
                    self.actor.bottom = tile.top
                    self.vy = 0
                    self.on_ground = True
                # Colisão por cima (teto)
                elif self.vy < 0 and self.actor.top <= tile.bottom and self.actor.top - self.vy >= tile.bottom:
                    self.actor.top = tile.bottom
                    self.vy = 0
                # Colisão pela esquerda
                elif self.vx < 0 and self.actor.left <= tile.right and self.actor.left - self.vx >= tile.right:
                    self.actor.left = tile.right
                    self.vx = 0
                # Colisão pela direita
                elif self.vx > 0 and self.actor.right >= tile.left and self.actor.right - self.vx <= tile.left:
                    self.actor.right = tile.left
                    self.vx = 0

    def animate(self):
        if self.state == "idle":
            self.frame_timer += 1
            if self.frame_timer >= 7:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            if self.direction == "left":
                self.actor.image = self.idle_frames_left[self.current_frame]
            else:
                self.actor.image = self.idle_frames[self.current_frame]
        elif self.state == "patrol":
            prev_bottom = self.actor.bottom
            self.frame_timer += 1
            if self.frame_timer >= 9:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            if self.direction == "left":
                self.actor.image = self.run_frames_left[self.current_frame]
                self.actor.bottom = prev_bottom
            else:
                self.actor.image = self.run_frames[self.current_frame]
                self.actor.bottom = prev_bottom
        elif self.state == "dead":
            self.frame_timer += 1
            if self.frame_timer >= 7:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.dead_frames)
            if self.direction == "left":
                self.actor.image = self.dead_frames_left[self.current_frame]
            else:
                self.actor.image = self.dead_frames[self.current_frame]

    def patrol(self):
        if self.state == "patrol":
            if self.actor.x <= self.patrol_min:
                self.actor.x = self.patrol_min
                self.direction = "right"
                self.vx = self.speed
            elif self.actor.x >= self.patrol_max:
                self.actor.x = self.patrol_max
                self.direction = "left"
                self.vx = -self.speed
            if self.direction == "right":
                self.vx = self.speed
            else:
                self.vx = -self.speed

    def random_state(self):
        if not self.state == "dead":
            previous = self.state
            self.timer += 0.5
            if self.timer >= 120:
                self.state = random.choice(["idle", "patrol"])
                self.timer = 0
            # reset de frames quando o estado muda para evitar index errors
            if self.state != previous:
                self.current_frame = 0
                self.frame_timer = 0            
            if self.state == "idle":
                self.vx = 0
            elif self.state == "patrol":
                self.patrol()
    def draw(self):
        self.actor.draw()
    
    def check_player_collision(self, player):
        global music_on
        if self.state == "dead":
            return
        if player.actor.colliderect(self.actor):
            # posição anterior do pé do herói (antes do movimento vertical)
            prev_bottom = player.actor.bottom - player.vy
            # se está caindo e antes do movimento estava acima da cabeça do slime -> stomp
            if player.vy > 0 and prev_bottom <= self.actor.top + 6:
                # remover/neutralizar o slime (alternativa simples sem tocar na classe Enemy)
                self.vx = 0
                self.vy = 0
                self.state = "dead"
                self.killed = True
                self.current_frame = 0
                self.frame_timer = 0
                if music_on:
                    sounds.hurt_1.play()
                # dar bounce no herói
                player.vy = -10
                player.on_ground = False
                player.state = "jump_up"
            else:
                # colisão lateral/por baixo: o herói morre
                player.state = "dead"
    def restart(self, x, y):
        self.state = "idle"
        self.killed = False
        self.current_frame = 0
        self.actor.center = (x, y)
     
class lifes:
    def __init__(self, x, y):
        self.actor = Actor("hearts_hud", (x, y))
        self.frame_timer = 0
        self.current_frame = 0
        self.lost_hearts_frames = [f"lost_hearts_anim_{i}" for i in range(1, 6)]

    def draw(self):
        self.actor.draw()
    def draw_lost_heart(self):
        self.actor.image = "no_hearts_hud"
        self.actor.draw()
    def animate_lost_heart(self):
        if player.state == "dead":
            self.frame_timer += 1
            if self.frame_timer >= 5:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.lost_hearts_frames)
            self.actor.image = self.lost_hearts_frames[self.current_frame]
    def update(self):
        self.animate_lost_heart()
    def restart(self):
        self.actor.image = "hearts_hud"

class strange_door:
    def __init__(self, x, y):
        self.actor = Actor("strange_door_closed_anim_1", (x, y))
        self.frame_timer = 0
        self.current_frame = 0
        self.state = "closed"
        self.door_closed_frames = [f"strange_door_closed_anim_{i}" for i in range(1, 11)]
        self.door_open_frames = [f"strange_door_opening_anim_{i}" for i in range(1, 15)]
    def draw(self):
        self.actor.draw()
    def animate(self):
        if self.state == "closed":
            self.frame_timer += 1
            if self.frame_timer >= 7:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.door_closed_frames)
            self.actor.image = self.door_closed_frames[self.current_frame]
        else:
            self.frame_timer += 1
            if self.frame_timer >= 10:
                self.frame_timer = 0
                if self.current_frame < len(self.door_open_frames) - 1:
                    self.current_frame += 1
            self.actor.image = self.door_open_frames[self.current_frame]
    def update(self):
        enemies = [slime_1, slime_2, slime_3]
        if all(getattr(e, "killed", False) for e in enemies):
            self.state = "open"
        if self.state == "open":
            self.animate()
            return
        else:
            self.animate()
    def restart(self):
        self.state = "closed"
        self.current_frame = 0
        self.frame_timer = 0

# --- MENU ---
start_button = Rect((270, 150),(300, 100))
sound_button = Rect((270, 300),(300, 100))
exit_button = Rect((270, 450),(300, 100))
COLOR = (136, 170, 189)
game_state = "menu"

# --- HERO ---
player = Hero(40, 500)

# --- SLIMES ---
slime_1 = Enemy(600, 400)
slime_2 = Enemy(600, 100)
slime_3 = Enemy(1000, 550)

# --- LIFE HUD --- 
life_hud_1 = lifes(50, 50) 
life_hud_2 = lifes(100, 50) 
life_hud_3 = lifes(150, 50) 

#--- BACKGROUND ---
bg = Actor("background")

# --- MAPA ---
tile_images = {
    0: 'tileset_01',
    1: 'tileset_02',
    2: 'tileset_03',
    6: 'tileset_07',
    7: 'tileset_08',
    8: 'tileset_09',
    12: 'tileset_13',
    13: 'tileset_14',
    14: 'tileset_15',
    18: 'tileset_19',
    20: 'tileset_21',
    24: 'tileset_25',
    25: 'tileset_26',
    26: 'tileset_27',
    27: 'tileset_28',
    29: 'tileset_30',
    30: 'tileset_31',
}

tiles = []

def load_map(mapa):
    with open(mapa) as file:
        reader = csv.reader(file)
        for y, row in enumerate(reader):
            for x, tile_id in enumerate(row):
                tile_id = int(tile_id)
                if tile_id in tile_images:
                    tile = Actor(tile_images[tile_id])
                    tile.topleft = (x * tile_size, y * tile_size)
                    tiles.append(tile)

load_map("map.csv")
VICTORY_ZONE = Rect((0, 144), (16, 48))
door = strange_door(8, 168)
music_on = True
music_playing = False
# --- DRAW ---
def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()
    elif game_state == "win":
        draw_win()
    elif game_state == "game_over":
        draw_game_over()

def update():
    global game_state
    musics()
    if game_state == "game":
        player.update()
        slime_1.update()
        slime_2.update()
        slime_3.update()
        win_condition()
        heart_hud()
        door.update()
                    
    if game_state == "game_over":
        if keyboard.r:
            restart_game()
    
    if game_state == "win":
        if keyboard.r:
            restart_game()

def on_mouse_down(pos):
    global game_state
    global music_on
    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "game"
            if music_on:
                sounds.confirmation_002.play()
        elif sound_button.collidepoint(pos):
            print("SOUND")
            if music_on:
                sounds.click_002.play()
            if music_on:
                music_on = False
                print(music_on)
            elif not music_on:
                music_on = True
                print(music_on)
        elif exit_button.collidepoint(pos):
            if music_on:
                sounds.click_002.play()
            print("EXIT")
            exit()

def draw_menu():
    bg.draw()
    screen.draw.filled_rect(start_button, COLOR)
    screen.draw.text("START", center=start_button.center, fontsize=40, color="white")
    screen.draw.filled_rect(sound_button, COLOR)
    if music_on:
        screen.draw.text("SOUND on", center=sound_button.center, fontsize=40, color="white")
    else:
        screen.draw.text("SOUND off", center=sound_button.center, fontsize=40, color="white")
    screen.draw.filled_rect(exit_button, COLOR)
    screen.draw.text("EXIT", center=exit_button.center, fontsize=40, color="white")

def draw_game():
    bg.draw()
    screen.draw.filled_rect(VICTORY_ZONE, (203,145,128))
    door.draw()
    for tile in tiles:
        tile.draw()
    player.draw()
    slime_1.draw()
    slime_2.draw()
    slime_3.draw()
    life_hud_1.draw()
    life_hud_2.draw()
    life_hud_3.draw()

def draw_win():
    screen.fill((0, 0, 0))
    screen.draw.text("YOU WIN!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="white")
    screen.draw.text("Press R to Restart", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")

def draw_game_over():
    screen.fill((0, 0, 0))
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="white")
    screen.draw.text("Press R to Restart", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")

def win_condition():
    global game_state
    enemies = [slime_1, slime_2, slime_3]
    #print([(e.state, getattr(e,"killed", False)) for e in enemies])
    if all(getattr(e, "killed", False) for e in enemies) and player.actor.colliderect(VICTORY_ZONE):
        game_state = "win"
        print("You Win!")

def restart_game():
    global game_state

    player.restart()
    
    slime_1.restart(600, 400)
    slime_2.restart(600, 100)
    slime_3.restart(1000, 550)

    life_hud_1.restart()
    life_hud_2.restart()
    life_hud_3.restart()
    
    door.restart()

    if game_state == "win":
        game_state = "menu"
    if game_state == "game_over":
        game_state = "game"

def heart_hud():
    if player.lifes == 3:
        life_hud_3.update()
    elif player.lifes == 2:
        life_hud_3.draw_lost_heart()
        life_hud_2.update()
    elif player.lifes == 1:
        life_hud_2.draw_lost_heart()
        life_hud_1.update()
    elif player.lifes == 0:
        life_hud_1.draw_lost_heart()

def musics():
    global music_on, music_playing
    music.set_volume(0.3)
    if music_on:
        if not music_playing:
            music.play('music_test')
            music_playing = True
    else:
        if music_playing:
            music.stop()
            music_playing = False