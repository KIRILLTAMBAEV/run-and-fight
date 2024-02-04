import pygame
import math
import pgzrun
from random import randint, choice
from game import Game

TITLE = 'CROSS ROAD'
WIDTH = 800
HEIGHT = 700
BULLET_SPEED = 10

current_level = 1

pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3')  
pygame.mixer.music.play(-1)  

gm = Game(Actor)
gm.init_lvl(1)

explosion = Actor('explosion/0', (-100, -100))
explosion.time = 0

state = 'main_menu'


bullets = []

def draw():
    if state == 'main_menu':
        screen.fill('black')
        screen.draw.text('CROSS ROAD', fontsize=80, center=(WIDTH//2, HEIGHT//4), color='white')
        screen.draw.text('Press S to toggle sound', fontsize=40, center=(WIDTH//2, HEIGHT//2), color='white')
        screen.draw.text('Press SPACE to start', fontsize=40, center=(WIDTH//2, HEIGHT//1.5), color='white')
        screen.draw.text('Press Q to quit', fontsize=40, center=(WIDTH//2, HEIGHT//1.2), color='white')
    else:
        gm.chicken.draw()
        gm.finish.draw()
        for road in gm.roads:
            road.draw()
        for grass in gm.grasses:
            grass.draw()
        for car in gm.cars:
            car.draw()
        for enemy in gm.enemies:
            enemy.draw()
            gm.chicken.draw()
            gm.finish.draw()
        for water in gm.water_sprites:
            water.draw()
        for log in gm.logs:
            log.draw()
        for bullet in bullets:
            bullet.draw()
            gm.chicken.draw()
            gm.finish.draw()
        if state == 'loose':
            screen.draw.text('GAME OVER', fontsize=80, center=(WIDTH//2, HEIGHT//2), color='red')
            explosion.draw()
        if state == 'win':
            screen.draw.text('YOU WIN!\nPRESS SPACE', fontsize=80, center=(WIDTH//2, HEIGHT//2), color='green')
        if state == 'pause':
            screen.draw.text('PAUSE', fontsize=80, center=(WIDTH//2, HEIGHT//2), color=(232, 228, 50))
        gm.chicken.draw()
        gm.finish.draw()
            
def on_key_up(key):
    global state
    if state == 'pause' and key == keys.SPACE:
        state = 'game'

def on_key_down(key):
    global state
    if state == 'main_menu':
        if key == keys.SPACE:
            state = 'game'
        elif key == keys.S:
            pygame.mixer.music.stop()  
        elif key == keys.Q:
            pgzrun.quit()
    elif key == keys.SPACE:
        state = 'pause'
    else:
        gm.chicken_move_x(key, keys, WIDTH)
        if state == 'pause':
            if key == keys.SPACE:
                state = 'game'
                return

        if state == 'win':
            if key == keys.SPACE:
                gm.init_lvl(2)
                state = 'game'


def on_mouse_down(pos, button):
    global state
    if state == 'game' and button == mouse.LEFT:
        angle = angle_between_points(gm.chicken.pos, pos)
        shoot_bullet(angle)

def angle_between_points(point1, point2):
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])


def shoot_bullet(angle):
    bullet = Actor("bulletblue", anchor=("center", "center"))
    bullet.x = gm.chicken.x
    bullet.y = gm.chicken.y
    bullet.angle = math.degrees(angle)
    bullets.append(bullet)

def move_bullets():
    global bullet_fired
    for bullet in bullets:
        bullet.x += BULLET_SPEED * math.cos(math.radians(bullet.angle))
        bullet.y += BULLET_SPEED * math.sin(math.radians(bullet.angle))
        
        if bullet.y < 0 or bullet.y > HEIGHT or bullet.x < 0 or bullet.x > WIDTH:
            bullets.remove(bullet)
            
def check_bullet_collision():
    global bullets, state

    for bullet in bullets:
        for enemy in gm.enemies:
            if bullet.colliderect(enemy):
                gm.enemies.remove(enemy)
                bullets.remove(bullet)
                break 

chicken_frame = 0

def update_chicken_animation():
    global chicken_frame
    chicken_frame += 1
    if chicken_frame > 7:
        chicken_frame = 0

def update(dt):
    global tracks, state, current_level, chicken_frame
    gm.finish.time += dt
    if gm.finish.time > 0.1:
        gm.finish.time = 0
        number = int(gm.finish.image.split('/')[-1])
        gm.finish.image = f'flag/{(number + 1) % 10}'
    
    if state == 'game':
        gm.update_enemies()
        gm.chicken_move_y(keyboard, HEIGHT)
        move_bullets()
        check_bullet_collision()
        
        for car in gm.cars:
            car.y -= car.speed
            if car.bottom < 0:
                gm.tracks.append(car.track)
                car.track = choice(gm.tracks)
                gm.tracks.remove(car.track)
                car.x = 43 + car.track
                car.top = 700
                car.image = choice(gm.cars_names)
        
        if gm.chicken.colliderect(gm.finish):
            state = 'win'
            if current_level == 1:
                pygame.mixer.music.load('sounds/win.mp3')
            elif current_level == 2:
                pygame.mixer.music.load('sounds/win.mp3')  
            pygame.mixer.music.play()
            
        if gm.chicken.collidelist(gm.cars) != -1 or gm.chicken.collidelist(gm.enemies) != -1:
            state = 'loose'  
            animate(gm.chicken, y=gm.chicken.y-60, tween='bounce_start_end', duration=0.5)
            pygame.mixer.music.load('sounds/car-crash-sound-effect.mp3')
            pygame.mixer.music.play()      
        screen.clear()
        draw()
            
    if state == 'loose':
        number = int(gm.finish.image.split('/')[-1])
        explosion.time += dt 
        if explosion.time > 0.2:
            explosion.time = 0
            index = int(explosion.image.split('/')[-1])
            if index == 0:
                explosion.pos = gm.chicken.pos
                explosion.image = f'explosion/{index + 1}'
            elif index == 7:
                explosion.pos = (-100, -100)
            else:
                explosion.image = f'explosion/{index + 1}'

    
    if state == 'win' and current_level == 1:
        current_level = 2
        gm.init_lvl(2)  
        pygame.mixer.music.load('background_music.mp3')  
        pygame.mixer.music.play(-1)  

pgzrun.go()

