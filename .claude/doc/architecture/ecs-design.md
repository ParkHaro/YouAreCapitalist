---
category: architecture
tags: [unity, ecs, dots, components, systems, jobs]
related: [technical-architecture.md, data-model.md, ui-system.md]
parent: INDEX.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# ECS System Design

[🇰🇷 Korean Version](./ecs-design_KOR.md)

## 📍 Navigation

[↩️ Back to Architecture](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. ECS Architecture Overview

### 1.1 Design Principles

#### Data-Oriented Design (DOD) Implementation
```csharp
// ❌ Object-oriented approach (inefficient)
class Citizen
{
    public float income;
    public float wealth;
    public float consumptionRate;
    public void Update() { /* 개별 처리 */ }
}

// ✅ Data-oriented approach (efficient)
struct PopulationComponent : IComponentData
{
    public float income;
    public float wealth;
    public float consumptionRate;
}
// → Process tens of thousands of entities in batch with Job System
```

#### Performance-First Design
- **Memory Locality**: Place related data in contiguous memory blocks
- **SIMD Utilization**: Vectorized operations through Burst Compiler
- **Cache Efficiency**: Maximum performance with minimal memory access

### 1.2 ECS World Structure

#### World Hierarchy
```
DefaultWorld (Main ECS World)
├── SimulationSystemGroup
│   ├── PopulationSystemGroup
│   ├── CompanySystemGroup  
│   ├── MarketSystemGroup
│   └── GovernmentSystemGroup
├── PresentationSystemGroup
│   ├── UIUpdateSystemGroup
│   └── DataVisualizationGroup
└── InitializationSystemGroup
```

## 2. Core Component Design

### 2.1 Economic Entity Components

#### Population Components
```csharp
// Basic population data
public struct PopulationComponent : IComponentData
{
    public int populationID;           // Unique identifier
    public PopulationClass socialClass; // Class (low/middle/high income)
    public float age;                  // Age (affects economic activity)
    public EmploymentStatus employment; // Employment status
}

// Economic attributes
public struct EconomicStatusComponent : IComponentData
{
    public float monthlyIncome;        // Monthly income
    public float totalWealth;          // Total assets
    public float savingsRate;          // Savings rate (0.0~1.0)
    public float consumptionRate;      // Consumption propensity (0.0~2.0)
    public float riskTolerance;        // Risk tolerance (investment preference)
}

// Consumption patterns
public struct ConsumptionComponent : IComponentData
{
    public float housingCost;          // Housing costs
    public float foodExpense;          // Food expenses
    public float luxurySpending;       // Luxury spending
    public float investmentAmount;     // Investment amount
    public float debtAmount;           // Debt amount
}

// Population classification enums
public enum PopulationClass : byte
{
    LowIncome = 0,    // Low income (bottom 30%)
    MiddleClass = 1,  // Middle class (middle 60%) 
    HighIncome = 2    // High income (top 10%)
}

public enum EmploymentStatus : byte
{
    Unemployed = 0,   // Unemployed
    Employed = 1,     // Employed
    SelfEmployed = 2, // Self-employed
    Retired = 3       // Retired
}
```

#### Company Components
```csharp
// Company basic information
public struct CompanyComponent : IComponentData
{
    public int companyID;
    public IndustryType industry;      // Industry type
    public CompanySize size;           // Company size
    public bool isPubliclyTraded;      // Public trading status
    public float foundedDate;          // Founded date (in-game time)
}

// Financial status
public struct FinancialComponent : IComponentData
{
    public float revenue;              // Revenue
    public float operatingCost;        // Operating costs
    public float netProfit;            // Net profit
    public float totalAssets;          // Total assets
    public float totalLiabilities;     // Total liabilities
    public float cashFlow;             // Cash flow
}

// Operational data
public struct OperationComponent : IComponentData
{
    public int employeeCount;          // Employee count
    public float productivity;         // Productivity index
    public float marketShare;          // Market share
    public float innovationLevel;      // Innovation level
    public float customerSatisfaction; // Customer satisfaction
}

// Stock data (public companies only)
public struct StockComponent : IComponentData
{
    public float stockPrice;           // Stock price
    public long sharesOutstanding;     // Outstanding shares
    public float dividendYield;        // Dividend yield
    public float pe_ratio;             // P/E ratio
    public float volatility;           // Volatility
}

// Industry classification
public enum IndustryType : byte
{
    Technology = 0,     // Technology
    Finance = 1,        // Finance
    Manufacturing = 2,  // Manufacturing
    Retail = 3,         // Retail
    Healthcare = 4,     // Healthcare
    Energy = 5,         // Energy
    RealEstate = 6,     // Real Estate
    Agriculture = 7     // Agriculture
}

public enum CompanySize : byte
{
    StartUp = 0,        // Startup (<50 employees)
    Small = 1,          // Small business (50-250 employees)
    Medium = 2,         // Medium business (250-1000 employees)
    Large = 3           // Large enterprise (1000+ employees)
}
```

#### Market Components
```csharp
// Product/service markets
public struct MarketComponent : IComponentData
{
    public MarketType marketType;      // Market type
    public float currentPrice;         // Current price
    public float demand;               // Total demand
    public float supply;               // Total supply
    public float volatility;           // Price volatility
    public float tradingVolume;        // Trading volume
}

// Financial markets (stocks, bonds, etc.)
public struct FinancialMarketComponent : IComponentData
{
    public float marketIndex;          // Market index
    public float totalMarketCap;       // Total market capitalization
    public float averagePE;            // Average P/E ratio
    public float interestRate;         // Interest rate
    public MarketSentiment sentiment;  // Market sentiment
}

public enum MarketType : byte
{
    Consumer = 0,       // Consumer goods
    Industrial = 1,     // Industrial goods
    Technology = 2,     // Technology
    Financial = 3,      // Financial products
    Commodity = 4       // Commodities
}

public enum MarketSentiment : byte
{
    VeryBearish = 0,    // Very bearish
    Bearish = 1,        // Bearish
    Neutral = 2,        // Neutral
    Bullish = 3,        // Bullish
    VeryBullish = 4     // Very bullish
}
```

### 2.2 Global State Components (Singleton)

#### Economic Indicators
```csharp
// Macroeconomic indicators
public struct MacroEconomicsComponent : IComponentData
{
    public float gdp;                  // GDP
    public float gdpGrowthRate;        // GDP growth rate
    public float inflationRate;        // Inflation rate
    public float unemploymentRate;     // Unemployment rate
    public float interestRate;         // Interest rate
    public float exchangeRate;         // Exchange rate (base: USD)
}

// Government policy
public struct GovernmentComponent : IComponentData
{
    public float taxRate;              // Tax rate
    public float governmentSpending;   // Government spending
    public float publicDebt;           // Public debt
    public float welfareSpending;      // Welfare spending
    public PolicyStance economicPolicy; // Economic policy stance
}

public enum PolicyStance : byte
{
    VeryLoose = 0,      // Very loose
    Loose = 1,          // Loose
    Neutral = 2,        // Neutral
    Tight = 3,          // Tight
    VeryTight = 4       // Very tight
}
```

## 3. Core System Design

### 3.1 Population Systems

#### PopulationBehaviorSystem
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateInGroup(typeof(PopulationSystemGroup))]
public partial class PopulationBehaviorSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = Time.DeltaTime;
        
        // Process in parallel with Job
        Dependency = new PopulationBehaviorJob
        {
            deltaTime = deltaTime,
            economicIndicators = GetSingleton<MacroEconomicsComponent>(),
            // Read/Write component handlers...
        }.ScheduleParallel(Dependency);
    }
}

[BurstCompile]
public struct PopulationBehaviorJob : IJobEntity
{
    [ReadOnly] public float deltaTime;
    [ReadOnly] public MacroEconomicsComponent economicIndicators;
    
    void Execute(ref EconomicStatusComponent economic, 
                ref ConsumptionComponent consumption,
                in PopulationComponent population)
    {
        // Adjust consumption patterns based on economic conditions
        float consumptionMultiplier = CalculateConsumptionMultiplier(
            economicIndicators.inflationRate,
            economicIndicators.unemploymentRate,
            population.socialClass
        );
        
        // Consumption decisions
        consumption.foodExpense = economic.monthlyIncome * 
            GetBaseFoodRate(population.socialClass) * consumptionMultiplier;
        
        consumption.luxurySpending = math.max(0, 
            (economic.monthlyIncome - GetBaseLivingCost(population)) * 
            economic.consumptionRate * consumptionMultiplier
        );
        
        // Savings and investment
        float remainingIncome = economic.monthlyIncome - 
            consumption.foodExpense - consumption.housingCost - consumption.luxurySpending;
        
        if (remainingIncome > 0)
        {
            consumption.investmentAmount = remainingIncome * economic.riskTolerance;
            economic.totalWealth += remainingIncome - consumption.investmentAmount;
        }
    }
    
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private float CalculateConsumptionMultiplier(float inflation, float unemployment, PopulationClass socialClass)
    {
        // Adjust consumption based on economic instability
        float baseMultiplier = 1.0f;
        
        // Inflation impact (negative)
        baseMultiplier -= inflation * 0.5f;
        
        // Unemployment impact (varies by class)
        float unemploymentImpact = socialClass switch
        {
            PopulationClass.LowIncome => unemployment * 1.5f,
            PopulationClass.MiddleClass => unemployment * 1.0f,
            PopulationClass.HighIncome => unemployment * 0.3f,
            _ => unemployment
        };
        
        baseMultiplier -= unemploymentImpact * 0.3f;
        
        return math.clamp(baseMultiplier, 0.1f, 2.0f);
    }
}
```

### 3.2 Company Systems

#### CompanyOperationSystem
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateInGroup(typeof(CompanySystemGroup))]
public partial class CompanyOperationSystem : SystemBase
{
    private EntityQuery marketQuery;
    private EntityQuery populationQuery;
    
    protected override void OnCreate()
    {
        marketQuery = GetEntityQuery(typeof(MarketComponent));
        populationQuery = GetEntityQuery(typeof(ConsumptionComponent));
    }
    
    protected override void OnUpdate()
    {
        // Calculate market demand
        var marketDemand = CalculateMarketDemand();
        
        Dependency = new CompanyOperationJob
        {
            marketDemand = marketDemand,
            deltaTime = Time.DeltaTime,
            macroEconomics = GetSingleton<MacroEconomicsComponent>()
        }.ScheduleParallel(Dependency);
    }
    
    private NativeHashMap<IndustryType, float> CalculateMarketDemand()
    {
        var demand = new NativeHashMap<IndustryType, float>(8, Allocator.TempJob);
        
        // Aggregate industry demand from population consumption patterns
        Entities.ForEach((in ConsumptionComponent consumption, in PopulationComponent population) =>
        {
            // Food demand
            demand.TryGetValue(IndustryType.Retail, out float currentRetailDemand);
            demand[IndustryType.Retail] = currentRetailDemand + consumption.foodExpense;
            
            // Luxury goods demand (technology, manufacturing)
            demand.TryGetValue(IndustryType.Technology, out float currentTechDemand);
            demand[IndustryType.Technology] = currentTechDemand + consumption.luxurySpending * 0.6f;
            
            // Calculate demand for other industries...
        }).Run();
        
        return demand;
    }
}

[BurstCompile]
public struct CompanyOperationJob : IJobEntity
{
    [ReadOnly] public NativeHashMap<IndustryType, float> marketDemand;
    [ReadOnly] public float deltaTime;
    [ReadOnly] public MacroEconomicsComponent macroEconomics;
    
    void Execute(ref FinancialComponent financial,
                ref OperationComponent operation,
                in CompanyComponent company)
    {
        // Analyze industry market demand
        marketDemand.TryGetValue(company.industry, out float industryDemand);
        
        // Calculate revenue based on market share
        float potentialRevenue = industryDemand * operation.marketShare;
        
        // Actual revenue based on productivity and innovation levels
        financial.revenue = potentialRevenue * 
            (0.7f + operation.productivity * 0.2f + operation.innovationLevel * 0.1f);
        
        // Calculate operating costs (employee wages + other costs)
        float laborCost = operation.employeeCount * GetAverageWage(company.industry) * deltaTime;
        float operationalOverhead = financial.revenue * GetOperationalCostRatio(company.size);
        financial.operatingCost = laborCost + operationalOverhead;
        
        // Net profit
        financial.netProfit = financial.revenue - financial.operatingCost;
        
        // Employment decisions (expand when demand increases)
        if (financial.netProfit > 0 && industryDemand > financial.revenue * 1.2f)
        {
            operation.employeeCount = (int)(operation.employeeCount * 1.01f); // 1% increase
        }
        else if (financial.netProfit < 0)
        {
            operation.employeeCount = (int)(operation.employeeCount * 0.99f); // 1% decrease
        }
        
        // Productivity improvement (R&D investment)
        if (financial.netProfit > 0)
        {
            float rdInvestment = financial.netProfit * 0.05f; // 5% of profit to R&D
            operation.innovationLevel += rdInvestment * 0.001f * deltaTime;
            operation.productivity = math.min(operation.productivity + rdInvestment * 0.0005f * deltaTime, 2.0f);
        }
    }
    
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private float GetAverageWage(IndustryType industry)
    {
        return industry switch
        {
            IndustryType.Technology => 5000f,
            IndustryType.Finance => 4500f,
            IndustryType.Manufacturing => 3000f,
            IndustryType.Retail => 2000f,
            _ => 3000f
        };
    }
    
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private float GetOperationalCostRatio(CompanySize size)
    {
        return size switch
        {
            CompanySize.StartUp => 0.8f,    // High cost structure
            CompanySize.Small => 0.7f,
            CompanySize.Medium => 0.6f,
            CompanySize.Large => 0.5f,      // Economies of scale
            _ => 0.6f
        };
    }
}
```

### 3.3 Market Systems

#### StockMarketSystem
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateInGroup(typeof(MarketSystemGroup))]
public partial class StockMarketSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = Time.DeltaTime;
        var macroEconomics = GetSingleton<MacroEconomicsComponent>();
        var marketSentiment = CalculateMarketSentiment(macroEconomics);
        
        Dependency = new StockPriceUpdateJob
        {
            deltaTime = deltaTime,
            marketSentiment = marketSentiment,
            interestRate = macroEconomics.interestRate,
            randomSeed = (uint)UnityEngine.Random.Range(1, int.MaxValue)
        }.ScheduleParallel(Dependency);
        
        // 시장 지수 업데이트
        UpdateMarketIndex();
    }
    
    private MarketSentiment CalculateMarketSentiment(MacroEconomicsComponent macro)
    {
        float sentimentScore = 0f;
        
        // GDP 성장률 영향
        sentimentScore += macro.gdpGrowthRate * 10f;
        
        // 인플레이션 영향 (부정적)
        sentimentScore -= macro.inflationRate * 5f;
        
        // 실업률 영향 (부정적)
        sentimentScore -= macro.unemploymentRate * 3f;
        
        // 금리 영향 (부정적, 주식에 대해)
        sentimentScore -= macro.interestRate * 2f;
        
        return sentimentScore switch
        {
            > 2f => MarketSentiment.VeryBullish,
            > 1f => MarketSentiment.Bullish,
            > -1f => MarketSentiment.Neutral,
            > -2f => MarketSentiment.Bearish,
            _ => MarketSentiment.VeryBearish
        };
    }
}

[BurstCompile]
public struct StockPriceUpdateJob : IJobEntity
{
    [ReadOnly] public float deltaTime;
    [ReadOnly] public MarketSentiment marketSentiment;
    [ReadOnly] public float interestRate;
    [ReadOnly] public uint randomSeed;
    
    void Execute([EntityInQueryIndex] int index, 
                ref StockComponent stock,
                in FinancialComponent financial,
                in OperationComponent operation)
    {
        var random = Random.CreateFromIndex((uint)(randomSeed + index));
        
        // 기본 주가 = 순이익 * PER
        float fundamentalValue = financial.netProfit * stock.pe_ratio;
        
        // 시장 심리에 따른 조정
        float sentimentMultiplier = marketSentiment switch
        {
            MarketSentiment.VeryBullish => 1.2f,
            MarketSentiment.Bullish => 1.1f,
            MarketSentiment.Neutral => 1.0f,
            MarketSentiment.Bearish => 0.9f,
            MarketSentiment.VeryBearish => 0.8f,
            _ => 1.0f
        };
        
        // Company-specific fundamental factors
        float companyMultiplier = 1.0f;
        companyMultiplier *= (0.8f + operation.productivity * 0.4f);        // Productivity
        companyMultiplier *= (0.9f + operation.innovationLevel * 0.2f);     // Innovation
        companyMultiplier *= (0.9f + operation.marketShare * 0.2f);         // Market share
        
        // Target price
        float targetPrice = fundamentalValue * sentimentMultiplier * companyMultiplier;
        
        // Gradual movement from current to target price (mean reversion)
        float priceChange = (targetPrice - stock.stockPrice) * 0.1f * deltaTime;
        
        // Add random volatility
        float randomVariation = random.NextFloat(-stock.volatility, stock.volatility) * stock.stockPrice * deltaTime;
        
        // Final stock price update
        stock.stockPrice = math.max(0.01f, stock.stockPrice + priceChange + randomVariation);
        
        // Adjust volatility based on market instability
        float baseVolatility = 0.02f; // Base 2% volatility
        float volatilityMultiplier = marketSentiment switch
        {
            MarketSentiment.VeryBullish => 0.8f,
            MarketSentiment.Bullish => 0.9f,
            MarketSentiment.Neutral => 1.0f,
            MarketSentiment.Bearish => 1.2f,
            MarketSentiment.VeryBearish => 1.5f,
            _ => 1.0f
        };
        
        stock.volatility = math.lerp(stock.volatility, baseVolatility * volatilityMultiplier, deltaTime * 0.1f);
        
        // Calculate dividend yield (percentage of profit)
        if (financial.netProfit > 0)
        {
            stock.dividendYield = (financial.netProfit * 0.3f) / (stock.stockPrice * stock.sharesOutstanding);
        }
    }
}
```

## 4. Performance Optimization Strategies

### 4.1 Memory Layout Optimization

#### Chunk Iteration Optimization
```csharp
[BurstCompile]
public struct OptimizedPopulationJob : IJobChunk
{
    [ReadOnly] public ComponentTypeHandle<PopulationComponent> populationHandle;
    [ReadOnly] public ComponentTypeHandle<EconomicStatusComponent> economicHandle;
    public ComponentTypeHandle<ConsumptionComponent> consumptionHandle;
    
    public void Execute(in ArchetypeChunk chunk, int unfilteredChunkIndex, bool useEnabledMask, in v128 chunkEnabledMask)
    {
        // Optimized processing by chunk
        var populations = chunk.GetNativeArray(ref populationHandle);
        var economics = chunk.GetNativeArray(ref economicHandle);
        var consumptions = chunk.GetNativeArray(ref consumptionHandle);
        
        // Vectorization for SIMD operations
        for (int i = 0; i < populations.Length; i += 4)
        {
            // Process 4 entities in parallel
            ProcessFourEntities(
                ref consumptions.GetSubArray(i, math.min(4, populations.Length - i)),
                populations.GetSubArray(i, math.min(4, populations.Length - i)),
                economics.GetSubArray(i, math.min(4, populations.Length - i))
            );
        }
    }
    
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private void ProcessFourEntities(ref NativeArray<ConsumptionComponent> consumptions,
                                   NativeArray<PopulationComponent> populations,
                                   NativeArray<EconomicStatusComponent> economics)
    {
        // Process 4 entities simultaneously using SIMD
        float4 incomes = new float4(
            economics[0].monthlyIncome,
            economics.Length > 1 ? economics[1].monthlyIncome : 0,
            economics.Length > 2 ? economics[2].monthlyIncome : 0,
            economics.Length > 3 ? economics[3].monthlyIncome : 0
        );
        
        float4 consumptionRates = new float4(
            economics[0].consumptionRate,
            economics.Length > 1 ? economics[1].consumptionRate : 0,
            economics.Length > 2 ? economics[2].consumptionRate : 0,
            economics.Length > 3 ? economics[3].consumptionRate : 0
        );
        
        // Vectorized consumption calculation
        float4 luxurySpending = incomes * consumptionRates * 0.3f; // 30% for luxury goods
        
        // Store results
        for (int i = 0; i < math.min(4, consumptions.Length); i++)
        {
            var consumption = consumptions[i];
            consumption.luxurySpending = luxurySpending[i];
            consumptions[i] = consumption;
        }
    }
}
```

### 4.2 Dynamic LOD System

#### Adaptive Simulation Depth
```csharp
public class AdaptiveLODSystem : SystemBase
{
    private EntityQuery allEntitiesQuery;
    private float targetFrameTime = 16.67f; // 60fps
    private SimulationLOD currentLOD = SimulationLOD.High;
    
    protected override void OnCreate()
    {
        allEntitiesQuery = GetEntityQuery(ComponentType.ReadOnly<PopulationComponent>());
    }
    
    protected override void OnUpdate()
    {
        int entityCount = allEntitiesQuery.CalculateEntityCount();
        float currentFrameTime = Time.unscaledDeltaTime * 1000f;
        
        // Adjust LOD based on frame time and entity count
        SimulationLOD newLOD = CalculateOptimalLOD(entityCount, currentFrameTime);
        
        if (newLOD != currentLOD)
        {
            currentLOD = newLOD;
            ApplyLODSettings(newLOD);
        }
        
        // Store LOD info in singleton entity
        SetSingleton(new SimulationLODComponent { currentLOD = currentLOD });
    }
    
    private SimulationLOD CalculateOptimalLOD(int entityCount, float frameTime)
    {
        // Performance-based LOD selection
        if (frameTime > targetFrameTime * 1.5f || entityCount > 50000)
            return SimulationLOD.Low;
        else if (frameTime > targetFrameTime * 1.2f || entityCount > 25000)
            return SimulationLOD.Medium;
        else if (frameTime > targetFrameTime * 1.1f || entityCount > 10000)
            return SimulationLOD.High;
        else
            return SimulationLOD.Ultra;
    }
    
    private void ApplyLODSettings(SimulationLOD lod)
    {
        var populationSystem = World.GetOrCreateSystemManaged<PopulationBehaviorSystem>();
        var companySystem = World.GetOrCreateSystemManaged<CompanyOperationSystem>();
        var stockSystem = World.GetOrCreateSystemManaged<StockMarketSystem>();
        
        switch (lod)
        {
            case SimulationLOD.Ultra:
                // All systems at full detail
                populationSystem.Enabled = true;
                companySystem.Enabled = true;
                stockSystem.Enabled = true;
                break;
                
            case SimulationLOD.High:
                // Most systems active, some simplified
                populationSystem.Enabled = true;
                companySystem.Enabled = true;
                stockSystem.Enabled = true;
                break;
                
            case SimulationLOD.Medium:
                // Core systems only active
                populationSystem.Enabled = true;
                companySystem.Enabled = false; // Companies processed in groups
                stockSystem.Enabled = true;
                break;
                
            case SimulationLOD.Low:
                // Minimal systems, statistical approximation
                populationSystem.Enabled = false; // Statistical processing
                companySystem.Enabled = false;
                stockSystem.Enabled = false;
                break;
        }
    }
}

public struct SimulationLODComponent : IComponentData
{
    public SimulationLOD currentLOD;
}

public enum SimulationLOD : byte
{
    Low = 0,      // Statistical approximation
    Medium = 1,   // Group-based processing
    High = 2,     // Most individual processing
    Ultra = 3     // All entities individually
}
```

## 5. Data Flow and Synchronization

### 5.1 Inter-System Data Dependencies

#### Execution Order Optimization
```csharp
// Define dependency chain
[UpdateInGroup(typeof(SimulationSystemGroup), OrderFirst = true)]
public partial class MacroEconomicsUpdateSystem : SystemBase { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(MacroEconomicsUpdateSystem))]
public partial class PopulationSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(PopulationSystemGroup))]
public partial class PopulationBehaviorSystem : SystemBase { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(PopulationSystemGroup))]
public partial class CompanySystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(CompanySystemGroup))]
public partial class CompanyOperationSystem : SystemBase { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(CompanySystemGroup))]
public partial class MarketSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(MarketSystemGroup))]
public partial class StockMarketSystem : SystemBase { }

[UpdateInGroup(typeof(SimulationSystemGroup), OrderLast = true)]
public partial class StatisticsAggregationSystem : SystemBase { }
```

### 5.2 Cache and Intermediate Result Storage

#### Statistics Caching System
```csharp
// Aggregated statistics cache
public struct CachedStatisticsComponent : IComponentData
{
    public float totalGDP;
    public float averageIncome;
    public float totalMarketCap;
    public float unemploymentRate;
    
    public int lastUpdateFrame;
    public bool isDirty;
}

[UpdateInGroup(typeof(SimulationSystemGroup), OrderLast = true)]
public partial class StatisticsAggregationSystem : SystemBase
{
    protected override void OnUpdate()
    {
        var cachedStats = GetSingleton<CachedStatisticsComponent>();
        
        // Recalculate only when cache is invalid or for periodic updates
        if (cachedStats.isDirty || Time.frameCount - cachedStats.lastUpdateFrame > 60)
        {
            UpdateCachedStatistics(ref cachedStats);
            SetSingleton(cachedStats);
        }
    }
    
    private void UpdateCachedStatistics(ref CachedStatisticsComponent cache)
    {
        // Calculate GDP (sum of all companies' value added)
        float totalRevenue = 0f;
        float totalCosts = 0f;
        
        Entities.ForEach((in FinancialComponent financial) =>
        {
            totalRevenue += financial.revenue;
            totalCosts += financial.operatingCost;
        }).Run();
        
        cache.totalGDP = totalRevenue - totalCosts;
        
        // Calculate average income
        float totalIncome = 0f;
        int populationCount = 0;
        
        Entities.ForEach((in EconomicStatusComponent economic) =>
        {
            totalIncome += economic.monthlyIncome;
            populationCount++;
        }).Run();
        
        cache.averageIncome = populationCount > 0 ? totalIncome / populationCount : 0f;
        
        // Calculate unemployment rate
        int employedCount = 0;
        int totalPopulation = 0;
        
        Entities.ForEach((in PopulationComponent population) =>
        {
            totalPopulation++;
            if (population.employment == EmploymentStatus.Employed)
                employedCount++;
        }).Run();
        
        cache.unemploymentRate = totalPopulation > 0 ? 
            1f - ((float)employedCount / totalPopulation) : 0f;
        
        // Total market capitalization
        cache.totalMarketCap = 0f;
        Entities.ForEach((in StockComponent stock) =>
        {
            cache.totalMarketCap += stock.stockPrice * stock.sharesOutstanding;
        }).Run();
        
        cache.lastUpdateFrame = Time.frameCount;
        cache.isDirty = false;
    }
}
```

## Next Documents
- [Data Model Specification](./data-model.md)
- [UI System Design](./ui-system.md) 
- [System Integration Guide](./integration-guide.md)