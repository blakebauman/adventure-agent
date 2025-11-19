# Human-in-the-Loop Implementation

This document describes the human-in-the-loop (HITL) functionality in the adventure agent system.

## Overview

The adventure agent supports human review of adventure plans before finalization. This allows for:
- Review of complex multi-day adventures
- Approval of high-cost recommendations
- Error review and correction
- Customization based on human feedback

## How It Works

### 1. Automatic Review Trigger

The system automatically requests human review when:
- Errors occurred during agent execution
- Multi-day adventures (duration > 7 days)
- Other conditions defined in `orchestrator.should_request_human_review()`

### 2. Interrupt Mechanism

When human review is needed, the graph execution pauses using LangGraph's `interrupt()` function:

```python
# In human_review_node
human_decision = interrupt(review_data)
```

The interrupt:
- Saves the current graph state (via checkpointing)
- Pauses execution indefinitely
- Returns control to the caller
- Waits for resume with human decision

### 3. Resuming Execution

To resume execution after human review, use `Command` with the human's decision:

```python
from langgraph.types import Command

# Resume with approval
result = graph.invoke(
    Command(resume={
        "status": "approved",
        "feedback": ""
    }),
    config={"configurable": {"thread_id": thread_id}}
)

# Resume with revision request
result = graph.invoke(
    Command(resume={
        "status": "needs_revision",
        "feedback": "Please add more camping options and reduce the daily distance"
    }),
    config={"configurable": {"thread_id": thread_id}}
)

# Resume with rejection
result = graph.invoke(
    Command(resume={
        "status": "rejected",
        "feedback": "This plan doesn't meet my requirements"
    }),
    config={"configurable": {"thread_id": thread_id}}
)
```

## Review Data Structure

When an interrupt occurs, the following data is provided for review:

```python
{
    "message": "Please review the adventure plan before finalization",
    "adventure_plan": {...},  # The generated plan
    "user_input": "...",     # Original user request
    "user_preferences": {...}, # User preferences
    "errors": [...],         # Any errors that occurred
    "completed_agents": [...] # List of agents that completed
}
```

## Human Decision Structure

When resuming, provide a decision with:

- `status`: One of:
  - `"approved"` - Plan is approved, proceed to completion
  - `"needs_revision"` - Plan needs changes, will loop back to synthesis
  - `"rejected"` - Plan is rejected, execution ends
- `feedback`: Optional feedback string that will be incorporated into revisions

## Example Usage

### Complete Workflow

```python
from langgraph.types import Command
import uuid

# Create a thread ID for state persistence
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

# Invoke the graph
result = graph.invoke(
    {
        "user_input": "Plan a 10-day mountain biking trip in Colorado",
        "user_preferences": {
            "activity_type": "mountain_biking",
            "duration_days": 10,
            "region": "Colorado"
        }
    },
    config=config
)

# Check if execution was interrupted for human review
if result.get("__interrupt__"):
    interrupt_data = result["__interrupt__"][0].value
    
    # Display the plan for review
    print("Adventure Plan for Review:")
    print(interrupt_data["adventure_plan"])
    
    # Get human decision (in a real app, this would be from a UI)
    human_decision = {
        "status": "needs_revision",
        "feedback": "Please add more rest days and include hotel options"
    }
    
    # Resume with decision
    result = graph.invoke(
        Command(resume=human_decision),
        config=config
    )
    
    # If revision was requested, check for another interrupt
    if result.get("__interrupt__"):
        # Review the revised plan
        # ... repeat as needed
        pass

# Final result
print("Final Adventure Plan:", result.get("adventure_plan"))
```

## Integration with LangGraph API

When using `langgraph dev` or LangGraph Cloud:

1. The API automatically handles checkpointing
2. Interrupts are surfaced in the API response
3. Resume by calling the API with `Command` payload
4. The Studio UI can display interrupts for review

## Routing Logic

After human review:
- `"approved"` → Graph ends successfully
- `"needs_revision"` → Routes back to `synthesize` node with feedback
- `"rejected"` → Graph ends

The synthesize node incorporates human feedback when creating revisions.

## Requirements

- **Checkpointing**: Required for interrupts to work (handled automatically by LangGraph API)
- **Thread ID**: Must provide `thread_id` in config for state persistence
- **Resume Command**: Must use `Command(resume={...})` to continue after interrupt

## Best Practices

1. **Always use thread_id**: Without it, state won't persist across interrupts
2. **Handle all statuses**: Implement logic for approved, needs_revision, and rejected
3. **Incorporate feedback**: The synthesize node should use human feedback for revisions
4. **Limit review scope**: Only request review when truly needed (complex plans, errors, etc.)
5. **Clear feedback**: Provide specific, actionable feedback for best revision results

## See Also

- [LangGraph Interrupts Documentation](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [Human-in-the-Loop Guide](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)

