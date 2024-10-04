import sqlparse
from dav_tools import argument_parser, messages


def read_query(filepath: str):
    with open(filepath) as f:
        return f.read()


def split(query):
    for x in query:
        messages.success(x)
        

if __name__ == '__main__':
    argument_parser.add_argument('files', nargs='+')
    argument_parser.args

    for file in argument_parser.args.files:
        messages.info('='*40, file, '='*40)

        query = read_query(file)

        try:
            query = sqlparse.parse(query)[0]
            split(query)
        except:
            messages.error(file)

