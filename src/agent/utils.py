"""Utility functions for the adventure agent."""

from __future__ import annotations

import asyncio
from typing import Any, Callable


async def invoke_tool_async(tool: Any, args: dict[str, Any]) -> Any:
    """Invoke a LangChain tool asynchronously to avoid blocking the event loop.
    
    Args:
        tool: The LangChain tool to invoke
        args: Arguments to pass to the tool
        
    Returns:
        Tool result
    """
    return await asyncio.to_thread(tool.invoke, args)

