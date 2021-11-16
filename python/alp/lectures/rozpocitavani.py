# Příklad na použití fronty - rozpočítávadlo.
#
# Děti v kruhu, rozpočítávadlo má $m$ slabik, začíná se prvním.
# Na koho padne poslední slabika, vypadává.
# Hraje se, dokud nevypadne poslední.
# Děti reprezentujeme pomocí fronty, budeme přesouvat ze začátku na konec.
#
# Jan Kybic, 2016

from knuthqueue import Queue

def rozpocitej(jmena,m):
  q=Queue()
  for j in jmena:   # ulož jména do fronty
    q.enqueue(j)
  while q.size()>1:
    for i in range(m-1):
      q.enqueue(q.dequeue())
    print("Vypadl(a): ",q.dequeue())

  return q.dequeue()  # vrať vítěze

if __name__=="__main__":
  v=rozpocitej(["Adam","Bára","Cyril","David","Emma","Franta","Gábina"],3)  
  print("Vyhrál(a): ",v)
