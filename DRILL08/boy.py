from pico2d import load_image, get_time
from sdl2 import SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

from state_machine import *


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) #소년 객체의 state machine 생성
        self.state_machine.start(Idle) # 초기 상태가 Idle로 설정됨
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, a_down: AutoRun, a_up: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, time_out: Idle},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
                AutoRun : {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        # event : 입력  이벤트 key, mouse
        #  그러나 우리가 state machine 에게 전달해줄껀 튜플로 만들어진 이벤트 ( , )
        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)

# 객체 상태를 클래스로 정의함
class Idle:
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass
    @staticmethod
    def enter(boy,e):
        if left_up(e) or right_down(e) or boy.dir == -1:
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e) or boy.dir == 1:
            boy.action = 3
            boy.face_dir = 1

        boy.dir = 0     #정지 상태이다.
        boy.frame = 0
        #현재 시간을 저장
        boy.start_time = get_time()


class Sleep:
    @staticmethod
    def enter(boy,e):
        pass

    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(
                boy.frame*100, 300, 100, 100,
                3.141592/2, # 90도 회전
                '', # 좌우 상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )
        else:
            boy.image.clip_composite_draw(boy.frame*100, 200, 100, 100, -3.141592/2,
                                          '', boy.x+25, boy.y-25, 100, 100)

class Run:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0

    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.x += boy.dir*5
        boy.frame = (boy.frame+1)%8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame*100, boy.action*100, 100, 100, boy.x, boy.y
        )
        pass


class AutoRun:
    @staticmethod
    def enter(boy,e):
        if boy.face_dir ==1:
            boy.dir = 1
            boy.action = 1
        else:
            boy.dir = -1
            boy.action = 0

        boy.start_time = get_time()

    @staticmethod
    def exit(boy,e):
        if boy.action ==0:
            boy.action = 3
        else :
            boy.action = 4
        pass
    @staticmethod
    def do(boy):
        boy.x += boy.dir * 10
        boy.frame = (boy.frame + 1) % 8
        if boy.x < 0 :
            boy.dir = 1
            boy.action =1
        elif boy.x > 800:
            boy.dir = -1
            boy.action = 0

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
            pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y+30, 200, 200
        )
        pass