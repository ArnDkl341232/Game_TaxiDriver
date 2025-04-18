from ast import Index

import pygame as pg
import random


FPS = 60
width, height = 700,450
x_direction = 0
y_direction = 0
pl_speed = 2
player_view = 'front'
BLACK = (0,0,0)

images_dict = {
    'bg' : pg.image.load('img/Background1.png'),
    'rear' : pg.image.load('img/cab_rear_old.png'),
    'left' : pg.image.load('img/cab_left_old.png'),
    'right' : pg.image.load('img/cab_right_old.png'),
    'front' : pg.image.load('img/cab_front_old.png'),
    'hole' : pg.image.load('img/hole.png'),
    'hotel' : pg.transform.scale(pg.image.load('img/hotel_old.png'), (80, 80)),
    'ps': pg.image.load('img/passenger.png'),
    'parking': pg.transform.scale(pg.image.load('img/parking.png'),(80,45)),
}

#taxi
player_view = 'rear'
player_rect = images_dict[player_view].get_rect()
player_rect.y = 300
player_rect.x = 300

#hotel
hotel_img = images_dict['hotel']
hotel_rect = hotel_img.get_rect()
hotel_positions = [
    (60,30),
    (555,30),
    (60,250),
    (555,250)
]
hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)

#parking
parking_img = images_dict['parking']
parking_rect = parking_img.get_rect()
(parking_rect.x,
 parking_rect.y) = (hotel_rect.x, hotel_rect.y + hotel_rect.height)

#passenger
passenger_img = images_dict['ps']
passenger_rect = passenger_img.get_rect()
(passenger_rect.x,
 passenger_rect.y) = random.choice(hotel_positions)
passenger_rect.y += hotel_rect.height


def is_crash():
    for x in range(player_rect.x, player_rect.topright[0], 1):
        for y in range(player_rect.y, player_rect.bottomleft[1], 1):
            try:
                if screen.get_at((x,y)) == (220,215,177):
                    return True
            except IndexError:
                pass

    if hotel_rect.colliderect(player_rect):
        return True
    return False


def draw_message(text,color):
    font = pg.font.SysFont(None,40)
    message = font.render(text,True, color)
    screen.blit(message,(320,150))
    pg.display.flip()
    pg.time.delay(1000)


pg.init()

screen = pg.display.set_mode([width, height])

timer = pg.time.Clock()

run = True

while run:
    timer.tick(FPS)
    keys_kl = pg.key.get_pressed()


    #Obrobotka
    for event in pg.event.get():
        if event.type  == pg.QUIT or keys_kl[pg.K_ESCAPE]:
            run = False

    if keys_kl[pg.K_RIGHT]:
        x_direction = 1
        player_view = 'right'
    elif keys_kl[pg.K_LEFT]:
        x_direction = -1
        player_view = 'left'
    elif keys_kl[pg.K_UP]:
        y_direction = -1
        player_view = 'rear'
    elif keys_kl[pg.K_DOWN]:
        y_direction = 1
        player_view = 'front'

    if player_rect.x >= width - player_rect.width:
        player_rect.x = width - player_rect.height
    if player_rect.y >= height - player_rect.height:
        player_rect.y = height - player_rect.width
    if player_rect.x <= 0:
        player_rect.x = 0
    if player_rect.y <= 0:
        player_rect.y = 0




    #Obnovlayem
    player_rect.y += pl_speed * y_direction
    player_rect.x += pl_speed * x_direction
    x_direction = 0
    y_direction = 0

    if is_crash():
        print("IS CRASH")
        player_view = 'rear'
        player_rect.x = 300
        player_rect.y = 300
        (passenger_rect.x, passenger_rect.y) = random.choice(hotel_positions)
        passenger_rect.y += hotel_rect.height
        continue

    if parking_rect.contains(player_rect):
        draw_message("Win!", pg.Color('green'))
        player_view = 'rear'
        player_rect.x = 300
        player_rect.y = 300

        hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)
        parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height
        (passenger_rect.x, passenger_rect.y) = random.choice(hotel_positions)
        passenger_rect.y += hotel_rect.height
        continue

    if player_rect.colliderect(passenger_rect):
        passenger_rect.x, passenger_rect.y = player_rect.x, player_rect.y

    #Visual
    # screen.blit()
    screen.fill(BLACK)
    screen.blit(images_dict['bg'], (0,0))

    #prorisovka
    screen.blit(hotel_img, hotel_rect)
    screen.blit(parking_img, parking_rect)
    screen.blit(passenger_img, passenger_rect)
    screen.blit(images_dict[player_view], player_rect)

    pg.display.flip()


pg.quit()