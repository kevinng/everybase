from django.test import TestCase
from processor.libraries.constants import (_TAG__TESTING_ONLY__START,
    _TAG__TESTING_ONLY__END)
from processor.libraries.marking import (mark_string)

class MarkStringTestCase(TestCase):
    def test_mark_string_in_middle_should_be_correct(self):
        self.assertEquals(
            mark_string('aaa bbb ccc', len('aaa b')-1, len('aaa bbb'),
                _TAG__TESTING_ONLY__START, _TAG__TESTING_ONLY__END),
            ('aaa ' + _TAG__TESTING_ONLY__START + 'bbb' + \
                _TAG__TESTING_ONLY__END + ' ccc',
                len('aaa ' + _TAG__TESTING_ONLY__START + 'bbb' + \
                    _TAG__TESTING_ONLY__END))
        )

    def test_mark_string_at_start_should_be_correct(self):
        self.assertEquals(
            mark_string('aaa bbb ccc', len('a')-1, len('aaa'),
                _TAG__TESTING_ONLY__START, _TAG__TESTING_ONLY__END),
            (_TAG__TESTING_ONLY__START + 'aaa' + \
                _TAG__TESTING_ONLY__END + ' bbb ccc',
                len(_TAG__TESTING_ONLY__START + 'aaa' + \
                    _TAG__TESTING_ONLY__END))
        )

    def test_mark_string_at_end_should_be_correct(self):
        self.assertEquals(
            mark_string('aaa bbb ccc', len('aaa bbb c')-1, len('aaa bbb ccc'),
                _TAG__TESTING_ONLY__START, _TAG__TESTING_ONLY__END),
            ('aaa bbb ' + _TAG__TESTING_ONLY__START + 'ccc' + \
                _TAG__TESTING_ONLY__END,
                len('aaa bbb ' + _TAG__TESTING_ONLY__START + 'ccc' + \
                    _TAG__TESTING_ONLY__END))
        )