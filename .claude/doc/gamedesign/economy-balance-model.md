---
category: gamedesign
tags: [economy, balance, model, parameters, formulas]
related: [capitalism-game-design-doc.md, core-gameplay-loop.md, investment-loop-mechanics.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# Economy Balance Model

[🇰🇷 Korean Version](./economy-balance-model_KOR.md)

## 📍 Navigation

[↩️ Back to Game Design](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Economic Balance Philosophy

### 1.1 Design Principles

#### Realistic Economic Dynamics
- **Pareto Distribution**: Wealth inequality follows real-world patterns (80/20 rule)
- **Market Efficiency**: Prices converge toward fair value through supply/demand
- **Economic Cycles**: Natural boom/bust cycles emerge from system dynamics
- **Emergent Complexity**: Complex patterns arise from simple rules

#### Player Experience Balance
- **Progressive Difficulty**: Early success builds confidence, later challenges maintain engagement
- **Multiple Viable Strategies**: No single "optimal" path to success
- **Risk/Reward Scaling**: Higher risks offer proportionally higher rewards
- **Automation Value**: Automation becomes increasingly valuable as complexity grows

### 1.2 Key Balance Metrics

#### Economic Health Indicators
```
GDP Growth Rate: 2-4% annually (healthy economy)
Inflation Rate: 1-3% annually (stable prices)
Unemployment Rate: 3-8% (realistic variation)
Market Volatility: 15-25% annual standard deviation
Wealth Gini Coefficient: 0.6-0.8 (realistic inequality)
```

## 2. Population Economic Model

### 2.1 Income Distribution Mathematics

#### Pareto Distribution Formula
```csharp
// Pareto distribution for income generation
public float GenerateParetoIncome(float alpha = 1.16f, float xMin = 25000f)
{
    float uniform = Random.Range(0.001f, 0.999f);
    return xMin * Mathf.Pow(1f - uniform, -1f / alpha);
}

// Income class thresholds
public PopulationClass DetermineIncomeClass(float income)
{
    if (income < 30000f) return PopulationClass.LowIncome;    // 60%
    if (income < 75000f) return PopulationClass.MiddleClass;  // 35%
    return PopulationClass.HighIncome;                        // 5%
}
```

#### Consumption Function
```csharp
// Keynes consumption function: C = a + b*Y
public float CalculateConsumption(float income, float wealth)
{
    float autonomousConsumption = 15000f; // Basic needs
    float marginalConsumption = 0.75f;    // 75% of income
    float wealthEffect = 0.05f;           // 5% of wealth
    
    return autonomousConsumption + 
           (marginalConsumption * income) + 
           (wealthEffect * wealth * 0.01f); // Annual wealth effect
}
```

### 2.2 Behavioral Economics Parameters

#### Decision-Making Factors
```csharp
[System.Serializable]
public struct BehaviorParameters
{
    [Header("Risk Tolerance")]
    public AnimationCurve riskByAge;           // Risk decreases with age
    public AnimationCurve riskByWealth;        // Risk tolerance increases with wealth
    public float baseRiskAversion;             // 0.5-0.8 typical range
    
    [Header("Social Influence")]
    public float conformityWeight;             // 0.3 - following others
    public float informationWeight;            // 0.4 - rational analysis
    public float emotionWeight;                // 0.3 - emotional decisions
    
    [Header("Time Preferences")]
    public float discountRate;                 // 0.03-0.15 annually
    public AnimationCurve patienceByEducation; // Higher education = more patience
}
```

## 3. Company Financial Model

### 3.1 Revenue Generation

#### Base Revenue Formula
```csharp
public float CalculateCompanyRevenue(CompanyComponent company, MarketDynamicsComponent market)
{
    // Base production capacity
    float productionCapacity = company.employeeCount * company.productivityIndex;
    
    // Market demand factor
    float demandMultiplier = Mathf.Clamp(market.demandLevel / market.supplyLevel, 0.5f, 2.0f);
    
    // Industry-specific multipliers
    float industryMultiplier = GetIndustryMultiplier(company.industry);
    
    // Company size economies of scale
    float scaleMultiplier = 1f + (company.employeeCount * 0.001f); // Larger = more efficient
    
    return productionCapacity * demandMultiplier * industryMultiplier * scaleMultiplier;
}

private float GetIndustryMultiplier(IndustryType industry)
{
    return industry switch
    {
        IndustryType.Technology => 2.0f,      // High margin
        IndustryType.Finance => 1.8f,         // High margin
        IndustryType.Healthcare => 1.5f,      // Stable demand
        IndustryType.Manufacturing => 1.2f,   // Moderate margin
        IndustryType.Retail => 1.0f,          // Base margin
        IndustryType.Agriculture => 0.8f,     // Low margin
        _ => 1.0f
    };
}
```

### 3.2 Cost Structure

#### Operating Cost Model
```csharp
[System.Serializable]
public struct OperatingCostModel
{
    [Header("Fixed Costs")]
    public float baseMonthlyCost;              // Base operating cost
    public float employeeCostPerHead;          // $4000/month average
    public float facilityCostPerEmployee;      // $500/month rent per employee
    
    [Header("Variable Costs")]
    public float materialCostRatio;            // 0.4 (40% of revenue)
    public float marketingCostRatio;           // 0.05 (5% of revenue)
    public float rdCostRatio;                  // 0.03 (3% of revenue)
    
    [Header("Financial Costs")]
    public float interestRate;                 // 0.05 (5% annually)
    public float taxRate;                      // 0.21 (21% corporate tax)
}

public float CalculateTotalCosts(CompanyComponent company, float revenue)
{
    var cost = operatingCostModel;
    
    float fixedCosts = cost.baseMonthlyCost + 
                       (company.employeeCount * cost.employeeCostPerHead) +
                       (company.employeeCount * cost.facilityCostPerEmployee);
    
    float variableCosts = revenue * (cost.materialCostRatio + 
                                    cost.marketingCostRatio + 
                                    cost.rdCostRatio);
    
    float financialCosts = company.totalDebt * (cost.interestRate / 12f);
    
    return fixedCosts + variableCosts + financialCosts;
}
```

## 4. Market Dynamics

### 4.1 Price Discovery Mechanism

#### Supply and Demand Balance
```csharp
public void UpdateMarketPrice(ref MarketDynamicsComponent market)
{
    // Calculate current supply and demand
    float totalSupply = CalculateIndustrySupply(market.industry);
    float totalDemand = CalculateIndustryDemand(market.industry);
    
    // Price elasticity factors
    float priceElasticity = GetPriceElasticity(market.industry);
    float supplyElasticity = GetSupplyElasticity(market.industry);
    
    // Equilibrium price calculation
    float equilibriumPrice = CalculateEquilibriumPrice(totalSupply, totalDemand, priceElasticity);
    
    // Price adjustment speed (prevents extreme volatility)
    float adjustmentSpeed = 0.1f; // 10% adjustment per update
    float priceChange = (equilibriumPrice - market.currentPrice) * adjustmentSpeed;
    
    // Apply random market noise
    float volatility = GetMarketVolatility(market.industry);
    float randomFactor = Random.Range(-volatility, volatility);
    
    market.currentPrice = Mathf.Max(0.1f, market.currentPrice + priceChange + randomFactor);
}

private float GetPriceElasticity(IndustryType industry)
{
    return industry switch
    {
        IndustryType.Healthcare => 0.2f,      // Inelastic (necessity)
        IndustryType.Agriculture => 0.3f,     // Inelastic (food)
        IndustryType.Finance => 0.8f,         // Moderately elastic
        IndustryType.Technology => 1.2f,      // Elastic (upgrades)
        IndustryType.Retail => 1.5f,          // Elastic (discretionary)
        _ => 1.0f
    };
}
```

### 4.2 Economic Cycles

#### Business Cycle Model
```csharp
[System.Serializable]
public struct BusinessCycleParameters
{
    [Header("Cycle Timing")]
    public float expansionDuration;        // 60-120 months
    public float recessionDuration;        // 6-18 months
    public float recoveryDuration;         // 12-24 months
    
    [Header("Economic Impact")]
    public AnimationCurve gdpGrowthCycle;  // GDP growth over cycle
    public AnimationCurve unemploymentCycle; // Unemployment rate changes
    public AnimationCurve inflationCycle;   // Inflation rate changes
    public AnimationCurve marketSentiment;  // Market confidence
}

public void ApplyCyclicalEffects(float cyclePosition)
{
    // cyclePosition: 0-1 representing position in business cycle
    
    float gdpMultiplier = businessCycle.gdpGrowthCycle.Evaluate(cyclePosition);
    float unemploymentRate = businessCycle.unemploymentCycle.Evaluate(cyclePosition);
    float inflationRate = businessCycle.inflationCycle.Evaluate(cyclePosition);
    
    // Apply to all companies and population
    ApplyGDPEffects(gdpMultiplier);
    ApplyUnemploymentEffects(unemploymentRate);
    ApplyInflationEffects(inflationRate);
}
```

## 5. Investment and Financial Markets

### 5.1 Stock Valuation Model

#### Fundamental Valuation
```csharp
public float CalculateStockValue(CompanyComponent company, FinancialComponent financial)
{
    // Discounted Cash Flow (DCF) model
    float expectedGrowthRate = CalculateExpectedGrowth(company);
    float discountRate = GetDiscountRate(company.riskLevel);
    float terminalGrowthRate = 0.02f; // Long-term economic growth
    
    // Free cash flow calculation
    float freeCashFlow = financial.netProfit - financial.capitalExpenditure;
    
    // 5-year DCF valuation
    float presentValue = 0f;
    for (int year = 1; year <= 5; year++)
    {
        float projectedCashFlow = freeCashFlow * Mathf.Pow(1f + expectedGrowthRate, year);
        float discountFactor = Mathf.Pow(1f + discountRate, year);
        presentValue += projectedCashFlow / discountFactor;
    }
    
    // Terminal value
    float terminalCashFlow = freeCashFlow * Mathf.Pow(1f + expectedGrowthRate, 5f);
    float terminalValue = terminalCashFlow * (1f + terminalGrowthRate) / 
                         (discountRate - terminalGrowthRate);
    presentValue += terminalValue / Mathf.Pow(1f + discountRate, 5f);
    
    // Per-share value
    return presentValue / company.sharesOutstanding;
}
```

## 6. Balance Parameters

### 6.1 Difficulty Scaling

#### Progressive Challenge
```csharp
[System.Serializable]
public struct DifficultyParameters
{
    [Header("Early Game (0-6 months)")]
    public float earlyGameAdvantage;       // 1.2x - easier to make profits
    public float marketStability;          // 0.8x - less volatility
    public float competitorAggression;     // 0.5x - AI less aggressive
    
    [Header("Mid Game (6-24 months)")]
    public float normalDifficulty;         // 1.0x - standard parameters
    public float increasedCompetition;     // 1.0x - normal competition
    public float marketEfficiency;         // 1.0x - fair pricing
    
    [Header("Late Game (24+ months)")]
    public float advancedChallenge;        // 0.9x - harder to find opportunities
    public float smarterAI;                // 1.5x - AI learns from player
    public float marketSaturation;         // 1.2x - fewer easy opportunities
}
```

### 6.2 Economic Realism Parameters

#### Real-World Calibration
```yaml
population_parameters:
  income_distribution:
    median_income: 50000      # USD annually
    gini_coefficient: 0.7     # Wealth inequality
    poverty_rate: 0.12        # 12% below poverty line
  
  demographics:
    working_age_ratio: 0.65   # 65% working age
    dependency_ratio: 0.55    # Dependents per worker
    education_premium: 1.8    # Income multiplier for college

company_parameters:
  size_distribution:
    micro_ratio: 0.70         # <10 employees
    small_ratio: 0.25         # 10-50 employees  
    medium_ratio: 0.04        # 50-250 employees
    large_ratio: 0.01         # >250 employees
  
  financial_ratios:
    average_profit_margin: 0.08   # 8% net margin
    debt_to_equity_ratio: 0.4     # 40% leverage
    employee_cost_ratio: 0.35     # 35% of revenue

market_parameters:
  volatility:
    daily_volatility: 0.02        # 2% daily moves
    annual_volatility: 0.20       # 20% annual volatility
    crisis_volatility: 0.50       # 50% during crisis
  
  efficiency:
    price_discovery_speed: 0.1    # 10% adjustment per period
    information_delay: 2.0        # 2 second information lag
```

## 7. Balancing Tools and Monitoring

### 7.1 Real-time Balance Monitoring

#### Key Performance Indicators
```csharp
[System.Serializable]
public struct BalanceMonitoringSystem
{
    [Header("Economic Health")]
    public float targetGDPGrowth;          // 2-4% annually
    public float targetInflation;          // 2% annually
    public float targetUnemployment;       // 5% natural rate
    
    [Header("Player Experience")]
    public float targetWinRate;            // 60% of decisions profitable
    public float targetEngagement;         // Minutes played per session
    public AnimationCurve difficultyCurve; // Challenge progression
    
    [Header("Market Stability")]
    public float maxVolatility;            // 30% maximum volatility
    public float minLiquidity;             // Minimum trading volume
    public float fairValueDeviation;       // Max 20% from fair value
}

public void MonitorBalance()
{
    var metrics = CalculateCurrentMetrics();
    
    if (metrics.gdpGrowth < balanceMonitor.targetGDPGrowth * 0.5f)
    {
        ApplyEconomicStimulus();
    }
    
    if (metrics.marketVolatility > balanceMonitor.maxVolatility)
    {
        ReduceMarketVolatility();
    }
    
    if (metrics.playerWinRate < balanceMonitor.targetWinRate * 0.8f)
    {
        ReduceDifficulty();
    }
}
```

### 7.2 Dynamic Balance Adjustment

#### Adaptive Difficulty System
```csharp
public void AdjustBalance(PlayerPerformanceData performance)
{
    float performanceScore = CalculatePerformanceScore(performance);
    
    // Adjust market conditions based on player success
    if (performanceScore > 0.8f) // Player too successful
    {
        IncreaseCompetition();
        ReduceMarketOpportunities();
        IncreaseEventFrequency();
    }
    else if (performanceScore < 0.4f) // Player struggling
    {
        ProvideMarketOpportunities();
        ReduceRandomEvents();
        ImproveInformationQuality();
    }
}
```

## 8. Testing and Validation

### 8.1 Economic Model Testing

#### Statistical Validation
- **Income Distribution**: Validate Pareto distribution matches real-world data
- **Market Efficiency**: Test price discovery reaches equilibrium
- **Business Cycles**: Verify realistic boom/bust patterns emerge
- **Player Progression**: Confirm satisfying difficulty curve

#### Balance Testing Scenarios
1. **Recession Simulation**: Economy survives 18-month downturn
2. **Inflation Shock**: System adapts to 10% inflation rate
3. **Market Crash**: Recovery within 6-12 months
4. **Player Strategies**: Multiple viable paths to success

### 8.2 Iteration and Refinement

#### Continuous Improvement Process
1. **Data Collection**: Monitor player behavior and economic indicators
2. **Analysis**: Identify imbalances and pain points
3. **Hypothesis**: Propose balance changes
4. **Testing**: A/B test changes with player groups
5. **Implementation**: Deploy successful balance updates

## Next Steps

1. **[Progression System](./progression-system.md)** - Player advancement and unlocks
2. **[AI Behavior Patterns](./ai-behavior-patterns.md)** - AI decision algorithms  
3. **[UI/UX Design](./ui-ux-design.md)** - Interface specifications

## Related Documents

- [Core Gameplay Loop](./core-gameplay-loop.md) - Main gameplay systems
- [Investment Loop Mechanics](./investment-loop-mechanics.md) - Investment system details
- [Implementation Roadmap](../architecture/implementation-roadmap.md) - Technical development plan