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
        def _road(n0, n1, name, clr0: bool, clr1: bool):
            return Road(cs[n0], cs[n1], name, s0=signal_params[n0][int(clr0)], s1=signal_params[n1][int(clr1)])


        rs = [_road(0, 1, "Троицкий", True, False),
              _road(1, 17, "Дворцовая", True, False),
              _road(17, 16, "Дворцовая", True, False),
              _road(16, 12, "К-ва 1", True, False),
              _road(12, 2, "Кутузова 2", True, False),
              _road(2, 3, "Литейный 1", True, False),
              _road(3, 4, "Пироговская 1", True, False),
              _road(4, 5, "Б Сам-ий", True, False),
              _road(5, 6, "Финляндский", True, False),
              _road(4, 6, "Пир-ая 2", True, False),
              _road(6, 7, "Самп-кий", True, False),
              _road(7, 8, "Петроградская 1", True, False),
              _road(8, 0, "Петроградская 2", True, False),
              _road(0, 9, "Каменноостровский", True, False),
              _road(9, 7, "Куйбышевская", True, False),
              _road(17, 18, "Лебяжьей к-и", True, False),
              _road(18, 19, "Р. Мойки", True, False),
              _road(19, 15, "Р. Фонтанки 1", True, False),
              _road(15, 16, "Р. Фонтанки 2", True, False),
              _road(15, 13, "Чайковского 1", True, False),
              _road(13, 11, "Гагаринская 1", False, False),  # Гагаринская
              _road(11, 12, "Гаг-ая 2", True, False),
              _road(11, 10, "Шпалерная", True, False),
              _road(10, 14, "Литейный 3", True, False),
              _road(14, 21, "Литейный 4", True, False),
              _road(21, 20, "Пестеля 1", True, False),
              _road(20, 19, "Пестеля 2", True, False),
              _road(13, 15, "Чайковского 2", True, False),
              _road(2, 10, "Литейный 2", True, False)]

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

    # def _simulate_and_save(self, dt, t_max, result, index):
    #     city = deepcopy(self.city)
    #     result[index] = city.loop(dt, t_max)
    #     return result

    # def simulate(self, dt=0.1, t_max=1000, n_eval=5):
    #     result = [None] * n_eval

    #     with ThreadPoolExecutor(max_workers=n_eval) as executor:
    #         futures = []
    #         for i in range(n_eval):
    #             futures.append(executor.submit(
    #                 self._simulate_and_save, dt, t_max, result, i))

    #         for future in futures:
    #             # Wait for the task to complete and populate the results.
    #             # Replace _ with actual variable if you want to capture return values
    #             _ = future.result()

    #     return result

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
    best_params = [35.334781398620066, 34.65566840904645, 36.777312120028554, 38.02428589041652, 39.91484775626096, 45.62723977140812, 24.62914654488359, 43.46211666953861, 23.550754379111634, 23.509832638649478,  37.3498126681518,  40.234231452719584,  41.3880437002321,  32.520092238043866,  40.46409322551679,  23.080566588266144,  29.46636031678918,  39.412482469126175,  40.39439974555297,  44.41406794916072,  25.025802268078493,  35.064535958728335]
    model = Model([[p, 50-p] for p in best_params])
    model.city.loop_plot()
