---
category: architecture
tags: [unity, ecs, dots, performance, capitalism-simulation]
related: [ecs-design.md, data-model.md, ui-system.md, integration-guide.md]
parent: INDEX.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# Capitalism Simulation Game - Technical Architecture

[🇰🇷 Korean Version](./technical-architecture_KOR.md)

## 📍 Navigation

[↩️ Back to Architecture](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. System Overview

### 1.1 Architecture Philosophy

#### Data-Oriented Design (DOD)
- **Core Principle**: Focus on data processing rather than rendering
- **Game Characteristics**: Numbers, charts, and statistical data are core, not visual objects
- **Performance Goal**: Real-time simulation of hundreds of thousands of economic entities

#### 3-Layer Architecture
```
┌─────────────────────────────────────────┐
│         UI Layer (MonoBehaviour)        │  ← Data visualization, user interaction
│  - UGUI/UI Toolkit                      │
│  - Charts, graphs, dashboards           │
│  - Event handling                       │
└─────────────────────────────────────────┘
                    ↕️ Events & Data
┌─────────────────────────────────────────┐
│      Bridge Layer (Event System)        │  ← Data synchronization, communication
│  - ECS ↔ UI data conversion             │
│  - Event broadcasting                   │
│  - State management                     │
└─────────────────────────────────────────┘
                    ↕️ Data Stream
┌─────────────────────────────────────────┐
│    ECS Layer (Pure Data Processing)     │  ← Game logic, computation engine
│  - Economic simulation                  │
│  - Job System parallel processing       │
│  - Burst Compiler optimization          │
└─────────────────────────────────────────┘
```

### 1.2 Technology Stack

#### Core Technologies
```yaml
Data Processing:
  - Unity DOTS (Data-Oriented Technology Stack)
  - ECS (Entity Component System)
  - Job System + Burst Compiler
  - Native Collections (NativeArray, NativeHashMap)

UI & Visualization:
  - UI Toolkit (Modern UI)
  - UGUI (Legacy support)
  - XCharts/Chart.js (Data visualization)
  - TextMeshPro (High-quality text)

Data Management:
  - ScriptableObject (Game configuration)
  - JSON (Save/Load)
  - SQLite (Historical data)
  - Binary Serialization (Performance optimization)

Platform:
  - Unity 6000.2.0f1+
  - .NET Standard 2.1
  - Universal Render Pipeline (URP)
  - Mobile/PC Cross-platform
```

### 1.3 Performance Goals and Constraints

#### Performance Targets
```yaml
Simulation Scale:
  - Economic entities: 100,000+ agents
  - Simulation speed: 1x~1000x variable
  - Frame rate: 60fps (1x), 30fps (100x+)
  - Memory usage: < 2GB (mobile compatible)

Processing Performance:
  - Pop simulation: 50,000/frame @60fps
  - Market calculation: Real-time price formation
  - Statistics aggregation: < 1ms/frame
  - UI updates: < 16ms/frame
```

#### Design Constraints
```yaml
Hardware Constraints:
  - Minimum spec: 4GB RAM, Quad-core CPU
  - Mobile support: Android API 24+, iOS 12+
  - Battery optimization: < 500mA power consumption

Software Constraints:
  - Unity 6000.2.0f1 compatibility
  - .NET Standard 2.1 limitations
  - URP 17.2.0 based rendering
```

## 2. Data Processing Pipeline

### 2.1 Simulation Loop Design

#### Game Time Management
```csharp
// Simulation time management
public class SimulationTimeManager : SystemBase
{
    public enum TimeScale
    {
        Paused = 0,
        Normal = 1,      // 1x real-time
        Fast = 10,       // 10x accelerated
        VeryFast = 100,  // 100x accelerated
        Ultra = 1000     // 1000x ultra-fast
    }
    
    private float gameTimePerSecond;
    private DateTime currentGameDate;
    private TimeScale currentScale;
}
```

#### Simulation Execution Order
```
1. Input Processing (User input)
   ↓
2. Economic Simulation (Economic simulation)
   ├── Population Behavior (Population behavior)
   ├── Company Operations (Company operations) 
   ├── Market Dynamics (Market dynamics)
   └── Government Policy (Government policy)
   ↓
3. Statistics Calculation (Statistics calculation)
   ├── Aggregate Statistics (Aggregate statistics)
   ├── Market Indices (Market indices)
   └── Economic Indicators (Economic indicators)
   ↓
4. Event Processing (Event processing)
   ├── Random Events (Random events)
   ├── Policy Changes (Policy changes)
   └── Market Shocks (Market shocks)
   ↓
5. UI Update (UI update)
```

### 2.2 Parallel Processing Strategy

#### Job System Utilization
```csharp
// Population behavior parallel processing
[BurstCompile]
public struct PopulationBehaviorJob : IJobEntityBatch
{
    [ReadOnly] public float deltaTime;
    [ReadOnly] public ComponentTypeHandle<PopulationData> populationHandle;
    public ComponentTypeHandle<EconomicActivity> activityHandle;
    
    public void Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
    {
        // Calculate economic activities of tens of thousands of Pops in parallel
        var populations = chunk.GetNativeArray(populationHandle);
        var activities = chunk.GetNativeArray(activityHandle);
        
        for (int i = 0; i < populations.Length; i++)
        {
            // SIMD optimized economic calculation
            CalculateConsumption(ref activities.ElementAt(i), populations[i]);
        }
    }
}
```

#### System Group Optimization
```csharp
// Simulation system groups
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(PopulationSystemGroup))]
public class MarketSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(MarketSystemGroup))]
public class StockMarketSystem : SystemBase { }

[UpdateInGroup(typeof(MarketSystemGroup))]
[UpdateAfter(typeof(StockMarketSystem))]
public class CommodityMarketSystem : SystemBase { }
```

### 2.3 Caching and Optimization

#### Multi-level Caching Strategy
```csharp
public class EconomicDataCache : SystemBase
{
    // Level 1: Frame cache (updated every frame)
    private NativeArray<float> frameGDPCache;
    
    // Level 2: Periodic cache (updated per second)
    private Dictionary<string, float> periodicCache;
    
    // Level 3: Long-term cache (updated per minute)
    private SQLiteDataCache longTermCache;
    
    protected override void OnUpdate()
    {
        // Selective updates based on cache level
        if (Time.frameCount % 60 == 0) // Every second
        {
            UpdatePeriodicCache();
        }
        
        if (Time.frameCount % 3600 == 0) // Every minute
        {
            UpdateLongTermCache();
        }
    }
}
```

#### LOD (Level of Detail) System
```csharp
// Simulation granularity control
public enum SimulationLOD
{
    Ultra,    // Individual simulation of all entities
    High,     // Individual for important entities, grouping for others
    Medium,   // Mostly group-based processing
    Low       // Statistical approximation
}

[BurstCompile]
public struct LODPopulationJob : IJob
{
    public SimulationLOD currentLOD;
    public NativeArray<PopulationData> populations;
    
    public void Execute()
    {
        switch (currentLOD)
        {
            case SimulationLOD.Ultra:
                ProcessIndividualBehavior();
                break;
            case SimulationLOD.High:
                ProcessGroupedBehavior();
                break;
            // ...
        }
    }
}
```

## 3. Scalability Considerations

### 3.1 Modular System Design

#### Plugin Architecture
```csharp
// Extensible system interface
public interface IEconomicModule
{
    string ModuleName { get; }
    Version Version { get; }
    void Initialize(World world);
    void Update(float deltaTime);
    void Shutdown();
}

// Module manager
public class EconomicModuleManager : MonoBehaviour
{
    private List<IEconomicModule> loadedModules;
    
    public void LoadModule(IEconomicModule module)
    {
        module.Initialize(World.DefaultGameObjectInjectionWorld);
        loadedModules.Add(module);
    }
}
```

#### Configuration-based System
```csharp
// ScriptableObject based configuration
[CreateAssetMenu(fileName = "EconomicSettings", menuName = "Game/Economic Settings")]
public class EconomicSettings : ScriptableObject
{
    [Header("Population Settings")]
    public int initialPopulation = 10000;
    public float baseConsumptionRate = 0.7f;
    
    [Header("Market Settings")]
    public float marketVolatility = 0.1f;
    public int numberOfCompanies = 1000;
    
    [Header("Performance Settings")]
    public SimulationLOD defaultLOD = SimulationLOD.High;
    public int maxEntitiesPerChunk = 128;
}
```

### 3.2 Performance Scaling Strategy

#### Dynamic LOD Adjustment
```csharp
public class PerformanceManager : SystemBase
{
    private float targetFrameTime = 16.67f; // 60fps
    private float currentFrameTime;
    private SimulationLOD currentLOD = SimulationLOD.High;
    
    protected override void OnUpdate()
    {
        currentFrameTime = Time.unscaledDeltaTime * 1000f;
        
        // Dynamic LOD adjustment based on performance
        if (currentFrameTime > targetFrameTime * 1.2f)
        {
            ReduceLOD();
        }
        else if (currentFrameTime < targetFrameTime * 0.8f)
        {
            IncreaseLOD();
        }
    }
}
```

#### Memory Pooling
```csharp
public class EntityPool : SystemBase
{
    private NativeQueue<Entity> pooledEntities;
    
    public Entity GetPooledEntity()
    {
        if (pooledEntities.Count > 0)
        {
            return pooledEntities.Dequeue();
        }
        
        return EntityManager.CreateEntity();
    }
    
    public void ReturnEntity(Entity entity)
    {
        // Initialize components and return to pool
        pooledEntities.Enqueue(entity);
    }
}
```

## 4. Development Tools and Debugging

### 4.1 Profiling Tools
```csharp
// Custom profiler markers
public static class EconomyProfiler
{
    public static readonly ProfilerMarker PopulationUpdate = 
        new ProfilerMarker("Economy.Population.Update");
    
    public static readonly ProfilerMarker MarketCalculation = 
        new ProfilerMarker("Economy.Market.Calculate");
}

// Usage example
using (EconomyProfiler.PopulationUpdate.Auto())
{
    // Population simulation code
}
```

### 4.2 Real-time Debug UI
```csharp
public class EconomyDebugUI : MonoBehaviour
{
    public bool showDebugInfo = false;
    
    void OnGUI()
    {
        if (!showDebugInfo) return;
        
        GUILayout.BeginArea(new Rect(10, 10, 300, 400));
        GUILayout.Label($"Active Entities: {GetEntityCount()}");
        GUILayout.Label($"Frame Time: {Time.deltaTime * 1000:F1}ms");
        GUILayout.Label($"Current LOD: {GetCurrentLOD()}");
        GUILayout.EndArea();
    }
}
```

## 5. Deployment and Operations

### 5.1 Platform-specific Optimization
```yaml
Mobile (Android/iOS):
  - Texture Compression: ASTC/ETC2
  - Audio Compression: Vorbis
  - Scripting Backend: IL2CPP
  - CPU Architecture: ARM64

Desktop (Windows/Mac/Linux):
  - Texture Compression: DXT/BC
  - Audio: Uncompressed
  - Scripting Backend: Mono/.NET
  - CPU Architecture: x64
```

### 5.2 Data Management
```csharp
// Save/Load system
public class SaveSystem : MonoBehaviour
{
    public void SaveGame(string filename)
    {
        var saveData = new GameSaveData
        {
            gameDate = TimeManager.CurrentDate,
            playerData = GetPlayerData(),
            economicState = GetEconomicState(),
            // Compressed entity data
            compressedEntities = CompressEntityData()
        };
        
        File.WriteAllText(filename, JsonUtility.ToJson(saveData));
    }
}
```

---

## Next Documents
- [ECS System Design](./ecs-design.md)
- [Data Model Specification](./data-model.md) 
- [UI System Design](./ui-system.md)
- [System Integration Guide](./integration-guide.md)