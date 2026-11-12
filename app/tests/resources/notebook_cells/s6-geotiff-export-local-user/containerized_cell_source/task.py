from laserfarm import GeotiffWriter
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
expected_arg_names.add('S5_done')
expected_arg_names.add('conf_feature_name')
expected_arg_names.add('conf_local_path_geotiff')
expected_arg_names.add('conf_local_path_targets')
expected_arg_names.add('conf_remote_path_geotiffs')
expected_arg_names.add('conf_wd_opts')
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

arg_name = 'S5_done'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = str
S5_done = _parse_value(arg_value, arg_name, arg_type)

conf_feature_name = 'perc_95_normalized_height'
conf_local_path_geotiff = os.path.join(pathlib.Path('/tmp/data').as_posix(), 'geotiff')
conf_local_path_targets = os.path.join(pathlib.Path('/tmp/data').as_posix(), 'targets')
conf_remote_path_geotiffs = pathlib.Path('/webdav/vl-laserfarm/' + '' + '/geotiffs')
conf_wd_opts = {'webdav_hostname': param_hostname, 'webdav_login': param_username, 'webdav_password': param_password}


arg_value = get_arg_value('id',args,raw_args)
id = _parse_value(arg_value, 'id', str)

S5_done

geotiff_export_input = {
    'setup_local_fs': {
        'input_folder': conf_local_path_targets,
         'output_folder': conf_local_path_geotiff
        },
    'parse_point_cloud': {},
    'data_split': {'xSub': 1, 'ySub': 1},
    'create_subregion_geotiffs': {'output_handle': 'geotiff'},
    'pushremote': conf_remote_path_geotiffs.as_posix(),
}

writer = GeotiffWriter(input_dir=conf_feature_name, bands=conf_feature_name, label=conf_feature_name).config(geotiff_export_input).setup_webdav_client(conf_wd_opts)
writer.run()

remote_path_geotiffs = str(conf_remote_path_geotiffs)
S6_done = 'True'

file_S6_done = open("/tmp/S6_done_" + id + ".json", "w")
file_S6_done.write(json.dumps(S6_done))
file_S6_done.close()
