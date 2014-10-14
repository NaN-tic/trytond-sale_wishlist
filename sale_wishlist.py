#This file is part of sale_wishlist module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateAction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.pyson import PYSONEncoder

import sys

__all__ = ['SaleWishlist', 'WishlistCreateSale']


class SaleWishlist(ModelSQL, ModelView):
    'Sale Wish List'
    __name__ = 'sale.wishlist'
    _rec_name = 'product'
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
        cls._sql_constraints += [
            ('wishlist_uniq', 'UNIQUE(party, product)',
                'A product must be unique for a party.'),
            ]
        cls._error_messages.update({
            'add_party': ('Add a party in wishlist ID "%s".'),
            })

    @staticmethod
    def default_quantity():
        return 1

    @classmethod
    def create_sale(cls, wishlists, values={}):
        '''
        Create sale from wishlists
        :param wishlists: list
        :param values: dict default values
        return obj list, error
        '''
        pool = Pool()
        Sale = pool.get('sale.sale')
        SaleLine = pool.get('sale.line')

        wishlist_group = {}
        sales = set()

        # Group wishlists in party
        for wishlist in wishlists:
            if not wishlist.party:
                cls.raise_user_error('add_party', (wishlist.id,))

            if not wishlist.party in wishlist_group:
                wishlist_group[wishlist.party] = [{
                    'product': wishlist.product,
                    'quantity': wishlist.quantity,
                    }]
            else:
                lines = wishlist_group.get(wishlist.party)
                lines.append({
                    'product': wishlist.product,
                    'quantity': wishlist.quantity,
                })
                wishlist_group[wishlist.party] = lines

        # Create sale and sale lines
        for party, lines in wishlist_group.iteritems():
            sale = Sale.get_sale_data(party)
            if values:
                for k, v in values.iteritems():
                    setattr(sale, k, v)
            try:
                sale.save()
            except:
                exc_type, exc_value = sys.exc_info()[:2]
                return [], exc_value
            sales.add(sale)

            for line in lines:
                sale_line = SaleLine.get_sale_line_data(sale,
                    line.get('product'), line.get('quantity'))
                sale_line.save()

        return sales, None


class WishlistCreateSale(Wizard):
    'Create Sale from Wish List'
    __name__ = 'wishlist.create_sale'
    start_state = 'create_sale'
    create_sale = StateTransition()
    open_ = StateAction('sale.act_sale_form')

    def transition_create_sale(self):
        Wishlist = Pool().get('sale.wishlist')
        wishlists = Wishlist.browse(Transaction().context['active_ids'])
        self.sales = Wishlist.create_sale(wishlists)
        return 'open_'

    def do_open_(self, action):
        sales, _ = self.sales
        ids = [sale.id for sale in list(sales)]
        action['pyson_domain'] = PYSONEncoder().encode(
            [('id', 'in', ids)])
        return action, {}
