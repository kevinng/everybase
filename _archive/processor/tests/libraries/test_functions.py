from django.test import TestCase
from processor.libraries.constants import TAGS
from processor.libraries.functions import (is_space, get_first_word, match,
    get_start_position_of_previous_word, get_end_position_of_next_word, is_tld,
    find_any, get_this_word, has_tag_dot_domain, mark_string,
    mark_around_symbol)

class IsSpaceTestCase(TestCase):
    def test_space_should_be_space(self):
        self.assertTrue(is_space(' '))

    def test_tab_should_be_tab(self):
        self.assertTrue(is_space('\t'))

    def test_newline_should_be_newline(self):
        self.assertTrue(is_space('\n'))

    def test_string_with_no_space_should_not_be_space(self):
        self.assertFalse(is_space('abc'))
    
    def test_string_with_space_should_not_be_space(self):
        self.assertFalse(is_space(' abc '))
    
    def test_string_with_tab_should_not_be_space(self):
        self.assertFalse(is_space('\tabc\t'))
    
    def test_string_with_newline_should_not_be_space(self):
        self.assertFalse(is_space('\nabc\n'))

class MatchTestCase(TestCase):
    def test_match_same_with_zero_t_should_return_true(self):
        self.assertTrue(match('aaa', 'aaa', 0))

    def test_match_same_with_one_t_should_return_true(self):
        self.assertTrue(match('aaa', 'aaa', 1))

    def test_match_one_diff_with_one_t_should_return_true(self):
        self.assertTrue(match('aaa', 'aab', 1))

    def test_match_one_diff_with_zero_t_should_return_false(self):
        self.assertFalse(match('aaa', 'aab', 0))

class GetStartPositionOfPreviousWordClass(TestCase):
    def test_point_ccc_should_return_bbb_start(self):
        self.assertEqual(
            get_start_position_of_previous_word(
                'aaa bbb ccc ddd eee', len('aaa bbb cc')-1),
            len('aaa b')-1
        )
    
    def test_point_bbb_should_return_aaa_start(self):
        self.assertEqual(
            get_start_position_of_previous_word(
                'aaa bbb ccc ddd eee', len('aaa bb')-1),
            0
        )
    
    def test_point_aaa_should_return_aaa_start(self):
        self.assertEqual(
            get_start_position_of_previous_word(
                'aaa bbb ccc ddd eee',
                len('aa')-1),
            0
        )

class GetEndPositionOfNextWordClass(TestCase):
    def test_point_ccc_should_return_one_after_end_of_ddd(self):
        self.assertEqual(
            get_end_position_of_next_word(
                'aaa bbb ccc ddd eee', len('aaa bbb cc')-1),
            len('aaa bbb ccc ddd')
        )
    
    def test_point_ddd_should_return_one_after_end_of_eee(self):
        self.assertEqual(
            get_end_position_of_next_word(
                'aaa bbb ccc ddd eee', len('aaa bbb ccc dd')-1),
            len('aaa bbb ccc ddd eee')
        )

    def test_point_eee_should_return_one_after_end_of_eee(self):
        self.assertEqual(
            get_end_position_of_next_word(
                'aaa bbb ccc ddd eee', len('aaa bbb ccc ddd ee')-1),
            len('aaa bbb ccc ddd eee')
        )

class IsTLDClass(TestCase):
    def test_com_should_be_tld(self):
        self.assertEqual(is_tld('com'), 'com')

class FindAnyClass(TestCase):
    def test_find_bbb_ddd_should_return_start_of_bbb(self):
        self.assertEqual(
            find_any('aaa bbb ccc ddd eee', ['bbb', 'ddd']),
            len('aaa b')-1
        )

    def test_find_ccc_ddd_eee_from_end_of_ccc_should_return_start_of_ddd(self):
        self.assertEqual(
            find_any('aaa bbb ccc ddd eee', ['ccc', 'ddd', 'eee'],
                len('aaa bbb ccc')),
            len('aaa bbb ccc d')-1
        )

class GetFirstWordTestCase(TestCase):
    def test_two_words_should_return_first(self):
        self.assertEqual(get_first_word('aaa bbb'), 'aaa')

    def test_one_word_should_return_first(self):
        self.assertEqual(get_first_word('aaa'), 'aaa')

    def test_one_word_after_space_should_return_none(self):
        self.assertEqual(get_first_word(' bbb'), None)

    def test_space_should_return_none(self):
        self.assertEqual(get_first_word(' '), None)

    def test_empty_should_return_none(self):
        self.assertEqual(get_first_word(''), None)

class GetThisWordTestClass(TestCase):
    def test_get_bbb_should_return_bbb(self):
        self.assertEqual(
            get_this_word('aaa bbb ccc', len('aaa bb')-1),
            ('bbb', 'aaa bbb ccc'.find('bbb'),
                'aaa bbb ccc'.find('bbb')+len('bbb'))
        )

    def test_get_aaa_should_return_aaa(self):
        self.assertEqual(
            get_this_word('aaa bbb ccc', len('aa')-1),
            ('aaa', 'aaa bbb ccc'.find('aaa'),
                'aaa bbb ccc'.find('aaa')+len('aaa'))
        )

    def test_get_ccc_should_return_ccc(self):
        self.assertEqual(
            get_this_word('aaa bbb ccc', len('aaa bbb cc')-1),
            ('ccc', 'aaa bbb ccc'.find('ccc'),
                'aaa bbb ccc'.find('ccc')+len('ccc'))
        )

class HasTagDotDomainClass(TestCase):
    def test_has_tag_only_should_return_true(self):
        self.assertTrue(has_tag_dot_domain(TAGS['DOT__DOMAIN__STARTEND']))

    def test_has_tag_in_text_should_return_true(self):
        self.assertTrue(has_tag_dot_domain(
            'aaa' + TAGS['DOT__DOMAIN__STARTEND'] + 'bbb'))

    def test_has_not_tag_in_text_should_return_false(self):
        self.assertFalse(has_tag_dot_domain('aaa bbb'))

    def test_has_no_text_should_return_false(self):
        self.assertFalse(has_tag_dot_domain(''))

class MarkStringTestCase(TestCase):
    def test_mark_string_in_middle_should_be_correct(self):
        target_string = 'aaa ' + TAGS['TESTING_ONLY__START'] + 'bbb' + \
            TAGS['TESTING_ONLY__END'] + ' ccc'
        target_pos = len('aaa ' + TAGS['TESTING_ONLY__START'] + 'bbb' + \
            TAGS['TESTING_ONLY__END'])

        self.assertEquals(
            mark_string(
                'aaa bbb ccc', # string
                len('aaa b')-1, # start_pos
                len('aaa bbb'), # end_pos
                TAGS['TESTING_ONLY__START'], # start_tag
                TAGS['TESTING_ONLY__END']), # end_tag
            (target_string, target_pos)
        )

    def test_mark_string_at_start_should_be_correct(self):
        target_string = TAGS['TESTING_ONLY__START'] + 'aaa' + \
            TAGS['TESTING_ONLY__END'] + ' bbb ccc'
        target_pos = len(TAGS['TESTING_ONLY__START'] + 'aaa' + \
            TAGS['TESTING_ONLY__END'])

        self.assertEquals(
            mark_string(
                'aaa bbb ccc', # string
                len('a')-1, # start_pos
                len('aaa'), # end_pos
                TAGS['TESTING_ONLY__START'], # start_tag
                TAGS['TESTING_ONLY__END']), # end_tag
            (target_string, target_pos)
        )

    def test_mark_string_at_end_should_be_correct(self):
        target_string = 'aaa bbb ' + TAGS['TESTING_ONLY__START'] + 'ccc' + \
            TAGS['TESTING_ONLY__END']
        target_pos = len('aaa bbb ' + TAGS['TESTING_ONLY__START'] + 'ccc' + \
            TAGS['TESTING_ONLY__END'])

        self.assertEquals(
            mark_string('aaa bbb ccc', len('aaa bbb c')-1, len('aaa bbb ccc'),
                TAGS['TESTING_ONLY__START'], TAGS['TESTING_ONLY__END']),
            (target_string, target_pos)
        )

class MarkAroundSymbolClass(TestCase):

    # 'aaa bbb ccc'

    def test_marking_on_bbb_should_yield_aaabbbccc(self):
        target_string = TAGS['TESTING_ONLY__START'] + 'aaa bbb ccc' + \
            TAGS['TESTING_ONLY__END']
        target_pos = len(target_string)

        self.assertEquals(
            mark_around_symbol(
                len('aaa b')-1, # symbol_pos
                len('bbb'), # symbol_len
                'aaa bbb ccc', # text
                TAGS['TESTING_ONLY__START'], # start_tag
                TAGS['TESTING_ONLY__END']), # end_tag
            (target_string, target_pos)
        )

    def test_marking_on_aaa_should_yield_aaabbb(self):
        target_string = TAGS['TESTING_ONLY__START'] + 'aaa bbb' + \
            TAGS['TESTING_ONLY__END'] + ' ccc'
        target_pos = len(TAGS['TESTING_ONLY__START'] + 'aaa bbb' + \
            TAGS['TESTING_ONLY__END'])

        self.assertEquals(
            mark_around_symbol(
                len('a')-1, # symbol_pos
                len('aaa'), # symbol_len
                'aaa bbb ccc', # text
                TAGS['TESTING_ONLY__START'], # start_tag
                TAGS['TESTING_ONLY__END']), # end_tag
            (target_string, target_pos)
        )
    
    def test_marking_on_ccc_should_yield_bbbccc(self):
        target_string = 'aaa ' + TAGS['TESTING_ONLY__START'] + 'bbb ccc' + \
            TAGS['TESTING_ONLY__END']
        target_pos = len(target_string)

        self.assertEquals(
            mark_around_symbol(
                len('aaa bbb c')-1, # symbol_pos
                len('ccc'), # symbol_len
                'aaa bbb ccc', # text
                TAGS['TESTING_ONLY__START'], # start_tag
                TAGS['TESTING_ONLY__END']), # end_tag
            (target_string, target_pos)
        )

    # 'aaa bbbcccddd eee'

    def test_marking_on_ccc_should_yield_bbbcccddd(self):
        target_string = 'aaa ' + TAGS['TESTING_ONLY__START'] + 'bbbcccddd' + \
            TAGS['TESTING_ONLY__END'] + ' eee'
        target_pos = len('aaa ' + TAGS['TESTING_ONLY__START'] + 'bbbcccddd' + \
            TAGS['TESTING_ONLY__END'])

        self.assertEquals(
            mark_around_symbol(
                len('aaa bbbc')-1, # symbol_pos
                len('ccc'), # symbol_len
                'aaa bbbcccddd eee', # text
                TAGS['TESTING_ONLY__START'], # start_tag
                TAGS['TESTING_ONLY__END']), # end_tag
            (target_string, target_pos)
        )

    def test_marking_on_bbb_should_yield_aaabbbcccddd(self):
        target_string = TAGS['TESTING_ONLY__START'] + 'aaa bbbcccddd' + \
            TAGS['TESTING_ONLY__END'] + ' eee'
        target_pos = len(TAGS['TESTING_ONLY__START'] + 'aaa bbbcccddd' + \
            TAGS['TESTING_ONLY__END'])

        self.assertEquals(
            mark_around_symbol(
                len('aaa b')-1, # symbol_pos
                len('bbb'), # symbol_len
                'aaa bbbcccddd eee', # text
                TAGS['TESTING_ONLY__START'], # start_tag
                TAGS['TESTING_ONLY__END']), # end_tag
            (target_string, target_pos)
        )