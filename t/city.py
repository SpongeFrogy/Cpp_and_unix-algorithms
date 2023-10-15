from __future__ import annotations
from scipy.spatial import distance
import random
import matplotlib.pyplot as plt
import time
import pygame
import numpy as np


class Road:
    def __init__(self, c0: CrossRoad, c1: CrossRoad, name: str, font, s0={}, s1={}):
        self.c0 = c0
        self.c1 = c1
        c1.add_road(self, Signal(c1, self, **s0))
        c0.add_road(self, Signal(c1, self, **s1))
        self.text = name
        self.font = font
        self.name = font.render(name, True, (0, 0, 0))

        self.length = distance.euclidean(c0.pos, c1.pos)
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
        screen.blit(self.name, (self.c0.pos[0] + (self.c1.pos[0] - self.c0.pos[0]) // 2 - self.font.size(
            self.text)[0] // 2, self.c0.pos[1] + (self.c1.pos[1] - self.c0.pos[1]) // 2))


class CrossRoad:
    def __init__(self, pos: tuple[int, int]):
        self.roads: dict[Road, Signal] = {}
        self.pos = pos

    def add_road(self, road: Road, signal: Signal) -> Road:
        self.roads[road] = signal
        return road

    def update_signal(self, t, dt):
        for sig in self.roads.values():
            sig.update(dt)

    def change_road(self, car: Car):
        # print(car in car.road.cars_true)
        if car in car.road.cars_true:
            car.road.cars_true.remove(car)
        if car in car.road.cars_false:
            car.road.cars_false.remove(car)

        r = [i for i in range(len(self.roads)) if i != list(
            self.roads.keys()).index(car.road)]
        i = random.choice(r)
        car.road = list(self.roads.keys())[i]
        if self is car.road.c0:
            car.pos = 0
            car.v = abs(car.v)
            car._v = car.v
            car.direction = True
            car.road.cars_true.append(car)
        else:
            car.pos = car.road.length
            car.v = -abs(car.v)
            car._v = car.v
            car.direction = False
            car.road.cars_false.append(car)

    def draw(self, screen):
        pygame.draw.circle(screen, (123, 123, 123), self.pos, 5)
        for road in self.roads.keys():
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
        cycle_time = self.time % sum(self.timing)
        if cycle_time < self.timing[0]:
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


X0 = 5


class Car:
    def __init__(self, road: Road, v: int, pos: float | int, direction: bool = True):
        self.road = road
        self.v = v
        self._v = v

        self.pos = pos
        self.going = True
        self.direction = direction

        # self.a = - 1 / (self.road.length -
        #                 self.pos) if self.direction else 1 / self.pos

        self.road.add_car(self)

    def _go(self, dt: float):
        # if self is not dir_road[0]:
        #     index = dir_road.index(self)
        #     delta_x = (dir_road[index - 1].pos - self.pos)
        #     delta_v = dir_road[index - 1].v - self.v
        #     self.v += 0.01 * (1 - X0/delta_x)
        #     if abs(delta_x - X0) < 0.01:
        #         self.v = dir_road[index - 1].v
        #     self.v = abs(max(self.v, self._v)
        #                  ) if self.direction else -abs(min(self.v, self._v))
        self.pos += self.v*dt  # + self.a * dt**2 / 2
        # self.v += self.a * dt

    def stop(self):
        self.going = False

    def unstop(self):
        self.going = True

    def update(self, dt):
        # print(self.road.text, self.pos, self.road.length, self.v, self.direction)
        dir_road = self.road.cars_true if self.direction else self.road.cars_false
        if self is not dir_road[0]:
            index = dir_road.index(self)
            if not dir_road[index - 1].going and (abs(self.pos - dir_road[index - 1].pos) - X0) <= 0:
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
                    self.road.c1.change_road(self)
        else:
            if self.pos < 10:
                if not self.road.c0.roads[self.road].can_go:
                    self.going = False
                else:
                    self.going = True
            if self.pos < 0.1:
                if self.going:
                    self.road.c0.change_road(self)

        if self.going:
            self._go(dt)

    def draw(self, screen):
        x = self.road.c0.pos[0] + self.pos * self.road.sin
        y = self.road.c0.pos[1] + self.pos * self.road.cos

        pygame.draw.circle(screen, (0, 0, 255), (x, y), 2)


class CarGenerator:
    def __init__(self, road: Road):
        self.road = road
        # default config of generated car
        self.config = {
            "v": 5,
            "pos": 30,
            "direction": True
        }

    def _generate_one(self, config):
        car = Car(self.road, **config)
        # self.road.add_car(car)
        return car

    def generate(self, city: City, timeout=2):
        if city.time % timeout < 0.1:
            self._generate_one(self.config)

    def update(self, city):
        self.generate(city)


class InitCarGenerator:
    def __init__(self,road: Road, v=5, n_cars_true: int = 10, n_cars_false: int | None = None):
        if not n_cars_false:
            n_cars_false = n_cars_true
        self.n_cars_true = n_cars_true
        self.n_cars_false = n_cars_false
        
        self.road = road
        self.v = abs(v)
        self.direction = v >= 0

    # def _generate_one(self, v=None, pos=None):
    #     if not v:
    #         v = self.v
    #     if not pos:
    #         pos = 0
    #     car = Car(self.road, v=v, pos=pos, direction=v >= 0)
    #     # self.road.add_car(car)
    #     return car

    def generate(self):
        self.road.cars_true = [Car(self.road, self.v, pos=self.road.length/self.n_cars_true*i, direction=True) for i in range(self.n_cars_true)]
        self.road.cars_false = [Car(self.road, -self.v, pos=self.road.length/self.n_cars_false*i, direction=False) for i in range(self.n_cars_false)]


class City:
    loadedRoads = {}

    def __init__(self, font, dt=0.1) -> None:
        self.font = font

        self.roads: list[Road] = []
        self.crossroads: list[CrossRoad] = []
        # self.cars: list[Car] = []
        # self.generators: list[CarGenerator] = []
        self.init_gens : list[InitCarGenerator] = []
        self.time = 0
        self.dt = dt

    def add_road(self, road: Road):
        self.roads.append(road)

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

    # def add_car(self, car: Car):
    #     self.cars.append(car)

    # def add_cars(self, list: list[Car]):
    #     for car in list:
    #         self.add_car(car)

    def add_car_generator(self, generator: CarGenerator):
        self.generators.append(generator)

    # def update(self):
    #     for c_road in self.crossroads:
    #         c_road.update_signal(self.time, self.dt)
    #     for car in self.cars:
    #         car.update(self.dt)
    #     for gen in self.generators:
    #         gen.update(self)

    # def draw(self, screen):
    #     for road in self.roads:
    #         road.draw(screen)
    #     for c_road in self.crossroads:
    #         c_road.draw(screen)
    #     for car in self.cars:
    #         car.draw(screen)

    def update_score(self):
        load_per_road = sorted([*[(r_t.text+"T", len(r_t.cars_true)) for r_t in self.roads],
                                *[(r_f.text+"F", len(r_f.cars_false)) for r_f in self.roads]], key=lambda x: x[1], reverse=True)
        score = 0.
        for r in self.roads:
            score += len(r.cars_true)/r.length
            score += len(r.cars_false)/r.length
        return load_per_road, score

    def loop_and_draw(self, condition=lambda x: True):

        for gen in self.init_gens:
            gen.generate()


        screen = pygame.display.set_mode([800, 800])
        img = pygame.image.load("t/back.png")
        running = True
        score_list = []
        std = []
        mean = []
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        fig.show()
        while running:
            # Did the user click the window close button?
            running = condition(running)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Fill the background with white
            # screen.fill("#FCFCF7")
            screen.blit(img, (0, 0))
            # if self.time < 4000:
            #     for gen in self.generators:
            #         gen.update(self)
            for r in self.roads:
                r.draw(screen)
                for car in r.cars_true:
                    car.update(self.dt)
                    car.draw(screen)
                for car in r.cars_false:
                    car.update(self.dt)
                    car.draw(screen)
            for c in self.crossroads:
                c.update_signal(self.time, self.dt)
                c.draw(screen)
            # for car in self.cars:
            #     car.update(self.dt)
            #     car.draw(screen)
            # Flip the display
            loaded, score = self.update_score()
            text_score = self.font.render(
                f'score={score:.5}', False, (0, 0, 0))
            screen.blit(text_score, (0, 0))
            for i in range(5):
                text = self.font.render(
                    f'{i+1}. {loaded[i][0]}: {loaded[i][1]}', False, (0, 0, 0))
                screen.blit(text, (0, 800 - (4 - i+1)*30))
            score_list.append(score)
            if len(score_list) > 100:
                ax.clear()
                std.append(np.std(score_list[-99:]))
                mean.append(np.mean(score_list[-99:]))
                ax.plot(range(100, len(score_list)), mean, color='g')
                ax.fill_between(range(100, len(score_list)), [
                                m+s for m, s in zip(mean, std)], [m-s for m, s in zip(mean, std)], alpha=0.2, color='g')
                fig.canvas.draw()
                fig.canvas.flush_events()
            time.sleep(0.00001)
            pygame.display.flip()
            self.time += self.dt
        # plt.show()

    def loop(self, condition=lambda x: True):
        running = True
        while running:
            for c in self.crossroads:
                c.update_signal(self.time, self.dt)
            # for car in self.cars:
            #     car.update(self.dt)
            self.time += self.dt
            running = condition(running)
