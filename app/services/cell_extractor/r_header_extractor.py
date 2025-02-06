from .header_extractor import HeaderExtractor


class RHeaderExtractor(HeaderExtractor):

    def __init__(self, notebook_data, base_image_tags_url: str):
        super().__init__(notebook_data, base_image_tags_url)

    def get_cell_confs(self) -> list[dict]:
        if self.cell_header is None:
            return []
        items = self.cell_header['NaaVRE']['cell'].get_base_image_tags('confs')
        if items is None:
            return []
        confs = []
        for item in items:
            for k, v in item.items():
                if 'assignation' in v:
                    assignation = v.get_base_image_tags('assignation')
                    if '[' in assignation and ']' in assignation:
                        # Replace to R list format
                        assignation = assignation.replace('[',
                                                          'list(').replace(']',
                                                                           ')')
                        item[k]['assignation'] = assignation
                conf = {'name': k, 'assignation': item[k]['assignation']}
                confs.append(conf)
        return confs
