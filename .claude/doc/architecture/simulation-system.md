---
category: architecture
tags: [simulation, ecs, automation, dots, economics]
related: [ecs-design.md, data-model.md, entity-generation.md]
parent: INDEX.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# Simulation System Architecture

[🇰🇷 Korean Version](./simulation-system_KOR.md)

## 📍 Navigation

[↩️ Back to Architecture](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Simulation Overview

### 1.1 Core Philosophy

#### Self-Sustaining Economic Ecosystem
- **Autonomous Entities**: Populations and companies operate independently
- **Emergent Behavior**: Complex economic patterns emerge from simple rules
- **Real-time Dynamics**: Continuous simulation without player intervention
- **Scalable Architecture**: Support for thousands of entities simultaneously

#### Design Principles
```csharp
// Example: Population autonomous decision-making
public struct PopulationDecisionComponent : IComponentData
{
    public DecisionType pendingDecision;    // What they want to do
    public float decisionConfidence;        // How sure they are
    public float decisionDeadline;          // When they must decide
    public Entity targetEntity;             // What/who they're targeting
}
```

### 1.2 Simulation Scope

#### Economic Entities
- **Population (Pops)**: 1,000-10,000 individual economic actors
- **Companies**: 100-1,000 business entities
- **Markets**: Sector-specific economic spaces
- **Government**: Policy-making and regulation entity

#### Time Scale
- **Game Time**: 1 day = 10 seconds (adjustable)
- **Economic Cycles**: Monthly/quarterly/annual events
- **Update Frequency**: 60 FPS simulation, 1 FPS economic decisions

## 2. System Architecture

### 2.1 ECS System Hierarchy

#### Core Simulation Systems
```
SimulationSystemGroup (FixedStepSimulationSystemGroup)
├── InitializationPhase
│   ├── EntitySpawningSystemGroup
│   │   ├── PopulationSpawnSystem
│   │   ├── CompanySpawnSystem
│   │   └── MarketInitializationSystem
│   └── ConfigurationSystemGroup
├── EconomicSimulationPhase  
│   ├── PopulationSystemGroup
│   │   ├── PopulationBehaviorSystem
│   │   ├── ConsumptionDecisionSystem
│   │   ├── EmploymentSeekingSystem
│   │   └── InvestmentDecisionSystem
│   ├── CompanySystemGroup
│   │   ├── CompanyOperationSystem
│   │   ├── HiringDecisionSystem
│   │   ├── ProductionPlanningSystem
│   │   └── PricingStrategySystem
│   ├── MarketSystemGroup
│   │   ├── SupplyDemandSystem
│   │   ├── PriceDiscoverySystem
│   │   ├── TradingExecutionSystem
│   │   └── MarketClearingSystem
│   └── InteractionSystemGroup
│       ├── EmploymentMatchingSystem
│       ├── ConsumerCompanyTransactionSystem
│       └── B2BTransactionSystem
├── StatisticsPhase
│   ├── DataAggregationSystemGroup
│   │   ├── PopulationStatisticsSystem
│   │   ├── CompanyStatisticsSystem
│   │   └── MarketStatisticsSystem
│   └── HistoryTrackingSystem
└── EventSystemGroup
    ├── RandomEventGenerationSystem
    ├── CyclicalEventSystem (seasons, cycles)
    └── CrisisSimulationSystem
```

### 2.2 System Execution Order

#### Fixed Update Loop (60 FPS)
1. **Entity State Updates**: Health checks, aging, basic state transitions
2. **Market Price Updates**: Real-time price fluctuations
3. **Statistics Collection**: Real-time data aggregation

#### Economic Decision Loop (1-5 FPS)
1. **Decision Evaluation**: Entities evaluate their options
2. **Action Planning**: Queue intended actions
3. **Conflict Resolution**: Handle competing demands
4. **Action Execution**: Execute planned actions
5. **State Propagation**: Update affected entities

#### Event Loop (Variable)
1. **Scheduled Events**: Execute time-based events
2. **Random Events**: Generate and process random events
3. **Crisis Detection**: Monitor for economic crisis conditions

### 2.3 Data Flow Architecture

#### Information Flow
```
[Entity Internal State] 
    ↓ (Read)
[Decision Systems] 
    ↓ (Plan)
[Action Queue Systems] 
    ↓ (Execute)
[Market/Transaction Systems] 
    ↓ (Update)
[Statistics Systems] 
    ↓ (Aggregate)
[UI Bridge Layer] 
    ↓ (Display)
[Player Interface]
```

## 3. Autonomous Behavior Systems

### 3.1 Population Behavior System

#### Decision-Making Framework
```csharp
public struct PopulationDecisionSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // 1. Evaluate current needs and wants
        foreach (var (population, economic, decision) in 
                 SystemAPI.Query<PopulationComponent, EconomicStatusComponent, PopulationDecisionComponent>())
        {
            // 2. Generate possible actions based on personality and situation
            DecisionOption[] options = GenerateDecisionOptions(population, economic);
            
            // 3. Evaluate each option using utility function
            float bestUtility = float.MinValue;
            DecisionType bestDecision = DecisionType.DoNothing;
            
            foreach (var option in options)
            {
                float utility = CalculateUtility(option, population, economic);
                if (utility > bestUtility)
                {
                    bestUtility = utility;
                    bestDecision = option.decisionType;
                }
            }
            
            // 4. Queue decision for execution
            decision.pendingDecision = bestDecision;
            decision.decisionConfidence = bestUtility;
        }
    }
}
```

#### Behavioral Archetypes
```csharp
public enum PopulationArchetype : byte
{
    Conservative,    // Risk-averse, saves money, stable job
    Ambitious,      // Risk-taking, seeks growth, entrepreneur
    Hedonistic,     // Present-focused, high consumption
    Analytical,     // Data-driven decisions, rational
    Impulsive,      // Emotion-driven, inconsistent
    Conformist      // Follows crowd, trend-follower
}
```

### 3.2 Company Behavior System

#### Business Strategy Framework
```csharp
public struct CompanyStrategyComponent : IComponentData
{
    public BusinessStrategy primaryStrategy;
    public float aggressiveness;        // Risk tolerance (0.0 = conservative, 1.0 = aggressive)
    public float marketFocus;          // Market share vs profit focus
    public float innovationTendency;   // R&D investment tendency
    public float growthAmbition;       // Expansion vs consolidation
}

public enum BusinessStrategy : byte
{
    CostLeadership,     // Compete on price
    Differentiation,    // Compete on quality/features
    FocusNiche,        // Serve specific market segment
    Innovation,        // First-mover advantage
    FastFollower,      // Copy successful innovations
    Consolidation      // Acquire competitors
}
```

## 4. Performance Optimization

### 4.1 Job System Integration

#### Parallel Processing Strategy
```csharp
[BurstCompile]
public struct PopulationDecisionJob : IJobChunk
{
    public ComponentTypeHandle<PopulationComponent> PopulationHandle;
    public ComponentTypeHandle<EconomicStatusComponent> EconomicHandle;
    [ReadWrite] public ComponentTypeHandle<PopulationDecisionComponent> DecisionHandle;
    
    public void Execute(in ArchetypeChunk chunk, int unfilteredChunkIndex, 
                       bool useEnabledMask, in v128 chunkEnabledMask)
    {
        var populations = chunk.GetNativeArray(ref PopulationHandle);
        var economics = chunk.GetNativeArray(ref EconomicHandle);
        var decisions = chunk.GetNativeArray(ref DecisionHandle);
        
        for (int i = 0; i < chunk.Count; i++)
        {
            // Parallel decision calculation for each entity in chunk
            decisions[i] = CalculateOptimalDecision(populations[i], economics[i]);
        }
    }
}
```

### 4.2 Configuration System

#### Economic Configuration
```csharp
[CreateAssetMenu(fileName = "EconomicConfig", menuName = "Capitalism/Economic Configuration")]
public class EconomicConfiguration : ScriptableObject
{
    [Header("Population Settings")]
    public int initialPopulationCount = 1000;
    public AnimationCurve incomeDistribution;
    public float populationGrowthRate = 0.02f;
    
    [Header("Company Settings")]
    public int initialCompanyCount = 100;
    public AnimationCurve industryDistribution;
    public float companyBirthRate = 0.05f;
    public float companyDeathRate = 0.03f;
    
    [Header("Simulation Speed")]
    public float timeScale = 1.0f;
    public int economicUpdateFrequency = 1; // Updates per second
}
```

## 5. Implementation Phases

### Phase 1: Basic Entity Generation
- Population and company spawning
- Basic component initialization
- Simple random parameter assignment

### Phase 2: Autonomous Behavior
- Population decision-making system
- Company operation system
- Basic market interactions

### Phase 3: Economic Dynamics
- Supply and demand mechanics
- Employment system
- Market price discovery

### Phase 4: Advanced Features
- Random events
- Crisis simulation
- Player interaction systems

## Next Steps

1. **[Entity Generation System](./entity-generation.md)** - Random entity creation algorithms
2. **[Implementation Roadmap](./implementation-roadmap.md)** - Step-by-step development guide

## Related Documents

- [ECS Design](./ecs-design.md) - Core ECS architecture
- [Data Model](./data-model.md) - Component specifications
- [Technical Architecture](./technical-architecture.md) - Overall system design