#coding: UTF-8
#Les consignes pour le devoir: https://github.com/jhroy/syllabus-edm5240-H2017/blob/master/devoir2.md

#Ce module nous permet d'importer les modules csv afin de faire ce devoir
import csv

#Ce module va permettre d'utiliser les expressions régulières dans la troisième partie du devoir
import re

#Trouver sur le site stackoverflow, cette manipulation permet la traduction des chiffres romains en chiffres entiers (Merci Shannon)
def rom_to_int(value):
    s = 0;
    a = dict();
    b = dict();
    r = value;
    
    a['CM'] = 900;
    a['IX'] = 9;
    a['IV'] = 4;
    a['XL'] = 40;
    a['CD'] = 400;
    a['XC'] = 90;
    
    b['M'] = 1000;
    b['C'] = 100;
    b['D'] = 500;
    b['X'] = 10;
    b['V'] = 5;
    b['L'] = 50;
    b['I'] = 1;

#Selon les tests, ce qui suit fonctionne, mais le raisonnement ne m'est pas entièrement familier. Si je comprends, on retire les cas difficiles avec les 4 et les 9 pour ensuite prendre les nombres romains d'un seul caractère, avant d'ajouter à nouveau à la solution finale ce qui avait été retiré précédement.     
#La manipulation suivante permet de règler le problème des 4 et des 9    
    for key in a:
            if key in r: 
                r = re.sub(key,'',r)
                s+=a[key];

#La suite des chiffres romains
    for key in b:
             s+= r.count(key) * b[key];
#Ici, nous aurons le nombre entier
    return s 

#Importer et lier le document concordia1.csv à mon script
fichier='concordia1.csv'
concordia=open(fichier)

lignes=csv.reader(concordia)
#Cette commande va permettre de sauter la première ligne avec les titres dans le document csv
next(lignes)

#Ici, nous plaçons les certaines informations importantes pour le print final
titre=[]
nom=[]
prenom=[]

#Nous disons où trouver les bonnes informations dans le fichier concordia
for ligne in lignes:
    titre.append(ligne[2])
    nom.append(ligne[0])
    prenom.append(ligne[1])

#Ce dispositif permet de remonter les listes après en avoir terminé une (Merci Shannon)
concordia.seek(0)
next(lignes)

#Question 1: Long titre

#Ouvrir une liste pour la longueur les titres
longTitre=list()

#On prend chacun des éléments afin d'ajouter la longueur en caractère des titres dans la liste
for ligne in lignes:
    longTitre.append(len(ligne[2]))
    # print(longTitre)

#réinitialisation
concordia.seek(0)
next(lignes)

#Question 2: Maitrise ou Doctorat

#La variable (ou plutôt la liste) s'appelle moud, car il est impossible de l'appeler type dans Python, car cela correspond à quelque chose d'autre
moud=list()

for ligne in lignes:

#Puisqu'il y a plusieurs façons d'écrire doctorat dans le csv, il faut plusieurs filtres afin de regrouper tous les doctorats sous le mot Doctorat
    if 'D' in ligne[6]:
        moud.append('Doctorat')
    elif 'PhD' in ligne[6]:
        moud.append('Doctorat')
    elif 'Ph.D' in ligne[6]:
        moud.append('Doctorat')

#Cette commande permet d'identifier les maîtrises
    elif 'M' in ligne[6]:
        moud.append('Maîtrise')

#Cette manipulation est une mesure de sécurité au cas où une ligne ne s'identifie pas à Doctorat ou Maîtrise
#Dans ce cas, nous pourrons manuellement aller voir où se trouve le problème
    else:
        print(ligne)
        moud.append('WTF')
# print(moud)

#réinitialisation
concordia.seek(0)
next(lignes)

#Question 3: Nombre de pages
#Je tiens absolument à remercier Shannon qui a été d'une très grande aide pour cette partie

#Création d'une nouvelle liste
nbPages=list()

#On dit au script où aller chercher l'information
for ligne in lignes:
    n=ligne[5]
    
#On va devoir commencer par séparer en deux la ligne qui contient le nombre de pages
#Nous allons pouvoir couper les informations avec l'expression suivante, en retirant autour de: (Leaves),(p.),(l.),(:)
    autourdeLeaves=re.split("leaves|p\.|l\.|:", n)

#Maintenant que nous avons séparé le nombre de pages (romain et numérique) du reste de la ligne, nous allons pouvoir travailler avec les chiffres des nombres de pages
    brutPages=autourdeLeaves[0]
#Ici, on sépare les nombres romains et les nombres de part et d'autres de la virgule
    netPages=brutPages.split(",")
    
#À partir d'ici, on s'occupe du cas des chiffres romains qu'il va falloir convertir afin de les additioner avec le nombre de pages numériques
    if len(netPages)==2:
        traduit=rom_to_int(netPages[0])
#Avec la manipulation précédente que nous avions utilisé au début du script, nous pouvons traduire les chiffres romains
        
#Le strip ici suivant nous permet d'enlever les espaces vides qui ne servent à rien
        netPagessansesp=netPages[1].strip()
        
#La prochaine manipulation nous permet de repérer que les chiffres
        if netPagessansesp.isdigit() is False:
#Ce dispositif est utilisé par mesure de sécurité (s'il y a d'autres choses que des chiffres). S'il ne respecte pas les conditions établies plus haut, on ne le traitera pas (Merci Shannon)
            nbPages.append("### (Non Valide parce que : {})".format(n))
#Certaines lignes ont un nombre de pages difficile à établir. Dans certains cas, on ne pourra pas les traiter et il sera écrit 'non valide'
        
#Ici, on ajoute le nombre de pages en chiffre romain nouvellement traduit avec les autres pages    
        else:
            nbrPages=int(netPagessansesp)
            total=traduit+nbrPages
            nbPages.append(total)

#Ici, on s'occupe des cas où il n'y a pas de chiffres romains (seulement des nombres de pages déjà en chiffre)       
    elif len(netPages)==1:
        netPagessansesp=netPages[0].strip()
        if netPagessansesp.isdigit() is False:
            nbPages.append("### (Non Valide parce que : {})".format(n))
#Certaines lignes ont un nombre de pages difficile à établir. Dans certains cas, on ne pourra pas les traiter et il sera écrit 'non valide'
        
        else:
            nbrPages=int(netPagessansesp)
            nbPages.append(nbrPages)
# print(nbPages)


#réinitialisation
concordia.seek(0)
next(lignes)

# for ligne in lignes:
#    print("La {papier} de {prénom} {nom} compte {nbpages} de pages. Son titre est {titre} ({lentitre} de caratères).\n####################################".format({papier,moud},{nom,ligne[0]},{prénom,ligne[1]},{nbpages,"nbpages"},{titre,ligne[3]},{lentitre,longTitre}))

#Dans le print final, on regroupe les informations nécessaires ensemble afin d'associer les bons titres aux bonnes personnes
#Les currents vont prendre les donnés ligne par ligne afin de former la phrase déterminer par le print
#Dans le format, on place dans l'ordre les currents dans l'ordre qu'on les veut
for index in range(len(longTitre)):
    currentlongTitre = longTitre[index]
    currentType = moud[index]
    currentnbPages = nbPages[index]
    currentTitre = titre[index]
    currentNom = nom[index]
    currentPrenom = prenom[index]
    print("Le papier de {} de {} {}, appelé «{}» ({} caractères), possède {} pages.".format(currentType, currentPrenom, currentNom, currentTitre, currentlongTitre, currentnbPages ))

#Maintenant que ce long script est enfin terminé, il est temps de dormir et de réviser pour les autres examens ;)
#Merci beaucoup à Shannon, sans elle ce devoir n'aurait jamais connu une fin
#Bye
