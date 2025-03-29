"""
HashScope LangChain Tools

This module provides LangChain tools for interacting with the HashScope API.
"""

from typing import Dict, Any, List, Optional
from langchain.tools import BaseTool, StructuredTool, Tool
from langchain.pydantic_v1 import BaseModel, Field
from .hashscope_client import HashScopeClient

class HashScopeToolkit:
    """
    Toolkit for HashScope API tools.
    """
    
    def __init__(self, api_key_id: str, api_key_secret: str, base_url: str = "https://api.hashscope.io"):
        """
        Initialize the HashScope toolkit.
        
        Args:
            api_key_id: The API key ID
            api_key_secret: The API key secret
            base_url: The base URL for the HashScope API (default: https://api.hashscope.io)
        """
        self.client = HashScopeClient(api_key_id, api_key_secret, base_url)
        
    def get_tools(self) -> List[BaseTool]:
        """
        Get all available HashScope tools.
        
        Returns:
            A list of LangChain tools
        """
        return [
            get_crypto_price_tool(self.client),
            get_crypto_historical_prices_tool(self.client),
            get_market_data_tool(self.client),
            get_trending_coins_tool(self.client),
            get_onchain_data_tool(self.client),
            get_wallet_balance_tool(self.client),
            get_social_sentiment_tool(self.client),
            get_news_tool(self.client),
        ]


# Tool Input Schemas
class CryptoPriceInput(BaseModel):
    symbol: str = Field(..., description="The cryptocurrency symbol (e.g., BTC, ETH)")
    currency: str = Field(default="USD", description="The currency to convert to (default: USD)")

class HistoricalPricesInput(BaseModel):
    symbol: str = Field(..., description="The cryptocurrency symbol (e.g., BTC, ETH)")
    currency: str = Field(default="USD", description="The currency to convert to (default: USD)")
    interval: str = Field(default="1d", description="The time interval (e.g., 1h, 1d, 1w)")
    limit: int = Field(default=30, description="The number of data points to return (default: 30)")

class MarketDataInput(BaseModel):
    symbol: str = Field(..., description="The cryptocurrency symbol (e.g., BTC, ETH)")

class TrendingCoinsInput(BaseModel):
    limit: int = Field(default=10, description="The number of trending coins to return (default: 10)")

class OnchainDataInput(BaseModel):
    symbol: str = Field(..., description="The cryptocurrency symbol (e.g., BTC, ETH)")
    metric: str = Field(..., description="The on-chain metric to retrieve (e.g., active_addresses, transaction_count)")

class WalletBalanceInput(BaseModel):
    address: str = Field(..., description="The wallet address")
    chain: str = Field(..., description="The blockchain (e.g., ethereum, bitcoin)")

class SocialSentimentInput(BaseModel):
    symbol: str = Field(..., description="The cryptocurrency symbol (e.g., BTC, ETH)")
    source: str = Field(default="all", description="The data source (e.g., twitter, reddit, all)")

class NewsInput(BaseModel):
    symbol: Optional[str] = Field(default=None, description="The cryptocurrency symbol (optional)")
    limit: int = Field(default=10, description="The number of news items to return (default: 10)")


# Tool Definitions
def get_crypto_price_tool(client: HashScopeClient) -> BaseTool:
    """Create a tool for getting cryptocurrency prices."""
    
    def _run(symbol: str, currency: str = "USD") -> str:
        try:
            result = client.get_crypto_price(symbol, currency)
            return f"Current price of {symbol} is {result['price']} {currency}. Last updated: {result['last_updated']}"
        except Exception as e:
            return f"Error fetching price: {str(e)}"
    
    return StructuredTool.from_function(
        func=_run,
        name="get_crypto_price",
        description="Get the current price of a cryptocurrency. Input should be the symbol (e.g., BTC, ETH) and optionally the currency (default: USD).",
        args_schema=CryptoPriceInput,
    )

def get_crypto_historical_prices_tool(client: HashScopeClient) -> BaseTool:
    """Create a tool for getting historical cryptocurrency prices."""
    
    def _run(symbol: str, currency: str = "USD", interval: str = "1d", limit: int = 30) -> str:
        try:
            result = client.get_crypto_historical_prices(symbol, currency, interval, limit)
            prices = result['prices']
            summary = f"Historical prices for {symbol} ({currency}) with {interval} interval (last {len(prices)} data points):\n"
            
            # Format a summary of the data
            for i, price_data in enumerate(prices[:5]):
                summary += f"- {price_data['date']}: {price_data['price']} {currency}\n"
            
            if len(prices) > 5:
                summary += f"... and {len(prices) - 5} more data points\n"
                
            summary += f"\nPrice change: {result['price_change_percentage']}%"
            return summary
        except Exception as e:
            return f"Error fetching historical prices: {str(e)}"
    
    return StructuredTool.from_function(
        func=_run,
        name="get_crypto_historical_prices",
        description="Get historical prices of a cryptocurrency. Input should include the symbol, and optionally currency, interval, and limit.",
        args_schema=HistoricalPricesInput,
    )

def get_market_data_tool(client: HashScopeClient) -> BaseTool:
    """Create a tool for getting cryptocurrency market data."""
    
    def _run(symbol: str) -> str:
        try:
            result = client.get_market_data(symbol)
            return (f"Market data for {symbol}:\n"
                   f"- Market Cap: ${result['market_cap']:,}\n"
                   f"- 24h Volume: ${result['volume_24h']:,}\n"
                   f"- Circulating Supply: {result['circulating_supply']:,} {symbol}\n"
                   f"- Max Supply: {result['max_supply']:,} {symbol}\n"
                   f"- Rank: #{result['market_cap_rank']}")
        except Exception as e:
            return f"Error fetching market data: {str(e)}"
    
    return StructuredTool.from_function(
        func=_run,
        name="get_crypto_market_data",
        description="Get market data for a cryptocurrency including market cap, volume, and supply information.",
        args_schema=MarketDataInput,
    )

def get_trending_coins_tool(client: HashScopeClient) -> BaseTool:
    """Create a tool for getting trending cryptocurrencies."""
    
    def _run(limit: int = 10) -> str:
        try:
            result = client.get_trending_coins(limit)
            coins = result['coins']
            
            response = f"Top {len(coins)} trending cryptocurrencies:\n"
            for i, coin in enumerate(coins, 1):
                response += f"{i}. {coin['name']} ({coin['symbol']}): ${coin['price']} ({coin['price_change_24h']}%)\n"
            
            return response
        except Exception as e:
            return f"Error fetching trending coins: {str(e)}"
    
    return StructuredTool.from_function(
        func=_run,
        name="get_trending_coins",
        description="Get a list of trending cryptocurrencies.",
        args_schema=TrendingCoinsInput,
    )

def get_onchain_data_tool(client: HashScopeClient) -> BaseTool:
    """Create a tool for getting on-chain data."""
    
    def _run(symbol: str, metric: str) -> str:
        try:
            result = client.get_onchain_data(symbol, metric)
            
            response = f"On-chain {metric} data for {symbol}:\n"
            if isinstance(result['data'], list):
                for item in result['data'][:5]:
                    response += f"- {item['date']}: {item['value']}\n"
                
                if len(result['data']) > 5:
                    response += f"... and {len(result['data']) - 5} more data points\n"
            else:
                response += f"Current value: {result['data']}\n"
            
            return response
        except Exception as e:
            return f"Error fetching on-chain data: {str(e)}"
    
    return StructuredTool.from_function(
        func=_run,
        name="get_crypto_onchain_data",
        description="Get on-chain data for a cryptocurrency. Available metrics include: active_addresses, transaction_count, transaction_volume, average_transaction_fee, mining_difficulty, etc.",
        args_schema=OnchainDataInput,
    )

def get_wallet_balance_tool(client: HashScopeClient) -> BaseTool:
    """Create a tool for getting wallet balance."""
    
    def _run(address: str, chain: str) -> str:
        try:
            result = client.get_wallet_balance(address, chain)
            
            response = f"Wallet balance for {address} on {chain}:\n"
            for token in result['tokens']:
                response += f"- {token['symbol']}: {token['balance']} (${token['usd_value']:,.2f})\n"
            
            response += f"\nTotal value: ${result['total_usd_value']:,.2f}"
            return response
        except Exception as e:
            return f"Error fetching wallet balance: {str(e)}"
    
    return StructuredTool.from_function(
        func=_run,
        name="get_wallet_balance",
        description="Get the balance of a wallet address on a specific blockchain.",
        args_schema=WalletBalanceInput,
    )

def get_social_sentiment_tool(client: HashScopeClient) -> BaseTool:
    """Create a tool for getting social sentiment data."""
    
    def _run(symbol: str, source: str = "all") -> str:
        try:
            result = client.get_social_sentiment(symbol, source)
            
            response = f"Social sentiment for {symbol} from {source}:\n"
            response += f"- Overall sentiment: {result['sentiment']}\n"
            response += f"- Positive: {result['positive_percentage']}%\n"
            response += f"- Neutral: {result['neutral_percentage']}%\n"
            response += f"- Negative: {result['negative_percentage']}%\n"
            
            if 'trending_topics' in result:
                response += "\nTrending topics:\n"
                for topic in result['trending_topics'][:5]:
                    response += f"- {topic}\n"
            
            return response
        except Exception as e:
            return f"Error fetching social sentiment: {str(e)}"
    
    return StructuredTool.from_function(
        func=_run,
        name="get_crypto_social_data",
        description="Get social sentiment data for a cryptocurrency from sources like Twitter, Reddit, etc.",
        args_schema=SocialSentimentInput,
    )

def get_news_tool(client: HashScopeClient) -> BaseTool:
    """Create a tool for getting cryptocurrency news."""
    
    def _run(symbol: Optional[str] = None, limit: int = 10) -> str:
        try:
            result = client.get_news(symbol, limit)
            
            if symbol:
                response = f"Latest {len(result['news'])} news for {symbol}:\n"
            else:
                response = f"Latest {len(result['news'])} cryptocurrency news:\n"
            
            for i, news in enumerate(result['news'], 1):
                response += f"{i}. {news['title']}\n"
                response += f"   Source: {news['source']} | Date: {news['date']}\n"
                response += f"   {news['summary'][:100]}...\n\n"
            
            return response
        except Exception as e:
            return f"Error fetching news: {str(e)}"
    
    return StructuredTool.from_function(
        func=_run,
        name="get_crypto_news",
        description="Get latest news for cryptocurrencies.",
        args_schema=NewsInput,
    )
