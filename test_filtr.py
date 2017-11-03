# coding: utf8
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import freqz
from scipy import signal

# chanelName = ('F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4')

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


readFileName = 'C:\Users\Alexander\Documents\Filtr\data/1/1Koval.csv'

# ОТЧЁТЫ ИСХОДНОГО СИГНАЛА
dataSet = pd.read_csv(readFileName)

# ЧАСТОТА ДИСКРЕТИЗАЦИИ
fs = 128.0

# НИЖНЯЯ ЧАСТОТА АЛЬФА-ДИАПАЗОНА
f_alfa = 8.0

# ГРАНИЧНАЯ ЧАСТОТА МЕЖДУ АЛЬФА И БЭТА
f_split = 13.0

# ВЕРХНЯЯ ЧАСТОТА БЭТА-ДИАПАЗОНА
f_beta = 30.0

# СРЕДНЕЕ ЗНАЧЕНИЕ ШУМА ДЛЯ КАЖДОГО КАНАЛА
noise = [2305.4753315853659, 2301.6848498780491, 2386.0438441463416, 2059.8952554878051, 2308.4687019512198, 2065.9882565853659, 2266.5526353658538, 2164.4456224390246, 1957.1570242682926, 2189.068528170732, 2012.3312125609757, 2323.6680578048786, 2006.4878440243901, 2285.2065632926833]

# k - НОМЕРА КАНАЛОВ
for k in range(1):

    # КОЛЛИЧЕСТВО ОТСЧЁТОВ ИСХОДНОГО СИГНАЛА ДЛЯ ТЕКУЩЕГО КАНАЛА
    loadData = dataSet.ix[:1280, k]
    # УБИРАЕМ ПОСТОЯННУЮ СОСТАВЛЯЮЩУЮ
    loadData = loadData - noise[k]
    dataSize = loadData.size

    t = np.arange(start=0, stop=dataSize, step=1)

    # ВЫЧИСЛЯЕМ ДИАПАЗОН ЧАСТОТ ДЛЯ ПОСТРОЕНИЯ СПЕКТРА
    # ПО Т.КОТЕЛЬНИКОВА  ВЕРХНЯЯ ЧАСТОТА СПЕКТРА РАВНА ПОЛОВИНЕ fs
    f = np.abs(np.fft.fftfreq(dataSize, 1. / fs))

    # ДЕЛИМ НА РАЗМЕР МАССИВА С ВХОДНЫМИ ДАННЫМИ (dataSize)  ДЛЯ НОРМАЛИЗАЦИИ
    signalFFT = np.fft.fft(loadData) / dataSize
    Amplitude_spector = np.abs(signalFFT)

    filteredSignal = butter_bandpass_filter(loadData, f_alfa, f_beta, fs, order=9)
    filtered_Signal_FFT = np.fft.fft(filteredSignal) / dataSize
    Amplitude_filtered_spector = np.abs(filtered_Signal_FFT)
    fildered_phase_spector = np.angle(filtered_Signal_FFT)


    # СРАВНЕНИЕ ДИАПАЗОНОВ:
    # ДАННЫЕ ПРЕДСТАВЛЕННЫ В ВИДЕ МАССИВА NUMPY
    # ПРОВЕРЯЕМ, ВХОДИТ ЛИ ЧАСТОТА В ЗАДАННЫЙ ДИАПАЗОН
    # ЕСЛИ ВХОДИТ, ТО СООТВЕТСВУЮЩЕЕ ЭТОЙ ЧАСТОТЕ ЗНАЧЕНИЕ АМПЛИТУДНОГО СПЕКТРА
    # ДОБАВЛЯЕМ В СПИСОК _frequensyList
    # ПОСЛЕ ЗАВЕРШЕНИЯ ЦИКЛА ВЫЧИСЛЯЕМ СКО ИМЕЮЩИХСЯ СПИСКОВ И РЕЗУЛЬТАТЫ ДЕЛИМ ДРУГ НА ДРУГА
    # ДАННЫЙ МЕТОД НЕКОРРЕКТНЫЙ, СРАВНИВАТЬ ДИАПАЗОНЫ НАДО ПО ДРУГИМ КРИТЕРИЯМ

    # alfa_frequensyList = list()
    # for i in range(f.size):
    #     if f[i] >= f_alfa and f[i] < f_split:
    #         alfa_frequensyList.append(spector[i])
    # alfa = np.std(alfa_frequensyList)
    #
    # beta_frequensyList = list()
    # for i in range(f.size):
    #     if f[i] >= f_split and f[i] < f_beta:
    #         beta_frequensyList.append(spector[i])
    # beta = np.std(beta_frequensyList)
    # div = alfa / beta

    # ДЛЯ ПОСТРОЕНИЯ  ГРАФИКА ЧАСТОТНОЙ ХАРАКТЕРИСТИКИ ФИЛЬТРА
    b, a = butter_bandpass(f_alfa, f_beta, fs, order=9)
    w, h = freqz(b, a, worN=2000)

    # ГРАФИКИ
    # fig, sbplt = plt.subplots(3, 2)
    #
    # sbplt[0, 0].plot(t, loadData, 'blue')
    # sbplt[0, 0].set_title('Main signal')
    #
    # sbplt[1, 0].plot(t, filteredSignal, 'green')
    # sbplt[1, 0].set_title('Filtered Signal')
    #
    # sbplt[2, 0].plot((fs * 0.5 / np.pi) * w, abs(h))
    # sbplt[2, 0].plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)])
    # sbplt[2, 0].set_title('Filter frequency response')
    #
    # sbplt[0, 1].plot(f, Amplitude_spector, 'red')
    # sbplt[0, 1].set_title('Main  Amplitude Spector ')
    #
    # sbplt[1, 1].plot(f, Amplitude_filtered_spector, 'black')
    # sbplt[1, 1].set_title('Filtered  Amplitude Spector')
    #
    # sbplt[2, 1].plot(fildered_phase_spector)
    # sbplt[2, 1].set_title('Phase Spector')
    #
    # plt.show()








