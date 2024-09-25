#CHEAT SHEET

#SEZNAMI IN NIZI
sez = [7, 3, 1, 2, 6, 8]
print(sez[2])
print(sez[-2])
print(sez[2: :2])
print(sez[2:5:2])               #od 2 do 5 s korakom 2
print(sez[2:])

sez1 = [1, 2, 3]
sez2 = [3, 4 ,5]
print(sez1 + sez2)
print(sez1, sez2)
print(list(zip(sez1, sez2)))    #nabere istoležne elemente, spredi mors dat list
print(7 in sez1)                #vrne True ali False, če vsebuje element

#spreminjanje vrednosti
sez1[2] = "Ladja"
print(sez1)
del sez2[0]
print(sez2)

#spreminjanje vrednosti v nizu
niz = "abcdef"
niz = niz[:3] + "ž" + niz[4:]
print(niz)

#sprehod skozi sezname
s = [1, 2 ,4, 7, 8, 9, 3, 6, 5, 9]
for element in s:
    print(element)
print(len(s))                   #nam da 10(zacne steti z 1 ne z 0)
print(list(enumerate(s)))       #urejeni pari, prva cifra indeks, druga vrednost na tem indeksu
for i in range(len(s) + 1):         
    print(i)

#obračanje seznama
s[::-1]

#split seznama
sz = [1, 4, 6, 7, 8, 8]
print(sz[:3], sz[3:])

#podseznam
ss = [[1, 2, 3], [4, 5, 9], [7, 8, 7]]
print(ss[2])                   #sprinta cel podseznam na indeksu 2
for podseznam in ss:
    print(podseznam[1])        #sprinta vse elemente podseznamov na indeksu 1
    print(max(podseznam))      #sprinta najvecje vrednosti iz vsakega podseznama posebej
    for element in podseznam:
        print(element)         #sprinta vse elemente
print(max(ss))                 #sprinta najvecji podseznam

#metode za nize
niz = "!!,.56282anDIa!:::"
print(niz.count("!"))
print(niz.index("a"))          #kje se znak pojavi prvič
print(niz.replace("!", "ž"))
print(niz.lower())
print(niz.upper())
print(niz.islower())           #vrneta True, False, če so vsi elementi z malo ali veliko
print(niz.isupper())
n = "  adad    d j  \n "       #vse nepotrebne presledke na koncu, \n, in tab pobrise 
print(n.strip())
print(" ".join(["Jaz", "sem", "zelo", "vesel"]))
print("".join(["Jaz", "sem", "zelo", "vesel"]))
print("!!!".join(["Jaz", "sem", "zelo", "vesel"]))
niz1 = "abc,de, fghj,cikcl"
print(niz1.split(","))
print(niz1.split())
i = niz1.find("c")            #najde prvi c
j = niz1.find("c", i + 1)     #najde nasledni c
print(i)
print(j)

sez = []
if not sez:                   #vrne True, ce je seznam prazen, False ce ni prazen
    print(sez)                 
                
#metode za sezname
sez = [8, 3, 1, 7, 8, 4, 2, 1]
nov_sez = sez[:]              #kopija seznama
sez.append(9)                 #doda na konec seznama
print(sez) 
sez.extend(["žaba", "če"])    #naredi sez1 + sez2
print(sez)                    
sez.insert(3, "hehe")         #na mesto z indeksom 3 vstavi element
print(sez)
sez.pop()                     #odstrani zadnji element in ga vrne
sez.pop(5)                    #odstrani element na indeksu 5 in ga vrne
sez.index(4)
sez.count(1)

sez1 = [8, 7, 2, 5, 2, 9, 1]
sez2 = ["D", "f", "E", "a", "A"]
sez1.sort()                   #uredi narascajoce
print(sez1)
sez2.sort()                   #po abecedi, prvo velke crke, pol male
print(sez2)
sez1.sort(reverse=False)      #uredi narascajoce
print(sez1)
sez1.sort(reverse=True)       #uredi padajoce
print(sez1)
sez2.sort(reverse=True)       #po abecedi v obratnem redu, prvo male crke od zadi, pol velike
print(sez2)

def sortirna(element):
    return element[2]
studenti_niz = [("John", "A", 15), ("Jane", "B", 12), ("Dave", "B", 10)]
print(sorted(studenti_niz, key=sortirna))

def sortirna1(element):
    return -element[2]       #minus pred element[2], nam uredi padajoce po drugem elementu(po tockah)
studenti_niz = [("John", "A", 15), ("Jane", "B", 12), ("Dave", "B", 12)]
print(sorted(studenti_niz, key=sortirna1))

studenti_niz = [("John", "A", 15), ("Jane", "B", 12), ("Dave", "B", 12)]
for x in studenti_niz:
    studenti_niz.sort(key = lambda x: (-x[2], x[0]))         #uredi padajoce po tockah, ce mata dva isto tock, uredi po imenih po abecedi
print(studenti_niz)

#NABORI
sadje = ["jabolko", "banana", "češnje"]
zeleno, rumeno, rdece = sadje
print(rdece, rumeno, zeleno)

#MNOŽICE
mnozica = set()
mnozica.add(3)
print(mnozica)
mnozica.add((5, 6, 7))
print(mnozica)
mnozica.add("žaba")
print(mnozica)

m = {1, 2, 3, 4, 5}
m.remove(2)
print(m)
m.discard(4)                #discard in remove nrdita isto
print(m)
m.pop()                     #pop odstrani prvi element in ga vrne, nemors nc v pop(napisat)
print(m)

mn1 = {3, 4, 5}
mn2 = {4, 6, 8}
print(mn1|mn2)              # | unija
print(mn1&mn2)              # & presek

#PRETVARJANJE MED TIPI
a = 13.21
print(int(a))               #vrne celo stevilo
print(float(a))             #vrne decimalno stevilo, ce mas 13 vrne 13.0

b = [1, 2, 3]
str(b)                      #niz
list(b)                     #seznam
print(tuple(b))             #nabor
print(set(b))               #mnozica

#SLOVARJI
s = {'a' : 6, 'b' : 'test', 123 : True}
print(s['b'])
print(s.get('a'))
print(s['ž'])               #ključ ne obstaja, dobimo key error
print(s.get('ž'))           #ključ ne obstaja, vrne none

#spreminjanje
s = {'a' : 6, 'b' : 'test', 123 : True}
s['b'] = 12                 #vrednost s ključem b spremeni v 12
print(s)
s['krava'] = 'zrezek'       #če ni ključa krava, ga doda v slovar in mu pripiše vrednost ki smo jo podali
print(s)
del s["a"]                  #zbrise kljuc in vrednost
print(s)

#metode za slovarje
s1 = {1 : 'a', 2 : 'b', 3 : 'c'}
s2 = {4 : 'd', 5 : 'e', 6 : 'f'}
print(s1.get(1))
print(s1.get(9, "ž"))      #ključ ne obstaja, vrne vrednosti ki smo jo napisali
print(s2.pop(5))           #odstrani par s ključem in vrne vrednost

s3 = {'mama' : 'torta', 'oče': 'sladoled', 'sestra': 'mafin'}
s4 = {'mama' : 'piškoti', 'stric' : 'sladoled', 'brat' : 'pivo'}
s3.update(s4) 
print(s3)                  #če se dvakrat pojavi isti ključ, prevlada tisti ki je v slovarju v oklepaju (s čimer updejtamo), dvakrat se lahko pojavi ista vrednost in nič ne spremeni
print(s4.values())         
print(s4.keys())
print(s4.items())          #vrne nabore ključev in vrednosti
print(list(s4.items()))    #vse 3 metode (keys, values, items) moramo pretvort v drugo obliko ponavadi, npr. list

slovar = {'tok_masa' : [[1, 2, 3], [4, 5, 6]]}
print(slovar.get('tok_masa')[0])

#zanke pri slovarjih
slovar = {'mama' : [0,1,2], 'oče': 'sladoled', 'sestra': 'mafin'}
for vrednosti in slovar.values():
    print(vrednosti)
for kljuci in slovar.keys():
    print(kljuci)
for kljuci in slovar:          #kljuci lahko pises brez .keys()
    print(kljuci)
for kljuci, vrednosti in slovar.items():
    print(kljuci, vrednosti)   #lahko obrnes kljuci, vrednosti in ti sprinta v drgacnem redu
for kljuci, vrednosti in slovar.items():
    print(kljuci, "--->", vrednosti)

#iz seznama v slovar
seznam = [('Audi', 200), ('Volvo', 150), ('Nissan', 100)]
slovar = {}
for ime, cena in seznam:
    slovar[ime] = cena         #slovar[kljuc] = vrednost
print(slovar)

#podslovarji (za vrednost imajo slovar, v tem slovarju lahko še kej)
slovar_piv = {'Slovenija' : {'Union' : (1.5, 5.0), 'Laško' : (1.7, 4.8)}, 'Češka' : {'Staropramen' : (2.0, 5.5), 'Kozel' : (1.8, 5.2)}}
sez = []
for drzava in slovar_piv:
    #print(drzava)
    for ime in slovar_piv[drzava]:                                #ce das samo for ime in drzava, ti sprinta drzavo crko pod crko in ne imena piva
        #print(ime)
        cena = slovar_piv[drzava][ime][0]       
        alko = slovar_piv[drzava][ime][1]
        sez.append((ime, drzava, alko, cena))
        #print(sez)
sez.sort(key=lambda sez: (-sez[3], sez[0], sez[2], sez[1]))       #prvo uredi po cenah padajoce, ce je iste cene po imenu, isto ime po alko in isto alko po drzavi. NE SPREMENI VRSTNEGA REDA ZAPISA V SEZNAMU,
print(sez)                                                        #vrstni red ostane isto kot smo dobili pri sez.append((ime, drzava, alko, cena))



#NUMPYYYYY :(
import numpy as np

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
print(a)
print(a.shape)                  #vrne oblike (2, 4) oz. (vrstice, stolpci)
print(a.ndim)                   #vrne dimenzijo, v našem primeru je 2, če mamo 1 [] je 1, če mamo 2[[]] je dva, če mamo 3 [[[]]] je 3....
print(a.size)                   #vrne velikost, koliko je vseh elementov not

import numpy as np
A = ((np.ones((5, 5)) * np.arange(1, 6)))        #množi po vrsticah od 1 do 6
B = ((np.ones((5, 5)) * np.arange(1, 6)).T)      #obrne prejšnjo
print(A)
print(B)
A[1:4, 1:4] = 0                                  #tabelo lahko "polniš" z elementi kot je 0
print(A)

import numpy as np
sez1 = [1, 2 ,3]
sez2 = [3, 4, 6]
print(np.concatenate((sez1, sez2)))

print(np.zeros((2, 5, 4)))       #2 nivoja, 5x4 tabel, 5 vrstic, 4 stolpci
print(np.ones((2,2)))
print(np.linspace(1, 10, 10))    #koliko delilnih tock
print(np.arange(1, 11, 1))       #s kolikšnim korakom

print(np.fromfunction(lambda i, j : i + j, (5, 5)))      #vsota indeksov, fromfunction uporabi podano funkcijo na celi tabeli, zraven podas se obliko (dim1, dim2)
print(np.fromfunction(lambda i, j: i, (5,5)))

a = np.array([[1, 2, 3, 4, 5], [5, 6, 7, 8, 3]])         #mora bit isto število elementov v arrayu ki ga sprejme in pri reshape
print(a.reshape(5, 2))

#uporabne funkcije
a = np.array([[1, 2, 3, 4, 5], [5, 6, 7, 8, 3]]) 
print(np.any(a) < 4)
print(np.all(a) > 2)
print(a.T)                         #a.T zamenja stolpce in vrstice (zrcali nam tabelo po diagonali)
print(a.flatten())                 #vrne flat tabelo a

b = np.array([1, 5, 0, 6, 3, 0])
c = np.array([2, 1, 5 ,7, 0, 1])
print(np.nonzero(b))               #indeksi neničelnih elementov
print(np.flatnonzero(c > b))       #indeksi kjer je c>b
print(np.where(b > c, b, c))       #np.where(pogoj, x, y) kjer je pogoj izpolnjen nam da x, drugje nam da y

print(b[0:, np.newaxis])           #iz vrstice v stolpce
 
#matematika
a = np.array([[1, 2, 3, 4, 5], [5, 6, 7, 8, 9]])
print(np.maximum(a))
print(np.minimum(a))
print(np.sum(a))                   #vrne vsoto vseh elementov
print(np.cumsum(a))                #vrne nov array, elementi so zaporedne vsote elemtov iz prvotnega arraya
print(np.prod(a))                  #zmnožek vseh elementov med sabo
print(np.prod(a, axis=0))          #množi po stoplcih 
print(np.prod(a, axis=1))          #množi po vrsticah
print(np.log(a))
print(np.exp(a))
print(np.average(a))               #povprecna vrednost elementov iz arraya

A = np.array([3, 4, 5, 6])
print(np.pad(A, (2, 2)))           #nam obloži tabelo iz obeh strani s tolko nulami, kokr napišemo (2,2)
print(np.pad(A, (1,1), "minimum")) #nam obloži tabelo z minimumom/maksimumom tabele
print(np.roll(A, 2))               #prestavi tabelo v desno ali levo(-)
print(np.roll(A, -1))
#povprečna vrednost
B = np.array([1, 3, 666, 5, 666, 10])
C = np.where(B == 666, (np.roll(B, 1) + np.roll(B, -1)) / 2, B)
print(C)

#rezine
tabela = np.arange(0, 49, 1).reshape(7,7)
print(tabela)
razrezano = tabela[0:4, 2:7:2]     #tabela, vrstice od indeksa 0 do 4, elementi v prvi vrstici od 2 do 7 s korakom 2, vse vrstice naprej se polnijo s korakom 2
print(razrezano)


#DATOTEKE
with open("vhodna", "r", encoding="utf-8") as f_r:
    besedilo = f_r.read()
with open("izhodna", "w", encoding="utf-8") as f_w:
    besedilo = f_w.write(besedilo)

#pregled cez vrstice
sez = []
for vrstica in besedilo:
    sez.append(vrstica.strip())

#zapis v izhodno datoteko
niz = "Matej, Lena, Mojca"
imena = niz.split(",")
for ime in imena:
    print(ime, str(imena.count(ime)))                 
    #print(ime, str(imena.count(ime)), file = f, sep = " ")     #ko zapisuješ v datoteko


