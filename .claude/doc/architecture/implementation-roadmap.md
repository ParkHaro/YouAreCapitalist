---
category: architecture
tags: [implementation, roadmap, development, phases, milestone]
related: [simulation-system.md, entity-generation.md, ecs-design.md]
parent: INDEX.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# Implementation Roadmap

[🇰🇷 Korean Version](./implementation-roadmap_KOR.md)

## 📍 Navigation

[↩️ Back to Architecture](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Development Overview

### 1.1 Implementation Strategy

#### Incremental Development Approach
- **MVP First**: Get basic simulation running as quickly as possible
- **Iterative Enhancement**: Add complexity in manageable chunks
- **Data-Driven Design**: Focus on getting ECS data flowing correctly
- **Early Testing**: Validate each phase before moving forward

#### Target Timeline
- **Phase 1**: 1-2 weeks - Basic entity generation
- **Phase 2**: 2-3 weeks - Autonomous behavior systems  
- **Phase 3**: 2-3 weeks - Economic interactions
- **Phase 4**: 3-4 weeks - Advanced features and polish

### 1.2 Success Metrics

#### Phase 1 Success Criteria
- 1,000 Pops + 100 Companies successfully generated
- All entities have valid component data
- Basic UI showing entity counts and statistics

#### Final Success Criteria
- **"1000개 Pop + 100개 Company 자동 시뮬레이션"**
- Entities make autonomous decisions
- Basic economic cycles functioning (employment, consumption, production)
- Real-time statistics and monitoring working

## 2. Phase 1: Foundation Setup

### 2.1 Unity Project Setup

#### Package Requirements
```json
{
  "dependencies": {
    "com.unity.entities": "1.0.16",
    "com.unity.entities.graphics": "1.0.16", 
    "com.unity.jobs": "0.70.0",
    "com.unity.collections": "2.2.1",
    "com.unity.mathematics": "1.2.6",
    "com.unity.burst": "1.8.12",
    "com.unity.ui.toolkit": "1.0.0-preview.11"
  }
}
```

#### Project Structure Setup
```
Assets/
├── Scripts/
│   ├── Components/
│   │   ├── PopulationComponents.cs
│   │   ├── CompanyComponents.cs
│   │   └── MarketComponents.cs
│   ├── Systems/
│   │   ├── Generation/
│   │   ├── Simulation/
│   │   └── Statistics/
│   ├── Configuration/
│   │   └── ScriptableObjects/
│   └── UI/
├── Data/
│   └── Configurations/
└── UI/
    └── Toolkit/
```

#### Implementation Checklist - Project Setup
- [ ] Install Unity DOTS packages
- [ ] Create folder structure
- [ ] Setup assembly definitions
- [ ] Create basic scene with ECS World
- [ ] Verify DOTS is working (create test entity)

### 2.2 Core Data Components

#### Essential Component Implementation
```csharp
// File: Assets/Scripts/Components/PopulationComponents.cs
using Unity.Entities;
using Unity.Mathematics;

// Basic population identity
public struct PopulationComponent : IComponentData
{
    public int populationID;
    public PopulationClass socialClass;
    public float age;
    public EmploymentStatus employment;
}

// Economic status and resources  
public struct EconomicStatusComponent : IComponentData
{
    public float monthlyIncome;
    public float totalWealth;
    public float savingsRate;
    public float consumptionRate;
    public float riskTolerance;
}

// Demographic information
public struct DemographicsComponent : IComponentData
{
    public Gender gender;
    public EducationLevel education;
    public Region residence;
    public FamilyStatus familyStatus;
    public int dependents;
}

// Behavioral traits
public struct BehaviorComponent : IComponentData
{
    public float optimismLevel;      
    public float conformityLevel;    
    public float loyaltyLevel;       
    public float informationLevel;   
}

// Decision-making state
public struct PopulationDecisionComponent : IComponentData
{
    public DecisionType pendingDecision;
    public float decisionConfidence;
    public float decisionDeadline;
    public Entity targetEntity;
}
```

#### Implementation Checklist - Components
- [ ] Create PopulationComponents.cs with all structs
- [ ] Create CompanyComponents.cs with business entities
- [ ] Create MarketComponents.cs with market data
- [ ] Create ConfigurationComponents.cs for singletons
- [ ] Test components compile without errors

### 2.3 Configuration System

#### ScriptableObject Setup
```csharp
// File: Assets/Scripts/Configuration/EconomicConfiguration.cs
[CreateAssetMenu(fileName = "EconomicConfig", menuName = "Capitalism/Economic Configuration")]
public class EconomicConfiguration : ScriptableObject
{
    [Header("Population Generation")]
    public int initialPopulationCount = 1000;
    public AnimationCurve ageDistribution;
    public AnimationCurve incomeDistribution;
    public float genderRatio = 0.5f;
    
    [Header("Company Generation")]
    public int initialCompanyCount = 100;
    public IndustryDistribution[] industryDistributions;
    
    [Header("Simulation Parameters")]
    public float timeScale = 1.0f;
    public float economicUpdateRate = 1.0f; // Updates per second
}

[System.Serializable]
public struct IndustryDistribution
{
    public IndustryType industry;
    public float weight;
    public float averageRevenue;
}
```

#### Implementation Checklist - Configuration
- [ ] Create EconomicConfiguration ScriptableObject
- [ ] Create default configuration asset
- [ ] Add configuration curves (age, income distribution)
- [ ] Create configuration singleton component
- [ ] Test configuration loading in game

### 2.4 Basic Entity Generation

#### Population Spawn System
```csharp
// File: Assets/Scripts/Systems/Generation/PopulationSpawnSystem.cs
public partial struct PopulationSpawnSystem : ISystem
{
    private Unity.Mathematics.Random random;
    private bool hasSpawnedInitial;
    
    public void OnCreate(ref SystemState state)
    {
        random = Unity.Mathematics.Random.CreateFromIndex((uint)System.DateTime.Now.Millisecond);
        hasSpawnedInitial = false;
    }
    
    public void OnUpdate(ref SystemState state)
    {
        if (!hasSpawnedInitial)
        {
            SpawnInitialPopulation(ref state);
            hasSpawnedInitial = true;
        }
    }
    
    private void SpawnInitialPopulation(ref SystemState state)
    {
        // Get singleton configuration
        if (!SystemAPI.TryGetSingleton<EconomicConfigurationData>(out var config))
            return;
            
        var commandBuffer = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                                   .CreateCommandBuffer(state.WorldUnmanaged);
        
        for (int i = 0; i < config.initialPopulationCount; i++)
        {
            Entity newPop = commandBuffer.CreateEntity();
            
            // Generate random demographics
            var demographics = GenerateRandomDemographics();
            var economics = GenerateRandomEconomics(demographics);
            var behavior = GenerateRandomBehavior();
            
            // Basic population data
            commandBuffer.AddComponent(newPop, new PopulationComponent 
            {
                populationID = i,
                socialClass = DetermineClass(economics.monthlyIncome),
                age = demographics.age,
                employment = DetermineEmployment(demographics)
            });
            
            commandBuffer.AddComponent(newPop, economics);
            commandBuffer.AddComponent(newPop, demographics);
            commandBuffer.AddComponent(newPop, behavior);
        }
    }
}
```

#### Implementation Checklist - Basic Generation
- [ ] Create PopulationSpawnSystem
- [ ] Implement basic random generation methods
- [ ] Create CompanySpawnSystem (similar pattern)
- [ ] Test entity generation (should create 1000 + 100 entities)
- [ ] Verify all components have valid data

### 2.5 Basic Statistics and UI

#### Statistics System
```csharp
// File: Assets/Scripts/Systems/Statistics/StatisticsSystem.cs
public partial struct StatisticsSystem : SystemBase
{
    protected override void OnUpdate()
    {
        // Count populations by class
        int totalPop = 0;
        int lowIncome = 0, middleClass = 0, highIncome = 0;
        
        Entities.ForEach((in PopulationComponent pop) => {
            totalPop++;
            switch(pop.socialClass)
            {
                case PopulationClass.LowIncome: lowIncome++; break;
                case PopulationClass.MiddleClass: middleClass++; break;
                case PopulationClass.HighIncome: highIncome++; break;
            }
        }).Run();
        
        // Count companies
        int totalCompanies = 0;
        Entities.ForEach((in CompanyComponent company) => {
            totalCompanies++;
        }).Run();
        
        // Update singleton statistics
        if (SystemAPI.TryGetSingleton<GameStatistics>(out var stats))
        {
            stats.totalPopulation = totalPop;
            stats.totalCompanies = totalCompanies;
            stats.lowIncomeCount = lowIncome;
            stats.middleClassCount = middleClass;
            stats.highIncomeCount = highIncome;
            
            SystemAPI.SetSingleton(stats);
        }
    }
}
```

#### Implementation Checklist - Statistics & UI
- [ ] Create StatisticsSystem for real-time counting
- [ ] Create GameStatistics singleton component
- [ ] Create basic UI using UI Toolkit
- [ ] Display: Total Population, Total Companies, Class breakdown
- [ ] Test statistics update in real-time

## 3. Phase 2: Autonomous Behavior

### 3.1 Basic Decision Systems

#### Population Decision Framework
```csharp
// File: Assets/Scripts/Systems/Simulation/PopulationBehaviorSystem.cs
public partial struct PopulationBehaviorSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (population, economic, decision) in 
                 SystemAPI.Query<PopulationComponent, EconomicStatusComponent, PopulationDecisionComponent>())
        {
            // Update decision deadline
            if (decision.decisionDeadline > 0)
            {
                decision.decisionDeadline -= deltaTime;
            }
            
            // Make new decision if needed
            if (decision.decisionDeadline <= 0)
            {
                decision.pendingDecision = ChooseRandomDecision(population, economic);
                decision.decisionConfidence = UnityEngine.Random.Range(0.5f, 1.0f);
                decision.decisionDeadline = UnityEngine.Random.Range(5f, 30f); // 5-30 seconds
            }
        }
    }
    
    private DecisionType ChooseRandomDecision(PopulationComponent pop, EconomicStatusComponent econ)
    {
        // Simple decision logic for Phase 2
        if (econ.monthlyIncome < 200f)
            return DecisionType.SeekJob;
        else if (econ.totalWealth > econ.monthlyIncome * 10f)
            return DecisionType.Invest;
        else
            return DecisionType.Consume;
    }
}
```

#### Implementation Checklist - Basic Behavior
- [ ] Create PopulationBehaviorSystem with simple decisions
- [ ] Create CompanyOperationSystem with basic business logic
- [ ] Add decision timers and random decision making
- [ ] Test that entities change their decisions over time
- [ ] Add decision logging for debugging

### 3.2 Employment System

#### Job Matching System
```csharp
// File: Assets/Scripts/Systems/Simulation/EmploymentSystem.cs
public partial struct EmploymentMatchingSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // Find unemployed population seeking jobs
        var jobSeekers = new NativeList<Entity>(Allocator.Temp);
        var jobOpenings = new NativeList<Entity>(Allocator.Temp);
        
        // Collect job seekers
        foreach (var (entity, pop, decision) in 
                 SystemAPI.Query<Entity, PopulationComponent, PopulationDecisionComponent>()
                         .WithAll<RefRO<PopulationComponent>>())
        {
            if (pop.employment == EmploymentStatus.Unemployed && 
                decision.pendingDecision == DecisionType.SeekJob)
            {
                jobSeekers.Add(entity);
            }
        }
        
        // Collect companies with job openings  
        foreach (var (entity, company, operation) in 
                 SystemAPI.Query<Entity, CompanyComponent, OperationComponent>())
        {
            if (operation.employeeCount < GetMaxEmployees(company))
            {
                jobOpenings.Add(entity);
            }
        }
        
        // Match job seekers with openings (simple random matching)
        int matches = math.min(jobSeekers.Length, jobOpenings.Length);
        for (int i = 0; i < matches; i++)
        {
            MatchEmployeeWithCompany(jobSeekers[i], jobOpenings[i], ref state);
        }
        
        jobSeekers.Dispose();
        jobOpenings.Dispose();
    }
}
```

#### Implementation Checklist - Employment System
- [ ] Create EmploymentMatchingSystem
- [ ] Implement basic job seeker identification
- [ ] Create company hiring logic
- [ ] Test unemployment rate changes over time
- [ ] Add employment statistics tracking

### 3.3 Basic Economic Interactions

#### Consumption System
```csharp
// File: Assets/Scripts/Systems/Simulation/ConsumptionSystem.cs
public partial struct ConsumptionSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (population, economic, decision) in 
                 SystemAPI.Query<RefRO<PopulationComponent>, RefRW<EconomicStatusComponent>, 
                                RefRO<PopulationDecisionComponent>>())
        {
            if (decision.ValueRO.pendingDecision == DecisionType.Consume)
            {
                // Simple consumption: spend money periodically
                float consumptionAmount = economic.ValueRO.monthlyIncome * 0.1f * deltaTime; // 10% per second
                economic.ValueRW.totalWealth = math.max(0, economic.ValueRO.totalWealth - consumptionAmount);
                
                // TODO: Find companies to spend money at
                // TODO: Update company revenue
            }
        }
    }
}
```

#### Implementation Checklist - Economic Interactions
- [ ] Create ConsumptionSystem for spending money
- [ ] Create basic company revenue from consumption
- [ ] Implement simple investment system
- [ ] Test money flow between pops and companies
- [ ] Add wealth distribution statistics

## 4. Phase 3: Market Dynamics

### 4.1 Supply and Demand

#### Market Price System
```csharp
// File: Assets/Scripts/Systems/Simulation/MarketDynamicsSystem.cs
public partial struct MarketDynamicsSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (market, dynamics) in 
                 SystemAPI.Query<RefRO<MarketComponent>, RefRW<MarketDynamicsComponent>>())
        {
            // Calculate supply (from companies in this industry)
            float totalSupply = CalculateIndustrySupply(market.ValueRO.industry);
            
            // Calculate demand (from population consumption)
            float totalDemand = CalculateIndustryDemand(market.ValueRO.industry);
            
            // Simple price discovery: price moves toward equilibrium
            float equilibriumPrice = totalDemand / totalSupply;
            float currentPrice = dynamics.ValueRO.currentPrice;
            float priceChange = (equilibriumPrice - currentPrice) * 0.1f; // 10% adjustment
            
            dynamics.ValueRW.currentPrice = math.max(0.1f, currentPrice + priceChange);
            dynamics.ValueRW.demandLevel = totalDemand;
            dynamics.ValueRW.supplyLevel = totalSupply;
        }
    }
}
```

#### Implementation Checklist - Market Dynamics
- [ ] Create MarketDynamicsSystem
- [ ] Implement supply/demand calculation
- [ ] Create price discovery mechanism
- [ ] Test market prices change over time
- [ ] Add market statistics and monitoring

### 4.2 Company Operations

#### Production and Revenue System
```csharp
// File: Assets/Scripts/Systems/Simulation/CompanyOperationSystem.cs
public partial struct CompanyOperationSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (company, financial, operation) in 
                 SystemAPI.Query<RefRO<CompanyComponent>, RefRW<FinancialComponent>, 
                                RefRO<OperationComponent>>())
        {
            // Simple production based on employees
            float productionCapacity = operation.ValueRO.employeeCount * operation.ValueRO.productivity;
            
            // Revenue from market demand
            float marketDemand = GetIndustryDemand(company.ValueRO.industry);
            float actualRevenue = math.min(productionCapacity, marketDemand) * deltaTime;
            
            // Operating costs (employee salaries, etc.)
            float operatingCosts = operation.ValueRO.employeeCount * 300f * deltaTime; // $300 per employee per day
            
            // Update financial state
            financial.ValueRW.revenue += actualRevenue;
            financial.ValueRW.operatingCost += operatingCosts;
            financial.ValueRW.netProfit = financial.ValueRO.revenue - financial.ValueRO.operatingCost;
            financial.ValueRW.cashFlow = financial.ValueRO.netProfit;
        }
    }
}
```

#### Implementation Checklist - Company Operations
- [ ] Create CompanyOperationSystem
- [ ] Implement production capacity calculation
- [ ] Create revenue generation from market demand
- [ ] Add operating cost calculation
- [ ] Test company profitability over time

## 5. Phase 4: Advanced Features

### 5.1 Random Events

#### Event System Framework
```csharp
// File: Assets/Scripts/Systems/Events/RandomEventSystem.cs
public partial struct RandomEventSystem : ISystem
{
    private Unity.Mathematics.Random random;
    private float eventTimer;
    
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        eventTimer -= deltaTime;
        
        if (eventTimer <= 0)
        {
            // Trigger random event
            if (random.NextFloat() < 0.1f) // 10% chance
            {
                TriggerRandomEvent(ref state);
            }
            
            eventTimer = 60f; // Check every minute
        }
    }
    
    private void TriggerRandomEvent(ref SystemState state)
    {
        EventType eventType = (EventType)random.NextInt(0, 5);
        
        switch(eventType)
        {
            case EventType.EconomicBoom:
                ApplyEconomicBoost();
                break;
            case EventType.Recession:
                ApplyEconomicRecession();  
                break;
            // ... other events
        }
    }
}
```

#### Implementation Checklist - Random Events
- [ ] Create RandomEventSystem
- [ ] Implement basic event types (boom, recession, etc.)
- [ ] Create event effect application
- [ ] Test events affect population and companies
- [ ] Add event notification UI

### 5.2 Advanced UI and Visualization

#### Real-time Dashboard
```csharp
// File: Assets/Scripts/UI/EconomicDashboard.cs
public class EconomicDashboard : MonoBehaviour
{
    [SerializeField] private Label populationLabel;
    [SerializeField] private Label companyLabel;
    [SerializeField] private Label unemploymentLabel;
    [SerializeField] private Label averageWealthLabel;
    
    void Update()
    {
        if (World.DefaultGameObjectInjectionWorld != null)
        {
            var statsSystem = World.DefaultGameObjectInjectionWorld.GetExistingSystemManaged<StatisticsSystem>();
            if (statsSystem != null && SystemAPI.TryGetSingleton<GameStatistics>(out var stats))
            {
                populationLabel.text = $"Population: {stats.totalPopulation}";
                companyLabel.text = $"Companies: {stats.totalCompanies}";
                unemploymentLabel.text = $"Unemployment: {stats.unemploymentRate:P1}";
                averageWealthLabel.text = $"Avg Wealth: ${stats.averageWealth:N0}";
            }
        }
    }
}
```

#### Implementation Checklist - Advanced UI
- [ ] Create comprehensive statistics dashboard
- [ ] Add real-time charts for economic indicators
- [ ] Create entity inspection panels
- [ ] Add simulation speed controls
- [ ] Implement save/load functionality

### 5.3 Performance Optimization

#### Job System Implementation
```csharp
// File: Assets/Scripts/Jobs/PopulationUpdateJob.cs
[BurstCompile]
public struct PopulationUpdateJob : IJobChunk
{
    public float deltaTime;
    
    [ReadOnly] public ComponentTypeHandle<PopulationComponent> PopulationHandle;
    public ComponentTypeHandle<EconomicStatusComponent> EconomicHandle;
    
    public void Execute(in ArchetypeChunk chunk, int unfilteredChunkIndex, 
                       bool useEnabledMask, in v128 chunkEnabledMask)
    {
        var populations = chunk.GetNativeArray(ref PopulationHandle);
        var economics = chunk.GetNativeArray(ref EconomicHandle);
        
        for (int i = 0; i < chunk.Count; i++)
        {
            var economic = economics[i];
            
            // Update wealth based on income
            economic.totalWealth += economic.monthlyIncome * (deltaTime / 30f); // Monthly income
            
            economics[i] = economic;
        }
    }
}
```

#### Implementation Checklist - Optimization
- [ ] Convert key systems to use Job System
- [ ] Add Burst compilation to performance-critical code
- [ ] Implement LOD system for distant entities
- [ ] Add performance profiling and monitoring
- [ ] Optimize memory allocations

## 6. Testing and Validation

### 6.1 Unit Tests

#### System Testing Framework
```csharp
// File: Assets/Scripts/Tests/PopulationSpawnTest.cs
[TestFixture]
public class PopulationSpawnSystemTests
{
    private World testWorld;
    private PopulationSpawnSystem spawnSystem;
    
    [SetUp]
    public void Setup()
    {
        testWorld = new World("TestWorld");
        spawnSystem = testWorld.GetOrCreateSystem<PopulationSpawnSystem>();
    }
    
    [Test]
    public void SpawnSystem_CreatesCorrectNumberOfEntities()
    {
        // Arrange
        var config = new EconomicConfigurationData { initialPopulationCount = 100 };
        testWorld.EntityManager.CreateSingleton(config);
        
        // Act
        spawnSystem.Update();
        
        // Assert
        var query = testWorld.EntityManager.CreateEntityQuery(typeof(PopulationComponent));
        Assert.AreEqual(100, query.CalculateEntityCount());
    }
}
```

### 6.2 Integration Testing

#### Full Simulation Test
```csharp
[Test]
public void FullSimulation_RunsFor60Seconds_WithoutErrors()
{
    // Setup complete simulation
    var world = CreateTestWorld();
    var systems = CreateAllSystems(world);
    
    // Run simulation for 60 seconds
    float totalTime = 0f;
    while (totalTime < 60f)
    {
        UpdateAllSystems(systems, 0.016f); // 60 FPS
        totalTime += 0.016f;
    }
    
    // Verify simulation state is valid
    AssertSimulationHealthy(world);
}
```

#### Implementation Checklist - Testing
- [ ] Create unit tests for all major systems
- [ ] Add integration tests for full simulation
- [ ] Create performance benchmarks
- [ ] Add automated validation for entity data
- [ ] Test simulation stability over time

## 7. Milestone Validation

### 7.1 Phase Completion Criteria

#### Phase 1 Complete When:
- [ ] 1000 Population entities generated with valid data
- [ ] 100 Company entities generated with valid data
- [ ] Basic UI shows correct entity counts
- [ ] All systems run without errors
- [ ] Performance: >30 FPS with all entities

#### Phase 2 Complete When:
- [ ] Entities make decisions every 5-30 seconds
- [ ] Employment system matches pops with companies
- [ ] Basic consumption reduces pop wealth
- [ ] Company revenue increases from consumption
- [ ] Unemployment rate fluctuates realistically (3-10%)

#### Phase 3 Complete When:
- [ ] Market prices change based on supply/demand
- [ ] Companies generate revenue from market demand
- [ ] Population consumption affects market prices
- [ ] Basic economic cycles visible (boom/bust periods)
- [ ] Economic statistics track meaningful changes

#### Phase 4 Complete When:
- [ ] Random events affect simulation meaningfully
- [ ] Advanced UI shows comprehensive statistics
- [ ] Performance optimized with Job System + Burst
- [ ] Save/load functionality working
- [ ] Full simulation runs stable for 10+ minutes

### 7.2 Final Success Metrics

#### **"1000개 Pop + 100개 Company 자동 시뮬레이션"** Achieved When:
- [ ] All entities operate autonomously without player input
- [ ] Economic interactions create realistic patterns
- [ ] Employment, consumption, production cycles functioning
- [ ] Statistics show meaningful economic indicators
- [ ] Simulation demonstrates emergent economic behavior
- [ ] Performance maintains >30 FPS throughout

## Next Steps

After completing this roadmap:
1. **Polish and Refinement** - Improve UI, add more event types, fine-tune parameters
2. **Player Interaction** - Add investment and policy influence mechanics  
3. **Advanced Economics** - Stock market, banking, government policy systems
4. **Scalability** - Support for 10,000+ entities with advanced optimization

## Related Documents

- [Simulation System](./simulation-system.md) - Complete system architecture
- [Entity Generation](./entity-generation.md) - Detailed generation algorithms
- [ECS Design](./ecs-design.md) - Core ECS patterns and practices