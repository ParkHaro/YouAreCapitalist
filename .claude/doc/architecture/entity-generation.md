---
category: architecture
tags: [entity-generation, random, population, company, spawning]
related: [simulation-system.md, data-model.md, ecs-design.md]
parent: INDEX.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# Entity Generation System

[🇰🇷 Korean Version](./entity-generation_KOR.md)

## 📍 Navigation

[↩️ Back to Architecture](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Generation Overview

### 1.1 Core Principles

#### Realistic Distribution Patterns
- **Income Inequality**: Follow real-world Pareto distribution (80/20 rule)
- **Industry Balance**: Reflect realistic economic sector proportions
- **Age Demographics**: Natural population pyramid with working age majority
- **Regional Variation**: Geographic and cultural diversity factors

#### Procedural Generation Strategy
```csharp
// Example: Population generation with realistic distributions
public struct PopulationGenerationConfig
{
    public AnimationCurve ageDistribution;      // Population pyramid curve
    public AnimationCurve incomeDistribution;   // Pareto distribution for income
    public AnimationCurve educationDistribution; // Education level curve
    public float genderRatio;                   // Male/Female ratio (0.5 = 50/50)
}
```

### 1.2 Generation Targets

#### Initial Population: 1,000 Entities
- **Low Income (60%)**: 600 entities
- **Middle Class (35%)**: 350 entities  
- **High Income (5%)**: 50 entities

#### Initial Companies: 100 Entities
- **Small Business (70%)**: 70 companies
- **Medium Business (25%)**: 25 companies
- **Large Corporation (5%)**: 5 companies

## 2. Population Generation System

### 2.1 Population Spawn System

#### Core Generation Logic
```csharp
public partial struct PopulationSpawnSystem : ISystem
{
    private Unity.Mathematics.Random random;
    
    public void OnCreate(ref SystemState state)
    {
        random = Unity.Mathematics.Random.CreateFromIndex((uint)System.DateTime.Now.Millisecond);
    }
    
    public void OnUpdate(ref SystemState state)
    {
        // Get configuration from singleton
        var config = SystemAPI.GetSingleton<EconomicConfiguration>();
        
        // Generate initial population if needed
        if (ShouldSpawnInitialPopulation())
        {
            SpawnInitialPopulation(ref state, config);
        }
        
        // Handle dynamic population growth
        HandlePopulationGrowth(ref state, config);
    }
    
    private void SpawnInitialPopulation(ref SystemState state, EconomicConfiguration config)
    {
        var commandBuffer = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                                   .CreateCommandBuffer(state.WorldUnmanaged);
        
        for (int i = 0; i < config.initialPopulationCount; i++)
        {
            Entity newPop = commandBuffer.CreateEntity();
            
            // Generate basic demographics
            var demographics = GenerateDemographics(config);
            var economics = GenerateEconomicStatus(demographics, config);
            var behavior = GenerateBehaviorProfile(demographics);
            
            // Add components
            commandBuffer.AddComponent(newPop, new PopulationComponent 
            {
                populationID = i,
                socialClass = DetermineClass(economics.monthlyIncome),
                age = demographics.age,
                employment = DetermineEmployment(demographics, economics)
            });
            
            commandBuffer.AddComponent(newPop, economics);
            commandBuffer.AddComponent(newPop, demographics);
            commandBuffer.AddComponent(newPop, behavior);
        }
    }
}
```

### 2.2 Demographic Generation Algorithms

#### Age Distribution
```csharp
private DemographicsComponent GenerateDemographics(EconomicConfiguration config)
{
    // Generate age using realistic population pyramid
    float ageRandom = random.NextFloat();
    float age = config.ageDistribution.Evaluate(ageRandom) * 80f + 18f; // 18-98 years
    
    // Gender distribution
    Gender gender = random.NextFloat() < config.genderRatio ? Gender.Male : Gender.Female;
    
    // Education level based on age cohort
    EducationLevel education = GenerateEducationLevel(age);
    
    // Regional distribution
    Region region = GenerateRegion();
    
    return new DemographicsComponent
    {
        gender = gender,
        education = education,
        residence = region,
        age = (int)age,
        familyStatus = GenerateFamilyStatus(age, gender),
        dependents = GenerateDependents(age)
    };
}

private EducationLevel GenerateEducationLevel(float age)
{
    // Younger generations are more educated
    float educationBonus = math.max(0, (60f - age) / 60f); // 0-1 bonus for younger people
    float educationRoll = random.NextFloat() + educationBonus * 0.3f;
    
    if (educationRoll > 0.95f) return EducationLevel.Graduate;
    if (educationRoll > 0.75f) return EducationLevel.University;
    if (educationRoll > 0.50f) return EducationLevel.College;
    if (educationRoll > 0.30f) return EducationLevel.HighSchool;
    if (educationRoll > 0.15f) return EducationLevel.MiddleSchool;
    return EducationLevel.Elementary;
}
```

#### Economic Status Generation
```csharp
private EconomicStatusComponent GenerateEconomicStatus(DemographicsComponent demo, 
                                                     EconomicConfiguration config)
{
    // Base income from education and age
    float baseIncome = CalculateBaseIncome(demo.education, demo.age);
    
    // Apply Pareto distribution for income inequality
    float incomeMultiplier = SampleParetoDistribution(1.16f); // Realistic Pareto parameter
    float monthlyIncome = baseIncome * incomeMultiplier;
    
    // Total wealth based on age and savings pattern
    float wealthMultiplier = math.max(0.1f, (demo.age - 18f) / 50f); // Wealth accumulates over time
    float totalWealth = monthlyIncome * 12f * wealthMultiplier * random.NextFloat(0.5f, 2.0f);
    
    // Risk tolerance based on age and education
    float riskTolerance = GenerateRiskTolerance(demo.age, demo.education);
    
    return new EconomicStatusComponent
    {
        monthlyIncome = monthlyIncome,
        totalWealth = math.max(0, totalWealth),
        savingsRate = random.NextFloat(0.05f, 0.30f),
        consumptionRate = random.NextFloat(0.70f, 1.20f),
        riskTolerance = riskTolerance
    };
}

private float SampleParetoDistribution(float alpha)
{
    // Generate Pareto-distributed random variable
    // 80% of wealth owned by 20% of population
    float uniform = random.NextFloat(0.001f, 0.999f); // Avoid extremes
    return math.pow(1f - uniform, -1f / alpha);
}

private float CalculateBaseIncome(EducationLevel education, float age)
{
    // Base salary by education level (monthly, in thousands)
    float baseSalary = education switch
    {
        EducationLevel.Elementary => 150f,
        EducationLevel.MiddleSchool => 180f,
        EducationLevel.HighSchool => 220f,
        EducationLevel.College => 280f,
        EducationLevel.University => 350f,
        EducationLevel.Graduate => 450f,
        _ => 200f
    };
    
    // Age factor: peak earnings in 40s-50s
    float ageFactor = math.sin(math.PI * math.clamp((age - 20f) / 50f, 0f, 1f)) * 0.5f + 0.75f;
    
    return baseSalary * ageFactor * random.NextFloat(0.8f, 1.2f);
}
```

### 2.3 Behavioral Profile Generation

#### Personality Traits
```csharp
private BehaviorComponent GenerateBehaviorProfile(DemographicsComponent demo)
{
    // Generate correlated personality traits
    float baseOptimism = random.NextFloat(0.3f, 0.7f);
    
    // Education affects information level and rationality
    float informationLevel = (float)demo.education / 6f + random.NextFloat(-0.2f, 0.2f);
    informationLevel = math.clamp(informationLevel, 0f, 1f);
    
    // Age affects conformity and conservatism
    float conformityLevel = (demo.age / 80f) * 0.6f + random.NextFloat(0.2f, 0.8f);
    conformityLevel = math.clamp(conformityLevel, 0f, 1f);
    
    // Loyalty is normally distributed
    float loyaltyLevel = SampleNormalDistribution(0.5f, 0.2f);
    
    return new BehaviorComponent
    {
        optimismLevel = baseOptimism,
        conformityLevel = conformityLevel,
        loyaltyLevel = loyaltyLevel,
        informationLevel = informationLevel
    };
}

private float SampleNormalDistribution(float mean, float stdDev)
{
    // Box-Muller transformation for normal distribution
    float u1 = random.NextFloat(0.001f, 0.999f);
    float u2 = random.NextFloat(0.001f, 0.999f);
    
    float z0 = math.sqrt(-2f * math.log(u1)) * math.cos(2f * math.PI * u2);
    return math.clamp(mean + z0 * stdDev, 0f, 1f);
}
```

## 3. Company Generation System

### 3.1 Company Spawn System

#### Core Company Generation
```csharp
public partial struct CompanySpawnSystem : ISystem
{
    private Unity.Mathematics.Random random;
    
    private void SpawnInitialCompanies(ref SystemState state, EconomicConfiguration config)
    {
        var commandBuffer = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                                   .CreateCommandBuffer(state.WorldUnmanaged);
        
        for (int i = 0; i < config.initialCompanyCount; i++)
        {
            Entity newCompany = commandBuffer.CreateEntity();
            
            // Generate company profile
            var company = GenerateCompanyProfile(i);
            var financial = GenerateFinancialProfile(company);
            var operation = GenerateOperationProfile(company, financial);
            var strategy = GenerateStrategyProfile(company);
            
            // Add components
            commandBuffer.AddComponent(newCompany, company);
            commandBuffer.AddComponent(newCompany, financial);
            commandBuffer.AddComponent(newCompany, operation);
            commandBuffer.AddComponent(newCompany, strategy);
            
            // Add stock component for public companies
            if (company.isPubliclyTraded)
            {
                var stock = GenerateStockProfile(company, financial);
                commandBuffer.AddComponent(newCompany, stock);
            }
        }
    }
}
```

### 3.2 Company Profile Generation

#### Industry Distribution
```csharp
private CompanyComponent GenerateCompanyProfile(int companyID)
{
    // Industry distribution based on realistic economic composition
    IndustryType industry = SelectIndustryByWeight();
    CompanySize size = SelectCompanySize();
    CompanyStage stage = SelectCompanyStage(size);
    
    // Public trading probability based on size
    bool isPublic = ShouldBePubliclyTraded(size);
    
    // Generate company name based on industry
    FixedString64Bytes companyName = GenerateCompanyName(industry, companyID);
    
    return new CompanyComponent
    {
        companyID = companyID,
        companyName = companyName,
        industry = industry,
        size = size,
        stage = stage,
        isPubliclyTraded = isPublic,
        foundedDate = GenerateFoundedDate()
    };
}

private IndustryType SelectIndustryByWeight()
{
    float roll = random.NextFloat();
    
    // Realistic industry distribution
    if (roll < 0.25f) return IndustryType.Retail;           // 25% - Service sector
    if (roll < 0.45f) return IndustryType.Manufacturing;    // 20% - Manufacturing
    if (roll < 0.60f) return IndustryType.Technology;       // 15% - Tech sector
    if (roll < 0.70f) return IndustryType.Construction;     // 10% - Construction
    if (roll < 0.80f) return IndustryType.Finance;         // 10% - Financial services
    if (roll < 0.85f) return IndustryType.Healthcare;      // 5% - Healthcare
    if (roll < 0.90f) return IndustryType.Education;       // 5% - Education
    if (roll < 0.95f) return IndustryType.Transportation;   // 5% - Transportation
    return IndustryType.Agriculture;                        // 5% - Other sectors
}

private CompanySize SelectCompanySize()
{
    float roll = random.NextFloat();
    
    // Realistic company size distribution (small business economy)
    if (roll < 0.70f) return CompanySize.Small;        // 70% - Small business
    if (roll < 0.90f) return CompanySize.Medium;       // 20% - Medium business
    if (roll < 0.98f) return CompanySize.Large;        // 8% - Large companies
    return CompanySize.Conglomerate;                    // 2% - Conglomerates
}
```

### 3.3 Financial Profile Generation

#### Revenue and Profitability
```csharp
private FinancialComponent GenerateFinancialProfile(CompanyComponent company)
{
    // Base revenue by size and industry
    float baseRevenue = CalculateBaseRevenue(company.size, company.industry);
    
    // Apply industry-specific multipliers and stage adjustments
    float stageMultiplier = company.stage switch
    {
        CompanyStage.Seed => random.NextFloat(0.1f, 0.3f),
        CompanyStage.StartUp => random.NextFloat(0.2f, 0.8f),
        CompanyStage.Growth => random.NextFloat(0.8f, 2.0f),
        CompanyStage.Mature => random.NextFloat(0.9f, 1.2f),
        CompanyStage.Decline => random.NextFloat(0.4f, 0.8f),
        _ => 1.0f
    };
    
    float revenue = baseRevenue * stageMultiplier;
    
    // Operating costs (70-90% of revenue typically)
    float operatingCost = revenue * random.NextFloat(0.70f, 0.90f);
    float netProfit = revenue - operatingCost;
    
    // Assets and liabilities based on revenue
    float totalAssets = revenue * random.NextFloat(0.8f, 2.5f);
    float totalLiabilities = totalAssets * random.NextFloat(0.30f, 0.70f);
    
    // Cash flow variation
    float cashFlow = netProfit * random.NextFloat(0.8f, 1.2f);
    
    return new FinancialComponent
    {
        revenue = revenue,
        operatingCost = operatingCost,
        netProfit = netProfit,
        totalAssets = totalAssets,
        totalLiabilities = totalLiabilities,
        cashFlow = cashFlow,
        retainedEarnings = netProfit * random.NextFloat(0.5f, 0.9f)
    };
}

private float CalculateBaseRevenue(CompanySize size, IndustryType industry)
{
    // Base monthly revenue by company size (in thousands)
    float sizeMultiplier = size switch
    {
        CompanySize.Micro => random.NextFloat(10f, 50f),
        CompanySize.Small => random.NextFloat(50f, 500f),
        CompanySize.Medium => random.NextFloat(500f, 5000f),
        CompanySize.Large => random.NextFloat(5000f, 50000f),
        CompanySize.Conglomerate => random.NextFloat(50000f, 500000f),
        _ => 100f
    };
    
    // Industry-specific revenue multipliers
    float industryMultiplier = industry switch
    {
        IndustryType.Technology => random.NextFloat(1.2f, 2.0f),    // High margins
        IndustryType.Finance => random.NextFloat(1.1f, 1.8f),       // Financial services
        IndustryType.Healthcare => random.NextFloat(1.0f, 1.5f),    // Stable demand
        IndustryType.Manufacturing => random.NextFloat(0.8f, 1.2f), // Capital intensive
        IndustryType.Retail => random.NextFloat(0.7f, 1.1f),        // Low margins
        IndustryType.Agriculture => random.NextFloat(0.6f, 0.9f),   // Commodity pricing
        _ => 1.0f
    };
    
    return sizeMultiplier * industryMultiplier;
}
```

### 3.4 Operational Characteristics

#### Employee and Productivity Generation
```csharp
private OperationComponent GenerateOperationProfile(CompanyComponent company, FinancialComponent financial)
{
    // Employee count based on company size and industry
    int employeeCount = CalculateEmployeeCount(company.size, company.industry);
    
    // Productivity index based on stage and industry
    float productivity = GenerateProductivityIndex(company.stage, company.industry);
    
    // Market share (small for most companies)
    float marketShare = CalculateMarketShare(company.size, financial.revenue);
    
    // Innovation and customer satisfaction
    float innovation = GenerateInnovationLevel(company.industry, company.stage);
    float customerSatisfaction = random.NextFloat(2.5f, 4.5f);
    
    // Brand value correlated with size and age
    float brandValue = CalculateBrandValue(company, financial);
    
    return new OperationComponent
    {
        employeeCount = employeeCount,
        productivity = productivity,
        marketShare = marketShare,
        innovationLevel = innovation,
        customerSatisfaction = customerSatisfaction,
        brandValue = brandValue
    };
}

private int CalculateEmployeeCount(CompanySize size, IndustryType industry)
{
    // Base employee count by size
    int baseEmployees = size switch
    {
        CompanySize.Micro => random.NextInt(1, 10),
        CompanySize.Small => random.NextInt(10, 50),
        CompanySize.Medium => random.NextInt(50, 300),
        CompanySize.Large => random.NextInt(300, 1000),
        CompanySize.Conglomerate => random.NextInt(1000, 10000),
        _ => 25
    };
    
    // Industry labor intensity multiplier
    float industryMultiplier = industry switch
    {
        IndustryType.Manufacturing => 1.3f,      // Labor intensive
        IndustryType.Retail => 1.2f,            // Service intensive
        IndustryType.Technology => 0.8f,         // Capital intensive
        IndustryType.Finance => 0.9f,           // Knowledge intensive
        _ => 1.0f
    };
    
    return (int)(baseEmployees * industryMultiplier);
}
```

## 4. Market Initialization

### 4.1 Market Entity Creation

#### Industry Market Setup
```csharp
public partial struct MarketInitializationSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        if (ShouldInitializeMarkets())
        {
            InitializeIndustryMarkets(ref state);
            InitializeFinancialMarkets(ref state);
        }
    }
    
    private void InitializeIndustryMarkets(ref SystemState state)
    {
        var commandBuffer = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                                   .CreateCommandBuffer(state.WorldUnmanaged);
        
        // Create market for each industry
        var industries = System.Enum.GetValues<IndustryType>();
        foreach (var industry in industries)
        {
            Entity marketEntity = commandBuffer.CreateEntity();
            
            var market = new MarketComponent
            {
                marketID = (int)industry,
                marketType = DetermineMarketType(industry),
                industry = industry,
                marketSize = CalculateMarketSize(industry),
                growthRate = CalculateGrowthRate(industry),
                structure = DetermineMarketStructure(industry)
            };
            
            var dynamics = new MarketDynamicsComponent
            {
                currentPrice = CalculateInitialPrice(industry),
                demandLevel = random.NextFloat(0.7f, 1.3f),
                supplyLevel = random.NextFloat(0.7f, 1.3f),
                elasticity = CalculatePriceElasticity(industry),
                seasonalFactor = 1.0f,
                trendFactor = 1.0f
            };
            
            commandBuffer.AddComponent(marketEntity, market);
            commandBuffer.AddComponent(marketEntity, dynamics);
        }
    }
}
```

## 5. Configuration System

### 5.1 Generation Parameters

#### ScriptableObject Configuration
```csharp
[CreateAssetMenu(fileName = "GenerationConfig", menuName = "Capitalism/Generation Configuration")]
public class GenerationConfiguration : ScriptableObject
{
    [Header("Population Generation")]
    public int targetPopulation = 1000;
    public AnimationCurve ageDistribution;
    public AnimationCurve incomeDistribution;
    public float genderRatio = 0.5f;
    
    [Header("Company Generation")]  
    public int targetCompanyCount = 100;
    public IndustryWeight[] industryWeights;
    public CompanySizeWeight[] sizeWeights;
    
    [Header("Economic Parameters")]
    public float baseInflationRate = 0.02f;
    public float unemploymentRate = 0.05f;
    public float economicGrowthRate = 0.03f;
    
    [Header("Random Seed")]
    public bool useRandomSeed = true;
    public uint fixedSeed = 12345;
}

[System.Serializable]
public struct IndustryWeight
{
    public IndustryType industry;
    public float weight;
    public float revenueMultiplier;
}

[System.Serializable]
public struct CompanySizeWeight  
{
    public CompanySize size;
    public float probability;
    public float publicTradingChance;
}
```

## 6. Validation and Testing

### 6.1 Generation Validation

#### Statistical Validation
```csharp
public static class GenerationValidator
{
    public static ValidationResult ValidatePopulationDistribution(NativeArray<PopulationComponent> population)
    {
        var result = new ValidationResult();
        
        // Validate income distribution follows Pareto principle
        float totalWealth = CalculateTotalWealth(population);
        float top20Wealth = CalculateTop20Wealth(population);
        float paretoRatio = top20Wealth / totalWealth;
        
        if (paretoRatio < 0.70f || paretoRatio > 0.90f)
        {
            result.AddWarning($"Income distribution ratio: {paretoRatio:P1} (expected: 70-90%)");
        }
        
        // Validate age distribution
        ValidateAgeDistribution(population, ref result);
        
        // Validate employment rates
        ValidateEmploymentRates(population, ref result);
        
        return result;
    }
    
    public static ValidationResult ValidateCompanyDistribution(NativeArray<CompanyComponent> companies)
    {
        var result = new ValidationResult();
        
        // Validate industry distribution
        ValidateIndustryBalance(companies, ref result);
        
        // Validate size distribution
        ValidateSizeDistribution(companies, ref result);
        
        return result;
    }
}
```

## Next Steps

1. **[Implementation Roadmap](./implementation-roadmap.md)** - Step-by-step development guide
2. **[Simulation System](./simulation-system.md)** - How generated entities interact

## Related Documents

- [Data Model](./data-model.md) - Component specifications
- [ECS Design](./ecs-design.md) - System architecture
- [Technical Architecture](./technical-architecture.md) - Overall system design