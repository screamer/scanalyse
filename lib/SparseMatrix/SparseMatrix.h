#pragma once
#include <cstring>
#include <stdio.h>
#include <stdlib.h>
#include "H5Cpp.h"
#include<iostream>
#include<unordered_map>
using namespace std;
class SparseMatrix
{
private:
	int *data;
	long long *indptr, *indices;
	char** barcodes;
	char** genes;
	unordered_map<int, string> numToCell;
	unordered_map<string, int> cellToNum;
	int gene_count;
	int cell_count, data_count;

public:
	SparseMatrix() {
	}
	~SparseMatrix()
	{
		
	}
	char** get_barcodes();
	char** get_gene_names();
	char** get_genes();
	long long* get_indices();
	int* get_data();
	int get_cell_count();
	int get_gene_count();
	int get_data_count();
	long long* get_indptr();
	int readHDF5File(string path);
	void createCellnameMap();
	int* createCellVectorByName(string cellname);
	unordered_map<int,int> cellFiltration();
	void write2HDF5(string path);
	void deleteSparseMatrix();
};