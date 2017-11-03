# coding: utf8

#  СКРИПТ ВЫПОЛНЯЕТ ЦИФРОВУЮ ОБРАБУТКУ СИГНАЛА
#  И СРАВНИВАЕТ ПО ЗАДАННЫМ КРИТЕРИЯМ ДВЕ ПОЛОСЫ ЧАСТОТ
#  (КРИТЕРИИ НАДО ИСПРАИТЬ, СКО НЕПОДХОДИТ)
#  ПОЛСЕ ЭТОГО СКРИПТ СОХРАНЯЕТ ПОЛУЧЕННЫЕ ДАННЫЕ В ВИДЕ PANDAS DATAFRAME.
#  ВЫЧИСЛЕНИЯ И ЗАПИСЬ В ФРЭЙМ ПРОИСХОДЯТ АВТОМАТИЧЕСКИ
#  ПООЧЕРЁДНО ДЛЯ ВСЕХ ФАЙЛОВ В УКАЗАННЫХ НИЖЕ ПУТЯХ,

# ПУТИ К ИСХОДНЫМ ДАННЫМ
Path1 = 'C:\Users\Alexander\Documents\Filtr\data/1/'
Path2 = 'C:\Users\Alexander\Documents\Filtr\data/2/'
Path3 = 'C:\Users\Alexander\Documents\Filtr\data/3/'
Path4 = 'C:\Users\Alexander\Documents\Filtr\data/4/'
Path = [Path1, Path2, Path3, Path4]

import numpy as np
import pandas as pd
import os

fileType = '.csv'
chanelName = ('F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4')

# ДАТАФРЭЙМ
df = pd.DataFrame({}, index=chanelName)
df.index.name = 'Channel'

# ЧАСТОТА ДИСКРЕТИЗАЦИИ
fs = 128.0

# НИЖНЯЯ ЧАСТОТА АЛЬФА-ДИАПАЗОНА
f_alfa = 8.0

# ГРАНИЧНАЯ ЧАСТОТА МЕЖДУ АЛЬФА И БЭТА
f_split = 13.0

# ВЕРХНЯЯ ЧАСТОТА БЭТА-ДИАПАЗОНА
f_beta = 40.0

# СРЕДНЕЕ ЗНАЧЕНИЕ ШУМА ДЛЯ КАЖДОГО КАНАЛА
noise = [2305.4753315853659, 2301.6848498780491, 2386.0438441463416, 2059.8952554878051, 2308.4687019512198, 2065.9882565853659, 2266.5526353658538, 2164.4456224390246, 1957.1570242682926, 2189.068528170732, 2012.3312125609757, 2323.6680578048786, 2006.4878440243901, 2285.2065632926833]

# CONDITION_NUM - СОСТОЯНИЕ (ОТ 1 ДО 4)
for condition_num in range(np.size(Path)):
    catalogList = os.listdir(Path[condition_num])

    # КОЛЛИЧЕСТВО ФАЙЛОВ В ПАПКЕ
    listSize = len(catalogList)

    for file_num in range(listSize):
        # file_num - НОМЕР ФАЙЛА С ИСХОДНЫМИ ДАННЫМИ В ПАПКЕ
        userName = catalogList[file_num][1 : -4]
        userCondition = catalogList[file_num][0]

        # ОЧИЩАЕМ СПИСОК ОТ ЗНАЧЕНИЙ С ПРЕДЫДУЩЕЙ ИТЕРАЦИИ
        result = list()

        for chanel_num in range(14):
            #  СЧИТЫВАЕМ ДАННЫЕ ИЗ ФАЙЛА
            readFileName = userCondition + userName + fileType
            dataSet = pd.read_csv(Path[condition_num] + readFileName)

            # ДАННЫЕ ИСХОДНОГО СИГНАЛА ДЛЯ ТЕКУЩЕГО КАНАЛА
            loadData = dataSet.ix[:128, chanel_num]

            # УБИРАЕМ ПОСТОЯННУЮ СОСТАВЛЯЮЩУЮ
            loadData = loadData - noise[chanel_num]
            dataSize = loadData.size

            # ВЫЧИСЛЯЕМ ДИАПАЗОН ЧАСТОТ ДЛЯ ПОСТРОЕНИЯ СПЕКТРА
            # ПО Т.КОТЕЛЬНИКОВА  ВЕРХНЯЯ ЧАСТОТА СПЕКТРА РАВНА ПОЛОВИНЕ fs
            f = np.abs(np.fft.fftfreq(dataSize, 1. / fs))
            # f = f[:(dataSize / 2 + 1)]

            # ВЫЧИСЛЯЕМ АМЛИТУДНЫЙ СПЕКТР
            # ДЕЛИМ НА РАЗМЕР МАССИВА С ВХОДНЫМИ ДАННЫМИ (dataSize)  ДЛЯ НОРМАЛИЗАЦИИ
            spector = np.abs(np.fft.fft(loadData) / dataSize)

            # СРАВНЕНИЕ ДИАПАЗОНОВ:
            # ДАННЫЕ ПРЕДСТАВЛЕННЫ В ВИДЕ МАССИВА NUMPY
            # ПРОВЕРЯЕМ, ВХОДИТ ЛИ ЧАСТОТА В ЗАДАННЫЙ ДИАПАЗОН
            # ЕСЛИ ВХОДИТ, ТО СООТВЕТСВУЮЩЕЕ ЭТОЙ ЧАСТОТЕ ЗНАЧЕНИЕ АМПЛИТУДНОГО СПЕКТРА
            # ДОБАВЛЯЕМ В СПИСОК _frequensyList
            # ПОСЛЕ ЗАВЕРШЕНИЯ ЦИКЛА ВЫЧИСЛЯЕМ СКО (STD) ИМЕЮЩИХСЯ СПИСКОВ И РЕЗУЛЬТАТЫ ДЕЛИМ ДРУГ НА ДРУГА
            alfa_frequensyList = list()
            for i in range(f.size):
                if f[i] >= f_alfa and f[i] < f_split:
                    alfa_frequensyList.append(spector[i])
            # ВЫЧИСЛЯЕМ СКО
            alfa = np.std(alfa_frequensyList)

            beta_frequensyList = list()
            for k in range(f.size):
                if f[k] >= f_split and f[k] < f_beta:
                    beta_frequensyList.append(spector[k])
            # ВЫЧИСЛЯЕМ СКО
            beta = np.std(beta_frequensyList)

            # РЕЗУЛЬТАТ СРАВНЕНИЯ ПОЛОС
            div = alfa / beta
            result.append(div)
            print('Condition ', condition_num + 1, 'File', userName, 'Chanel ', chanel_num + 1)

        # ЗАПИСЬ ДАННЫХ ТЕКУЩЕГО ЧЕЛОВЕКА В ДАТАФРЭЙМ
        df[userName] = result
    # СОХРАНЕНИЕ В CSV (ДЛЯ КАЖДОГО СОСТОЯНИЯ СОЗДАСТСЯ ОТДЕЛЬНЫЙ ФАЙЛ)
    df.to_csv(str(condition_num + 1) + fileType)