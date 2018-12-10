#include <iostream>
#include <math.h>
using namespace std;
/*
 * Provovadi vypocet parametru v obvodu realne civky se 
 * zdrojem stridaveho napeti.
 * 
 * Na zaklade zadanych hodnot napeti, proudu, frekvence a 
 * vnitrniho odporu civky urci fazovy posuv mezi napetim a proudem
 * a cinny, jalovy a zdanlivy vykon
 */

int main(int argc, char** argv) 
{ 
	double napeti, proud, frekvence, odpor, indukcnost, Pi;
	napeti=220; //napeti ve V
	proud=1.8; //proud v A
	frekvence=50; //frekvence v Hz
	odpor=28; //odpor v ohmech
	Pi=3.14;
	cout<<"napeti="<<napeti<<" V"<<endl;
	cout<<"proud="<<proud<<endl;
	cout<<"frekvence="<<frekvence<<endl;
	cout<<"odpor="<<odpor<<endl;
	cout<< "---------------------------------------------------------------------------\n";
	
	
	double impedance=napeti/proud;
	
	double induktance=sqrt(impedance*impedance-odpor*odpor);
	
	cout<<"induktance="<<induktance<<" ohm [sqrt(impedance*impedance-odpor*odpor)]\n";
	cout<<"impedance="<<impedance<<" ohm (napeti/proud) \n";
	cout<<"indukcnost="<<induktance/(2*M_PI*frekvence)<<" H\n";
	cout<<"tg fi="<<induktance/odpor<<"\n";
	
	// fazovy posun v radianech 
	double fi_rad = atan(induktance/odpor);
	cout<<"fi="<<fi_rad<<" rad\n";
	// fazovy posun ve stupnich
	cout<<"fi="<<fi_rad*(180/M_PI)<<" stupnu\n";
	
	double cinny_vykon = napeti*proud*cos(fi_rad);
	double jalovy_vykon = napeti*proud*sin(fi_rad);
	
	printf ("cinny vykon = %fW, jalovy vykon = %fW\n\n", cinny_vykon, jalovy_vykon);
	printf("Kontrola vypoctu cinneho a jaloveho vykonu\n");
	printf ("sqrt(cinny_vykon^2 + jalovy_vykon^2) = %fW, zdanlivy vykon %fW\n", sqrt(pow(cinny_vykon,2) + pow(jalovy_vykon,2)), napeti*proud);
	
	return 0;
}
