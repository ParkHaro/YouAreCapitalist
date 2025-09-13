---
category: template
tags: [template, checkpoint, recovery, documentation]
related: [CHECKPOINT_PROTOCOL.md, SESSION_LOG_TEMPLATE.md]
parent: ../reference/CHECKPOINT_PROTOCOL.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# Checkpoint Template

[🇰🇷 한국어 버전](./CHECKPOINT_TEMPLATE_KOR.md)

## 📍 Navigation

[📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 🎯 Template Usage

**File Naming Convention**: `CHECKPOINT_[type]_[timestamp]_[session-id].md`

**Examples**: 
- `CHECKPOINT_micro_20250913_1430_investment-automation.md`
- `CHECKPOINT_standard_20250913_1600_investment-automation.md`
- `CHECKPOINT_emergency_20250913_1445_investment-automation.md`

---

# Checkpoint: [Brief Description]

**Checkpoint ID**: [unique-checkpoint-identifier]  
**Type**: [micro/standard/major/emergency]  
**Timestamp**: [YYYY-MM-DD HH:MM:SS]  
**Session ID**: [related-session-identifier]  
**Recovery Estimate**: [< X minutes]

## 📋 Checkpoint Metadata

### Context References
**Work Plan**: [WORK_PLAN_[date]_[feature].md]  
**Session Log**: [SESSION_LOG_[date]_[id].md]  
**Previous Checkpoint**: [CHECKPOINT_[timestamp].md] (if applicable)

### Trigger Information
**Trigger Type**: [time-based/task-completion/context-switch/emergency/manual]  
**Trigger Reason**: [Specific reason this checkpoint was created]  
**Planned/Unplanned**: [Was this checkpoint scheduled or reactive]

## 🎯 Current State

### Active Task Context
**Current TodoList Task**: [Specific task being worked on]  
**Completion Percentage**: [X% complete]  
**Last Completed Action**: [Most recent specific action taken]  
**Immediate Next Action**: [Very next step planned for continuation]

### Code Location Context
**Primary File**: `[path/to/current/file.cs]`  
**Function/Method**: `[CurrentMethod() or CurrentArea]`  
**Line/Section**: [Specific location within file]  
**Edit State**: [What kind of edit is in progress]

### Working Approach
**Current Strategy**: [Method/approach being used to solve current problem]  
**Implementation Pattern**: [ECS pattern, architectural approach, or coding pattern being followed]  
**Key Decisions Made**: [Recent important technical choices that affect current work]

## 🏗️ Technical State

### Build and Compilation
**Build Status**: [Clean/Compiling/Errors/Warnings]  
**Error Details**: [Specific compilation errors if any]  
**Warning Count**: [Number and severity of current warnings]  
**Last Successful Build**: [Timestamp of last clean compilation]

### Testing Status
**Unit Tests**: [Passing/Failing - count of each]  
**Integration Tests**: [Status of relevant integration tests]  
**Manual Testing**: [What was last manually tested and result]  
**Performance Tests**: [Current performance test status]

### Git Repository State
**Branch**: [current-branch-name]  
**Last Commit**: [commit-hash] - [commit message]  
**Uncommitted Changes**: [List of modified files]  
**Staged Changes**: [Files ready for commit]  
**Git Status Summary**: [Clean/Modified/Untracked files present]

### Unity Project State
**Unity Version**: [2023.x.xf1]  
**Package Manager**: [Any package operations in progress or needed]  
**Project Settings**: [Any recent changes to project configuration]  
**Scene State**: [Current scene loaded and any unsaved changes]

## 📊 Progress Assessment

### Session Progress
**Session Start Time**: [HH:MM]  
**Elapsed Time**: [X hours Y minutes at checkpoint creation]  
**Completed Since Last Checkpoint**: [List of completed work items]  
**Progress Rate**: [Assessment of progress speed: ahead/on-track/behind]

### Work Plan Progress
**Epic/Story Progress**: [Current position in larger work plan]  
**Milestone Status**: [Relationship to next major milestone]  
**Scope Changes**: [Any modifications to original scope]  
**Timeline Status**: [On schedule/Behind/Ahead with specific details]

### Quality Metrics
**Code Quality**: [Self-assessment of current code quality]  
**Architecture Compliance**: [Adherence to established patterns]  
**Test Coverage**: [Coverage percentage for modified areas]  
**Technical Debt**: [Any shortcuts taken that need future attention]

## 🧠 Decision Trail

### Recent Technical Decisions
**Decision 1**: [What was decided]  
**Context**: [Why the decision was needed]  
**Options Considered**: [Alternative approaches that were evaluated]  
**Rationale**: [Why this option was chosen]  
**Implementation Status**: [How much of this decision has been implemented]

**Decision 2**: [What was decided]  
**Context**: [Situation requiring decision]  
**Impact**: [Expected effect on current and future work]

### Problem-Solution Pairs
**Problem**: [Issue that was encountered and resolved]  
**Solution**: [How it was solved]  
**Knowledge Gained**: [Learning that should be preserved]

### Alternative Approaches Rejected
**Approach**: [Method that was considered but not used]  
**Rejection Reason**: [Why it wasn't selected]  
**Future Relevance**: [Whether this might be useful later]

## ⚠️ Current Issues and Blockers

### Active Blockers
**Blocker 1**: [Description of issue preventing progress]  
**Impact**: [How this affects current work]  
**Status**: [Investigation/Escalation/Resolution progress]  
**Owner**: [Who is working on resolution]  
**Estimated Resolution**: [When this might be resolved]

**Blocker 2**: [Another blocking issue]  
**Workaround**: [Temporary solution being used]  
**Risk**: [Risk if workaround fails]

### Known Issues (Non-Blocking)
**Issue 1**: [Problem that doesn't prevent progress]  
**Severity**: [Low/Medium/High]  
**Tracking**: [How this is being monitored]  
**Resolution Plan**: [When/how this will be addressed]

**Issue 2**: [Another non-blocking issue]  
**Impact Assessment**: [Effect on system or future work]

### Technical Concerns
**Concern 1**: [Potential future problem or risk]  
**Likelihood**: [Probability this will become a real issue]  
**Mitigation**: [Steps being taken to prevent/minimize]

## 🔄 Continuation Context

### Immediate Next Steps (Next 1-3 Actions)
1. **[Specific Action 1]**  
   - **Description**: [Detailed description of what needs to be done]
   - **Estimated Time**: [X minutes]
   - **Dependencies**: [Prerequisites or requirements]
   - **Risks**: [Potential complications]

2. **[Specific Action 2]**  
   - **Description**: [Detailed description of what needs to be done]
   - **Estimated Time**: [X minutes]
   - **Context Needed**: [Important background information]

3. **[Specific Action 3]**  
   - **Description**: [Detailed description of what needs to be done]
   - **Estimated Time**: [X minutes]
   - **Success Criteria**: [How to know this is done correctly]

### Medium-Term Goals (Next Session)
**Primary Objective**: [Main goal for next work session]  
**Secondary Objectives**: [Additional goals if time permits]  
**Success Metrics**: [How to measure success of next session]  
**Preparation Needed**: [Setup or preparation required before continuing]

### Context Preservation Notes
**Mental Model**: [Important conceptual understanding to preserve]  
**Key Files to Have Open**: [Files that should be loaded in IDE]  
**Environment Configuration**: [Any special settings or configurations]  
**Reference Materials**: [Documentation or examples that are relevant]

## 📚 Knowledge and Learning

### New Knowledge Acquired
**Technical Learning**: [New techniques, patterns, or technologies learned]  
**Domain Learning**: [New understanding about business logic or game mechanics]  
**Process Learning**: [Insights about development workflow or tools]

### Problem Patterns Identified
**Pattern**: [Recurring type of problem or situation]  
**Frequency**: [How often this pattern appears]  
**Standard Solution**: [Effective approach for this pattern]  
**Prevention Strategy**: [How to avoid this pattern in future]

### Documentation Needs Identified
**Missing Documentation**: [Information that should be documented]  
**Outdated Documentation**: [Docs that need updating based on current work]  
**Knowledge Gaps**: [Areas where team knowledge is insufficient]

## 🎯 Risk Assessment

### Technical Risks
**Risk 1**: [Specific technical risk]  
**Probability**: [High/Medium/Low]  
**Impact**: [Severity if this risk materializes]  
**Current Mitigation**: [What is being done to address this]  
**Escalation Trigger**: [Conditions that would require escalation]

**Risk 2**: [Another technical risk]  
**Early Warning Signs**: [How to detect if this risk is materializing]  
**Contingency Plan**: [What to do if this risk becomes reality]

### Project Risks
**Timeline Risk**: [Risk to schedule or delivery]  
**Scope Risk**: [Risk of scope creep or requirements change]  
**Quality Risk**: [Risk to code quality or system stability]  
**Resource Risk**: [Risk related to availability of resources or dependencies]

## 📈 Performance Context

### Current Performance Metrics
**Frame Time**: [Current system performance measurement]  
**Memory Usage**: [Current memory consumption]  
**Entity Count**: [Number of entities currently processed]  
**Bottlenecks**: [Known performance bottlenecks]

### Performance Impact of Current Work
**Expected Impact**: [How current changes will affect performance]  
**Measurements Taken**: [Performance tests or profiling done]  
**Optimization Opportunities**: [Performance improvements identified]  
**Performance Risks**: [Ways current work might hurt performance]

## 🔧 Environment and Tools

### Development Environment State
**IDE Configuration**: [Any special settings or plugins active]  
**Debugging State**: [Debugger attached, breakpoints set, etc.]  
**Profiling Tools**: [Performance monitoring tools active]  
**External Tools**: [Other tools or services being used]

### Workspace Organization
**Open Files**: [Key files currently open in editor]  
**Window Layout**: [Important aspects of current workspace setup]  
**Running Processes**: [Background processes or services needed]

---

## 🎯 Recovery Instructions

### Quick Recovery (< 2 minutes)
1. **Open Primary File**: `[path/to/current/file.cs]`
2. **Navigate to Location**: [Line number or method name]
3. **Review Context**: [Read these specific comments or sections]
4. **Check Status**: [Verify current state matches checkpoint expectations]
5. **Resume Work**: [Execute the immediate next action described above]

### Standard Recovery (< 5 minutes)
1. **Environment Setup**: [IDE configuration and file setup]
2. **Git State Verification**: [Confirm repository state]
3. **Build Verification**: [Ensure project compiles]
4. **Test Verification**: [Run relevant test subset]
5. **Context Loading**: [Review session goals and current objectives]
6. **Work Resumption**: [Begin with immediate next steps]

### Deep Recovery (< 15 minutes)
1. **Full Context Review**: [Read session log and work plan]
2. **State Validation**: [Comprehensive verification of system state]
3. **Progress Assessment**: [Understand current position in work plan]
4. **Risk Evaluation**: [Review current risks and blockers]
5. **Goal Alignment**: [Confirm current work aligns with objectives]
6. **Strategic Planning**: [Update approach based on current context]

## 📊 Checkpoint Quality Metrics

### Completeness Assessment
- [ ] **All essential information captured**
- [ ] **Technical state accurately described**  
- [ ] **Continuation path clearly defined**
- [ ] **Recovery instructions specific and actionable**

### Accuracy Verification
- [ ] **Current state matches system reality**
- [ ] **File locations and code references correct**
- [ ] **Time estimates realistic based on experience**
- [ ] **Risk assessment reflects actual situation**

### Usability Check
- [ ] **Another developer could continue work from this checkpoint**
- [ ] **Recovery instructions tested and validated**
- [ ] **Information organized for quick comprehension**
- [ ] **Critical information easily identifiable**

---

**Checkpoint Created By**: [Creator name/identifier]  
**Validation Status**: [Self-validated/Peer-reviewed/Untested]  
**Next Checkpoint Due**: [Estimated time for next checkpoint]  
**Archive Date**: [When this checkpoint should be archived]