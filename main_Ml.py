from collections import defaultdict
import numpy as np
import pygame as pg
import random


def start_positions():
    global player_view
    player_view = 'rear'
    player_rect.x = 300
    player_rect.y = 300
    hotel_rect.x, hotel_rect.y = random.choice(hotel_positions)
    parking_rect.x, parking_rect.y = hotel_rect.x, hotel_rect.y + hotel_rect.height
    passenger_rect.x, passenger_rect.y = random.choice(hotel_positions)
    passenger_rect.y += hotel_rect.height

def draw():
    if learned:
        pg.time.delay(1)

    screen.fill(BLACK)
    screen.blit(images_dict['bg'], (0, 0))

    for img, rect in objects:
        screen.blit(img, rect)
    pg.display.flip()

def apply_action(action):
    if action is None:
        return
    global player_view
    x_direction = 0
    y_direction = 0
    if action == 0:
        x_direction = 1
        player_view = 'right'
    elif action == 1:
        x_direction = -1
        player_view = 'left'
    elif action == 2:
        y_direction = -1
        player_view = 'rear'
    elif action == 3:
        y_direction = 1
        player_view = 'front'

    new_x = player_rect.x + player_rect.width * x_direction
    new_y = player_rect.y + player_rect.height * y_direction



    if 0 < new_x < width - player_rect.width:
        player_rect.x = new_x
    if 0 < new_y < height - player_rect.height:
        player_rect.y = new_y


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

FPS = 60
width, height = 700,450
BLACK = (0,0,0)

images_dict = {
    'bg' : pg.image.load('img/Background.png'),
    'rear' : pg.image.load('img/cab_rear.png'),
    'left' : pg.image.load('img/cab_left.png'),
    'right' : pg.image.load('img/cab_right.png'),
    'front' : pg.image.load('img/cab_front.png'),
    'hole' : pg.image.load('img/hole.png'),
    'hotel' : pg.transform.scale(pg.image.load('img/hotel.png'), (80, 80)),
    'ps': pg.image.load('img/passenger.png'),
    'parking': pg.transform.scale(pg.image.load('img/parking.png'),(80,45)),
}

#taxi
player_view = 'rear'
player_rect = images_dict[player_view].get_rect()



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

#passenger
passenger_img = images_dict['ps']
passenger_rect = passenger_img.get_rect()



#objects for prorisovka
objects = [
        (hotel_img, hotel_rect),
        (parking_img, parking_rect),
        (passenger_img, passenger_rect),
        (images_dict[player_view], player_rect)
    ]


###########################################################################################################################
#Q-learn
actions = [0, 1, 2, 3] #0- right ,1- left, 2- up, 3- down

Q_tab = defaultdict(lambda:[0, 0, 0, 0])

learning_rate = 0.9
discount_factor = 0.9
# epsilon = 0.1
epsilon = -1

def choose_action(state):
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        return np.argmax(Q_tab[state])

def update_q(state, action, reward, next_state):
    best_n = max(Q_tab[next_state])
    Q_tab[state][action] += learning_rate * (reward + discount_factor * best_n - Q_tab[state][action])

def make_step():
    current_state = (player_rect.x , player_rect.y)
    action = choose_action(current_state)
    apply_action(action)
    draw()
    reward = -1
    episode_end = False
    success = False

    if is_crash():
        print("IS CRASH ----100")
        reward = -100
        episode_end = True

    if parking_rect.contains(player_rect):
        print("contein 100")
        reward = 100
        episode_end = True
        success = True

    next_state = (player_rect.x, player_rect.y)

    update_q(current_state, action, reward, next_state)

    return (episode_end, success)

#main learning circle
num_episodes = 200
max_steps = 50

pg.init()
screen = pg.display.set_mode([width, height])
timer = pg.time.Clock()
start_positions()
learned = False
draw()

for episode in range(num_episodes):
    player_rect.y = 300
    player_rect.x = 300
    for step in range(max_steps):
        (episode_end, succes) = make_step()
        if episode_end:
            print("Win?", succes)
            break

learned = True
print(Q_tab)

draw_message("Таксі навчилось!", pg.Color("blue"))

###########################################################################################################################
FPS = 10
run = True
while run:
    timer.tick(FPS)
    keys_kl = pg.key.get_pressed()

    current_state = (player_rect.x, player_rect.y)
    action = choose_action(current_state)
    apply_action(action)

    #Obrobotka
    for event in pg.event.get():
        if event.type  == pg.QUIT or keys_kl[pg.K_ESCAPE]:
            run = False

    if is_crash():
        print("IS CRASH")
        #run = False
        #start_positions()

    if parking_rect.contains(player_rect):
        draw_message("Win!", pg.Color('green'))

    if player_rect.colliderect(passenger_rect):
        passenger_rect.x,passenger_rect.y = player_rect.x, player_rect.y


    draw()

pg.quit()