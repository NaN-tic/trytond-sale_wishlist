# This file is part sale_wishlist module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import sale_wishlist

def register():
    Pool.register(
        sale_wishlist.SaleWishlist,
        module='sale_wishlist', type_='model')
    Pool.register(
        sale_wishlist.WishlistCreateSale,
        module='sale_wishlist', type_='wizard')
