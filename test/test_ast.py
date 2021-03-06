# -*- coding: utf-8 -*-
################################
# Angularize
# @author: Savor d'Isavano
# @date:  2014-06-13
################################

import unittest
from test.test_utils import code_matches_rule
from utils.lang import class_stringify, issubclass_of_any
from angularize.translator import AstTranslator

class TestAst(unittest.TestCase):
    '''测试translator模块'''

    def setUp(self):
        pass

    def test_issubclass_of_any(self):
        from collections import defaultdict
        self.assertTrue(issubclass_of_any(defaultdict, [dict, int, str]))
        self.assertFalse(issubclass_of_any(defaultdict, [int, str, float]))

    def test_class_stringify(self):
        import ast
        self.assertEqual(class_stringify(ast.stmt), 'stmt')
        self.assertEqual(class_stringify(ast.Module), 'Module')
        self.assertEqual(class_stringify(int), 'int')

    def test_ast_translator_methods_created_properly(self):
        self.assertTrue('_stmt_translate' in AstTranslator.__dict__)
        translator = AstTranslator(None)
        translator = AstTranslator(None)
        self.assertTrue(getattr(translator, '_stmt_translate') is not None)

    def test_ast_mro(self):
        import ast
        lv1_type = ast.Assign.mro()[-3]
        self.assertTrue(lv1_type is ast.stmt)

    def test_ast_translator_translate_functions(self):

        code = '''def func(a, b): print(a // b)'''
        translator = AstTranslator(code)
        rule = " function func ( a , b ) { console.log ( parseInt ( a / b ) ) ; } "
        result = translator.translate()
        self.assertTrue(code_matches_rule(result, rule))

        code = '''def func(x): x = 3;  x = 4; y = 5; y = 6; print(x + y * y)'''
        translator = AstTranslator(code)
        rule = " function func ( x ) { x = 3 ; x = 4 ; var y = 5 ; y = 6; console.log ( x + y * y ) ; } "
        result = translator.translate()
        self.assertTrue(code_matches_rule(result, rule))
