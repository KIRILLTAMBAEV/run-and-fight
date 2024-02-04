import json
from random import choice, randint



class Game:
    def __init__(self, Actor):
        self.actor = Actor
        self.enemy_spawn_interval = 1000  
        self.enemy_spawn_timer = 0
    def make_car(self):
        track = choice(self.tracks)
        car = self.actor(choice(self.cars_names), (43+track * track, randint(100, 700)))
        car.track = track
        self.tracks.remove(track)
        car.speed = randint(1, 10)
        return car

    def init_lvl(self, lvl):
        with open(f'lvls/lvl{lvl}.json', 'r') as f:
            data = json.load(f)
        self.roads = []
        for coord in data['roads']['coordinates']:
            self.roads.append(self.actor('road', topleft=coord))
        self.grasses = []
        for coord in data['grass']['coordinates']:
            self.grasses.append(self.actor('grass', topleft=coord))
        self.water_sprites = []
        for coord in data['water']['coordinates']:
            self.water_sprites.append(self.actor('water', topleft=coord))
        self.logs = []
        for coord in data['logs']['coordinates']:
            self.logs.append(self.actor(choice(['log1', 'log2']), topleft=coord))
        self.sound_enabled = True
        self.music_enabled = True
        self.finish = self.actor('flag/1', data['finish']['coordinates'])
        self.finish.time = 0
        self.chicken = self.actor('chicken', data['chicken']['coordinates'])
        self.tracks = data['roads']['tracks']
        self.cars_names = data['cars']
        self.enemies = []
        for enemy_data in data['enemies']['data']:
            enemy = self.actor(choice(['enemy']), (enemy_data['x'], enemy_data['y']))
            enemy = self.actor('enemy', (enemy_data['x'], enemy_data['y']))
            enemy.speed = enemy_data['speed']
            enemy.max_y = enemy_data['max_y']
            enemy.min_y = enemy_data['min_y']
            enemy.up = True
            self.enemies.append(enemy)
        self.cars = []
        for _ in range(len(self.tracks)):
            car = self.make_car()
            self.cars.append(car)
  
    def update_enemies(self):
        for enemy in self.enemies:
            if enemy.up:
                enemy.y -= enemy.speed
                if enemy.y < enemy.min_y:
                    enemy.up = False
            else:
                enemy.y += enemy.speed
                if enemy.y > enemy.max_y:
                    enemy.up = True
                    
    def chicken_move_x(self, key, keys, WIDTH):
        if key == keys.LEFT:
            if self.chicken.x > 43:
                self.chicken.x -= 80
            if self.chicken.collidelist(self.logs) != -1:
                return
            if self.chicken.collidelist(self.water_sprites) != -1:
                self.chicken.x -= 80
        if key == keys.RIGHT:
            if self.chicken.x < WIDTH - 43:
                self.chicken.x += 80
            if self.chicken.collidelist(self.logs) != -1:
                return
            if self.chicken.collidelist(self.water_sprites) != -1:
                self.chicken.x += 80
    def chicken_move_y(self, keyboard, HEIGHT):
        if keyboard.UP:
            if self.chicken.collidelist(self.logs) != -1:
                return
            if self.chicken.y > 40:
                self.chicken.y -= 5
        if keyboard.DOWN:
            if self.chicken.collidelist(self.logs) != -1:
                return
            if self.chicken.y < HEIGHT - 40:
                self.chicken.y += 5
            
    
