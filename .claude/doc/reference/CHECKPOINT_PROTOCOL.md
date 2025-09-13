---
category: reference
tags: [workflow, checkpoint, session-management, continuity, recovery]
related: [WORK_SESSION_TRACKER.md, WORK_PLANNING_PROTOCOL.md, DEVELOPMENT_WORKFLOW.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# Checkpoint Protocol

[🇰🇷 한국어 버전](./CHECKPOINT_PROTOCOL_KOR.md)

## 📍 Navigation

[↩️ Back to Reference](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## 🎯 Purpose

**Systematic checkpoint creation and management protocol** ensuring reliable work state preservation, enabling seamless work continuity and rapid recovery from interruptions or failures.

## 1. Checkpoint Architecture

### 1.1 Checkpoint Types

```yaml
Checkpoint Categories:
  Micro Checkpoint (every 30 minutes):
    Trigger: Regular progress preservation
    Content: Current task state, immediate next steps
    Recovery Time: <2 minutes
    Usage: Short-term interruption recovery
    
  Standard Checkpoint (every 2 hours):
    Trigger: Scheduled session breakpoints
    Content: Complete context snapshot, progress assessment
    Recovery Time: <5 minutes
    Usage: Session boundary management
    
  Major Checkpoint (task/milestone completion):
    Trigger: Significant progress milestones
    Content: Achievement summary, validation results, next phase planning
    Recovery Time: <3 minutes
    Usage: Work phase transitions
    
  Emergency Checkpoint (on-demand):
    Trigger: Unexpected interruption or critical decision points
    Content: Critical state preservation, urgent continuation needs
    Recovery Time: <1 minute
    Usage: Immediate interruption handling
```

### 1.2 Checkpoint Data Structure

```yaml
Checkpoint Information Hierarchy:
  
  Level 1 - Critical State:
    Current Task: Active TodoList item and completion percentage
    Code Location: Specific files/functions being modified
    Last Action: Most recent development action taken
    Immediate Next: Planned next 1-3 specific actions
    
  Level 2 - Context State:
    Session Objectives: Current session goals and priorities
    Technical Approach: Method/strategy being used
    Decision Trail: Recent technical choices and rationale
    Known Issues: Identified problems and current resolution status
    
  Level 3 - Environment State:
    Build Status: Compilation state and error status
    Test Status: Test execution results and coverage
    Git Status: Working directory state and pending changes
    Performance Metrics: Current performance measurements
    
  Level 4 - Planning State:
    Work Plan Reference: Link to active work plan document
    Progress Assessment: Completion against planned milestones
    Risk Status: Current risk factors and mitigation status
    Resource Requirements: Continuing resource needs and availability
```

## 2. Checkpoint Creation Protocol

### 2.1 Automatic Checkpoint Triggers

#### **Time-Based Triggers**
```yaml
Micro Checkpoints (30 minutes):
  Condition: 30 minutes of continuous work
  Action: Create lightweight state snapshot
  Content:
    - Current file and line of focus
    - Last completed action
    - Next intended action
    - Any blocking issues encountered
  
  Quality Gate:
    - TodoList reflects current reality
    - No uncommitted critical changes
    - Basic functionality still working

Standard Checkpoints (2 hours):
  Condition: 2 hours of active development
  Action: Create comprehensive context snapshot
  Content:
    - Complete session progress assessment
    - Technical decisions made and rationale
    - Testing status and validation results
    - Updated risk assessment and mitigation
  
  Quality Gate:
    - All changes committed with descriptive messages
    - Tests passing for completed functionality
    - Documentation updated for significant changes
    - No known critical issues left unaddressed
```

#### **Event-Based Triggers**
```yaml
Task Completion:
  Condition: TodoList task marked as completed
  Action: Create achievement checkpoint
  Content:
    - Completion validation evidence
    - Integration test results
    - Performance impact assessment
    - Next task readiness verification
  
  Quality Gate:
    - Completion criteria fully satisfied
    - Quality validation passed
    - No regressions introduced
    - Documentation updated

Context Switch:
  Condition: Changing focus between major components or systems
  Action: Create context boundary checkpoint
  Content:
    - Current context completion state
    - Handoff information for new context
    - Dependencies between contexts
    - Context switch impact assessment
  
  Quality Gate:
    - Current context in stable state
    - All context-specific changes committed
    - No loose ends that could cause issues
    - Clear continuation path defined

Critical Decision:
  Condition: Making significant architectural or implementation decisions
  Action: Create decision checkpoint
  Content:
    - Decision description and rationale
    - Alternatives considered and rejected
    - Implementation implications
    - Validation criteria for decision success
  
  Quality Gate:
    - Decision thoroughly analyzed
    - Stakeholder considerations documented
    - Implementation plan clear
    - Rollback strategy defined
```

### 2.2 Manual Checkpoint Creation

#### **Emergency Checkpoints**
```yaml
Immediate Interruption:
  Usage: Unexpected need to stop work immediately
  Time Limit: <2 minutes to create
  Essential Content:
    - Current exact state and percentage complete
    - Critical next step for continuation
    - Any urgent issues requiring immediate attention
    - Essential context for rapid resumption
  
  Creation Process:
    1. Update TodoList with current task reality (30 seconds)
    2. Commit current work with "CHECKPOINT:" prefix (30 seconds)
    3. Create emergency checkpoint file (60 seconds)
    4. Note any critical issues or blockers (30 seconds)

Planned Interruption:
  Usage: Known need to pause work (meeting, break, end of day)
  Time Limit: <10 minutes to create comprehensive checkpoint
  Content:
    - Complete current state assessment
    - Progress validation and testing
    - Clean code state with descriptive commits
    - Detailed continuation planning
  
  Creation Process:
    1. Complete current logical unit of work (variable)
    2. Run tests and validate current functionality (2-3 minutes)
    3. Commit all changes with clear descriptions (2 minutes)
    4. Create comprehensive checkpoint documentation (3-5 minutes)
    5. Update work plan and TodoList (2 minutes)
```

#### **Strategic Checkpoints**
```yaml
Before Major Changes:
  Usage: Before implementing significant modifications
  Purpose: Create rollback point and context preservation
  Content:
    - Current working state validation
    - Proposed change description and rationale
    - Risk assessment and mitigation plan
    - Success criteria for proposed changes
  
  Quality Requirements:
    - All current functionality tested and working
    - Clean git state with descriptive commit history
    - Performance baseline established
    - Documentation current and accurate

After Problem Resolution:
  Usage: After solving significant bugs or technical challenges
  Purpose: Preserve solution knowledge and context
  Content:
    - Problem description and root cause analysis
    - Solution approach and implementation details
    - Testing validation and verification results
    - Prevention strategies for similar issues
  
  Quality Requirements:
    - Solution thoroughly tested and validated
    - Root cause clearly identified and documented
    - Fix integrated without introducing regressions
    - Knowledge captured for future reference
```

## 3. Checkpoint Content Standards

### 3.1 Minimum Viable Checkpoint

```yaml
Essential Information (every checkpoint):
  Timestamp: Exact time of checkpoint creation
  Session ID: Reference to current work session
  Task State: Current TodoList task and completion status
  Code State: Current file/function being worked on
  Last Action: Most recent development action completed
  Next Action: Specific next step planned for continuation
  Build State: Current compilation and basic test status
  Critical Issues: Any blocking problems or urgent concerns
```

### 3.2 Comprehensive Checkpoint

```yaml
Complete Context Information:
  
  Session Context:
    Work Plan: Reference to active work plan document
    Session Objectives: Current session goals and priorities
    Progress Summary: Achievements and milestones reached
    Time Investment: Actual time spent vs. estimated time
    
  Technical Context:
    Architecture Decisions: Recent design choices and rationale
    Performance Metrics: Current performance measurements
    Testing Status: Test coverage and validation results
    Integration State: System integration and compatibility status
    
  Knowledge Context:
    Learning Outcomes: New knowledge or insights gained
    Problem Solutions: Issues resolved and solution approaches
    Best Practices: Effective techniques or patterns discovered
    Mistakes Learned: Errors made and lessons learned
    
  Continuation Context:
    Immediate Priorities: Next 3-5 specific actions to take
    Resource Requirements: Tools, documentation, or dependencies needed
    Risk Factors: Potential issues or complications to watch for
    Success Criteria: How to validate successful continuation
```

## 4. Checkpoint Recovery Protocol

### 4.1 Rapid Recovery Process

#### **Context Restoration (< 5 minutes)**
```yaml
Step 1: Checkpoint Validation (1 minute)
  Actions:
    - Locate most recent relevant checkpoint
    - Verify checkpoint completeness and currency
    - Assess time gap since checkpoint creation
    - Identify any intervening changes or updates
  
  Validation Criteria:
    - Checkpoint less than 4 hours old
    - Contains all essential information elements
    - Technical state still valid and current
    - No major external changes since creation

Step 2: Environment Restoration (2 minutes)
  Actions:
    - Restore git state to checkpoint commit
    - Verify build and compilation status
    - Run basic test suite to validate functionality
    - Check Unity project and package integrity
  
  Validation Criteria:
    - Code compiles without errors
    - Basic tests pass successfully
    - Unity project opens without issues
    - No missing dependencies or references

Step 3: Context Loading (2 minutes)
  Actions:
    - Review checkpoint context and state information
    - Restore TodoList to checkpoint state
    - Load relevant documentation and work plans
    - Refresh understanding of current objectives
  
  Validation Criteria:
    - Clear understanding of current task and progress
    - TodoList accurately reflects current state
    - Work objectives and priorities clear
    - Continuation path clearly defined
```

### 4.2 Detailed Recovery Process

#### **Comprehensive Context Restoration (< 15 minutes)**
```yaml
Phase 1: State Verification (5 minutes)
  Technical Verification:
    - Full build and test suite execution
    - Performance baseline validation
    - Integration test verification
    - Code quality metrics validation
  
  Context Verification:
    - Work plan alignment assessment
    - Progress against milestones validation
    - Risk factor current status review
    - Resource availability confirmation

Phase 2: Gap Analysis (5 minutes)
  Change Assessment:
    - Identify any changes since last checkpoint
    - Assess impact of external updates or modifications
    - Review any new requirements or constraints
    - Evaluate progress against original timeline
  
  Priority Adjustment:
    - Update priorities based on current context
    - Adjust approach based on new information
    - Revise timeline estimates if necessary
    - Update risk assessment and mitigation plans

Phase 3: Continuation Planning (5 minutes)
  Immediate Planning:
    - Define next 3-5 specific actions
    - Identify any required preparation or setup
    - Confirm resource availability and dependencies
    - Set checkpoint schedule for continuing work
  
  Quality Assurance:
    - Establish validation criteria for continued work
    - Define testing approach for new changes
    - Plan documentation updates and maintenance
    - Set performance and quality targets
```

## 5. Checkpoint Quality Assurance

### 5.1 Checkpoint Validation

```yaml
Content Quality Checks:
  Completeness:
    - [ ] All essential information elements present
    - [ ] Technical context sufficiently detailed
    - [ ] Continuation path clearly defined
    - [ ] Critical issues and blockers documented
  
  Accuracy:
    - [ ] Current state accurately reflects reality
    - [ ] Code state matches checkpoint description
    - [ ] Progress assessment realistic and measurable
    - [ ] Time estimates based on actual experience
  
  Clarity:
    - [ ] Information clearly written and understandable
    - [ ] Technical decisions well-explained
    - [ ] Next steps specific and actionable
    - [ ] Context sufficient for someone else to continue
  
  Currency:
    - [ ] Information current and up-to-date
    - [ ] No outdated references or assumptions
    - [ ] Reflects latest code and documentation state
    - [ ] Incorporates recent changes and decisions
```

### 5.2 Recovery Testing

```yaml
Recovery Validation Process:
  Self-Recovery Test:
    Method: Test your own ability to recover from checkpoint
    Timeline: Wait 24-48 hours, then attempt full context restoration
    Success Criteria: Full productive work resumption within 10 minutes
    Feedback: Identify missing information and improve checkpoint process
  
  Cross-Recovery Test:
    Method: Another developer attempts to continue work from checkpoint
    Timeline: Fresh perspective without prior session context
    Success Criteria: Productive work continuation within 15 minutes
    Feedback: Validate checkpoint completeness and clarity
  
  Stress Recovery Test:
    Method: Recovery under suboptimal conditions (tired, distracted, time pressure)
    Timeline: Challenging recovery scenarios
    Success Criteria: Successful recovery even under stress
    Feedback: Ensure checkpoint robustness and reliability
```

## 6. Checkpoint Management

### 6.1 Checkpoint Storage and Organization

```yaml
File Organization:
  Directory Structure:
    .claude/checkpoints/
      YYYY-MM/
        YYYY-MM-DD_session-id/
          checkpoints/
            micro/
            standard/
            major/
            emergency/
  
  Naming Convention:
    CHECKPOINT_[type]_[timestamp]_[session-id].md
    Examples:
      - CHECKPOINT_micro_20250913_1430_invest-automation.md
      - CHECKPOINT_standard_20250913_1600_invest-automation.md
      - CHECKPOINT_emergency_20250913_1445_invest-automation.md
  
  Retention Policy:
    Micro Checkpoints: Keep for 1 week
    Standard Checkpoints: Keep for 1 month
    Major Checkpoints: Keep for 6 months
    Emergency Checkpoints: Keep for 3 months
```

### 6.2 Checkpoint Maintenance

```yaml
Regular Maintenance:
  Weekly Cleanup:
    - Remove outdated micro checkpoints
    - Archive completed work checkpoints
    - Validate checkpoint integrity and accessibility
    - Update checkpoint index and references
  
  Monthly Review:
    - Assess checkpoint effectiveness and utility
    - Identify improvement opportunities
    - Update checkpoint templates and standards
    - Optimize checkpoint creation and recovery processes
  
  Quarterly Optimization:
    - Analyze checkpoint usage patterns and effectiveness
    - Refine checkpoint creation triggers and content
    - Improve recovery processes and tools
    - Update documentation and training materials
```

## 7. Integration with Work Management

### 7.1 TodoList Integration

```yaml
Checkpoint-TodoList Synchronization:
  At Checkpoint Creation:
    - Update TodoList to reflect current accurate state
    - Mark completed tasks with evidence and validation
    - Update in-progress tasks with completion percentage
    - Add any newly discovered tasks or dependencies
  
  At Recovery:
    - Restore TodoList from checkpoint state
    - Validate current state against TodoList expectations
    - Update any tasks based on intervening changes
    - Confirm next task priorities and dependencies
  
  Quality Assurance:
    - TodoList state must be consistent with checkpoint reality
    - All task state changes must have supporting evidence
    - Progress estimates must be realistic and measurable
    - Dependencies and blockers must be clearly identified
```

### 7.2 Work Plan Integration

```yaml
Work Plan Synchronization:
  Progress Updates:
    - Update work plan with checkpoint progress information
    - Document any scope changes or requirement modifications
    - Update timeline estimates based on actual progress
    - Revise risk assessment based on discovered issues
  
  Decision Documentation:
    - Record significant technical decisions in work plan
    - Update architectural approach based on implementation learning
    - Document any changes to success criteria or validation
    - Maintain traceability from requirements to implementation
  
  Quality Maintenance:
    - Ensure work plan remains current and accurate
    - Validate checkpoint progress against planned milestones
    - Maintain consistency between checkpoint and plan information
    - Update work plan based on checkpoint insights and learning
```

---

## 🎯 Checkpoint Success Criteria

**Recovery Effectiveness:**
- ✅ **<5 minute recovery**: Full context restoration from standard checkpoints within 5 minutes
- ✅ **<2 minute emergency recovery**: Critical state restoration from emergency checkpoints within 2 minutes
- ✅ **100% continuity**: No work lost due to inadequate checkpoint coverage
- ✅ **Cross-developer usability**: Other developers can continue work from checkpoints within 15 minutes

**Quality Assurance:**
- ✅ **Complete information**: All essential context preserved in every checkpoint
- ✅ **Accurate state**: Checkpoint information exactly matches actual system state
- ✅ **Clear continuation**: Next steps clearly defined and immediately actionable
- ✅ **Validated recovery**: All checkpoints tested for successful recovery

**Process Efficiency:**
- ✅ **<10% overhead**: Checkpoint creation and management less than 10% of total work time
- ✅ **Automated triggers**: Checkpoint creation automatically triggered by appropriate events
- ✅ **Optimized content**: Checkpoint information optimized for rapid comprehension and action
- ✅ **Continuous improvement**: Checkpoint process continuously refined based on effectiveness metrics

---

**Remember: Effective checkpoints are the insurance policy for your development work. Invest in systematic checkpoint creation to protect against loss and enable rapid recovery from any interruption.**