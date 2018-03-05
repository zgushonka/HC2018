#!/usr/bin/python3

import os
import time
import sys
import taxi_routines

# ---------------------- Point
class Point(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column


# ---------------------- Car
class Car(object):
    def __init__(self, index):
        self.location = Point(0, 0)
        self.current_time = 0
        self.routes_map = []
        self.score = 0
        self.index = index

    def add_route(self, route, distance_to_route, profit=0):
        self.routes_map.append(route)
        self.location = route.finish_point
        self.current_time = max((self.current_time + distance_to_route), route.start_time) + route.distance
        self.score += profit
    
    @property
    def result(self) -> str:
        result = "{}".format(len(self.routes_map))
        for route in self.routes_map:
            result += " {}".format(route.index)
        return result


# ---------------------- Route
class Route(object):
    def __init__(self, start_row, start_column, finish_row, finish_column, start_time, finish_time, index):
        self.start_point = Point(start_row, start_column)
        self.finish_point = Point(finish_row, finish_column)
        self.start_time = start_time
        self.finish_time = finish_time
        self.is_assigned = False
        self.index = index

    @property
    def distance(self) -> int:
        dist = abs(self.start_point.row - self.finish_point.row) + abs(self.start_point.column - self.finish_point.column)
        return dist


# ---------------------- Profit_calculator
class Profit_calculator(object):
    def __init__(self, route, car):
        self.route = route
        self.car = car
        self.distance_from_car_to_route = self.calc_distance_from_car_to_route()
        self.wait_time = self.calc_waitTime()
        self.is_finish_before_deadline = self.calc_is_finish_before_deadline()

    @property
    def cost(self):
        return self.cost_function()

    def calc_distance_from_car_to_route(self) -> int:
        distance_row = abs(self.route.start_point.row - self.car.location.row)
        distance_col = abs(self.route.start_point.column - self.car.location.column)
        return distance_row + distance_col

    @property
    def time_car_arrival_to_start(self) -> int:
        time = self.car.current_time + self.distance_from_car_to_route
        return time

    def calc_is_finish_before_deadline(self) -> bool:
        can_finish_at = self.time_car_arrival_to_start + self.route.distance
        can_make_it = can_finish_at <= self.route.finish_time
        return can_make_it

    @property
    def willTakeBonus(self):
        willTakeBonus = (self.time_car_arrival_to_start <= self.route.start_time)
        return willTakeBonus

    @property
    def bonus(self) -> int:
        bonus = bonus_B if self.willTakeBonus else 0
        return bonus

    @property
    def profit(self) -> int:
        profit = (self.bonus + self.route.distance)
        return profit

    @property
    def profit_for_car(self) -> int:
        return self.profit if self.is_finish_before_deadline else 0

    def calc_waitTime(self) -> int:
        time_before_route_starts = (self.route.start_time - self.car.current_time)
        wait_time = time_before_route_starts - self.distance_from_car_to_route
        return wait_time

    def cost_function(self) -> int:
        if not self.is_finish_before_deadline: return None
        # profit = self.profit - self.distance_from_car_to_route #- self.wait_time
        
        profit = self.bonus - self.distance_from_car_to_route - self.wait_time
        return profit


# -------------------------- calc routes
def calc_routes(routes, cars):
    while True:
        repeat = calc_costs_profits(routes, cars)
        if not repeat: break
    # end while


def calc_costs_profits(routes, cars):
    is_routes_to_check = False
    for car in cars:
        made_route = calc_costs_for_car(routes, car)
        if made_route:
            is_routes_to_check = True
    return is_routes_to_check


def calc_costs_for_car(routes, car):
    this_car_profits = []
    for route in routes:
        if route.is_assigned: continue

        calc = Profit_calculator(route, car)
        profit = calc.profit_for_car

        cost = calc.cost
        if cost is not None:
            this_car_profits.append((route, car, cost, profit, calc.distance_from_car_to_route))
    
    if this_car_profits:
        this_car_profits.sort(key=lambda tup: tup[2], reverse=True)
        (route, car, cost, profit, distance) = this_car_profits[0]
        try_assign_route(route, car, profit, distance)
    else:
        # nithing else to do
        return False
    return True


def try_assign_route(route, car, profit, distance):
    if profit > 0:
        car.add_route(route, distance, profit)
        route.is_assigned = True











def sort_by_start_time(routes) -> list:
    sorted_routes = sorted(routes, key=lambda item: item.start_time)
    return sorted_routes

# -------------------------- main
if __name__ == '__main__':
    data_sets = {
        'a_example': 'a_example.in',
        'b_should_be_easy': 'b_should_be_easy.in',
        # 'c_no_hurry': 'c_no_hurry.in',
        # 'd_metropolis': 'd_metropolis.in',
        # 'e_high_bonus': 'e_high_bonus.in'
    }

    total_max_distance = 0
    total_max_score = 0
    total_our_score = 0
    start = time.time()
    for data_set in data_sets:
        (rows_R, columns_C, fleet_F, rides_N, bonus_B, steps_T, routes_raw) \
            = taxi_routines.load_data(data_sets[data_set])

        routes = [Route(*route_raw) for route_raw in routes_raw]
        routes_copy = [Route(*route_raw) for route_raw in routes_raw]
        # sorted_routes = sort_by_start_time(routes)

        cars = [Car(i) for i in range(fleet_F)]

        # calc car routes
        start_data_set = time.time()
        calc_routes(routes, cars)
        end_data_set = time.time()

        # uncomment this to see snalytics
        (total_distance, max_dataset_score, our_score) \
            = taxi_routines.printAnalyticsData(data_set, routes_copy, cars, rides_N, bonus_B, steps_T)

        total_max_distance += total_distance
        total_max_score += max_dataset_score
        total_our_score += our_score
        print('time - {:0.4f}s'.format(end_data_set - start_data_set))
        print()

        taxi_routines.write_out(cars, filename=data_set)

    print('total_max_dist  - {}'.format(total_max_distance))
    print('total_max_score - {}'.format(total_max_score))
    print('total_our_score - {}'.format(total_our_score))
    print('total efficiency - {:0.2f}%'.format(total_our_score/total_max_score*100))
    end = time.time()
    print('total time - {:0.2}s'.format(end - start))


