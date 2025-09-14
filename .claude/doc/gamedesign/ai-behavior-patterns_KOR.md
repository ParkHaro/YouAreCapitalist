---
category: gamedesign
tags: [ai, 행동, 패턴, 의사결정, 알고리즘]
related: [economy-balance-model_KOR.md, simulation-system_KOR.md, entity-generation_KOR.md]
parent: INDEX_KOR.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# AI 행동 패턴

[🇺🇸 English Version](./ai-behavior-patterns.md)

## 📍 내비게이션

[↩️ 게임 디자인으로 돌아가기](./INDEX_KOR.md) | [📚 문서 색인](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. AI 행동 철학

### 1.1 설계 원칙

#### 현실적인 경제 주체
- **제한된 합리성**: AI 개체는 제한된 정보로 불완전한 결정을 내림
- **다양한 동기**: 다른 성격 유형이 다양한 경제적 행동을 이끎
- **적응 학습**: AI는 변화하는 시장 조건과 플레이어 행동에 적응
- **창발적 복잡성**: 단순한 개별 규칙에서 복잡한 시장 패턴이 나타남

#### 플레이어 상호작용 디자인
- **도전적인 대립**: AI는 불공정하지 않으면서도 의미 있는 경쟁 제공
- **교육 기회**: AI의 실수와 성공이 학습 순간을 제공
- **시장 현실성**: AI 행동이 믿을 만한 시장 조건 창조
- **확장 가능한 지능**: AI 난이도가 플레이어 기술 수준에 맞춰 조정

### 1.2 AI 개체 카테고리

#### 인구 AI (소비자)
- **주요 목표**: 개인 효용과 재정 보안 극대화
- **결정 범위**: 고용, 소비, 저축, 기본 투자
- **행동 동인**: 위험 허용도, 사회 계층, 인생 단계, 교육
- **업데이트 빈도**: 주요 결정은 일일, 사소한 조정은 시간별

#### 회사 AI (비즈니스)
- **주요 목표**: 장기 주주 가치 극대화
- **결정 범위**: 생산, 고용, 가격 책정, 확장, 인수합병
- **행동 동인**: 산업 역학, 경쟁 위치, 재정 건강
- **업데이트 빈도**: 전략적 결정은 월별, 운영은 주별

#### 투자자 AI (자본가)
- **주요 목표**: 우수한 위험 조정 수익 창출
- **결정 범위**: 자산 배분, 증권 선택, 타이밍, 레버리지
- **행동 동인**: 투자 철학, 위험 능력, 시장 전망
- **업데이트 빈도**: 전술적 결정은 실시간, 전략적은 분기별

## 2. 인구 AI 행동

### 2.1 의사결정 프레임워크

#### 효용 극대화 모델
```csharp
[System.Serializable]
public struct PopulationUtilityFunction
{
    [Header("기본 필요")]
    public float survivalWeight;          // 0.4 - 음식, 주거, 안전
    public float comfortWeight;           // 0.3 - 생활 수준 향상
    public float securityWeight;          // 0.2 - 재정 보안, 보험
    public float statusWeight;            // 0.1 - 사회적 지위, 명성
    
    [Header("시간 선호")]
    public float presentBias;             // 0.7 - 현재 vs 미래 효용
    public AnimationCurve discountCurve;  // 미래 가치 할인 방식
    
    [Header("위험 태도")]
    public float riskAversion;            // 0.6 - 보수적 vs 공격적
    public float lossAversion;            // 2.0 - 손실이 이익보다 2배 무게
}

public float CalculateUtility(PopulationComponent pop, DecisionOption option)
{
    float baseUtility = 0f;
    
    // 각 필요 카테고리에서 효용 계산
    baseUtility += option.survivalValue * pop.utilityFunction.survivalWeight;
    baseUtility += option.comfortValue * pop.utilityFunction.comfortWeight;
    baseUtility += option.securityValue * pop.utilityFunction.securityWeight;
    baseUtility += option.statusValue * pop.utilityFunction.statusWeight;
    
    // 시간 선호 할인 적용
    float timeDiscount = pop.utilityFunction.discountCurve.Evaluate(option.timeHorizon);
    baseUtility *= timeDiscount;
    
    // 위험 조정 적용
    float riskPenalty = option.riskLevel * pop.utilityFunction.riskAversion;
    baseUtility -= riskPenalty;
    
    // 부정적 결과에 대한 손실 회피 적용
    if (option.expectedValue < 0)
    {
        baseUtility *= pop.utilityFunction.lossAversion;
    }
    
    return baseUtility;
}
```

#### 행동경제학 통합
```csharp
[System.Serializable]
public struct CognitiveBiases
{
    [Header("정보 처리")]
    public float confirmationBias;        // 0.3 - 확증 정보 추구
    public float availabilityHeuristic;   // 0.4 - 최근 사건이 더 가능성 있게 보임
    public float anchoringBias;           // 0.5 - 첫 정보가 과도하게 영향력 행사
    
    [Header("사회적 영향")]
    public float herdBehavior;            // 0.6 - 군중 결정 따라 하기
    public float authorityBias;           // 0.4 - 전문가 의견 신뢰
    public float socialProofWeight;       // 0.5 - 타인의 행동이 선택에 영향
    
    [Header("시간적 편향")]
    public float hyperbolicDiscounting;   // 0.8 - 즉각적 보상 과중시
    public float planningFallacy;         // 0.3 - 시간/비용 과소평가
    public float statusQuoBias;           // 0.7 - 현재 상황 선호
}

public void ApplyCognitiveBiases(ref DecisionOption option, PopulationComponent pop, MarketContext context)
{
    var biases = pop.cognitiveBiases;
    
    // 확증 편향 - 기존 믿음을 확인하는 정보 추구
    if (option.alignsWithBeliefs)
    {
        option.perceivedValue *= (1f + biases.confirmationBias);
    }
    
    // 가용성 휴리스틱 - 최근 사건이 더 가능성 있게 보임
    if (context.recentSimilarEvents > 0)
    {
        float availabilityBoost = biases.availabilityHeuristic * context.recentSimilarEvents;
        option.perceivedProbability += availabilityBoost;
    }
    
    // 군중 행동 - 타인이 하는 것을 따라 함
    float crowdFactor = context.percentageDoingSame * biases.herdBehavior;
    option.socialUtility += crowdFactor;
    
    // 현상 유지 편향 - 현재 상황 선호
    if (option.requiresChange)
    {
        option.perceivedCost *= (1f + biases.statusQuoBias);
    }
}
```

### 2.2 고용 결정 AI

#### 구직 알고리즘
```csharp
public partial struct EmploymentDecisionSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (entity, pop, economic, decision) in 
                 SystemAPI.Query<Entity, PopulationComponent, EconomicStatusComponent, DecisionComponent>()
                          .WithAll<UnemployedTag>())
        {
            // 사용 가능한 모든 직업 기회 평가
            var jobOptions = FindAvailableJobs(pop.skillLevel, pop.education, pop.location);
            
            if (jobOptions.Length == 0)
            {
                // 직업이 없으면 기대치 낮추기
                pop.reservationWage *= 0.95f; // 최소 수용 가능 임금 감소
                decision.searchIntensity += 0.1f; // 더 열심히 찾기
                continue;
            }
            
            // 각 직업 기회 점수 매기기
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
            
            // 직업 결정하기
            if (bestJob != null && ShouldAcceptJob(bestJob, pop, economic))
            {
                AcceptJobOffer(entity, bestJob, ref state);
            }
            else
            {
                // 계속 찾기, 찾기 전략 조정
                AdjustJobSearchStrategy(ref pop, jobOptions);
            }
        }
    }
    
    private float EvaluateJobOption(JobOption job, PopulationComponent pop, EconomicStatusComponent economic)
    {
        float score = 0f;
        
        // 임금 구성 요소 (가장 중요)
        float wageUtility = job.salary / pop.reservationWage;
        score += wageUtility * 0.5f;
        
        // 위치 편의성
        float commutePenalty = CalculateCommutePenalty(job.location, pop.location);
        score -= commutePenalty * 0.2f;
        
        // 경력 발전 잠재력
        float careerValue = job.skillGrowthPotential * pop.careerAmbition;
        score += careerValue * 0.2f;
        
        // 직업 안정성
        float securityValue = job.jobSecurity * pop.riskAversion;
        score += securityValue * 0.1f;
        
        return score;
    }
}
```

### 2.3 소비 결정 AI

#### 지출 행동 모델
```csharp
[System.Serializable]
public struct ConsumptionBehaviorAI
{
    [Header("지출 카테고리")]
    public float necessitySpending;       // 0.5 - 필수 지출
    public float comfortSpending;         // 0.3 - 생활 수준 향상
    public float socialSpending;          // 0.1 - 지위/사회적 신호
    public float impulsiveSpending;       // 0.1 - 계획되지 않은 구매
    
    [Header("결정 요인")]
    public AnimationCurve incomeElasticity; // 지출 vs 소득 관계
    public float priceElasticity;         // 가격 변화에 대한 반응
    public float brandLoyalty;           // 익숙한 브랜드 선호
    public float qualityPreference;      // 품질에 대한 지불 의사
}

public ConsumptionDecision MakeConsumptionDecision(PopulationComponent pop, 
                                                  EconomicStatusComponent economic,
                                                  ProductOption[] availableProducts)
{
    var behavior = pop.consumptionBehavior;
    float availableBudget = economic.monthlyIncome * economic.consumptionRate;
    
    var decision = new ConsumptionDecision();
    
    // 카테고리별 예산 배분
    decision.necessityBudget = availableBudget * behavior.necessitySpending;
    decision.comfortBudget = availableBudget * behavior.comfortSpending;
    decision.socialBudget = availableBudget * behavior.socialSpending;
    decision.impulsiveBudget = availableBudget * behavior.impulsiveSpending;
    
    // 각 카테고리에서 최적 제품 선택
    decision.selectedProducts = new List<ProductPurchase>();
    
    // 필수품 구매 (음식, 공과금, 임대료)
    var necessityProducts = availableProducts.Where(p => p.category == ProductCategory.Necessity);
    SelectOptimalProducts(necessityProducts, decision.necessityBudget, behavior, ref decision);
    
    // 편의품 구매 (오락, 외식, 취미)
    var comfortProducts = availableProducts.Where(p => p.category == ProductCategory.Comfort);
    SelectOptimalProducts(comfortProducts, decision.comfortBudget, behavior, ref decision);
    
    // 사회적 구매 (패션, 자동차, 휴가)
    var socialProducts = availableProducts.Where(p => p.category == ProductCategory.Social);
    SelectOptimalProducts(socialProducts, decision.socialBudget, behavior, ref decision);
    
    // 충동 구매 (무작위, 감정 주도)
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

## 3. 회사 AI 행동

### 3.1 비즈니스 전략 AI

#### 전략적 결정 프레임워크
```csharp
[System.Serializable]
public struct CompanyStrategyAI
{
    [Header("전략적 방향")]
    public BusinessStrategy primaryStrategy;   // 비용 우위, 차별화 등
    public float riskTolerance;               // 0.3 보수적, 0.8 공격적
    public float growthAmbition;              // 0.5 안정적, 0.9 급속 확장
    public float innovationFocus;             // R&D 투자 성향
    
    [Header("결정 가중치")]
    public float profitabilityWeight;         // 0.4 - 단기 수익
    public float marketShareWeight;           // 0.3 - 시장 지배력
    public float sustainabilityWeight;        // 0.2 - 장기 생존력
    public float stakeholderWeight;           // 0.1 - 직원/고객 만족
    
    [Header("경쟁 대응")]
    public float competitorAwareness;         // 경쟁자 주시 정도
    public float firstMoverAdvantage;         // 선발자 되려는 의지
    public float imitationSpeed;              // 경쟁자 행동 복사 속도
}

public BusinessDecision MakeStrategicDecision(CompanyComponent company, 
                                            MarketContext market,
                                            CompetitorAction[] recentActions)
{
    var strategy = company.strategyAI;
    var decision = new BusinessDecision();
    
    // 시장 조건 분석
    float marketAttractiveness = AnalyzeMarketConditions(market);
    float competitivePressure = AnalyzeCompetitivePressure(recentActions);
    float resourceConstraints = AnalyzeResourceConstraints(company);
    
    // 전략적 옵션 생성
    var options = GenerateStrategicOptions(company, market, strategy);
    
    // 각 옵션 평가
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
    
    // 결정 실행
    if (bestOption != null)
    {
        decision = ConvertToBusinessDecision(bestOption, company);
        
        // 결정에 기반한 전략 업데이트
        UpdateStrategyFromDecision(ref strategy, bestOption, market);
    }
    
    return decision;
}
```

#### 가격 전략 AI
```csharp
[System.Serializable]
public struct PricingStrategyAI
{
    [Header("가격 철학")]
    public PricingStrategy strategy;          // 침투, 스키밍, 경쟁적
    public float priceElasticityEstimate;     // 가격 변화에 대한 수요 반응
    public float competitorResponseSpeed;     // 경쟁자 반응 속도
    
    [Header("최적화 매개변수")]
    public float profitMarginTarget;          // 원하는 이익률
    public float marketShareImportance;       // 점유율 vs 마진 가격
    public float brandPremiumCapacity;        // 프리미엄 책정 능력
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
    
    // 동적 조정 적용
    optimalPrice = ApplyDynamicPricingAdjustments(optimalPrice, market, company);
    
    // 가격 범위 검증
    float minPrice = product.marginalCost * 1.1f; // 최소 10% 마진
    float maxPrice = market.averagePrice * 2.0f;  // 시장 평균의 최대 2배
    
    return Mathf.Clamp(optimalPrice, minPrice, maxPrice);
}
```

## 4. 투자자 AI 행동

### 4.1 투자 전략 AI

#### 포트폴리오 구성 알고리즘
```csharp
[System.Serializable]
public struct InvestmentStrategyAI
{
    [Header("투자 철학")]
    public InvestmentStyle style;            // 가치, 성장, 모멘텀 등
    public float riskTolerance;             // 0.3 보수적, 0.8 공격적
    public int investmentHorizon;           // 일반적인 보유 기간 (월)
    
    [Header("포트폴리오 관리")]
    public float diversification_target;     // 단일 포지션 최대 %
    public float cashBufferPercent;         // 기회를 위한 현금 배분
    public float rebalanceThreshold;        // 리밸런싱 전 편차
    
    [Header("의사결정")]
    public float fundamentalWeight;         // 0.6 - 기본 분석 가중치
    public float technicalWeight;           // 0.3 - 기술 분석 가중치  
    public float sentimentWeight;           // 0.1 - 시장 심리 가중치
}

public InvestmentDecision MakeInvestmentDecision(InvestorAI investor,
                                               SecurityOption[] availableSecurities,
                                               MarketContext market,
                                               PortfolioState currentPortfolio)
{
    var strategy = investor.investmentStrategy;
    var decision = new InvestmentDecision();
    
    // 시장 조건 분석
    MarketRegime regime = AnalyzeMarketRegime(market);
    
    // 투자 스타일에 따른 증권 스크리닝
    var screenedSecurities = ScreenSecurities(availableSecurities, strategy.style, regime);
    
    // 각 증권 평가
    var securityScores = new Dictionary<SecurityOption, float>();
    
    foreach (var security in screenedSecurities)
    {
        float score = EvaluateSecurity(security, strategy, market, regime);
        securityScores[security] = score;
    }
    
    // 포트폴리오 최적화
    var topSecurities = securityScores
        .OrderByDescending(kvp => kvp.Value)
        .Take(20)  // 상위 20개 후보 고려
        .ToArray();
    
    // 최적 포트폴리오 구성
    decision.portfolioChanges = OptimizePortfolio(
        topSecurities, 
        currentPortfolio, 
        strategy,
        investor.availableCash
    );
    
    // 위험 관리 오버레이
    ApplyRiskManagement(ref decision, strategy, market);
    
    return decision;
}
```

#### 위험 관리 AI
```csharp
[System.Serializable]  
public struct RiskManagementAI
{
    [Header("포지션 사이징")]
    public float maxPositionSize;            // 단일 포지션 최대 %
    public float correlationLimit;           // 포지션 간 최대 상관관계
    public float sectorConcentrationLimit;   // 단일 섹터 최대 %
    
    [Header("손절매 전략")]
    public bool useStopLosses;              // 손절매 사용 여부
    public float stopLossPercent;           // -15% 일반적인 손절매
    public float trailingStopPercent;       // 추적 손절매 거리
    
    [Header("헤징")]
    public float hedgeRatio;                // 포트폴리오 헤징 %
    public HedgingInstrument[] hedgingTools; // 사용 가능한 헤징 도구
    public float volatilityThreshold;       // 헤징 유발하는 VIX 수준
}

public void ApplyRiskManagement(ref InvestmentDecision decision,
                               InvestmentStrategyAI strategy,
                               MarketContext market)
{
    var risk = strategy.riskManagement;
    
    // 포지션 사이징 규칙
    foreach (var change in decision.portfolioChanges)
    {
        // 개별 포지션 크기 제한
        float maxSize = decision.totalPortfolioValue * risk.maxPositionSize;
        change.targetValue = Mathf.Min(change.targetValue, maxSize);
        
        // 섹터 집중도 확인
        float sectorExposure = CalculateSectorExposure(change.security.sector, decision);
        if (sectorExposure > risk.sectorConcentrationLimit)
        {
            change.targetValue *= (risk.sectorConcentrationLimit / sectorExposure);
        }
    }
    
    // 시장 변동성이 높으면 헤징 적용
    if (market.volatilityIndex > risk.volatilityThreshold)
    {
        var hedgeTrade = CreateHedgingTrade(decision, risk, market);
        if (hedgeTrade != null)
        {
            decision.portfolioChanges.Add(hedgeTrade);
        }
    }
    
    // 새 포지션에 손절매 설정
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

## 5. 적응 학습 시스템

### 5.1 기계 학습 통합

#### AI 행동을 위한 강화 학습
```csharp
[System.Serializable]
public struct ReinforcementLearningAI
{
    [Header("학습 매개변수")]
    public float learningRate;               // 0.01 - 적응 속도
    public float explorationRate;            // 0.1 - 무작위 행동 확률
    public float discountFactor;             // 0.95 - 미래 보상 할인
    
    [Header("경험 재생")]
    public int replayBufferSize;             // 10000 - 저장된 경험
    public int batchSize;                    // 32 - 훈련 배치 크기
    public int updateFrequency;              // 100번 행동마다
    
    [Header("신경망")]
    public int[] hiddenLayers;               // [128, 64] - 네트워크 구조
    public ActivationFunction activation;    // ReLU, Sigmoid 등
    public float dropout_rate;               // 0.2 - 정규화
}

public void UpdateAIBehavior(AIEntity entity, ActionResult result)
{
    var rl = entity.reinforcementLearning;
    
    // 경험을 재생 버퍼에 저장
    var experience = new Experience
    {
        state = result.previousState,
        action = result.action,
        reward = result.reward,
        nextState = result.currentState,
        done = result.episodeComplete
    };
    
    rl.replayBuffer.Add(experience);
    
    // 주기적으로 신경망 훈련
    if (rl.stepCount % rl.updateFrequency == 0 && 
        rl.replayBuffer.Count >= rl.batchSize)
    {
        var batch = rl.replayBuffer.Sample(rl.batchSize);
        TrainNetwork(entity.neuralNetwork, batch, rl);
    }
    
    // 탐험율 업데이트 (엡실론 감소)
    rl.explorationRate *= 0.995f;
    rl.explorationRate = Mathf.Max(rl.explorationRate, 0.01f);
    
    rl.stepCount++;
}
```

### 5.2 행동 진화

#### 전략 진화를 위한 유전자 알고리즘
```csharp
[System.Serializable]
public struct GeneticAlgorithmAI
{
    [Header("인구 매개변수")]
    public int populationSize;              // 50 - AI 개체 수
    public int generations;                 // 100 - 진화 반복
    public float mutationRate;              // 0.1 - 무작위 돌연변이 확률
    
    [Header("선택 전략")]
    public SelectionMethod selectionMethod; // 토너먼트, 룰렛 등
    public float elitismRate;              // 0.1 - 최고 성과자 보존
    public int tournamentSize;             // 5 - 토너먼트 선택 크기
}

public void EvolveAIPopulation(AIEntity[] population, float[] fitnessScores)
{
    var ga = geneticAlgorithm;
    
    // 선택: 다음 세대를 위한 부모 선택
    var parents = SelectParents(population, fitnessScores, ga);
    
    // 새 세대 생성
    var newGeneration = new AIEntity[ga.populationSize];
    
    // 엘리트주의: 최고 성과자 보존
    int eliteCount = Mathf.RoundToInt(ga.populationSize * ga.elitismRate);
    var elite = population.OrderByDescending(ai => ai.fitness).Take(eliteCount);
    
    for (int i = 0; i < eliteCount; i++)
    {
        newGeneration[i] = elite.ElementAt(i).Clone();
    }
    
    // 나머지 인구를 위한 교차와 돌연변이
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
    
    // 이전 인구 교체
    Array.Copy(newGeneration, population, ga.populationSize);
}
```

## 6. 성능 최적화

### 6.1 행동 캐싱

#### 결정 캐싱 시스템
```csharp
[System.Serializable]
public struct DecisionCache
{
    public Dictionary<StateHash, CachedDecision> cache;
    public int maxCacheSize;                 // 1000개 항목
    public float cacheValidityTime;          // 60초
    public float similarityThreshold;        // 0.95 - 상태 유사성
}

public DecisionResult GetCachedDecision(AIEntity entity, GameState currentState)
{
    var cache = entity.decisionCache;
    var stateHash = CalculateStateHash(currentState);
    
    if (cache.cache.ContainsKey(stateHash))
    {
        var cached = cache.cache[stateHash];
        
        // 캐시가 여전히 유효한지 확인
        if (Time.time - cached.timestamp < cache.cacheValidityTime)
        {
            return cached.decision;
        }
        else
        {
            // 만료된 항목 제거
            cache.cache.Remove(stateHash);
        }
    }
    
    // 유사한 상태 확인
    foreach (var kvp in cache.cache)
    {
        float similarity = CalculateStateSimilarity(currentState, kvp.Value.state);
        if (similarity > cache.similarityThreshold)
        {
            return kvp.Value.decision;
        }
    }
    
    return null; // 캐시된 결정을 찾지 못함
}
```

## 다음 단계

1. **[UI/UX 디자인](./ui-ux-design_KOR.md)** - 인터페이스 디자인 사양
2. **[튜토리얼 온보딩](./tutorial-onboarding_KOR.md)** - 학습 시스템 디자인
3. **[이벤트 위기 시스템](./events-crisis-system_KOR.md)** - 동적 이벤트 및 위기 관리

## 관련 문서

- [경제 밸런스 모델](./economy-balance-model_KOR.md) - 경제 밸런스 매개변수
- [시뮬레이션 시스템](../architecture/simulation-system_KOR.md) - 기술적 시뮬레이션 구조
- [개체 생성](../architecture/entity-generation_KOR.md) - AI 개체 생성 시스템