import util

from enum import Enum
from abc import abstractmethod


class SQL_Code:
    def __init__(self, tokens: list):
        self.tokens = util.strip_spaces_and_comments(tokens)

    def __str__(self):
        return '\n'.join([str(token) for token in self.tokens])
    
    def __repr__(self):
        tokens = ',\n '.join([token.__repr__() for token in self.tokens])
        return f'[{tokens}]'


# class ConditionEvaluationResult(Enum):
#     TRUE        = 1
#     FALSE       = 2
#     CONSTANT    = 3
#     UNKNOWN     = 4
#     ERROR       = 5


# class Condition:
#     @abstractmethod
#     def eval(self) -> ConditionEvaluationResult:
#         pass

# class Comparison(SQL_Code):
#     def __init__(self, tokens):
#         super().__init__(tokens)

#     def eval(self) -> ConditionEvaluationResult:
#         pass


# class BinaryCondition(Condition):
#     def __init__(self, operator1: Comparison, operator2: Comparison):
#         self.operator1 = operator1
#         self.operator2 = operator2

#     @abstractmethod
#     def eval(self) -> ConditionEvaluationResult:
#         pass

    
# class And(BinaryCondition):
#     def __init__(self, operator1: Comparison, operator2: Comparison):
#         super().__init__(operator1, operator2)

#     def eval(self) -> ConditionEvaluationResult:
#         res1 = self.operator1.eval()
#         res2 = self.operator2.eval()

#         if res1 == ConditionEvaluationResult.ERROR or res2 == ConditionEvaluationResult.ERROR:
#             return ConditionEvaluationResult.ERROR
        
#         if res1 == ConditionEvaluationResult.UNKNOWN or res2 == ConditionEvaluationResult.UNKNOWN:
#             return ConditionEvaluationResult.UNKNOWN

#         if res1 == ConditionEvaluationResult.TRUE and res2 == ConditionEvaluationResult.TRUE:
#             return ConditionEvaluationResult.TRUE
        
#         return ConditionEvaluationResult.FALSE
    
# class Or(BinaryCondition):
#     def __init__(self, operator1: Comparison, operator2: Comparison):
#         super().__init__(operator1, operator2)

#     def eval(self) -> ConditionEvaluationResult:
#         res1 = self.operator1.eval()
#         res2 = self.operator2.eval()

#         if res1 == ConditionEvaluationResult.ERROR or res2 == ConditionEvaluationResult.ERROR:
#             return ConditionEvaluationResult.ERROR
        
#         if res1 == ConditionEvaluationResult.UNKNOWN or res2 == ConditionEvaluationResult.UNKNOWN:
#             return ConditionEvaluationResult.UNKNOWN

#         if res1 == ConditionEvaluationResult.TRUE or res2 == ConditionEvaluationResult.TRUE:
#             return ConditionEvaluationResult.TRUE
        
#         return ConditionEvaluationResult.FALSE