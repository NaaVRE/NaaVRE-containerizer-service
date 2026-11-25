import numpy as np

import argparse
import json
import os

def _load_json_args(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def _parse_value(value, field_name, target_type, elem_type=None):
    if target_type is list:
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # the value may be "['list_str', 'space in elem', '3']"
                if value.startswith('[') and value.endswith(']'):
                    value = value[1:-1].strip()  # remove the brackets and trim whitespace
                    if value:
                        return [elem.strip().strip("'").strip('"') for elem in value.split(',')]
                    else:
                        return []
                else:
                    arg_parser.error(field_name + " is not a valid list")

    if target_type is str:
        return value

    if target_type is int:
        return int(value)

    if target_type is float:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return float(value)
    arg_parser.error(field_name + " has unsupported target type")

def get_arg_value(name,args,raw_args):
    for arg in raw_args:
        if arg['name'] == name:
            return arg['value']
    arg_parser.error("Argument '" + name + "' not found in JSON args")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--args_json', action='store', type=str, required=True, dest='args_json')

args = arg_parser.parse_args()

expected_arg_names = set()
expected_arg_names.add('id')

raw_args = _load_json_args(args.args_json)
for arg in raw_args:
    if 'name' not in arg:
        arg_parser.error("Argument with no name found in JSON args")
    if arg['name'] not in expected_arg_names:
        arg_parser.error("Unexpected argument '" + arg['name'] + "' found in JSON args")
    if not arg['name'].startswith('conf'):
            if 'value' not in arg or arg['value'] is None:
                arg_parser.error("Argument '" + arg['name'] + "' has no value in JSON args")
    if arg['name'].startswith('conf'):
            if 'assignation' not in arg or arg['assignation'] is None:
                arg_parser.error("Argument '" + arg['name'] + "' has no assignation in JSON args")




arg_value = get_arg_value('id',args,raw_args)
id = _parse_value(arg_value, 'id', str)

class FoxTree:
    def __init__(self, points_array, radius, vertical_resolution, min_pts_per_cluster):
        """
        :param points_array: numpy array of shape (N, 3) containing x, y, z
        """
        self.radius = radius
        self.vertical_resolution = vertical_resolution
        self.min_pts_seeds = min_pts_per_cluster
        
        self.points_data = points_array
        self.num_pts = len(points_array)
        
        self.tree_ids = np.full(self.num_pts, -1, dtype=int)
        
        self.z_min = np.min(points_array[:, 2])
        self.z_max = np.max(points_array[:, 2])
        
        self.parsed_pt_indices = [] # List of indices
        self.next_tree_id = 0
        
        self.trees = {}

    def generate_tree_clusters(self, pt_clusters):
        for cluster_indices in pt_clusters:
            current_id = self.next_tree_id
            self.next_tree_id += 1
            self.trees[current_id] = []
            for idx in cluster_indices:
                self.tree_ids[idx] = current_id
                self.trees[current_id].append(idx)

