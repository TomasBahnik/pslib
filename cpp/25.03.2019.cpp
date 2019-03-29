#include <iostream>
#include <string>
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

/*
 * Pocet studentu ve tride podle zadani
 */
int pocet_studentu(string trida);

/*
 * Maximalni pocet bodu ve tride podle zadani
 */
int max_bodu(string trida);

int main(int argc, char** argv) 
{
	int soucet_znamek_trida=0,pocet_dvojek=0;
	float prumer_znamek=0.0;
	string trida;
	
	cout<<"Zadej tridu (P1,P2,P3,P4) : ";
	cin>>trida;
	cout<<"Pocet studentu ve tride : "<<trida<<" = "<< pocet_studentu(trida)<<"\n";
	cout<<"Maximalni pocet bodu ve tride "<<trida<<" = "<< max_bodu(trida)<<"\n";
	
	for (int student=1; student<=pocet_studentu(trida); student++) {
		int znamka_studenta,pocet_bodu_studenta;
		cout<<"\nZadej body pro "<<student<<". studenta : ";
		cin>>pocet_bodu_studenta;
		//TODO doplnit kontrolu actual<=max_bodu(trida);
		znamka_studenta = znamka(max_bodu(trida),pocet_bodu_studenta);
		if (znamka_studenta == 2) pocet_dvojek += 1;
		cout<<"Znamka "<<student<<". studenta = "<<znamka_studenta<<"\n";
		
		//soucet znamek je pro vypocet prumeru za celou tridu - mimo zadani
		soucet_znamek_trida += znamka_studenta;
		//a = a + b lze zapsat jako a += b (obvykly zpusob)
		//soucet_znamek_trida = soucet_znamek_trida + znamka_studenta;
		//cout<<"Soucet znamek ve tride = "<<soucet_znamek_trida<<"\n";
	}
	cout<<"\nPocet 2 ve tride = "<<pocet_dvojek<<"\n";
	
	//Vypocet prumeru je mimo zadani
	//prumer je desetinne cislo
	prumer_znamek = 1.0*soucet_znamek_trida/pocet_studentu(trida);
	cout<<"Prumer znamek ve tride = "<<trida<<" = "<<prumer_znamek<<"\n";

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
	float percent = 100.0*actual/max;
	//pouze pro odladeni
    //cout << "procenta = "<< percent<<"%\n";
	if (percent > 90) return 1;
	if (percent > 70) return 2;
	if (percent > 50) return 3;
	if (percent > 30) return 4;
	return 5;
}

/*
 * Funkce compare vraci v pripade rovnosti '0'. Nerovnosti bud > 0 beno < 0
 * https://www.geeksforgeeks.org/stdstringcompare-in-c/
 */
int pocet_studentu(string trida) {
	if (trida.compare("P1")==0) return 30;
	if (trida.compare("P2")==0) return 28;
	if (trida.compare("P3")==0) return 28;
	if (trida.compare("P4")==0) return 37;
	return 0;
}

/*
 * Lze zjednosusit kontrolou zda trida obsahuje 1,2,3,4 - funkce `find`
 */
int max_bodu(string trida) {
	if (trida.compare("P1")==0) return 75;
	if (trida.compare("P2")==0) return 120;
	if (trida.compare("P3")==0) return 150;
	if (trida.compare("P4")==0) return 170;
	return 0;
}

