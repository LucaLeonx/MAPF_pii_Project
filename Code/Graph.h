#ifndef __GRAPH_H__
#define __GRAPH_H__

#include <set>
#include <optional>
#include "Node.h"

class Graph
{
public:
	Graph(set<Node> nodeSet);
	~Graph();
	bool isNodePresent(int position);
	option<Node> getNode(int position);
	bool isEdgePresent(int sartNodePosition, int endNode);
};

#endif // !__GRAPH_H__
