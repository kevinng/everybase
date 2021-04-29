from django.test import TestCase
from processor.libraries.utils import (is_space, get_first_string, match)

class IsSpaceTestCase(TestCase):
    def test_is_space(self):
        self.assertTrue(is_space(' '))

    def test_is_tab(self):
        self.assertTrue(is_space('\t'))

    def test_is_newline(self):
        self.assertTrue(is_space('\n'))

    def test_string_with_no_space_is_not_space(self):
        self.assertFalse(is_space('abc'))
    
    def test_string_with_space_is_not_space(self):
        self.assertFalse(is_space(' abc '))
    
    def test_string_with_tab_is_not_space(self):
        self.assertFalse(is_space('\tabc\t'))
    
    def test_string_with_newline_is_not_space(self):
        self.assertFalse(is_space('\nabc\n'))

class GetFirstStringTestCase(TestCase):
    def test_two_strings_returns_first(self):
        self.assertEqual(get_first_string('aaa bbb'), 'aaa')

    def test_one_string_returns_first(self):
        self.assertEqual(get_first_string('aaa'), 'aaa')

    def test_one_string_after_space_returns_None(self):
        self.assertEqual(get_first_string(' bbb'), None)

    def test_space_returns_none(self):
        self.assertEqual(get_first_string(' '), None)

    def test_empty_returns_none(self):
        self.assertEqual(get_first_string(''), None)

class MatchTestCase(TestCase):
    def test_match_same_zero_t_returns_true(self):
        self.assertTrue(match('aaa', 'aaa', 0))

    def test_match_same_one_t_returns_true(self):
        self.assertTrue(match('aaa', 'aaa', 1))

    def test_match_one_diff_one_t_returns_true(self):
        self.assertTrue(match('aaa', 'aab', 1))

    def test_match_one_diff_zero_t_returns_false(self):
        self.assertFalse(match('aaa', 'aab', 0))