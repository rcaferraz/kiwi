bl
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import gobject

from kiwi import ValueUnset
from kiwi import datatypes
from kiwi.ui.entry import KiwiEntry
from kiwi.ui.widgets.entry import ProxyEntry

import utils

class EntryTest(unittest.TestCase):
    def testModel(self):
        entry = ProxyEntry()
        entry.set_text('value')
        entry.set_property("data-type", "str")
        self.assertEqual(entry.read(), 'value')

    # FIXME
    def _testValidDataType(self):

        entry = ProxyEntry()
        entry.set_property("data-type", "date")
        # let's make the entry complain!
        entry.set_text("string")
        self.assertEqual(entry.read(), ValueUnset)
        self.assertNotEqual(entry._complaint_checker_id, -1)

        # now let's put proper data
        entry.set_text(self.date_format)
        date = datatypes.date2str(entry.read())
        self.assertEqual(date, self.date_format)
        self.assertEqual(entry._background_timeout_id, -1)

        locale_dictionary = datatypes.locale_dictionary

        # now change the data-type and do it again
        entry.set_property("data-type", "float")
        if locale_dictionary["thousands_sep"] == ',':
            # correct value
            entry.set_text("23,400,000.2")
            self.assertEqual(entry.read(), 23400000.2)
            self.assertEqual(entry._background_timeout_id, -1)

            # wrong value
            entry.set_text("23.400.000,2")
            self.assertEqual(entry.read(), ValueUnset)

    def testDigitMask(self):
        e = ProxyEntry()
        e.set_mask('000.000')
        self.assertEqual(e.get_text(), '   .   ')
        self.assertEqual(e.get_field_text(), [None, None])
        e.set_text('123.456')
        self.assertEqual(e.get_text(), '123.456')
        self.assertEqual(e.get_field_text(), [123, 456])
        e.delete_text(0, 2)
        self.assertEqual(e.get_text(), '  3.456')
        self.assertEqual(e.get_field_text(), [3, 456])

    def testAsciiMask(self):
        e = ProxyEntry()
        e.set_mask('LLLL-L')
        self.assertEqual(e.get_text(), '    - ')
        self.assertEqual(e.get_field_text(), ['', ''])
        e.set_text('abcd-e')
        self.assertEqual(e.get_text(), 'abcd-e')
        self.assertEqual(e.get_field_text(), ['abcd', 'e'])

    def testAlphaNumericMask(self):
        e = ProxyEntry()
        e.set_mask('&&&-aaa')
        self.assertEqual(e.get_text(), '   -   ')
        self.assertEqual(e.get_field_text(), ['', ''])
        e.set_text('aáé-á1e')
        self.assertEqual(e.get_text(), 'aáé-á1e')
        self.assertEqual(e.get_field_text(), ['aáé', 'á1e'])

    def testMaskSmallFields(self):
        e = ProxyEntry()
        e.set_mask('0.0.0')
        self.assertEqual(e.get_text(), ' . . ')
        self.assertEqual(e.get_field_text(), [None, None, None])
        e.set_text('1.2.3')
        self.assertEqual(e.get_text(), '1.2.3')
        self.assertEqual(e.get_field_text(), [1, 2, 3])

    def testGType(self):
        entry = KiwiEntry()
        self.assertEqual(gobject.type_name(entry), 'KiwiEntry')

        entry = ProxyEntry()
        self.assertEqual(gobject.type_name(entry), 'ProxyEntry')

if __name__ == '__main__':
    unittest.main()
