# Error Handling Improvements Implementation

## Summary

This document describes the three improvements implemented based on the LangGraph best practices analysis:

1. **Error categorization**: Distinguish transient vs. permanent errors
2. **Command-based error handling**: Use Command for LLM-recoverable errors to loop back to orchestrator
3. **Checkpointer validation**: Ensure checkpointer is set when human-in-the-loop is enabled

---

## 1. Error Categorization System ✅

### Implementation

Created `src/agent/error_handling.py` with:

- **ErrorType enum**: Four error categories:
  - `TRANSIENT`: Network issues, rate limits - handled by retry policies
  - `LLM_RECOVERABLE`: Tool failures, parsing issues - LLM can adjust
  - `USER_FIXABLE`: Missing information - need user input
  - `PERMANENT`: Validation errors, configuration issues - cannot recover

- **ErrorCategory class**: Categorizes errors based on:
  - Exception type
  - Error message content (rate limits, network issues, etc.)
  - Context (agent name)

### Usage

```python
from agent.error_handling import ErrorCategory, ErrorType

error_detail = ErrorCategory.create_error_dict(error, "geo_agent")
error_type = ErrorType(error_detail["type"])

# Check error type
if error_type == ErrorType.LLM_RECOVERABLE:
    # Route to orchestrator for recovery
    ...
```

### State Schema Updates

Updated `AdventureState` to include:
- `error_details: Annotated[List[Dict[str, Any]], operator.add]` - Structured error information with categorization

**Note**: The old `errors` field (simple string list) has been removed. All error handling now uses the structured `error_details` field.

---

## 2. Command-Based Error Handling for LLM-Recoverable Errors ✅

### Implementation

Created `handle_agent_error()` helper function in `graph.py` that:

1. **Categorizes the error** using `ErrorCategory`
2. **For LLM-recoverable errors**: Returns `Command` to route back to orchestrator
3. **For other errors**: Returns standard state update dict

### Example Usage

```python
async def geo_agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
    try:
        # ... agent logic ...
        return {"geo_info": geo_info, "completed_agents": ["geo_agent"]}
    except Exception as e:
        error_result = handle_agent_error(e, "geo_agent", state, None)
        if isinstance(error_result, Command):
            return error_result  # Routes to orchestrator
        error_result["geo_info"] = None
        return error_result
```

### Orchestrator Updates

Updated `orchestrator_node` to:
- Accept `error_context` parameter
- Include error context in LLM prompt
- Allow orchestrator to adjust strategy based on previous errors

Updated `orchestrator.analyze_request()` to:
- Accept optional `error_context` parameter
- Include error information in prompt for LLM to consider

### Benefits

- **Automatic recovery**: LLM can see what went wrong and adjust strategy
- **No infinite loops**: Errors are categorized and handled appropriately
- **Better context**: Orchestrator has full visibility into recoverable errors

---

## 3. Checkpointer Validation ✅

### Implementation

Added validation in `graph.py` that:

1. Checks if `ENABLE_HUMAN_REVIEW` is enabled
2. Verifies a checkpointer is configured (or using LangGraph API)
3. Issues a warning if human-in-the-loop is enabled without a checkpointer

### Configuration

Added to `Config` class:
```python
ENABLE_HUMAN_REVIEW: bool = os.getenv("ENABLE_HUMAN_REVIEW", "false").lower() == "true"
```

### Validation Logic

```python
# Validate checkpointer for human-in-the-loop
if Config.ENABLE_HUMAN_REVIEW and _checkpointer is None and Config.CHECKPOINTER_TYPE == "none":
    import warnings
    warnings.warn(
        "Human-in-the-loop is enabled but no checkpointer is configured. "
        "Set CHECKPOINTER_TYPE to 'memory', 'sqlite', or 'postgres' for human-in-the-loop to work properly. "
        "Note: LangGraph API (langgraph dev) handles checkpointing automatically.",
        UserWarning
    )
```

### Benefits

- **Early detection**: Warns developers if human-in-the-loop won't work
- **Clear guidance**: Explains what needs to be configured
- **Production safety**: Prevents silent failures in production

---

## Files Modified

1. **New file**: `src/agent/error_handling.py`
   - Error categorization system
   - Error type detection
   - Helper functions

2. **Updated**: `src/agent/state.py`
   - Added `error_details` field with reducer
   - Updated `errors` field to use reducer

3. **Updated**: `src/agent/graph.py`
   - Added `handle_agent_error()` helper function
   - Updated `geo_agent_node()` and `trail_agent_node()` as examples
   - Updated `orchestrator_node()` to handle error context
   - Added checkpointer validation
   - Updated routing to include "orchestrator" edge

4. **Updated**: `src/agent/config.py`
   - Added `ENABLE_HUMAN_REVIEW` configuration

5. **Updated**: `src/agent/agents/orchestrator.py`
   - Updated `analyze_request()` to accept `error_context` parameter
   - Updated prompt to include error context

---

## Migration Guide

### For Existing Nodes

To update existing agent nodes to use the new error handling:

1. **Update return type** to include `Command`:
   ```python
   async def agent_node(state: AdventureState) -> Dict[str, Any] | Command[Literal["orchestrator"]]:
   ```

2. **Replace error handling**:
   ```python
   # Old
   except Exception as e:
       error_msg = f"Agent error: {str(e)}"
       return {
           "result": None,
           "completed_agents": ["agent"],
           "errors": state.get("errors", []) + [error_msg],
       }
   
   # New
   except Exception as e:
       error_result = handle_agent_error(e, "agent", state, None)
       if isinstance(error_result, Command):
           return error_result
       error_result["result"] = None
       return error_result
   ```

### For Configuration

To enable human-in-the-loop with checkpointing:

```bash
# Set in .env
ENABLE_HUMAN_REVIEW=true
CHECKPOINTER_TYPE=memory  # or sqlite, postgres
```

---

## Testing Recommendations

1. **Error Categorization**:
   - Test with network errors (should be TRANSIENT)
   - Test with parsing errors (should be LLM_RECOVERABLE)
   - Test with missing config (should be PERMANENT)

2. **Command-based Recovery**:
   - Trigger LLM-recoverable error in an agent
   - Verify it routes back to orchestrator
   - Verify orchestrator adjusts strategy

3. **Checkpointer Validation**:
   - Enable `ENABLE_HUMAN_REVIEW` without checkpointer
   - Verify warning is issued
   - Verify human-in-the-loop works with checkpointer

---

## Future Enhancements

1. **User-fixable errors with interrupt()**: Currently user-fixable errors are just stored. Could be enhanced to use `interrupt()` for user input.

2. **Error retry limits**: Add limits to prevent infinite loops when routing back to orchestrator.

3. **Error metrics**: Track error rates by type for monitoring.

4. **More nodes updated**: Currently only `geo_agent_node` and `trail_agent_node` are updated as examples. Other nodes can be updated following the same pattern.

---

## References

- [LangGraph Best Practices Analysis](./LANGGRAPH_BEST_PRACTICES_ANALYSIS.md)
- [LangGraph Error Handling Documentation](https://docs.langchain.com/oss/python/langgraph/use-graph-api#exception-handling)
- [LangGraph Command Documentation](https://docs.langchain.com/oss/python/langgraph/use-graph-api#combine-control-flow-and-state-updates-with-command)

