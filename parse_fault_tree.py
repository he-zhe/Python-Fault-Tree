import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict


def parse_falt_tree(xml_filename, output):
    with open(xml_filename) as file:
        with open('temp.xml', mode='w') as modified_file:
            for line in file:
                line = line.lstrip()
                if line.startswith('<src'):
                    line = '<n ' + line[1:]
                modified_file.write(line)

    # value: [{}, 'AND']

    node_counter = defaultdict(int)  # number of times that each node in src
    node_name_incre = {}
    node_children_dict = {}

    with open('temp.xml', mode='r') as modified_file:
        tree = ET.parse(modified_file)

        for child in tree.getroot():
            node_name = child.attrib['src']
            node_counter[node_name] += 1
            node_name_incre[node_name] = 1

        for child in tree.getroot():
            node_name = child.attrib['src']
            node_children = child.attrib['route'].split(', ')
            if node_counter[node_name] > 1:
                node_path_name = node_name + '-path' + \
                    str(node_name_incre[node_name])
                node_name_incre[node_name] += 1
                node_children_dict[node_path_name] = set(node_children)
            else:
                node_children_dict[node_name] = set(node_children)

    os.remove('temp.xml')
    list_ele = ET.Element('list')

    # create root
    root_ele = ET.Element('node', {'id': 'Root'})
    root_gate = ET.Element('gate')
    root_gate.text = 'AND'
    root_ele.append(root_gate)
    for node in sorted(node_counter.keys()):
        dep_ele = ET.Element('dep')
        dep_ele.text = node
        root_ele.append(dep_ele)

    list_ele.append(root_ele)

    # create node with paths
    for node in sorted(node_counter.keys()):
        n_node = node_counter[node]
        if n_node > 1:
            node_ele = ET.Element('node', {'id': node})
            node_gate = ET.Element('gate')
            node_gate.text = 'AND'
            node_ele.append(node_gate)
            for i in range(1, n_node + 1):
                dep_ele = ET.Element('dep')
                dep_ele.text = node + '-path' + str(i)
                node_ele.append(dep_ele)
            list_ele.append(node_ele)

    for node in sorted(node_children_dict.keys()):
        node_ele = ET.Element('node', {'id': node})
        node_gate = ET.Element('gate')
        node_gate.text = 'OR'
        node_ele.append(node_gate)
        for child in sorted(node_children_dict[node]):
            dep_ele = ET.Element('dep')
            dep_ele.text = child
            node_ele.append(dep_ele)
        list_ele.append(node_ele)

    result_tree = ET.ElementTree(list_ele)
    result_tree.write(output)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        xml_filename = 'example/raw_tree.xml'
        output = 'output.xml'
    elif len(sys.argv) == 2:
        xml_filename = sys.argv[2]
        output = 'output.xml'
    elif len(sys.argv) == 3:
        xml_filename = sys.argv[2]
        output = sys.argv[3]

    parse_falt_tree(xml_filename, output)
