from city import *
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Manager


def make_signal_params(cs: list[CrossRoad], timings: list[int, int]):
    res = {}
    for i, timing in zip(range(len(cs)), timings):
        res[i] = [{"timing": timing,
                   "signal": True,
                   "time": 0},
                  {"timing": timing,
                   "signal": False,
                   "time": timing[0]}]
    return res


class Model:
    def __init__(self, timings: list[int, int]) -> None:
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

        signal_params = make_signal_params(cs, timings)

        def _road(n0, n1, name, clr0: bool, clr1: bool, v):
            return Road(cs[n0], cs[n1], name, s0=signal_params[n0][int(clr0)], s1=signal_params[n1][int(clr1)], v=v)


        rs = [_road(0, 1, "Троицкий", True, False, 10),
              _road(1, 17, "Дворцовая", True, False, 8),
              _road(17, 16, "Дворцовая", True, False, 4),
              _road(16, 12, "К-ва 1", True, False, 10),
              _road(12, 2, "Кутузова 2", True, False, 14),
              _road(2, 3, "Литейный 1", True, False, 5),
              _road(3, 4, "Пироговская 1", True, False, 2),
              _road(4, 5, "Б Сам-ий", True, False, 10),
              _road(5, 6, "Финляндский", True, False, 10),
              _road(4, 6, "Пир-ая 2", True, False, 10),
              _road(6, 7, "Самп-кий", True, False, 10),
              _road(7, 8, "Петроградская 1", True, False, 10),
              _road(8, 0, "Петроградская 2", True, False, 10),
              _road(0, 9, "Каменноостровский", True, False, 10),
              _road(9, 7, "Куйбышевская", True, False, 10),
              _road(17, 18, "Лебяжьей к-и", True, False, 30),
              _road(18, 19, "Р. Мойки", True, False, 19),
              _road(19, 15, "Р. Фонтанки 1", True, False, 10),
              _road(15, 16, "Р. Фонтанки 2", True, False, 2),
              _road(15, 13, "Чайковского 1", True, False, 1),
              _road(13, 11, "Гагаринская 1", False, False, 6),  # Гагаринская
              _road(11, 12, "Гаг-ая 2", True, False, 4),
              _road(11, 10, "Шпалерная", True, False, 8),
              _road(10, 14, "Литейный 3", True, False, 12),
              _road(14, 21, "Литейный 4", True, False, 13),
              _road(21, 20, "Пестеля 1", True, False, 10),
              _road(20, 19, "Пестеля 2", True, False, 2),
              _road(13, 15, "Чайковского 2", True, False, 15),
              _road(2, 10, "Литейный 2", True, False, 1)]

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
    best_params =  [ 7.675447134961057, 5.306722725032909, 9.672194056398018, 2.5424687666404533, 6.577404240604412, 7.588633806966979, 5.366467594598852, 4.694434096702121, 4.7776705306988365, 9.223291973657577,  7.1672629236121725,  8.402297655683864,  9.625685966321265,  5.468455928177309,  7.303268611787422,  4.549349878092204,  5.871253374241523,  3.6352711162557982,  5.348859810474501,  6.043749826463642,  5.7698757754962315,  7.336785235353177]

    model = Model([[p, 10-p] for p in best_params])
    model.city.loop_plot()
