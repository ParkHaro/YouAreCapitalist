---
category: gamedesign
tags: [progression, levels, unlock, achievement, milestone]
related: [capitalism-game-design-doc.md, economy-balance-model.md, core-gameplay-loop.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# Progression System

[🇰🇷 Korean Version](./progression-system_KOR.md)

## 📍 Navigation

[↩️ Back to Game Design](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Progression Philosophy

### 1.1 Design Principles

#### Capitalist Learning Curve
- **Progressive Complexity**: Start with simple investments, gradually unlock complex financial instruments
- **Realistic Timeline**: Mirror real capitalist journey from individual investor to empire builder
- **Multiple Pathways**: Allow specialization in different investment strategies
- **Meaningful Milestones**: Each unlock represents genuine progress in capitalist sophistication

#### Player Motivation Framework
- **Achievement Recognition**: Clear feedback for successful capitalist decisions
- **Knowledge Building**: Each level teaches new economic concepts
- **Status Symbols**: Unlock prestigious investments and properties
- **Automation Rewards**: Higher levels offer better automation capabilities

### 1.2 Progression Pillars

#### Capital Growth Progression
- **Net Worth Milestones**: Traditional wealth accumulation markers
- **Cash Flow Achievement**: Passive income generation targets
- **Portfolio Diversification**: Investment type and geographic spread
- **Market Influence**: Ability to affect market conditions

#### Knowledge Progression  
- **Economic Literacy**: Understanding of financial concepts
- **Market Analysis**: Ability to interpret economic indicators
- **Risk Management**: Sophisticated portfolio balancing techniques
- **Strategic Thinking**: Long-term capital allocation planning

## 2. Level Structure

### 2.1 Progression Tiers

#### Tier 1: Individual Investor (Levels 1-10)
**Theme**: Personal wealth building fundamentals
**Duration**: 2-4 weeks typical play time
**Key Learning**: Basic investment principles

```csharp
[System.Serializable]
public struct ProgressionTier
{
    [Header("Tier 1: Individual Investor")]
    public int startLevel;                    // 1
    public int endLevel;                      // 10
    public float requiredCapital;             // $100K - $1M
    public string[] unlockedFeatures;         // Basic stocks, bonds, savings
    public string themeDescription;           // "Personal wealth building"
}
```

#### Tier 2: Portfolio Manager (Levels 11-25) 
**Theme**: Diversified investment strategies
**Duration**: 4-8 weeks typical play time
**Key Learning**: Portfolio theory and risk management

#### Tier 3: Angel Investor (Levels 26-40)
**Theme**: Private equity and startup investments  
**Duration**: 6-12 weeks typical play time
**Key Learning**: Company valuation and growth investing

#### Tier 4: Investment Fund Manager (Levels 41-60)
**Theme**: Managing other people's money
**Duration**: 8-16 weeks typical play time  
**Key Learning**: Fund management and institutional investing

#### Tier 5: Market Maker (Levels 61-80)
**Theme**: Market manipulation and arbitrage
**Duration**: 12-24 weeks typical play time
**Key Learning**: Advanced trading strategies and market psychology

#### Tier 6: Economic Influencer (Levels 81-100)
**Theme**: Systemic market influence
**Duration**: Ongoing end-game content
**Key Learning**: Macroeconomic policy and wealth concentration

### 2.2 Level Requirements Matrix

#### Experience Point Sources
```csharp
[System.Serializable]
public struct ExperienceGainConfig
{
    [Header("Investment Actions")]
    public float profitableTradeXP;          // 10 XP per $1000 profit
    public float portfolioRebalanceXP;       // 50 XP per rebalance
    public float newInvestmentTypeXP;        // 100 XP first time
    
    [Header("Business Activities")]
    public float companyIPOParticipationXP;  // 200 XP per IPO
    public float mergerAcquisitionXP;        // 500 XP per M&A deal
    public float marketInfluenceXP;          // 1000 XP per market event caused
    
    [Header("Knowledge Building")]
    public float economicEventPredictionXP;  // 150 XP correct prediction
    public float marketAnalysisXP;           // 75 XP per analysis completed
    public float tutorialCompletionXP;       // 250 XP per tutorial section
    
    [Header("Automation Mastery")]
    public float automationSetupXP;          // 300 XP per automation rule
    public float passiveIncomeXP;            // 5 XP per $1000 passive income
}
```

#### Leveling Formula
```csharp
public int CalculateRequiredXP(int level)
{
    // Exponential growth with diminishing returns
    float baseXP = 1000f;
    float growthFactor = 1.15f;
    float levelPenalty = level * 50f; // Linear increase
    
    return Mathf.RoundToInt(baseXP * Mathf.Pow(growthFactor, level - 1) + levelPenalty);
}

public ProgressionTier GetCurrentTier(int level)
{
    if (level <= 10) return ProgressionTier.IndividualInvestor;
    if (level <= 25) return ProgressionTier.PortfolioManager;
    if (level <= 40) return ProgressionTier.AngelInvestor;
    if (level <= 60) return ProgressionTier.InvestmentFundManager;
    if (level <= 80) return ProgressionTier.MarketMaker;
    return ProgressionTier.EconomicInfluencer;
}
```

## 3. Unlock System

### 3.1 Investment Instruments Progression

#### Level-Based Unlocks
```csharp
[System.Serializable]
public struct InvestmentUnlockConfig
{
    [Header("Basic Investments (Levels 1-10)")]
    public InvestmentType[] basicInvestments = {
        InvestmentType.SavingsAccount,        // Level 1
        InvestmentType.GovernmentBonds,       // Level 2
        InvestmentType.BlueChipStocks,        // Level 3
        InvestmentType.MutualFunds,           // Level 5
        InvestmentType.IndexFunds,            // Level 7
        InvestmentType.CorporateBonds         // Level 10
    };
    
    [Header("Intermediate Investments (Levels 11-25)")]
    public InvestmentType[] intermediateInvestments = {
        InvestmentType.GrowthStocks,          // Level 12
        InvestmentType.ValueStocks,           // Level 15
        InvestmentType.InternationalFunds,    // Level 18
        InvestmentType.SectorETFs,            // Level 20
        InvestmentType.REITs,                 // Level 22
        InvestmentType.CommodityFunds         // Level 25
    };
    
    [Header("Advanced Investments (Levels 26-40)")]
    public InvestmentType[] advancedInvestments = {
        InvestmentType.PrivateEquity,         // Level 28
        InvestmentType.StartupInvestments,    // Level 30
        InvestmentType.HedgeFunds,           // Level 32
        InvestmentType.VentureCapital,       // Level 35
        InvestmentType.DirectRealEstate,     // Level 38
        InvestmentType.Art_Collectibles      // Level 40
    };
}
```

#### Performance-Based Unlocks
```csharp
[System.Serializable]
public struct PerformanceUnlock
{
    public InvestmentType investmentType;
    public float requiredROI;              // 15% annually
    public int minimumDuration;            // 6 months
    public float riskTolerance;            // Maximum acceptable volatility
    public string unlockDescription;       // "Achieve 15% ROI for 6 months"
}
```

### 3.2 Feature Unlock Progression

#### Automation Features
```csharp
public enum AutomationFeature
{
    BasicRebalancing,        // Level 8  - Simple 60/40 portfolio rebalancing
    DollarCostAveraging,     // Level 12 - Automated regular investments  
    StopLossOrders,          // Level 15 - Risk management automation
    TaxLossHarvesting,       // Level 20 - Tax optimization
    SmartRebalancing,        // Level 25 - Advanced portfolio optimization
    AdvancedScreening,       // Level 30 - AI-powered stock screening
    MarketTimingAlerts,      // Level 35 - Economic indicator automation
    PortfolioInsurance,      // Level 40 - Dynamic hedging strategies
    AlgorithmicTrading,      // Level 50 - Custom trading algorithms
    MarketMaking,            // Level 60 - Provide market liquidity
    SystemicHedging          // Level 75 - Economy-wide risk management
}
```

#### Analysis Tools
```csharp
[System.Serializable]  
public struct AnalysisToolUnlock
{
    [Header("Basic Analysis (Levels 1-15)")]
    public string[] basicTools = {
        "Price Charts",              // Level 1
        "Volume Analysis",           // Level 3  
        "Moving Averages",           // Level 5
        "P/E Ratio Calculator",      // Level 7
        "Dividend Yield Tracker",    // Level 10
        "Sector Performance",        // Level 12
        "Market Cap Analysis"        // Level 15
    };
    
    [Header("Advanced Analysis (Levels 16-40)")]
    public string[] advancedTools = {
        "Technical Indicators",      // Level 18
        "Fundamental Analysis",      // Level 20
        "Risk Metrics",             // Level 22
        "Correlation Analysis",      // Level 25
        "Option Greeks",            // Level 28
        "Monte Carlo Simulation",   // Level 30
        "Scenario Analysis",        // Level 35
        "Macro Economic Indicators" // Level 40
    };
}
```

### 3.3 Prestige and Reputation System

#### Social Status Levels
```csharp
public enum SocialStatus
{
    RetailInvestor,          // 0-$100K net worth
    AccreditedInvestor,      // $1M+ net worth  
    QualifiedPurchaser,      // $5M+ investable assets
    InstitutionalInvestor,   // $25M+ under management
    FamilyOffice,            // $100M+ family wealth
    SovereignWealth,         // $1B+ influence
    EconomicRoyalty          // $10B+ systemic influence
}
```

#### Reputation Benefits
```csharp
[System.Serializable]
public struct ReputationBenefits
{
    [Header("Access Benefits")]
    public float betterDealFlow;           // 20% more investment opportunities
    public float reducedFees;              // 15% lower management fees
    public float earlyInformation;         // 24h advance market intelligence
    
    [Header("Influence Benefits")]
    public float marketImpact;             // Ability to move markets
    public float politicalAccess;          // Influence policy decisions
    public float exclusiveDeals;           // Private placement access
    
    [Header("Automation Benefits")]
    public float smarterAlgorithms;        // Advanced AI trading systems
    public float betterRiskManagement;     // Sophisticated hedging
    public float passiveIncome;            // Higher yield opportunities
}
```

## 4. Achievement System

### 4.1 Achievement Categories

#### Wealth Accumulation Achievements
```csharp
[System.Serializable]
public struct WealthAchievement
{
    public string achievementName;
    public float requiredNetWorth;
    public float timeRequirement;      // Maximum time allowed
    public string rewardDescription;
    public int experienceReward;
    public string unlockBenefit;
}

// Example achievements
private WealthAchievement[] wealthAchievements = {
    new WealthAchievement {
        achievementName = "First $100K",
        requiredNetWorth = 100000f,
        timeRequirement = 3600f,       // 1 hour game time
        experienceReward = 1000,
        unlockBenefit = "Unlock stock market access"
    },
    new WealthAchievement {
        achievementName = "Millionaire Status", 
        requiredNetWorth = 1000000f,
        timeRequirement = 43200f,      // 12 hours game time
        experienceReward = 5000,
        unlockBenefit = "Unlock private equity investments"
    }
};
```

#### Strategic Achievements
```csharp
public enum StrategicAchievement
{
    DiversificationMaster,    // Hold 20+ different asset types
    MarketTimer,             // Correctly predict 5 market turns
    RiskManager,             // Survive 3 market crashes with minimal loss
    ValueInvestor,           // Hold undervalued stocks for 2+ years
    GrowthHacker,            // Achieve 50%+ annual return
    DividendAristocrat,      // Build $10K+ monthly passive income
    ArbitrageExpert,         // Exploit 100+ market inefficiencies
    MarketMaker,             // Provide liquidity in 10+ markets
    EconomicForecaster,      // Predict 10 economic events correctly
    SystemInfluencer         // Cause 5+ market-wide events
}
```

### 4.2 Progress Tracking

#### Achievement Progress System
```csharp
[System.Serializable]
public struct AchievementProgress
{
    public string achievementId;
    public float currentProgress;        // 0.0 to 1.0
    public float[] milestoneValues;      // Interim milestones
    public bool[] milestoneCompleted;    // Track milestone completion
    public DateTime startTime;           // When progress began
    public string[] progressRewards;     // Rewards at each milestone
}

public void UpdateAchievementProgress(string achievementId, float newValue)
{
    var progress = GetAchievementProgress(achievementId);
    
    // Update progress
    progress.currentProgress = newValue;
    
    // Check for milestone completions
    for (int i = 0; i < progress.milestoneValues.Length; i++)
    {
        if (!progress.milestoneCompleted[i] && newValue >= progress.milestoneValues[i])
        {
            progress.milestoneCompleted[i] = true;
            GrantMilestoneReward(achievementId, i);
            ShowMilestoneNotification(achievementId, i);
        }
    }
    
    // Check for full achievement completion
    if (newValue >= 1.0f)
    {
        CompleteAchievement(achievementId);
    }
}
```

## 5. Milestone System

### 5.1 Major Milestones

#### Capital Milestones
```csharp
[System.Serializable]
public struct CapitalMilestone
{
    public string milestoneName;
    public float requiredNetWorth;
    public string significanceDescription;
    public UnlockReward[] rewards;
    public string realWorldContext;        // Educational context
}

private CapitalMilestone[] majorMilestones = {
    new CapitalMilestone {
        milestoneName = "Emergency Fund Established",
        requiredNetWorth = 25000f,
        significanceDescription = "3-6 months expenses saved",
        realWorldContext = "Financial security foundation"
    },
    new CapitalMilestone {
        milestoneName = "Accredited Investor Status",
        requiredNetWorth = 1000000f,
        significanceDescription = "Access to private investments",
        realWorldContext = "SEC definition for sophisticated investors"
    },
    new CapitalMilestone {
        milestoneName = "Ultra-High Net Worth",
        requiredNetWorth = 30000000f,
        significanceDescription = "Family office territory",
        realWorldContext = "Top 0.1% wealth bracket"
    }
};
```

#### Knowledge Milestones
```csharp
public enum KnowledgeMilestone
{
    BasicEconomics,           // Understand supply/demand, inflation, interest rates
    PortfolioTheory,          // Modern portfolio theory, diversification
    TechnicalAnalysis,        // Chart reading, technical indicators  
    FundamentalAnalysis,      // Financial statement analysis
    BehavioralEconomics,      // Market psychology, cognitive biases
    MacroEconomics,           // Central banking, fiscal policy
    AdvancedDerivatives,      // Complex financial instruments
    SystemicRisk,             // Economic crisis understanding
    WealthManagement,         // Tax optimization, estate planning
    MarketMicrostructure      // How markets actually work
}
```

### 5.2 Milestone Rewards

#### Unlock Rewards
```csharp
[System.Serializable]
public struct UnlockReward
{
    public RewardType rewardType;
    public string rewardName;
    public string description;
    public float numericValue;           // For monetary or percentage rewards
    public bool isPermanentUnlock;       // vs temporary bonus
}

public enum RewardType
{
    NewInvestmentType,        // Unlock new investment category
    BetterInformation,        // Earlier/better market data
    ReducedFees,             // Lower transaction costs
    AutomationFeature,        // New automation capability
    AnalysisTool,            // New analysis feature
    SocialStatus,            // Reputation/prestige increase
    SpecialEvent,            // Trigger unique market event
    ExclusiveContent,        // Special education content
    CostReduction,           // Permanent cost savings
    IncomeBonus              // Passive income multiplier
}
```

#### Milestone Celebration System
```csharp
public void CelebrateMilestone(CapitalMilestone milestone)
{
    // Visual celebration
    TriggerConfettiEffect();
    PlayFanfareSound();
    
    // Educational moment
    ShowMilestoneEducation(milestone.realWorldContext);
    
    // Reward distribution
    foreach (var reward in milestone.rewards)
    {
        GrantReward(reward);
    }
    
    // Social sharing
    GenerateShareableAchievement(milestone);
    
    // Progress tracking
    UpdatePlayerProfile(milestone);
}
```

## 6. Difficulty Scaling

### 6.1 Dynamic Difficulty Adjustment

#### Performance-Based Scaling
```csharp
[System.Serializable]
public struct DifficultyScaling
{
    [Header("Player Performance Metrics")]
    public float averageROI;             // Player's historical returns
    public float riskAdjustedReturns;    // Sharpe ratio equivalent
    public float marketTimingAccuracy;   // % correct market predictions
    public float automationEfficiency;   // How well automation performs
    
    [Header("Difficulty Adjustments")]
    public float marketVolatilityMultiplier;  // Increase market chaos
    public float competitionLevel;            // AI player aggressiveness  
    public float informationDelay;            // Reduce information advantage
    public float opportunityFrequency;        // Fewer "easy" opportunities
}

public void AdjustDifficulty(PlayerPerformanceData performance)
{
    float performanceScore = CalculatePerformanceScore(performance);
    
    if (performanceScore > 0.8f) // Player performing too well
    {
        // Make the game more challenging
        IncreaseMarketVolatility(1.2f);
        ReduceInformationAdvantage(0.8f);
        IncreaseCompetition(1.3f);
    }
    else if (performanceScore < 0.4f) // Player struggling
    {
        // Provide more opportunities
        ReduceMarketVolatility(0.8f);
        ProvideEducationalHints();
        CreateMarketOpportunities();
    }
}
```

### 6.2 Level-Appropriate Challenges

#### Challenge Scaling Matrix
```csharp
public struct LevelChallenge
{
    public int levelRange;
    public ChallengeType[] availableChallenges;
    public float difficultyMultiplier;
    public string educationalFocus;
}

private LevelChallenge[] challengeProgression = {
    new LevelChallenge {
        levelRange = 1-10,
        availableChallenges = { 
            ChallengeType.SimpleInvesting,
            ChallengeType.BudgetManagement,
            ChallengeType.SavingsGoals
        },
        difficultyMultiplier = 0.8f,
        educationalFocus = "Basic financial literacy"
    },
    new LevelChallenge {
        levelRange = 40-60,
        availableChallenges = {
            ChallengeType.MarketCrash,
            ChallengeType.GeopoliticalEvents,
            ChallengeType.CurrencyDevaluation
        },
        difficultyMultiplier = 1.3f,
        educationalFocus = "Advanced risk management"
    }
};
```

## 7. Tutorial Integration

### 7.1 Progressive Tutorial System

#### Just-in-Time Learning
```csharp
[System.Serializable]
public struct TutorialTrigger
{
    public int triggerLevel;
    public InvestmentType newUnlock;
    public string tutorialContent;
    public bool isOptional;
    public int experienceReward;
    public float knowledgePoints;
}

public void OnInvestmentUnlocked(InvestmentType investmentType)
{
    var tutorial = GetTutorialForInvestment(investmentType);
    
    if (tutorial != null && ShouldShowTutorial(tutorial))
    {
        ShowInteractiveTutorial(tutorial);
        
        // Track tutorial engagement
        RecordTutorialStart(tutorial.tutorialId);
        
        // Reward completion
        OnTutorialCompleted += (id) => {
            if (id == tutorial.tutorialId)
            {
                GrantExperience(tutorial.experienceReward);
                AddKnowledgePoints(tutorial.knowledgePoints);
            }
        };
    }
}
```

### 7.2 Knowledge Progression

#### Economic Education Framework
```csharp
public enum EducationalTopic
{
    TimeValueOfMoney,         // Compound interest basics
    RiskVsReturn,            // Investment fundamentals  
    Diversification,         // Portfolio theory
    MarketEfficiency,        // How prices are set
    EconomicIndicators,      // GDP, inflation, unemployment
    CentralBankingPolicy,    // Interest rates, money supply
    BehavioralBias,          // Psychological investing mistakes
    TaxOptimization,         // Tax-efficient investing
    AssetAllocation,         // Strategic portfolio construction
    AlternativeInvestments,  // Private equity, hedge funds
    DerivativesBasics,       // Options, futures, swaps
    CreditRisk,              // Bond and lending risk
    InflationHedging,        // Protecting purchasing power
    GlobalMarkets,           // International investing
    QuantitativeAnalysis     // Mathematical modeling
}
```

## 8. Endgame Progression

### 8.1 Post-Level 100 Content

#### Prestige System
```csharp
[System.Serializable]
public struct PrestigeLevel
{
    public int prestigeLevel;            // 1-10 prestige levels
    public float requiredNetWorth;       // Increasing thresholds
    public string prestigeTitle;         // "Economic Titan", "Market God"
    public Color titleColor;             // Visual distinction
    public float globalInfluence;        // Ability to affect world economy
    public PrestigeBenefit[] benefits;   // Permanent bonuses
}
```

#### Legacy Building
```csharp
public enum LegacyAchievement
{
    FoundationBuilder,        // Establish charitable foundation
    MarketCreator,           // Create new financial markets
    EconomicTheory,          // Develop new investment strategies
    MentorshipProgram,       // Teach other players
    SystemicChange,          // Influence global economic policy
    WealthDynasty,           // Multi-generational wealth transfer
    PhilanthropicImpact,     // Solve major world problems
    EconomicStability,       // Prevent/mitigate financial crises
    InnovationSponsor,       // Fund breakthrough technologies
    SocialEntrepreneur       // Create sustainable business models
}
```

### 8.2 Infinite Progression

#### Paragon Levels
```csharp
public struct ParagonProgression
{
    public int paragonLevel;             // Unlimited progression
    public ParagonCategory category;     // Specialization focus
    public float bonusMultiplier;        // Small incremental benefits
    public int requiredParagonXP;        // Exponential XP requirements
}

public enum ParagonCategory
{
    WealthAccumulation,      // +1% to all investment returns
    RiskManagement,          // +2% crisis resistance
    MarketTiming,            // +3% prediction accuracy  
    AutomationEfficiency,    // +1% automation performance
    GlobalInfluence,         // +5% market impact
    KnowledgeRetention,      // +10% tutorial effectiveness
    SocialStatus,            // +15% reputation gains
    LegacyBuilding           // +20% philanthropy impact
}
```

## 9. Measurement and Analytics

### 9.1 Progression Metrics

#### Player Engagement Tracking
```csharp
[System.Serializable]
public struct ProgressionAnalytics
{
    [Header("Engagement Metrics")]
    public float averageSessionLength;    // Minutes per session
    public float levelCompletionTime;     // Time between level ups
    public float featureAdoptionRate;     // % of unlocks actually used
    public float tutorialCompletionRate;  // Educational engagement
    
    [Header("Difficulty Metrics")]
    public float playerWinRate;          // % of profitable decisions
    public float ragequitRate;           // % players stopping at level
    public float difficultyRating;       // Player-reported challenge
    public float learningCurve;          // Knowledge acquisition speed
    
    [Header("Monetization Metrics")]
    public float timeToFirstPurchase;    // Premium feature adoption
    public float lifetimeValue;          // Total player spending
    public float retentionRate;          // 30-day player retention
    public float recommendationScore;    // Net promoter score
}
```

### 9.2 Balance Testing

#### A/B Test Framework
```csharp
public struct ProgressionTest
{
    public string testName;
    public float testGroupRatio;         // 10% of players
    public ProgressionVariable variable; // What we're testing
    public float baselineValue;          // Current value
    public float testValue;              // New value to test
    public string successMetric;         // How we measure success
    public float minimumSampleSize;      // Statistical significance
}

public void RunProgressionTest(string testName)
{
    var test = GetProgressionTest(testName);
    var playerGroup = AssignPlayerToTestGroup(test.testGroupRatio);
    
    if (playerGroup == TestGroup.Experimental)
    {
        ApplyTestParameters(test);
        TrackTestMetrics(test.successMetric);
    }
    
    // Analyze results after minimum sample size reached
    if (GetTestSampleSize(testName) >= test.minimumSampleSize)
    {
        AnalyzeTestResults(testName);
        MakeBalanceDecision(testName);
    }
}
```

## Next Steps

1. **[AI Behavior Patterns](./ai-behavior-patterns.md)** - AI decision-making algorithms
2. **[UI/UX Design](./ui-ux-design.md)** - Interface design specifications
3. **[Tutorial Onboarding](./tutorial-onboarding.md)** - Learning system design

## Related Documents

- [Economy Balance Model](./economy-balance-model.md) - Economic balancing parameters
- [Core Gameplay Loop](./core-gameplay-loop.md) - Main gameplay systems
- [Investment Loop Mechanics](./investment-loop-mechanics.md) - Investment system details