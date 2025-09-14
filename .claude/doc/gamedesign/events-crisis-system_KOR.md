---
category: gamedesign
tags: [이벤트, 위기, 무작위이벤트, 블랙스완, 경제주기]
related: [economy-balance-model_KOR.md, ai-behavior-patterns_KOR.md, capitalism-game-design-doc_KOR.md]
parent: INDEX_KOR.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# 이벤트 및 위기 시스템

[🇺🇸 English Version](./events-crisis-system.md)

## 📍 내비게이션

[↩️ 게임 디자인으로 돌아가기](./INDEX_KOR.md) | [📚 문서 색인](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 이벤트 시스템 철학

### 1.1 설계 원칙

#### 현실적인 경제 역학
- **역사적 정확성**: 실제 경제 현상을 기반으로 한 이벤트
- **상호연결된 시스템**: 이벤트가 경제 전반에 현실적으로 파급
- **플레이어 주도권**: 이벤트는 임의적 처벌이 아닌 기회와 도전 창조
- **교육적 가치**: 각 이벤트가 실제 경제 개념 교육

#### 참여도와 도전
- **의미 있는 선택**: 이벤트 중 플레이어 결정이 지속적인 결과 초래
- **위험과 기회**: 이벤트가 위협과 투자 기회 모두 창조
- **전략적 깊이**: 고급 플레이어는 특정 이벤트 예측하고 준비 가능
- **감정적 투자**: 이벤트가 기억에 남는 순간과 스토리 창조

### 1.2 이벤트 분류 시스템

#### 영향 규모별 이벤트 카테고리
```csharp
[System.Serializable]
public enum EventScale
{
    Personal,        // 개별 회사에 영향 (실적 발표)
    Sectoral,        // 산업 섹터에 영향 (규제 변경)
    National,        // 전체 국가에 영향 (금리 변경)
    Regional,        // 지역적 영향 (무역 전쟁)
    Global,          // 세계 경제에 영향 (팬데믹, 전쟁)
    Systemic         // 전체 금융 시스템 위협 (2008년 위기)
}

[System.Serializable]
public enum EventType
{
    // 정기 시장 이벤트
    EarningsReport,      // 분기별 회사 실적
    ProductLaunch,       // 신제품 발표
    ManagementChange,    // CEO/경영진 변경
    
    // 경제 이벤트
    InterestRateChange,  // 중앙은행 금리 결정
    InflationReport,     // CPI/인플레이션 발표
    GDPReport,          // 경제 성장 데이터
    UnemploymentData,    // 고용 시장 통계
    
    // 정치적 이벤트
    ElectionResults,     // 정치적 지도부 변경
    PolicyAnnouncement,  // 새로운 정부 정책
    TradeAgreement,      // 국제 무역 협정
    RegulatoryChange,    // 새로운 규제
    
    // 위기 이벤트
    BankingCrisis,       // 금융 기관 실패
    CurrencyDevaluation, // 통화 붕괴
    NaturalDisaster,     // 기상/지질학적 이벤트
    GeopoliticalTension, // 전쟁, 제재, 갈등
    
    // 블랙 스완 이벤트
    Pandemic,            // 글로벌 보건 위기
    TechnologicalDisruption, // 혁신적 기술
    SystemicFailure,     // 인프라 붕괴
    UnpredictableShock   // 진정으로 무작위인 주요 이벤트
}
```

#### 이벤트 빈도 분포
```csharp
[System.Serializable]
public struct EventFrequencyConfig
{
    [Header("정기 이벤트")]
    public float dailyEventProbability;     // 0.3 - 일일 30% 확률
    public float weeklyEventProbability;    // 0.8 - 주간 80% 확률
    public float monthlyEventProbability;   // 0.95 - 월간 95% 확률
    
    [Header("위기 이벤트")]
    public float minorCrisisProbability;    // 0.1 - 월간 10% 확률
    public float majorCrisisProbability;    // 0.02 - 월간 2% 확률
    public float systemicCrisisProbability; // 0.005 - 월간 0.5% 확률
    
    [Header("블랙 스완 이벤트")]
    public float blackSwanProbability;      // 0.001 - 월간 0.1% 확률
    public int blackSwanCooldownMonths;     // 최소 12개월 간격
    public bool enableConsecutiveEvents;    // 연속 위기 허용
}
```

## 2. 정기 경제 이벤트

### 2.1 시장 주기 이벤트

#### 경기 주기 통합
```csharp
[System.Serializable]
public struct BusinessCycleEvents
{
    [Header("확장 단계 이벤트")]
    public CyclicalEvent[] expansionEvents = {
        new CyclicalEvent {
            eventName = "강력한 GDP 성장",
            description = "경제가 전년 대비 4.2% 성장",
            marketImpact = MarketImpact.Positive,
            sectors = new[] { "기술", "소비재" },
            probability = 0.4f,
            durationDays = 90
        },
        new CyclicalEvent {
            eventName = "낮은 실업률",
            description = "실업률이 3.5%로 하락",
            marketImpact = MarketImpact.Mixed,
            sectors = new[] { "전체" },
            probability = 0.3f,
            durationDays = 180
        }
    };
    
    [Header("정점 단계 이벤트")]
    public CyclicalEvent[] peakEvents = {
        new CyclicalEvent {
            eventName = "자산 버블 경고",
            description = "중앙은행이 자산 과평가 경고",
            marketImpact = MarketImpact.Negative,
            sectors = new[] { "부동산", "기술" },
            probability = 0.6f,
            durationDays = 30
        }
    };
    
    [Header("수축 단계 이벤트")]
    public CyclicalEvent[] contractionEvents = {
        new CyclicalEvent {
            eventName = "증가하는 실업률",
            description = "실업률이 7.2%로 증가",
            marketImpact = MarketImpact.Negative,
            sectors = new[] { "소비재", "소매" },
            probability = 0.5f,
            durationDays = 120
        }
    };
}
```

#### 계절적 경제 패턴
```csharp
[System.Serializable]
public struct SeasonalEvents
{
    [Header("분기별 패턴")]
    public SeasonalEvent[] quarterlyEvents;  // 4분기 소매 급등, 1분기 둔화
    public bool enableSeasonalVolatility;   // 특정 기간 높은 변동성
    
    [Header("연간 패턴")]
    public SeasonalEvent[] annualEvents;     // 세무 시즌, 휴일 지출
    public bool enableYearEndEffects;       // 12월 포트폴리오 리밸런싱
    
    [Header("휴일 효과")]
    public HolidayEvent[] holidayEvents;     // 크리스마스, 블랙 프라이데이
    public bool enableHolidayTrading;       // 휴일 중 거래량 감소
}

public struct SeasonalEvent
{
    public string eventName;               // "휴일 쇼핑 시즌"
    public MonthRange activeMonths;        // 11월-12월
    public SectorImpact[] sectorImpacts;   // 다른 섹터에 미치는 영향
    public float volatilityMultiplier;     // 일반 변동성의 1.2배
    public string educationalNote;         // 왜 이런 일이 일어나는지 설명
}
```

### 2.2 기업 이벤트

#### 회사별 이벤트
```csharp
[System.Serializable]
public struct CorporateEventSystem
{
    [Header("실적 이벤트")]
    public EarningsEventConfig earningsConfig;
    public bool enableEarningsSurprises;    // 예상치 못한 결과
    public float earningsBeatProbability;   // 60% 확률로 예상치 상회
    
    [Header("경영진 이벤트")]
    public ManagementEventConfig managementConfig;
    public bool enableSuccessionPlanning;  // CEO 은퇴 발표
    public bool enableScandals;            // 기업 지배구조 문제
    
    [Header("제품 이벤트")]
    public ProductEventConfig productConfig;
    public bool enableInnovationBreakthroughs; // 혁신적 제품
    public bool enableProductRecalls;      // 제품 안전 문제
}

public struct EarningsEvent
{
    public CompanyComponent company;       // 실적을 발표하는 회사
    public float expectedEPS;              // 월스트리트 컨센서스
    public float actualEPS;                // 실제 보고된 수익
    public float revenueGrowth;            // 전년 대비 성장률
    public EarningsQuality quality;        // 수익의 질
    public string[] keyHighlights;         // 경영진 코멘트
    public float stockImpact;              // 예상 주가 반응
}

public void ProcessEarningsAnnouncement(EarningsEvent earnings)
{
    var company = earnings.company;
    
    // 실적 서프라이즈 계산
    float surprise = (earnings.actualEPS - earnings.expectedEPS) / earnings.expectedEPS;
    
    // 시장 반응 결정
    float stockReaction = CalculateStockReaction(surprise, earnings.quality, earnings.revenueGrowth);
    
    // 주가 변동 적용
    company.stockPrice *= (1f + stockReaction);
    
    // 기본 지표 업데이트
    company.financials.earningsPerShare = earnings.actualEPS;
    company.financials.peRatio = company.stockPrice / earnings.actualEPS;
    
    // 섹터 동조/전염 효과
    ApplySectorEffects(company.industry, stockReaction * 0.3f);
    
    // 뉴스 및 플레이어 알림 생성
    CreateEarningsNews(earnings, stockReaction);
}
```

#### 인수합병 이벤트
```csharp
[System.Serializable]
public struct MergerAcquisitionSystem
{
    [Header("M&A 확률")]
    public float monthlyMAprob;            // 회사당 월 2% 확률
    public CompanySize[] targetSizes;      // 보통 작은 회사들
    public Industry[] activeIndustries;    // 기술, 헬스케어 통합
    
    [Header("거래 구조")]
    public MAStructure[] dealTypes;        // 현금, 주식, 혼합
    public float premiumRange;             // 시장 가격 대비 20-50% 프리미엄
    public bool enableHostileOffers;       // 적대적 인수 제안
    
    [Header("규제 승인")]
    public float approvalProbability;      // 85% 거래가 승인
    public int approvalTimeMonths;         // 6-18개월 승인 과정
    public bool enableAntitrustBlocking;   // 대규모 거래 차단 가능
}

public struct MAEvent
{
    public CompanyComponent acquirer;      // 제안하는 회사
    public CompanyComponent target;        // 인수 대상 회사
    public float offerPrice;               // 제안된 주당 가격
    public float premiumPercent;           // 시장 가격 대비 프리미엄
    public MAStructure structure;          // 거래 구조
    public float completionProbability;   // 거래 완료 가능성
    public int expectedCompletionDays;     // 완료까지 시간
    public string strategicRationale;      // 인수 이유
}
```

## 3. 위기 이벤트

### 3.1 금융 위기

#### 은행 위기 시뮬레이션
```csharp
[System.Serializable]
public struct BankingCrisisConfig
{
    [Header("위기 촉발 요인")]
    public CrisisTrigger[] triggers = {
        new CrisisTrigger {
            triggerName = "부동산 버블 붕괴",
            description = "주택 가격이 6개월간 30% 하락",
            probability = 0.05f,    // 정점 단계에서 5% 확률
            severity = CrisisSeverity.Major
        },
        new CrisisTrigger {
            triggerName = "주요 은행 실패",
            description = "시스템적으로 중요한 은행 파산",
            probability = 0.02f,    // 2% 확률
            severity = CrisisSeverity.Systemic
        }
    };
    
    [Header("전파 메커니즘")]
    public ContagionEffect[] contagionEffects;
    public float bankFailureProbability;      // 위기 중 은행 실패 확률
    public float creditCrunchSeverity;        // 신용 긴축 정도
    
    [Header("정부 대응")]
    public GovernmentResponse[] responseOptions;
    public bool enableBankBailouts;          // 은행 구제금융
    public bool enableFiscalStimulus;        // 재정 부양책
    public float responseDelay;              // 대응 지연 시간
}

public struct BankingCrisisEvent
{
    public string crisisName;                // "주택담보대출 위기"
    public CrisisTrigger trigger;           // 위기 촉발 요인
    public BankComponent[] affectedBanks;   // 영향받는 은행들
    public float systemicRiskScore;         // 시스템 리스크 점수
    public int durationMonths;              // 위기 지속 기간
    public EconomicImpact impact;           // 경제적 영향
    public string[] playerChoices;          // 플레이어 대응 선택지
}

public void TriggerBankingCrisis(BankingCrisisEvent crisis)
{
    // 은행 자본 감소
    foreach (var bank in crisis.affectedBanks)
    {
        bank.capitalRatio *= (1f - crisis.systemicRiskScore * 0.5f);
        if (bank.capitalRatio < 0.08f) // 최소 자본 비율 미만
        {
            TriggerBankFailure(bank);
        }
    }
    
    // 신용 경색
    ApplyCreditCrunch(crisis.impact.creditAvailability);
    
    // 주식 시장 충격
    ApplyMarketShock(crisis.impact.stockMarketDrop);
    
    // 정부 대응 옵션 제시
    PresentGovernmentResponseOptions(crisis);
    
    // 플레이어 결정 기회 제공
    PresentPlayerCrisisOptions(crisis.playerChoices);
}
```

### 3.2 시장 붕괴 이벤트

#### 주식 시장 크래시
```csharp
[System.Serializable]
public struct MarketCrashConfig
{
    [Header("크래시 유형")]
    public MarketCrashType[] crashTypes = {
        new MarketCrashType {
            crashName = "기술 버블 붕괴",
            triggerSectors = new[] { "기술", "통신" },
            marketDrop = 0.4f,      // 40% 하락
            durationDays = 180,     // 6개월 지속
            recoveryTime = 720      // 2년 회복
        },
        new MarketCrashType {
            crashName = "금융 위기",
            triggerSectors = new[] { "금융", "부동산" },
            marketDrop = 0.5f,      // 50% 하락
            durationDays = 360,     // 1년 지속
            recoveryTime = 1080     // 3년 회복
        }
    };
    
    [Header("회복 패턴")]
    public RecoveryPattern[] recoveryPatterns;
    public bool enableVolatilitySpikes;     // 회복 중 변동성 급증
    public bool enableDeadCatBounce;        // 일시적 반등
}

public struct MarketCrashEvent
{
    public string crashName;               // 크래시 이름
    public float initialDrop;              // 초기 하락폭
    public float totalDrop;                // 총 하락폭
    public SectorImpact[] sectorImpacts;   // 섹터별 영향
    public int crashDurationDays;          // 하락 지속 기간
    public int recoveryDurationDays;       // 회복 기간
    public string[] educationalContent;    // 교육적 설명
    public PlayerOpportunity[] opportunities; // 플레이어 기회
}

public void ExecuteMarketCrash(MarketCrashEvent crashEvent)
{
    // 초기 시장 충격
    ApplyInitialShock(crashEvent.initialDrop);
    
    // 섹터별 차별 영향
    foreach (var sectorImpact in crashEvent.sectorImpacts)
    {
        ApplySectorCrash(sectorImpact.sector, sectorImpact.dropPercent);
    }
    
    // 변동성 급증
    IncreaseMarketVolatility(3.0f);
    
    // AI 행동 변화
    TriggerPanicSelling();
    ActivateFlightToQuality();
    
    // 플레이어에게 기회 제시
    PresentCrashOpportunities(crashEvent.opportunities);
    
    // 교육적 순간
    ShowCrashEducationalContent(crashEvent.educationalContent);
}
```

### 3.3 글로벌 위기 이벤트

#### 팬데믹 시뮬레이션
```csharp
[System.Serializable]
public struct PandemicCrisisConfig
{
    [Header("팬데믹 단계")]
    public PandemicPhase[] phases = {
        new PandemicPhase {
            phaseName = "초기 발생",
            economicImpact = 0.1f,     // GDP 10% 감소
            durationMonths = 3,
            restrictions = LockdownLevel.Partial
        },
        new PandemicPhase {
            phaseName = "전면 봉쇄",
            economicImpact = 0.3f,     // GDP 30% 감소
            durationMonths = 6,
            restrictions = LockdownLevel.Full
        },
        new PandemicPhase {
            phaseName = "점진적 회복",
            economicImpact = -0.1f,    // GDP 10% 회복
            durationMonths = 12,
            restrictions = LockdownLevel.Gradual
        }
    };
    
    [Header("섹터별 영향")]
    public PandemicSectorImpact[] sectorImpacts;
    public bool enableRemoteWorkShift;     // 재택근무 전환
    public bool enableSupplyChainDisruption; // 공급망 차단
    
    [Header("정부 대응")]
    public StimulusPackage[] stimulusOptions;
    public bool enableUBI;                 // 기본소득 도입
    public bool enableBusinessSupport;     // 기업 지원
}

public struct PandemicEvent
{
    public string pandemicName;            // "글로벌 팬데믹 2020"
    public PandemicPhase currentPhase;     // 현재 단계
    public float infectionRate;            // 감염률
    public float mortalityRate;            // 치사율
    public EconomicShock economicShock;    // 경제적 충격
    public SectorWinner[] winners;         // 승자 섹터 (기술, 헬스케어)
    public SectorLoser[] losers;           // 패자 섹터 (여행, 레스토랑)
    public GovernmentPolicy[] policies;    // 정부 정책 대응
}
```

## 4. 블랙 스완 이벤트

### 4.1 예측 불가능한 충격

#### 블랙 스완 이벤트 시스템
```csharp
[System.Serializable]
public struct BlackSwanEventSystem
{
    [Header("블랙 스완 특성")]
    public float unpredictabilityScore;    // 0.9 - 90% 예측 불가
    public float extremeImpactMultiplier;  // 3.0 - 일반 이벤트의 3배 영향
    public bool enableNarrativeFallacy;    // 사후 설명 편향
    
    [Header("역사적 블랙 스완")]
    public BlackSwanEvent[] historicalEvents = {
        new BlackSwanEvent {
            eventName = "9/11 테러 공격",
            description = "예상치 못한 테러 공격으로 시장 폐쇄",
            marketImpact = -0.15f,     // 15% 즉시 하락
            recoveryDays = 30,
            sectors = new[] { "항공", "보험", "관광" }
        },
        new BlackSwanEvent {
            eventName = "후쿠시마 원전 사고",
            description = "자연재해로 인한 원전 사고",
            marketImpact = -0.12f,     // 12% 하락
            recoveryDays = 90,
            sectors = new[] { "에너지", "보험" }
        }
    };
    
    [Header("가상 블랙 스완")]
    public BlackSwanEvent[] hypotheticalEvents;
    public bool enableTechnologyDisruption;  // 기술적 파괴
    public bool enableAliensContact;        // 외계인 접촉 (극단적 예시)
}

public void TriggerBlackSwanEvent(BlackSwanEvent blackSwan)
{
    // 극도의 시장 충격
    ApplyExtremeMarketShock(blackSwan.marketImpact);
    
    // 불확실성과 변동성 급증
    spikeUncertaintyIndex(5.0f);
    IncreaseMarketVolatility(10.0f);
    
    // AI 행동 패닉 모드
    TriggerAIPanic();
    EnableHerdBehavior();
    
    // 플레이어에게 극한 상황 선택 제시
    PresentExtremeChoices(blackSwan);
    
    // 사후 분석 및 교육
    ProvidePostEventAnalysis(blackSwan);
    ExplainNarrativeFallacy();
}
```

### 4.2 기술적 파괴 이벤트

#### 혁신적 기술 도입
```csharp
[System.Serializable]
public struct TechnologicalDisruptionEvent
{
    [Header("파괴적 기술")]
    public DisruptiveTechnology[] technologies = {
        new DisruptiveTechnology {
            technologyName = "인공 일반 지능 (AGI)",
            description = "인간 수준의 AI가 대부분 업무 자동화",
            affectedIndustries = new[] { "전체" },
            adoptionSpeed = 0.8f,       // 빠른 채택
            jobDisplacement = 0.6f,     // 60% 일자리 영향
            productivityGain = 3.0f     // 300% 생산성 증가
        },
        new DisruptiveTechnology {
            technologyName = "핵융합 상용화",
            description = "무제한 청정 에너지 공급",
            affectedIndustries = new[] { "에너지", "제조업", "운송" },
            adoptionSpeed = 0.3f,       // 느린 채택
            jobDisplacement = 0.2f,     // 20% 에너지 업계 영향
            productivityGain = 1.5f     // 150% 에너지 효율성
        }
    };
    
    [Header("경제적 영향")]
    public EconomicTransformation transformation;
    public bool enableCreativeDestruction;   // 창조적 파괴
    public bool enableNewIndustryCreation;   // 새로운 산업 창조
}
```

## 5. 이벤트 대응 시스템

### 5.1 플레이어 선택과 결과

#### 위기 대응 선택
```csharp
[System.Serializable]
public struct CrisisResponseSystem
{
    [Header("대응 옵션")]
    public ResponseOption[] availableResponses = {
        new ResponseOption {
            responseName = "현금 보유 증가",
            description = "포트폴리오의 30%를 현금으로 전환",
            riskLevel = RiskLevel.Conservative,
            expectedOutcome = "안정성 증가, 기회 비용 발생"
        },
        new ResponseOption {
            responseName = "하락장 매수",
            description = "가격 하락을 기회로 보고 추가 투자",
            riskLevel = RiskLevel.Aggressive,
            expectedOutcome = "높은 수익 가능성, 높은 위험"
        },
        new ResponseOption {
            responseName = "헤징 전략",
            description = "풋 옵션으로 포트폴리오 보호",
            riskLevel = RiskLevel.Moderate,
            expectedOutcome = "위험 감소, 비용 발생"
        }
    };
    
    [Header("결과 시스템")]
    public bool enableDelayedConsequences;   // 지연된 결과
    public bool trackDecisionHistory;        // 결정 이력 추적
    public bool provideLearningFeedback;     // 학습 피드백
}

public void ProcessPlayerCrisisResponse(ResponseOption choice, CrisisEvent crisis)
{
    var outcome = CalculateResponseOutcome(choice, crisis);
    
    // 즉시 효과 적용
    ApplyImmediateEffects(choice, outcome);
    
    // 장기 결과 예약
    ScheduleDelayedConsequences(choice, crisis, outcome);
    
    // 교육적 피드백 제공
    ProvideFeedback(choice, outcome);
    
    // AI 반응 조정
    AdjustAIBehaviorToPlayerChoice(choice);
    
    // 결정 이력에 기록
    RecordDecisionInHistory(choice, crisis, outcome);
}
```

### 5.2 교육적 순간

#### 이벤트 기반 학습
```csharp
[System.Serializable]
public struct EducationalMomentConfig
{
    [Header("학습 기회")]
    public bool enableRealTimeEducation;     // 실시간 교육
    public bool explainEventCauses;          // 이벤트 원인 설명
    public bool showHistoricalParallels;     // 역사적 유사 사례
    public bool demonstrateRiskManagement;   // 위험 관리 시연
    
    [Header("교육 콘텐츠")]
    public EducationalContent[] eventEducation;
    public bool enableInteractiveExplanations; // 상호작용 설명
    public bool provideAdditionalResources;  // 추가 자료 제공
    
    [Header("평가 및 성찰")]
    public bool enablePostEventQuiz;         // 이벤트 후 퀴즈
    public bool encourageSelfReflection;     // 자기 성찰 격려
    public bool trackLearningProgress;       // 학습 진행 추적
}

public void TriggerEducationalMoment(GameEvent gameEvent, PlayerAction playerAction)
{
    // 맥락적 교육 콘텐츠 선택
    var educationalContent = SelectRelevantEducation(gameEvent, playerAction);
    
    // 대화형 설명 표시
    ShowInteractiveExplanation(educationalContent);
    
    // 역사적 사례 연결
    ConnectToHistoricalEvents(gameEvent);
    
    // 학습 이해도 확인
    AssessUnderstanding(educationalContent);
    
    // 추가 학습 자료 제안
    SuggestAdditionalLearning(gameEvent.eventType);
}
```

## 6. 이벤트 밸런싱

### 6.1 동적 밸런싱 시스템

#### 적응형 이벤트 빈도
```csharp
[System.Serializable]
public struct DynamicEventBalancing
{
    [Header("플레이어 성과 기반")]
    public bool adjustBasedOnPerformance;    // 성과에 따른 조정
    public float goodPerformanceThreshold;   // 0.8 - 좋은 성과 임계값
    public float poorPerformanceThreshold;   // 0.4 - 나쁜 성과 임계값
    
    [Header("게임 페이스 조정")]
    public bool maintainOptimalChallenge;    // 최적 도전 유지
    public float targetEngagementLevel;      // 0.7 - 목표 참여도
    public bool preventEventFatigue;         // 이벤트 피로 방지
    
    [Header("학습 목표 연계")]
    public bool alignWithLearningObjectives; // 학습 목표와 연계
    public EducationalTopic[] priorityTopics; // 우선 교육 주제
    public bool reinforcePreviousLessons;    // 이전 학습 강화
}

public void AdjustEventFrequency(PlayerPerformanceData performance)
{
    var balancing = dynamicEventBalancing;
    
    if (performance.overallScore > balancing.goodPerformanceThreshold)
    {
        // 성과가 좋으면 더 어려운 이벤트
        IncreaseEventDifficulty(1.2f);
        IntroduceAdvancedScenarios();
    }
    else if (performance.overallScore < balancing.poorPerformanceThreshold)
    {
        // 성과가 나쁘면 교육적 이벤트 증가
        IncreaseEducationalEvents();
        ReduceEventComplexity();
    }
    
    // 이벤트 피로도 확인
    if (DetectEventFatigue())
    {
        ReduceEventFrequency();
        FocusOnQualityOverQuantity();
    }
}
```

## 다음 단계

1. **[AI 행동 패턴](./ai-behavior-patterns_KOR.md)** - AI 의사결정 알고리즘
2. **[경제 밸런스 모델](./economy-balance-model_KOR.md)** - 경제 밸런스 매개변수
3. **[진행 시스템](./progression-system_KOR.md)** - 플레이어 발전과 잠금 해제

## 관련 문서

- [경제 밸런스 모델](./economy-balance-model_KOR.md) - 경제 시스템과 이벤트 상호작용
- [AI 행동 패턴](./ai-behavior-patterns_KOR.md) - 이벤트에 대한 AI 반응
- [자본주의 게임 디자인 문서](./capitalism-game-design-doc_KOR.md) - 전체 게임 디자인 맥락