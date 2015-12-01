# This file is part of the sale_wishlist module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SaleWishlistTestCase(ModuleTestCase):
    'Test Sale Wishlist module'
    module = 'sale_wishlist'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        SaleWishlistTestCase))
    return suite