import urllib.request
import re
import json


def downloading_posts():
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-128254611&count=100')#скачиваем посты из группы
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    post = json.loads(result)
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-128254611&count=100&offset=50')
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    post1 = json.loads(result)
    post1["response"].pop(0)
    post["response"].extend(post1["response"])
    fw = open('D:/posts.txt', 'a', encoding = 'utf-8')
    
    md_lst = [] #массив с средней длинной коммента для поста
    nm_lst = []#массив с длиной поста
    d_age = {} #словарь, у которого ключи - возраста, а значения - общее количество слов текстов
    d_age_n = {} #словарь, у которого ключи - возраста, а значения - количество самих текстов 
    d_city = {} #аналогичные словари для городов; вместе они доносят информацию о среднем количестве слов на один текст
    d_city_n = {}
   
    for i in range(len(post["response"])-1):
        i = i + 1
        text = post["response"][i]["text"] #читаем текст
        ident = post["response"][i]["id"] #находим id записи
        author = post["response"][i]["from_id"] #находим id автора поста
        old = age(author) #выясняем возраст автора
        town = city(author) #выясняем город автора
        nm = how_many_words(text) #считаем, сколько в тексте слов
        if old not in d_age: #наполняем словари 
            d_age[old] = nm
            d_age_n[old] = 0
        else:
            d_age[old] = d_age[old] + nm
            d_age_n[old] += 1
        if town not in d_city:
            d_city[town] = nm
            d_city_n[town] = 0
        else:
            d_city[town] = d_city[town]+ nm
            d_city_n[town] += 1
        md, d_age, dage_n = downloading_comments(ident, d_age, d_age_n, d_city, d_city_n) #
        md_lst.append(md)
        nm_lst.append(nm)

        fw.write('ПОСТ ' + str(i) + '\n' + post["response"][i]["text"] +'\n' + 'Количество слов: ' + str(nm) + '\n')
    fw.close()
    plt.bar(nm_lst, md_lst)
    plt.title('Зависимость средней длины комментария от длины поста')
    plt.ylabel('Средняя длина комментария')
    plt.xlabel('Длина текста')
    plt.show()
    
    dict_graph(d_age, d_age_n,True)
    dict_graph(d_city, d_city_n, False)
    
def how_many_words(text):
    tlist = text.split()
    nmb = len(tlist)
    return nmb
def downloading_comments(x, d_age, d_age_n, d_city, d_city_n):
    req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-128254611&post_id='+ str(x) +'&count=100') 
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    post = json.loads(result)
    req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-128254611&post_id='+ str(x) +'&count=100&offset=50') 
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    post1 = json.loads(result)
    post1["response"].pop(0)
    post["response"].extend(post1["response"])
    fw = open('D:/comments.txt', 'a', encoding = 'utf-8')
    
    k = 0
    summa = 0
    for i in range(len(post["response"])-1):
        i = i + 1
        text = post["response"][i]["text"]
        nm = how_many_words(text)
        author = post["response"][i]["from_id"]
            
        old = age(author)
        town = city(author)
        if old not in d_age:
            d_age[old] = nm
            d_age_n[old] = 0
        else:
            d_age[old] = d_age[old] + nm
            d_age_n[old] += 1
        k = k+1
        if town not in d_city:
            d_city[town] = nm
            d_city_n[town] = 0
        else:
            d_city[town] = d_city[town]+ nm
            d_city_n[town] += 1            
        summa = summa + nm
        fw.write('Комментарий ' + str(i) + '\n' + post["response"][i]["text"] +'\n' + 'Количество слов: ' + str(nm) + '\n')
        
    if k != 0:
        med = summa/k
    else:
        med = 0
    fw.close()
    return med, d_age, d_age_n

def age(author):
    req = urllib.request.Request('https://api.vk.com/method/users.get?uids=' + str(author) + '&fields=bdate' )
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    a = re.findall('"bdate":"[0-9][0-9]\.[0-9]+\.([0-9][0-9][0-9][0-9])"', result)
    #для упрощения расчётов не будем учитывать дату в рамках года, "омолодим" всех людей, которые уже праздновали день рождения в этом году
    old = 0
    if a != [] :
        old = 2016 - int(a[0])
    return old   
def city(author):
    req = urllib.request.Request('https://api.vk.com/method/users.get?uids=' + str(author) + '&fields=city' )
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    a = re.findall('"city":([0-9]*)', result)
    town = -1
    if a != []:
        town = int(a[0])
    return town
def dict_graph(d, d_n, vex):
    x = []
    y = []
    for key in d.keys():
        if d_n[key] != 0:
            y.append(d[key]/d_n[key])
        else:
            y.append(0)
        x.append(key)
    plt.bar(x, y)
    if vex == True:
        plt.title('Age')
    else:
        plt.title('City')
    plt.ylabel('Средняя длина текста')
    plt.xlabel('Возраст или год')
    plt.show()

downloading_posts()
