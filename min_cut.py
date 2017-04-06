import random

from import_tree_from_xml import import_tree_from_xml


def min_cut_monte_carlo(n_result, n_repeat, xmlfile='example/example.xml'):

    node_dict, leaf_node_dict = import_tree_from_xml(xmlfile)

    leaf_node_tuple = tuple(leaf_node_dict.values())

    result = []
    root = node_dict['Root']

    # cache the sequence of tree traversal
    post_order_sequence = root.get_post_order_sequence_without_leaves()

    for i in range(n_repeat):
        #  Throw coin for all leaves
        for leaf_node in leaf_node_tuple:
            # http://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
            leaf_node.state = random.random() > 0.5

        # Update the whole tree
        for node in post_order_sequence:
            node.calculate_state()

        # root is 1, record the result
        if n_result > 0 and root.state:
            one_leaf_dict = {}
            n_leaf = 0

            for leaf_name in leaf_node_dict:
                leaf_node = leaf_node_dict[leaf_name]
                one_leaf_dict[leaf_name] = leaf_node.state
                if leaf_node.state:
                    n_leaf += 1

            # This part can be improved by implementing a fixed length sorted
            # list or max_heap, but trivial for smaller n_result
            if (n_leaf, one_leaf_dict) not in result:
                if len(result) < n_result:
                    result.append((n_leaf, one_leaf_dict))
                    result.sort(key=lambda x: x[0])
                elif result and n_leaf < result[-1][0]:
                    result.append((n_leaf, one_leaf_dict))
                    result.sort(key=lambda x: x[0])
                    result.pop()

    result_beauty = [[node for node in each[1] if each[1][node]]
                     for each in result]
    return result_beauty


if __name__ == '__main__':
    import sys
    import time
    if len(sys.argv) == 4:
        n_result = int(sys.argv[1])
        n_repeat = int(sys.argv[2])
        xmlfile = sys.argv[3]
        start_time = time.time()
        min_cut_monte_carlo(n_result, n_repeat, xmlfile)
        print("--- Running file {} finished in {} seconds ---".format(xmlfile, time.time() - start_time))
    else:
        print("python min_cut n_result n_repeat xmlfile")
