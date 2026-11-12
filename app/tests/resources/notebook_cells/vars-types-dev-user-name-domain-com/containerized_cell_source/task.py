
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

param_string = 'param_string value'
param_string_with_comment = 'param_string value'  # comment
param_int = 1
param_float = 1.1
param_list_int = [1, 2, 3]
param_list_str = ["list_str", "space in elem", "3"]

conf_string = 'param_string value'
conf_string_with_comment = 'param_string value'  # comment
conf_int = 1
conf_float = 1.1
conf_list_int = [1, 2, 3]
conf_list_str = ["list_str", "space in elem", "3"]

var_string = 'var_string value'
var_string_with_comment = 'var_string value'  # comment
var_int = 1
var_float = 1.1
var_list_int = [1, 2, 3]
var_list_str = ["list_str", "space in elem", "3"]

file_var_string = open("/tmp/var_string_" + id + ".json", "w")
file_var_string.write(json.dumps(var_string))
file_var_string.close()
file_var_string_with_comment = open("/tmp/var_string_with_comment_" + id + ".json", "w")
file_var_string_with_comment.write(json.dumps(var_string_with_comment))
file_var_string_with_comment.close()
file_var_int = open("/tmp/var_int_" + id + ".json", "w")
file_var_int.write(json.dumps(var_int))
file_var_int.close()
file_var_float = open("/tmp/var_float_" + id + ".json", "w")
file_var_float.write(json.dumps(var_float))
file_var_float.close()
file_var_list_int = open("/tmp/var_list_int_" + id + ".json", "w")
file_var_list_int.write(json.dumps(var_list_int))
file_var_list_int.close()
file_var_list_str = open("/tmp/var_list_str_" + id + ".json", "w")
file_var_list_str.write(json.dumps(var_list_str))
file_var_list_str.close()
