import uuid

from colorhash import ColorHash


class ConverterReactFlowChart:

    @staticmethod
    def get_node(title: str,
                 inputs: list,
                 outputs: list,
                 params: list,
                 secrets: list
                 ):
        node = {}
        position = {}
        ports = {}
        node['type'] = 'input-output'
        position['x'] = 35
        position['y'] = 15
        node['position'] = position
        properties = {'title': title,
                      'vars': [],
                      'params': params,
                      'secrets': secrets,
                      'inputs': inputs,
                      'outputs': outputs}
        node['properties'] = properties

        for cell_input in inputs:
            input_name = cell_input['name']
            ports[input_name] = {}
            ports[input_name]['properties'] = {}
            ports[input_name]['id'] = input_name
            ports[input_name]['type'] = 'left'
            ports[input_name]['properties']['color'] = (
                ColorHash(cell_input).hex)
            properties['vars'].append({
                'name': input_name,
                'direction': 'input',
                'type': 'datatype',
                'color': ports[input_name]['properties']['color']
            })

        for cell_outputs in outputs:
            output_name = cell_outputs['name']
            ports[output_name] = {}
            ports[output_name]['properties'] = {}
            ports[output_name]['id'] = output_name
            ports[output_name]['type'] = 'right'
            ports[output_name]['properties']['color'] = (
                ColorHash(output_name).hex)
            properties['vars'].append({
                'name': output_name,
                'direction': 'output',
                'type': 'datatype',
                'color': ports[output_name]['properties']['color']
            })

        node['ports'] = ports
        return node


class ConverterReactFlow:

    @staticmethod
    def get_input_nodes(inputs):
        nodes = []
        idx = 0

        for i in inputs:
            i_node = {'data': {}, 'position': {}, 'id': i, 'type': 'input'}
            i_node['data']['label'] = i
            i_node['position']['x'] = 10 + idx * 200
            i_node['position']['y'] = 10
            nodes.append(i_node)
            idx += 1

        return nodes

    @staticmethod
    def get_output_nodes(outputs):
        nodes = []
        idx = 0

        for o in outputs:
            o_node = {'data': {}, 'position': {}, 'id': o, 'type': 'output'}
            o_node['data']['label'] = o
            o_node['position']['x'] = 10 + idx * 200
            o_node['position']['y'] = 200
            nodes.append(o_node)
            idx += 1

        return nodes

    @staticmethod
    def get_default_node(title, node_uuid):
        d_node = {'data': {}, 'position': {}, 'id': node_uuid}
        d_node['data']['label'] = title
        d_node['position']['x'] = 100
        d_node['position']['y'] = 100

        return d_node

    @staticmethod
    def get_edges(d_node_id, inputs, outputs):
        edges = []

        for cell_input in inputs:
            input_name = cell_input['name']
            i_edge = {'id': "%s-%s" % (input_name, d_node_id),
                      'source': input_name,
                      'target': d_node_id,
                      'animated': True
                      }
            edges.append(i_edge)

        for cell_output in outputs:
            output_name = cell_output['name']
            o_edge = {'id': "%s-%s" % (d_node_id, output_name),
                      'source': d_node_id,
                      'target': output_name,
                      'animated': True
                      }
            edges.append(o_edge)

        return edges


class ConverterFlume:

    @staticmethod
    def get_ports(inputs, outputs):
        colors = [
            'yellow',
            'orange',
            'red',
            'pink',
            'purple',
            'blue',
            'green',
            'grey'
        ]

        ports = set()
        ports_types = []

        ports.update(inputs)
        ports.update(outputs)

        color_i = 0
        for port in ports:
            p_type = {'type': port,
                      'name': port,
                      'label': port,
                      'color': (colors[color_i],)
                      }
            color_i = (color_i + 1) % len(colors)

            ports_types.append(p_type)

        return ports_types

    @staticmethod
    def get_node(source, ports, inputs, outputs):
        title = source.partition('\n')[0]
        short_uuid = str(uuid.uuid4())[:7]

        n_type = {'type': short_uuid,
                  'label': title if title[0] == "#" else
                  "Untitled %s" % short_uuid,
                  'description': short_uuid}

        ports_in = [p for p in ports if p['name'] in inputs]
        ports_out = [p for p in ports if p['name'] in outputs]

        n_type['inputs'] = ports_in
        n_type['outputs'] = ports_out

        return n_type
