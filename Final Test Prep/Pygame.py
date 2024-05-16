import pygame
import random
import time
from datetime import datetime

#이미지 관리 클래스 정의
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

#충돌 함수 정의
def crash(a, b):
    if (a.x - b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else:
            return False
    else:
        return False

# 게임 초기화
pygame.init()

# 게임창 옵션 설정
size = [400, 900]
screen = pygame.display.set_mode(size)

title = "미사일 게임"

pygame.display.set_caption(title)

# 게임 내 필요한 설정
clock = pygame.time.Clock() #FPS를 위한 변수

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

# 게임 시작 대기 화면
SB = 0
while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1
    screen.fill(black)
    font = pygame.font.SysFont("arial", 30, True, True)
    text_kill = font.render("스페이스키를 눌러주세요!", True, (255, 255, 255))
    screen.blit(text_kill, (90, round(size[1] / 2 - 50)))
    pygame.display.flip()

# 메인 이벤트
SB = 0
k = 0

while SB == 0:
    # FPS 설정
    clock.tick(60) # 1초에 60번 while문 반복

    # 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 게임 종료
            SB = 1
        if event.type == pygame.KEYDOWN: # 키가 눌렸을 때
            if event.key == pygame.K_LEFT: # 키가 왼쪽 키이면
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

    # 입력, 시간에 따른 변화
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
            
    # 미사일 생성하기
    if space_go == True and k % 6 == 0:
        mm = imageManager()
        mm.put_img("jeon4.png")
        mm.change_size(20, 40)
        mm.x = round(ss.x + ss.sx / 2 - mm.sx / 2)
        mm.y = ss.y - mm.sy - 10
        mm.move = 15
        m_list.append(mm)

    k += 1
    
    # 화면에서 나간 미사일 지우기
    d_list = []
    for i in range(len(m_list)):
        m = m_list[i]
        m.y -= m.move
        if m.y < -m.sy:
            d_list.append(i)

    for d in d_list:
        del m_list[d]

    # 외계인 등장
    if random.random() > 0.98:
        aa = imageManager()
        aa.put_img("jeon1.png")
        aa.change_size(50, 50)
        aa.x = random.randrange(0, size[0] - aa.sx - round(ss.sx / 2)) # 외계인의 크기만큼 빼준다
        aa.y = 10
        aa.move = 1
        a_list.append(aa)

    for i in range(len(a_list)):
        a = a_list[i]
        a.y += a.move
        if a.y >= size[1]:
            d_list.append(i)
            loss += 1 # 외계인이 지나가면 loss + 1
            score -= 10

    dd_list = []
    for d in dd_list:
        del a_list[d]

    # 외계인 vs 미사일 충돌하는 경우 제거
    dm_list = []
    da_list = []

    for i in range(len(m_list)):
        for j in range(len(a_list)):
            m = m_list[i]
            a = a_list[j]
            if crash(m, a) == True:
                dm_list.append(i)
                da_list.append(j)

    dm_list = list(set(dm_list)) # 중복 제거
    da_list = list(set(da_list)) # 중복 제거

    for d in dm_list:
        del m_list[d]

    for a in da_list:
        del a_list[a]
        kill += 1 # 외계인이 사라지면 kill + 1
        score += 20

    # 비행기 vs 외계인 충돌하면 죽음
    for i in range(len(a_list)):
        a = a_list[i]
        if crash(a, ss) == True:
            SB = 1
            GO = 1
            
    # 그리기 
    screen.fill(black)
    ss.show()
    for m in m_list:
        m.show()
    for a in a_list:
        a.show()

    # 텍스트 그리기
    font = pygame.font.SysFont("arial", 10, True, True)
    text_kill = font.render(
        "kill : {} loss : {} score : {}".format(kill, loss, score), True,
        (255, 255, 0))
    screen.blit(text_kill, (10, 5))

    text_time = font.render("time : {}".format(delta_time), True,
                            (255, 255, 255))
    screen.blit(text_time, (size[0] - 100, 5))

    # 업데이트
    pygame.display.flip()

# 게임 종료
while GO == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GO = 0
    screen.fill(black)
    font = pygame.font.SysFont("arial", 50, True, True)
    text = font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(text, (90, round(size[1] / 2 - 50)))
    pygame.display.flip()

pygame.quit()
