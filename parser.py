import re
import json
import argparse
from collections import Counter, deque


parser = argparse.ArgumentParser(description='Process access.log')
parser.add_argument('-f', dest='file',  action='store', help='Path to logfile', default='access.log')
args = parser.parse_args()


def reader(filename):
    # Регулярные выражения
    reg_ip = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    reg_method = r'\] \"(POST|GET|PUT|DELETE|HEAD)'
    reg_err_client = r' 4\d\d '
    reg_err_server = r' 5\d\d '
    reg_time = r'\d\d\d*$'

    with open(filename) as file:
        requests = 0    # Счетчик запросов
        ip_list = []    # Список всех IP адресов
        method_list = []    # Список всех методов
        err_client_list = []    # Список запросов с клиентскими ошибками
        err_server_list = []    # Список запросов с серверными ошибками
        biggest_time = deque(['1'], maxlen=10)    # Список с наибольшим временем запроса
        biggest_request = deque(maxlen=10)   # Список запросов с наибольшим временем
        for line in file:
            requests += 1   # Подсчет количества строк
            try:
                ip = re.findall(reg_ip, line)
                ip_list.append(ip[0])  # Добавление адреса ip в список
            except IndexError:
                pass
            try:
                method = re.findall(reg_method, line)
                method_list.append(method[0])  # Добавление метода в список
            except IndexError:
                pass
            # Добавление всех запросов с клиентской ошибкой в соответствующий список
            err_client_request = re.findall(reg_err_client, line)
            if err_client_request:
                err_client_list.append(line)
            # Добавление всех запросов с серверной ошибкой в соответствующий список
            err_server_request = re.findall(reg_err_server, line)
            if err_server_request:
                err_client_list.append(line)
            # Пополнение списка топ 10 самых долгих запросов
            time = re.findall(reg_time, line)
            int_time = int(time[0])
            for i in biggest_time:
                int_i = int(i[0])
                if int_time > int_i:
                    biggest_request.appendleft(line)
                    biggest_time.appendleft(time)
                    break

    top10ip = Counter(ip_list).most_common(10)  # Топ 10 ip адресов
    method_count = Counter(method_list)     # Словарь с количеством использования всех методов
    top10error_client = Counter(err_client_list).most_common(10)    # Топ 10 запросов с клиентской ошибкой
    top10error_server = Counter(err_server_list).most_common(10)  # Топ 10 запросов с серверной ошибкой

    biggest_request_list = []
    for i in biggest_request:
        biggest_request_list.append(i)


if __name__ == '__main__':
    reader(args.file)
