# ЛР #3: Алгоритм работы с графами (моделирование транспортной системы)

## Цель

Познакомить студента с инструментами, направленными на решение задач, использующих графовые модели.

## Задача

Моделирование сложных транспортных процессов города, выявление узких участков, а также
формирование предложений по оптимизации.

__Дано__: На изображении отображены перекрестки, которые рассматривать для решения задачи.
В качестве агентов (автомобилей) и маршрутов их перемещения использовать придуманные
данные, отраженные в отчете по лабораторной работе (предусмотреть часы пик утром и
вечером).

![img](/sem7/lab3/map.png)

## Задача 1: Необходимо определить TOP-10 самых загруженных участков

между перекрестками, а также время на «рассасывание» этого затора.
Отображать такие параметры, как:
количество агентов (автомобилей) на участке;
процент загруженности участка;
длительность высокой загруженности (более 90%).

### Решение

Кратко опишем модель:

Основные классы:

```python
class Road:
    def __init__(self, c0: CrossRoad, c1: CrossRoad, name: str, s0={}, s1={}):
        ...

    def add_car(self, car: Car):
        ...

    def draw(self, screen: pygame.display):
        ...
```

```python
class CrossRoad:
    def __init__(self, pos: tuple[int, int]):
        ...

    def add_road(self, road: Road, signal: Signal) -> Road:
        ...

    def update_signal(self, t, dt):
        ...

    def draw(self, screen):
        ...
```

```python
class Signal:
    def __init__(self, crossroad: CrossRoad, road: Road, timing: tuple[int, int], signal: bool, time: int):
        ...

    def update(self, dt: int) -> bool:
        ...

    @property
    def _color(self):
        ...

    def draw(self, screen):
        ...
```

```python
class Car:
    def __init__(self, road: Road, v: int, pos: float | int, direction: bool = True):
        ...

    def _go(self, dt: float):
        ...

    def change_road(self):
        ...

    def update(self, dt):
        ...

    def draw(self, screen):
        ...
```

```python
class InitCarGenerator:
    def __init__(self, road: Road, v=5, n_cars_true: int = 10, n_cars_false: int | None = None):
        ...

    def generate(self):
        ...
```

```python
class City:
    def __init__(self) -> None:
        ...

    def add_road(self, road: Road):
        ...

    def add_roads(self, list: list[Road]):
        ...

    def add_c_road(self, crossroad: CrossRoad):
        ...

    def add_c_roads(self, list: list[CrossRoad]):
        ...

    def add_init_car_gen(self, gen: InitCarGenerator):
        ...

    def add_init_car_gens(self, list: list[InitCarGenerator]):
        ...

    def generate(self):
        ...

    def reset(self):
        ...

    def update_mean_v(self):
        ...

    def loop(self, dt=0.1, t_max=1000):
        """
        return time, score : list[float], list[float]
        """
        ...

    def loop_draw(self, score_font_params=(None, 24), road_font_params=(None, 13), dt=0.1, condition=lambda x: True):
        ...

    def loop_plot(self, dt=0.1, condition=lambda x: True):
        ...
```
