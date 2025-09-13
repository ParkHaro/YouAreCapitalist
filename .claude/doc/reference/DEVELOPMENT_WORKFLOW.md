---
category: reference
tags: [workflow, guidelines, development, best-practices, mandatory]
related: [DOMAIN_KNOWLEDGE.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: critical
---

# Development Workflow Guidelines

[🇰🇷 한국어 버전](./DEVELOPMENT_WORKFLOW_KOR.md)

## 📍 Navigation

[↩️ Back to Reference](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## 🚨 MANDATORY WORKFLOW

**This workflow MUST be followed for all development tasks involving code changes.**

## 1. Pre-Development Phase

### 1.0 Work Planning Protocol (MANDATORY)
**ALL development work MUST begin with planning consultation:**

```yaml
Planning Requirement:
  Protocol: Follow WORK_PLANNING_PROTOCOL.md exactly
  Duration: 15-20 minutes minimum consultation
  Trigger: ANY coding task, regardless of perceived complexity
  Exception: NONE - all work requires planning

Planning Steps:
  1. Document Guidance (5 minutes):
     - Verify domain knowledge reading
     - Identify missing documentation
     - Assess architecture requirements
  
  2. Requirement Gathering (10-15 minutes):
     - Interactive dialogue for scope clarification
     - Technical constraint identification
     - Success criteria definition
     - Risk assessment and mitigation planning
  
  3. Work Plan Creation:
     - Generate WORK_PLAN_[date]_[feature].md
     - Create structured TodoList via TodoWrite
     - Document technical approach and timeline
     - Establish checkpoints and validation criteria

Quality Gate: No coding begins until work plan is complete and approved.
```

### 1.1 Required Reading (MANDATORY)
**After planning consultation, you MUST read:**

```yaml
Step 1: Read Domain Knowledge
  File: .claude/doc/reference/DOMAIN_KNOWLEDGE.md
  Purpose: Understand Unity ECS architecture and project constraints
  Time: 10-15 minutes
  Critical: Performance and architecture principles

Step 2: Review Related Architecture
  Files: 
    - .claude/doc/architecture/technical-architecture.md
    - .claude/doc/architecture/ecs-design.md
  Purpose: Understand system integration patterns
  Time: 5-10 minutes per document

Step 3: Check Game Design Context
  Files: 
    - .claude/doc/gamedesign/core-gameplay-loop.md
    - Related gameplay mechanics documents
  Purpose: Understand business logic and game rules
  Time: Variable based on task scope
```

### 1.2 Session Management Setup (MANDATORY)
**Before beginning implementation, establish session management:**

```yaml
Session Initialization:
  Reference: Follow WORK_SESSION_TRACKER.md protocol
  Session Type: Determine based on estimated duration and complexity
  Checkpoint Schedule: Set intervals based on work complexity
  
Session Types:
  Single-Task (30min-2h): Basic TodoList + final summary
  Multi-Task (2-8h): Detailed checkpoints every 2 hours  
  Project (days/weeks): Daily summaries + weekly planning
  Investigation (variable): Evidence collection + findings

Checkpoint Protocol:
  Reference: Follow CHECKPOINT_PROTOCOL.md exactly
  Micro Checkpoints: Every 30 minutes (lightweight state)
  Standard Checkpoints: Every 2 hours (comprehensive context)
  Major Checkpoints: Task completion (achievement validation)
  Emergency Checkpoints: On-demand (unexpected interruption)

Quality Gate: Session management established before coding begins.
```

### 1.3 Task Analysis Framework
```python
# Use this mental framework before coding:
def analyze_task(task_description):
    analysis = {
        'data_scale': 'How many entities will this affect?',
        'performance_critical': 'Is this in the hot path?',
        'ecs_vs_mono': 'Should this use ECS or MonoBehaviour?',
        'ui_integration': 'Does this need UI communication?',
        'automation_impact': 'How does this affect game automation?'
    }
    
    # Decision matrix:
    if analysis['data_scale'] > 1000:
        use_ecs = True
        use_job_system = True
        use_burst = True
    
    if analysis['performance_critical']:
        optimize_for_cache = True
        use_native_collections = True
    
    return analysis
```

## 2. Development Standards

### 2.1 Code Organization Rules

#### ✅ ECS Code Structure
```csharp
// File: Assets/Scripts/ECS/Systems/Economic/PopulationConsumptionSystem.cs
[UpdateInGroup(typeof(EconomicSimulationGroup))]
public class PopulationConsumptionSystem : SystemBase
{
    protected override void OnUpdate()
    {
        // Job-based implementation required for >1000 entities
        var job = new ConsumptionJob { /* ... */ };
        Dependency = job.ScheduleParallel(Dependency);
    }
}

// File: Assets/Scripts/ECS/Jobs/PopulationJobs.cs
[BurstCompile]
public struct ConsumptionJob : IJobEntityBatch
{
    // Burst-compiled for performance
}

// File: Assets/Scripts/ECS/Components/Economic/PopulationData.cs
public struct PopulationData : IComponentData
{
    // Pure data only - no methods
}
```

#### ✅ UI Code Structure
```csharp
// File: Assets/Scripts/UI/Controllers/MarketChartController.cs
public class MarketChartController : MonoBehaviour
{
    // UI logic only - no simulation data processing
    private void UpdateChart(float[] marketData)
    {
        // Visualization logic
    }
}

// File: Assets/Scripts/UI/Bridges/MarketDataBridge.cs
public class MarketDataBridge : MonoBehaviour
{
    // ECS ↔ UI communication
    private EntityQuery marketQuery;
    public event Action<MarketData> OnMarketDataUpdated;
}
```

### 2.2 Performance Requirements

#### Mandatory Performance Checks
```csharp
// Include performance validation in all ECS systems:
public class YourEconomicSystem : SystemBase
{
    protected override void OnUpdate()
    {
        #if UNITY_EDITOR
        using var marker = new ProfilerMarker("YourSystem.Update").Auto();
        #endif
        
        // Your implementation
        var job = new YourJob();
        Dependency = job.ScheduleParallel(Dependency);
        
        #if UNITY_EDITOR
        // Validate entity count doesn't exceed targets
        var entityCount = m_EntityQuery.CalculateEntityCount();
        if (entityCount > 10000)
        {
            Debug.LogWarning($"High entity count in {nameof(YourEconomicSystem)}: {entityCount}");
        }
        #endif
    }
}
```

#### Memory Management Checklist
```csharp
public class EconomicDataSystem : SystemBase
{
    private NativeHashMap<Entity, float> dataMap;
    
    protected override void OnCreate()
    {
        // ✅ Always specify capacity for known sizes
        dataMap = new NativeHashMap<Entity, float>(10000, Allocator.Persistent);
    }
    
    protected override void OnDestroy()
    {
        // ✅ MANDATORY: Dispose all native collections
        if (dataMap.IsCreated) 
            dataMap.Dispose();
    }
    
    protected override void OnUpdate()
    {
        // ✅ Use TempJob allocator for temporary data
        var tempArray = new NativeArray<float>(100, Allocator.TempJob);
        
        // Process data...
        
        // ✅ Dispose temp allocations
        tempArray.Dispose();
    }
}
```

## 3. Code Review Process

### 3.1 Self-Review Checklist
Before submitting any code, verify:

#### ECS Implementation
- [ ] **Uses pure data components** (no methods in IComponentData)
- [ ] **Job System integration** for >1000 entities
- [ ] **Burst compilation** for performance-critical paths
- [ ] **Proper system group attribution** ([UpdateInGroup])
- [ ] **Native collection disposal** in OnDestroy
- [ ] **No managed references** in components
- [ ] **Chunk-based processing** where applicable

#### Performance Validation
- [ ] **Profiler markers** added for timing
- [ ] **Entity count warnings** for scale validation  
- [ ] **Memory allocation** patterns reviewed
- [ ] **Cache-friendly** data access patterns
- [ ] **No Update() loops** for ECS data access

#### Architecture Compliance
- [ ] **Three-layer separation** maintained (ECS/Bridge/UI)
- [ ] **Event-based UI communication** (no direct ECS access from UI)
- [ ] **ScriptableObject configuration** for game data
- [ ] **Consistent naming conventions** (EconomicSystem, PopulationJob, etc.)

### 3.2 Architecture Validation
```csharp
// Use this pattern to validate architecture compliance:

// ❌ WRONG: UI directly accessing ECS
public class BadUIController : MonoBehaviour
{
    void Update()
    {
        var world = World.DefaultGameObjectInjectionWorld;
        var entities = world.EntityManager.GetAllEntities(); // NEVER DO THIS
    }
}

// ✅ CORRECT: Event-based bridge pattern
public class EconomicUIController : MonoBehaviour
{
    [SerializeField] private MarketDataBridge dataBridge;
    
    void Start()
    {
        dataBridge.OnMarketDataUpdated += UpdateMarketUI;
    }
    
    private void UpdateMarketUI(MarketData data)
    {
        // UI update logic only
    }
}
```

## 4. Testing Requirements

### 4.1 Mandatory Tests

#### Performance Tests
```csharp
// Required for all ECS systems processing >1000 entities
[Test]
public void PopulationSystem_HandlesLargeScale_WithinFrameTarget()
{
    // Arrange: Create 100,000 population entities
    var entities = CreatePopulationEntities(100000);
    
    // Act: Run system update
    var stopwatch = Stopwatch.StartNew();
    World.GetOrCreateSystem<PopulationConsumptionSystem>().Update();
    stopwatch.Stop();
    
    // Assert: Should complete within 16ms (60fps target)
    Assert.That(stopwatch.ElapsedMilliseconds, Is.LessThan(16));
}
```

#### Memory Tests
```csharp
[Test]
public void EconomicSystem_DoesNotLeakMemory_AfterManyUpdates()
{
    // Measure memory before
    var initialMemory = GC.GetTotalMemory(true);
    
    // Run many updates
    for (int i = 0; i < 1000; i++)
    {
        system.Update();
    }
    
    // Force cleanup and measure
    GC.Collect();
    var finalMemory = GC.GetTotalMemory(true);
    
    // Should not have significant memory growth
    var memoryGrowth = finalMemory - initialMemory;
    Assert.That(memoryGrowth, Is.LessThan(1024 * 1024)); // <1MB growth
}
```

### 4.2 Integration Tests
```csharp
// Test ECS-UI bridge communication
[Test]
public void MarketDataBridge_UpdatesUI_WhenMarketChanges()
{
    // Arrange
    var bridge = CreateMarketDataBridge();
    var uiUpdated = false;
    bridge.OnMarketDataUpdated += _ => uiUpdated = true;
    
    // Act: Simulate market data change in ECS
    CreateMarketEntity(initialPrice: 100f);
    UpdateMarketPrice(newPrice: 150f);
    bridge.UpdateFromECS(); // Trigger bridge update
    
    // Assert
    Assert.IsTrue(uiUpdated, "UI should be notified of market changes");
}
```

## 5. Performance Monitoring

### 5.1 Continuous Performance Validation
```csharp
// Add to all economic systems:
public class MarketSimulationSystem : SystemBase
{
    private static readonly ProfilerMarker s_UpdateMarker = 
        new ProfilerMarker("MarketSimulation.Update");
    
    private MovingAverage frameTimeAverage = new MovingAverage(60);
    
    protected override void OnUpdate()
    {
        using (s_UpdateMarker.Auto())
        {
            var startTime = Time.realtimeSinceStartup;
            
            // Your system logic here
            var job = new MarketCalculationJob();
            Dependency = job.ScheduleParallel(Dependency);
            
            // Track performance
            var frameTime = Time.realtimeSinceStartup - startTime;
            frameTimeAverage.Add(frameTime * 1000f); // Convert to ms
            
            #if UNITY_EDITOR
            // Alert if performance degrades
            if (frameTimeAverage.Average > 5.0f) // 5ms warning threshold
            {
                Debug.LogWarning($"{GetType().Name} average frame time: {frameTimeAverage.Average:F2}ms");
            }
            #endif
        }
    }
}
```

### 5.2 Automated Performance Alerts
```csharp
// Include in performance-critical systems:
public static class PerformanceValidator
{
    private static readonly Dictionary<Type, float> SystemThresholds = new()
    {
        { typeof(PopulationBehaviorSystem), 8.0f },    // 8ms max
        { typeof(MarketSimulationSystem), 5.0f },      // 5ms max
        { typeof(CompanyOperationsSystem), 6.0f }      // 6ms max
    };
    
    public static void ValidateSystemPerformance(Type systemType, float frameTimeMs)
    {
        if (SystemThresholds.TryGetValue(systemType, out float threshold))
        {
            if (frameTimeMs > threshold)
            {
                Debug.LogError($"PERFORMANCE VIOLATION: {systemType.Name} took {frameTimeMs:F2}ms (threshold: {threshold}ms)");
                
                #if UNITY_EDITOR
                // Pause in editor for investigation
                UnityEditor.EditorApplication.isPaused = true;
                #endif
            }
        }
    }
}
```

## 6. Documentation Requirements

### 6.1 Code Documentation Standards
```csharp
/// <summary>
/// Calculates consumption patterns for population entities based on income and economic conditions.
/// Processes up to 100,000 entities per frame using Job System + Burst.
/// </summary>
/// <remarks>
/// Performance: Target 8ms frame time for 50,000 entities at 60fps.
/// Memory: Uses 2MB native arrays for chunk processing.
/// Dependencies: Requires EconomicData and PopulationClass components.
/// </remarks>
[UpdateInGroup(typeof(EconomicSimulationGroup))]
[UpdateAfter(typeof(IncomeCalculationSystem))]
public class PopulationConsumptionSystem : SystemBase
{
    /// <summary>
    /// Job struct for parallel consumption calculation.
    /// Burst-compiled for SIMD optimization.
    /// </summary>
    [BurstCompile]
    public struct ConsumptionJob : IJobEntityBatch
    {
        // Implementation...
    }
}
```

### 6.2 Performance Documentation
```csharp
// Include performance characteristics in system comments:
/*
 * PERFORMANCE PROFILE:
 * - Entity Scale: 10,000 - 100,000 entities
 * - Target Frame Time: 8ms (60fps)
 * - Memory Usage: ~2MB native arrays
 * - Parallelization: 8-way parallel job execution
 * - Cache Efficiency: Chunk-based processing for data locality
 * - Burst Optimization: Full SIMD vectorization
 * 
 * SCALING BEHAVIOR:
 * - Linear scaling with entity count
 * - Memory usage: 20 bytes per entity
 * - CPU scaling: Utilizes all available cores
 * 
 * DEPENDENCIES:
 * - Must run after: IncomeCalculationSystem
 * - Must run before: MarketDemandSystem
 * - Required Components: PopulationData, EconomicClass
 */
```

## 7. Emergency Procedures

### 7.1 Performance Regression Response
```yaml
If frame rate drops below 30fps:
  1. Check Unity Profiler immediately
  2. Identify bottleneck system
  3. Temporarily reduce entity count by 50%
  4. Enable LOD system fallback
  5. Report performance regression with profiler data

If memory usage exceeds 1.5GB:
  1. Check for native collection leaks
  2. Force garbage collection
  3. Enable memory profiling
  4. Identify allocation sources
  5. Implement immediate cleanup
```

### 7.2 Build Failure Protocol
```yaml
If build fails with ECS errors:
  1. Check for missing [BurstCompile] attributes
  2. Verify all native collections are disposed
  3. Validate system update group dependencies
  4. Check for managed references in IComponentData
  5. Review job dependencies and safety systems
```

---

## 🎯 Success Criteria

**Your implementation is ready when:**
- ✅ **Passes all performance tests** (entity scale + frame time)
- ✅ **No memory leaks** detected in profiler
- ✅ **Architecture compliance** validated (3-layer separation)
- ✅ **Documentation complete** (performance characteristics noted)
- ✅ **Integration tests pass** (ECS-UI communication works)

**Remember: This is a data processing game. Every line of code should be optimized for handling 100,000+ entities efficiently.**