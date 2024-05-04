import hashlib
import os
import json
from datetime import datetime
from time import time
'''
Поиск дубликатов в заданной директории
На входе скрпит запрашивает директорию и проверяет ее существование
На выходе получаем отчет report_имя_директории_текущая_дата.json
'''


def score_hash(filename):
    '''
    функция вычисления хешсумму MD5 для передаваемого файла filename
    '''
    block_size = 65536
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()


def dir_score_all(path):
    '''
    перебираем все файлы во всех каталогах и подкаталогах
    '''
    res = {}
    count_ = sum(len(filenames) for dirpath, dirnames, filenames in os.walk(path))
    percent = 100 / count_
    progress = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            progress += percent
            print('\rОбработка файлов завершена на %d%%' % progress, end='', flush=True)
            res[os.path.join(dirpath, filename)] = score_hash(os.path.join(dirpath, filename))
    print('\rОбработка файлов завершена на 100%')
    return res


def create_report(dir_scan:dict, report_filename:str):
    hash_set = set(dir_scan.values())
    filenames_duplicate = []
    if len(dir_scan) != len(hash_set):
        print("Есть файлы дубликаты")
        for h in hash_set:
            if list(dir_scan.values()).count(h) > 1:
                filenames_duplicate.append(h)
    else:
        print("Дубликатов файлов нет")
        return exit(0)

    report_dict = {}
    all_size = 0
    percent = 100 / len(dir_scan)
    progress = 0

    for k, v in dir_scan.items():
        if v in filenames_duplicate:
            create_file_date = datetime.fromtimestamp(os.stat(k).st_ctime)
            last_change_file_date = datetime.fromtimestamp(os.stat(k).st_mtime)
            report_dict[k] = [f"{(os.stat(k).st_size / 1024):.2f}Kb",
                              f"дата создания {create_file_date:%Y.%m.%d_%H:%M}",
                              f"дата изменения {last_change_file_date:%Y.%m.%d_%H:%M}"], f"MD5 {v}"
            progress += percent
            print('\rСоздание файла отчета завершена на %d%%' % progress, end='', flush=True)

            all_size += os.stat(k).st_size
    report_dict = dict(sorted(report_dict.items(), key=lambda x: x[1][1]))
    print('\rСоздание файла отчета завершена на 100%')
    report_dict[f"Всего дубликатов найдено {len(report_dict)} шт"] = f"Общий размер файлов {all_size / 1024:.2f}Kb"

    with open(report_filename, "w", encoding="utf-8") as json_file:
        json.dump(report_dict, json_file, ensure_ascii=False, indent=4)
    return len(report_dict), all_size


if __name__ == '__main__':
    path_filename = input('Введите директорию ')
    if not os.path.isdir(path_filename):
        print("Не существующая директория")
        exit(0)
    start_time = time()
    a = path_filename.replace(':\\', '_').replace('\\', '_')
    today = datetime.today()
    report_filename = f"report_{a}_{today:%Y-%m-%d}.json"

    dir_scan = dir_score_all(path_filename)

    all_duplicate_files, all_size = create_report(dir_scan, report_filename)
    end_time = time()
    print(f"Всего дубликатов найдено {all_duplicate_files} шт Общий размер файлов {all_size / 1024:.2f}Kb")
    print(f"Выполнено за {(end_time - start_time):.3f} сек")
