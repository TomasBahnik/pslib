#include <iostream>
#include <math.h>
using namespace std;

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
	cout<<"fi="<<atan(induktance/odpor)<<" rad\n";
	cout<<"fi="<<atan(induktance/odpor)*(180/M_PI)<<" stupnu\n";
	return 0;
}
