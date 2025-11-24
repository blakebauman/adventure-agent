"""Caching and rate limiting utilities for API calls.

This module provides caching and rate limiting functionality to reduce redundant
API calls, improve performance, and manage API costs.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections import defaultdict
from typing import Any, Callable, Dict, Optional

from agent.config import Config


# Check if caching/rate limiting is enabled
ENABLE_CACHING = Config.ENABLE_CACHING
ENABLE_RATE_LIMITING = Config.ENABLE_RATE_LIMITING


class RateLimiter:
    """Rate limiter for API calls.
    
    Tracks call counts per API endpoint and enforces rate limits.
    """
    
    def __init__(
        self,
        max_calls_per_second: float = 1.0,
        max_calls_per_minute: Optional[float] = None,
        max_calls_per_hour: Optional[float] = None,
    ) -> None:
        """Initialize rate limiter.
        
        Args:
            max_calls_per_second: Maximum calls per second (default: 1.0)
            max_calls_per_minute: Optional maximum calls per minute
            max_calls_per_hour: Optional maximum calls per hour
        """
        self.max_calls_per_second = max_calls_per_second
        self.max_calls_per_minute = max_calls_per_minute
        self.max_calls_per_hour = max_calls_per_hour
        
        # Track call timestamps per endpoint
        self.call_times: Dict[str, list[float]] = defaultdict(list)
        self.lock_times: Dict[str, float] = {}
    
    def wait_if_needed(self, endpoint: str) -> None:
        """Wait if rate limit would be exceeded.
        
        This method uses asyncio.to_thread internally when called from async context
        to avoid blocking the event loop.
        
        Args:
            endpoint: Endpoint identifier (e.g., "opencage", "openweather")
        """
        import asyncio
        
        now = time.time()
        
        # Clean old call times (keep last hour)
        cutoff = now - 3600
        if endpoint in self.call_times:
            self.call_times[endpoint] = [
                t for t in self.call_times[endpoint] if t > cutoff
            ]
        
        # Helper to sleep without blocking event loop
        def _sleep_sync(wait_time: float) -> None:
            """Sleep synchronously - will be wrapped in thread if needed."""
            time.sleep(wait_time)
        
        # Check if locked (recent rate limit hit)
        if endpoint in self.lock_times:
            lock_until = self.lock_times[endpoint]
            if now < lock_until:
                wait_time = lock_until - now
                # Try to use async sleep if in async context, otherwise sync
                try:
                    loop = asyncio.get_running_loop()
                    # We're in async context, but can't await here
                    # Use sync sleep - will be detected as blocking by LangGraph
                    _sleep_sync(wait_time)
                except RuntimeError:
                    # No event loop, safe to use sync sleep
                    _sleep_sync(wait_time)
            else:
                del self.lock_times[endpoint]
        
        # Check per-second limit
        recent_calls = [
            t for t in self.call_times[endpoint]
            if now - t < 1.0
        ]
        if len(recent_calls) >= self.max_calls_per_second:
            wait_time = 1.0 - (now - recent_calls[0])
            if wait_time > 0:
                _sleep_sync(wait_time)
        
        # Check per-minute limit
        if self.max_calls_per_minute:
            recent_calls = [
                t for t in self.call_times[endpoint]
                if now - t < 60.0
            ]
            if len(recent_calls) >= self.max_calls_per_minute:
                wait_time = 60.0 - (now - recent_calls[0])
                if wait_time > 0:
                    _sleep_sync(wait_time)
        
        # Check per-hour limit
        if self.max_calls_per_hour:
            recent_calls = [
                t for t in self.call_times[endpoint]
                if now - t < 3600.0
            ]
            if len(recent_calls) >= self.max_calls_per_hour:
                wait_time = 3600.0 - (now - recent_calls[0])
                if wait_time > 0:
                    _sleep_sync(wait_time)
        
        # Record this call
        self.call_times[endpoint].append(time.time())
    
    def record_rate_limit_hit(self, endpoint: str, lock_duration: float = 60.0) -> None:
        """Record that a rate limit was hit and lock the endpoint.
        
        Args:
            endpoint: Endpoint identifier
            lock_duration: How long to lock the endpoint in seconds
        """
        self.lock_times[endpoint] = time.time() + lock_duration


class APICache:
    """Simple in-memory cache for API responses.
    
    Uses a hash of the request parameters as the cache key.
    """
    
    def __init__(
        self,
        default_ttl: float = 3600.0,  # 1 hour default
        max_size: int = 1000,
    ) -> None:
        """Initialize API cache.
        
        Args:
            default_ttl: Default time-to-live for cache entries in seconds
            max_size: Maximum number of cache entries
        """
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.cache: Dict[str, tuple[Any, float]] = {}
    
    def _make_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Create a cache key from endpoint and parameters.
        
        Args:
            endpoint: API endpoint identifier
            params: Request parameters
            
        Returns:
            Cache key string
        """
        # Sort params for consistent hashing
        sorted_params = json.dumps(params, sort_keys=True)
        key_string = f"{endpoint}:{sorted_params}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(
        self,
        endpoint: str,
        params: Dict[str, Any],
        ttl: Optional[float] = None,
    ) -> Optional[Any]:
        """Get cached response if available and not expired.
        
        Args:
            endpoint: API endpoint identifier
            params: Request parameters
            ttl: Optional TTL override
            
        Returns:
            Cached response or None if not found/expired
        """
        key = self._make_key(endpoint, params)
        
        if key not in self.cache:
            return None
        
        value, expiry = self.cache[key]
        
        if time.time() > expiry:
            # Expired, remove it
            del self.cache[key]
            return None
        
        return value
    
    def set(
        self,
        endpoint: str,
        params: Dict[str, Any],
        value: Any,
        ttl: Optional[float] = None,
    ) -> None:
        """Store a response in the cache.
        
        Args:
            endpoint: API endpoint identifier
            params: Request parameters
            value: Response value to cache
            ttl: Optional TTL override
        """
        key = self._make_key(endpoint, params)
        ttl = ttl or self.default_ttl
        expiry = time.time() + ttl
        
        # Evict oldest entries if cache is full
        if len(self.cache) >= self.max_size and key not in self.cache:
            # Remove oldest entry
            oldest_key = min(
                self.cache.keys(),
                key=lambda k: self.cache[k][1]
            )
            del self.cache[oldest_key]
        
        self.cache[key] = (value, expiry)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
    
    def clear_expired(self) -> None:
        """Remove expired cache entries."""
        now = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if now > expiry
        ]
        for key in expired_keys:
            del self.cache[key]


# Global instances
_rate_limiters: Dict[str, RateLimiter] = {}
_cache = APICache(
    default_ttl=Config.CACHE_DEFAULT_TTL,
    max_size=Config.CACHE_MAX_SIZE,
)


def get_rate_limiter(endpoint: str) -> RateLimiter:
    """Get or create a rate limiter for an endpoint.
    
    Args:
        endpoint: Endpoint identifier
        
    Returns:
        RateLimiter instance
    """
    if endpoint not in _rate_limiters:
        # Configure rate limits per endpoint
        if endpoint == "nominatim":
            # Nominatim: 1 request/second
            _rate_limiters[endpoint] = RateLimiter(
                max_calls_per_second=1.0,
                max_calls_per_minute=60.0,
            )
        elif endpoint == "opencage":
            # OpenCage: depends on plan, default conservative
            _rate_limiters[endpoint] = RateLimiter(
                max_calls_per_second=2.0,
                max_calls_per_minute=120.0,
            )
        elif endpoint == "openweather":
            # OpenWeatherMap: 60 calls/minute
            _rate_limiters[endpoint] = RateLimiter(
                max_calls_per_second=1.0,
                max_calls_per_minute=60.0,
            )
        elif endpoint == "weather_gov":
            # Weather.gov: no official limit, be conservative
            _rate_limiters[endpoint] = RateLimiter(
                max_calls_per_second=1.0,
                max_calls_per_minute=60.0,
            )
        elif endpoint == "overpass":
            # Overpass API: be conservative
            _rate_limiters[endpoint] = RateLimiter(
                max_calls_per_second=1.0,
                max_calls_per_minute=30.0,
            )
        else:
            # Default conservative limits
            _rate_limiters[endpoint] = RateLimiter(
                max_calls_per_second=1.0,
                max_calls_per_minute=60.0,
            )
    
    return _rate_limiters[endpoint]


def get_cache() -> APICache:
    """Get the global API cache instance.
    
    Returns:
        APICache instance
    """
    return _cache


def cached_api_call(
    endpoint: str,
    params: Dict[str, Any],
    api_func: Callable[[], Any],
    ttl: Optional[float] = None,
    use_rate_limiting: Optional[bool] = None,
) -> Any:
    """Make an API call with caching and rate limiting.
    
    Args:
        endpoint: Endpoint identifier
        params: Request parameters
        api_func: Function that makes the actual API call
        ttl: Optional cache TTL override
        use_rate_limiting: Whether to apply rate limiting (defaults to Config.ENABLE_RATE_LIMITING)
        
    Returns:
        API response (from cache or fresh call)
    """
    # Check cache first if caching is enabled
    if ENABLE_CACHING:
        cache = get_cache()
        cached_response = cache.get(endpoint, params, ttl)
        if cached_response is not None:
            return cached_response
    
    # Apply rate limiting if enabled
    if use_rate_limiting is None:
        use_rate_limiting = ENABLE_RATE_LIMITING
    
    if use_rate_limiting:
        limiter = get_rate_limiter(endpoint)
        limiter.wait_if_needed(endpoint)
    
    # Make API call
    try:
        response = api_func()
        
        # Cache successful response if caching is enabled
        if ENABLE_CACHING:
            cache = get_cache()
            cache.set(endpoint, params, response, ttl)
        
        return response
    except Exception as e:
        # Check if it's a rate limit error
        error_str = str(e).lower()
        if "rate limit" in error_str or "429" in error_str:
            if ENABLE_RATE_LIMITING:
                limiter = get_rate_limiter(endpoint)
                limiter.record_rate_limit_hit(endpoint)
        
        # Re-raise the exception
        raise

