from laserfarm import Retiler
import os
import pathlib

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
expected_arg_names.add('split_laz_files')
expected_arg_names.add('conf_local_path_retiled')
expected_arg_names.add('conf_local_path_split')
expected_arg_names.add('conf_max_x')
expected_arg_names.add('conf_max_y')
expected_arg_names.add('conf_min_x')
expected_arg_names.add('conf_min_y')
expected_arg_names.add('conf_n_tiles_side')
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

arg_name = 'split_laz_files'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = list
split_laz_files = _parse_value(arg_value, arg_name, arg_type)

conf_local_path_retiled = os.path.join(pathlib.Path('/tmp/data').as_posix(), 'retiled')
conf_local_path_split = os.path.join(pathlib.Path('/tmp/data').as_posix(), 'split')
conf_max_x = '398892.19'
conf_max_y = '726783.87'
conf_min_x = '-113107.81'
conf_min_y = '214783.87'
conf_n_tiles_side = '512'


arg_value = get_arg_value('id',args,raw_args)
id = _parse_value(arg_value, 'id', str)

split_laz_files

grid_retile = {
    'min_x': float(conf_min_x),
    'max_x': float(conf_max_x),
    'min_y': float(conf_min_y),
    'max_y': float(conf_max_y),
    'n_tiles_side': int(conf_n_tiles_side)
}

retiling_input = {
    'setup_local_fs': {
        'input_folder': conf_local_path_split,
        'output_folder': conf_local_path_retiled
    },
    'set_grid': grid_retile,
    'split_and_redistribute': {},
    'validate': {},
}

for file in split_laz_files:
    clean_file = file.replace('"','').replace('[','').replace(']','')
    print(clean_file)
    retiler = Retiler(clean_file,label=clean_file).config(retiling_input)
    retiler_output = retiler.run()

S3_done = 'True'

file_S3_done = open("/tmp/S3_done_" + id + ".json", "w")
file_S3_done.write(json.dumps(S3_done))
file_S3_done.close()
