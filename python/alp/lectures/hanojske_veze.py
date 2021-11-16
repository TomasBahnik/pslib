# Hanojske veze
import sys

print("Hanojske veze")


def tisk_stav(tyce):
    for i in range(3):
        print("Tyc ", i, " ", tyce[i])


def presun_disk(tyce, odkud, kam):
    print("Presun z tyce ", odkud, " na ", kam)
    assert (len(tyce[kam]) == 0 or tyce[odkud][-1] < tyce[kam][-1])  # kontrola leg�lnosti tahu
    tyce[kam] += [tyce[odkud][-1]]
    tyce[odkud].pop()  # sma� posledn� disk
    tisk_stav(tyce)


def presun_tyc(tyce, kolik, odkud, kam, pomocna):
    if kolik >= 1:
        presun_tyc(tyce, kolik - 1, odkud, pomocna, kam)
        presun_disk(tyce, odkud, kam)
        presun_tyc(tyce, kolik - 1, pomocna, kam, odkud)


def vyres_hanojske_veze(n):
    """ Vyresi Hanojske veze s 'n' disky, ktere presune z tyce 0 na tyc 1 """
    # pocatecni stav disku na tycich, např. [[3,2,1],[],[]]
    # tyče indexujeme 0,1,2
    tyce = [list(range(n, 0, -1)), [], []]
    tisk_stav(tyce)
    presun_tyc(tyce, n, 0, 1, 2)


if __name__ == "__main__":
    vyres_hanojske_veze(3)
    sys.exit(0)
