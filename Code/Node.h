#ifndef __NODE_H__
#define __NODE_H__

#include<set>

class Node {

private: 
	int position;

public:
	Node(int position, int adjacentNote);
	~Node();
	set<int> getAdjacentNodes();
	bool isConnected(int node);
};


#endif // !__NODE_H__
