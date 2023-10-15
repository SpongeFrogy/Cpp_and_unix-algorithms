from __future__ import annotations
from city import *
import pygame

"""
TODO: 
- моделирование 
      // ошибка в счётчике количестве машин из-за генератора   

      ! машины добавляются где-то в cars_true cars_false одновременно, не решено до конца
      // странная ошибка в:
            line 156, in update
            index = dir_road.index(self)
            ValueError: <city.Car object at 0x00000249EDA1B010> is not in list
      
      // сделать функцию энтропии 
- оптимизация
      * сделать функцию оптимизации
            должна учитывать что на каждом перекрестке хотя бы один сигнал должен быть красным 
      * определиться с методом (генетический алгоритм или optuna)
            по сложности как? можно за неделю доделать?
      * оптимизировать
- (опционально)
      * разделить классы по файлам 
      * просмотреть весь код на лишние куски и неоптимальные if 
"""


pygame.init()

font = pygame.font.SysFont(None, 15)

screen = pygame.display.set_mode([800, 800])
img = pygame.image.load("t/back.png")


cs = [CrossRoad((130, 245)),   # 1
      CrossRoad((190, 396)),   # 2
      CrossRoad((492, 288)),   # 3
      CrossRoad((510, 170)),   # 4
      CrossRoad((390, 126)),   # 5
      CrossRoad((425,  34)),   # 6
      CrossRoad((345,  35)),   # 7
      CrossRoad((278,  38)),   # 8
      CrossRoad((314, 146)),   # 9
      CrossRoad((102, 178)),   # 10
      CrossRoad((488, 311)),   # 11
      CrossRoad((383, 344)),   # 12
      CrossRoad((367, 318)),   # 13
      CrossRoad((393, 384)),   # 14
      CrossRoad((483, 391)),   # 15
      CrossRoad((325, 395)),   # 16
      CrossRoad((310, 348)),   # 17
      CrossRoad((228, 380)),   # 18
      CrossRoad((293, 543)),   # 19
      CrossRoad((345, 522)),   # 20
      CrossRoad((402, 512)),   # 21
      CrossRoad((481, 505))]   # 22

s = {"timing": [5, 5],
     "signal": True,
     "time": 0}

rs = [Road(cs[0], cs[1], name="Троицкий", font=font, s0=s, s1=s),
      Road(cs[1], cs[17], name="Дворцовая", font=font, s0=s, s1=s),
      Road(cs[17], cs[16], name="Дворцовая", font=font, s0=s, s1=s),
      Road(cs[16], cs[12], name="Кутузова 1", font=font, s0=s, s1=s),
      Road(cs[12], cs[2], name="Кутузова 2", font=font, s0=s, s1=s),
      Road(cs[2], cs[3], name="Литейный 1", font=font, s0=s, s1=s),
      Road(cs[3], cs[4], name="Пироговская 1", font=font, s0=s, s1=s),
      Road(cs[4], cs[5], name="Б Сампсониевский", font=font, s0=s, s1=s),
      Road(cs[5], cs[6], name="Финляндский", font=font, s0=s, s1=s),
      Road(cs[4], cs[6], name="Пироговская 2", font=font, s0=s, s1=s),
      Road(cs[6], cs[7], name="Сампсониевский", font=font, s0=s, s1=s),
      Road(cs[7], cs[8], name="Петроградская 1", font=font, s0=s, s1=s),
      Road(cs[8], cs[0], name="Петроградская 2", font=font, s0=s, s1=s),
      Road(cs[0], cs[9], name="Каменноостровский", font=font, s0=s, s1=s),
      Road(cs[9], cs[7], name="Куйбышевская", font=font, s0=s, s1=s),
      Road(cs[17], cs[18], name="Лебяжьей канавки", font=font, s0=s, s1=s),
      Road(cs[18], cs[19], name="Реки Мойки", font=font, s0=s, s1=s),
      Road(cs[19], cs[15], name="Реки Фонтанки 1", font=font, s0=s, s1=s),
      Road(cs[15], cs[16], name="Реки Фонтанки 2", font=font, s0=s, s1=s),
      Road(cs[15], cs[13], name="Чайковского 1", font=font, s0=s, s1=s),
      Road(cs[13], cs[11], name="Гагаринская 1", font=font, s0=s, s1=s),
      Road(cs[11], cs[12], name="Гагаринская 2", font=font, s0=s, s1=s),
      Road(cs[11], cs[10], name="Шпалерная", font=font, s0=s, s1=s),
      Road(cs[10], cs[14], name="Литейный 3", font=font, s0=s, s1=s),
      Road(cs[14], cs[21], name="Литейный 4", font=font, s0=s, s1=s),
      Road(cs[21], cs[20], name="Пестеля 1", font=font, s0=s, s1=s),
      Road(cs[20], cs[19], name="Пестеля 2", font=font, s0=s, s1=s),
      Road(cs[13], cs[15], name="Чайковского 2", font=font, s0=s, s1=s),
      Road(cs[2], cs[10], name="Литейный 2", font=font, s0=s, s1=s)]

iGens = [InitCarGenerator(r, n_cars_true=int(r.length//20)) for r in rs]

gen = CarGenerator(rs[0])
iGen = InitCarGenerator(rs[0])
SPB = City(pygame.font.SysFont(None, 24))

SPB.add_roads(rs)
SPB.add_c_roads(cs)
# SPB.add_cars(crs)
# SPB.add_car_generator(gen)
SPB.add_init_car_gens(iGens)
#SPB.loop(condition=lambda x: SPB.time < 1000)
SPB.loop_and_draw()


pygame.quit()