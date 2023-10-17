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
// оптимизация
      // сделать функцию оптимизации
      //    должна учитывать что на каждом перекрестке хотя бы один сигнал должен быть красным 
      // определиться с методом (генетический алгоритм или optuna)
      //    по сложности как? можно за неделю доделать?
      // оптимизировать
- (опционально)
      * разделить классы по файлам 
      * просмотреть весь код на лишние куски и неоптимальные if 
"""




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

s1 = {"timing": [5, 5],
     "signal": True,
     "time": 5}

ss = {}

for c in cs:
    ss[c] = s

rs = [Road(cs[0], cs[1], name="Троицкий", s0=s, s1=s1),
      Road(cs[1], cs[17], name="Дворцовая", s0=s, s1=s1),
      Road(cs[17], cs[16], name="Дворцовая", s0=s, s1=s1),
      Road(cs[16], cs[12], name="К-ва 1", s0=s, s1=s1),
      Road(cs[12], cs[2], name="Кутузова 2", s0=s, s1=s1),
      Road(cs[2], cs[3], name="Литейный 1", s0=s, s1=s1),
      Road(cs[3], cs[4], name="Пироговская 1", s0=s, s1=s1),
      Road(cs[4], cs[5], name="Б Сам-ий", s0=s, s1=s1),
      Road(cs[5], cs[6], name="Финляндский", s0=s, s1=s1),
      Road(cs[4], cs[6], name="Пир-ая 2", s0=s, s1=s1),
      Road(cs[6], cs[7], name="Самп-кий", s0=s, s1=s1),
      Road(cs[7], cs[8], name="Петроградская 1", s0=s, s1=s1),
      Road(cs[8], cs[0], name="Петроградская 2", s0=s, s1=s1),
      Road(cs[0], cs[9], name="Каменноостровский", s0=s, s1=s1),
      Road(cs[9], cs[7], name="Куйбышевская", s0=s, s1=s1),
      Road(cs[17], cs[18], name="Лебяжьей к-и", s0=s, s1=s1),
      Road(cs[18], cs[19], name="Р. Мойки", s0=s, s1=s1),
      Road(cs[19], cs[15], name="Р. Фонтанки 1", s0=s, s1=s1),
      Road(cs[15], cs[16], name="Р. Фонтанки 2", s0=s, s1=s1),
      Road(cs[15], cs[13], name="Чайковского 1", s0=s, s1=s1),
      Road(cs[13], cs[11], name="Гагаринская 1", s0=s1, s1=s1), # Гагаринская
      Road(cs[11], cs[12], name="Гаг-ая 2", s0=s, s1=s1),
      Road(cs[11], cs[10], name="Шпалерная", s0=s, s1=s1),
      Road(cs[10], cs[14], name="Литейный 3", s0=s, s1=s1),
      Road(cs[14], cs[21], name="Литейный 4", s0=s, s1=s1),
      Road(cs[21], cs[20], name="Пестеля 1", s0=s, s1=s1),
      Road(cs[20], cs[19], name="Пестеля 2", s0=s, s1=s1),
      Road(cs[13], cs[15], name="Чайковского 2", s0=s, s1=s1),
      Road(cs[2], cs[10], name="Литейный 2", s0=s, s1=s1)]

iGens = [InitCarGenerator(r, n_cars_true=int(r.length//10)) for r in rs]

iGen = InitCarGenerator(rs[0])
SPB = City()

SPB.add_roads(rs)
SPB.add_c_roads(cs)

SPB.add_init_car_gens(iGens)
#SPB.loop(condition=lambda x: SPB.time < 1000)
SPB.loop_plot()
#SPB.loop_draw()

