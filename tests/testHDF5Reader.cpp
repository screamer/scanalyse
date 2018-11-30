#include "HDF5Reader.h"

#include<iostream>
using namespace std;
int main(int argc, const char ** argv)
{
	int gene_count;
	int cell_count;
	int data_count;
	HDF5reader hr;
	string path = argv[1];
	hr.readHDF5File(path);
	char**a = hr.get_barcodes();
	hr.createCellnameMap();
	int* paraCellVector1=hr.createCellVectorByName(a[0]);
	cout << "first cell" << endl;
	for (int i = 33664; i >= 33653; i--)
	{
		cout << paraCellVector1[i]<<" ";
	}
	cout << endl;
	cout <<"second cell"<< endl;
	int* paraCellVector2 = hr.createCellVectorByName(a[1]);
	cout << paraCellVector2[32919]<<" "<< paraCellVector2[31978] << " " << paraCellVector2[31763] << " " << paraCellVector2[31453] << " " << paraCellVector2[31365] << " " << paraCellVector2[30936] << " " << paraCellVector2[30740] << " " << paraCellVector2[30434] << " " << paraCellVector2[30420] << " " << paraCellVector2[29944];
	cout << endl;
	
	
	/*for (int i = 0; i < 1000; i++)
	{
		cout << paraCellVector1[i]<<" ";
	}*/
	cin.get();
	cin.get();
	return 0;
}