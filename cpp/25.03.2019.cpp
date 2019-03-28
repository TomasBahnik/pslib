#include <iostream>
#include <cmath>
using namespace std;
/* 
 * 1. Ucitel zada na vyzvani do programu maximalni mozny pocet bodu ziskany z testu sve tridy.
 * 2. Nasledne do programu zadava body ziskane n-tym studentem.
 * 3. Program, po zadani ziskanych bodu, zobrazi znamku daneho studenta.
 * 4. Na konci program vypise *pocet dvojkaru* a prumernou znamku cele tridy
 *
 * Znamka za dosazene body v procentech
 * 100-90 : 1
 * 90-70  : 2
 * 70-50  : 3
 * 50-30  : 4
 * 30-0   : 5
 *
 * Pocty zaku ve tridach
 * E1A : 28
 * E1B : 27
 * E1C : 24
 * E2A : 30
 * E2B : 29
 * E3A : 28
 * E3B : 26
 * E4A : 30
 * E4B : 20
 * L1  : 30
 * L2  : 29
 * L3  : 29
 * L4  : 27
 * P1  : 30
 * P2  : 28
 * P3  : 28
 * P4  : 27
 * 
 * Maximalni pocet bodu z testu
 * 1. rocnik : 75
 * 2. rocnik : 120
 * 3. rocnik : 150
 * 4. rocnik : 180
 */

/*
 * deklarace funkce znamka. Tato funkce vypocita znamku na zaklade 
 * maximalniho a skutecne dosazeneho poctu bodu
 * max    : maximalni mozny pocet bodu
 * actual : skutecne dosazeny pocet bodu
 * vraci znamku 1-5 viz komentar.
 */
int znamka(int max, int actual);

int main(int argc, char** argv) 
{
	float max,s1;
	cout<<"Pro tridu P1 zadej maximalni pocet bodu z testu (Maximalne 75)";
	cin>>max;
	cout<<"1.Student:";
	cin>>s1;
    
	cout << znamka(max,s1);

	return 0;
}

/*
 * Implementace funcke znamka
 * Prikaz return ukonci provadeni funkce.
 * Priklad : percent = 35
 *   1. podminka je false -> nevola se return, jde se dal
 *   2. podminka je false -> nevola se return a jde se dal
 *   3. podminka je false -> nevola se return a jde se dal
 *   4. podminka je true -> vola se return a vrati se 4
 *   
 */
int znamka(int max, int actual) {
	int percent = actual*100/max;
    cout << "\nprocenta=";
	cout << percent;
	cout << "%\n";
	if (percent > 90) return 1;
	if (percent > 70) return 2;
	if (percent > 50) return 3;
	if (percent > 30) return 4;
	return 5;
}

