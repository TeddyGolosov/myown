from pymystem3 import Mystem
import pymorphy2
from pymorphy2 import MorphAnalyzer
import re
import random
def preparation(morph): #в этой части мы читаем словоформы из списка, анализируем их и делаем словарик, где ключ - это набор неизменяемых признаков, а значение - массив из слов, удовлетворяющих такому требованию
    f = open('D:/lemmas.txt', 'r', encoding = 'utf-8')
    text = f.readlines()[:100000]
    f.close()
    d = {}
    for word in text:
        ana = morph.parse(word.strip('\n'))
        gr = ana[0]
        q = str(gr.tag).split(' ')[0] #сохраняем набор неизменяемых признаков - будущий ключ
        if q not in d:
            d[q] = []
        d[q].append(str(gr.word))
        
        
    return d
def reading(d, morph): #а здесь мы уже обрабатываем введённое предложение (и спрашиваем его)
    ans = ''
    text = input('Доброе время суток! Разрешите поиздеваться над вашим синтаксисом. Введите предложение: ').split(' ')

    for indx in range(len(text)):
        text[indx] = text[indx].strip('.,:;"?!') #очищаем слова от пунктуации
        ana = morph.parse(text[indx]) #проводим морфанализ
        gr = ana[0] #берём самый первый разбор
        q = str(gr.tag).split(' ')[0] 
        
        if q in d and len(str(gr.tag).split(' ')) != 1:
            g = str(gr.tag).split(' ')[1]
            m = set(g.split(','))
            wrd = random.choice(d[q])
            anz = morph.parse(wrd)
            gram = anz[0]
            new = str(gram.inflect(m).word)
            ans = ans + ' ' + new
        elif q in d:
            wrd = random.choice(d[q])
            ans = ans + ' ' + wrd
        else:
            ans = ans + ' ' + text[indx]
    return ans

def main():
    morph = MorphAnalyzer()
    d = preparation(morph)
    while 1:
        print(reading(d, morph))
if __name__ == '__main__':
    main()
