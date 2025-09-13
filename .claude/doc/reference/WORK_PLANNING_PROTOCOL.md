---
category: reference
tags: [workflow, planning, protocol, mandatory, collaboration]
related: [DEVELOPMENT_WORKFLOW.md, DOMAIN_KNOWLEDGE.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: critical
---

# Work Planning Protocol

[🇰🇷 한국어 버전](./WORK_PLANNING_PROTOCOL_KOR.md)

## 📍 Navigation

[↩️ Back to Reference](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## 🚨 MANDATORY PROTOCOL

**This planning protocol MUST be followed before starting any development work.**

## 1. Pre-Work Consultation Phase (15-20 minutes)

### 1.1 Document Guidance System

#### **Step 1: Essential Document Check**
Before discussing the work, I will guide you to relevant documentation:

```yaml
Required Reading Check:
  Domain Knowledge: 
    File: .claude/doc/reference/DOMAIN_KNOWLEDGE.md
    Status: [✅ Read / ❌ Need to read]
    Time: 10-15 minutes
  
  Related Architecture:
    Files: [List of relevant architecture docs]
    Status: [✅ Read / ❌ Need to read]
    Time: 5-10 minutes per document

  Game Design Context:
    Files: [List of relevant game design docs]  
    Status: [✅ Read / ❌ Need to read]
    Time: Variable based on scope
```

#### **Step 2: Missing Documentation Assessment**
If essential documentation is missing, I will:
1. **Identify the gap**: "We need a [System Design] document for this work"
2. **Assess necessity**: "This is critical because [reason]"
3. **Propose creation**: "Should we create this document first?"
4. **Estimate time**: "This will take approximately [time] to document properly"

### 1.2 Interactive Requirement Gathering

#### **Essential Questions Checklist**
```yaml
Scope & Scale:
  - [ ] What is the final objective of this work?
  - [ ] How many entities will be affected? (>1000 = ECS mandatory)
  - [ ] Is this performance-critical? (hot path analysis)
  - [ ] What are the success criteria?

Technical Constraints:
  - [ ] Does this require UI integration?
  - [ ] What are the dependencies on existing code?
  - [ ] Are there Unity version constraints?
  - [ ] Mobile/PC platform considerations?

Timeline & Resources:
  - [ ] What is the preferred timeline?
  - [ ] Are there blocking dependencies?
  - [ ] Can this be broken into smaller tasks?
  - [ ] What is the risk tolerance?
```

#### **Project-Specific Constraints**
```yaml
Unity Technical Stack:
  - Engine: Unity 6000.2.0f1
  - Architecture: Unity DOTS (ECS)
  - Performance Target: 100,000+ entities @ 60fps
  - Platforms: Mobile/PC cross-platform

YouAreCapitalist Game Constraints:
  - Data-driven simulation (not visual game)
  - 3-layer architecture (ECS/Bridge/UI)
  - Automation system integration
  - Economic simulation accuracy
```

## 2. Work Breakdown Structure (WBS)

### 2.1 Task Hierarchy Definition
```yaml
Epic (1-2 weeks):
  - Large feature implementation
  - System architecture changes
  - Major refactoring initiatives
  - Example: "Implement complete Pop simulation system"

Story (2-3 days):
  - Implementable feature units
  - Testable components
  - Clear acceptance criteria
  - Example: "Create PopulationBehaviorSystem with basic AI"

Task (2-4 hours):
  - Concrete implementation work
  - Single responsibility focus
  - Measurable completion
  - Example: "Implement PopulationData ECS component"

Subtask (30 minutes - 2 hours):
  - Specific detailed steps
  - No further breakdown needed
  - Immediate actionable work
  - Example: "Add Burst compilation to PopulationJob"
```

### 2.2 Priority Matrix Framework
```yaml
Priority Levels:
  P0 - Critical (Immediate):
    - Blocking other work
    - Performance/stability issues
    - Security vulnerabilities
  
  P1 - High (This Sprint):
    - Important features
    - Architectural improvements
    - User-facing functionality
  
  P2 - Medium (Next Sprint):
    - Nice-to-have features
    - Code quality improvements
    - Non-critical optimizations
  
  P3 - Low (Backlog):
    - Future enhancements
    - Experimental features
    - Documentation updates
```

### 2.3 Dependency Mapping
```yaml
Dependency Types:
  Technical:
    - Code dependencies (must implement X before Y)
    - System dependencies (ECS before UI bridge)
    - External dependencies (Unity packages)
  
  Knowledge:
    - Documentation dependencies (need specs before coding)
    - Decision dependencies (need architecture decision)
    - Review dependencies (need expert validation)
  
  Resource:
    - Time dependencies (sequence constraints)
    - Tool dependencies (profiler, testing tools)
    - Environment dependencies (development setup)
```

## 3. Collaborative Planning Session

### 3.1 Dialogue Framework

#### **Opening Discussion**
```
Assistant: "I see you want to [work description]. Before we start coding, let's make sure we have everything we need:

1. 📚 Have you reviewed the Domain Knowledge document? It covers Unity ECS patterns essential for this work.

2. 🔍 I've checked our documentation and found:
   ✅ Available: [list of relevant docs]
   ❌ Missing: [list of needed docs]
   
3. 💡 Based on your description, I estimate this involves:
   - Scale: [entity count estimate]
   - Architecture: [ECS/MonoBehaviour recommendation]
   - Timeline: [rough estimate]

Would you like to create a detailed plan together?"
```

#### **Requirement Clarification**
```yaml
Iterative Questions:
  Round 1: High-level understanding
    - "What problem are we solving?"
    - "Who are the users/systems affected?"
    - "What does success look like?"
  
  Round 2: Technical details
    - "How does this fit into existing architecture?"
    - "What are the performance requirements?"
    - "Are there any constraints or limitations?"
  
  Round 3: Implementation approach
    - "What's your preferred technical approach?"
    - "How should we handle [specific technical challenge]?"
    - "What are the testing requirements?"
```

### 3.2 Plan Documentation Generation

#### **Work Plan Creation**
```yaml
Generated Outputs:
  1. WORK_PLAN_[YYYY-MM-DD].md:
     - Objective statement
     - Technical approach
     - Task breakdown
     - Success criteria
     - Risk assessment

  2. TodoList (via TodoWrite):
     - Prioritized task list
     - Progress tracking
     - Checkpoint markers
     - Dependencies noted

  3. Reference Links:
     - Related documentation
     - Code examples
     - Performance benchmarks
```

## 4. Risk Assessment & Mitigation

### 4.1 Risk Categories
```yaml
Technical Risks:
  Performance:
    - Risk: Frame rate drops with large entity counts
    - Mitigation: ECS + Job System + LOD implementation
    - Monitoring: Continuous profiling

  Architecture:
    - Risk: Breaking existing system integration
    - Mitigation: Interface-based design, gradual rollout
    - Monitoring: Integration tests

  Compatibility:
    - Risk: Unity version incompatibilities
    - Mitigation: Version pinning, compatibility testing
    - Monitoring: Build verification

Project Risks:
  Scope Creep:
    - Risk: Requirements expanding during implementation
    - Mitigation: Clear scope documentation, change control
    - Monitoring: Regular scope review

  Knowledge Gaps:
    - Risk: Unfamiliarity with ECS patterns
    - Mitigation: Documentation study, proof-of-concept
    - Monitoring: Code review checkpoints

  Time Estimation:
    - Risk: Underestimating complexity
    - Mitigation: Conservative estimates, buffer time
    - Monitoring: Progress tracking every 30 minutes
```

### 4.2 Mitigation Strategies
```yaml
Preventive Measures:
  - Mandatory document review before coding
  - Proof-of-concept for uncertain approaches
  - Regular checkpoint creation
  - Incremental implementation with testing

Contingency Plans:
  - Performance fallback: LOD system activation
  - Architecture fallback: MonoBehaviour alternative
  - Timeline fallback: Scope reduction options
  - Quality fallback: Technical debt documentation
```

## 5. Success Criteria Definition

### 5.1 Acceptance Criteria Template
```yaml
Functional Requirements:
  - [ ] Feature works as specified
  - [ ] All edge cases handled
  - [ ] Error handling implemented
  - [ ] User experience validated

Technical Requirements:
  - [ ] Performance targets met (specific metrics)
  - [ ] Memory usage within bounds
  - [ ] ECS patterns properly implemented
  - [ ] Integration tests passing

Quality Requirements:
  - [ ] Code review completed
  - [ ] Documentation updated
  - [ ] Test coverage >80%
  - [ ] Performance profiled
```

### 5.2 Definition of Done
```yaml
Implementation Complete:
  ✅ All tasks in TodoList completed
  ✅ Code compiles without warnings
  ✅ All tests passing
  ✅ Performance benchmarks met

Quality Assurance:
  ✅ Code review approved
  ✅ Architecture compliance verified
  ✅ Documentation updated
  ✅ Integration verified

Deployment Ready:
  ✅ Build verification passed
  ✅ Performance regression test passed
  ✅ No new technical debt introduced
  ✅ Handoff documentation complete
```

## 6. Planning Session Examples

### 6.1 Simple Task Planning

**Example 1: Simple ECS Component Addition**

```
User: "I want to add a new ECS component for population income"

Assistant: "I'll help you add a population income ECS component. Let me first check our documentation:

📚 Have you reviewed our Domain Knowledge document? It covers ECS component patterns essential for this work.

🔍 I've checked our documentation:
   ✅ Available: DOMAIN_KNOWLEDGE.md (ECS patterns and performance guidelines)
   ✅ Available: DEVELOPMENT_WORKFLOW.md (coding standards and validation)
   ❌ Missing: Population economic system design document

💡 Based on your request, this involves:
   - Scale: Single component creation (~100 entities initially)
   - Architecture: Pure ECS data component (no methods)
   - Timeline: ~30 minutes implementation + testing

This is a simple task that doesn't require extensive planning. Shall we proceed directly?"

User: "Yes, let's proceed"

Assistant: Creates TodoList with:
  - Create PopulationIncomeData component
  - Add component to existing systems
  - Update integration tests
```

**Example 2: Complex Feature Implementation**

```
User: "I need to implement a complete market sentiment analysis system"

Assistant: "This is a significant feature that requires careful planning. Let me start our consultation:

📚 Document Review Required:
   - Domain Knowledge (ECS patterns): 15 minutes
   - Economic System Architecture: 10 minutes  
   - Market Data Design: 5 minutes

🔍 Documentation Assessment:
   ✅ Available: DOMAIN_KNOWLEDGE.md, technical-architecture.md
   ❌ Missing: Market sentiment system design
   ❌ Missing: Data ingestion pipeline specification
   
💡 This appears to be a complex system requiring:
   - Multiple ECS systems integration
   - External data processing
   - Real-time analysis capabilities
   
Let's spend 15-20 minutes planning this properly. First, what's the scope of sentiment analysis you need?

**Essential Questions:**
- How many market entities will this analyze? (>1000 requires ECS optimization)
- What data sources will feed sentiment analysis?
- Do you need real-time updates or periodic batch processing?
- What's the performance target for analysis updates?
- How will this integrate with existing market systems?"

[Interactive planning session follows with requirement gathering]
```

### 6.2 Complex Planning Session

**Example: Multi-System Integration**

```
User: "I want to implement a complete automation system for investment decisions"

Assistant: "This is a complex system that will affect multiple parts of our architecture. Let's plan this systematically:

## Pre-Planning Document Review (15 minutes)
**Required Reading:**
  📚 Domain Knowledge: Unity ECS patterns and performance requirements
  🏗️ Technical Architecture: System integration patterns  
  🎮 Investment Loop Mechanics: Business logic and automation levels
  ⚠️ Missing: AI decision-making system specification

## Requirement Gathering Session

**Scope & Scale Questions:**
- Final Objective: What level of automation (Manual → Assisted → Semi-Auto → Full Auto)?
- Entity Scale: How many investment decisions per frame (performance critical?)  
- Success Criteria: What defines successful automated investment?
- Risk Tolerance: How do we handle edge cases and failures?

**Technical Constraints:**
- Unity ECS Integration: Will this use Job System for parallel processing?
- UI Integration: How will users monitor/override automated decisions?
- Data Dependencies: What market data systems must this integrate with?
- Performance Target: Frame rate impact acceptable?

**Timeline & Resources:**
- Preferred Timeline: Days or weeks of implementation?
- Blocking Dependencies: What systems must exist first?
- Testing Strategy: How do we validate decision quality?

## Interactive Planning

Assistant: "Based on our conversation, I recommend:

1. **Architecture Approach**: 
   - ECS-based decision system for performance
   - Strategy pattern for different automation levels
   - Event-driven UI communication

2. **Implementation Phases**:
   - Phase 1: Core decision framework (2-3 days)
   - Phase 2: Market data integration (1-2 days)  
   - Phase 3: UI and user controls (1-2 days)
   - Phase 4: Testing and validation (1 day)

3. **Risk Assessment**:
   - High: Market data reliability and performance impact
   - Medium: AI decision quality and user override complexity
   - Low: UI integration (established patterns exist)

Shall I create a detailed work plan document for this implementation?"
```

## 7. Planning Session Outcomes

### 7.1 Generated Documentation

**For Every Planning Session, Generate:**

```yaml
Work Plan Document:
  File: .claude/doc/workplans/WORK_PLAN_[YYYY-MM-DD]_[feature-name].md
  Contents:
    - Objective Statement
    - Technical Approach Summary
    - Task Breakdown (Epic/Story/Task hierarchy)
    - Success Criteria & Validation
    - Risk Assessment & Mitigation
    - Resource Requirements
    - Timeline Estimation

TodoList (TodoWrite):
  Tasks: Prioritized implementation tasks
  States: pending/in_progress/completed tracking
  Dependencies: Task sequence and blocking relationships
  Checkpoints: Major milestones for progress validation

Reference Documentation:
  Links: Related documents and code examples
  Patterns: Architectural patterns to follow
  Benchmarks: Performance and quality targets
  Validation: Testing and acceptance criteria
```

### 7.2 Session Handoff Protocol

```yaml
Session Checkpoint Creation:
  Trigger: Every 2 hours of work or before session break
  Contents:
    - Current task status and completion percentage
    - Work artifacts created (files, tests, documentation)
    - Known issues and blocking dependencies
    - Next steps and priority sequence
    - Context preservation for session resumption

Session Resume Protocol:
  Review: Previous checkpoint and work plan status
  Validation: Verify current state matches checkpoint
  Planning: Assess any changes in requirements or constraints
  Execution: Continue from documented next steps
```

## 8. Quality Assurance

### 8.1 Planning Quality Gates

```yaml
Planning Completeness Check:
  - [ ] Objective clearly defined with success criteria
  - [ ] Technical approach validated against architecture
  - [ ] All dependencies identified and availability confirmed
  - [ ] Performance requirements specified and feasible
  - [ ] Risk assessment completed with mitigation strategies
  - [ ] Resource requirements estimated and available
  - [ ] Timeline realistic based on complexity assessment
  - [ ] Testing strategy defined with acceptance criteria

Documentation Quality Check:
  - [ ] Work plan document created and accessible
  - [ ] TodoList properly structured with dependencies
  - [ ] Reference documentation linked and current
  - [ ] Success criteria measurable and testable
  - [ ] Risk mitigation strategies actionable
```

### 8.2 Continuous Planning Validation

```yaml
Daily Validation (if multi-day work):
  - Progress against TodoList tasks
  - Blocker identification and resolution
  - Requirement changes or clarifications needed
  - Resource availability and timeline adjustments

Weekly Planning Review (if multi-week work):
  - Objective alignment with evolving requirements  
  - Architecture decision validation
  - Performance target progress
  - Risk materialization and mitigation effectiveness
```

---

## 🎯 Protocol Success Metrics

**Planning Effectiveness:**
- ✅ **95%+ Work Completion Rate**: Tasks planned vs. tasks completed successfully
- ✅ **<10% Scope Creep**: Requirements changes during implementation
- ✅ **Zero Critical Blockers**: No work-stopping dependencies discovered post-planning
- ✅ **Timeline Accuracy**: ±20% of estimated completion time

**Quality Outcomes:**  
- ✅ **Architecture Compliance**: All implementations follow established patterns
- ✅ **Performance Targets**: Meet or exceed specified performance requirements
- ✅ **Test Coverage**: ≥90% coverage for planned functionality
- ✅ **Documentation Currency**: All related documentation updated and accurate

**Collaboration Effectiveness:**
- ✅ **Requirement Clarity**: <5% clarification requests during implementation
- ✅ **Context Preservation**: Seamless work resumption after breaks
- ✅ **Knowledge Transfer**: Complete handoff documentation for future work

---

**Remember: This protocol transforms ad-hoc requests into structured, successful implementations. Invest 15-20 minutes in planning to save hours in execution and rework.**