# Bug Fix Template

Use this template when fixing bugs in ecowitt2mqtt. Capture enough detail to fix the issue efficiently and prevent regressions.

## Bug Information

**Bug ID**: [GitHub issue number or internal tracking ID]

**Severity**: [Critical / High / Medium / Low]

**Priority**: [P0 / P1 / P2 / P3]

**Reported Date**: [YYYY-MM-DD]

**Reporter**: [Name or GitHub username]

**Affected Version(s)**: [e.g., 2024.10.0, dev branch]

---

## Bug Description

**Summary**: [One-line description of the bug]

**Detailed Description**:
[Comprehensive description of what's wrong. Be specific about symptoms, not just the effect.]

**Impact**:
- **User Impact**: [How does this affect users? How many users?]
- **System Impact**: [Does this affect stability, performance, data integrity?]
- **Business Impact**: [Does this block critical workflows?]

---

## Reproduction Steps

**Prerequisites**:
- [ ] Python version: [e.g., 3.10]
- [ ] Installation method: [pip / Docker / source]
- [ ] Operating system: [e.g., Ubuntu 22.04, Unraid 6.12]
- [ ] Ecowitt device: [Model number, firmware version if known]
- [ ] Configuration: [Relevant config options]

**Steps to Reproduce**:
1. [First step]
2. [Second step]
3. [Third step]
4. [Continue until bug manifests]

**Expected Behavior**:
[What should happen?]

**Actual Behavior**:
[What actually happens?]

**Reproducibility**:
- [ ] Always (100%)
- [ ] Frequently (>50%)
- [ ] Sometimes (<50%)
- [ ] Rarely / Once

---

## Evidence

### Error Messages

**Console Output**:
```
[Paste complete error message, stack trace, or console output]
```

**Log Output**:
```
[Paste relevant log entries - include timestamps if available]
[Be sure to redact sensitive information like passwords, API keys, etc.]
```

### Screenshots/Recordings
[Attach or link to any visual evidence]

### Data Samples

**Input Data** (if relevant):
```json
{
  "sample": "data that triggers the bug"
}
```

**Configuration File** (if relevant):
```yaml
# Paste relevant config sections
# Redact sensitive information
```

---

## Environment Details

**System Information**:
- Python Version: [e.g., 3.11.5]
- ecowitt2mqtt Version: [e.g., 2024.10.0]
- Operating System: [e.g., Ubuntu 22.04 LTS]
- Docker: [Yes/No - if yes, include image version]
- Unraid: [Yes/No - if yes, include version]

**Dependencies** (if possibly related):
```
# Output of: pip list | grep -E "aiohttp|paho-mqtt|pyyaml"
aiohttp==3.9.0
paho-mqtt==1.6.1
pyyaml==6.0.1
```

**Network Configuration** (if relevant):
- MQTT Broker: [e.g., Mosquitto 2.0.15]
- MQTT Broker Location: [Local / Remote]
- Network: [Same subnet / Different subnet / VPN]

**Ecowitt Device Details** (if relevant):
- Device Model: [e.g., GW1000, GW2000]
- Firmware Version: [If known]
- Connected Sensors: [List sensor types]

---

## Root Cause Analysis

### Initial Hypothesis:
[What do you think might be causing this? What's your gut feeling?]

### Investigation Notes:
[Document your investigation process, tools used, hypotheses tested]

1. **Checked**: [What you investigated]
   - **Finding**: [What you discovered]
   
2. **Checked**: [What you investigated]
   - **Finding**: [What you discovered]

### Confirmed Root Cause:
[After investigation, what's the actual cause?]

**Location in Code**:
- **File**: `path/to/file.py`
- **Function/Class**: `function_name` or `ClassName`
- **Line(s)**: [Line numbers]

**Code Snippet** (current buggy code):
```python
# Show the problematic code
def buggy_function():
    # Problem is here
    pass
```

**Why This Causes the Bug**:
[Explain the mechanism by which this code causes the observed behavior]

---

## Fix Strategy

### Proposed Solution:
[Describe the fix at a high level]

**Code Changes Required**:
```python
# Show the proposed fix
def fixed_function():
    # Better implementation
    pass
```

**Why This Fixes the Issue**:
[Explain why your proposed change resolves the root cause]

### Alternative Approaches Considered:
1. **Approach 1**: [Description]
   - **Pros**: [Advantages]
   - **Cons**: [Disadvantages]
   - **Why not chosen**: [Reason]

2. **Approach 2**: [Description]
   - **Pros**: [Advantages]
   - **Cons**: [Disadvantages]
   - **Why not chosen**: [Reason]

---

## Implementation Details

### Files to Modify:
- [ ] `ecowitt2mqtt/module.py` - [Specific changes]
- [ ] `ecowitt2mqtt/config.py` - [Specific changes]
- [ ] `tests/test_module.py` - [Add regression test]

### Code Changes:

**Before**:
```python
# Current buggy implementation
```

**After**:
```python
# Fixed implementation
```

**Explanation**:
[Line-by-line explanation of what changed and why]

---

## Testing Strategy

### Regression Test

**Test Name**: `test_bug_<bug_id>_<description>`

**Test Code**:
```python
@pytest.mark.asyncio
async def test_bug_123_description():
    """Test that bug #123 is fixed.
    
    This test ensures that [specific behavior] works correctly
    when [specific conditions] are met.
    """
    # Setup
    
    # Action
    
    # Assert
    
```

**Why This Test Prevents Regression**:
[Explain what this test validates and why it would fail if the bug returns]

### Related Test Updates

**Existing Tests to Update**:
- [ ] `test_existing_function()` - [Why it needs updating]

**New Edge Case Tests**:
- [ ] `test_edge_case_1()` - [Description]
- [ ] `test_edge_case_2()` - [Description]

### Manual Testing Checklist

- [ ] Reproduce the original bug in dev environment
- [ ] Apply the fix
- [ ] Verify bug no longer occurs
- [ ] Test related functionality to ensure no side effects
- [ ] Test with multiple configurations (if config-related)
- [ ] Test with different Ecowitt devices (if device-specific)
- [ ] Run full test suite and confirm 100% coverage
- [ ] Test in Docker container
- [ ] Test on Unraid (if applicable)
- [ ] Check logs for any unexpected warnings/errors

---

## Side Effects & Risks

### Potential Side Effects:
[List any other parts of the system that might be affected by this fix]

1. [Potential side effect 1]
   - **Mitigation**: [How you'll prevent or handle this]

2. [Potential side effect 2]
   - **Mitigation**: [How you'll prevent or handle this]

### Backward Compatibility:
- [ ] This fix is backward compatible
- [ ] This fix introduces breaking changes:
  - [Description of breaking change]
  - [Migration path for users]

### Performance Impact:
- [ ] No performance impact expected
- [ ] Potential performance impact:
  - [Description]
  - [Benchmarks or profiling results]

---

## Verification

### Definition of Done:
- [ ] Bug can no longer be reproduced
- [ ] Regression test added and passing
- [ ] All existing tests still pass
- [ ] Code coverage remains at 100%
- [ ] Code passes linting (ruff, pylint)
- [ ] Type checking passes (mypy)
- [ ] Documentation updated (if needed)
- [ ] Changelog updated
- [ ] Tested in target environment (Unraid/Docker)

### Post-Deployment Verification:
- [ ] Monitor logs for related errors
- [ ] Check user reports for recurrence
- [ ] Verify metrics (if applicable)

---

## Documentation Updates

### Code Documentation:
- [ ] Add/update docstrings explaining the fix
- [ ] Add inline comments for complex logic
- [ ] Update type hints if changed

### User-Facing Documentation:
- [ ] Update README.md (if user-visible behavior changed)
- [ ] Update configuration documentation
- [ ] Add to known issues (if workaround needed)
- [ ] Update Docker documentation (if applicable)

### Changelog Entry:
```markdown
### Bug Fixes
- Fixed [brief description] (#bug-id)
```

---

## Communication

### Who Needs to Know:
- [ ] Original bug reporter
- [ ] Users who reported similar issues
- [ ] Team members working on related features
- [ ] Community (via GitHub issue comment)

### Release Notes:
[Draft release note entry]

---

## References

**Related Issues**:
- [Link to GitHub issue]
- [Link to related bug reports]

**Related Pull Requests**:
- [Link to PR that may have introduced the bug]
- [Link to related PRs]

**External References**:
- [Documentation]
- [Stack Overflow thread]
- [Library issue tracker]

---

## Lessons Learned

### What Caused This Bug:
[Reflect on how this bug was introduced]

### How to Prevent Similar Bugs:
[Improvements to process, testing, code review, etc.]

### Suggestions for Future:
[Ideas for preventing this class of bug]

---

## Review Checklist

Before marking this fix as "ready for merge":

- [ ] Root cause clearly identified and documented
- [ ] Fix strategy is sound and reviewed
- [ ] Regression test added
- [ ] All tests pass with 100% coverage
- [ ] No unintended side effects identified
- [ ] Documentation updated
- [ ] Changelog entry added
- [ ] Manual testing completed
- [ ] Code review completed

---

## Development Notes

[Use this section for notes during implementation, debugging discoveries, etc.]
