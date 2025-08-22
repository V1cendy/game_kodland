import csv

WIDTH = 1280
HEIGHT = 736
tile_size = 18

class Hero:
    def __init__(self, x, y):
        self.actor = Actor("herochar_idle_anim_1", (x, y))
        self.lifes = 3
        self.invincible = False
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
        # Verificar colisão com o inimigo
        self.enemy_collision()

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
    # Verificar colisão com o inimigo
    def enemy_collision(self):
        if self.actor.colliderect(slime.actor):
            self.state = "dead"
            
    
    def respawn(self):
        if self.lifes > 0:
            self.lifes -= 1
            self.actor.topleft = (40, 600)
            self.vx = 0
            self.vy = 0
            self.on_ground = True
            self.state = "idle"
            self.current_frame = 0
            self.frame_timer = 0
            self.actor.image = self.idle_frames[0] if self.direction == "right" else self.idle_frames_left[0]
            print(f"Lifes remaining: {self.lifes}")
        else:
            print("Game Over")
            global game_state
            game_state = "game_over"


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

        self.idle_frames = [f"slime_idle_anim_{i}" for i in range(1, 6)]
        self.idle_frames_left = [f"slime_idle_anim_left_{i}" for i in range(1, 6)]

    def update(self):
        self.vx = 0
        # Gravidade
        self.vy += 0.5
        if self.vy > 10:
            self.vy = 10


        # Aplicar movimento
        self.actor.x += self.vx
        self.actor.y += self.vy

        self.check_collision()
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

    def animate(self):
        if self.state == "idle":
            self.frame_timer += 1
            if self.frame_timer >= 5:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            if self.direction == "left":
                self.actor.image = self.idle_frames_left[self.current_frame]
            else:
                self.actor.image = self.idle_frames[self.current_frame]

    def draw(self):
        self.actor.draw()
        
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
        
# --- MENU ---
start_button = Rect((270, 150),(300, 100))
sound_button = Rect((270, 300),(300, 100))
exit_button = Rect((270, 450),(300, 100))
COLOR = (136, 170, 189)
game_state = "menu"

# --- HERO ---
player = Hero(40, 686)

# --- SLIME ---
slime = Enemy(550, 460)

# --- LIFE HUD --- 
life_hud_1 = lifes(50, 50) 
life_hud_2 = lifes(100, 50) 
life_hud_3 = lifes(150, 50) 

# --- MAPA ---
tile_images = {
    1: 'tile_0001',
    2: 'tile_0002',
    3: 'tile_0003',
    4: 'tile_0004',
    20: 'tile_0020',
    21: 'tile_0021',
    22: 'tile_0022',
    23: 'tile_0023',
    27: 'tile_0027',
    28: 'tile_0028',
    47: 'tile_0047',
    68: 'tile_0068',
    87: 'tile_0087',
    88: 'tile_0088',
    120: 'tile_0120',
    121: 'tile_0121',
    123: 'tile_0123',
    141: 'tile_0141',
    142: 'tile_0142',
    143: 'tile_0143',
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

load_map("mapa.csv")

# --- DRAW ---
def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_game()
    elif game_state == "game_over":
        draw_game_over()

def draw_menu():
    screen.fill((79, 150, 189 ))
    screen.draw.filled_circle((1280, 700),700,(57, 108, 136))
    screen.draw.filled_rect(start_button, COLOR)
    screen.draw.text("START", center=start_button.center, fontsize=40, color="white")
    screen.draw.filled_rect(sound_button, COLOR)
    screen.draw.text("SOUND", center=sound_button.center, fontsize=40, color="white")
    screen.draw.filled_rect(exit_button, COLOR)
    screen.draw.text("EXIT", center=exit_button.center, fontsize=40, color="white")

def draw_game():
    for tile in tiles:
        tile.draw()
    player.draw()
    slime.draw()
    life_hud_1.draw()
    life_hud_2.draw()
    life_hud_3.draw()

def draw_game_over():
    screen.fill((0, 0, 0))
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="white")
    screen.draw.text("Press R to Restart", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")
# --- INPUT ---
def on_mouse_down(pos):
    global game_state
    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "game"
            sounds.confirmation_002.play()
        elif sound_button.collidepoint(pos):
            print("SOUND")
            sounds.click_002.play()
        elif exit_button.collidepoint(pos):
            print("EXIT")
            sounds.click_002.play()

def update():
    global game_state
    if game_state == "game":
        player.update()
        slime.update()
        
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
            
    if game_state == "game_over":
        if keyboard.r:
            print("Restarting game...")
            # Resetar jogador
            player.lifes = 3
            player.actor.topleft = (40, 600)
            player.vx = 0
            player.vy = 0
            player.on_ground = True
            player.state = "idle"
            player.current_frame = 0
            player.frame_timer = 0
            player.actor.image = player.idle_frames[0]
            game_state = "game"
