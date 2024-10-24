#!/usr/bin/env python

import query
import util
import misconceptions_check


# debugging
script_select = util.read_file('test.sql')
script_create = util.read_file('test_create.sql')
q = query.SelectQuery(script_select, script_create)


if __name__ == '__main__':
    from dav_tools import argument_parser, messages
    
    argument_parser.add_argument('file', help='File containing the SELECT query')
    argument_parser.add_argument('table', help='File containing the CREATE TABLE query')
    argument_parser.add_verbose_mode()

    argument_parser.set_developer_info('Davide Ponzini', 'davide.ponzini@edu.unige.it')

    script_select = util.read_file(argument_parser.args.file)
    script_create = util.read_file(argument_parser.args.table)
    q = query.SelectQuery(script_select, script_create)


    sel = q.select_clause
    fr = q.from_clause
    wh = q.where_clause
    gb = q.group_by_clause
    hav = q.having_clause
    ob = q.order_by_clause

    if argument_parser.args.verbose:
        messages.info('============= SCHEMA =============')
        print(repr(q.schema))

        if sel is not None:
            messages.info('============= SELECT =============')
            print(repr(sel))
            messages.message(sel.distinct, icon='DISTINCT', icon_options=[messages.TextFormat.Color.BLUE])
            for identifier in sel.identifiers:
                messages.message(str(identifier), repr(identifier), f'{identifier.get_parent_name()}.{identifier.get_real_name()} -> {identifier.get_parent_name()}.{identifier.get_name()}',
                                icon='column', icon_options=[messages.TextFormat.Color.GREEN],
                                text_min_len=[30, 50])

        if fr is not None:
            messages.info('============= FROM =============')
            print(repr(fr))
            for k,v in fr.tables.items():
                messages.message(k, v,
                                icon='table', icon_options=[messages.TextFormat.Color.GREEN],
                                additional_text_options=[[], [messages.TextFormat.Style.DIM]],
                                text_min_len=[20])

        if wh is not None:
            messages.info('============= WHERE =============')
            print(repr(wh))

        if gb is not None:
            messages.info('============= GROUP BY =============')
            print(repr(gb))

        if hav is not None:
            messages.info('============= HAVING =============')
            print(repr(hav))

        if ob is not None:
            messages.info('============= ORDER BY =============')
            print(repr(ob))

        messages.info('============= MISCONCEPTIONS =============')

    misconceptions_check.syn_6_common_syntax_error_using_where_twice(q)
    misconceptions_check.syn_6_common_syntax_error_additional_semicolon(q)
    
    q.print_misconceptions()
