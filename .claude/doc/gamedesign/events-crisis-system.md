---
category: gamedesign
tags: [events, crisis, random-events, black-swan, economic-cycles]
related: [economy-balance-model.md, ai-behavior-patterns.md, capitalism-game-design-doc.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# Events and Crisis System

[🇰🇷 Korean Version](./events-crisis-system_KOR.md)

## 📍 Navigation

[↩️ Back to Game Design](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Event System Philosophy

### 1.1 Design Principles

#### Realistic Economic Dynamics
- **Historical Accuracy**: Events based on real economic phenomena
- **Interconnected Systems**: Events cascade through economy realistically
- **Player Agency**: Events create opportunities and challenges, not arbitrary punishment
- **Educational Value**: Each event teaches real economic concepts

#### Engagement and Challenge
- **Meaningful Choices**: Player decisions during events have lasting consequences
- **Risk and Opportunity**: Events create both threats and investment opportunities
- **Strategic Depth**: Advanced players can predict and prepare for certain events
- **Emotional Investment**: Events create memorable moments and stories

### 1.2 Event Classification System

#### Event Categories by Impact Scale
```csharp
[System.Serializable]
public enum EventScale
{
    Personal,        // Affects individual companies (earnings announcement)
    Sectoral,        // Affects industry sectors (regulatory changes)
    National,        // Affects entire country (interest rate changes)
    Regional,        // Affects geographic regions (trade wars)
    Global,          // Affects world economy (pandemic, war)
    Systemic         // Threatens entire financial system (2008 crisis)
}

[System.Serializable]
public enum EventType
{
    // Regular Market Events
    EarningsReport,      // Quarterly company earnings
    ProductLaunch,       // New product announcements
    ManagementChange,    // CEO/leadership changes
    
    // Economic Events
    InterestRateChange,  // Central bank rate decisions
    InflationReport,     // CPI/inflation announcements
    GDPReport,          // Economic growth data
    UnemploymentData,    // Job market statistics
    
    // Political Events
    ElectionResults,     // Political leadership changes
    PolicyAnnouncement,  // New government policies
    TradeAgreement,      // International trade deals
    RegulatoryChange,    // New regulations
    
    // Crisis Events
    BankingCrisis,       // Financial institution failures
    CurrencyDevaluation, // Currency collapse
    NaturalDisaster,     // Weather/geological events
    GeopoliticalTension, // Wars, sanctions, conflicts
    
    // Black Swan Events
    Pandemic,            // Global health crisis
    TechnologicalDisruption, // Revolutionary technology
    SystemicFailure,     // Infrastructure collapse
    UnpredictableShock   // Truly random major event
}
```

#### Event Frequency Distribution
```csharp
[System.Serializable]
public struct EventFrequencyConfig
{
    [Header("Regular Events")]
    public float dailyEventProbability;     // 0.3 - 30% chance daily
    public float weeklyEventProbability;    // 0.8 - 80% chance weekly
    public float monthlyEventProbability;   // 0.95 - 95% chance monthly
    
    [Header("Crisis Events")]
    public float minorCrisisProbability;    // 0.1 - 10% chance monthly
    public float majorCrisisProbability;    // 0.02 - 2% chance monthly
    public float systemicCrisisProbability; // 0.005 - 0.5% chance monthly
    
    [Header("Black Swan Events")]
    public float blackSwanProbability;      // 0.001 - 0.1% chance monthly
    public int blackSwanCooldownMonths;     // 12 months minimum between
    public bool enableConsecutiveEvents;    // Allow multiple crises
}
```

## 2. Regular Economic Events

### 2.1 Market Cycle Events

#### Business Cycle Integration
```csharp
[System.Serializable]
public struct BusinessCycleEvents
{
    [Header("Expansion Phase Events")]
    public CyclicalEvent[] expansionEvents = {
        new CyclicalEvent {
            eventName = "Strong GDP Growth",
            description = "Economy grows 4.2% year-over-year",
            marketImpact = MarketImpact.Positive,
            sectors = new[] { "Technology", "Consumer Discretionary" },
            probability = 0.4f,
            durationDays = 90
        },
        new CyclicalEvent {
            eventName = "Low Unemployment",
            description = "Unemployment drops to 3.5%",
            marketImpact = MarketImpact.Mixed,
            sectors = new[] { "All" },
            probability = 0.3f,
            durationDays = 180
        }
    };
    
    [Header("Peak Phase Events")]
    public CyclicalEvent[] peakEvents = {
        new CyclicalEvent {
            eventName = "Asset Bubble Warning",
            description = "Central bank warns of overvalued assets",
            marketImpact = MarketImpact.Negative,
            sectors = new[] { "Real Estate", "Technology" },
            probability = 0.6f,
            durationDays = 30
        }
    };
    
    [Header("Contraction Phase Events")]
    public CyclicalEvent[] contractionEvents = {
        new CyclicalEvent {
            eventName = "Rising Unemployment",
            description = "Unemployment increases to 7.2%",
            marketImpact = MarketImpact.Negative,
            sectors = new[] { "Consumer Discretionary", "Retail" },
            probability = 0.5f,
            durationDays = 120
        }
    };
}
```

#### Seasonal Economic Patterns
```csharp
[System.Serializable]
public struct SeasonalEvents
{
    [Header("Quarterly Patterns")]
    public SeasonalEvent[] quarterlyEvents;  // Q4 retail surge, Q1 slowdown
    public bool enableSeasonalVolatility;   // Higher volatility in certain periods
    
    [Header("Annual Patterns")]
    public SeasonalEvent[] annualEvents;     // Tax season, holiday spending
    public bool enableYearEndEffects;       // December portfolio rebalancing
    
    [Header("Holiday Effects")]
    public HolidayEvent[] holidayEvents;     // Christmas, Black Friday
    public bool enableHolidayTrading;       // Reduced volume during holidays
}

public struct SeasonalEvent
{
    public string eventName;               // "Holiday Shopping Season"
    public MonthRange activeMonths;        // November-December
    public SectorImpact[] sectorImpacts;   // How different sectors are affected
    public float volatilityMultiplier;     // 1.2x normal volatility
    public string educationalNote;         // Explain why this happens
}
```

### 2.2 Corporate Events

#### Company-Specific Events
```csharp
[System.Serializable]
public struct CorporateEventSystem
{
    [Header("Earnings Events")]
    public EarningsEventConfig earningsConfig;
    public bool enableEarningsSurprises;    // Unexpected results
    public float earningsBeatProbability;   // 60% chance to beat estimates
    
    [Header("Management Events")]
    public ManagementEventConfig managementConfig;
    public bool enableSuccessionPlanning;  // CEO retirement announcements
    public bool enableScandals;            // Corporate governance issues
    
    [Header("Product Events")]
    public ProductEventConfig productConfig;
    public bool enableInnovationBreakthroughs; // Revolutionary products
    public bool enableProductRecalls;      // Product safety issues
}

public struct EarningsEvent
{
    public CompanyComponent company;       // Which company reports
    public float expectedEPS;              // Wall Street consensus
    public float actualEPS;                // Actual reported earnings
    public float revenueGrowth;            // Year-over-year growth
    public EarningsQuality quality;        // Quality of earnings
    public string[] keyHighlights;         // Management commentary
    public float stockImpact;              // Expected stock price reaction
}

public void ProcessEarningsAnnouncement(EarningsEvent earnings)
{
    var company = earnings.company;
    
    // Calculate earnings surprise
    float surprise = (earnings.actualEPS - earnings.expectedEPS) / earnings.expectedEPS;
    
    // Determine market reaction
    float stockReaction = CalculateStockReaction(surprise, earnings.quality, earnings.revenueGrowth);
    
    // Apply stock price change
    company.stockPrice *= (1f + stockReaction);
    
    // Update fundamental metrics
    company.financials.earningsPerShare = earnings.actualEPS;
    company.financials.peRatio = company.stockPrice / earnings.actualEPS;
    
    // Sector sympathy/contagion effects
    ApplySectorEffects(company.industry, stockReaction * 0.3f);
    
    // Generate news and player notifications
    CreateEarningsNews(earnings, stockReaction);
}
```

#### Merger and Acquisition Events
```csharp
[System.Serializable]
public struct MergerAcquisitionSystem
{
    [Header("M&A Probability")]
    public float monthlyMAprob;            // 2% chance per company per month
    public CompanySize[] targetSizes;      // Usually smaller companies
    public Industry[] activeIndustries;    // Tech, Healthcare consolidation
    
    [Header("Deal Structure")]
    public MAStructure[] dealTypes;        // Cash, Stock, Mixed
    public float premiumRange;             // 20-50% premium to market price
    public bool enableHostileOffers;       // Unsolicited takeover bids
    
    [Header("Regulatory Approval")]
    public float approvalProbability;      // 85% deals get approved
    public int approvalTimeMonths;         // 6-18 months approval process
    public bool enableAntitrustBlocking;   // Large deals may be blocked
}

public struct MAEvent
{
    public CompanyComponent acquirer;      // Company making the offer
    public CompanyComponent target;        // Company being acquired
    public float offerPrice;               // Price per share offered
    public float premiumPercent;           // Premium over market price
    public MAStructure structure;          // How deal is structured
    public float completionProbability;   // Likelihood deal completes
    public int expectedCompletionDays;     // Time to completion
    public string strategicRationale;      // Why this acquisition makes sense
}
```

## 3. Crisis Events

### 3.1 Financial Crises

#### Banking Crisis Simulation
```csharp
[System.Serializable]
public struct BankingCrisisConfig
{
    [Header("Crisis Triggers")]
    public CrisisTrigger[] triggers = {
        new CrisisTrigger {
            triggerName = "Real Estate Bubble Burst",
            description = "Housing prices fall 30% in 6 months",
            probability = 0.05f,    // 5% chance during peak phases
            severity = CrisisSeverity.Major
        },
        new CrisisTrigger {
            triggerName = "Major Bank Failure",
            description = "Large regional bank becomes insolvent",
            probability = 0.02f,    // 2% chance during stress
            severity = CrisisSeverity.Severe
        }
    };
    
    [Header("Crisis Progression")]
    public CrisisPhase[] phases;           // How crisis unfolds over time
    public bool enableContagionEffects;   // Crisis spreads between institutions
    public bool enableGovernmentResponse; // Bailouts, FDIC insurance
    
    [Header("Market Impact")]
    public float creditSpreadIncrease;     // +500 basis points during crisis
    public float stockMarketDecline;       // -40% peak to trough
    public float volatilityMultiplier;     // 3x normal volatility
}

public struct BankingCrisisEvent
{
    public string crisisName;              // "Subprime Mortgage Crisis 2.0"
    public CrisisTrigger trigger;          // What started the crisis
    public CrisisPhase currentPhase;       // Current stage of crisis
    public int daysInProgress;             // How long crisis has lasted
    public float marketStressLevel;        // 0-1 stress indicator
    public BankFailure[] bankFailures;     // Which banks have failed
    public GovernmentResponse[] responses; // Policy responses implemented
}

public void ProcessBankingCrisis(BankingCrisisEvent crisis)
{
    // Update market stress indicators
    UpdateMarketStress(crisis.marketStressLevel);
    
    // Apply sector-specific impacts
    ApplySectorImpacts(new Dictionary<Industry, float> {
        { Industry.Finance, -0.15f },      // Banking sector hit hardest
        { Industry.RealEstate, -0.12f },   // Real estate also severely affected
        { Industry.Construction, -0.10f },  // Construction follows real estate
        { Industry.Technology, -0.05f },    // Tech relatively resilient
        { Industry.Healthcare, -0.02f }     // Defensive sectors hold up better
    });
    
    // Credit market effects
    IncreaseCreditSpreads(crisis.marketStressLevel * 5.0f); // 5% max increase
    ReduceCreditAvailability(crisis.marketStressLevel);
    
    // Flight to quality
    IncreaseGovernmentBondDemand();
    DecreaseCorporateBondDemand();
    
    // Generate crisis-specific investment opportunities
    CreateDistressedDebtOpportunities();
    CreateBankStockBargains(); // For brave bottom-fishers
}
```

#### Currency Crisis Events
```csharp
[System.Serializable]
public struct CurrencyCrisisConfig
{
    [Header("Crisis Conditions")]
    public float currentAccountDeficit;    // >5% of GDP trigger
    public float inflationRate;            // >10% annual inflation
    public float debtToGDPratio;          // >90% debt/GDP ratio
    public float politicalStabilityIndex; // Political risk factor
    
    [Header("Crisis Mechanisms")]
    public bool enableSpeculativeAttacks; // George Soros style attacks
    public bool enableCapitalFlightModeling; // Money fleeing country
    public bool enableCentralBankIntervention; // CB defending currency
    
    [Header("Global Contagion")]
    public bool enableContagionEffects;   // Crisis spreads to similar countries
    public float contagionProbability;    // 30% chance of spreading
    public string[] vulnerableCountries;  // Countries at risk
}
```

### 3.2 Market Crashes

#### Stock Market Crash Simulation
```csharp
[System.Serializable]
public struct MarketCrashConfig
{
    [Header("Crash Triggers")]
    public CrashTrigger[] crashTriggers = {
        new CrashTrigger {
            name = "Algorithmic Trading Malfunction",
            description = "High-frequency trading algorithms malfunction, causing flash crash",
            probability = 0.01f,
            severity = CrashSeverity.Moderate,
            duration = 1 // 1 day flash crash
        },
        new CrashTrigger {
            name = "Geopolitical Shock",
            description = "Major geopolitical crisis sparks investor panic",
            probability = 0.03f,
            severity = CrashSeverity.Severe,
            duration = 30 // 30 day bear market
        }
    };
    
    [Header("Crash Characteristics")]
    public AnimationCurve crashProgression; // How crash unfolds over time
    public float maxDrawdown;              // -50% maximum decline
    public bool enableCircuitBreakers;     // Trading halts during crash
    public bool enableVolatilitySpikes;    // VIX spikes to 80+
    
    [Header("Recovery Patterns")]
    public RecoveryPattern[] recoveryTypes; // V-shape, U-shape, L-shape
    public float averageRecoveryMonths;    // 18 months average recovery
    public bool enableDeadCatBounce;       // False recoveries during crash
}

public struct MarketCrashEvent
{
    public string crashName;               // "Black Monday III"
    public CrashTrigger trigger;           // What caused the crash
    public int daysSinceCrashStart;       // Crash duration
    public float currentDrawdown;          // Current decline from peak
    public float volatilityIndex;         // VIX equivalent
    public bool[] circuitBreakersTriggered; // Which trading halts occurred
    public SectorPerformance[] sectorPerformance; // How each sector performed
    public RecoverySignals recoverySignals; // Signs of potential recovery
}

public void SimulateMarketCrash(MarketCrashEvent crash)
{
    var crashDay = crash.daysSinceCrashStart;
    
    // Calculate daily market movement based on crash progression
    float dailyReturn = crash.trigger.crashProgression.Evaluate(crashDay / crash.trigger.duration);
    
    // Apply market-wide decline
    ApplyMarketDecline(dailyReturn);
    
    // Sector rotation during crash
    ApplyCrashSectorEffects(crash.sectorPerformance);
    
    // Volatility explosion
    UpdateVolatilityIndex(crash.volatilityIndex);
    
    // Liquidity crunch
    ReduceMarketLiquidity(crash.currentDrawdown);
    
    // Flight to safety
    CreateFlightToSafetyMoves();
    
    // Opportunity creation
    if (crash.currentDrawdown > 0.2f) // 20%+ decline
    {
        CreateValueInvestmentOpportunities();
        EnableDollarCostAveragingBenefits();
    }
    
    // Check for recovery signals
    MonitorRecoverySignals(ref crash.recoverySignals);
}
```

### 3.3 Sector-Specific Crises

#### Technology Bubble Burst
```csharp
[System.Serializable]
public struct TechBubbleConfig
{
    [Header("Bubble Indicators")]
    public float techSectorPEratio;        // >50 P/E ratio warning
    public float ipoActivity;              // Excessive IPO volume
    public float speculativeInvestment;    // Meme stock activity
    public float marginTradingLevel;       // High leverage usage
    
    [Header("Burst Mechanics")]
    public BubbleTrigger[] burstTriggers;  // What pops the bubble
    public float techSectorDecline;        // -70% sector decline
    public int bubbleBurstDuration;        // 18 months burst period
    
    [Header("Sector Effects")]
    public TechSubsectorImpact[] subsectorImpacts; // Different tech areas
    public bool enableFundamentalSort;     // Strong companies survive better
    public bool enableFlightToQuality;     // Money moves to profitable companies
}

public struct TechBubbleBurst
{
    public string bubbleName;              // "AI Bubble Burst"
    public BubbleTrigger trigger;          // Interest rate hike, regulation
    public TechSubsector[] affectedAreas;  // Cloud, AI, Crypto, etc.
    public float[] sectorDeclines;         // Decline by subsector
    public int daysSinceBurst;            // Duration of burst
    public CompanyCategory[] survivors;    // Which companies weather the storm
    public InvestmentOpportunity[] opportunities; // Bottom-fishing chances
}
```

## 4. Black Swan Events

### 4.1 Unpredictable Shocks

#### Pandemic Simulation
```csharp
[System.Serializable]
public struct PandemicEventConfig
{
    [Header("Pandemic Characteristics")]
    public string pandemicName;            // "COVID-19", "Bird Flu H5N1"
    public float mortalityRate;            // Case fatality rate
    public float transmissionRate;         // R0 reproduction number
    public int incubationPeriod;          // Days before symptoms
    
    [Header("Economic Impact")]
    public LockdownSeverity lockdownLevel; // Government response severity
    public Industry[] essentialSectors;   // Sectors allowed to operate
    public float supplyChainDisruption;   // % of normal supply chain function
    public float consumerSpendingDecline; // % reduction in spending
    
    [Header("Market Response")]
    public float initialMarketPanic;       // -30% immediate decline
    public SectorResilience[] sectorResilience; // Which sectors survive
    public TechnologyAdoption[] acceleratedTech; // Digital transformation
    public PolicyResponse[] governmentResponses; // Fiscal/monetary policy
}

public struct PandemicEvent
{
    public string name;                    // Pandemic identifier
    public int daysSinceOutbreak;         // Duration
    public float currentSeverity;         // Current impact level (0-1)
    public LockdownStatus[] regionLockdowns; // Lockdown status by region
    public EconomicMetrics impactMetrics; // GDP, unemployment effects
    public VaccineProgress vaccineStatus; // Vaccine development progress
    public MarketAdaptation[] adaptations; // How markets adapted
}

public void SimulatePandemicImpact(PandemicEvent pandemic)
{
    var day = pandemic.daysSinceOutbreak;
    
    // Initial panic phase (days 1-30)
    if (day <= 30)
    {
        ApplyPanicSelling();
        SpikeCommodityPrices(new[] { "Gold", "Silver", "Food" });
        CrashTravelSectors();
        BoostTechnologySectors();
    }
    
    // Adaptation phase (days 31-200)
    else if (day <= 200)
    {
        AccelerateDigitalTransformation();
        CreateNewBusinessModels();
        ShiftConsumerBehavior();
        ImplementGovernmentSupport();
    }
    
    // Recovery phase (days 200+)
    else
    {
        BeginEconomicRecovery();
        RestoreSupplyChains();
        AnalyzePermanentChanges();
        CreatePostPandemicOpportunities();
    }
    
    // Update affected sectors
    foreach (var sector in pandemic.impactMetrics.sectorImpacts)
    {
        ApplySectorImpact(sector.industry, sector.impactLevel);
    }
}
```

#### Technological Disruption Events
```csharp
[System.Serializable]
public struct TechDisruptionConfig
{
    [Header("Disruption Types")]
    public DisruptionType[] disruptionTypes = {
        new DisruptionType {
            name = "Artificial General Intelligence",
            description = "AGI breakthrough revolutionizes all industries",
            probability = 0.001f,
            impactMagnitude = 1.0f,
            affectedSectors = new[] { "All" }
        },
        new DisruptionType {
            name = "Quantum Computing Breakthrough",
            description = "Quantum supremacy breaks current encryption",
            probability = 0.005f,
            impactMagnitude = 0.8f,
            affectedSectors = new[] { "Technology", "Finance", "Defense" }
        }
    };
    
    [Header("Adoption Curve")]
    public AdoptionPhase[] phases;         // Research, Development, Deployment, Mass Adoption
    public float adoptionSpeed;            // How quickly disruption spreads
    public bool enableNetworkEffects;     // Faster adoption due to network effects
    
    [Header("Market Response")]
    public CreativeDestruction creativeDestruction; // Schumpeter's concept
    public bool enableWinnerTakeAll;      // Platform effects
    public float valuationMultipliers;    // How much winning companies appreciate
}
```

### 4.2 Geopolitical Shocks

#### War and Conflict Simulation
```csharp
[System.Serializable]
public struct GeopoliticalCrisisConfig
{
    [Header("Crisis Types")]
    public CrisisType[] crisisTypes = {
        new CrisisType {
            name = "Trade War Escalation",
            description = "Major trading partners impose heavy tariffs",
            probability = 0.1f,
            duration = 180,    // 6 months
            globalImpact = 0.6f
        },
        new CrisisType {
            name = "Regional Military Conflict",
            description = "Armed conflict in strategically important region",
            probability = 0.05f,
            duration = 360,    // 12 months
            globalImpact = 0.8f
        }
    };
    
    [Header("Economic Weapons")]
    public bool enableSanctions;           // Economic sanctions
    public bool enableCommodityWeapons;    // Oil/gas as weapons
    public bool enableCyberWarfare;        // Attacks on financial systems
    public bool enableCurrencyManipulation; // Competitive devaluations
    
    [Header("Market Effects")]
    public CommodityImpact[] commodityEffects; // Oil, gas, grain prices
    public RegionalImpact[] regionalEffects;   // Geographic impact variations
    public SafeHavenDemand safeHavenEffects;  // Flight to safe assets
}

public struct GeopoliticalShock
{
    public string eventName;               // "Ukraine-Russia Conflict"
    public CrisisType crisisType;          // Type of geopolitical event
    public string[] involvedCountries;     // Primary participants
    public int daysInProgress;            // Duration of crisis
    public float intensityLevel;          // Current crisis intensity (0-1)
    public CommodityPrice[] commodityPrices; // Affected commodity prices
    public SafeHavenFlow[] capitalFlows;   // Flight to safety patterns
    public SanctionImpact[] sanctions;     // Economic sanctions in effect
}
```

## 5. Event Response System

### 5.1 Player Decision Framework

#### Crisis Decision Points
```csharp
[System.Serializable]
public struct CrisisDecisionSystem
{
    [Header("Decision Triggers")]
    public DecisionTrigger[] triggers;     // When to prompt player decisions
    public float decisionTimeLimit;        // 24 hours to decide
    public bool enableDelayedConsequences; // Decisions have long-term effects
    
    [Header("Decision Categories")]
    public CrisisDecision[] portfolioDecisions; // Buy, sell, hold decisions
    public CrisisDecision[] riskDecisions;     // Hedge, leverage, derisk
    public CrisisDecision[] opportunityDecisions; // Contrarian investments
    
    [Header("Information Availability")]
    public InformationQuality infoQuality; // How much player knows
    public bool enableRealTimeInfo;        // Updates during decision period
    public bool enableExpertAnalysis;      // AI advisor recommendations
}

public struct CrisisDecision
{
    public string decisionName;            // "Sell Everything and Go to Cash"
    public string description;             // Decision explanation
    public DecisionConsequence[] consequences; // Potential outcomes
    public float difficultyLevel;          // How hard to predict outcome
    public string educationalNote;         // What this teaches about investing
}

public void PresentCrisisDecision(CrisisEvent crisis, Player player)
{
    var decisions = GenerateApplicableDecisions(crisis, player.portfolio);
    
    // Filter decisions based on player level and experience
    var levelAppropriate = FilterByPlayerLevel(decisions, player.level);
    
    // Present decision interface
    ShowDecisionInterface(crisis, levelAppropriate);
    
    // Start decision timer
    StartDecisionTimer(crisis.decisionTimeLimit);
    
    // Provide decision support tools
    EnableDecisionSupportTools(crisis, player);
}
```

#### Opportunity Recognition System
```csharp
[System.Serializable]
public struct OpportunityRecognitionConfig
{
    [Header("Opportunity Types")]
    public OpportunityType[] opportunityTypes = {
        new OpportunityType {
            name = "Value Investing Opportunity",
            description = "High-quality companies trading at discounts",
            triggerEvents = new[] { "Market Crash", "Sector Rotation" },
            difficultyLevel = 0.3f,    // Relatively easy to spot
            potentialReturn = 2.0f     // 100% potential return
        },
        new OpportunityType {
            name = "Distressed Debt Investment",
            description = "Bonds of troubled companies at deep discounts",
            triggerEvents = new[] { "Banking Crisis", "Corporate Bankruptcies" },
            difficultyLevel = 0.8f,    // Advanced strategy
            potentialReturn = 3.0f     // 200% potential return
        }
    };
    
    [Header("Recognition Mechanics")]
    public bool enableHints;               // Give players hints about opportunities
    public bool adaptHintsByLevel;         // More hints for beginners
    public float hintDelay;               // 3 days before showing hints
    
    [Header("Execution Challenges")]
    public bool requireResearch;           // Must research before investing
    public bool simulateExecutionRisk;    // Not all opportunities work out
    public float averageSuccessRate;       // 60% of opportunities succeed
}
```

### 5.2 Event Learning System

#### Post-Event Analysis
```csharp
[System.Serializable]
public struct EventEducationSystem
{
    [Header("Analysis Tools")]
    public bool enablePostEventAnalysis;   // Detailed event retrospective
    public bool showPlayerPerformance;     // How player performed vs market
    public bool compareToHistorical;       // Compare to real historical events
    
    [Header("Learning Content")]
    public EducationalContent[] lessons;   // What each event teaches
    public bool enableInteractiveReview;   // Interactive lesson review
    public bool assessLearning;           // Quiz player on concepts
    
    [Header("Skill Development")]
    public SkillProgression[] skillGains; // Which skills improved
    public bool enableReflectiveExercise; // Self-reflection on decisions
    public bool trackDecisionQuality;     // Measure decision-making improvement
}

public struct EventEducation
{
    public string eventName;              // Event being analyzed
    public string[] keyLessons;           // Main learning points
    public PlayerDecisionAnalysis[] playerDecisions; // Analysis of player choices
    public string historicalParallel;     // Similar real-world event
    public string[] expertInsights;       // Professional investor perspectives
    public SkillGain[] skillsLearned;     // Quantified skill improvements
}
```

## 6. Event Generation Engine

### 6.1 Dynamic Event Creation

#### Procedural Event Generation
```csharp
[System.Serializable]
public struct ProceduralEventEngine
{
    [Header("Generation Parameters")]
    public EventTemplate[] eventTemplates; // Base templates for events
    public bool enableDynamicNaming;       // Generate unique event names
    public bool enableParameterVariation;  // Vary event characteristics
    
    [Header("Realism Constraints")]
    public RealismCheck[] realismChecks;   // Ensure events make sense
    public bool enableHistoricalValidation; // Check against historical data
    public bool preventImpossibleEvents;   // No contradictory events
    
    [Header("Player Adaptation")]
    public bool adaptToPlayerSkill;        // Harder events for better players
    public bool preventRepetition;         // Don't repeat same events too often
    public bool maintainEducationalValue;  // Each event teaches something
}

public struct EventTemplate
{
    public string templateName;            // "Corporate Scandal Template"
    public ParameterRange[] parameters;    // Variable parameters
    public string[] narrativeElements;     // Story components
    public LearningObjective[] objectives; // What this event teaches
    public float complexityLevel;          // 0.1 to 1.0 complexity
}
```

#### Market Condition Response
```csharp
[System.Serializable]
public struct MarketConditionEngine
{
    [Header("Condition Monitoring")]
    public MarketIndicator[] indicators;   // VIX, yield curve, sentiment
    public bool enablePredictiveModeling;  // Predict likely events
    public float reactionSensitivity;      // How quickly markets react
    
    [Header("Event Chaining")]
    public bool enableEventChains;         // Events trigger other events
    public ChainProbability[] chainRules;  // Rules for event sequences
    public int maxChainLength;            // Maximum 5 events in chain
    
    [Header("Equilibrium Restoration")]
    public bool enableMeanReversion;       // Markets return to normal
    public float reversionSpeed;           // How quickly markets normalize
    public bool enableOvershoot;           // Markets overshoot equilibrium
}
```

### 6.2 Historical Event Recreation

#### Real-World Event Database
```csharp
[System.Serializable]
public struct HistoricalEventDatabase
{
    [Header("Event Categories")]
    public HistoricalEvent[] stockMarketCrashes; // 1929, 1987, 2000, 2008
    public HistoricalEvent[] inflationCrises;    // 1970s stagflation
    public HistoricalEvent[] currencyCrises;     // Asian Financial Crisis
    public HistoricalEvent[] geopoliticalEvents; // Gulf War, 9/11
    
    [Header("Recreation Settings")]
    public bool enableHistoricalMode;     // Replay historical events
    public bool adaptToCurrentContext;    // Update for modern markets
    public bool maintainEducationalValue; // Focus on learning
    
    [Header("Accuracy vs Engagement")]
    public float historicalAccuracy;      // 80% accuracy vs entertainment
    public bool enableWhatIfScenarios;    // "What if Fed acted differently?"
    public bool allowPlayerInterference;  // Can player change history?
}

public struct HistoricalEvent
{
    public string eventName;              // "Black Monday 1987"
    public DateTime originalDate;          // When it actually happened
    public EventCause[] causes;           // What led to the event
    public TimeSeries marketData;         // Actual market performance
    public PolicyResponse[] responses;    // How authorities responded
    public string[] lessons;              // What investors learned
    public ModernEquivalent modernContext; // How to understand in today's context
}
```

## 7. Balancing and Tuning

### 7.1 Event Impact Calibration

#### Severity Scaling
```csharp
[System.Serializable]
public struct EventSeverityConfig
{
    [Header("Impact Scaling")]
    public SeverityLevel[] severityLevels = {
        new SeverityLevel {
            name = "Minor",
            marketImpact = 0.02f,      // 2% market move
            durationDays = 3,
            frequency = 0.3f           // 30% of events
        },
        new SeverityLevel {
            name = "Moderate", 
            marketImpact = 0.08f,      // 8% market move
            durationDays = 14,
            frequency = 0.5f           // 50% of events
        },
        new SeverityLevel {
            name = "Major",
            marketImpact = 0.20f,      // 20% market move
            durationDays = 90,
            frequency = 0.15f          // 15% of events
        },
        new SeverityLevel {
            name = "Catastrophic",
            marketImpact = 0.50f,      // 50% market move
            durationDays = 365,
            frequency = 0.05f          // 5% of events
        }
    };
    
    [Header("Player Level Adaptation")]
    public bool scaleWithPlayerLevel;      // Harder events for advanced players
    public float difficultyMultiplier;     // 1.5x difficulty at max level
    public bool enableSkillBasedScaling;   // Scale based on player performance
}
```

### 7.2 Educational Value Optimization

#### Learning Outcome Measurement
```csharp
[System.Serializable]
public struct EducationalMetrics
{
    [Header("Learning Assessment")]
    public LearningOutcome[] targetOutcomes; // What players should learn
    public bool trackConceptMastery;        // Monitor understanding progress
    public bool enableKnowledgeRetention;   // Test retention over time
    
    [Header("Engagement Measurement")]
    public float eventEngagementRate;      // % players who actively participate
    public float decisionCompletionRate;   // % players who make decisions
    public float educationContentViews;    // % who read educational content
    
    [Header("Behavior Change")]
    public bool measureDecisionImprovement; // Are players making better decisions?
    public bool trackRiskManagement;       // Better risk management over time?
    public bool monitorLongTermRetention;  // Do lessons stick?
}
```

## Next Steps

1. **Implementation Guide** - Technical implementation specifications
2. **Content Creation Guide** - Event content development process
3. **Integration Testing** - Testing event system with overall game economy

## Related Documents

- [Economy Balance Model](./economy-balance-model.md) - Economic balancing parameters
- [AI Behavior Patterns](./ai-behavior-patterns.md) - How AI responds to events
- [Tutorial Onboarding](./tutorial-onboarding.md) - Educational integration
- [Simulation System](../architecture/simulation-system.md) - Technical architecture