# This file is part of sale_wishlist module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields, Unique


class SaleWishlist(ModelSQL, ModelView):
    'Sale Wish List'
    __name__ = 'sale.wishlist'

    party = fields.Many2One('party.party', 'Party', required=True)
    quantity = fields.Float('Quantity',
        digits=(16, 2), required=True)
    product = fields.Many2One('product.product', 'Product',
        domain=[('salable', '=', True)], required=True,
        context={
            'salable': True,
            })

    @classmethod
    def __setup__(cls):
        super(SaleWishlist, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
            ('wishlist_uniq', Unique(t, t.party, t.product),
                'A product must be unique for a party.'),
            ]

    @staticmethod
    def default_quantity():
        return 1

    def get_rec_name(self, name):
        if self.product:
            return self.product.rec_name
