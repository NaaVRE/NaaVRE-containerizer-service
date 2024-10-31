import uuid

from colorhash import ColorHash


class ConverterReactFlowChart:

    @staticmethod
    def get_node(node_id, title, ins, outs, params, secrets):
        node = {}
        position = {}
        ports = {}
        node['id'] = node_id
        node['type'] = 'input-output'
        position['x'] = 35
        position['y'] = 15
        node['position'] = position
        properties = {'title': title,
                      'vars': [],
                      'params': list(params),
                      'secrets': list(secrets),
                      'inputs': list(ins),
                      'outputs': list(outs),
                      'og_node_id': node_id}
        node['properties'] = properties

        for i in ins:
            ports[i] = {}
            ports[i]['properties'] = {}
            ports[i]['id'] = i
            ports[i]['type'] = 'left'
            ports[i]['properties']['color'] = ColorHash(i).hex
            properties['vars'].append({
                'name': i,
                'direction': 'input',
                'type': 'datatype',
                'color': ports[i]['properties']['color']
            })

        for o in outs:
            ports[o] = {}
            ports[o]['properties'] = {}
            ports[o]['id'] = o
            ports[o]['type'] = 'right'
            ports[o]['properties']['color'] = ColorHash(o).hex
            properties['vars'].append({
                'name': o,
                'direction': 'output',
                'type': 'datatype',
                'color': ports[o]['properties']['color']
            })

        node['ports'] = ports
        return node


class ConverterReactFlow:

    @staticmethod
    def get_input_nodes(ins):
        nodes = []
        idx = 0

        for i in ins:
            i_node = {'data': {}, 'position': {}, 'id': i, 'type': 'input'}
            i_node['data']['label'] = i
            i_node['position']['x'] = 10 + idx * 200
            i_node['position']['y'] = 10
            nodes.append(i_node)
            idx += 1

        return nodes

    @staticmethod
    def get_output_nodes(outs):
        nodes = []
        idx = 0

        for o in outs:
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
    def get_edges(d_node_id, ins, outs):
        edges = []

        for i in ins:
            i_edge = {'id': "%s-%s" % (i, d_node_id), 'source': i,
                      'target': d_node_id, 'animated': True}
            edges.append(i_edge)

        for o in outs:
            o_edge = {'id': "%s-%s" % (d_node_id, o), 'source': d_node_id,
                      'target': o, 'animated': True}
            edges.append(o_edge)

        return edges


class ConverterFlume:

    @staticmethod
    def get_ports(ins, outs):
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

        ports.update(ins)
        ports.update(outs)

        color_i = 0
        for port in ports:
            p_type = {'type': port, 'name': port, 'label': port,
                      'color': (colors[color_i],)}
            color_i = (color_i + 1) % len(colors)

            ports_types.append(p_type)

        return ports_types

    @staticmethod
    def get_node(source, ports, ins, outs):
        title = source.partition('\n')[0]
        short_uuid = str(uuid.uuid4())[:7]

        n_type = {'type': short_uuid,
                  'label': title if title[0] == "#" else
                  "Untitled %s" % short_uuid,
                  'description': short_uuid}

        ports_in = [p for p in ports if p['name'] in ins]
        ports_out = [p for p in ports if p['name'] in outs]

        n_type['inputs'] = ports_in
        n_type['outputs'] = ports_out

        return n_type
