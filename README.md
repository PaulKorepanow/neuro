# neuro
Work_prototipe.py 

  СКРИПТ ВЫПОЛНЯЕТ ЦИФРОВУЮ ОБРАБУТКУ СИГНАЛА
  И СРАВНИВАЕТ ПО ЗАДАННЫМ КРИТЕРИЯМ ДВЕ ПОЛОСЫ ЧАСТОТ
  (КРИТЕРИИ НАДО ИСПРАИТЬ, СКО НЕПОДХОДИТ)
  ПОЛСЕ ЭТОГО СКРИПТ СОХРАНЯЕТ ПОЛУЧЕННЫЕ ДАННЫЕ В ВИДЕ PANDAS DATAFRAME.
  ВЫЧИСЛЕНИЯ И ЗАПИСЬ В ФРЭЙМ ПРОИСХОДЯТ АВТОМАТИЧЕСКИ
  ПООЧЕРЁДНО ДЛЯ ВСЕХ ФАЙЛОВ В УКАЗАННЫХ НИЖЕ ПУТЯХ.
  
 test_filtr.py
 
     СРАВНЕНИЕ ДИАПАЗОНОВ:
     ДАННЫЕ ПРЕДСТАВЛЕННЫ В ВИДЕ МАССИВА NUMPY
     ПРОВЕРЯЕМ, ВХОДИТ ЛИ ЧАСТОТА В ЗАДАННЫЙ ДИАПАЗОН
     ЕСЛИ ВХОДИТ, ТО СООТВЕТСВУЮЩЕЕ ЭТОЙ ЧАСТОТЕ ЗНАЧЕНИЕ АМПЛИТУДНОГО СПЕКТРА
     ДОБАВЛЯЕМ В СПИСОК _frequensyList
     ПОСЛЕ ЗАВЕРШЕНИЯ ЦИКЛА ВЫЧИСЛЯЕМ СКО ИМЕЮЩИХСЯ СПИСКОВ И РЕЗУЛЬТАТЫ ДЕЛИМ ДРУГ НА ДРУГА
     ДАННЫЙ МЕТОД НЕКОРРЕКТНЫЙ, СРАВНИВАТЬ ДИАПАЗОНЫ НАДО ПО ДРУГИМ КРИТЕРИЯМ
