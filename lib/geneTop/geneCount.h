#ifndef GENECOUNT
#define GENECOUNT
#include<string>
using namespace std;
class geneCount {
	string geneName;
	int count=0;
public:
	void setGeneName(string geneName);
	void setCount(int count);

	string getGeneName(); 
	int getCount();
	void countAdd(int num);
	bool operator < (const geneCount &x)const;

};
#endif // !GENECOUNT

