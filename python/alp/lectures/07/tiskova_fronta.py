# Příklad na použití fronty - rozpočítávadlo.
#
#
# Jan Kybic, 2016

from knuthqueue import Queue
import random

class Uloha:
  def __init__(self,t,s):
    self.time=t   # čas vytvoření
    self.stran=s  # počet stran

class Tiskarna:
  def __init__(self):
    self.uloha=None
    self.zbyvajici_cas=0
    
def simuluj(num_people,prob_second,max_pages,seconds_per_page,simulation_time):
  """ Nasimuluje chování tiskové fronty.
       "num_people" - počet lidí
       "prob_second" - pravděpodobnost vytvoření tiskové úlohy v konkrétní vteřině
       "max_pages"  - maximální počet stran v úloze
       "seconds_per_page" - počet sekund na stránku 
       "simulation_time" - délka simulace v sekundách """
  q=Queue()      # tisková fronta
  t=Tiskarna()   # stav tiskárny
  casy_cekani=[] # délky čekání na vytisknutí v sekundách
  for i in range(simulation_time):
    simuluj_lidi(num_people,prob_second,max_pages,q,i)
    simuluj_tiskarnu(seconds_per_page,q,t,i,casy_cekani)
  avg_time=sum(casy_cekani)/len(casy_cekani)
  print("Průměrná doba čekání  %5.2fs." % avg_time)
  return avg_time

def simuluj_lidi(num_people,prob_second,max_pages,q,i):
  for j in range(num_people):  
    if random.random()<prob_second:
      pocet_stran=random.randrange(1,max_pages+1)
      print("Čas %d, požadavek na tisk %d stran." % (i,pocet_stran))
      q.enqueue(Uloha(i,pocet_stran))

def simuluj_tiskarnu(seconds_per_page,q,t,i,casy_cekani):
  if t.uloha!=None:       # tiskárna tiskne
    t.zbyvajici_cas-=1
    if t.zbyvajici_cas<=0: # hotovo
      print("Čas %d, tisk %d stran/y hotov, čekání %5.1fs." % (i,t.uloha.stran,i-t.uloha.time))
      casy_cekani+=[i-t.uloha.time]
      t.uloha=None         
  if t.uloha==None:       # tiskárna je volná
    if not q.is_empty():  # ve frontě je úloha         
       t.uloha=q.dequeue()
       print("Čas %d, začínáme tisknout úlohu mající %d stran." % (i,t.uloha.stran))
       t.zbyvajici_cas=t.uloha.stran*seconds_per_page

               
if __name__=="__main__":
  simuluj(10,1./(60.*60.),10,12,100*60*60)
#  simuluj(10,1./(60.*60.),10,12,100*60*60)
