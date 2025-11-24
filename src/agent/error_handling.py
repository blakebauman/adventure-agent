"""Error handling and categorization for the adventure agent system."""

from __future__ import annotations

from enum import Enum
from typing import Any


class ErrorType(str, Enum):
    """Error types for categorization and handling strategies."""

    TRANSIENT = "transient"  # Network issues, rate limits - retry with backoff
    LLM_RECOVERABLE = "llm_recoverable"  # Tool failures, parsing issues - LLM can adjust
    USER_FIXABLE = "user_fixable"  # Missing information, unclear instructions - need user input
    PERMANENT = "permanent"  # Validation errors, configuration issues - cannot recover


class ErrorCategory:
    """Categorizes errors for appropriate handling strategies."""

    # Transient errors (network, rate limits, timeouts)
    TRANSIENT_EXCEPTIONS = (
        ConnectionError,
        TimeoutError,
        OSError,  # Network-related OS errors
    )

    # LLM-recoverable errors (tool failures, parsing issues)
    LLM_RECOVERABLE_EXCEPTIONS = (
        ValueError,  # Invalid input that LLM can adjust
        KeyError,  # Missing keys that LLM can provide
        AttributeError,  # Missing attributes that LLM can handle
    )

    # User-fixable errors (missing required info)
    USER_FIXABLE_EXCEPTIONS = (
        TypeError,  # Type mismatches often indicate user input issues
    )

    # Permanent errors (should not be retried)
    PERMANENT_EXCEPTIONS = (
        ImportError,
        SyntaxError,
        NameError,
        ReferenceError,
        RuntimeError,  # General runtime errors
    )

    @classmethod
    def categorize_error(cls, error: Exception, agent_name: str = "") -> ErrorType:
        """Categorize an error based on its type and message.
        
        Args:
            error: The exception that was raised
            agent_name: Name of the agent that raised the error (for context)
        
        Returns:
            ErrorType indicating how the error should be handled
        """
        error_type = type(error)
        error_msg = str(error).lower()

        # Check for transient errors (network, rate limits)
        if isinstance(error, cls.TRANSIENT_EXCEPTIONS):
            return ErrorType.TRANSIENT

        # Check for rate limit indicators in message
        if any(indicator in error_msg for indicator in ["rate limit", "429", "too many requests", "quota"]):
            return ErrorType.TRANSIENT

        # Check for network indicators
        if any(indicator in error_msg for indicator in ["connection", "timeout", "network", "dns"]):
            return ErrorType.TRANSIENT

        # Check for LLM-recoverable errors
        if isinstance(error, cls.LLM_RECOVERABLE_EXCEPTIONS):
            return ErrorType.LLM_RECOVERABLE

        # Check for parsing/format errors that LLM can fix
        if any(indicator in error_msg for indicator in ["parse", "format", "invalid json", "malformed"]):
            return ErrorType.LLM_RECOVERABLE

        # Check for user-fixable errors
        if isinstance(error, cls.USER_FIXABLE_EXCEPTIONS):
            return ErrorType.USER_FIXABLE

        # Check for missing information indicators
        if any(indicator in error_msg for indicator in ["missing", "required", "not provided", "not found"]):
            # If it's a missing API key or config, it's permanent
            if any(config in error_msg for config in ["api key", "api_key", "configuration", "config"]):
                return ErrorType.PERMANENT
            return ErrorType.USER_FIXABLE

        # Check for permanent errors
        if isinstance(error, cls.PERMANENT_EXCEPTIONS):
            return ErrorType.PERMANENT

        # Default to permanent for unknown errors (safer to not retry)
        return ErrorType.PERMANENT

    @classmethod
    def create_error_dict(
        cls, error: Exception, agent_name: str, error_type: ErrorType | None = None
    ) -> dict[str, Any]:
        """Create a structured error dictionary for state.
        
        Args:
            error: The exception that was raised
            agent_name: Name of the agent that raised the error
            error_type: Optional pre-categorized error type
        
        Returns:
            Dictionary with error information
        """
        if error_type is None:
            error_type = cls.categorize_error(error, agent_name)

        return {
            "agent": agent_name,
            "type": error_type.value,
            "message": str(error),
            "error_class": type(error).__name__,
        }


def is_transient_error(error: Exception) -> bool:
    """Check if an error is transient and should be retried.
    
    Args:
        error: The exception to check
    
    Returns:
        True if the error is transient and should be retried
    """
    return ErrorCategory.categorize_error(error) == ErrorType.TRANSIENT


def is_llm_recoverable_error(error: Exception) -> bool:
    """Check if an error can be recovered by the LLM.
    
    Args:
        error: The exception to check
    
    Returns:
        True if the error can be recovered by the LLM
    """
    return ErrorCategory.categorize_error(error) == ErrorType.LLM_RECOVERABLE


def is_user_fixable_error(error: Exception) -> bool:
    """Check if an error requires user input to fix.
    
    Args:
        error: The exception to check
    
    Returns:
        True if the error requires user input
    """
    return ErrorCategory.categorize_error(error) == ErrorType.USER_FIXABLE

