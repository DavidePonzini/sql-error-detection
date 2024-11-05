# SQL Syntax and Logic Analysis - To Do List

## Ambiguous Database Objects

- [ ] **syn_1_ambiguous_database_object_omitting_correlation_names**
  - [x] multiple tables in FROM clause with the same name/alias

- [ ] **syn_1_ambiguous_database_object_ambiguous_column**  
  - [x] selecting a column for which multiple definitions exist and table is not specified

- [ ] **syn_1_ambiguous_database_object_ambiguous_function**

## Undefined Database Objects

- [ ] **syn_2_undefined_database_object_undefined_column**  
  - [x] selecting from a column that does not exist (or is not available from FROM clause)

- [ ] **syn_2_undefined_database_object_undefined_function**

- [ ] **syn_2_undefined_database_object_undefined_parameter**

- [ ] **syn_2_undefined_database_object_undefined_object**  
  - [x] table selected in FROM but not available in the schema

- [ ] **syn_2_undefined_database_object_invalid_schema_name**

- [ ] **syn_2_undefined_database_object_misspellings**

- [ ] **syn_2_undefined_database_object_synonyms**

- [ ] **syn_2_undefined_database_object_omitting_quotes_around_character_data**

## Data Type Mismatch

- [ ] **syn_3_data_type_mismatch_failure_to_specify_column_name_twice**

- [ ] **syn_3_data_type_mismatch**

## Illegal Aggregate Function Placement

- [ ] **syn_4_illegal_aggregate_function_placement_using_aggregate_function_outside_select_or_having**

- [ ] **syn_4_illegal_aggregate_function_placement_grouping_error_aggregate_functions_cannot_be_nested**

## Illegal or Insufficient Grouping

- [ ] **syn_5_illegal_or_insufficient_grouping_grouping_error_extraneous_or_omitted_grouping_column**

- [ ] **syn_5_illegal_or_insufficient_grouping_strange_having_having_without_group_by**

## Common Syntax Errors

- [ ] **syn_6_common_syntax_error_confusing_function_with_function_parameter**

- [ ] **syn_6_common_syntax_error_using_where_twice**  
  - [x] multiple where in WHERE clause, multiple WHERE clauses in different places

- [ ] **syn_6_common_syntax_error_omitting_the_from_clause**

- [ ] **syn_6_common_syntax_error_comparison_with_null**

- [ ] **syn_6_common_syntax_error_omitting_the_semicolon**

- [ ] **syn_6_common_syntax_error_date_time_field_overflow**

- [ ] **syn_6_common_syntax_error_duplicate_clause**

- [ ] **syn_6_common_syntax_error_using_an_undefined_correlation_name**

- [ ] **syn_6_common_syntax_error_too_many_columns_in_subquery**

- [ ] **syn_6_common_syntax_error_confusing_table_names_with_column_names**

- [ ] **syn_6_common_syntax_error_restriction_in_select_clause**

- [ ] **syn_6_common_syntax_error_projection_in_where_clause**

- [ ] **syn_6_common_syntax_error_confusing_the_order_of_keywords**

- [ ] **syn_6_common_syntax_error_confusing_the_logic_of_keywords**

- [ ] **syn_6_common_syntax_error_confusing_the_syntax_of_keywords**

- [ ] **syn_6_common_syntax_error_omitting_commas**

- [ ] **syn_6_common_syntax_error_curly_square_or_unmatched_brackets**

- [ ] **syn_6_common_syntax_error_is_where_not_applicable**

- [ ] **syn_6_common_syntax_error_nonstandard_keywords_or_standard_keywords_in_wrong_context**

- [ ] **syn_6_common_syntax_error_nonstandard_operators**

- [ ] **syn_6_common_syntax_error_additional_semicolon**  
  - [x] multiple semicolons in main query  
  - [ ] semicolons in subqueries

## Semantic Errors

### Inconsistent Expression

- [ ] **sem_1_inconsistent_expression_and_instead_of_or**

- [ ] **sem_1_inconsistent_expression_tautological_or_inconsistent_expression**

- [ ] **sem_1_inconsistent_expression_distinct_in_sum_or_avg**

- [ ] **sem_1_inconsistent_expression_distinct_that_might_remove_important_duplicates**

- [ ] **sem_1_inconsistent_expression_wildcards_without_like**

- [ ] **sem_1_inconsistent_expression_incorrect_wildcard_using_underscore_instead_of_percent**

- [ ] **sem_1_inconsistent_expression_mixing_a_greater_than_0_with_is_not_null**

### Inconsistent Join

- [ ] **sem_2_inconsistent_join_null_in_subquery**

- [ ] **sem_2_inconsistent_join_join_on_incorrect_column**

### Missing Join

- [ ] **sem_3_missing_join_omitting_a_join**

### Duplicate Rows

- [ ] **sem_4_duplicate_rows_many_duplicates**

### Redundant Column Output

- [ ] **sem_5_redundant_column_output_constant_column_output**

- [ ] **sem_5_redundant_column_output_duplicate_column_output**

## Logical Errors

### Operator Error

- [ ] **log_1_operator_error_or_instead_of_and**

- [ ] **log_1_operator_error_extraneous_not_operator**

- [ ] **log_1_operator_error_missing_not_operator**

- [ ] **log_1_operator_error_substituting_existence_negation_with_not_equal_to**

- [ ] **log_1_operator_error_putting_not_in_front_of_incorrect_in_or_exists**

- [ ] **log_1_operator_error_incorrect_comparison_operator_or_value**

### Join Errors

- [ ] **log_2_join_error_join_on_incorrect_table**

- [ ] **log_2_join_error_join_when_join_needs_to_be_omitted**

- [ ] **log_2_join_error_join_on_incorrect_column_matches_possible**

- [ ] **log_2_join_error_join_with_incorrect_comparison_operator**

- [ ] **log_2_join_error_missing_join**

### Nesting Errors

- [ ] **log_3_nesting_error_improper_nesting_of_expressions**

- [ ] **log_3_nesting_error_improper_nesting_of_subqueries**

### Expression Errors

- [ ] **log_4_expression_error_extraneous_quotes**

- [ ] **log_4_expression_error_missing_expression**

- [ ] **log_4_expression_error_expression_on_incorrect_column**

- [ ] **log_4_expression_error_extraneous_expression**

- [ ] **log_4_expression_error_expression_in_incorrect_clause**

### Projection Errors

- [ ] **log_5_projection_error_extraneous_column_in_select**

- [ ] **log_5_projection_error_missing_column_from_select**

- [ ] **log_5_projection_error_missing_distinct_from_select**

- [ ] **log_5_projection_error_missing_as_from_select**

- [ ] **log_5_projection_error_missing_column_from_order_by**

- [ ] **log_5_projection_error_incorrect_column_in_order_by**

- [ ] **log_5_projection_error_extraneous_order_by_clause**

- [ ] **log_5_projection_error_incorrect_ordering_of_rows**

### Function Errors

- [ ] **log_6_function_error_distinct_as_function_parameter_where_not_applicable**

- [ ] **log_6_function_error_missing_distinct_from_function_parameter**

- [ ] **log_6_function_error_incorrect_function**

- [ ] **log_6_function_error_incorrect_column_as_function_parameter**

## Complications

- [ ] **com_1_complication_unnecessary_complication**

- [ ] **com_1_complication_unnecessary_distinct_in_select_clause**

- [ ] **com_1_complication_unnecessary_join**

- [ ] **com_1_complication_unused_correlation_name**

- [ ] **com_1_complication_correlation_names_are_always_identical**

- [ ] **com_1_complication_unnecessarily_general_comparison_operator**

- [ ] **com_1_complication_like_without_wildcards**

- [ ] **com_1_complication_unnecessarily_complicated_select_in_exists_subquery**

- [ ] **com_1_complication_in_exists_can_be_replaced_by_comparison**

- [ ] **com_1_complication_unnecessary_aggregate_function**

- [ ] **com_1_complication_unnecessary_distinct_in_aggregate_function**

- [ ] **com_1_complication_unnecessary_argument_of_count**

- [ ] **com_1_complication_unnecessary_group_by_in_exists_subquery**

- [ ] **com_1_complication_group_by_with_singleton_groups**

- [ ] **com_1_complication_group_by_can_be_replaced_with_distinct**

- [ ] **com_1_complication_union_can_be_replaced_by_or**

- [ ] **com_1_complication_unnecessary_column_in_order_by_clause**

- [ ] **com_1_complication_order_by_in_subquery**

- [ ] **com_1_complication_inefficient_having**

- [ ] **com_1_complication_inefficient_union**

- [ ] **com_1_complication_condition_in_subquery_can_be_moved_up**

- [ ] **com_1_complication_condition_on_left_table_in_left_outer_join**

- [ ] **com_1_complication_outer_join_can_be_replaced_by_inner_join**

- [ ] **com_x_complication_join_condition_in_where_clause**

## Other Misconceptions

- [ ] **other_misconception_does_not_fit_any_category**
