from .header_extractor import HeaderExtractor


class RHeaderExtractor(HeaderExtractor):

    def __init__(self, notebook_data, base_image_tags_url: str):
        super().__init__(notebook_data, base_image_tags_url)

    def get_cell_confs(self) -> list[dict] | None:
        confs = super().get_cell_confs()

        # Convert lists to R format, because the parent HeaderExtractor
        # produces JSON/YAML/Python lists.
        # e.g. [1, 2, ...] to list(1, 2, ...)
        if confs is not None:
            for conf in confs:
                conf['assignation'] = (conf['assignation']
                                       .replace('[', 'list(')
                                       .replace(']', ')'))

        return confs
