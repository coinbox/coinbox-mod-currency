__all__ = ('convert', 'default', 'round_units', 'decompose')

from .form import *

import cbpos
logger = cbpos.get_logger(__name__)

def convert(price_in_src, src, dst):
    if price_in_src == 0:
        return 0
    
    if src == dst:
        return price_in_src
    
    logger.debug(u'Converting {} from {} to {}'.format(repr(price_in_src), src, dst))
    
    price_in_dst = price_in_src * src.current_rate.reference_to_currency_ratio * dst.current_rate.currency_to_reference_ratio
    
    logger.debug(u'Price in {}: {}'.format(dst, repr(price_in_dst)))

    return price_in_dst

_default_cache = None
def get_default():
    global _default_cache
    if _default_cache is None:
        currency_id = cbpos.config['mod.currency', 'default']
        currency_id = None if currency_id == '' else currency_id
        
        session = cbpos.database.session()
        if currency_id is not None:
            _default_cache = (currency_id, session.query(Currency).filter_by(id=currency_id).one())
        else:
            _default_cache = (None, session.query(Currency).first())
    return _default_cache[1]

from peak.util.proxies import ObjectProxy, CallbackProxy
#import weakref
default = CallbackProxy(get_default)
#default = weakref.proxy(get_default)

def round_units(price, currency):
    unit = min(currency.units).value
    remainder = price%unit
    return price+(unit-remainder if remainder != 0 else 0)

def decompose(price, currency):
    remainder = price
    units = []
    while remainder>0:
        biggest = (u for u in sorted(currency.units, reverse=True) if u.value<=remainder)
        try:
            u = biggest.next()
        except StopIteration:
            u = min(currency.units)
        remainder -= u.value
        units.append(u)
    return units
