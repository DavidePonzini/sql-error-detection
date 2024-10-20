#!/usr/bin/env python

from query import Query
from util import read_query
import misconceptions_check


if __name__ == '__main__':
    from dav_tools import argument_parser, messages
    
    argument_parser.add_argument('file')
    text = read_query(argument_parser.args.file)
    query = Query(text)

    messages.info('============= SELECT =============')
    sel = query.extract_select()
    print(repr(sel))
    messages.message(sel.distinct, icon='DISTINCT', icon_options=[messages.TextFormat.Color.BLUE])
    for identifier in sel.identifiers:
        messages.message(f'{identifier.get_parent_name()}.{identifier.get_real_name()} -> {identifier.get_parent_name()}.{identifier.get_name()}', icon='column', icon_options=[messages.TextFormat.Color.GREEN])

    messages.info('============= FROM =============')
    fr = query.extract_from()
    print(repr(fr))
    for identifier in fr.identifiers:
        messages.message(f'{identifier.get_real_name()} -> {identifier.get_name()}', icon='table', icon_options=[messages.TextFormat.Color.GREEN])

    messages.info('============= WHERE =============')
    wh = query.extract_where()
    print(repr(wh))

    messages.info('============= GROUP BY =============')
    gb = query.extract_group_by()
    print(repr(gb))

    messages.info('============= HAVING =============')
    hav = query.extract_having()
    print(repr(hav))

    messages.info('============= ORDER BY =============')
    ob = query.extract_order_by()
    print(repr(ob))

    messages.info('============= MISCONCEPTIONS =============')
    misconceptions_check.syn_6_common_syntax_error_using_where_twice(query)
