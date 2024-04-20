graph = {}
graph["a"] = {}
graph["a"]["fin"] = 1

graph["b"] = {}
graph["b"]["a"] = 3
graph["b"]["fin"] = 5

graph["fin"] = {}

#权重列表
infinity = float("inf")
costs = {}
costs["a"] = 6
costs["b"] = 2
costs["fin"] = infinity
#继承列表
parents = {}
parents["a"] = "start"
parents["b"] = "start"
parents["fin"] = None

procesed = []


def find_lowest_cost_node(costs):
    min_val = infinity
    min_key = None
    for node in costs:
        cost = costs[node]
        if not node in procesed:
            if cost < min_val:
                min_val = cost
                min_key = node
    return min_key
    

if __name__ == "__main__":
    node = find_lowest_cost_node(costs)
    while node is not None:
        cost = costs[node]
        neighbors = graph[node]
        for key in neighbors.keys():
                new_cost = cost + neighbors[key]
                if new_cost < costs[key]: 
                    costs[key] = new_cost
                    parents[key] = node
        procesed.append(node)
        node = find_lowest_cost_node(costs)

print(parents)
print(costs)