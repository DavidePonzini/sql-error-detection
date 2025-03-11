#!/usr/bin/env python

import query
import util


if __name__ == '__main__':
    from dav_tools import argument_parser
    
    argument_parser.add_argument('file', help='File containing the SELECT query')
    argument_parser.add_argument('table', help='File containing the CREATE TABLE query')

    argument_parser.set_developer_info('Davide Ponzini', 'davide.ponzini@edu.unige.it')

    script_select = util.read_file(argument_parser.args.file)
    script_create = util.read_file(argument_parser.args.table)

    query.SelectQuery(script_select, script_create).print_misconceptions()
