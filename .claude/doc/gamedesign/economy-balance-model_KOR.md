---
category: gamedesign
tags: [경제, 밸런스, 모델, 매개변수, 공식]
related: [capitalism-game-design-doc_KOR.md, core-gameplay-loop_KOR.md, investment-loop-mechanics_KOR.md]
parent: INDEX_KOR.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# 경제 밸런스 모델

[🇺🇸 English Version](./economy-balance-model.md)

## 📍 내비게이션

[↩️ 게임 디자인으로 돌아가기](./INDEX_KOR.md) | [📚 문서 색인](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 경제 밸런스 철학

### 1.1 설계 원칙

#### 현실적인 경제 역학
- **파레토 분포**: 부의 불평등은 실제 세계 패턴을 따름 (80/20 법칙)
- **시장 효율성**: 가격이 수요/공급을 통해 공정 가치로 수렴
- **경제 주기**: 시스템 역학에서 자연스러운 호황/불황 주기 발생
- **창발적 복잡성**: 단순한 규칙에서 복잡한 패턴이 나타남

#### 플레이어 경험 밸런스
- **점진적 난이도**: 초기 성공으로 자신감을 쌓고, 후기 도전으로 몰입도 유지
- **다양한 전략 경로**: 성공을 위한 단일 "최적" 경로 없음
- **위험/보상 균형**: 높은 위험은 비례적으로 높은 보상 제공
- **자동화 가치**: 복잡성이 증가함에 따라 자동화의 가치 증대

### 1.2 핵심 밸런스 지표

#### 경제 건강성 지표
```
GDP 성장률: 연 2-4% (건강한 경제)
인플레이션율: 연 1-3% (안정적인 물가)
실업률: 3-8% (현실적인 변동)
시장 변동성: 연 표준편차 15-25%
부의 지니 계수: 0.6-0.8 (현실적인 불평등)
```

## 2. 인구 경제 모델

### 2.1 소득 분배 수학

#### 파레토 분포 공식
```csharp
// 소득 생성을 위한 파레토 분포
public float GenerateParetoIncome(float alpha = 1.16f, float xMin = 25000f)
{
    float uniform = Random.Range(0.001f, 0.999f);
    return xMin * Mathf.Pow(1f - uniform, -1f / alpha);
}

// 소득 계층 임계값
public PopulationClass DetermineIncomeClass(float income)
{
    if (income < 30000f) return PopulationClass.LowIncome;    // 60%
    if (income < 75000f) return PopulationClass.MiddleClass;  // 35%
    return PopulationClass.HighIncome;                        // 5%
}
```

#### 소비 함수
```csharp
// 케인즈 소비 함수: C = a + b*Y
public float CalculateConsumption(float income, float wealth)
{
    float autonomousConsumption = 15000f; // 기본 필요
    float marginalConsumption = 0.75f;    // 소득의 75%
    float wealthEffect = 0.05f;           // 자산의 5%
    
    return autonomousConsumption + 
           (marginalConsumption * income) + 
           (wealthEffect * wealth * 0.01f); // 연간 자산 효과
}
```

### 2.2 행동 경제학 매개변수

#### 의사결정 요인
```csharp
[System.Serializable]
public struct BehaviorParameters
{
    [Header("위험 허용도")]
    public AnimationCurve riskByAge;           // 나이에 따라 위험 감소
    public AnimationCurve riskByWealth;        // 자산에 따라 위험 허용도 증가
    public float baseRiskAversion;             // 0.5-0.8 일반적인 범위
    
    [Header("사회적 영향")]
    public float conformityWeight;             // 0.3 - 타인을 따라 함
    public float informationWeight;            // 0.4 - 합리적 분석
    public float emotionWeight;                // 0.3 - 감정적 결정
    
    [Header("시간 선호")]
    public float discountRate;                 // 연 0.03-0.15
    public AnimationCurve patienceByEducation; // 고등교육 = 더 많은 인내
}
```

## 3. 회사 재무 모델

### 3.1 수익 생성

#### 기본 수익 공식
```csharp
public float CalculateCompanyRevenue(CompanyComponent company, MarketDynamicsComponent market)
{
    // 기본 생산 능력
    float productionCapacity = company.employeeCount * company.productivityIndex;
    
    // 시장 수요 요인
    float demandMultiplier = Mathf.Clamp(market.demandLevel / market.supplyLevel, 0.5f, 2.0f);
    
    // 산업별 승수
    float industryMultiplier = GetIndustryMultiplier(company.industry);
    
    // 회사 규모의 규모의 경제
    float scaleMultiplier = 1f + (company.employeeCount * 0.001f); // 큰 회사 = 더 효율적
    
    return productionCapacity * demandMultiplier * industryMultiplier * scaleMultiplier;
}

private float GetIndustryMultiplier(IndustryType industry)
{
    return industry switch
    {
        IndustryType.Technology => 2.0f,      // 고마진
        IndustryType.Finance => 1.8f,         // 고마진
        IndustryType.Healthcare => 1.5f,      // 안정적 수요
        IndustryType.Manufacturing => 1.2f,   // 중간 마진
        IndustryType.Retail => 1.0f,          // 기본 마진
        IndustryType.Agriculture => 0.8f,     // 저마진
        _ => 1.0f
    };
}
```

### 3.2 비용 구조

#### 운영 비용 모델
```csharp
[System.Serializable]
public struct OperatingCostModel
{
    [Header("고정 비용")]
    public float baseMonthlyCost;              // 기본 운영 비용
    public float employeeCostPerHead;          // 월 평균 $4000/인
    public float facilityCostPerEmployee;      // 직원당 월 임대료 $500
    
    [Header("변동 비용")]
    public float materialCostRatio;            // 0.4 (수익의 40%)
    public float marketingCostRatio;           // 0.05 (수익의 5%)
    public float rdCostRatio;                  // 0.03 (수익의 3%)
    
    [Header("금융 비용")]
    public float interestRate;                 // 0.05 (연 5%)
    public float taxRate;                      // 0.21 (법인세 21%)
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

## 4. 시장 역학

### 4.1 가격 발견 메커니즘

#### 수요와 공급 균형
```csharp
public void UpdateMarketPrice(ref MarketDynamicsComponent market)
{
    // 현재 공급과 수요 계산
    float totalSupply = CalculateIndustrySupply(market.industry);
    float totalDemand = CalculateIndustryDemand(market.industry);
    
    // 가격 탄력성 요인
    float priceElasticity = GetPriceElasticity(market.industry);
    float supplyElasticity = GetSupplyElasticity(market.industry);
    
    // 균형 가격 계산
    float equilibriumPrice = CalculateEquilibriumPrice(totalSupply, totalDemand, priceElasticity);
    
    // 가격 조정 속도 (극심한 변동성 방지)
    float adjustmentSpeed = 0.1f; // 업데이트당 10% 조정
    float priceChange = (equilibriumPrice - market.currentPrice) * adjustmentSpeed;
    
    // 무작위 시장 노이즈 적용
    float volatility = GetMarketVolatility(market.industry);
    float randomFactor = Random.Range(-volatility, volatility);
    
    market.currentPrice = Mathf.Max(0.1f, market.currentPrice + priceChange + randomFactor);
}

private float GetPriceElasticity(IndustryType industry)
{
    return industry switch
    {
        IndustryType.Healthcare => 0.2f,      // 비탄력적 (필수품)
        IndustryType.Agriculture => 0.3f,     // 비탄력적 (음식)
        IndustryType.Finance => 0.8f,         // 중간 탄력적
        IndustryType.Technology => 1.2f,      // 탄력적 (업그레이드)
        IndustryType.Retail => 1.5f,          // 탄력적 (재량 지출)
        _ => 1.0f
    };
}
```

### 4.2 경제 주기

#### 경기 주기 모델
```csharp
[System.Serializable]
public struct BusinessCycleParameters
{
    [Header("주기 시기")]
    public float expansionDuration;        // 60-120개월
    public float recessionDuration;        // 6-18개월
    public float recoveryDuration;         // 12-24개월
    
    [Header("경제적 영향")]
    public AnimationCurve gdpGrowthCycle;  // 주기 동안 GDP 성장
    public AnimationCurve unemploymentCycle; // 실업률 변화
    public AnimationCurve inflationCycle;   // 인플레이션율 변화
    public AnimationCurve marketSentiment;  // 시장 신뢰도
}

public void ApplyCyclicalEffects(float cyclePosition)
{
    // cyclePosition: 경기 주기에서의 위치를 나타내는 0-1
    
    float gdpMultiplier = businessCycle.gdpGrowthCycle.Evaluate(cyclePosition);
    float unemploymentRate = businessCycle.unemploymentCycle.Evaluate(cyclePosition);
    float inflationRate = businessCycle.inflationCycle.Evaluate(cyclePosition);
    
    // 모든 회사와 인구에 적용
    ApplyGDPEffects(gdpMultiplier);
    ApplyUnemploymentEffects(unemploymentRate);
    ApplyInflationEffects(inflationRate);
}
```

## 5. 투자 및 금융 시장

### 5.1 주식 평가 모델

#### 기본 평가
```csharp
public float CalculateStockValue(CompanyComponent company, FinancialComponent financial)
{
    // 할인 현금흐름(DCF) 모델
    float expectedGrowthRate = CalculateExpectedGrowth(company);
    float discountRate = GetDiscountRate(company.riskLevel);
    float terminalGrowthRate = 0.02f; // 장기 경제 성장률
    
    // 잉여 현금흐름 계산
    float freeCashFlow = financial.netProfit - financial.capitalExpenditure;
    
    // 5년 DCF 평가
    float presentValue = 0f;
    for (int year = 1; year <= 5; year++)
    {
        float projectedCashFlow = freeCashFlow * Mathf.Pow(1f + expectedGrowthRate, year);
        float discountFactor = Mathf.Pow(1f + discountRate, year);
        presentValue += projectedCashFlow / discountFactor;
    }
    
    // 터미널 가치
    float terminalCashFlow = freeCashFlow * Mathf.Pow(1f + expectedGrowthRate, 5f);
    float terminalValue = terminalCashFlow * (1f + terminalGrowthRate) / 
                         (discountRate - terminalGrowthRate);
    presentValue += terminalValue / Mathf.Pow(1f + discountRate, 5f);
    
    // 주당 가치
    return presentValue / company.sharesOutstanding;
}
```

## 6. 밸런스 매개변수

### 6.1 난이도 확장

#### 점진적 도전
```csharp
[System.Serializable]
public struct DifficultyParameters
{
    [Header("초기 게임 (0-6개월)")]
    public float earlyGameAdvantage;       // 1.2배 - 수익 내기 쉬움
    public float marketStability;          // 0.8배 - 변동성 낮음
    public float competitorAggression;     // 0.5배 - AI 덜 공격적
    
    [Header("중기 게임 (6-24개월)")]
    public float normalDifficulty;         // 1.0배 - 표준 매개변수
    public float increasedCompetition;     // 1.0배 - 일반적인 경쟁
    public float marketEfficiency;         // 1.0배 - 공정한 가격 책정
    
    [Header("후기 게임 (24개월 이상)")]
    public float advancedChallenge;        // 0.9배 - 기회 찾기 어려움
    public float smarterAI;                // 1.5배 - AI가 플레이어로부터 학습
    public float marketSaturation;         // 1.2배 - 쉬운 기회 적음
}
```

### 6.2 경제 현실성 매개변수

#### 실제 세계 보정
```yaml
population_parameters:
  income_distribution:
    median_income: 50000      # 연간 USD
    gini_coefficient: 0.7     # 부의 불평등
    poverty_rate: 0.12        # 빈곤선 이하 12%
  
  demographics:
    working_age_ratio: 0.65   # 근로 연령층 65%
    dependency_ratio: 0.55    # 근로자당 부양가족 수
    education_premium: 1.8    # 대학 교육 소득 배수

company_parameters:
  size_distribution:
    micro_ratio: 0.70         # 직원 10명 미만
    small_ratio: 0.25         # 10-50명
    medium_ratio: 0.04        # 50-250명
    large_ratio: 0.01         # 250명 초과
  
  financial_ratios:
    average_profit_margin: 0.08   # 순이익률 8%
    debt_to_equity_ratio: 0.4     # 레버리지 40%
    employee_cost_ratio: 0.35     # 수익의 35%

market_parameters:
  volatility:
    daily_volatility: 0.02        # 일일 2% 변동
    annual_volatility: 0.20       # 연간 20% 변동성
    crisis_volatility: 0.50       # 위기 시 50%
  
  efficiency:
    price_discovery_speed: 0.1    # 기간당 10% 조정
    information_delay: 2.0        # 2초 정보 지연
```

## 7. 밸런싱 도구 및 모니터링

### 7.1 실시간 밸런스 모니터링

#### 핵심 성과 지표
```csharp
[System.Serializable]
public struct BalanceMonitoringSystem
{
    [Header("경제 건강성")]
    public float targetGDPGrowth;          // 연 2-4%
    public float targetInflation;          // 연 2%
    public float targetUnemployment;       // 자연 실업률 5%
    
    [Header("플레이어 경험")]
    public float targetWinRate;            // 결정의 60%가 수익성 있음
    public float targetEngagement;         // 세션당 플레이 시간(분)
    public AnimationCurve difficultyCurve; // 도전 진행
    
    [Header("시장 안정성")]
    public float maxVolatility;            // 최대 30% 변동성
    public float minLiquidity;             // 최소 거래량
    public float fairValueDeviation;       // 공정 가치에서 최대 20% 편차
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

### 7.2 동적 밸런스 조정

#### 적응형 난이도 시스템
```csharp
public void AdjustBalance(PlayerPerformanceData performance)
{
    float performanceScore = CalculatePerformanceScore(performance);
    
    // 플레이어 성공에 따른 시장 조건 조정
    if (performanceScore > 0.8f) // 플레이어가 너무 성공적
    {
        IncreaseCompetition();
        ReduceMarketOpportunities();
        IncreaseEventFrequency();
    }
    else if (performanceScore < 0.4f) // 플레이어가 고전
    {
        ProvideMarketOpportunities();
        ReduceRandomEvents();
        ImproveInformationQuality();
    }
}
```

## 8. 테스트 및 검증

### 8.1 경제 모델 테스트

#### 통계적 검증
- **소득 분배**: 파레토 분포가 실제 데이터와 일치하는지 검증
- **시장 효율성**: 가격 발견이 균형에 도달하는지 테스트
- **경기 주기**: 현실적인 호황/불황 패턴 발생 검증
- **플레이어 진행**: 만족스러운 난이도 곡선 확인

#### 밸런스 테스트 시나리오
1. **경기 침체 시뮬레이션**: 경제가 18개월 침체를 버티는지
2. **인플레이션 충격**: 시스템이 10% 인플레이션율에 적응하는지
3. **시장 붕괴**: 6-12개월 내 회복하는지
4. **플레이어 전략**: 성공을 위한 다양한 경로 존재하는지

### 8.2 반복 및 개선

#### 지속적 개선 프로세스
1. **데이터 수집**: 플레이어 행동과 경제 지표 모니터링
2. **분석**: 불균형과 문제점 식별
3. **가설**: 밸런스 변경 제안
4. **테스트**: 플레이어 그룹으로 A/B 테스트
5. **구현**: 성공적인 밸런스 업데이트 배포

## 다음 단계

1. **[진행 시스템](./progression-system_KOR.md)** - 플레이어 발전과 잠금 해제
2. **[AI 행동 패턴](./ai-behavior-patterns_KOR.md)** - AI 결정 알고리즘  
3. **[UI/UX 디자인](./ui-ux-design_KOR.md)** - 인터페이스 사양

## 관련 문서

- [핵심 게임플레이 루프](./core-gameplay-loop_KOR.md) - 메인 게임플레이 시스템
- [투자 루프 메커니즘](./investment-loop-mechanics_KOR.md) - 투자 시스템 세부사항
- [구현 로드맵](../architecture/implementation-roadmap_KOR.md) - 기술적 개발 계획
