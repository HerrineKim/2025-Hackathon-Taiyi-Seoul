"""
HashScope API Client

This module provides a client for interacting with the HashScope API.
"""

import requests
from typing import Dict, Any, Optional, List, Union
import json

class HashScopeClient:
    """
    Client for interacting with the HashScope API.
    """
    
    def __init__(self, api_key_id: str, api_key_secret: str, base_url: str = "https://api.hashscope.io"):
        """
        Initialize the HashScope API client.
        
        Args:
            api_key_id: The API key ID
            api_key_secret: The API key secret
            base_url: The base URL for the HashScope API (default: https://api.hashscope.io)
        """
        self.api_key_id = api_key_id
        self.api_key_secret = api_key_secret
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'api-key-id': api_key_id,
            'api-key-secret': api_key_secret,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                     data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the HashScope API.
        
        Args:
            method: The HTTP method to use
            endpoint: The API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            The API response as a dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.lower() == 'get':
                response = self.session.get(url, params=params)
            elif method.lower() == 'post':
                response = self.session.post(url, params=params, json=data)
            elif method.lower() == 'put':
                response = self.session.put(url, params=params, json=data)
            elif method.lower() == 'delete':
                response = self.session.delete(url, params=params, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('detail', str(e))
                except ValueError:
                    error_message = e.response.text or str(e)
            else:
                error_message = str(e)
            
            raise Exception(f"HashScope API error: {error_message}")
    
    # Crypto Price API
    def get_crypto_price(self, symbol: str, currency: str = "USD") -> Dict[str, Any]:
        """
        Get the current price of a cryptocurrency.
        
        Args:
            symbol: The cryptocurrency symbol (e.g., BTC, ETH)
            currency: The currency to convert to (default: USD)
            
        Returns:
            The current price data
        """
        return self._make_request('get', f'/crypto/price', params={'symbol': symbol, 'currency': currency})
    
    def get_crypto_historical_prices(self, symbol: str, currency: str = "USD", 
                                    interval: str = "1d", limit: int = 30) -> Dict[str, Any]:
        """
        Get historical prices of a cryptocurrency.
        
        Args:
            symbol: The cryptocurrency symbol (e.g., BTC, ETH)
            currency: The currency to convert to (default: USD)
            interval: The time interval (e.g., 1h, 1d, 1w)
            limit: The number of data points to return (default: 30)
            
        Returns:
            Historical price data
        """
        return self._make_request('get', f'/crypto/historical-prices', 
                                params={'symbol': symbol, 'currency': currency, 
                                        'interval': interval, 'limit': limit})
    
    # Market Data API
    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Get market data for a cryptocurrency.
        
        Args:
            symbol: The cryptocurrency symbol (e.g., BTC, ETH)
            
        Returns:
            Market data including volume, market cap, etc.
        """
        return self._make_request('get', f'/crypto/market-data', params={'symbol': symbol})
    
    def get_trending_coins(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get trending cryptocurrencies.
        
        Args:
            limit: The number of trending coins to return (default: 10)
            
        Returns:
            List of trending cryptocurrencies
        """
        return self._make_request('get', f'/crypto/trending', params={'limit': limit})
    
    # On-chain Data API
    def get_onchain_data(self, symbol: str, metric: str) -> Dict[str, Any]:
        """
        Get on-chain data for a cryptocurrency.
        
        Args:
            symbol: The cryptocurrency symbol (e.g., BTC, ETH)
            metric: The on-chain metric to retrieve (e.g., active_addresses, transaction_count)
            
        Returns:
            On-chain data for the specified metric
        """
        return self._make_request('get', f'/crypto/onchain', params={'symbol': symbol, 'metric': metric})
    
    def get_wallet_balance(self, address: str, chain: str) -> Dict[str, Any]:
        """
        Get the balance of a wallet address.
        
        Args:
            address: The wallet address
            chain: The blockchain (e.g., ethereum, bitcoin)
            
        Returns:
            Wallet balance information
        """
        return self._make_request('get', f'/crypto/wallet-balance', 
                                params={'address': address, 'chain': chain})
    
    # Social Data API
    def get_social_sentiment(self, symbol: str, source: str = "all") -> Dict[str, Any]:
        """
        Get social sentiment data for a cryptocurrency.
        
        Args:
            symbol: The cryptocurrency symbol (e.g., BTC, ETH)
            source: The data source (e.g., twitter, reddit, all)
            
        Returns:
            Social sentiment data
        """
        return self._make_request('get', f'/crypto/social-sentiment', 
                                params={'symbol': symbol, 'source': source})
    
    def get_news(self, symbol: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Get latest news for cryptocurrencies.
        
        Args:
            symbol: The cryptocurrency symbol (optional)
            limit: The number of news items to return (default: 10)
            
        Returns:
            Latest news data
        """
        params = {'limit': limit}
        if symbol:
            params['symbol'] = symbol
        
        return self._make_request('get', f'/crypto/news', params=params)
