---
category: template
tags: [template, work-plan, planning, documentation]
related: [WORK_PLANNING_PROTOCOL.md, SESSION_LOG_TEMPLATE.md]
parent: ../reference/WORK_PLANNING_PROTOCOL.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# Work Plan Template

[🇰🇷 한국어 버전](./WORK_PLAN_TEMPLATE_KOR.md)

## 📍 Navigation

[📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 🎯 Template Usage

**File Naming Convention**: `WORK_PLAN_[YYYY-MM-DD]_[feature-name].md`

**Example**: `WORK_PLAN_2025-09-13_investment-automation.md`

---

# Work Plan: [Feature/System Name]

**Date**: [YYYY-MM-DD]  
**Estimated Duration**: [X hours/days]  
**Complexity Level**: [Simple/Moderate/Complex]  
**Priority**: [P0-Critical/P1-High/P2-Medium/P3-Low]  

## 📋 Objective Statement

### Primary Goal
[Clear, specific description of what needs to be accomplished]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

### User Value
[How this work benefits users or improves the system]

## 🏗️ Technical Approach

### Architecture Decision
**Approach**: [ECS/MonoBehaviour/Hybrid]  
**Justification**: [Why this approach was selected]

### Key Components
1. **[Component Name]**
   - Purpose: [What this component does]
   - Location: `Assets/Scripts/[path]`
   - Dependencies: [List of dependencies]

2. **[System Name]**
   - Purpose: [What this system does]  
   - Update Group: [ECS update group if applicable]
   - Performance Target: [Specific metrics]

### Data Structure Design
```csharp
// Example ECS Component Structure
public struct [ComponentName]Data : IComponentData
{
    public float [field1];
    public int [field2];
    // Pure data only - no methods
}
```

### Performance Considerations
- **Entity Scale**: [Expected number of entities]
- **Frame Time Budget**: [Target milliseconds per frame]
- **Memory Usage**: [Expected memory footprint]
- **Optimization Strategy**: [Job System/Burst/LOD/etc.]

## 📊 Work Breakdown Structure

### Epic Level (if applicable)
**Epic**: [Large feature name]  
**Timeline**: [1-2 weeks]  
**Description**: [High-level feature description]

### Story Level
**Story 1**: [Implementable feature unit]  
**Estimate**: [2-3 days]  
**Acceptance Criteria**:
- [ ] [Specific testable outcome]
- [ ] [Specific testable outcome]

**Story 2**: [Another feature unit]  
**Estimate**: [1-2 days]  
**Acceptance Criteria**:
- [ ] [Specific testable outcome]
- [ ] [Specific testable outcome]

### Task Level
**Task 1.1**: [Concrete implementation task]  
**Estimate**: [2-4 hours]  
**Description**: [Specific work to be done]  
**Dependencies**: [Prerequisites]

**Task 1.2**: [Another implementation task]  
**Estimate**: [1-3 hours]  
**Description**: [Specific work to be done]  
**Dependencies**: [Prerequisites]

## 🔗 Dependencies

### Technical Dependencies
- [ ] **[Dependency Name]**: [Description and current status]
- [ ] **[System/Component]**: [Why it's needed and availability]
- [ ] **[Unity Package/Library]**: [Version and compatibility]

### Knowledge Dependencies
- [ ] **[Domain Knowledge Document]**: [Specific sections needed]
- [ ] **[Architecture Decision]**: [What needs to be decided]
- [ ] **[Expert Consultation]**: [Who needs to validate approach]

### Resource Dependencies
- [ ] **[Development Tool]**: [Unity version, packages, etc.]
- [ ] **[Testing Environment]**: [Specific setup requirements]
- [ ] **[Documentation]**: [What docs need to be created/updated]

## ⚠️ Risk Assessment

### High Risk Issues
**Risk**: [Specific potential problem]  
**Probability**: [High/Medium/Low]  
**Impact**: [Critical/High/Medium/Low]  
**Mitigation**: [How to prevent or handle this risk]  
**Contingency**: [Backup plan if risk materializes]

**Risk**: [Another potential problem]  
**Probability**: [High/Medium/Low]  
**Impact**: [Critical/High/Medium/Low]  
**Mitigation**: [Prevention strategy]  
**Contingency**: [Backup plan]

### Medium Risk Issues
**Risk**: [Less severe potential problem]  
**Mitigation**: [Prevention strategy]

## 🧪 Testing Strategy

### Unit Testing
- **Coverage Target**: [>80% for new code]
- **Key Test Cases**:
  - [ ] [Critical functionality test]
  - [ ] [Edge case test]
  - [ ] [Performance test]

### Integration Testing
- **ECS Integration**: [How components work together]
- **UI Integration**: [Bridge layer communication]
- **Performance Integration**: [System-wide performance impact]

### Validation Approach
- **Functional Validation**: [How to verify features work]
- **Performance Validation**: [Specific metrics and benchmarks]
- **Quality Validation**: [Code quality and architecture compliance]

## 📈 Performance Targets

### Entity Scale Targets
- **Minimum**: [X entities at Y fps]
- **Target**: [X entities at Y fps]
- **Maximum**: [X entities at Y fps with degradation]

### Memory Targets
- **Component Memory**: [X MB for Y entities]
- **System Memory**: [X MB overhead]
- **Native Collections**: [Specific allocator strategy]

### Frame Time Targets
- **Target Frame Time**: [X ms per system update]
- **Critical Path**: [Most performance-sensitive operations]
- **Fallback Strategy**: [LOD or reduced functionality plan]

## 📋 Implementation Sequence

### Phase 1: Foundation ([X hours])
1. [First foundational task]
2. [Second foundational task]  
3. [Basic structure setup]

**Checkpoint**: [What should be working after Phase 1]

### Phase 2: Core Functionality ([X hours])
1. [Main feature implementation]
2. [Core system integration]
3. [Basic testing and validation]

**Checkpoint**: [What should be working after Phase 2]

### Phase 3: Integration & Polish ([X hours])
1. [System integration]
2. [Performance optimization]
3. [Final testing and validation]

**Completion**: [Full feature working with all acceptance criteria met]

## 📚 Related Documentation

### Required Reading
- [DOMAIN_KNOWLEDGE.md](../reference/DOMAIN_KNOWLEDGE.md) - Unity ECS patterns
- [DEVELOPMENT_WORKFLOW.md](../reference/DEVELOPMENT_WORKFLOW.md) - Development standards
- [Architecture Document] - Relevant system architecture

### Reference Materials
- [Game Design Document] - Business logic and requirements
- [Performance Benchmarks] - Current system performance baselines
- [Code Examples] - Similar implementations for reference

### Documentation Updates Required
- [ ] [Architecture document to update]
- [ ] [API documentation to create/update]
- [ ] [User guide sections to update]

## 🎯 Definition of Done

### Functional Completion
- [ ] All acceptance criteria met and validated
- [ ] All planned tasks completed successfully
- [ ] Integration testing passed
- [ ] No critical bugs or issues remaining

### Quality Gates
- [ ] Code review completed and approved
- [ ] Performance targets met or exceeded
- [ ] Architecture compliance validated
- [ ] Test coverage >80% for new code

### Documentation
- [ ] All relevant documentation updated
- [ ] API documentation current and accurate
- [ ] Implementation decisions documented
- [ ] Known issues and limitations documented

### Integration
- [ ] System integrates cleanly with existing codebase
- [ ] No regressions in existing functionality
- [ ] Performance impact within acceptable limits
- [ ] UI integration working correctly (if applicable)

---

## 📝 Planning Session Notes

### Consultation Session ([Date])
**Participants**: [Who was involved in planning]  
**Duration**: [Actual time spent planning]

### Key Decisions Made
- **[Decision 1]**: [What was decided and why]
- **[Decision 2]**: [What was decided and why]

### Alternative Approaches Considered
- **[Alternative 1]**: [Why it was rejected]
- **[Alternative 2]**: [Why it was rejected]

### Open Questions Resolved
- **[Question 1]**: [Resolution]
- **[Question 2]**: [Resolution]

---

## 📈 Progress Tracking

### Session Log References
- [SESSION_LOG_[date]_[id].md] - [Brief description]
- [SESSION_LOG_[date]_[id].md] - [Brief description]

### Checkpoint References  
- [CHECKPOINT_[timestamp].md] - [Major milestone]
- [CHECKPOINT_[timestamp].md] - [Major milestone]

### Actual vs. Estimated Time
**Planned**: [X hours/days]  
**Actual**: [Y hours/days]  
**Variance**: [±Z% - analysis of difference]

---

**Template Version**: 1.0  
**Last Updated**: 2025-09-13  
**Next Review**: [When to review this template for improvements]