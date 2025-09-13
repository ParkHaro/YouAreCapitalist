---
category: template
tags: [template, session-log, tracking, documentation]
related: [WORK_SESSION_TRACKER.md, CHECKPOINT_TEMPLATE.md]
parent: ../reference/WORK_SESSION_TRACKER.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# Session Log Template

[🇰🇷 한국어 버전](./SESSION_LOG_TEMPLATE_KOR.md)

## 📍 Navigation

[📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 🎯 Template Usage

**File Naming Convention**: `SESSION_LOG_[YYYY-MM-DD]_[session-id].md`

**Example**: `SESSION_LOG_2025-09-13_investment-automation-001.md`

---

# Session Log: [Session Description]

**Session ID**: [unique-session-identifier]  
**Date**: [YYYY-MM-DD]  
**Start Time**: [HH:MM]  
**End Time**: [HH:MM]  
**Duration**: [X hours Y minutes]  
**Session Type**: [single-task/multi-task/project/investigation]

## 📋 Session Metadata

### Related Work Plan
**Work Plan**: [WORK_PLAN_[date]_[feature].md](../workplans/WORK_PLAN_[date]_[feature].md)  
**Epic/Story**: [Reference to larger work context]  
**Session Objective**: [Primary goal for this session]

### Previous Session
**Previous Log**: [SESSION_LOG_[date]_[id].md] (if applicable)  
**Context Continuation**: [Brief description of how this continues previous work]

### TodoList State at Start
```yaml
Active Tasks at Session Start:
  - [Task 1]: [Status - percentage complete]
  - [Task 2]: [Status - percentage complete]
  - [Task 3]: [Status - percentage complete]

Priority for This Session:
  1. [Primary task for this session]
  2. [Secondary task if time permits]
  3. [Tertiary task if time permits]
```

## 🎯 Session Objectives

### Primary Goals
- [ ] [Specific objective 1]
- [ ] [Specific objective 2]
- [ ] [Specific objective 3]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

### Time Allocation Plan
- **[Task/Activity 1]**: [X minutes/hours]
- **[Task/Activity 2]**: [X minutes/hours]
- **[Testing/Validation]**: [X minutes]
- **[Documentation]**: [X minutes]

## 🏗️ Technical Context

### Current System State
**Build Status**: [Compiling/Errors/Warnings]  
**Test Status**: [Passing/Failing - specific details]  
**Git State**: [Clean/Modified files/Uncommitted changes]  
**Unity Project**: [Version/Packages/Settings status]

### Active Development Area
**Primary Focus**: [Specific system/component being worked on]  
**Files in Focus**: 
- `[File path 1]` - [Purpose/Status]
- `[File path 2]` - [Purpose/Status]
- `[File path 3]` - [Purpose/Status]

### Dependencies Status
- **[Dependency 1]**: [Available/Blocked/In Progress]
- **[Dependency 2]**: [Available/Blocked/In Progress]
- **[External Resource]**: [Available/Unavailable]

## 📊 Progress Tracking

### Achievements This Session

#### Completed Tasks
**[Task Name]** ✅  
**Duration**: [Actual time spent]  
**Description**: [What was accomplished]  
**Evidence**: [Commit hash/Test results/File changes]  
**Quality Validation**: [How completion was verified]

**[Task Name]** ✅  
**Duration**: [Actual time spent]  
**Description**: [What was accomplished]  
**Evidence**: [Commit hash/Test results/File changes]  
**Quality Validation**: [How completion was verified]

#### Partial Progress
**[Task Name]** 🔄  
**Progress**: [X% complete]  
**Duration**: [Time spent so far]  
**Description**: [What was accomplished]  
**Remaining Work**: [What still needs to be done]  
**Blockers**: [Any obstacles encountered]

### Code Changes Made

#### New Files Created
- `[File path]` - [Purpose and functionality]
- `[File path]` - [Purpose and functionality]

#### Files Modified
- `[File path]` - [Changes made and reason]
  - Lines changed: [+X/-Y]
  - Key modifications: [Brief description]
- `[File path]` - [Changes made and reason]
  - Lines changed: [+X/-Y]
  - Key modifications: [Brief description]

#### Commits Made
```
[commit-hash]: [Commit message]
Description: [Detailed description of changes]
Files: [List of files changed]

[commit-hash]: [Commit message]
Description: [Detailed description of changes]
Files: [List of files changed]
```

### Testing Results

#### Unit Tests
**New Tests Created**: [Number]  
**Tests Modified**: [Number]  
**Test Coverage**: [X% for modified code]  
**All Tests Status**: [Passing/Failing with details]

#### Integration Tests
**Systems Tested**: [List of integrated systems tested]  
**Performance Tests**: [Results of performance validation]  
**Manual Testing**: [User workflow or functionality tested]

#### Quality Validation
**Code Review**: [Self-review completed/Peer review requested]  
**Architecture Compliance**: [Validated against patterns]  
**Performance Impact**: [Measured impact on system performance]

## 🧠 Decisions and Learning

### Technical Decisions Made

#### Decision 1
**Context**: [What situation required a decision]  
**Options Considered**: 
- Option A: [Description] - [Pros/Cons]
- Option B: [Description] - [Pros/Cons]
- Option C: [Description] - [Pros/Cons]

**Decision**: [Option chosen]  
**Rationale**: [Why this option was selected]  
**Implementation**: [How it was implemented]  
**Validation**: [How success will be measured]

#### Decision 2
**Context**: [What situation required a decision]  
**Decision**: [What was decided]  
**Rationale**: [Why this decision was made]  
**Impact**: [Expected consequences of this decision]

### Problem-Solution Patterns

#### Problem Encountered
**Problem**: [Specific issue faced]  
**Investigation**: [How the problem was analyzed]  
**Root Cause**: [Underlying cause identified]  
**Solution**: [How it was resolved]  
**Prevention**: [How to avoid similar issues]  
**Knowledge Gained**: [What was learned]

#### Challenge Overcome
**Challenge**: [Difficulty faced]  
**Approach**: [Method used to address it]  
**Outcome**: [Result achieved]  
**Lessons**: [Insights for future work]

### New Knowledge Acquired
- **[Technical Knowledge]**: [What was learned about technology/patterns]
- **[Domain Knowledge]**: [What was learned about business/game logic]
- **[Process Knowledge]**: [What was learned about development workflow]

## ⚠️ Issues and Blockers

### Active Blockers
**Blocker 1**: [Description of blocking issue]  
**Impact**: [How this affects progress]  
**Status**: [Investigation/Escalated/Waiting for resolution]  
**Next Steps**: [What needs to happen to resolve]  
**Owner**: [Who is responsible for resolution]

**Blocker 2**: [Description of blocking issue]  
**Impact**: [How this affects progress]  
**Action Plan**: [Steps being taken to resolve]

### Known Issues
**Issue 1**: [Description of non-blocking issue]  
**Severity**: [Low/Medium/High]  
**Workaround**: [Temporary solution if available]  
**Resolution Plan**: [How/when this will be properly fixed]

**Issue 2**: [Description of non-blocking issue]  
**Impact**: [Effect on system or development]  
**Tracking**: [Issue number or reference]

### Technical Debt Incurred
**Debt Item 1**: [Description of shortcuts taken]  
**Reason**: [Why this debt was necessary]  
**Impact**: [Future implications]  
**Repayment Plan**: [When/how this will be addressed]

## 📈 Performance Analysis

### Performance Measurements
**Frame Time**: [Current system performance]  
**Memory Usage**: [Current memory consumption]  
**Entity Count**: [Number of entities being processed]  
**Bottlenecks Identified**: [Performance issues found]

### Optimization Results
**Before**: [Baseline measurements]  
**After**: [Post-optimization measurements]  
**Improvement**: [Quantified improvement achieved]  
**Method**: [Optimization technique used]

### Performance Goals Progress
- **Target 1**: [X ms frame time] - Status: [On track/Behind/Achieved]
- **Target 2**: [Y entities @ Z fps] - Status: [On track/Behind/Achieved]
- **Target 3**: [Memory usage < W MB] - Status: [On track/Behind/Achieved]

## 🔄 Session Continuity

### Current State Summary
**Active Task**: [Current TodoList task being worked on]  
**Completion Status**: [X% complete]  
**Last Working Approach**: [Method/strategy currently being used]  
**Code Location**: [Specific file/function being modified]

### Immediate Next Steps
1. **[Next Action 1]**: [Specific next step to take]  
   - **Estimated Time**: [X minutes/hours]  
   - **Dependencies**: [Prerequisites]
   
2. **[Next Action 2]**: [Specific next step to take]  
   - **Estimated Time**: [X minutes/hours]  
   - **Context**: [Additional context needed]

3. **[Next Action 3]**: [Specific next step to take]  
   - **Estimated Time**: [X minutes/hours]  
   - **Risk**: [Potential complications]

### Context for Next Session
**Current Focus**: [What the next session should concentrate on]  
**Key Files**: [Important files to have open]  
**Mental Model**: [Important context about approach/strategy]  
**Environment Setup**: [Any special configuration needed]

### Checkpoint Created
**Checkpoint File**: [CHECKPOINT_[timestamp].md]  
**Checkpoint Type**: [micro/standard/major/emergency]  
**Recovery Time**: [Estimated time to restore context]

## 📚 Documentation Impact

### Documentation Updated
- **[Document Name]**: [What sections were updated and why]
- **[Architecture Doc]**: [Changes made to reflect new implementation]
- **[API Documentation]**: [New or modified API descriptions]

### Documentation Needed
- [ ] **[Document to Create]**: [What needs to be documented]
- [ ] **[Document to Update]**: [What sections need updating]
- [ ] **[Knowledge to Capture]**: [Important information to preserve]

## 📊 Session Effectiveness Analysis

### Time Analysis
**Planned Duration**: [X hours]  
**Actual Duration**: [Y hours]  
**Variance**: [±Z minutes - reasons for difference]

**Time Breakdown**:
- **Productive Coding**: [X% of time]
- **Testing/Debugging**: [X% of time]
- **Research/Learning**: [X% of time]
- **Documentation**: [X% of time]
- **Context Switching**: [X% of time]

### Productivity Assessment
**Goals Achievement**: [X out of Y objectives completed]  
**Code Quality**: [Satisfied with output quality]  
**Learning Value**: [Knowledge gained during session]  
**Momentum**: [Prepared for next session]

### Improvement Opportunities
- **[Process Improvement]**: [What could be done more efficiently]
- **[Tool/Environment]**: [Tools or setup that could be improved]
- **[Planning]**: [Better estimation or preparation needed]

---

## 🎯 Session Outcomes

### TodoList State at End
```yaml
Completed Tasks:
  - [Task 1]: ✅ [Brief completion note]
  - [Task 2]: ✅ [Brief completion note]

In Progress Tasks:
  - [Task 3]: 🔄 [X% complete - current status]

New Tasks Discovered:
  - [New Task 1]: [Why this task was identified]
  - [New Task 2]: [Dependencies and priority]
```

### Work Plan Progress
**Epic Progress**: [X% complete overall]  
**Current Story**: [Story name] - [X% complete]  
**Milestone Status**: [On track/Behind schedule/Ahead of schedule]

### Quality Gates Status
- [ ] **Code Quality**: [All standards met]
- [ ] **Test Coverage**: [Adequate coverage maintained]
- [ ] **Performance**: [No regressions introduced]
- [ ] **Documentation**: [Current and accurate]

---

**Session Completion**: [YYYY-MM-DD HH:MM]  
**Next Session Planned**: [YYYY-MM-DD] (estimated)  
**Session Rating**: [1-5 stars based on productivity and progress]  
**Log Reviewed**: [Yes/No - was this log reviewed for accuracy]