from decimal import Decimal

def convert(val: float or int) -> str:
    
    val = Decimal(val).quantize(Decimal('0.00'))
    val = str(val).replace('.',',')
    
    return val
