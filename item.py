class Item:

    def __init__(self, quantity: int, detail: str, price: float, aliquot: float = None) -> None:
        # Assing
        self.quantity = quantity
        self.detail = detail
        self.price = price        
        self.aliquot = aliquot if aliquot != None else 21
        
        # Calculate
        self.tribute = price * (self.aliquot/100) * float(self.quantity) if self.aliquot else 0
        self.total = (price + price * (self.aliquot/100)) * float(self.quantity) if self.aliquot else price * float(self.quantity)