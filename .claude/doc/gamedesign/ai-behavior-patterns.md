---
category: gamedesign
tags: [ai, behavior, patterns, decision-making, algorithms]
related: [economy-balance-model.md, simulation-system.md, entity-generation.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# AI Behavior Patterns

[🇰🇷 Korean Version](./ai-behavior-patterns_KOR.md)

## 📍 Navigation

[↩️ Back to Game Design](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. AI Behavior Philosophy

### 1.1 Design Principles

#### Realistic Economic Actors
- **Bounded Rationality**: AI entities make imperfect decisions with limited information
- **Diverse Motivations**: Different personality types drive varied economic behaviors
- **Adaptive Learning**: AI adapts to changing market conditions and player actions
- **Emergent Complexity**: Complex market patterns emerge from simple individual rules

#### Player Interaction Design
- **Challenging Opposition**: AI provides meaningful competition without being unfair
- **Teaching Opportunities**: AI mistakes and successes provide learning moments
- **Market Realism**: AI behavior creates believable market conditions
- **Scalable Intelligence**: AI difficulty adapts to player skill level

### 1.2 AI Entity Categories

#### Population AI (Consumers)
- **Primary Goal**: Maximize personal utility and financial security
- **Decision Scope**: Employment, consumption, savings, basic investments
- **Behavior Drivers**: Risk tolerance, social class, life stage, education
- **Update Frequency**: Daily for major decisions, hourly for minor adjustments

#### Company AI (Businesses)
- **Primary Goal**: Maximize long-term shareholder value
- **Decision Scope**: Production, hiring, pricing, expansion, M&A
- **Behavior Drivers**: Industry dynamics, competitive position, financial health
- **Update Frequency**: Monthly for strategic decisions, weekly for operational

#### Investor AI (Capitalists)
- **Primary Goal**: Generate superior risk-adjusted returns
- **Decision Scope**: Asset allocation, security selection, timing, leverage
- **Behavior Drivers**: Investment philosophy, risk capacity, market outlook
- **Update Frequency**: Real-time for tactical decisions, quarterly for strategic

## 2. Population AI Behavior

### 2.1 Decision-Making Framework

#### Utility Maximization Model
```csharp
[System.Serializable]
public struct PopulationUtilityFunction
{
    [Header("Basic Needs")]
    public float survivalWeight;          // 0.4 - Food, shelter, safety
    public float comfortWeight;           // 0.3 - Lifestyle improvements
    public float securityWeight;          // 0.2 - Financial security, insurance
    public float statusWeight;            // 0.1 - Social status, prestige
    
    [Header("Time Preferences")]
    public float presentBias;             // 0.7 - Present vs future utility
    public AnimationCurve discountCurve;  // How future value is discounted
    
    [Header("Risk Attitudes")]
    public float riskAversion;            // 0.6 - Conservative vs aggressive
    public float lossAversion;            // 2.0 - Loss weighs 2x more than gain
}

public float CalculateUtility(PopulationComponent pop, DecisionOption option)
{
    float baseUtility = 0f;
    
    // Calculate utility from each need category
    baseUtility += option.survivalValue * pop.utilityFunction.survivalWeight;
    baseUtility += option.comfortValue * pop.utilityFunction.comfortWeight;
    baseUtility += option.securityValue * pop.utilityFunction.securityWeight;
    baseUtility += option.statusValue * pop.utilityFunction.statusWeight;
    
    // Apply time preference discount
    float timeDiscount = pop.utilityFunction.discountCurve.Evaluate(option.timeHorizon);
    baseUtility *= timeDiscount;
    
    // Apply risk adjustment
    float riskPenalty = option.riskLevel * pop.utilityFunction.riskAversion;
    baseUtility -= riskPenalty;
    
    // Apply loss aversion for negative outcomes
    if (option.expectedValue < 0)
    {
        baseUtility *= pop.utilityFunction.lossAversion;
    }
    
    return baseUtility;
}
```

#### Behavioral Economics Integration
```csharp
[System.Serializable]
public struct CognitiveBiases
{
    [Header("Information Processing")]
    public float confirmationBias;        // 0.3 - Seek confirming information
    public float availabilityHeuristic;   // 0.4 - Recent events seem more likely
    public float anchoringBias;           // 0.5 - First information overly influential
    
    [Header("Social Influences")]
    public float herdBehavior;            // 0.6 - Follow crowd decisions
    public float authorityBias;           // 0.4 - Trust expert opinions
    public float socialProofWeight;       // 0.5 - What others do influences choice
    
    [Header("Temporal Biases")]
    public float hyperbolicDiscounting;   // 0.8 - Overweight immediate rewards
    public float planningFallacy;         // 0.3 - Underestimate time/cost
    public float statusQuoBias;           // 0.7 - Prefer current situation
}

public void ApplyCognitiveBiases(ref DecisionOption option, PopulationComponent pop, MarketContext context)
{
    var biases = pop.cognitiveBiases;
    
    // Confirmation bias - seek information that confirms existing beliefs
    if (option.alignsWithBeliefs)
    {
        option.perceivedValue *= (1f + biases.confirmationBias);
    }
    
    // Availability heuristic - recent events seem more probable
    if (context.recentSimilarEvents > 0)
    {
        float availabilityBoost = biases.availabilityHeuristic * context.recentSimilarEvents;
        option.perceivedProbability += availabilityBoost;
    }
    
    // Herd behavior - follow what others are doing
    float crowdFactor = context.percentageDoingSame * biases.herdBehavior;
    option.socialUtility += crowdFactor;
    
    // Status quo bias - prefer current situation
    if (option.requiresChange)
    {
        option.perceivedCost *= (1f + biases.statusQuoBias);
    }
}
```

### 2.2 Employment Decision AI

#### Job Search Algorithm
```csharp
public partial struct EmploymentDecisionSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (entity, pop, economic, decision) in 
                 SystemAPI.Query<Entity, PopulationComponent, EconomicStatusComponent, DecisionComponent>()
                          .WithAll<UnemployedTag>())
        {
            // Evaluate all available job opportunities
            var jobOptions = FindAvailableJobs(pop.skillLevel, pop.education, pop.location);
            
            if (jobOptions.Length == 0)
            {
                // Lower expectations if no jobs found
                pop.reservationWage *= 0.95f; // Reduce minimum acceptable wage
                decision.searchIntensity += 0.1f; // Search harder
                continue;
            }
            
            // Score each job opportunity
            JobOption bestJob = null;
            float bestScore = float.MinValue;
            
            foreach (var job in jobOptions)
            {
                float jobScore = EvaluateJobOption(job, pop, economic);
                
                if (jobScore > bestScore && jobScore > pop.reservationWage)
                {
                    bestScore = jobScore;
                    bestJob = job;
                }
            }
            
            // Make job decision
            if (bestJob != null && ShouldAcceptJob(bestJob, pop, economic))
            {
                AcceptJobOffer(entity, bestJob, ref state);
            }
            else
            {
                // Continue searching, adjust search strategy
                AdjustJobSearchStrategy(ref pop, jobOptions);
            }
        }
    }
    
    private float EvaluateJobOption(JobOption job, PopulationComponent pop, EconomicStatusComponent economic)
    {
        float score = 0f;
        
        // Wage component (most important)
        float wageUtility = job.salary / pop.reservationWage;
        score += wageUtility * 0.5f;
        
        // Location convenience
        float commutePenalty = CalculateCommutePenalty(job.location, pop.location);
        score -= commutePenalty * 0.2f;
        
        // Career advancement potential
        float careerValue = job.skillGrowthPotential * pop.careerAmbition;
        score += careerValue * 0.2f;
        
        // Job security
        float securityValue = job.jobSecurity * pop.riskAversion;
        score += securityValue * 0.1f;
        
        return score;
    }
}
```

#### Career Development Patterns
```csharp
[System.Serializable]
public struct CareerProgressionAI
{
    [Header("Skill Development")]
    public float learningRate;            // How quickly skills improve
    public AnimationCurve experienceCurve; // Skill growth over time
    public float trainingInvestment;       // Willingness to invest in education
    
    [Header("Job Mobility")]
    public float jobSwitchingRate;        // Likelihood to change jobs
    public float loyaltyDecay;            // How quickly loyalty decreases
    public float careerAmbition;          // Drive for advancement
    
    [Header("Salary Negotiation")]
    public float negotiationSkill;        // Ability to get better offers
    public float marketAwareness;         // Knowledge of salary ranges
    public float risktaking;              // Willingness to make demands
}

public void UpdateCareerProgression(ref PopulationComponent pop, float deltaTime)
{
    var career = pop.careerProgression;
    
    // Skill improvement over time
    float skillGain = career.learningRate * deltaTime;
    skillGain *= career.experienceCurve.Evaluate(pop.yearsExperience);
    pop.skillLevel += skillGain;
    
    // Update job satisfaction based on performance vs expectations
    float expectationGap = pop.currentSalary / pop.expectedSalary;
    pop.jobSatisfaction = Mathf.Lerp(pop.jobSatisfaction, expectationGap, 0.1f);
    
    // Consider job switching if dissatisfied
    if (pop.jobSatisfaction < 0.6f)
    {
        float switchProbability = career.jobSwitchingRate * (1f - pop.jobSatisfaction);
        
        if (Random.value < switchProbability)
        {
            InitiateJobSearch(pop);
        }
    }
    
    // Negotiate salary increases periodically
    if (pop.timeInCurrentJob > 12f) // After 1 year
    {
        AttemptSalaryNegotiation(ref pop);
    }
}
```

### 2.3 Consumption Decision AI

#### Spending Behavior Model
```csharp
[System.Serializable]
public struct ConsumptionBehaviorAI
{
    [Header("Spending Categories")]
    public float necessitySpending;       // 0.5 - Non-discretionary spending
    public float comfortSpending;         // 0.3 - Lifestyle improvements
    public float socialSpending;          // 0.1 - Status/social signaling
    public float impulsiveSpending;       // 0.1 - Unplanned purchases
    
    [Header("Decision Factors")]
    public AnimationCurve incomeElasticity; // Spending vs income relationship
    public float priceElasticity;         // Response to price changes
    public float brandLoyalty;           // Preference for familiar brands
    public float qualityPreference;      // Willingness to pay for quality
}

public ConsumptionDecision MakeConsumptionDecision(PopulationComponent pop, 
                                                  EconomicStatusComponent economic,
                                                  ProductOption[] availableProducts)
{
    var behavior = pop.consumptionBehavior;
    float availableBudget = economic.monthlyIncome * economic.consumptionRate;
    
    var decision = new ConsumptionDecision();
    
    // Allocate budget across categories
    decision.necessityBudget = availableBudget * behavior.necessitySpending;
    decision.comfortBudget = availableBudget * behavior.comfortSpending;
    decision.socialBudget = availableBudget * behavior.socialSpending;
    decision.impulsiveBudget = availableBudget * behavior.impulsiveSpending;
    
    // For each category, select best products
    decision.selectedProducts = new List<ProductPurchase>();
    
    // Necessity purchases (food, utilities, rent)
    var necessityProducts = availableProducts.Where(p => p.category == ProductCategory.Necessity);
    SelectOptimalProducts(necessityProducts, decision.necessityBudget, behavior, ref decision);
    
    // Comfort purchases (entertainment, dining out, hobbies)
    var comfortProducts = availableProducts.Where(p => p.category == ProductCategory.Comfort);
    SelectOptimalProducts(comfortProducts, decision.comfortBudget, behavior, ref decision);
    
    // Social purchases (fashion, cars, vacations)
    var socialProducts = availableProducts.Where(p => p.category == ProductCategory.Social);
    SelectOptimalProducts(socialProducts, decision.socialBudget, behavior, ref decision);
    
    // Impulse purchases (random, emotion-driven)
    if (Random.value < behavior.impulsiveSpending)
    {
        var impulseProduct = availableProducts[Random.Range(0, availableProducts.Length)];
        if (impulseProduct.price <= decision.impulsiveBudget)
        {
            decision.selectedProducts.Add(new ProductPurchase 
            { 
                product = impulseProduct, 
                quantity = 1,
                reason = PurchaseReason.Impulse
            });
        }
    }
    
    return decision;
}
```

#### Brand Preference and Market Response
```csharp
public struct BrandPreferenceAI
{
    public Dictionary<string, float> brandAffinity;   // 0.0 to 1.0 preference
    public float brandSwitchingCost;                  // Psychological cost to switch
    public float advertisingImpact;                   // How much ads influence choice
    public float wordOfMouthWeight;                   // Social influence on brand choice
    
    public ProductOption SelectPreferredBrand(ProductOption[] similarProducts, 
                                            PopulationComponent pop)
    {
        float bestScore = float.MinValue;
        ProductOption bestProduct = null;
        
        foreach (var product in similarProducts)
        {
            float score = 0f;
            
            // Base utility from product features
            score += product.qualityRating * pop.qualityPreference;
            
            // Price consideration (diminishing utility)
            float priceUtility = Mathf.Log(1f + product.price) * pop.priceElasticity * -1f;
            score += priceUtility;
            
            // Brand affinity bonus
            if (brandAffinity.ContainsKey(product.brand))
            {
                score += brandAffinity[product.brand] * 2f;
                
                // Current brand gets switching cost bonus
                if (product.brand == pop.currentPreferredBrand)
                {
                    score += brandSwitchingCost;
                }
            }
            
            // Social proof (how many others bought this)
            score += product.marketShare * wordOfMouthWeight;
            
            // Recent advertising exposure
            score += product.advertisingExposure * advertisingImpact;
            
            if (score > bestScore)
            {
                bestScore = score;
                bestProduct = product;
            }
        }
        
        // Update brand affinity based on purchase experience
        if (bestProduct != null)
        {
            UpdateBrandAffinity(bestProduct.brand, bestProduct.satisfactionRating);
        }
        
        return bestProduct;
    }
}
```

## 3. Company AI Behavior

### 3.1 Business Strategy AI

#### Strategic Decision Framework
```csharp
[System.Serializable]
public struct CompanyStrategyAI
{
    [Header("Strategic Orientation")]
    public BusinessStrategy primaryStrategy;   // Cost leadership, differentiation, etc.
    public float riskTolerance;               // 0.3 conservative, 0.8 aggressive
    public float growthAmbition;              // 0.5 stable, 0.9 rapid expansion
    public float innovationFocus;             // R&D investment tendency
    
    [Header("Decision Weights")]
    public float profitabilityWeight;         // 0.4 - Short-term profits
    public float marketShareWeight;           // 0.3 - Market dominance
    public float sustainabilityWeight;        // 0.2 - Long-term viability
    public float stakeholderWeight;           // 0.1 - Employee/customer satisfaction
    
    [Header("Competitive Response")]
    public float competitorAwareness;         // How much they watch competitors
    public float firstMoverAdvantage;         // Willingness to be first
    public float imitationSpeed;              // Speed of copying competitor moves
}

public BusinessDecision MakeStrategicDecision(CompanyComponent company, 
                                            MarketContext market,
                                            CompetitorAction[] recentActions)
{
    var strategy = company.strategyAI;
    var decision = new BusinessDecision();
    
    // Analyze market conditions
    float marketAttractiveness = AnalyzeMarketConditions(market);
    float competitivePressure = AnalyzeCompetitivePressure(recentActions);
    float resourceConstraints = AnalyzeResourceConstraints(company);
    
    // Generate strategic options
    var options = GenerateStrategicOptions(company, market, strategy);
    
    // Evaluate each option
    BusinessOption bestOption = null;
    float bestScore = float.MinValue;
    
    foreach (var option in options)
    {
        float score = EvaluateStrategicOption(option, strategy, market, company);
        
        if (score > bestScore)
        {
            bestScore = score;
            bestOption = option;
        }
    }
    
    // Execute decision
    if (bestOption != null)
    {
        decision = ConvertToBusinessDecision(bestOption, company);
        
        // Update strategy based on decision
        UpdateStrategyFromDecision(ref strategy, bestOption, market);
    }
    
    return decision;
}

private float EvaluateStrategicOption(BusinessOption option, 
                                    CompanyStrategyAI strategy,
                                    MarketContext market,
                                    CompanyComponent company)
{
    float score = 0f;
    
    // Profitability impact
    float profitImpact = option.expectedProfitChange / company.currentProfit;
    score += profitImpact * strategy.profitabilityWeight;
    
    // Market share impact
    float shareImpact = option.expectedMarketShareChange;
    score += shareImpact * strategy.marketShareWeight;
    
    // Long-term sustainability
    float sustainabilityImpact = option.sustainabilityScore;
    score += sustainabilityImpact * strategy.sustainabilityWeight;
    
    // Risk adjustment
    float riskPenalty = option.riskLevel * (1f - strategy.riskTolerance);
    score -= riskPenalty;
    
    // Strategic fit
    float strategicFit = CalculateStrategicFit(option, strategy.primaryStrategy);
    score *= strategicFit;
    
    return score;
}
```

#### Pricing Strategy AI
```csharp
[System.Serializable]
public struct PricingStrategyAI
{
    [Header("Pricing Philosophy")]
    public PricingStrategy strategy;          // Penetration, skimming, competitive
    public float priceElasticityEstimate;     // Demand response to price changes
    public float competitorResponseSpeed;     // How quickly competitors react
    
    [Header("Optimization Parameters")]
    public float profitMarginTarget;          // Desired profit margin
    public float marketShareImportance;       // Price for share vs margin
    public float brandPremiumCapacity;        // Ability to charge premium
}

public float CalculateOptimalPrice(CompanyComponent company, 
                                  ProductComponent product,
                                  MarketDynamicsComponent market)
{
    var pricing = company.pricingAI;
    float optimalPrice = 0f;
    
    switch (pricing.strategy)
    {
        case PricingStrategy.CostPlus:
            optimalPrice = CalculateCostPlusPrice(product, pricing.profitMarginTarget);
            break;
            
        case PricingStrategy.CompetitiveParity:
            optimalPrice = CalculateCompetitivePrice(market.averagePrice, company.competitivePosition);
            break;
            
        case PricingStrategy.ValueBased:
            optimalPrice = CalculateValueBasedPrice(product.customerValue, pricing.brandPremiumCapacity);
            break;
            
        case PricingStrategy.Penetration:
            optimalPrice = CalculatePenetrationPrice(market.averagePrice, pricing.marketShareImportance);
            break;
            
        case PricingStrategy.Skimming:
            optimalPrice = CalculateSkimmingPrice(product.innovationLevel, market.priceElasticity);
            break;
    }
    
    // Apply dynamic adjustments
    optimalPrice = ApplyDynamicPricingAdjustments(optimalPrice, market, company);
    
    // Validate price bounds
    float minPrice = product.marginalCost * 1.1f; // Minimum 10% margin
    float maxPrice = market.averagePrice * 2.0f;  // Maximum 2x market average
    
    return Mathf.Clamp(optimalPrice, minPrice, maxPrice);
}

private float ApplyDynamicPricingAdjustments(float basePrice, 
                                           MarketDynamicsComponent market,
                                           CompanyComponent company)
{
    float adjustedPrice = basePrice;
    
    // Inventory level adjustment
    if (company.inventoryLevel > company.optimalInventoryLevel * 1.2f)
    {
        adjustedPrice *= 0.95f; // Discount to move inventory
    }
    else if (company.inventoryLevel < company.optimalInventoryLevel * 0.8f)
    {
        adjustedPrice *= 1.05f; // Premium for scarce inventory
    }
    
    // Demand surge adjustment
    if (market.demandLevel > market.averageDemand * 1.3f)
    {
        adjustedPrice *= 1.1f; // Surge pricing
    }
    
    // Competitive pressure adjustment
    if (market.competitorCount > market.averageCompetitors * 1.5f)
    {
        adjustedPrice *= 0.98f; // Price competition response
    }
    
    // Seasonal adjustment
    float seasonalMultiplier = market.seasonalityFactor;
    adjustedPrice *= seasonalMultiplier;
    
    return adjustedPrice;
}
```

### 3.2 Production and Operations AI

#### Production Planning Algorithm
```csharp
public struct ProductionPlanningAI
{
    [Header("Planning Horizon")]
    public float forecastAccuracy;            // How well company predicts demand
    public int planningPeriods;               // Months ahead to plan
    public float bufferStock;                 // Safety stock multiplier
    
    [Header("Cost Optimization")]
    public float economies_of_scale;          // Production efficiency curves
    public float capacityUtilization;        // Target capacity usage
    public float qualityTradeoff;             // Quality vs cost balance
}

public ProductionPlan CreateProductionPlan(CompanyComponent company,
                                         DemandForecast forecast,
                                         ResourceConstraints resources)
{
    var planning = company.productionAI;
    var plan = new ProductionPlan();
    
    // Forecast demand for planning horizon
    float[] demandForecast = new float[planning.planningPeriods];
    for (int period = 0; period < planning.planningPeriods; period++)
    {
        demandForecast[period] = ForecastDemand(period, forecast, planning.forecastAccuracy);
    }
    
    // Calculate production requirements
    float totalDemand = demandForecast.Sum();
    float productionTarget = totalDemand * (1f + planning.bufferStock);
    
    // Optimize production schedule
    plan.monthlyProduction = OptimizeProductionSchedule(
        productionTarget, 
        resources, 
        planning.economies_of_scale,
        planning.capacityUtilization
    );
    
    // Resource allocation
    plan.laborRequirement = CalculateLaborNeed(plan.monthlyProduction, company.productivity);
    plan.materialRequirement = CalculateMaterialNeed(plan.monthlyProduction, company.efficiency);
    plan.capitalInvestment = CalculateCapitalNeed(plan.monthlyProduction, company.capacity);
    
    // Quality targets
    plan.qualityLevel = DetermineQualityLevel(planning.qualityTradeoff, company.brandPosition);
    
    return plan;
}
```

#### Supply Chain Management AI
```csharp
[System.Serializable]
public struct SupplyChainAI
{
    [Header("Supplier Strategy")]
    public float supplierLoyalty;            // Preference for existing suppliers
    public float costVsQuality;              // 0.7 = prefer cost, 0.3 = prefer quality
    public float riskAversion;               // Diversification vs efficiency
    
    [Header("Inventory Management")]
    public float inventoryTurnover;          // Target inventory turns per year
    public float stockoutCost;               // Penalty for running out of stock
    public float holdingCostSensitivity;     // Sensitivity to inventory costs
}

public SupplierDecision SelectSuppliers(CompanyComponent company,
                                      SupplierOption[] availableSuppliers,
                                      MaterialRequirement requirements)
{
    var supplyChain = company.supplyChainAI;
    var decision = new SupplierDecision();
    
    // Score each supplier
    var supplierScores = new Dictionary<SupplierOption, float>();
    
    foreach (var supplier in availableSuppliers)
    {
        float score = 0f;
        
        // Cost consideration
        float costScore = (requirements.budgetPerUnit - supplier.pricePerUnit) / requirements.budgetPerUnit;
        score += costScore * supplyChain.costVsQuality;
        
        // Quality consideration
        float qualityScore = supplier.qualityRating / 10f;
        score += qualityScore * (1f - supplyChain.costVsQuality);
        
        // Reliability consideration
        float reliabilityScore = supplier.onTimeDeliveryRate;
        score += reliabilityScore * 0.3f;
        
        // Existing relationship bonus
        if (company.currentSuppliers.Contains(supplier.supplierId))
        {
            score += supplyChain.supplierLoyalty;
        }
        
        // Risk assessment (geographical, financial, political)
        float riskPenalty = supplier.riskLevel * supplyChain.riskAversion;
        score -= riskPenalty;
        
        supplierScores[supplier] = score;
    }
    
    // Select optimal supplier portfolio
    if (supplyChain.riskAversion > 0.7f)
    {
        // Risk-averse: diversify across multiple suppliers
        decision.selectedSuppliers = SelectDiversifiedSuppliers(supplierScores, requirements);
    }
    else
    {
        // Risk-tolerant: select single best supplier
        var bestSupplier = supplierScores.OrderByDescending(kvp => kvp.Value).First();
        decision.selectedSuppliers = new[] { bestSupplier.Key };
        decision.allocationRatios = new[] { 1.0f };
    }
    
    return decision;
}
```

### 3.3 Human Resources AI

#### Hiring Decision Algorithm
```csharp
[System.Serializable]
public struct HiringStrategyAI
{
    [Header("Hiring Philosophy")]
    public float talentVsCost;               // Prefer best talent vs lowest cost
    public float experienceVsPotential;      // Experienced vs trainable candidates
    public float culturefit_importance;      // Cultural alignment weight
    
    [Header("Growth Strategy")]
    public float aggressiveGrowthRate;       // How quickly to expand team
    public float skillGapUrgency;            // Speed of addressing skill shortages
    public float retention_focus;            // Effort to retain existing employees
}

public HiringDecision MakeHiringDecision(CompanyComponent company,
                                       JobOpening position,
                                       CandidateProfile[] candidates)
{
    var hiring = company.hiringAI;
    var decision = new HiringDecision();
    
    // Determine hiring urgency
    float urgency = CalculateHiringUrgency(company, position);
    
    // Score each candidate
    CandidateProfile bestCandidate = null;
    float bestScore = float.MinValue;
    
    foreach (var candidate in candidates)
    {
        float score = EvaluateCandidate(candidate, position, hiring, company.culture);
        
        if (score > bestScore)
        {
            bestScore = score;
            bestCandidate = candidate;
        }
    }
    
    // Make hiring decision based on score and budget constraints
    if (bestCandidate != null && 
        bestScore > hiring.hiringThreshold &&
        bestCandidate.salaryExpectation <= position.budgetMax)
    {
        decision.shouldHire = true;
        decision.selectedCandidate = bestCandidate;
        decision.salaryOffer = CalculateSalaryOffer(bestCandidate, position, hiring);
        decision.startDate = CalculateStartDate(urgency);
    }
    else
    {
        decision.shouldHire = false;
        decision.reason = DetermineRejectionReason(bestScore, bestCandidate);
        
        // Adjust hiring criteria if no suitable candidates
        if (bestScore < hiring.hiringThreshold * 0.8f)
        {
            AdjustHiringCriteria(ref hiring, position, candidates);
        }
    }
    
    return decision;
}

private float EvaluateCandidate(CandidateProfile candidate,
                               JobOpening position,
                               HiringStrategyAI hiring,
                               CompanyCulture culture)
{
    float score = 0f;
    
    // Technical skills match
    float skillMatch = CalculateSkillMatch(candidate.skills, position.requiredSkills);
    score += skillMatch * 0.4f;
    
    // Experience vs potential tradeoff
    float experienceScore = candidate.yearsExperience / position.desiredExperience;
    float potentialScore = candidate.learningAbility * candidate.adaptability;
    float experienceWeight = hiring.experienceVsPotential;
    
    score += (experienceScore * experienceWeight + potentialScore * (1f - experienceWeight)) * 0.3f;
    
    // Cultural fit assessment
    float cultureFit = CalculateCultureFit(candidate.personality, culture);
    score += cultureFit * hiring.culturefit_importance * 0.2f;
    
    // Cost consideration
    float costEfficiency = position.budgetMax / candidate.salaryExpectation;
    float costWeight = 1f - hiring.talentVsCost;
    score += costEfficiency * costWeight * 0.1f;
    
    return score;
}
```

## 4. Investor AI Behavior

### 4.1 Investment Strategy AI

#### Portfolio Construction Algorithm
```csharp
[System.Serializable]
public struct InvestmentStrategyAI
{
    [Header("Investment Philosophy")]
    public InvestmentStyle style;            // Value, Growth, Momentum, etc.
    public float riskTolerance;             // 0.3 conservative, 0.8 aggressive
    public int investmentHorizon;           // Months for typical holding period
    
    [Header("Portfolio Management")]
    public float diversification_target;     // Max % in single position
    public float cashBufferPercent;         // Cash allocation for opportunities
    public float rebalanceThreshold;        // Deviation before rebalancing
    
    [Header("Decision Making")]
    public float fundamentalWeight;         // 0.6 - Fundamental analysis weight
    public float technicalWeight;           // 0.3 - Technical analysis weight  
    public float sentimentWeight;           // 0.1 - Market sentiment weight
}

public InvestmentDecision MakeInvestmentDecision(InvestorAI investor,
                                               SecurityOption[] availableSecurities,
                                               MarketContext market,
                                               PortfolioState currentPortfolio)
{
    var strategy = investor.investmentStrategy;
    var decision = new InvestmentDecision();
    
    // Analyze market conditions
    MarketRegime regime = AnalyzeMarketRegime(market);
    
    // Screen securities based on investment style
    var screenedSecurities = ScreenSecurities(availableSecurities, strategy.style, regime);
    
    // Evaluate each security
    var securityScores = new Dictionary<SecurityOption, float>();
    
    foreach (var security in screenedSecurities)
    {
        float score = EvaluateSecurity(security, strategy, market, regime);
        securityScores[security] = score;
    }
    
    // Portfolio optimization
    var topSecurities = securityScores
        .OrderByDescending(kvp => kvp.Value)
        .Take(20)  // Consider top 20 candidates
        .ToArray();
    
    // Construct optimal portfolio
    decision.portfolioChanges = OptimizePortfolio(
        topSecurities, 
        currentPortfolio, 
        strategy,
        investor.availableCash
    );
    
    // Risk management overlay
    ApplyRiskManagement(ref decision, strategy, market);
    
    return decision;
}

private float EvaluateSecurity(SecurityOption security,
                              InvestmentStrategyAI strategy,
                              MarketContext market,
                              MarketRegime regime)
{
    float score = 0f;
    
    // Fundamental analysis score
    float fundamentalScore = AnalyzeFundamentals(security, strategy.style);
    score += fundamentalScore * strategy.fundamentalWeight;
    
    // Technical analysis score
    float technicalScore = AnalyzeTechnicals(security, regime);
    score += technicalScore * strategy.technicalWeight;
    
    // Market sentiment score
    float sentimentScore = AnalyzeSentiment(security, market);
    score += sentimentScore * strategy.sentimentWeight;
    
    // Risk-adjusted return expectation
    float expectedReturn = security.expectedReturn;
    float riskPenalty = security.volatility * (1f - strategy.riskTolerance);
    score = expectedReturn - riskPenalty;
    
    // Liquidity consideration
    if (security.averageVolume < strategy.minimumLiquidity)
    {
        score *= 0.5f; // Penalize illiquid securities
    }
    
    return score;
}
```

#### Risk Management AI
```csharp
[System.Serializable]  
public struct RiskManagementAI
{
    [Header("Position Sizing")]
    public float maxPositionSize;            // Maximum % in single position
    public float correlationLimit;           // Max correlation between positions
    public float sectorConcentrationLimit;   // Max % in single sector
    
    [Header("Stop Loss Strategy")]
    public bool useStopLosses;              // Whether to use stop losses
    public float stopLossPercent;           // -15% typical stop loss
    public float trailingStopPercent;       // Trailing stop distance
    
    [Header("Hedging")]
    public float hedgeRatio;                // % of portfolio to hedge
    public HedgingInstrument[] hedgingTools; // Available hedging instruments
    public float volatilityThreshold;       // VIX level that triggers hedging
}

public void ApplyRiskManagement(ref InvestmentDecision decision,
                               InvestmentStrategyAI strategy,
                               MarketContext market)
{
    var risk = strategy.riskManagement;
    
    // Position sizing rules
    foreach (var change in decision.portfolioChanges)
    {
        // Limit individual position sizes
        float maxSize = decision.totalPortfolioValue * risk.maxPositionSize;
        change.targetValue = Mathf.Min(change.targetValue, maxSize);
        
        // Check sector concentration
        float sectorExposure = CalculateSectorExposure(change.security.sector, decision);
        if (sectorExposure > risk.sectorConcentrationLimit)
        {
            change.targetValue *= (risk.sectorConcentrationLimit / sectorExposure);
        }
    }
    
    // Apply hedging if market volatility is high
    if (market.volatilityIndex > risk.volatilityThreshold)
    {
        var hedgeTrade = CreateHedgingTrade(decision, risk, market);
        if (hedgeTrade != null)
        {
            decision.portfolioChanges.Add(hedgeTrade);
        }
    }
    
    // Set stop losses for new positions
    if (risk.useStopLosses)
    {
        foreach (var change in decision.portfolioChanges)
        {
            if (change.action == TradeAction.Buy)
            {
                change.stopLoss = change.entryPrice * (1f + risk.stopLossPercent);
            }
        }
    }
}
```

### 4.2 Market Making AI

#### Liquidity Provision Algorithm  
```csharp
[System.Serializable]
public struct MarketMakingAI
{
    [Header("Spread Management")]
    public float targetSpread;               // Bid-ask spread target
    public float minimumSpread;              // Minimum profitable spread
    public AnimationCurve spreadByVolatility; // Spread vs market volatility
    
    [Header("Inventory Management")]  
    public float maxInventoryRisk;           // Maximum inventory position
    public float inventoryHalfLife;          // Time to reduce inventory by half
    public float skewSensitivity;            // Price skew based on inventory
    
    [Header("Risk Controls")]
    public float maxDailyLoss;              // Daily loss limit
    public float positionTimeout;           // Max time to hold inventory
    public float correlationLimit;          // Max correlation in inventory
}

public MarketMakingDecision MakeMarketDecision(MarketMakerAI marketMaker,
                                             SecurityContext security,
                                             OrderBookState orderBook,
                                             InventoryPosition currentInventory)
{
    var mmAI = marketMaker.marketMakingAI;
    var decision = new MarketMakingDecision();
    
    // Calculate fair value estimate
    float fairValue = EstimateFairValue(security, orderBook);
    
    // Determine optimal spread based on market conditions
    float volatility = CalculateCurrentVolatility(security);
    float optimalSpread = mmAI.spreadByVolatility.Evaluate(volatility);
    optimalSpread = Mathf.Max(optimalSpread, mmAI.minimumSpread);
    
    // Apply inventory skew
    float inventorySkew = CalculateInventorySkew(currentInventory, mmAI);
    
    // Set bid and ask prices
    decision.bidPrice = fairValue - (optimalSpread * 0.5f) - inventorySkew;
    decision.askPrice = fairValue + (optimalSpread * 0.5f) - inventorySkew;
    
    // Determine order sizes
    float baseOrderSize = CalculateOptimalOrderSize(security, mmAI);
    decision.bidSize = AdjustSizeForRisk(baseOrderSize, currentInventory.longExposure, mmAI);
    decision.askSize = AdjustSizeForRisk(baseOrderSize, currentInventory.shortExposure, mmAI);
    
    // Risk management checks
    if (currentInventory.totalRisk > mmAI.maxInventoryRisk)
    {
        // Reduce making in direction of inventory
        if (currentInventory.netPosition > 0)
        {
            decision.bidSize *= 0.5f; // Reduce buying
        }
        else
        {
            decision.askSize *= 0.5f; // Reduce selling
        }
    }
    
    // Daily loss check
    if (marketMaker.dailyPnL < -mmAI.maxDailyLoss)
    {
        decision.shouldMakeMarket = false;
        decision.reason = "Daily loss limit reached";
        return decision;
    }
    
    decision.shouldMakeMarket = true;
    return decision;
}
```

## 5. Adaptive Learning Systems

### 5.1 Machine Learning Integration

#### Reinforcement Learning for AI Behavior
```csharp
[System.Serializable]
public struct ReinforcementLearningAI
{
    [Header("Learning Parameters")]
    public float learningRate;               // 0.01 - How quickly to adapt
    public float explorationRate;            // 0.1 - Random action probability
    public float discountFactor;             // 0.95 - Future reward discounting
    
    [Header("Experience Replay")]
    public int replayBufferSize;             // 10000 - Stored experiences
    public int batchSize;                    // 32 - Training batch size
    public int updateFrequency;              // Every 100 actions
    
    [Header("Neural Network")]
    public int[] hiddenLayers;               // [128, 64] - Network architecture
    public ActivationFunction activation;    // ReLU, Sigmoid, etc.
    public float dropout_rate;               // 0.2 - Regularization
}

public void UpdateAIBehavior(AIEntity entity, ActionResult result)
{
    var rl = entity.reinforcementLearning;
    
    // Store experience in replay buffer
    var experience = new Experience
    {
        state = result.previousState,
        action = result.action,
        reward = result.reward,
        nextState = result.currentState,
        done = result.episodeComplete
    };
    
    rl.replayBuffer.Add(experience);
    
    // Train neural network periodically
    if (rl.stepCount % rl.updateFrequency == 0 && 
        rl.replayBuffer.Count >= rl.batchSize)
    {
        var batch = rl.replayBuffer.Sample(rl.batchSize);
        TrainNetwork(entity.neuralNetwork, batch, rl);
    }
    
    // Update exploration rate (epsilon decay)
    rl.explorationRate *= 0.995f;
    rl.explorationRate = Mathf.Max(rl.explorationRate, 0.01f);
    
    rl.stepCount++;
}
```

### 5.2 Behavioral Evolution

#### Genetic Algorithm for Strategy Evolution
```csharp
[System.Serializable]
public struct GeneticAlgorithmAI
{
    [Header("Population Parameters")]
    public int populationSize;              // 50 - Number of AI entities
    public int generations;                 // 100 - Evolution iterations
    public float mutationRate;              // 0.1 - Random mutation chance
    
    [Header("Selection Strategy")]
    public SelectionMethod selectionMethod; // Tournament, Roulette, etc.
    public float elitismRate;              // 0.1 - Top performers kept
    public int tournamentSize;             // 5 - Tournament selection size
}

public void EvolveAIPopulation(AIEntity[] population, float[] fitnessScores)
{
    var ga = geneticAlgorithm;
    
    // Selection: Choose parents for next generation
    var parents = SelectParents(population, fitnessScores, ga);
    
    // Create new generation
    var newGeneration = new AIEntity[ga.populationSize];
    
    // Elitism: Keep best performers
    int eliteCount = Mathf.RoundToInt(ga.populationSize * ga.elitismRate);
    var elite = population.OrderByDescending(ai => ai.fitness).Take(eliteCount);
    
    for (int i = 0; i < eliteCount; i++)
    {
        newGeneration[i] = elite.ElementAt(i).Clone();
    }
    
    // Crossover and mutation for rest of population
    for (int i = eliteCount; i < ga.populationSize; i++)
    {
        var parent1 = parents[Random.Range(0, parents.Length)];
        var parent2 = parents[Random.Range(0, parents.Length)];
        
        var offspring = Crossover(parent1, parent2);
        
        if (Random.value < ga.mutationRate)
        {
            offspring = Mutate(offspring);
        }
        
        newGeneration[i] = offspring;
    }
    
    // Replace old population
    Array.Copy(newGeneration, population, ga.populationSize);
}
```

## 6. Performance Optimization

### 6.1 Behavioral Caching

#### Decision Caching System
```csharp
[System.Serializable]
public struct DecisionCache
{
    public Dictionary<StateHash, CachedDecision> cache;
    public int maxCacheSize;                 // 1000 entries
    public float cacheValidityTime;          // 60 seconds
    public float similarityThreshold;        // 0.95 - State similarity
}

public DecisionResult GetCachedDecision(AIEntity entity, GameState currentState)
{
    var cache = entity.decisionCache;
    var stateHash = CalculateStateHash(currentState);
    
    if (cache.cache.ContainsKey(stateHash))
    {
        var cached = cache.cache[stateHash];
        
        // Check if cache is still valid
        if (Time.time - cached.timestamp < cache.cacheValidityTime)
        {
            return cached.decision;
        }
        else
        {
            // Remove expired entry
            cache.cache.Remove(stateHash);
        }
    }
    
    // Check for similar states
    foreach (var kvp in cache.cache)
    {
        float similarity = CalculateStateSimilarity(currentState, kvp.Value.state);
        if (similarity > cache.similarityThreshold)
        {
            return kvp.Value.decision;
        }
    }
    
    return null; // No cached decision found
}

public void CacheDecision(AIEntity entity, GameState state, DecisionResult decision)
{
    var cache = entity.decisionCache;
    var stateHash = CalculateStateHash(state);
    
    // Add to cache
    cache.cache[stateHash] = new CachedDecision
    {
        state = state,
        decision = decision,
        timestamp = Time.time
    };
    
    // Maintain cache size limit
    if (cache.cache.Count > cache.maxCacheSize)
    {
        // Remove oldest entries
        var oldestEntry = cache.cache.OrderBy(kvp => kvp.Value.timestamp).First();
        cache.cache.Remove(oldestEntry.Key);
    }
}
```

### 6.2 Hierarchical Decision Making

#### Multi-Level AI Processing
```csharp
public enum AIProcessingLevel
{
    Strategic,      // Monthly decisions - complex analysis
    Tactical,       // Weekly decisions - moderate analysis  
    Operational,    // Daily decisions - simple heuristics
    Reactive        // Real-time decisions - cached responses
}

[System.Serializable]
public struct HierarchicalAI
{
    [Header("Processing Allocation")]
    public float strategicBudget;    // 10% - Complex decisions
    public float tacticalBudget;     // 20% - Moderate decisions
    public float operationalBudget;  // 40% - Simple decisions
    public float reactiveBudget;     // 30% - Cached responses
    
    public Dictionary<AIProcessingLevel, Queue<AITask>> taskQueues;
    public int maxTasksPerLevel;
}

public void ProcessAIHierarchy(float processingBudget)
{
    var hierarchy = aiHierarchy;
    
    // Allocate processing time across levels
    float strategicTime = processingBudget * hierarchy.strategicBudget;
    float tacticalTime = processingBudget * hierarchy.tacticalBudget;
    float operationalTime = processingBudget * hierarchy.operationalBudget;
    float reactiveTime = processingBudget * hierarchy.reactiveBudget;
    
    // Process each level in priority order
    ProcessTaskQueue(AIProcessingLevel.Strategic, strategicTime);
    ProcessTaskQueue(AIProcessingLevel.Tactical, tacticalTime);
    ProcessTaskQueue(AIProcessingLevel.Operational, operationalTime);
    ProcessTaskQueue(AIProcessingLevel.Reactive, reactiveTime);
}

private void ProcessTaskQueue(AIProcessingLevel level, float timeAllocation)
{
    var taskQueue = aiHierarchy.taskQueues[level];
    float remainingTime = timeAllocation;
    
    while (taskQueue.Count > 0 && remainingTime > 0)
    {
        var task = taskQueue.Dequeue();
        float taskTime = ExecuteAITask(task, level);
        
        remainingTime -= taskTime;
        
        // If task wasn't completed, re-queue for next frame
        if (!task.isCompleted)
        {
            taskQueue.Enqueue(task);
            break;
        }
    }
}
```

## Next Steps

1. **[UI/UX Design](./ui-ux-design.md)** - Interface design specifications
2. **[Tutorial Onboarding](./tutorial-onboarding.md)** - Learning system design
3. **[Events Crisis System](./events-crisis-system.md)** - Event system design

## Related Documents

- [Economy Balance Model](./economy-balance-model.md) - Economic balancing parameters
- [Simulation System](../architecture/simulation-system.md) - System architecture
- [Entity Generation](../architecture/entity-generation.md) - Entity creation algorithms