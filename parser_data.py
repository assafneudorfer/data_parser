from collections import defaultdict
from zipfile import ZipFile
from utils import *

# Constance

# The relevant widths fields for the task
WIDTHS = [5, 6, -2, 11, -3, 2, 12, 12, 12, 12]

# only the number id field
ID_ONLY = [-5, -6, -2, 11]

# The relevant names fields for the task
FIELD_NAMES = ['entity_code', 'information_date', 'identification_number',
               'situation', 'loans', 'participations', 'guarantees_granted', 'other_concepts']

# the field for calculate dept
DEPT_FIELDS = ['loans', 'participations', 'guarantees_granted', 'other_concepts']


# Data parser class that build to parser the zip file that supply and all his sub files
class DataParser:
    def __init__(self, zip_path: str, file_names: List[str] = None):
        with ZipFile(zip_path, 'r') as archive:
            # extract the files
            self.file_names = file_names if file_names else [f.filename for f in archive.filelist]
            for member in self.file_names:
                archive.extract(member)

            self.line_size = 0
            self.data_file = None

            # Not using this field for the task
            # mapping between id number to his depts
            self.data = defaultdict(list)

            # mapping between id number to his lines on the file
            self.index_mapping = defaultdict(list)

            self.mapping_file = None
            self.entity_mapping = {}

            # If we want to output the parsing to file
            self.output_file = None

    # extract the file from zip and open connection to file that need to process
    def __enter__(self):
        # open the data.txt in bytes mode
        self.data_file = open(get_file_name(self.file_names, '.txt'), 'rb')

        # fwf file all lines have the same size take the size and return the seek to 0
        self.line_size = len(self.data_file.readline())
        self.data_file.seek(0)

        # the file must be encoding for reading
        self.mapping_file = open(get_file_name(self.file_names, '.tsv'), 'r', encoding="utf8")

        return self

    # close connections
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.data_file.close()
        self.mapping_file.close()
        if self.output_file:
            self.output_file.close()

    def load_mapping(self):
        for line in self.mapping_file:
            entity_code, entity_name = tuple(line.strip().split('\t'))
            self.entity_mapping[entity_code] = entity_name

    # This function use to load the data for dict object
    # Not Using this function for the task
    def load_data(self):
        # reading line by line and not load all the file to memory
        for i, line in enumerate(self.data_file):
            self.get_dept(line)

    def print_line_by_line(self):
        # fill the index mapping for each id number to his index lines
        for i, line in enumerate(self.data_file):
            id_number = extract_line(line, ID_ONLY, ['identification_number'])['identification_number']
            self.index_mapping[id_number] += [i]

        for key, indexes in self.index_mapping.items():
            self.print_line(key, indexes)

    def print_line(self, key: str, indexes: List[int]):
        debts = []
        for i in indexes:
            # use the index and line size to move the seek to the right starting position of the line
            self.data_file.seek(i * self.line_size)
            line = self.data_file.readline()

            # self.output_file.write(line)

            # get the dept of the line
            res = self.get_dept(line)
            if res:
                debts.append(res)
        if debts:
            print({'dentification_number': key, 'debts': debts}, file=self.output_file)

    def get_dept(self, line: bytes) -> Dict[str, str]:
        # extract the line base of the widths of the fields
        row = extract_line(line, WIDTHS, FIELD_NAMES)

        # condition which skip wrong lines
        if check_situation(row['situation']) and row['entity_code'] in self.entity_mapping:
            # get the entity name from mapping
            entity_name = self.entity_mapping[row['entity_code']]
            # build dept dict
            debt = {'entity_name': entity_name, 'situation': row['situation'],
                    'debt_amount': 1000 * sum([int(row[k]) for k in DEPT_FIELDS]),
                    'information_date': get_current_date(row['information_date']).strftime('%Y-%m-%d')}
            return debt

    # Not Using this function for the task
    def print_data(self):
        for key, value in self.data.items():
            print({'dentification_number': key, 'debts': value}, file=self.output_file)

    def parse(self, file: TextIO = None):
        # open file to write if need
        self.output_file = file
        self.load_mapping()
        self.print_line_by_line()
