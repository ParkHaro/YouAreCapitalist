---
category: gamedesign
tags: [진행, 레벨, 잠금해제, 업적, 마일스톤]
related: [capitalism-game-design-doc_KOR.md, economy-balance-model_KOR.md, core-gameplay-loop_KOR.md]
parent: INDEX_KOR.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# 진행 시스템

[🇺🇸 English Version](./progression-system.md)

## 📍 내비게이션

[↩️ 게임 디자인으로 돌아가기](./INDEX_KOR.md) | [📚 문서 색인](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 진행 철학

### 1.1 설계 원칙

#### 자본주의 학습 곡선
- **점진적 복잡성**: 단순한 투자로 시작하여 점진적으로 복잡한 금융 상품 잠금 해제
- **현실적인 시간표**: 개인 투자자에서 제국 건설자까지의 실제 자본주의 여정을 반영
- **다양한 경로**: 다양한 투자 전략의 전문화 허용
- **의미 있는 마일스톤**: 각 잠금 해제는 자본주의 수준의 실질적인 진전을 나타냄

#### 플레이어 동기 프레임워크
- **성과 인정**: 성공적인 자본주의 결정에 대한 명확한 피드백
- **지식 구축**: 각 레벨마다 새로운 경제 개념 교육
- **지위 상징**: 명망 있는 투자와 부동산 잠금 해제
- **자동화 보상**: 높은 레벨에서 더 나은 자동화 기능 제공

### 1.2 진행 기둥

#### 자본 성장 진행
- **순자산 마일스톤**: 전통적인 부의 축적 지표
- **현금흐름 성취**: 수동 소득 생성 목표
- **포트폴리오 다변화**: 투자 유형 및 지리적 분산
- **시장 영향력**: 시장 조건에 영향을 미칠 수 있는 능력

#### 지식 진행
- **경제적 문해력**: 금융 개념의 이해
- **시장 분석**: 경제 지표 해석 능력
- **위험 관리**: 정교한 포트폴리오 균형 기술
- **전략적 사고**: 장기 자본 배분 계획

## 2. 레벨 구조

### 2.1 진행 단계

#### 1단계: 개인 투자자 (레벨 1-10)
**테마**: 개인 부 구축 기초
**기간**: 일반적인 플레이 시간 2-4주
**핵심 학습**: 기본 투자 원칙

```csharp
[System.Serializable]
public struct ProgressionTier
{
    [Header("1단계: 개인 투자자")]
    public int startLevel;                    // 1
    public int endLevel;                      // 10
    public float requiredCapital;             // $100K - $1M
    public string[] unlockedFeatures;         // 기본 주식, 채권, 저축
    public string themeDescription;           // "개인 부 구축"
}
```

#### 2단계: 포트폴리오 관리자 (레벨 11-25) 
**테마**: 다변화된 투자 전략
**기간**: 일반적인 플레이 시간 4-8주
**핵심 학습**: 포트폴리오 이론과 위험 관리

#### 3단계: 엔젤 투자자 (레벨 26-40)
**테마**: 사모 펀드 및 스타트업 투자  
**기간**: 일반적인 플레이 시간 6-12주
**핵심 학습**: 회사 평가와 성장 투자

#### 4단계: 투자 펀드 매니저 (레벨 41-60)
**테마**: 타인의 자금 관리
**기간**: 일반적인 플레이 시간 8-16주  
**핵심 학습**: 펀드 관리와 기관 투자

#### 5단계: 마켓 메이커 (레벨 61-80)
**테마**: 시장 조작과 차익거래
**기간**: 일반적인 플레이 시간 12-24주
**핵심 학습**: 고급 거래 전략과 시장 심리

#### 6단계: 경제 영향력자 (레벨 81-100)
**테마**: 시스템적 시장 영향
**기간**: 지속적인 엔드게임 콘텐츠
**핵심 학습**: 거시경제 정책과 부의 집중

### 2.2 레벨 요구사항 매트릭스

#### 경험치 획득 소스
```csharp
[System.Serializable]
public struct ExperienceGainConfig
{
    [Header("투자 행동")]
    public float profitableTradeXP;          // 수익 $1000당 10 XP
    public float portfolioRebalanceXP;       // 리밸런스당 50 XP
    public float newInvestmentTypeXP;        // 첫 투자 시 100 XP
    
    [Header("사업 활동")]
    public float companyIPOParticipationXP;  // IPO당 200 XP
    public float mergerAcquisitionXP;        // M&A 거래당 500 XP
    public float marketInfluenceXP;          // 시장 이벤트 유발 시 1000 XP
    
    [Header("지식 구축")]
    public float economicEventPredictionXP;  // 올바른 예측 시 150 XP
    public float marketAnalysisXP;           // 분석 완료 시 75 XP
    public float tutorialCompletionXP;       // 튜토리얼 섹션당 250 XP
    
    [Header("자동화 숙련")]
    public float automationSetupXP;          // 자동화 규칙당 300 XP
    public float passiveIncomeXP;            // 수동소득 $1000당 5 XP
}
```

#### 레벨링 공식
```csharp
public int CalculateRequiredXP(int level)
{
    // 수확체감 지수 성장
    float baseXP = 1000f;
    float growthFactor = 1.15f;
    float levelPenalty = level * 50f; // 선형 증가
    
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

## 3. 잠금해제 시스템

### 3.1 투자 상품 진행

#### 레벨 기반 잠금해제
```csharp
[System.Serializable]
public struct InvestmentUnlockConfig
{
    [Header("기본 투자 (레벨 1-10)")]
    public InvestmentType[] basicInvestments = {
        InvestmentType.SavingsAccount,        // 레벨 1
        InvestmentType.GovernmentBonds,       // 레벨 2
        InvestmentType.BlueChipStocks,        // 레벨 3
        InvestmentType.MutualFunds,           // 레벨 5
        InvestmentType.IndexFunds,            // 레벨 7
        InvestmentType.CorporateBonds         // 레벨 10
    };
    
    [Header("중간 투자 (레벨 11-25)")]
    public InvestmentType[] intermediateInvestments = {
        InvestmentType.GrowthStocks,          // 레벨 12
        InvestmentType.ValueStocks,           // 레벨 15
        InvestmentType.InternationalFunds,    // 레벨 18
        InvestmentType.SectorETFs,            // 레벨 20
        InvestmentType.REITs,                 // 레벨 22
        InvestmentType.CommodityFunds         // 레벨 25
    };
    
    [Header("고급 투자 (레벨 26-40)")]
    public InvestmentType[] advancedInvestments = {
        InvestmentType.PrivateEquity,         // 레벨 28
        InvestmentType.StartupInvestments,    // 레벨 30
        InvestmentType.HedgeFunds,           // 레벨 32
        InvestmentType.VentureCapital,       // 레벨 35
        InvestmentType.DirectRealEstate,     // 레벨 38
        InvestmentType.Art_Collectibles      // 레벨 40
    };
}
```

#### 성과 기반 잠금해제
```csharp
[System.Serializable]
public struct PerformanceUnlock
{
    public InvestmentType investmentType;
    public float requiredROI;              // 연 15%
    public int minimumDuration;            // 6개월
    public float riskTolerance;            // 수용 가능한 최대 변동성
    public string unlockDescription;       // "6개월간 15% ROI 달성"
}
```

### 3.2 기능 잠금해제 진행

#### 자동화 기능
```csharp
public enum AutomationFeature
{
    BasicRebalancing,        // 레벨 8  - 간단한 60/40 포트폴리오 리밸런싱
    DollarCostAveraging,     // 레벨 12 - 정기적인 자동 투자  
    StopLossOrders,          // 레벨 15 - 위험 관리 자동화
    TaxLossHarvesting,       // 레벨 20 - 세금 최적화
    SmartRebalancing,        // 레벨 25 - 고급 포트폴리오 최적화
    AdvancedScreening,       // 레벨 30 - AI 기반 종목 스크리닝
    MarketTimingAlerts,      // 레벨 35 - 경제 지표 자동화
    PortfolioInsurance,      // 레벨 40 - 동적 헤징 전략
    AlgorithmicTrading,      // 레벨 50 - 커스텀 트레이딩 알고리즘
    MarketMaking,            // 레벨 60 - 시장 유동성 제공
    SystemicHedging          // 레벨 75 - 경제 전반 위험 관리
}
```

#### 분석 도구
```csharp
[System.Serializable]  
public struct AnalysisToolUnlock
{
    [Header("기본 분석 (레벨 1-15)")]
    public string[] basicTools = {
        "가격 차트",              // 레벨 1
        "거래량 분석",           // 레벨 3  
        "이동평균",             // 레벨 5
        "P/E 비율 계산기",       // 레벨 7
        "배당수익률 추적기",      // 레벨 10
        "섹터 성과",            // 레벨 12
        "시가총액 분석"         // 레벨 15
    };
    
    [Header("고급 분석 (레벨 16-40)")]
    public string[] advancedTools = {
        "기술적 지표",          // 레벨 18
        "기본 분석",           // 레벨 20
        "리스크 지표",         // 레벨 22
        "상관관계 분석",        // 레벨 25
        "옵션 그리스",         // 레벨 28
        "몬테카를로 시뮬레이션", // 레벨 30
        "시나리오 분석",        // 레벨 35
        "거시경제 지표"        // 레벨 40
    };
}
```

### 3.3 명성과 평판 시스템

#### 사회적 지위 레벨
```csharp
public enum SocialStatus
{
    RetailInvestor,          // 0-$100K 순자산
    AccreditedInvestor,      // $1M+ 순자산  
    QualifiedPurchaser,      // $5M+ 투자 가능 자산
    InstitutionalInvestor,   // $25M+ 관리 자산
    FamilyOffice,            // $100M+ 가족 재산
    SovereignWealth,         // $1B+ 영향력
    EconomicRoyalty          // $10B+ 시스템적 영향력
}
```

#### 평판 혜택
```csharp
[System.Serializable]
public struct ReputationBenefits
{
    [Header("접근 혜택")]
    public float betterDealFlow;           // 20% 더 많은 투자 기회
    public float reducedFees;              // 15% 낮은 관리 수수료
    public float earlyInformation;         // 24시간 먼저 받는 시장 정보
    
    [Header("영향력 혜택")]
    public float marketImpact;             // 시장을 움직일 수 있는 능력
    public float politicalAccess;          // 정책 결정에 영향을 미침
    public float exclusiveDeals;           // 사모 투자 접근권
    
    [Header("자동화 혜택")]
    public float smarterAlgorithms;        // 고급 AI 트레이딩 시스템
    public float betterRiskManagement;     // 정교한 헤징
    public float passiveIncome;            // 높은 수익률 기회
}
```

## 4. 업적 시스템

### 4.1 업적 카테고리

#### 부의 축적 업적
```csharp
[System.Serializable]
public struct WealthAchievement
{
    public string achievementName;
    public float requiredNetWorth;
    public float timeRequirement;      // 허용되는 최대 시간
    public string rewardDescription;
    public int experienceReward;
    public string unlockBenefit;
}

// 업적 예시
private WealthAchievement[] wealthAchievements = {
    new WealthAchievement {
        achievementName = "첫 10만 달러",
        requiredNetWorth = 100000f,
        timeRequirement = 3600f,       // 게임 시간 1시간
        experienceReward = 1000,
        unlockBenefit = "주식 시장 접근 잠금 해제"
    },
    new WealthAchievement {
        achievementName = "백만장자 지위", 
        requiredNetWorth = 1000000f,
        timeRequirement = 43200f,      // 게임 시간 12시간
        experienceReward = 5000,
        unlockBenefit = "사모 펀드 투자 잠금 해제"
    }
};
```

#### 전략적 업적
```csharp
public enum StrategicAchievement
{
    DiversificationMaster,    // 20가지 이상 다른 자산 유형 보유
    MarketTimer,             // 시장 전환점 5회 정확히 예측
    RiskManager,             // 최소 손실로 시장 크래시 3회 생존
    ValueInvestor,           // 저평가 주식을 2년 이상 보유
    GrowthHacker,            // 연 50% 이상 수익률 달성
    DividendAristocrat,      // 월 $10K 이상 수동 소득 구축
    ArbitrageExpert,         // 100가지 이상 시장 비효율성 활용
    MarketMaker,             // 10개 이상 시장에서 유동성 제공
    EconomicForecaster,      // 경제 이벤트 10회 정확히 예측
    SystemInfluencer         // 시장 전반 이벤트 5회 이상 유발
}
```

### 4.2 진행 추적

#### 업적 진행 시스템
```csharp
[System.Serializable]
public struct AchievementProgress
{
    public string achievementId;
    public float currentProgress;        // 0.0에서 1.0
    public float[] milestoneValues;      // 중간 마일스톤
    public bool[] milestoneCompleted;    // 마일스톤 완료 추적
    public DateTime startTime;           // 진행 시작 시점
    public string[] progressRewards;     // 각 마일스톤에서의 보상
}

public void UpdateAchievementProgress(string achievementId, float newValue)
{
    var progress = GetAchievementProgress(achievementId);
    
    // 진행도 업데이트
    progress.currentProgress = newValue;
    
    // 마일스톤 완료 확인
    for (int i = 0; i < progress.milestoneValues.Length; i++)
    {
        if (!progress.milestoneCompleted[i] && newValue >= progress.milestoneValues[i])
        {
            progress.milestoneCompleted[i] = true;
            GrantMilestoneReward(achievementId, i);
            ShowMilestoneNotification(achievementId, i);
        }
    }
    
    // 업적 완료 확인
    if (newValue >= 1.0f)
    {
        CompleteAchievement(achievementId);
    }
}
```

## 5. 마일스톤 시스템

### 5.1 주요 마일스톤

#### 자본 마일스톤
```csharp
[System.Serializable]
public struct CapitalMilestone
{
    public string milestoneName;
    public float requiredNetWorth;
    public string significanceDescription;
    public UnlockReward[] rewards;
    public string realWorldContext;        // 교육적 맥락
}

private CapitalMilestone[] majorMilestones = {
    new CapitalMilestone {
        milestoneName = "비상 자금 확립",
        requiredNetWorth = 25000f,
        significanceDescription = "3-6개월 지출 절약",
        realWorldContext = "재정 보안의 기반"
    },
    new CapitalMilestone {
        milestoneName = "인증 투자자 지위",
        requiredNetWorth = 1000000f,
        significanceDescription = "사모 투자 접근권",
        realWorldContext = "정교한 투자자에 대한 SEC 정의"
    },
    new CapitalMilestone {
        milestoneName = "초고 순자산",
        requiredNetWorth = 30000000f,
        significanceDescription = "패밀리 오피스 영역",
        realWorldContext = "상위 0.1% 부 계층"
    }
};
```

#### 지식 마일스톤
```csharp
public enum KnowledgeMilestone
{
    BasicEconomics,           // 수요/공급, 인플레이션, 이자율 이해
    PortfolioTheory,          // 현대 포트폴리오 이론, 다변화
    TechnicalAnalysis,        // 차트 읽기, 기술적 지표  
    FundamentalAnalysis,      // 재무제표 분석
    BehavioralEconomics,      // 시장 심리, 인지 편향
    MacroEconomics,           // 중앙은행, 재정 정책
    AdvancedDerivatives,      // 복잡한 금융 상품
    SystemicRisk,             // 경제 위기 이해
    WealthManagement,         // 세금 최적화, 부동산 계획
    MarketMicrostructure      // 시장 실제 작동 방식
}
```

### 5.2 마일스톤 보상

#### 잠금해제 보상
```csharp
[System.Serializable]
public struct UnlockReward
{
    public RewardType rewardType;
    public string rewardName;
    public string description;
    public float numericValue;           // 금전적 또는 백분율 보상
    public bool isPermanentUnlock;       // vs 일시적 보너스
}

public enum RewardType
{
    NewInvestmentType,        // 새로운 투자 카테고리 잠금 해제
    BetterInformation,        // 더 빠른/더 나은 시장 데이터
    ReducedFees,             // 더 낮은 거래 비용
    AutomationFeature,        // 새로운 자동화 기능
    AnalysisTool,            // 새로운 분석 기능
    SocialStatus,            // 평판/명성 증가
    SpecialEvent,            // 고유한 시장 이벤트 트리거
    ExclusiveContent,        // 특별 교육 콘텐츠
    CostReduction,           // 영구적인 비용 절감
    IncomeBonus              // 수동 소득 배수
}
```

#### 마일스톤 축하 시스템
```csharp
public void CelebrateMilestone(CapitalMilestone milestone)
{
    // 시각적 축하
    TriggerConfettiEffect();
    PlayFanfareSound();
    
    // 교육적 순간
    ShowMilestoneEducation(milestone.realWorldContext);
    
    // 보상 배분
    foreach (var reward in milestone.rewards)
    {
        GrantReward(reward);
    }
    
    // 소셜 공유
    GenerateShareableAchievement(milestone);
    
    // 진행도 추적
    UpdatePlayerProfile(milestone);
}
```

## 6. 난이도 조정

### 6.1 동적 난이도 조정

#### 성과 기반 스케일링
```csharp
[System.Serializable]
public struct DifficultyScaling
{
    [Header("플레이어 성과 지표")]
    public float averageROI;             // 플레이어의 역사적 수익률
    public float riskAdjustedReturns;    // 샤프 비율 등가
    public float marketTimingAccuracy;   // 시장 예측 정확도 %
    public float automationEfficiency;   // 자동화 성능
    
    [Header("난이도 조정")]
    public float marketVolatilityMultiplier;  // 시장 혼란 증가
    public float competitionLevel;            // AI 플레이어 공격성  
    public float informationDelay;            // 정보 우위 감소
    public float opportunityFrequency;        // "쉬운" 기회 감소
}

public void AdjustDifficulty(PlayerPerformanceData performance)
{
    float performanceScore = CalculatePerformanceScore(performance);
    
    if (performanceScore > 0.8f) // 플레이어가 너무 잘함
    {
        // 게임을 더 어렵게 만들기
        IncreaseMarketVolatility(1.2f);
        ReduceInformationAdvantage(0.8f);
        IncreaseCompetition(1.3f);
    }
    else if (performanceScore < 0.4f) // 플레이어가 고전
    {
        // 더 많은 기회 제공
        ReduceMarketVolatility(0.8f);
        ProvideEducationalHints();
        CreateMarketOpportunities();
    }
}
```

### 6.2 레벨에 적합한 도전

#### 도전 스케일링 매트릭스
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
        educationalFocus = "기본 금융 문해력"
    },
    new LevelChallenge {
        levelRange = 40-60,
        availableChallenges = {
            ChallengeType.MarketCrash,
            ChallengeType.GeopoliticalEvents,
            ChallengeType.CurrencyDevaluation
        },
        difficultyMultiplier = 1.3f,
        educationalFocus = "고급 위험 관리"
    }
};
```

## 7. 튜토리얼 통합

### 7.1 점진적 튜토리얼 시스템

#### 적시 학습
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
        
        // 튜토리얼 참여도 추적
        RecordTutorialStart(tutorial.tutorialId);
        
        // 완료 보상
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

### 7.2 지식 진행

#### 경제 교육 프레임워크
```csharp
public enum EducationalTopic
{
    TimeValueOfMoney,         // 복리 기초
    RiskVsReturn,            // 투자 기본  
    Diversification,         // 포트폴리오 이론
    MarketEfficiency,        // 가격이 결정되는 방식
    EconomicIndicators,      // GDP, 인플레이션, 실업
    CentralBankingPolicy,    // 이자율, 통화 공급
    BehavioralBias,          // 투자 심리적 실수
    TaxOptimization,         // 세금 효율적 투자
    AssetAllocation,         // 전략적 포트폴리오 구성
    AlternativeInvestments,  // 사모 펀드, 헤지 펀드
    DerivativesBasics,       // 옵션, 선물, 스왑
    CreditRisk,              // 채권과 대출 위험
    InflationHedging,        // 구매력 보호
    GlobalMarkets,           // 국제 투자
    QuantitativeAnalysis     // 수학적 모델링
}
```

## 8. 엔드게임 진행

### 8.1 레벨 100 이후 콘텐츠

#### 프레스티지 시스템
```csharp
[System.Serializable]
public struct PrestigeLevel
{
    public int prestigeLevel;            // 1-10 프레스티지 레벨
    public float requiredNetWorth;       // 증가하는 임계값
    public string prestigeTitle;         // "경제 거물", "시장의 신"
    public Color titleColor;             // 시각적 구분
    public float globalInfluence;        // 세계 경제에 영향을 미치는 능력
    public PrestigeBenefit[] benefits;   // 영구적 보너스
}
```

#### 유산 구축
```csharp
public enum LegacyAchievement
{
    FoundationBuilder,        // 자선 재단 설립
    MarketCreator,           // 새로운 금융 시장 창조
    EconomicTheory,          // 새로운 투자 전략 개발
    MentorshipProgram,       // 다른 플레이어 가르치기
    SystemicChange,          // 글로벌 경제 정책에 영향
    WealthDynasty,           // 다세대 부의 이전
    PhilanthropicImpact,     // 주요 세계 문제 해결
    EconomicStability,       // 금융 위기 방지/완화
    InnovationSponsor,       // 획기적인 기술 지원
    SocialEntrepreneur       // 지속 가능한 비즈니스 모델 창조
}
```

### 8.2 무한 진행

#### 파라곤 레벨
```csharp
public struct ParagonProgression
{
    public int paragonLevel;             // 무제한 진행
    public ParagonCategory category;     // 전문화 초점
    public float bonusMultiplier;        // 작은 점진적 혜택
    public int requiredParagonXP;        // 지수적 XP 요구사항
}

public enum ParagonCategory
{
    WealthAccumulation,      // 모든 투자 수익률에 +1%
    RiskManagement,          // 위기 저항력 +2%
    MarketTiming,            // 예측 정확도 +3%  
    AutomationEfficiency,    // 자동화 성능 +1%
    GlobalInfluence,         // 시장 영향력 +5%
    KnowledgeRetention,      // 튜토리얼 효과 +10%
    SocialStatus,            // 평판 획득 +15%
    LegacyBuilding           // 자선 활동 영향력 +20%
}
```

## 9. 측정 및 분석

### 9.1 진행 지표

#### 플레이어 참여도 추적
```csharp
[System.Serializable]
public struct ProgressionAnalytics
{
    [Header("참여도 지표")]
    public float averageSessionLength;    // 세션당 분
    public float levelCompletionTime;     // 레벨업 간 시간
    public float featureAdoptionRate;     // 잠금해제의 실제 사용 %
    public float tutorialCompletionRate;  // 교육 참여도
    
    [Header("난이도 지표")]
    public float playerWinRate;          // 수익성 있는 결정 %
    public float ragequitRate;           // 레벨에서 중단하는 플레이어 %
    public float difficultyRating;       // 플레이어 보고 도전도
    public float learningCurve;          // 지식 습득 속도
    
    [Header("수익화 지표")]
    public float timeToFirstPurchase;    // 프리미엄 기능 채택
    public float lifetimeValue;          // 총 플레이어 지출
    public float retentionRate;          // 30일 플레이어 유지율
    public float recommendationScore;    // 순 추천 지수
}
```

### 9.2 밸런스 테스트

#### A/B 테스트 프레임워크
```csharp
public struct ProgressionTest
{
    public string testName;
    public float testGroupRatio;         // 플레이어의 10%
    public ProgressionVariable variable; // 테스트할 것
    public float baselineValue;          // 현재 값
    public float testValue;              // 테스트할 새 값
    public string successMetric;         // 성공 측정 방법
    public float minimumSampleSize;      // 통계적 유의성
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
    
    // 최소 샘플 크기 도달 후 결과 분석
    if (GetTestSampleSize(testName) >= test.minimumSampleSize)
    {
        AnalyzeTestResults(testName);
        MakeBalanceDecision(testName);
    }
}
```

## 다음 단계

1. **[AI 행동 패턴](./ai-behavior-patterns_KOR.md)** - AI 의사결정 알고리즘
2. **[UI/UX 디자인](./ui-ux-design_KOR.md)** - 인터페이스 디자인 사양
3. **[튜토리얼 온보딩](./tutorial-onboarding_KOR.md)** - 학습 시스템 디자인

## 관련 문서

- [경제 밸런스 모델](./economy-balance-model_KOR.md) - 경제 밸런스 매개변수
- [핵심 게임플레이 루프](./core-gameplay-loop_KOR.md) - 메인 게임플레이 시스템
- [투자 루프 메커니즘](./investment-loop-mechanics_KOR.md) - 투자 시스템 세부사항