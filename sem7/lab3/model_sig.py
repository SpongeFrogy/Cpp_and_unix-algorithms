from city import *
from copy import deepcopy
from multiprocessing import Process, Manager


def make_signal_params(cs: list[CrossRoad], current_signals: list[bool]):
    res = []
    for current_signal in current_signals:
        res.append([{"timing": [5, 5],
                   "signal": current_signal[0],
                   "time": 5*int(not current_signal[0])},
                  {"timing": [5, 5],
                   "signal": current_signal[0],
                   "time": 5*int(not current_signal[0])}])
    return res


class Model:
    def __init__(self, current_signals: list[bool]) -> None:
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

        signal_params = make_signal_params(cs, current_signals)
        #print(len(signal_params))
        def _road(n0, n1, name, s0, s1, v):
            return Road(cs[n0], cs[n1], name, s0=s0, s1=s1, v=v)


        rs = [_road(0, 1, "Троицкий", signal_params[0][0], signal_params[0][1], 10),
              _road(1, 17, "Дворцовая", signal_params[1][0], signal_params[1][1], 8),
              _road(17, 16, "Дворцовая", signal_params[2][0], signal_params[2][1], 4),
              _road(16, 12, "К-ва 1", signal_params[3][0], signal_params[3][1], 10),
              _road(12, 2, "Кутузова 2", signal_params[4][0], signal_params[4][1], 14),
              _road(2, 3, "Литейный 1", signal_params[5][0], signal_params[5][1], 5),
              _road(3, 4, "Пироговская 1", signal_params[6][0], signal_params[6][1], 2),
              _road(4, 5, "Б Сам-ий", signal_params[7][0], signal_params[7][1], 10),
              _road(5, 6, "Финляндский", signal_params[8][0], signal_params[8][1], 10),
              _road(4, 6, "Пир-ая 2", signal_params[9][0], signal_params[9][1], 10),
              _road(6, 7, "Самп-кий", signal_params[10][0], signal_params[10][1], 10),
              _road(7, 8, "Петроградская 1", signal_params[11][0], signal_params[11][1], 10),
              _road(8, 0, "Петроградская 2", signal_params[12][0], signal_params[12][1], 10),
              _road(0, 9, "Каменноостровский", signal_params[13][0], signal_params[13][1], 10),
              _road(9, 7, "Куйбышевская", signal_params[14][0], signal_params[14][1], 10),
              _road(17, 18, "Лебяжьей к-и", signal_params[15][0], signal_params[15][1], 30),
              _road(18, 19, "Р. Мойки", signal_params[16][0], signal_params[16][1], 19),
              _road(19, 15, "Р. Фонтанки 1", signal_params[17][0], signal_params[17][1], 10),
              _road(15, 16, "Р. Фонтанки 2", signal_params[18][0], signal_params[18][1], 2),
              _road(15, 13, "Чайковского 1", signal_params[19][0], signal_params[19][1], 1),
              _road(13, 11, "Гагаринская 1", signal_params[20][0], signal_params[20][1], 6),  # Гагаринская
              _road(11, 12, "Гаг-ая 2", signal_params[21][0], signal_params[21][1], 4),
              _road(11, 10, "Шпалерная", signal_params[22][0], signal_params[22][1], 8),
              _road(10, 14, "Литейный 3", signal_params[23][0], signal_params[23][1], 12),
              _road(14, 21, "Литейный 4", signal_params[24][0], signal_params[24][1], 13),
              _road(21, 20, "Пестеля 1", signal_params[25][0], signal_params[25][1], 10),
              _road(20, 19, "Пестеля 2", signal_params[26][0], signal_params[26][1], 2),
              _road(13, 15, "Чайковского 2", signal_params[27][0], signal_params[27][1], 15),
              _road(2, 10, "Литейный 2", signal_params[28][0], signal_params[28][1], 1)]

        iGens = [InitCarGenerator(
            r, n_cars_true=int(r.length//10)) for r in rs]

        SPB = City()

        SPB.add_roads(rs)
        SPB.add_c_roads(cs)

        SPB.add_init_car_gens(iGens)

        self.city = SPB

    def simulate_one(self, t_max=1000):
        city = deepcopy(self.city)
        return city.loop(t_max=t_max)

    def _simulate_and_save(self, dt, t_max, result, index):
        city = deepcopy(self.city)
        output = city.loop(dt, t_max)

        # Safely writing the result
        result[index] = output

    def simulate(self, dt=0.1, t_max=1000, n_eval=5):
        with Manager() as manager:
            result = manager.list([None] * n_eval)

            # Create and start processes
            processes = []
            for i in range(n_eval):
                process = Process(target=self._simulate_and_save,
                                  args=(dt, t_max, result, i))
                processes.append(process)
                process.start()

            # Wait for all processes to finish
            for process in processes:
                process.join()
            return list(result)


if __name__ == "__main__":
    params = [
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [True, False],
        [False, False],
        [False, False],
        [False, True]
    ]
    model = Model(params)
    model.city.loop_draw()
