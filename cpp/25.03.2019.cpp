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

int main(int argc, char** argv) 
{
	float a,b,c,d,e,f,g,h,i,j,k;
	
	
	cout<<"Pro tridu P1 zadej maximalni pocet bodu z testu (Maximalne 75)";
	cin>>a;
	cout<<"1.Student:";
	cin>>b;
	if(b/a*100>=90) && (b/a*100<=100)
		cout<<"Jednicka";
	else if(b/a*100>=70) && (b/a*100<=70)
		cout<<"Dvojka";
	cout<<"2.Student:";
	cin>>c;	

	cout<<"3.Student:";
	cin>>d;


	cout<<"4.Student:";
	cin>>e;


	cout<<"5.Student:";
	cin>>f;


	cout<<"6.Student:";
	cin>>g;


	cout<<"7.Student:";
	cin>>h;


	cout<<"8.Student:";
	cin>>i;


	cout<<"9.Student:";
	cin>>j;


	cout<<"10.Student:";
	cin>>k;
	
	return 0;
}

