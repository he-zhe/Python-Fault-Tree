import os
import random
import time

from import_tree_from_xml import import_tree_from_xml

start_time = time.time()

MAX_N_RESULT = 5
N_Rep = 10000000

node_dict, leaf_node_dict = import_tree_from_xml(
    os.path.join('example', 'example.xml'))

result = []
root = node_dict['Root']

for i in range(N_Rep):
    #  Throw coin for all leaves
    for leaf in leaf_node_dict:
        # http://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
        leaf_node_dict[leaf].state = bool(random.getrandbits(1))

    # Update the whole tree
    root.update_all_from_leaf()

    # root is 1, record the result
    if root.state:
        one_leaf_dict = {}
        n_leaf = 0

        for leaf_name in leaf_node_dict:
            leaf_node = leaf_node_dict[leaf_name]
            one_leaf_dict[leaf_name] = leaf_node.state
            if leaf_node.state:
                n_leaf += 1

        # This part can be improved by implementing a fixed length sorted list
        # or max_heap, but trivial for smaller MAX_N_RESULT
        if (n_leaf, one_leaf_dict) not in result:
            if len(result) <= MAX_N_RESULT:
                result.append((n_leaf, one_leaf_dict))
                result.sort(key=lambda x: x[0])
            elif n_leaf < result[-1][0]:
                result.append((n_leaf, one_leaf_dict))
                result.sort(key=lambda x: x[0])
                result.pop()

print (result)
print("===== %s seconds =====" % (time.time() - start_time))
