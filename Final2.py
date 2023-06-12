import pygame
import random
import time
from datetime import datetime


class imageManager:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self, address):
        if address[-3:] == "png":
            self.image = pygame.image.load(address).convert_alpha()
        else:
            self.image = pygame.image.load(address)
        self.sx, self.sy = self.image.get_size()

    def change_size(self, sx, sy):
        self.image = pygame.transform.scale(self.image, (sx, sy))
        self.sx, self.sy = self.image.get_size()

    def show(self):
        screen.blit(self.image, (self.x, self.y))


def crash(a, b):
    if (a.x - b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else:
            return False
    else:
        return False


pygame.init()

size = [500, 750]
screen = pygame.display.set_mode(size)

title = "미사일 게임"

pygame.display.set_caption(title)

clock = pygame.time.Clock()

ss = imageManager()
ss.put_img("jeon3.png")
ss.change_size(80, 80)
ss.x = round(size[0] / 2) - ss.sx / 2
ss.y = size[1] - ss.sy - 150
ss.move = 10

black = (0, 0, 0)

left_go = False
right_go = False
space_go = False

GO = 0
score = 0
kill = 0
loss = 0

a_list = []
m_list = []

start_time = datetime.now()

SB = 0
while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1
    screen.fill(black)
    font = pygame.font.SysFont("arial", 30, True, True)
    text_kill = font.render("press the space bar", True, (255, 255, 255))
    screen.blit(text_kill, (90, round(size[1] / 2 - 50)))
    pygame.display.flip()

SB = 0
k = 0

while SB == 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 2

    if score >= 500:
        SB = 0
        GO = 1

while SB == 0:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            if event.key == pygame.K_RIGHT:
                right_go = True
            if event.key == pygame.K_SPACE:
                space_go = True
                k = 0

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            if event.key == pygame.K_RIGHT:
                right_go = False
            if event.key == pygame.K_SPACE:
                space_go = False

    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())

    if left_go == True:
        ss.x -= ss.move
        if ss.x <= 0:
            ss.x = 0

    elif right_go == True:
        ss.x += ss.move
        if ss.x >= size[0] - ss.sx:
            ss.x = size[0] - ss.sx

    if space_go == True and k % 6 == 0:
        mm = imageManager()
        mm.put_img("jeon4.png")
        mm.change_size(20, 40)
        mm.x = round(ss.x + ss.sx / 2 - mm.sx / 2)
        mm.y = ss.y - mm.sy - 10
        mm.move = 15
        m_list.append(mm)

    k += 1

    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move
        if m.y < -m.sy:
            d_list.append(i)

    for d in d_list:
        del m_list[d]

    if random.random() > 0.98:
        aa = imageManager()
        aa.put_img("jeon1.png")
        aa.change_size(50, 50)
        aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx / 2))
        aa.y = 10
        aa.move = 1
        a_list.append(aa)

    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y >= size[1]:
            d_list.append(i)
            loss += 1
            score -= 10

    dd_list = []
    for d in dd_list:
        del a_list[d]

    dm_list = []
    da_list = []

    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]
            if crash(m, a) == True:
                dm_list.append(i)
                da_list.append(j)

    dm_list = list(set(dm_list))
    da_list = list(set(da_list))

    for d in dm_list:
        del m_list[d]

    for a in da_list:
        del a_list[a]
        kill += 1
        score += 20

    for i in range(len(a_list)):
        a = a_list[i]
        if crash(a, ss) == True:
            SB = 1
            GO = 1

    screen.fill(black)
    ss.show()
    for m in m_list:
        m.show()
    for a in a_list:
        a.show()

    font = pygame.font.SysFont("arial", 10, True, True)
    text_kill = font.render(
        "kill : {} loss : {} score : {}".format(kill, loss, score), True,
        (255, 255, 0))
    screen.blit(text_kill, (10, 5))

    text_time = font.render("time : {}".format(delta_time), True,
                            (255, 255, 255))
    screen.blit(text_time, (size[0] - 100, 5))

    pygame.display.flip()

while GO == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GO = 0
    screen.fill(black)
    font = pygame.font.SysFont("arial", 50, True, True)
    if score >= 500:
        text = font.render("VICTORY!", True, (0, 255, 0))
    else:
        text = font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(text, (90, round(size[1] / 2 - 50)))
    pygame.display.flip()

pygame.quit()
