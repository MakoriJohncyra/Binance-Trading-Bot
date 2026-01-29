"""
This file checks if user inputs are valid before we use them.
Think of it as a security guard checking IDs at the door.
"""

import re

class Validator:
    """
    A class with tools to check if user inputs are valid.
    """
    
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Check if trading pair symbol is valid.
        Example: BTCUSDT is valid, BTC-USD is not.
        
        Rules:
        1. Only uppercase letters and numbers
        2. 5-12 characters long
        3. No special characters
        """
        symbol = symbol.upper().strip()  # Convert to uppercase and remove spaces
        
        # Define pattern: only letters and numbers, 5-12 characters
        pattern = r'^[A-Z0-9]{5,12}$'
        
        if not re.match(pattern, symbol):
            raise ValueError(f"Invalid symbol: {symbol}. Must be like 'BTCUSDT', 'ETHUSDT'")
        
        return symbol
    
    @staticmethod
    def validate_side(side: str) -> str:
        """
        Check if trading side is valid. Must be BUY or SELL.
        """
        side = side.upper().strip()
        
        if side not in ['BUY', 'SELL']:
            raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'")
        
        return side
    
    @staticmethod
    def validate_order_type(order_type: str) -> str:
        """
        Check if order type is valid. Must be MARKET or LIMIT.
        """
        order_type = order_type.upper().strip()
        
        if order_type not in ['MARKET', 'LIMIT']:
            raise ValueError(f"Invalid order type: {order_type}. Must be 'MARKET' or 'LIMIT'")
        
        return order_type
    
    @staticmethod
    def validate_quantity(quantity: str) -> float:
        """
        Check if quantity is a valid positive number.
        
        Example valid: "0.001", "1", "10.5"
        Example invalid: "0", "-1", "abc"
        """
        try:
            # Try to convert to float
            qty = float(quantity)
            
            # Check if positive
            if qty <= 0:
                raise ValueError("Quantity must be greater than 0")
            
            # Check if too small (Binance minimum is usually 0.001 for BTC)
            if qty < 0.001:
                print(f"Warning: Quantity {qty} might be too small for some symbols")
            
            return qty
            
        except ValueError:
            # If conversion fails or value is invalid
            raise ValueError(f"Invalid quantity: {quantity}. Must be a positive number")
    
    @staticmethod
    def validate_price(price: str) -> float:
        """
        Check if price is a valid positive number.
        """
        try:
            p = float(price)
            
            if p <= 0:
                raise ValueError("Price must be greater than 0")
            
            return p
            
        except ValueError:
            raise ValueError(f"Invalid price: {price}. Must be a positive number")