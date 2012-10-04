__all__ = ('convert', 'default', 'round_units', 'decompose')

def convert(price, src, dest):
    s_val = float(src.value)
    d_val = float(dest.value)
    #ps*vs = pd*vd

    return float(price)*s_val/d_val
    #return round(float(price)*s_val/d_val, dest_currency.decimal_places)

_default_cache = None
@property
def default():
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

def round_units(price, currency):
    unit = min(currency.units).value
    remainder = price%unit
    return float(price)+(unit-remainder if remainder != 0 else 0)

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
