import re
import os
def task1():
    f = open('D:/words.txt', 'r', encoding = 'utf-8')
    string = f.read()
    f.close()
    text = string.split('\n')
    f = open('D:/adygh.html', 'r', encoding = 'utf-8')
    s = f.read()
    f.close()
    voc = set()
    s = re.sub('[\.,:;"()\-]', ' ', s)
    for word in text:
        
        if ' ' + word + ' ' in s:
            voc.add(word)
    fw = open('D:/wordlist.txt', 'a', encoding = 'utf-8')
    for word in voc:
        fw.write(word + '\n')
    f.close()
def task2():
    os.system("C:\mystem.exe D:/words.txt -nig D:/results.txt")
    f = open('D:/results.txt', 'r', encoding = 'utf-8')
    s = f.read()
    f.close()
    m = set()
    n = set()
    state = s.split('}')
    for el in state:
        if '?=' not in el and '=S' in el and '=A' not in el and 'им,ед' in el:
            elx = re.sub('{.*', ' ', el)
            n.add(el)
            m.add(elx)
    fw = open('D:/rus_nouns.txt', 'w', encoding = 'utf-8')
    for word in m:
        fw.write(word + '\n')
    f.close()
    return n
def task3(n):
    q = set()
    
    fw = open('D:/sql1.txt', 'w', encoding = 'utf-8')
    for word in n:
        regex = '(\w+?){(\w+?)=S'
        a = re.findall(regex, word)
        if a != []:
            
            com = 'INSERT INTO rus_words(wordform, lemma) VALUES(\'' + a[0][0] + ', \'' + a[0][1] + '\');\n'
            if com not in q:
                q.add(com)
                fw.write(com)

        reg = '(\w+?){.+?\|(\w+?)=S'
        a = re.findall(reg, word)
        if a != []:
            
            com = 'INSERT INTO rus_words(wordform, lemma) VALUES(\'' + a[0][0] + ', \'' + a[0][1] + '\');\n'
            if com not in q:
                q.add(com)
                fw.write(com)
    fw.close()
def main():
    task1()
    task3(task2())
if __name__ == '__main__':
    main()
    
