import pygame
import pymunk
import pymunk.pygame_util
import random

# 초기화 (초기화는 시뮬레이션이 시작되는 1회만 진행되고 안정적인 실행을 위해 필요함.)
pygame.init()

# 시뮬레이션 창 옵션 설정
size = (1000, 1000)
screen = pygame.display.set_mode(size)
title="물체 충돌"
pygame.display.set_caption(title)

#시뮬 내 필요한 설정
clock=pygame.time.Clock() #시계
black = (0, 0, 0)  # 백그라운드의 색을 검은색 설정
white = (255,255,255)
screen.fill(black)
#물체에 이미지파일을 덮을 땐 이미지를 불러와야 함. 객체 이름 = pygame.image.load("D또는 C:/!#@#$")

#파이게임 업데이트
pygame.display.flip()

screen = pygame.display.set_mode(size)  # pygame과 pymunk 화면 연동
pygame.display.set_caption("은하 충돌 시뮬레이션")  # 시뮬레이션 창 제목


# 공간 만들기
space = pymunk.Space()
space.gravity = (0, 0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# 은하 개체 설정
num_galaxies = 2       #은하의 개수 설정
galaxy_radius = 50            #은하는 원 모양으로 가정, 반지름 길이
galaxy_mass = 10000          #은하의 질량 (일단 kg으로 가정하려고 했는데 pygame이랑 pymunk에서 얼마나 큰지 몰라서 그냥 넣음)

# 은하 생성 함수
def create_galaxy(position, num_particles, radius, mass):
    galaxy = []
    num_particles=1 #파티클 개수가 너무 많으면 이상해져서 랜덤값 말고 1로 설정함. 은하는 작은 원 하나로
    for _ in range(num_particles):
        body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))  #물체의 관성모멘트 설정(moment_for_circle이 질량과 반지름을 넣어주면 물체의 성질을 계산해줌)
        x = random.uniform(-radius, radius) + position[0]  # x방향 위치 
        y = random.uniform(-radius, radius) + position[1]  # y방향 위치
        body.position = (x, y)
        shape = pymunk.Circle(body, radius)
        space.add(body, shape)
        galaxy.append(body)
    return galaxy


#은하들 생성
galaxies = []
for _ in range(num_galaxies):  #은하 개수만큼 랜덤하게 생성
    x = random.uniform(galaxy_radius, size[0] - galaxy_radius) #이건 x값 y값임. size[0]과 [1]은 각각 가로세로의 창 길이를 말함
    y = random.uniform(galaxy_radius, size[1] - galaxy_radius)
    galaxy = create_galaxy((x, y), 50, galaxy_radius, galaxy_mass)
    galaxies.append(galaxy)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 중력 상수
G = 1

    # 은하들 간의 중력 적용
for i in range(num_galaxies):
    for j in range(i + 1, num_galaxies):
        galaxy1 = galaxies[i][0]
        galaxy2 = galaxies[j][0]
        
        # 은하들 간의 거리 계산
        distance = pymunk.Vec2d(galaxy2.position.x, galaxy2.position.y) - pymunk.Vec2d(galaxy1.position.x, galaxy1.position.y)
        
        # 은하들 간의 거리와 방향에 비례하는 중력 벡터 계산
        gravity_vector = G * galaxies[i][0].mass * galaxies[j][0].mass / distance.length ** 2 * distance
        
        # 은하들에 중력 벡터를 적용
        galaxies[i][0].apply_force(gravity_vector)
        galaxies[j][0].apply_force(-gravity_vector)

    space.step(1/60)

    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(60)

