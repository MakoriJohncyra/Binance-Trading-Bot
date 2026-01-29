"""
This file handles communication with Binance.
Think of it as a messenger who delivers your orders to the exchange.
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging

# Get our program's diary
logger = logging.getLogger('trading_bot.client')

class BinanceFuturesClient:
    """
    A client to communicate with Binance Futures Testnet.
    This is like having a personal assistant for Binance trading.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the connection to Binance.
        
        Parameters:
        - api_key: Your Binance API key (like username)
        - api_secret: Your Binance API secret (like password)
        - testnet: Whether to use test server (True) or real server (False)
        """
        logger.info("Starting Binance Futures client...")
        
        try:
            # Create Binance client with our credentials
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet  # Always True for practice mode
            )
            logger.info(" Binance client connected successfully!")
            
        except Exception as e:
            logger.error(f" Failed to connect to Binance: {str(e)}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float):
        """
        Place a MARKET order (buys/sells immediately at current price).
        
        Example: "Buy 0.001 BTC right now at whatever price it is"
        
        Parameters:
        - symbol: Trading pair like "BTCUSDT"
        - side: "BUY" or "SELL"
        - quantity: How much to buy/sell
        """
        try:
            logger.info(f" Placing MARKET order: {side} {quantity} {symbol}")
            
            # Send order to Binance
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),  # Convert to uppercase
                type='MARKET',      # Market order type
                quantity=quantity   # How much to trade
            )
            
            logger.info(f" Market order placed! Order ID: {order.get('orderId')}")
            return order
            
        except BinanceAPIException as e:
            # Handle Binance-specific errors
            error_msg = f"Binance API Error: {e.message} (Error code: {e.code})"
            logger.error(error_msg)
            raise Exception(error_msg)
            
        except Exception as e:
            # Handle any other errors
            error_msg = f"Unexpected error placing market order: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        """
        Place a LIMIT order (sets specific price to buy/sell).
        
        Example: "Buy 0.001 BTC only if price drops to $50,000"
        
        Parameters:
        - symbol: Trading pair
        - side: "BUY" or "SELL"
        - quantity: How much to trade
        - price: At what price to execute
        """
        try:
            logger.info(f" Placing LIMIT order: {side} {quantity} {symbol} @ ${price}")
            
            # Send order to Binance
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce='GTC'  # Good Till Cancelled (order stays until filled or cancelled)
            )
            
            logger.info(f" Limit order placed! Order ID: {order.get('orderId')}")
            return order
            
        except BinanceAPIException as e:
            error_msg = f"Binance API Error: {e.message} (Error code: {e.code})"
            logger.error(error_msg)
            raise Exception(error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error placing limit order: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def get_order_status(self, symbol: str, order_id: int):
        """
        Check the status of an order.
        
        Useful to see if order was filled, cancelled, or still waiting.
        """
        try:
            logger.info(f" Checking order status for ID: {order_id}")
            order_status = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order status: {order_status.get('status')}")
            return order_status
            
        except Exception as e:
            logger.error(f"Failed to check order status: {str(e)}")
            return None