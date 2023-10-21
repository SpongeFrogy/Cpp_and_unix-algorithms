from __future__ import annotations
from scipy.spatial import distance
import random
import matplotlib.pyplot as plt
import pygame
import numpy as np


class Road:
    def __init__(self, c0: CrossRoad, c1: CrossRoad, name: str, v, s0={}, s1={}):
        self.c0 = c0
        self.c1 = c1
        self.signal0 = Signal(c0, self, **s0)
        self.signal1 = Signal(c1, self, **s1)
        c0.add_road(self, self.signal0)
        c1.add_road(self, self.signal1)

        self.name = name

        self.length = distance.euclidean(c0.pos, c1.pos)
        self.v = self.length / 10
        self.sin = (c1.pos[0] - c0.pos[0]) / self.length
        self.cos = (c1.pos[1] - c0.pos[1]) / self.length

        self.cars_true: list[Car] = []
        self.cars_false: list[Car] = []

    def add_car(self, car: Car):
        if car.direction:
            self.cars_true.append(car)
        else:
            self.cars_false.append(car)

    def draw(self, screen: pygame.display):
        pygame.draw.line(screen, "#FEDA97", self.c0.pos, self.c1.pos, 2)


class CrossRoad:
    def __init__(self, pos: tuple[int, int]):
        self.roads: dict[Road, Signal] = {}
        self.pos = pos

    def add_road(self, road: Road, signal: Signal) -> Road:
        self.roads[road] = signal
        return road

    def update_signal(self, dt):
        for sig in self.roads.values():
            sig.update(dt)

    def draw(self, screen):
        pygame.draw.circle(screen, (123, 123, 123), self.pos, 5)
        for road in self.roads.keys():
            # draw Signals
            if self is road.c0:
                pygame.draw.circle(screen, self.roads[road]._color, (
                    self.pos[0] + road.sin * 7, self.pos[1] + road.cos * 7), 4)
            else:
                pygame.draw.circle(screen, self.roads[road]._color, (
                    self.pos[0] - road.sin * 7, self.pos[1] - road.cos * 7), 4)


class Signal:
    def __init__(self, crossroad: CrossRoad, road: Road, timing: tuple[int, int], signal: bool, time: int):
        self.can_go = signal
        self.crossroad = crossroad
        self.road = road
        self.timing = timing
        self.time = time

    def update(self, dt: int) -> bool:
        self.time += dt
        circle_time = self.time % sum(self.timing)
        if circle_time < self.timing[0]:
            self.can_go = True
        else:
            self.can_go = False
        return self.can_go

    @property
    def _color(self):
        if self.can_go:
            return (0, 255, 0)
        else:
            return (255, 0, 0)

    def draw(self, screen):
        x = self.crossroad.pos[0] + self.road.sin * 5
        y = self.crossroad.pos[1] + self.road.cos * 5
        pygame.draw.circle(screen, self._color, (x, y), 3)


class Car:
    X0 = 5

    def __init__(self, road: Road, v: int, pos: float | int, direction: bool = True):
        self.road = road
        self.v = v
        self.possibility = 1
        self.pos = pos
        self.going = True
        self.direction = direction

        self.s = 0

        self.road.add_car(self)

    def _go(self, dt: float):
        self.pos += self.v*dt
        self.s += abs(self.v)*dt

    def change_road(self):
        c = self.road.c1 if self.direction else self.road.c0
        if self in self.road.cars_true:
            self.road.cars_true.remove(self)
        if self in self.road.cars_false:
            self.road.cars_false.remove(self)

        out_road_index = list(c.roads.keys()).index(self.road)
        r = []
        w = []
        for i, road in zip(range(len(c.roads)), c.roads.keys()):
            if i != out_road_index:
                if c is road.c0:
                    if True:  # not
                        r.append(i)
                        w.append(1/road.length)
                if c is road.c1:
                    if True:  # not road.signal1
                        r.append(i)
                        w.append(1/road.length)

        i = random.choices(r, weights=w)[0]

        self.road = list(c.roads.keys())[i]

        self.possibility = self.road.length * sum(w)

        if c is self.road.c0:
            self.pos = 0
            self.v = abs(self.road.v)
            self.direction = True
            self.road.cars_true.append(self)
        else:
            self.pos = self.road.length
            self.v = -abs(self.road.v)
            self.direction = False
            self.road.cars_false.append(self)

    def update(self, dt):
        dir_road = self.road.cars_true if self.direction else self.road.cars_false
        if self is not dir_road[0]:
            index = dir_road.index(self)
            if not dir_road[index - 1].going and (abs(self.pos - dir_road[index - 1].pos) - self.X0) <= 0:
                self.going = False
            else:
                self.going = True

        if self.direction:
            if (self.road.length - self.pos) < 15:
                if not self.road.c1.roads[self.road].can_go:
                    self.going = False
                else:
                    self.going = True
            if (self.road.length - self.pos) < 0.1:
                if self.going:
                    self.change_road()
        else:
            if self.pos < 10:
                if not self.road.c0.roads[self.road].can_go:
                    self.going = False
                else:
                    self.going = True
            if self.pos < 0.1:
                if self.going:
                    self.change_road()

        if self.going:
            self._go(dt)

    def draw(self, screen):
        x = self.road.c0.pos[0] + self.pos * self.road.sin
        y = self.road.c0.pos[1] + self.pos * self.road.cos

        pygame.draw.circle(screen, (0, 0, 255), (x, y), 2)


class InitCarGenerator:
    def __init__(self, road: Road, v=5, n_cars_true: int = 10, n_cars_false: int | None = None):
        if not n_cars_false:
            n_cars_false = n_cars_true
        self.n_cars_true = n_cars_true
        self.n_cars_false = n_cars_false

        self.road = road
        self.v = abs(v)
        self.direction = v >= 0

    def generate(self):
        self.road.cars_true = [Car(self.road, self.v, pos=self.road.length /
                                   self.n_cars_true*i, direction=True) for i in range(self.n_cars_true)]
        self.road.cars_false = [Car(self.road, -self.v, pos=self.road.length /
                                    self.n_cars_false*i, direction=False) for i in range(self.n_cars_false)]

        return self.n_cars_true, self.n_cars_false


class City:
    def __init__(self) -> None:

        self.roads: list[Road] = []
        self.crossroads: list[CrossRoad] = []
        self.init_gens: list[InitCarGenerator] = []
        self.road_titles = []
        self.road_v = []
        self.time = 0

        self.sum_length = 0.
        self.sum_cars = 0
        self.n_roads = 0

    def add_road(self, road: Road):
        self.roads.append(road)
        self.sum_length += 2*road.length
        self.n_roads += 1

    def add_roads(self, list: list[Road]):
        for road in list:
            self.add_road(road)

    def add_c_road(self, crossroad: CrossRoad):
        self.crossroads.append(crossroad)

    def add_c_roads(self, list: list[CrossRoad]):
        for c in list:
            self.add_c_road(c)

    def add_init_car_gen(self, gen: InitCarGenerator):
        self.init_gens.append(gen)

    def add_init_car_gens(self, list: list[InitCarGenerator]):
        for gen in list:
            self.init_gens.append(gen)

    def generate(self):
        for gen in self.init_gens:
            self.sum_cars += sum(gen.generate())

    def reset(self):
        for r in self.roads:
            r.cars_true = []
            r.cars_false = []
        self.time = 0

    def update_load_road(self):
        load_per_road = sorted([*[(r_t.name+" T", len(r_t.cars_true)) for r_t in self.roads],
                                *[(r_f.name+" F", len(r_f.cars_false)) for r_f in self.roads]], key=lambda x: x[1], reverse=True)
        return load_per_road

    def update_mean_v(self):
        score = 0.
        max_v = 0
        for r in self.roads:
            max_v = max(max_v, r.v)
            for car in r.cars_true:
                score += car.s / self.time
            for car in r.cars_false:
                score += car.s / self.time
        score /= self.sum_cars * max_v
        return score

    def update_entropy(self):
        score = 0.
        for r in self.roads:
            for c in r.cars_true:
                score += c.possibility * np.log(c.possibility)
            for c in r.cars_false:
                score += c.possibility * np.log(c.possibility)
        return score

    def loop(self, dt=0.1, t_max=1000):
        """
        return:
            time: list[float]
            mean_v: list[float]
            entropy: list[float]
        """
        running = True
        self.time = 0
        self.generate()
        running = True

        score_list = []
        entropy_list = []

        def condition(x): return self.time <= t_max
        while running:
            running = condition(running)
            for r in self.roads:
                for car in r.cars_true:
                    car.update(dt)
                for car in r.cars_false:
                    car.update(dt)
            for c in self.crossroads:
                c.update_signal(dt)

            self.time += dt
            score_list.append(self.update_mean_v())
            entropy_list.append(self.update_entropy())

            running = condition(running)
        self.reset()
        return [i*dt for i in range(len(score_list))], score_list, entropy_list

    def loop_draw(self, score_font_params=(None, 24), road_font_params=(None, 13), dt=0.1, condition=lambda x: True):
        self.time = 0
        self.generate()
        score_list = []
        entropy_list = []
        pygame.init()

        FPS = 120

        clock = pygame.time.Clock()

        self.score_font = pygame.font.SysFont(*score_font_params)

        self.road_font = pygame.font.SysFont(*road_font_params)
        for r in self.roads:
            self.road_titles.append(
                self.road_font.render(r.name, False, (0, 0, 0)))

        for r in self.roads:
            self.road_v.append(
                self.road_font.render(f"{r.v:.2f}", False, (0, 0, 0)))

        screen = pygame.display.set_mode([800, 800], pygame.RESIZABLE)
        img = pygame.image.load("sem7/lab3/back.png")

        running = True
        while running:
            # Did the user click the window close button?
            running = condition(running)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.blit(img, (0, 0))

            for r in self.roads:
                r.draw(screen)
                for car in r.cars_true:
                    car.update(dt)
                    car.draw(screen)
                for car in r.cars_false:
                    car.update(dt)
                    car.draw(screen)

            for c in self.crossroads:
                c.update_signal(dt)
                c.draw(screen)

            self.time += dt

            for t, r in zip(self.road_titles, self.roads):
                screen.blit(t, (r.c0.pos[0] + (r.c1.pos[0] - r.c0.pos[0]) // 2 - self.road_font.size(
                    r.name)[0] // 2, r.c0.pos[1] + (r.c1.pos[1] - r.c0.pos[1]) // 2))

            # for t, r in zip(self.road_v, self.roads):
            #     screen.blit(t, (r.c0.pos[0] + (r.c1.pos[0] - r.c0.pos[0]) // 2, r.c0.pos[1] + (r.c1.pos[1] - r.c0.pos[1]) // 2))

            loaded = self.update_load_road()
            mean_v = self.update_mean_v()
            entropy = self.update_entropy()

            text_time = self.score_font.render(
                f'time   = {self.time:.1f} inner s', False, (0, 0, 0))
            screen.blit(text_time, (0, 0))

            text_score = self.score_font.render(
                f'mean v = {mean_v:.5}', False, (0, 0, 0))
            screen.blit(text_score, (0, score_font_params[1]))

            text_score = self.score_font.render(
                f'entropy = {entropy:.5}', False, (0, 0, 0))
            screen.blit(text_score, (0, score_font_params[1]*2))

            for i in range(5):
                text = self.score_font.render(
                    f'{i+1}. {loaded[i][0]}: {loaded[i][1]}', False, (0, 0, 0))
                screen.blit(text, (0, 800 - (4 - i+1)*30))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        self.reset()

    def loop_plot(self, dt=0.1, condition=lambda x: True):
        running = True
        self.time = 0
        self.generate()
        running = True
        score_list = []
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        fig.show()
        while running:
            # Did the user click the window close button?
            running = condition(running)

            for r in self.roads:
                for car in r.cars_true:
                    car.update(dt)
                for car in r.cars_false:
                    car.update(dt)
            for c in self.crossroads:
                c.update_signal(dt)

            self.time += dt
            score = self.update_mean_v()
            score_list.append(score)
            time = np.linspace(0*dt, len(score_list)*dt, (len(score_list)-0))
            ax1.clear()

            ax1.plot(time, score_list, color='r')
            ax1.set_xlabel("inner time")
            ax1.set_ylabel("mean v")
            ax1.set_title(f"time = {self.time:.1f}, mean v = {score:.3f}")
            fig.canvas.draw()
            fig.canvas.flush_events()

            running = condition(running)
        self.reset()
