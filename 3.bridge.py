from threading import Lock, Thread
import random, time


class Bridge:

    # Class constructor implementation.
    def __init__(self):
        self.threads = []
        self.bridge_counter = 0
        self.side_passing = None
        self.ask_cross_lock = Lock()
        self.cross_lock = Lock()
        self.full_bridge = False

    def arrive_bridge(self, car):
        print(car, 'arrived')

        while True:

            # If the bridge is full, stop crossing until bridge is empty, to not starve opposite side
            with self.cross_lock:
                if self.full_bridge:
                    continue

            self.ask_cross_lock.acquire()
            # If same side with car is crossing, or bridge is empty, attempt crossing
            if self.side_passing == car[2] or not self.side_passing:
                self.side_passing = car[2]
                self.ask_cross_lock.release()

                self.cross_lock.acquire()
                # If less than three on bridge allow car to pass
                if self.bridge_counter < 3:

                    self.cross_bridge(car)
                    break

                else:
                    # Bridge was full, start again
                    self.cross_lock.release()
            else:
                # Other side was crossing, start again
                self.ask_cross_lock.release()

    def cross_bridge(self, car):

        self.bridge_counter += 1
        if self.bridge_counter == 3:
            self.full_bridge = True
        self.cross_lock.release()

        time.sleep(car[1])
        print(car, 'in')

        with self.cross_lock:
            self.bridge_counter -= 1
            self.exit_bridge(car)

    def exit_bridge(self, car):
        with self.ask_cross_lock:
            if self.bridge_counter == 0:
                self.full_bridge = False
                self.side_passing = None
        print(car, 'exiting bridge')

    def run_thread(self, car):
        # Wait for random time t_arrive, before arriving bridge
        time.sleep(car[3])
        self.arrive_bridge(car)

    def create_threads(self, cars):
        for car in cars:
            thread = Thread(target=self.run_thread, args=(car,))
            self.threads.append(thread)

    def run_threads(self):
        for thread in self.threads:
            thread.start()


def create_cars(min_cars, max_cars, t_min, t_max):
    num_cars = random.randint(min_cars, max_cars)
    cars = []
    for num_car in range(num_cars):
        cross_time = random.randint(t_min, t_max)
        t_arrive = random.randint(t_min, t_max)
        side_num = random.randint(0, 1)
        side = 'L' if side_num == 0 else 'R'
        car = [num_car, cross_time, side, t_arrive]
        cars.append(car)
    return cars


def main():
    min_cars = 3
    max_cars = 9
    t_min = 1
    t_max = 3
    cars = create_cars(min_cars,  max_cars, t_min, t_max)

    print('created', cars)
    bridge = Bridge()
    bridge.create_threads(cars)
    bridge.run_threads()


if __name__ == '__main__':
    main()