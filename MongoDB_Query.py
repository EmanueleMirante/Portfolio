from pymongo import MongoClient
from stop_words import get_stop_words
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pprint
plt.style.use('ggplot')

'''


THE GOAL IS TO RESOLVE 9 QUERIES:

Query 1] Number of contents for each author
Query 2] Number of comments for each author
Query 3]Word Cloud  
Query 4]First 5 terms more used for each author
Query 5]First 5 terms more used for each time slot of the day[morning, afternoon,evening, night]
Query 6]Mean number of word in each title
Query 7]Authors with more than 350 comments in alphabetical order 
Query 8]Given as input a term, show the graph related to its usage over time
Query 9] Given as input a time slot, show the tagCloud of the terms used


'''

#Connect to localhost
client=MongoClient()
db=client.HakerNews
collezione=db.HakerNews

#Function for print query
def printQuery(a):
    for i in a:
        print(i)

#[Query 1] Number of contents for each author


nContenuti=collezione.aggregate([{"$group": {'_id': "$Author", 'count': {'$sum': 1}}},{'$sort':{"count":-1}}])
printQuery(nContenuti)


#[Query 2] Number of comments for each author


sCommenti=collezione.aggregate([{"$group":{'_id':'$Author','sum':{'$sum':'$num_comments'}}},{'$sort':{'sum':-1}}])
printQuery(sCommenti)


#[Query 3]Word Cloud  

stop_words = get_stop_words('en')
diz={}

for i in collezione.aggregate([{'$project': {'occorrenze': {'$regexFindAll': {'input': '$Title','regex': r"\w[\w']+"}}}},
      {'$unwind': '$occorrenze'},
      {'$group': {'_id': '$occorrenze.match','Conteggio': {'$sum': 1}}},
      {'$sort': {'Conteggio':-1}}]):
    if i['_id'].lower() not in stop_words:
        diz[i['_id']]=i['Conteggio']

wc = WordCloud(width=500, height=500, background_color='black')
wc.generate_from_frequencies(diz)
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()


#[Query 4]First 5 terms more used for each author


diz={}
stop_words = get_stop_words('en')
for i in collezione.aggregate([ {'$project': {'Author':1,'occorrenze': { '$split': ["$Title", " "] }}},
          {'$unwind': '$occorrenze'},{'$group': {'_id': {'Autore':'$Author','occ':'$occorrenze'},'Conteggio': {'$sum': 1}}},
          {'$sort': {'Conteggio':-1}}]):
    iu = i['_id']
    aut = iu['Autore']
    termine = i['_id']['occ']
    if aut not in diz.keys():
        if termine.lower() not in stop_words:
            lista = []
            diz[aut] = lista
            diz[aut].append(termine)
        else:
            continue
    else:
        if len(diz[aut]) < 5:
            if termine.lower() not in stop_words:
                diz[aut].append(termine)
            else:
                continue
        else:
            continue
pprint.pprint(diz)

#[Query 5]First 5 terms more used for each time slot of the day[morning, afternoon,evening, night]


diz={}
stop_words = get_stop_words('en')
for i in collezione.aggregate([{'$project': {'FasciaOraria':1,'occorrenze': { '$split': ["$Title", " "] }}},
          {'$unwind': '$occorrenze'},{'$group': {'_id': {'Fascia':'$FasciaOraria','occ':'$occorrenze'},'Conteggio': {'$sum': 1}}},
          {'$sort': {'Conteggio':-1}}]):
    iu = i['_id']
    Fascia = iu['Fascia']
    termine = i['_id']['occ']
    if Fascia not in diz.keys():
        if termine.lower() not in stop_words:
            lista = []
            diz[Fascia] = lista
            diz[Fascia].append(termine)
        else:
            continue
    else:
        if len(diz[Fascia]) < 5:
            if termine.lower() not in stop_words:
                diz[Fascia].append(termine)
            else:
                continue
        else:
            continue
pprint.pprint(diz)



#[Query 6]Mean number of word in each title

NTermini=collezione.aggregate([{'$project':{'Title':1,'termini':{'$split': ['$Title',' ']}}},{'$unwind': '$termini'},{'$group':{'_id':'$Title','count':{'$sum':1}}},
                               {'$group':{'_id':0,'NumeroMedioDiParole':{'$avg':'$count'}}}])
printQuery(NTermini)



#[Query 7]Authors with more than 350 comments in alphabetical order 


a350=collezione.aggregate([{'$project':{'Author':1,'num_comments':1}},{'$group':{'_id':'$Author','Ncommenti':{'$sum':'$num_comments'}}},{'$match':{
    'Ncommenti':{'$gt':350}}},{'$sort':{'_id':1}}])
printQuery(a350)


#[Query 8]Given as input a term, show the graph related to its usage over time;


stop_words = get_stop_words('en')

inp=str(input('Scrivi un termine da cercare oppure premi 0 per uscire: '))
while inp != '0':
    if len(inp.split())>1:
        print('Devi cercare una singola parola')
        inp=str(input('Scrivi un termine da cercare oppure premi 0 per uscire: '))
    else:
        if inp.lower() not in stop_words:
            AnnoC = {}
            for i in collezione.aggregate([
              {'$project': {"Anno":{'$year':'$created_date'},'occorrenze': {'$regexFindAll': {'input': '$Title','regex': inp,'options':'i'}}}},
              {'$unwind': '$occorrenze'},
              {'$group': {'_id': {'occ':'$occorrenze.match','Anno':'$Anno'},'Conteggio': {'$sum': 1}}},
              {'$sort': {'_id.Anno':1}}]):
                I = i['_id']
                AnnoC[I['Anno']] = i['Conteggio']
            print(AnnoC)
            if len(AnnoC) == 0:
                print('Termine mai utilizzato')
                pass
            else:
                plt.bar(list(AnnoC.keys()), AnnoC.values(), color='yellow')
                plt.xlabel('Anni')
                plt.ylabel('Conteggio')
                plt.title(inp)
                plt.show(block=False)
                plt.pause(10)
                plt.close()
            inp = str(input('Scrivi un termine da cercare oppure premi 0 per uscire: '))
        else:
            print('Termine mai utilizzato')
            inp = str(input('Scrivi un termine da cercare oppure premi 0 per uscire: '))
print('bye bye')


#[Query 9] Given as input a time slot, show the tagCloud of the terms used


stop_words = get_stop_words('en')
fascia=input('Inserisci una fascia giornaliera(mattina,pomeriggio,sera,notte) Oppure premi 0 per uscire: ')
while fascia != '0':
    if fascia.lower() not in ('mattina', 'pomeriggio', 'sera', 'notte'):
        print('Fascia giornaliera non presente')
        fascia = input('Inserisci una fascia giornaliera(mattina,pomeriggio,sera,notte) Oppure premi 0 per uscire: ')
    else:
        diz = {}
        for i in collezione.aggregate([ {'$match':{'FasciaOraria':fascia.lower()}},{'$project': {'FasciaOraria':1,'occorrenze': {'$split': ["$Title", " "]}}},
                  {'$unwind': '$occorrenze'},
                  {'$group': {'_id': '$occorrenze','Conteggio': {'$sum': 1}}},
                  {'$sort': {'Conteggio':-1}}]):
            if i['_id'].lower() not in stop_words:
                diz[i['_id']] = i['Conteggio']
                pass
        wc = WordCloud(width=500, height=500, background_color='black')
        wc.generate_from_frequencies(diz)
        plt.imshow(wc, interpolation="bilinear")
        plt.title(fascia)
        plt.pause(10)     
        plt.close()
        fascia = input('Inserisci una fascia giornaliera (mattina,pomeriggio,sera,notte) Oppure premi 0 per uscire: ')
print('bye bye')



