from app.services.cell_extractor.header_extractor import HeaderExtractor


class PyHeaderExtractor(HeaderExtractor):

    def __init__(self, notebook_data):
        super().__init__(notebook_data)
