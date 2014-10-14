#This file is part sale_wishlist module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from .sale_wishlist import *

def register():
    Pool.register(
        SaleWishlist,
        module='sale_wishlist', type_='model')
    Pool.register(
        WishlistCreateSale,
        module='sale_wishlist', type_='wizard')
