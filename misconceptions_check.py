from sqlparse import tokens as ttypes

from misconceptions import Misconceptions
from query import Query
import util


def syn_1_ambiguous_database_object_omitting_correlation_names(query: Query):
    return False

def syn_1_ambiguous_database_object_ambiguous_column(query: Query):
    return False

def syn_1_ambiguous_database_object_ambiguous_function(query: Query):
    return False

def syn_2_undefined_database_object_undefined_column(query: Query):
    return False

def syn_2_undefined_database_object_undefined_function(query: Query):
    return False

def syn_2_undefined_database_object_undefined_parameter(query: Query):
    return False

def syn_2_undefined_database_object_undefined_object(query: Query):
    return False

def syn_2_undefined_database_object_invalid_schema_name(query: Query):
    return False

def syn_2_undefined_database_object_misspellings(query: Query):
    return False

def syn_2_undefined_database_object_synonyms(query: Query):
    return False

def syn_2_undefined_database_object_omitting_quotes_around_character_data(query: Query):
    return False

def syn_3_data_type_mismatch_failure_to_specify_column_name_twice(query: Query):
    return False

def syn_3_data_type_mismatch(query: Query):
    return False

def syn_4_illegal_aggregate_function_placement_using_aggregate_function_outside_select_or_having(query: Query):
    return False

def syn_4_illegal_aggregate_function_placement_grouping_error_aggregate_functions_cannot_be_nested(query: Query):
    return False

def syn_5_illegal_or_insufficient_grouping_grouping_error_extraneous_or_omitted_grouping_column(query: Query):
    return False

def syn_5_illegal_or_insufficient_grouping_strange_having_having_without_group_by(query: Query):
    return False

def syn_6_common_syntax_error_confusing_function_with_function_parameter(query: Query):
    return False

def syn_6_common_syntax_error_using_where_twice(query: Query):
    where = query.extract_where()
    clauses = where.tokens
    
    if len(clauses) == 0:
        return
    
    if len(clauses) > 2:
        # TODO: where used twice, most likely not in the right place!
        pass

    # merge multiple where clauses into a single one
    #   (if where is used twice in the 'correct' place, we have a single clause, if it is used in two random places, we have two separate clauses)

    tokens = util.merge_tokens(*clauses)

    count = 0
    for token in tokens:
        if token.ttype is ttypes.Keyword and token.value.upper() == 'WHERE':
            count += 1
    
    if count > 1:
        query.log_misconception(Misconceptions.SYN_6_COMMON_SYNTAX_ERROR_USING_WHERE_TWICE)


def syn_6_common_syntax_error_omitting_the_from_clause(query: Query):
    return False

def syn_6_common_syntax_error_comparison_with_null(query: Query):
    return False

def syn_6_common_syntax_error_omitting_the_semicolon(query: Query):
    return False

def syn_6_common_syntax_error_date_time_field_overflow(query: Query):
    return False

def syn_6_common_syntax_error_duplicate_clause(query: Query):
    return False

def syn_6_common_syntax_error_using_an_undefined_correlation_name(query: Query):
    return False

def syn_6_common_syntax_error_too_many_columns_in_subquery(query: Query):
    return False

def syn_6_common_syntax_error_confusing_table_names_with_column_names(query: Query):
    return False

def syn_6_common_syntax_error_restriction_in_select_clause(query: Query):
    return False

def syn_6_common_syntax_error_projection_in_where_clause(query: Query):
    return False

def syn_6_common_syntax_error_confusing_the_order_of_keywords(query: Query):
    return False

def syn_6_common_syntax_error_confusing_the_logic_of_keywords(query: Query):
    return False

def syn_6_common_syntax_error_confusing_the_syntax_of_keywords(query: Query):
    return False

def syn_6_common_syntax_error_omitting_commas(query: Query):
    return False

def syn_6_common_syntax_error_curly_square_or_unmatched_brackets(query: Query):
    return False

def syn_6_common_syntax_error_is_where_not_applicable(query: Query):
    return False

def syn_6_common_syntax_error_nonstandard_keywords_or_standard_keywords_in_wrong_context(query: Query):
    return False

def syn_6_common_syntax_error_nonstandard_operators(query: Query):
    return False

def syn_6_common_syntax_error_additional_semicolon(query: Query):
    semicolons = 0

    for token in query.tokens:
        if token.ttype is ttypes.Punctuation and token.value == ';':
            semicolons += 1

    if semicolons > 1:
        query.log_misconception(Misconceptions.SYN_6_COMMON_SYNTAX_ERROR_ADDITIONAL_SEMICOLON)

def sem_1_inconsistent_expression_and_instead_of_or(query: Query):
    return False

def sem_1_inconsistent_expression_tautological_or_inconsistent_expression(query: Query):
    return False

def sem_1_inconsistent_expression_distinct_in_sum_or_avg(query: Query):
    return False

def sem_1_inconsistent_expression_distinct_that_might_remove_important_duplicates(query: Query):
    return False

def sem_1_inconsistent_expression_wildcards_without_like(query: Query):
    return False

def sem_1_inconsistent_expression_incorrect_wildcard_using_underscore_instead_of_percent(query: Query):
    return False

def sem_1_inconsistent_expression_mixing_a_greater_than_0_with_is_not_null(query: Query):
    return False

def sem_2_inconsistent_join_null_in_subquery(query: Query):
    return False

def sem_2_inconsistent_join_join_on_incorrect_column(query: Query):
    return False

def sem_3_missing_join_omitting_a_join(query: Query):
    return False

def sem_4_duplicate_rows_many_duplicates(query: Query):
    return False

def sem_5_redundant_column_output_constant_column_output(query: Query):
    return False

def sem_5_redundant_column_output_duplicate_column_output(query: Query):
    return False

def log_1_operator_error_or_instead_of_and(query: Query):
    return False

def log_1_operator_error_extraneous_not_operator(query: Query):
    return False

def log_1_operator_error_missing_not_operator(query: Query):
    return False

def log_1_operator_error_substituting_existence_negation_with_not_equal_to(query: Query):
    return False

def log_1_operator_error_putting_not_in_front_of_incorrect_in_or_exists(query: Query):
    return False

def log_1_operator_error_incorrect_comparison_operator_or_value(query: Query):
    return False

def log_2_join_error_join_on_incorrect_table(query: Query):
    return False

def log_2_join_error_join_when_join_needs_to_be_omitted(query: Query):
    return False

def log_2_join_error_join_on_incorrect_column_matches_possible(query: Query):
    return False

def log_2_join_error_join_with_incorrect_comparison_operator(query: Query):
    return False

def log_2_join_error_missing_join(query: Query):
    return False

def log_3_nesting_error_improper_nesting_of_expressions(query: Query):
    return False

def log_3_nesting_error_improper_nesting_of_subqueries(query: Query):
    return False

def log_4_expression_error_extraneous_quotes(query: Query):
    return False

def log_4_expression_error_missing_expression(query: Query):
    return False

def log_4_expression_error_expression_on_incorrect_column(query: Query):
    return False

def log_4_expression_error_extraneous_expression(query: Query):
    return False

def log_4_expression_error_expression_in_incorrect_clause(query: Query):
    return False

def log_5_projection_error_extraneous_column_in_select(query: Query):
    return False

def log_5_projection_error_missing_column_from_select(query: Query):
    return False

def log_5_projection_error_missing_distinct_from_select(query: Query):
    return False

def log_5_projection_error_missing_as_from_select(query: Query):
    return False

def log_5_projection_error_missing_column_from_order_by(query: Query):
    return False

def log_5_projection_error_incorrect_column_in_order_by(query: Query):
    return False

def log_5_projection_error_extraneous_order_by_clause(query: Query):
    return False

def log_5_projection_error_incorrect_ordering_of_rows(query: Query):
    return False

def log_6_function_error_distinct_as_function_parameter_where_not_applicable(query: Query):
    return False

def log_6_function_error_missing_distinct_from_function_parameter(query: Query):
    return False

def log_6_function_error_incorrect_function(query: Query):
    return False

def log_6_function_error_incorrect_column_as_function_parameter(query: Query):
    return False

def com_1_complication_unnecessary_complication(query: Query):
    return False

def com_1_complication_unnecessary_distinct_in_select_clause(query: Query):
    return False

def com_1_complication_unnecessary_join(query: Query):
    return False

def com_1_complication_unused_correlation_name(query: Query):
    return False

def com_1_complication_correlation_names_are_always_identical(query: Query):
    return False

def com_1_complication_unnecessarily_general_comparison_operator(query: Query):
    return False

def com_1_complication_like_without_wildcards(query: Query):
    return False

def com_1_complication_unnecessarily_complicated_select_in_exists_subquery(query: Query):
    return False

def com_1_complication_in_exists_can_be_replaced_by_comparison(query: Query):
    return False

def com_1_complication_unnecessary_aggregate_function(query: Query):
    return False

def com_1_complication_unnecessary_distinct_in_aggregate_function(query: Query):
    return False

def com_1_complication_unnecessary_argument_of_count(query: Query):
    return False

def com_1_complication_unnecessary_group_by_in_exists_subquery(query: Query):
    return False

def com_1_complication_group_by_with_singleton_groups(query: Query):
    return False

def com_1_complication_group_by_can_be_replaced_with_distinct(query: Query):
    return False

def com_1_complication_union_can_be_replaced_by_or(query: Query):
    return False

def com_1_complication_unnecessary_column_in_order_by_clause(query: Query):
    return False

def com_1_complication_order_by_in_subquery(query: Query):
    return False

def com_1_complication_inefficient_having(query: Query):
    return False

def com_1_complication_inefficient_union(query: Query):
    return False

def com_1_complication_condition_in_subquery_can_be_moved_up(query: Query):
    return False

def com_1_complication_condition_on_left_table_in_left_outer_join(query: Query):
    return False

def com_1_complication_outer_join_can_be_replaced_by_inner_join(query: Query):
    return False

def com_x_complication_join_condition_in_where_clause(query: Query):
    return False

def exemplary_query_has_no_issues(query: Query):
    return False

def other_Misconceptions_does_not_fit_any_category(query: Query):
    return False
