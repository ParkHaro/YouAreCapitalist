---
category: reference
tags: [domain-knowledge, unity, ecs, capitalism-simulation, technical-guide]
related: [../architecture/technical-architecture.md, ../architecture/ecs-design.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: critical
---

# Domain Knowledge Reference - YouAreCapitalist

[🇰🇷 한국어 버전](./DOMAIN_KNOWLEDGE_KOR.md)

## 📍 Navigation

[↩️ Back to Reference](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## 🚨 MANDATORY READING

**⚠️ READ THIS BEFORE ANY CODING WORK ⚠️**

This document contains essential domain knowledge that must be understood before making any code changes to the YouAreCapitalist project. Failure to follow these guidelines may result in performance degradation or architectural inconsistencies.

## 1. Project Overview

### 1.1 Core Technology Stack
```yaml
Game Engine: Unity 6000.2.0f1
Architecture: Unity DOTS (Data-Oriented Technology Stack)
Primary Framework: ECS (Entity Component System)
Performance: Job System + Burst Compiler
Platform: Mobile/PC Cross-platform
Rendering: Universal Render Pipeline (URP)
Language: C# (.NET Standard 2.1)
```

### 1.2 Project Nature
- **NOT a visual game**: Primarily data processing and visualization
- **Simulation-heavy**: Processing 100,000+ economic entities
- **Performance-critical**: Real-time economic calculations
- **Data-driven**: Numbers, charts, statistics over graphics

## 2. Architecture Principles

### 2.1 Data-Oriented Design (DOD)
```csharp
// ✅ CORRECT: ECS Component (Pure Data)
public struct PopulationData : IComponentData
{
    public float income;
    public float consumptionRate;
    public EducationLevel education;
    public int age;
}

// ❌ WRONG: MonoBehaviour for simulation data
public class Population : MonoBehaviour
{
    public float income;  // Don't use MonoBehaviour for simulation
}
```

### 2.2 Three-Layer Architecture
```
┌─────────────────────────────────────────┐
│         UI Layer (MonoBehaviour)        │  ← Charts, dashboards, UI
│  - UGUI/UI Toolkit                      │
│  - Data visualization                   │
└─────────────────────────────────────────┘
                    ↕️
┌─────────────────────────────────────────┐
│      Bridge Layer (Event System)        │  ← Data synchronization
│  - ECS ↔ UI communication               │
└─────────────────────────────────────────┘
                    ↕️
┌─────────────────────────────────────────┐
│    ECS Layer (Pure Data Processing)     │  ← Game logic, calculations
│  - Economic simulation                  │
│  - Job System + Burst                   │
└─────────────────────────────────────────┘
```

### 2.3 Performance-First Mentality
- **Target**: 100,000+ entities at 60fps
- **Use ECS for**: Economic calculations, market simulation, population behavior
- **Use MonoBehaviour for**: UI, input handling, visual effects only
- **Always consider**: Memory layout, cache friendliness, parallel processing

## 3. ECS Implementation Guidelines

### 3.1 Component Design Patterns

#### ✅ Pure Data Components
```csharp
// Market participant data
public struct MarketParticipant : IComponentData
{
    public float netWorth;
    public float liquidCash;
    public Entity portfolio;  // Reference to portfolio entity
}

// Company financial data
public struct CompanyFinancials : IComponentData
{
    public float revenue;
    public float expenses;
    public float marketCap;
    public int employeeCount;
}
```

#### ✅ Shared Components for Grouping
```csharp
// Group entities by economic class
public struct EconomicClass : ISharedComponentData
{
    public ClassType type;  // LowerClass, MiddleClass, UpperClass
}

// Group companies by industry
public struct Industry : ISharedComponentData
{
    public IndustryType type;  // Technology, Finance, Manufacturing, etc.
}
```

#### ✅ Buffer Components for Collections
```csharp
// Stock holdings (dynamic array)
[InternalBufferCapacity(8)]
public struct StockHolding : IBufferElementData
{
    public Entity stockEntity;
    public int shares;
    public float averageCost;
}

// Transaction history
[InternalBufferCapacity(16)]
public struct TransactionHistory : IBufferElementData
{
    public TransactionType type;
    public float amount;
    public DateTime timestamp;
}
```

### 3.2 System Design Patterns

#### ✅ Job-Based Systems
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
public class PopulationConsumptionSystem : SystemBase
{
    protected override void OnUpdate()
    {
        // Burst-compiled parallel job
        var job = new ConsumptionCalculationJob
        {
            deltaTime = Time.DeltaTime,
            economicData = GetComponentDataFromEntity<EconomicData>(true)
        };
        
        Dependency = job.ScheduleParallel(Dependency);
    }
}

[BurstCompile]
public struct ConsumptionCalculationJob : IJobEntityBatch
{
    [ReadOnly] public float deltaTime;
    [ReadOnly] public ComponentDataFromEntity<EconomicData> economicData;
    
    public void Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
    {
        // High-performance bulk processing
        var populations = chunk.GetNativeArray(populationHandle);
        // ... SIMD-optimized calculations
    }
}
```

#### ✅ System Update Groups
```csharp
// Define execution order
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateBefore(typeof(MarketSystemGroup))]
public class PopulationSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(PopulationSystemGroup))]
public class MarketSystemGroup : ComponentSystemGroup { }
```

### 3.3 Data Management Patterns

#### ✅ Native Collections for Performance
```csharp
public class MarketDataSystem : SystemBase
{
    private NativeHashMap<Entity, float> stockPrices;
    private NativeArray<float> marketIndices;
    
    protected override void OnCreate()
    {
        stockPrices = new NativeHashMap<Entity, float>(10000, Allocator.Persistent);
        marketIndices = new NativeArray<float>(100, Allocator.Persistent);
    }
    
    protected override void OnDestroy()
    {
        if (stockPrices.IsCreated) stockPrices.Dispose();
        if (marketIndices.IsCreated) marketIndices.Dispose();
    }
}
```

## 4. Game-Specific Domain Logic

### 4.1 Economic Simulation Core
```csharp
// Core economic entities
public enum EntityTypes
{
    Population,     // Individual economic actors (Pops)
    Company,        // Business entities
    Stock,          // Tradeable securities
    Market,         // Market segments
    Government,     // Policy makers
    Bank           // Financial institutions
}

// Simulation time scales
public enum TimeScale
{
    Paused = 0,
    Normal = 1,      // 1x real-time
    Fast = 10,       // 10x acceleration
    VeryFast = 100,  // 100x acceleration
    Ultra = 1000     // 1000x ultra-fast
}
```

### 4.2 Market Mechanics
```csharp
// Stock market simulation
public struct StockData : IComponentData
{
    public float currentPrice;
    public float previousPrice;
    public float marketCap;
    public int totalShares;
    public float dividendYield;
    public float peRatio;
}

// Market events
public struct MarketEvent : IComponentData
{
    public EventType type;    // Earnings, Merger, Scandal, etc.
    public float impact;      // Price impact multiplier
    public DateTime expiry;   // When event expires
}
```

### 4.3 Automation System
```csharp
// Player automation levels
public enum AutomationLevel
{
    Manual = 0,        // Full player control
    Assisted = 1,      // AI recommendations
    SemiAuto = 2,      // AI executes with approval
    FullAuto = 3       // Complete AI control
}

// AI decision making
public struct AIDecision : IComponentData
{
    public DecisionType type;
    public float confidence;
    public Entity targetEntity;
    public bool requiresApproval;
}
```

## 5. Performance Optimization Guidelines

### 5.1 Entity Management
```csharp
// ✅ Entity pooling for performance
public class EntityPool : SystemBase
{
    private NativeQueue<Entity> pooledPopulation;
    private NativeQueue<Entity> pooledCompanies;
    
    public Entity GetPooledPopulation()
    {
        if (pooledPopulation.Count > 0)
            return pooledPopulation.Dequeue();
        
        return EntityManager.CreateEntity(populationArchetype);
    }
}
```

### 5.2 LOD (Level of Detail) System
```csharp
// Dynamic quality scaling
public enum SimulationLOD
{
    Ultra,    // Individual entity simulation
    High,     // Important entities individual, others grouped
    Medium,   // Most entities grouped
    Low       // Statistical approximation
}

// Performance-based LOD adjustment
public class PerformanceManager : SystemBase
{
    private float targetFrameTime = 16.67f; // 60fps
    
    protected override void OnUpdate()
    {
        if (Time.unscaledDeltaTime > targetFrameTime * 1.2f)
            ReduceLOD();
        else if (Time.unscaledDeltaTime < targetFrameTime * 0.8f)
            IncreaseLOD();
    }
}
```

### 5.3 Memory Management
```csharp
// Chunk-based processing for cache efficiency
[BurstCompile]
public struct OptimizedMarketJob : IJobEntityBatch
{
    public void Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
    {
        // Process entire chunks for memory locality
        var prices = chunk.GetNativeArray(priceHandle);
        var volumes = chunk.GetNativeArray(volumeHandle);
        
        // Vectorized operations for SIMD
        for (int i = 0; i < chunk.Count; i++)
        {
            // Bulk calculations
        }
    }
}
```

## 6. UI Integration Patterns

### 6.1 ECS-UI Bridge
```csharp
// Event-based communication
public class MarketDataBridge : MonoBehaviour
{
    public event System.Action<float[]> OnStockPricesUpdated;
    
    private EntityQuery stockQuery;
    
    void Start()
    {
        var world = World.DefaultGameObjectInjectionWorld;
        stockQuery = world.EntityManager.CreateEntityQuery(typeof(StockData));
    }
    
    void Update()
    {
        // Poll ECS data and broadcast to UI
        var stockData = stockQuery.ToComponentDataArray<StockData>(Allocator.TempJob);
        var prices = ExtractPrices(stockData);
        OnStockPricesUpdated?.Invoke(prices);
        stockData.Dispose();
    }
}
```

### 6.2 Data Visualization
```csharp
// Chart data preparation
public class EconomicChartController : MonoBehaviour
{
    [SerializeField] private LineChart gdpChart;
    [SerializeField] private BarChart sectorChart;
    
    private void UpdateGDPChart(float[] gdpData)
    {
        // Convert ECS data to chart format
        var chartData = new List<Vector2>();
        for (int i = 0; i < gdpData.Length; i++)
        {
            chartData.Add(new Vector2(i, gdpData[i]));
        }
        gdpChart.UpdateData(chartData);
    }
}
```

## 7. Common Pitfalls & Anti-Patterns

### 7.1 ❌ What NOT to Do
```csharp
// ❌ Don't use MonoBehaviour for simulation data
public class PopulationMonoBehaviour : MonoBehaviour
{
    public float income; // This breaks ECS performance
}

// ❌ Don't access ECS from Update loops
public class BadUIController : MonoBehaviour
{
    void Update()
    {
        // This is expensive every frame!
        var entities = World.DefaultGameObjectInjectionWorld.EntityManager
                           .GetAllEntities();
    }
}

// ❌ Don't use Managed components for performance data
public class ManagedData : IComponentData
{
    public List<float> expensiveList; // Managed memory!
}
```

### 7.2 ✅ Correct Alternatives
```csharp
// ✅ Use ECS components for simulation
public struct PopulationECS : IComponentData
{
    public float income;
    public float consumption;
}

// ✅ Cache UI queries and update periodically
public class GoodUIController : MonoBehaviour
{
    private float updateInterval = 0.1f; // 10fps UI updates
    private float lastUpdate;
    
    void Update()
    {
        if (Time.time - lastUpdate >= updateInterval)
        {
            UpdateUI();
            lastUpdate = Time.time;
        }
    }
}

// ✅ Use NativeCollections for performance
public struct OptimizedData : IComponentData
{
    public BlobAssetReference<BlobArray<float>> efficientArray;
}
```

## 8. Development Workflow

### 8.1 Before Starting Any Task
1. **Read this document completely**
2. **Review related architecture documents**
3. **Check existing ECS patterns in the project**
4. **Understand performance implications**
5. **Plan ECS vs MonoBehaviour separation**

### 8.2 Code Review Checklist
- [ ] Uses ECS for simulation data?
- [ ] Follows three-layer architecture?
- [ ] Implements Job System where appropriate?
- [ ] Uses Burst compilation for performance?
- [ ] Properly manages Native Collections?
- [ ] Separates UI from simulation logic?
- [ ] Considers memory layout and cache efficiency?

### 8.3 Testing Approach
- **Unit Tests**: Individual system logic
- **Performance Tests**: Frame time and memory usage
- **Scale Tests**: 100K+ entity scenarios
- **Integration Tests**: ECS-UI communication

## 9. Key References

### 9.1 Essential Documents
- [Technical Architecture](../architecture/technical-architecture.md) - Overall system design
- [ECS System Design](../architecture/ecs-design.md) - ECS implementation details
- [Simulation System](../architecture/simulation-system.md) - Economic simulation logic

### 9.2 Unity DOTS Resources
- [Unity DOTS Official Documentation](https://docs.unity3d.com/Packages/com.unity.entities@latest)
- [Job System Guide](https://docs.unity3d.com/Manual/JobSystem.html)
- [Burst Compiler](https://docs.unity3d.com/Packages/com.unity.burst@latest)

---

## 🎯 Remember

**This is a DATA PROCESSING game, not a graphics game. Every decision should prioritize:**
1. **Data throughput** over visual fidelity
2. **Simulation accuracy** over graphical effects  
3. **Performance scalability** over feature complexity
4. **ECS patterns** over traditional MonoBehaviour approaches

**When in doubt, choose the solution that can handle 100,000+ entities efficiently.**