---
category: architecture
tags: [unity, ecs, data-model, components, economics]
related: [ecs-design.md, technical-architecture.md, ui-system.md]
parent: INDEX.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# Data Model Specification

[🇰🇷 Korean Version](./data-model_KOR.md)

## 📍 Navigation

[↩️ Back to Architecture](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Data Model Overview

### 1.1 Design Philosophy

#### Normalization vs Denormalization Strategy
```csharp
// ✅ Denormalized data optimized for ECS
struct PopulationComponent : IComponentData
{
    public float income;           // Direct storage (fast access)
    public float wealth;
    public PopulationClass class;  // Normalized as enum
}

// ❌ Traditional normalization (inefficient for ECS)
// class Person { public int classId; } 
// class SocialClass { public int id; public string name; }
```

#### Data Locality Optimization
- **Hot Data**: Frequently accessed data → Separate components
- **Cold Data**: Infrequently accessed data → SharedComponent or separate storage
- **Static Data**: Immutable data → ScriptableObject

### 1.2 Data Flow Architecture

```
Input Events → Command Buffer → ECS Entities → Statistics Cache → UI Display
     ↓              ↓              ↓               ↓              ↓
[Player Actions][Entity Changes][Simulation][Aggregation][Visualization]
```

## 2. Core Data Structures

### 2.1 Population Data Model

#### Basic Population Structure
```csharp
// Core population data (Hot Data)
public struct PopulationComponent : IComponentData
{
    public int populationID;
    public PopulationClass socialClass;
    public float age;
    public EmploymentStatus employment;
}

// Economic activity data (Hot Data)
public struct EconomicStatusComponent : IComponentData
{
    public float monthlyIncome;
    public float totalWealth;
    public float savingsRate;
    public float consumptionRate;
    public float riskTolerance;
}

// Consumption patterns (Hot Data)
public struct ConsumptionComponent : IComponentData
{
    public float housingCost;
    public float foodExpense;
    public float luxurySpending;
    public float investmentAmount;
    public float debtAmount;
}

// Demographic information (Cold Data)
public struct DemographicsComponent : IComponentData
{
    public Gender gender;
    public EducationLevel education;
    public Region residence;
    public FamilyStatus familyStatus;
    public int dependents;
}

// Behavioral patterns (Cold Data)
public struct BehaviorComponent : IComponentData
{
    public float optimismLevel;      // Optimism/pessimism tendency
    public float conformityLevel;    // Conformity tendency (crowd psychology)
    public float loyaltyLevel;       // Brand/company loyalty
    public float informationLevel;   // Information level (rational decision-making)
}
```

#### Population Group Classification System
```csharp
public enum PopulationClass : byte
{
    LowIncome = 0,      // Low income: Monthly income under $2,000
    LowerMiddle = 1,    // Lower middle: $2,000-3,500
    MiddleClass = 2,    // 중산층: 350-600만원
    UpperMiddle = 3,    // 중상위층: 600-1000만원
    HighIncome = 4,     // 고소득층: 1000만원 이상
    WealthyElite = 5    // 부유층: 최상위 1%
}

public enum EmploymentStatus : byte
{
    Unemployed = 0,     // 실업
    PartTime = 1,       // 시간제 근무
    FullTime = 2,       // 정규직
    SelfEmployed = 3,   // 자영업
    Executive = 4,      // 경영진
    Retired = 5,        // 은퇴
    Student = 6         // 학생
}

public enum EducationLevel : byte
{
    Elementary = 0,     // 초등교육
    MiddleSchool = 1,   // 중등교육
    HighSchool = 2,     // 고등교육
    College = 3,        // 전문대
    University = 4,     // 대학교
    Graduate = 5        // 대학원
}
```

### 2.2 회사 데이터 모델

#### 회사 핵심 데이터
```csharp
// 회사 기본 정보
public struct CompanyComponent : IComponentData
{
    public int companyID;
    public FixedString64Bytes companyName;
    public IndustryType industry;
    public CompanySize size;
    public CompanyStage stage;
    public bool isPubliclyTraded;
    public float foundedDate;
}

// 재무 정보 (Hot Data)
public struct FinancialComponent : IComponentData
{
    public float revenue;              // 매출
    public float operatingCost;        // 운영비
    public float netProfit;            // 순이익
    public float totalAssets;          // 총자산
    public float totalLiabilities;     // 총부채
    public float cashFlow;             // 현금흐름
    public float retainedEarnings;     // 이익잉여금
}

// 운영 데이터
public struct OperationComponent : IComponentData
{
    public int employeeCount;
    public float productivity;         // 생산성 지수 (0.5 ~ 2.0)
    public float marketShare;          // 시장 점유율 (0.0 ~ 1.0)
    public float innovationLevel;      // 혁신 수준 (0.0 ~ 10.0)
    public float customerSatisfaction; // 고객 만족도 (0.0 ~ 5.0)
    public float brandValue;           // 브랜드 가치
}

// 상장 회사 전용 (주식 데이터)
public struct StockComponent : IComponentData
{
    public float stockPrice;
    public long sharesOutstanding;     // 발행 주식 수
    public float dividendYield;        // 배당 수익률
    public float pe_ratio;             // PER
    public float volatility;           // 변동성
    public float beta;                 // 베타 (시장 대비 변동성)
    public TradingVolume dailyVolume;  // 일일 거래량
}

// 거래량 구조체
public struct TradingVolume
{
    public long shares;                // 거래 주식 수
    public float value;                // 거래 대금
    public int transactions;           // 거래 건수
}
```

#### 산업 분류 체계
```csharp
public enum IndustryType : byte
{
    // 1차 산업
    Agriculture = 0,        // 농업
    Mining = 1,            // 광업
    Energy = 2,            // 에너지
    
    // 2차 산업
    Manufacturing = 10,     // 제조업
    Construction = 11,      // 건설업
    Chemicals = 12,         // 화학
    Electronics = 13,       // 전자
    Automotive = 14,        // 자동차
    
    // 3차 산업
    Retail = 20,           // 소매업
    Wholesale = 21,        // 도매업
    Transportation = 22,    // 운송업
    Hospitality = 23,      // 호텔/외식
    
    // 4차 산업
    Technology = 30,        // 기술/IT
    Software = 31,         // 소프트웨어
    Telecommunications = 32, // 통신
    Media = 33,            // 미디어
    
    // 서비스업
    Finance = 40,          // 금융
    Insurance = 41,        // 보험
    RealEstate = 42,       // 부동산
    Healthcare = 43,       // 의료
    Education = 44,        // 교육
    Legal = 45,            // 법무
    Consulting = 46        // 컨설팅
}

public enum CompanyStage : byte
{
    Seed = 0,              // 시드 단계
    StartUp = 1,           // 스타트업
    Growth = 2,            // 성장기
    Mature = 3,            // 성숙기
    Decline = 4,           // 쇠퇴기
    Restructuring = 5      // 구조조정
}

public enum CompanySize : byte
{
    Micro = 0,             // 소상공인 (<10명)
    Small = 1,             // 소기업 (10-50명)
    Medium = 2,            // 중기업 (50-300명)
    Large = 3,             // 대기업 (300-1000명)
    Conglomerate = 4       // 재벌/대기업집단 (1000명+)
}
```

### 2.3 시장 데이터 모델

#### 상품/서비스 시장
```csharp
// 시장 기본 정보
public struct MarketComponent : IComponentData
{
    public int marketID;
    public MarketType marketType;
    public IndustryType industry;
    public float marketSize;           // 시장 규모 (연간)
    public float growthRate;           // 성장률
    public MarketStructure structure;   // 시장 구조
}

// 시장 역학
public struct MarketDynamicsComponent : IComponentData
{
    public float currentPrice;
    public float demandLevel;          // 수요 수준
    public float supplyLevel;          // 공급 수준
    public float elasticity;           // 가격 탄력성
    public float seasonalFactor;       // 계절성 요인
    public float trendFactor;          // 트렌드 요인
}

// 시장 참여자 정보
public struct MarketParticipantsComponent : IComponentData
{
    public int numberOfSuppliers;      // 공급자 수
    public int numberOfBuyers;         // 구매자 수
    public float marketConcentration;  // 시장 집중도 (HHI)
    public float barrierToEntry;       // 진입 장벽
    public float brandLoyalty;         // 브랜드 충성도
}

public enum MarketStructure : byte
{
    PerfectCompetition = 0,    // 완전 경쟁
    MonopolisticCompetition = 1, // 독점적 경쟁
    Oligopoly = 2,             // 과점
    Monopoly = 3               // 독점
}

public enum MarketType : byte
{
    Consumer = 0,              // 소비재
    Industrial = 1,            // 산업재
    Intermediate = 2,          // 중간재
    Luxury = 3,               // 사치품
    Necessity = 4,            // 필수재
    Service = 5               // 서비스
}
```

#### 금융 시장
```csharp
// 주식 시장 전체
public struct StockMarketComponent : IComponentData
{
    public float marketIndex;          // 종합 주가 지수
    public float totalMarketCap;       // 총 시가총액
    public float averagePE;            // 평균 PER
    public float averageDividendYield; // 평균 배당 수익률
    public long totalVolume;           // 총 거래량
    public MarketSentiment sentiment;   // 시장 심리
    public float volatilityIndex;      // 변동성 지수
}

// 채권 시장
public struct BondMarketComponent : IComponentData
{
    public float governmentBondYield;  // 국채 수익률
    public float corporateBondYield;   // 회사채 수익률
    public float creditSpread;         // 신용 스프레드
    public float yieldCurveSlope;      // 수익률 곡선 기울기
    public float defaultRate;          // 부도율
}

// 외환 시장
public struct ForexMarketComponent : IComponentData
{
    public float exchangeRate;         // 환율 (USD 기준)
    public float exchangeVolatility;   // 환율 변동성
    public float currentAccountBalance; // 경상수지
    public float foreignReserves;      // 외환 보유액
    public float capitalFlows;         // 자본 유출입
}

public enum MarketSentiment : byte
{
    VeryBearish = 0,    // 매우 약세 (공포)
    Bearish = 1,        // 약세 (비관)
    Neutral = 2,        // 중립
    Bullish = 3,        // 강세 (낙관)
    VeryBullish = 4,    // 매우 강세 (탐욕)
    Euphoric = 5        // 광기 (버블)
}
```

### 2.4 정부/정책 데이터 모델

#### 정부 정책
```csharp
// 정부 기본 정보
public struct GovernmentComponent : IComponentData
{
    public PolicyStance economicStance;  // 경제 정책 기조
    public PolicyStance fiscalStance;    // 재정 정책 기조
    public PolicyStance monetaryStance;  // 통화 정책 기조
    public float approvalRating;         // 정부 지지율
    public float politicalStability;     // 정치 안정성
}

// 재정 정책
public struct FiscalPolicyComponent : IComponentData
{
    public float governmentRevenue;      // 정부 수입 (세수)
    public float governmentSpending;     // 정부 지출
    public float budgetBalance;          // 재정 수지
    public float publicDebt;             // 국가 채무
    public float debtToGDPRatio;         // GDP 대비 국가채무비율
}

// 세금 정책
public struct TaxPolicyComponent : IComponentData
{
    public float incomeTaxRate;          // 소득세율
    public float corporateTaxRate;       // 법인세율
    public float vatRate;                // 부가가치세율
    public float capitalGainsTaxRate;    // 자본이득세율
    public float propertyTaxRate;        // 재산세율
    public TaxProgressivity progressivity; // 누진성
}

// 통화 정책
public struct MonetaryPolicyComponent : IComponentData
{
    public float baseInterestRate;       // 기준 금리
    public float moneySupply;            // 통화 공급량
    public float bankReserveRatio;       // 지급준비율
    public float inflationTarget;        // 인플레이션 목표
    public float realInterestRate;       // 실질 금리
}

// 규제 정책
public struct RegulatoryPolicyComponent : IComponentData
{
    public float laborRegulationIndex;   // 노동 규제 강도
    public float environmentalStandards; // 환경 규제 수준
    public float financialRegulation;    // 금융 규제 강도
    public float antitrustEnforcement;   // 독점 방지 집행 강도
    public float tradePolicyIndex;       // 무역 정책 (보호주의 ↔ 자유무역)
}

public enum PolicyStance : byte
{
    VeryExpansionary = 0,   // 매우 확장적
    Expansionary = 1,       // 확장적
    Neutral = 2,           // 중립적
    Contractionary = 3,     // 긴축적
    VeryContractionary = 4  // 매우 긴축적
}

public enum TaxProgressivity : byte
{
    Regressive = 0,        // 역진적 (부자에게 유리)
    Proportional = 1,      // 비례적 (균등)
    Progressive = 2,       // 누진적 (서민에게 유리)
    HighlyProgressive = 3  // 고누진적
}
```

## 3. 이벤트 데이터 모델

### 3.1 경제 이벤트
```csharp
// 이벤트 기본 구조
public struct EconomicEventComponent : IComponentData
{
    public int eventID;
    public EventType eventType;
    public EventSeverity severity;
    public float duration;             // 지속 시간
    public float timeRemaining;        // 남은 시간
    public float probability;          // 발생 확률
    public bool isActive;
}

// 이벤트 효과
public struct EventEffectComponent : IComponentData
{
    public float gdpMultiplier;        // GDP 영향
    public float inflationEffect;      // 인플레이션 영향
    public float unemploymentEffect;   // 실업률 영향
    public float stockMarketEffect;    // 주식 시장 영향
    public float consumerConfidenceEffect; // 소비자 신뢰도 영향
}

// 이벤트 대상
public struct EventTargetComponent : IComponentData
{
    public TargetScope targetScope;    // 영향 범위
    public IndustryType targetIndustry; // 대상 업종 (업종별 이벤트)
    public PopulationClass targetClass; // 대상 계층 (계층별 이벤트)
    public CompanySize targetSize;     // 대상 기업 규모
}

public enum EventType : byte
{
    // 자연재해
    NaturalDisaster = 0,
    Pandemic = 1,
    
    // 기술 혁신
    TechnologicalBreakthrough = 10,
    DisruptiveInnovation = 11,
    
    // 정치/사회
    PoliticalCrisis = 20,
    SocialUnrest = 21,
    PolicyChange = 22,
    
    // 경제
    MarketCrash = 30,
    BubbleBurst = 31,
    FinancialCrisis = 32,
    RecessionWarning = 33,
    
    // 국제
    TradeWar = 40,
    GeopoliticalTension = 41,
    CurrencyDevaluation = 42,
    
    // 업종별
    IndustryShakeup = 50,
    RegulatoryChange = 51,
    SupplyChainDisruption = 52,
    
    // 랜덤
    BlackSwanEvent = 60,
    MarketAnomaly = 61
}

public enum EventSeverity : byte
{
    Negligible = 0,    // 무시할 수 있는 수준
    Minor = 1,         // 경미한 영향
    Moderate = 2,      // 중간 수준 영향
    Major = 3,         // 큰 영향
    Severe = 4,        // 심각한 영향
    Catastrophic = 5   // 재앙적 수준
}

public enum TargetScope : byte
{
    Individual = 0,    // 개별 엔티티
    Industry = 1,      // 특정 업종
    Region = 2,        // 특정 지역
    SocialClass = 3,   // 특정 계층
    CompanySize = 4,   // 특정 기업 규모
    Global = 5         // 전체 경제
}
```

### 3.2 플레이어 액션 데이터
```csharp
// 플레이어 투자 포트폴리오
public struct PlayerPortfolioComponent : IComponentData
{
    public float totalAssets;          // 총 자산
    public float liquidAssets;         // 유동 자산 (현금)
    public float stockInvestments;     // 주식 투자
    public float bondInvestments;      // 채권 투자
    public float realEstateInvestments; // 부동산 투자
    public float alternativeInvestments; // 대안 투자
    public float totalLiabilities;     // 총 부채
    public float netWorth;             // 순자산
}

// 자동화 설정
public struct AutomationComponent : IComponentData
{
    public bool portfolioRebalancing;  // 포트폴리오 리밸런싱 자동화
    public bool dividendReinvestment;  // 배당 재투자 자동화
    public bool taxOptimization;       // 세금 최적화 자동화
    public bool riskManagement;        // 리스크 관리 자동화
    public float riskTolerance;        // 위험 감수도 설정
    public float targetReturn;         // 목표 수익률
}

// 플레이어 의사결정 히스토리
public struct DecisionHistoryComponent : IComponentData
{
    public BlobArray<PlayerDecision> pastDecisions; // 과거 의사결정 기록
    public float successRate;          // 성공률
    public float averageReturn;        // 평균 수익률
    public float riskAdjustedReturn;   // 위험 조정 수익률
    public DecisionStyle playStyle;    // 플레이 스타일
}

public struct PlayerDecision
{
    public float timestamp;
    public DecisionType type;
    public float amount;
    public int targetEntityID;
    public float expectedReturn;
    public float actualReturn;
    public bool wasSuccessful;
}

public enum DecisionType : byte
{
    BuyStock = 0,
    SellStock = 1,
    BuyBond = 2,
    SellBond = 3,
    InvestInCompany = 4,
    Divest = 5,
    TakeOutLoan = 6,
    PayOffDebt = 7,
    SetAutomation = 8,
    PolicyInfluence = 9
}

public enum DecisionStyle : byte
{
    Conservative = 0,      // 보수적 (안정 선호)
    Moderate = 1,         // 온건한 (균형)
    Aggressive = 2,       // 공격적 (수익 추구)
    Speculative = 3,      // 투기적 (고위험)
    DataDriven = 4,       // 데이터 중심 (분석적)
    Intuitive = 5,        // 직관적 (감정적)
    Contrarian = 6,       // 역투자 (역발상)
    Momentum = 7          // 추세 추종
}
```

## 4. 통계 및 집계 데이터

### 4.1 실시간 통계
```csharp
// 실시간 경제 지표 (매 프레임 업데이트)
public struct LiveEconomicIndicators : IComponentData
{
    public float currentGDP;
    public float gdpGrowthRate;
    public float currentInflation;
    public float unemploymentRate;
    public float consumerConfidenceIndex;
    public float businessConfidenceIndex;
    public float stockMarketIndex;
    public float averageWage;
    public float giniCoefficient;          // 소득 불평등 지수
}

// 업종별 통계
public struct IndustryStatistics : IComponentData
{
    public IndustryType industry;
    public float totalRevenue;
    public float averageProfit;
    public int numberOfCompanies;
    public int totalEmployees;
    public float averageProductivity;
    public float marketConcentration;
    public float growthRate;
    public MarketSentiment sentiment;
}

// 계층별 통계
public struct SocialClassStatistics : IComponentData
{
    public PopulationClass socialClass;
    public int population;
    public float averageIncome;
    public float averageWealth;
    public float averageConsumption;
    public float unemploymentRate;
    public float mobilityIndex;            // 사회 이동성
}
```

### 4.2 히스토리 데이터 (외부 저장)
```csharp
// SQLite 등 외부 DB에 저장할 히스토리 데이터
public struct EconomicHistoryEntry
{
    public float timestamp;
    public float gdp;
    public float inflation;
    public float unemployment;
    public float stockIndex;
    public float interestRate;
}

public struct CompanyHistoryEntry
{
    public float timestamp;
    public int companyID;
    public float revenue;
    public float profit;
    public float stockPrice;
    public int employees;
    public float marketCap;
}

public struct PlayerPerformanceEntry
{
    public float timestamp;
    public float netWorth;
    public float totalReturn;
    public float portfolioValue;
    public float riskScore;
    public int rank;                       // 전체 순위 (멀티플레이어)
}
```

## 5. 데이터 검증 및 제약사항

### 5.1 데이터 무결성 검증
```csharp
public struct DataValidationComponent : IComponentData
{
    public bool isValid;
    public ValidationError errors;
    public float lastValidationTime;
}

[System.Flags]
public enum ValidationError : uint
{
    None = 0,
    NegativeIncome = 1 << 0,
    ExcessiveDebt = 1 << 1,
    InvalidStockPrice = 1 << 2,
    InconsistentEmployment = 1 << 3,
    MarketAnomalies = 1 << 4,
    SumValidationError = 1 << 5,       // 합계 불일치
    RangeValidationError = 1 << 6,     // 범위 초과
    RelationValidationError = 1 << 7   // 관계 무결성 위반
}

// 데이터 범위 제약
public struct DataConstraints
{
    // 인구 데이터 제약
    public static readonly float MIN_INCOME = 0f;
    public static readonly float MAX_INCOME = 1000000000f; // 10억원
    public static readonly float MIN_AGE = 0f;
    public static readonly float MAX_AGE = 120f;
    
    // 회사 데이터 제약
    public static readonly float MIN_STOCK_PRICE = 0.01f;
    public static readonly float MAX_STOCK_PRICE = 100000f;
    public static readonly int MIN_EMPLOYEES = 0;
    public static readonly int MAX_EMPLOYEES = 10000000;
    
    // 시장 데이터 제약
    public static readonly float MIN_MARKET_CAP = 0f;
    public static readonly float MAX_MARKET_CAP = float.MaxValue;
    public static readonly float MIN_INTEREST_RATE = -0.1f; // 마이너스 금리 허용
    public static readonly float MAX_INTEREST_RATE = 1.0f;  // 100%
}
```

### 5.2 성능 최적화 고려사항

#### 메모리 레이아웃 최적화
```csharp
// ✅ 캐시 효율적인 구조 (64바이트 정렬)
[StructLayout(LayoutKind.Sequential, Pack = 4)]
public struct OptimizedPopulationComponent : IComponentData
{
    public float income;           // 4 bytes
    public float wealth;           // 4 bytes
    public float consumptionRate;  // 4 bytes
    public int populationID;       // 4 bytes
    public PopulationClass class;  // 1 byte
    public EmploymentStatus status;// 1 byte
    public byte age;              // 1 byte (0-120)
    public byte padding;          // 1 byte (정렬용)
    // Total: 20 bytes
}

// ❌ 비효율적인 구조 (패딩 낭비)
public struct InfficientComponent : IComponentData
{
    public double income;         // 8 bytes
    public bool isEmployed;       // 1 byte + 7 bytes padding
    public float wealth;          // 4 bytes + 4 bytes padding
    public int id;               // 4 bytes + 4 bytes padding
    // Total: 32 bytes (20바이트 데이터에 32바이트 사용)
}
```

#### 데이터 압축 전략
```csharp
// 정밀도를 희생하여 메모리 절약
public struct CompressedStockData : IComponentData
{
    public ushort stockPrice_x100;     // 가격 * 100 (소수점 둘째자리까지)
    public uint marketCap_millions;    // 시가총액 (백만원 단위)
    public byte volatility_percent;    // 변동성 (퍼센트, 0-100)
    public byte dividend_x100;         // 배당률 * 100
    
    // 압축 해제 함수
    public float StockPrice => stockPrice_x100 / 100f;
    public float MarketCap => marketCap_millions * 1000000f;
    public float Volatility => volatility_percent / 100f;
    public float DividendYield => dividend_x100 / 10000f;
}
```

## 다음 문서
- [UI 시스템 설계](./ui-system.md)
- [시스템 통합 가이드](./integration-guide.md)