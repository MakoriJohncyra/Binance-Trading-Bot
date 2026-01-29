#!/usr/bin/env python3
"""
TRADING BOT - Command Line Interface
This is the main file users run to place orders.
Think of it as the control panel for our trading bot.
"""

import argparse
import os
import sys
from dotenv import load_dotenv

# Import our custom modules
from bot.client import BinanceFuturesClient
from bot.validators import Validator
from bot.logging_config import setup_logging

# Import logging
import logging

# Load environment variables from .env file
load_dotenv()

# Setup logging (our program's diary)
logger = setup_logging()

def print_banner():
    """Print a nice welcome banner"""
    print("\n" + "="*60)
    print("           BINANCE FUTURES TRADING BOT")
    print("                 (TESTNET MODE)")
    print("="*60)

def print_order_summary(symbol, side, order_type, quantity, price=None):
    """Print a summary of the order before placing it"""
    print("\n ORDER SUMMARY:")
    print("-" * 40)
    print(f"   Symbol:       {symbol}")
    print(f"   Side:         {side}")
    print(f"   Order Type:   {order_type}")
    print(f"   Quantity:     {quantity}")
    if price:
        print(f"   Price:        ${price}")
    print("-" * 40)
    
    # Ask for confirmation
    confirm = input("\n  Confirm this order? (yes/no): ").lower()
    return confirm == 'yes'

def print_order_result(order_response):
    """Print the result of the placed order"""
    print("\n ORDER PLACED SUCCESSFULLY!")
    print("="*50)
    print(f"   Order ID:     {order_response.get('orderId')}")
    print(f"   Status:       {order_response.get('status')}")
    print(f"   Executed Qty: {order_response.get('executedQty', '0')}")
    print(f"   Avg Price:    ${order_response.get('avgPrice', 'N/A')}")
    print("="*50)
    
    # Give some advice based on order type
    if order_response.get('type') == 'LIMIT':
        print("\n Your limit order is now active!")
        print("   It will execute when the market reaches your price.")
    else:
        print("\n Market order executed immediately!")

def main():
    """
    Main function - the starting point of our program.
    This handles command line arguments and orchestrates everything.
    """
    print_banner()
    
    # Setup command line argument parser
    parser = argparse.ArgumentParser(
        description='Place orders on Binance Futures Testnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Market order (buy immediately)
  python cli.py BTCUSDT BUY MARKET 0.001
  
  # Limit order (buy at specific price)
  python cli.py ETHUSDT SELL LIMIT 0.1 --price 2500
  
  # Get help
  python cli.py --help
        """
    )
    
    # Define command line arguments
    parser.add_argument(
        'symbol',
        help='Trading pair symbol (e.g., BTCUSDT, ETHUSDT)'
    )
    
    parser.add_argument(
        'side',
        help='BUY or SELL'
    )
    
    parser.add_argument(
        'order_type',
        help='MARKET or LIMIT'
    )
    
    parser.add_argument(
        'quantity',
        help='Amount to trade (e.g., 0.001 for BTC)'
    )
    
    parser.add_argument(
        '--price',
        type=float,
        help='Price for LIMIT orders (required for LIMIT)'
    )
    
    # Parse arguments from command line
    args = parser.parse_args()
    
    try:
        logger.info("Starting order placement process...")
        
        # STEP 1: Validate all inputs using our Validator class
        print("\n Validating inputs...")
        try:
            symbol = Validator.validate_symbol(args.symbol)
            side = Validator.validate_side(args.side)
            order_type = Validator.validate_order_type(args.order_type)
            quantity = Validator.validate_quantity(args.quantity)
            
            # Special check for LIMIT orders
            if order_type == 'LIMIT':
                if not args.price:
                    raise ValueError(" Price is required for LIMIT orders!")
                price = Validator.validate_price(str(args.price))
            else:
                price = None
                
            print(" All inputs validated successfully!")
            
        except ValueError as e:
            # If validation fails, show error and exit
            logger.error(f"Input validation failed: {str(e)}")
            print(f"\n Error: {str(e)}")
            print("\n Tip: Use --help to see examples")
            return 1
        
        # STEP 2: Get API credentials
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            print("\n API credentials not found!")
            print("   Please create a '.env' file with:")
            print("   BINANCE_API_KEY=your_key_here")
            print("   BINANCE_API_SECRET=your_secret_here")
            print("\n   See '.env.example' for an example.")
            return 1
        
        # STEP 3: Show order summary and ask for confirmation
        if not print_order_summary(symbol, side, order_type, quantity, price):
            print("\n Order cancelled by user.")
            return 0
        
        # STEP 4: Connect to Binance
        print("\n Connecting to Binance...")
        try:
            client = BinanceFuturesClient(api_key, api_secret)
            print(" Connected to Binance Testnet!")
        except Exception as e:
            print(f"\n Failed to connect to Binance: {str(e)}")
            print("\n Check your API credentials and internet connection")
            return 1
        
        # STEP 5: Place the order
        print(f"\n Placing {order_type} order...")
        try:
            if order_type == 'MARKET':
                response = client.place_market_order(symbol, side, quantity)
            else:  # LIMIT order
                response = client.place_limit_order(symbol, side, quantity, price)
            
            # STEP 6: Show results
            print_order_result(response)
            
            logger.info(f"Order {response.get('orderId')} placed successfully")
            return 0
            
        except Exception as e:
            print(f"\n Failed to place order: {str(e)}")
            logger.error(f"Order placement failed: {str(e)}")
            return 1
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n  Operation cancelled by user.")
        return 0
    
    except Exception as e:
        # Catch any other unexpected errors
        print(f"\n Unexpected error: {str(e)}")
        logger.error(f"Unexpected error in main: {str(e)}")
        return 1

# This makes the file executable
if __name__ == "__main__":
    sys.exit(main())