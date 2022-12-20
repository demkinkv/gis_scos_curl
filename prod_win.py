#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import re
import time
import json
import shutil
from glob import glob
from pathlib import Path

#*функция счётчик
def create_counter():
    i = 0
    def func():
        nonlocal i
        i += 1
        return i
    return func

#!_3
#?функция обработки файлов после отправки jcon/curl
def operation_to_file(list_item_one, json_key):
    #*чистим файл от привязки путей
    rem_lng=len(str(env_workdir))
    list_item_one_solt=list_item_one[rem_lng+1:]
    #*строим путь до файла
    list_item_one_solt_path = Path(env_workdir, list_item_one_solt) 
    print(list_item_one_solt_path)
    #* выведем значение переменной list_item_one_solt_path:
    print(list_item_one_solt_path)
    time.sleep(0.2)
    file_stats = os.stat(str(list_item_one_solt_path)+'.log')
    print(f'!File Size in Bytes is {file_stats.st_size}')
    #*проверка размера лога,т.е. его выгрузку
    if (int(file_stats.st_size) > 2048):
        print (f'!Успешная выгрузка файла, его размер: {file_stats.st_size}')
        file_stats_test = ('correct')
        counter_correct()
    else:
        print (f'!Ошибка выгрузки, проверьте файл, его размер: {file_stats.st_size}')
        file_stats_test = 'error'
        counter_error()
    #*генерируем имя каталога распределения&создаём каталоги, если их нет
    os.makedirs(os.path.join(env_workdir,file_stats_test,json_key), mode=0o777, exist_ok=True)
    #*перемещение файлов
    os.replace(list_item_one_solt_path, str(Path(env_workdir,file_stats_test,json_key,list_item_one_solt)))
    os.replace(str(list_item_one_solt_path)+'.log', str(Path(env_workdir,file_stats_test,json_key,list_item_one_solt))+'.log')

#!_2
#?функция по выгрузке файлов
def curl_upload (list_item_one, json_key):
    curl_command=(f"{env_path_to_curl} -k -i -X POST -H Content-Type:application/json -H X-CN-UUID:{X_CN_UUID}  https://tls.online.edu.ru/vam/api/v2/{json_key} -d @{list_item_one} > {list_item_one}.log")
    print (f'Curl_command execute: '+curl_command)
    if Debug:
        pass
    else:
        os.system(curl_command)

#!_1
#*функция обработки JSON файлов
def search_json():
    #*выводим элементы папки с нужным расширением
    list_item = list(glob(os.path.join(env_workdir, '*.json')))
    for list_item_one in list_item:
        print (f'!Found JSON: '+list_item_one)
        #*открытие файла для проверки
        with open(list_item_one, 'rt', encoding='utf-8-sig') as read_file_json:
            data_json = json.load(read_file_json)
            #*Проверка JSON файла на пустоту ID организации
            if not (data_json.get('organization_id') == organization_id):
                print('!organization_id is None/JSON Write add binary')
                data_json["organization_id"] = organization_id
                #*сохранение файла после модицикации
                with open(list_item_one, 'wt', encoding='utf-8-sig') as read_file_json:
                    json.dump(data_json, read_file_json, ensure_ascii=False, indent=4)
            #*выборка файлов по категори и подготовка переменных для отправки
            if 'educational_programs' in data_json:
                json_key = 'educational_programs'
            elif 'study_plans' in data_json:
                json_key = 'study_plans'
            elif 'disciplines' in data_json:
                json_key = 'disciplines'
            elif 'study_plans_disciplines' in data_json:
                json_key = 'study_plan_disciplines'
            elif 'students' in data_json:
                json_key = 'students'
            elif 'study_plans_students' in data_json:
                json_key = 'study_plans_students'
            elif 'contingent_flows' in data_json:
                json_key = 'contingent_flows'
            elif 'marks' in data_json:
                json_key = 'marks'
            else:
                print('!No str to json')
                pass
        #*отправка данных в функцию выгрузки (json file&json_key)
        print('!Find keys: '+json_key)
        #?вызыв функции по выгрузке файлов&передача переменных для выгрузки
        curl_upload(list_item_one, json_key) #!_2 
        #?фунция операции с файлом&перемещание по папкам
        operation_to_file(list_item_one, json_key) #!_3

#?объявление переменных выгрузки
organization_id='!!!organization_id!!!'
X_CN_UUID= '!!!X_CN_UUID!!!'
env_workdir = '051222'
Debug = True
env_path_to_curl = 'curl.exe'

#?объявление счётчиков функций
counter_correct = create_counter()
counter_error = create_counter()

#*start __main__
def main():
    search_json() #!_1
    print(f'!Done!\n Correct: {counter_correct()-1} Error: {counter_error()-1}')
 
#*start project&start __main__
if __name__ == "__main__":
    main()
