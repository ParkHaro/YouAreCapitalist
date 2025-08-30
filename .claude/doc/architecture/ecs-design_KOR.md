# ECS 시스템 설계 문서

[🇬🇧 English Version](./ecs-design.md)

## 📍 네비게이션

[↩️ 아키텍처 문서로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. ECS 아키텍처 개요

### 1.1 설계 원칙

#### Data-Oriented Design (DOD) 적용
```csharp
// ❌ 객체지향적 접근 (비효율적)
class Citizen
{
    public float income;
    public float wealth;
    public float consumptionRate;
    public void Update() { /* 개별 처리 */ }
}

// ✅ 데이터 중심 접근 (효율적)
struct PopulationComponent : IComponentData
{
    public float income;
    public float wealth;
    public float consumptionRate;
}
// → Job System으로 수만 개체 일괄 처리
```

#### 성능 우선 설계
- **메모리 지역성**: 관련 데이터를 연속된 메모리에 배치
- **SIMD 활용**: Burst Compiler를 통한 벡터화 연산
- **캐시 효율성**: 최소한의 메모리 액세스로 최대 성능

### 1.2 ECS World 구조

#### World 계층 구조
```
DefaultWorld (Main ECS World)
├── SimulationSystemGroup
│   ├── PopulationSystemGroup
│   ├── CompanySystemGroup  
│   ├── MarketSystemGroup
│   └── GovernmentSystemGroup
├── PresentationSystemGroup
│   ├── UIUpdateSystemGroup
│   └── DataVisualizationGroup
└── InitializationSystemGroup
```

## 2. 핵심 Components 설계

### 2.1 경제 주체 Components

#### 인구 (Population) Components
```csharp
// 기본 인구 데이터
public struct PopulationComponent : IComponentData
{
    public int populationID;           // 고유 식별자
    public PopulationClass socialClass; // 계층 (저소득/중산층/고소득)
    public float age;                  // 연령 (경제활동 영향)
    public EmploymentStatus employment; // 고용 상태
}

// 경제적 속성
public struct EconomicStatusComponent : IComponentData
{
    public float monthlyIncome;        // 월 소득
    public float totalWealth;          // 총 자산
    public float savingsRate;          // 저축률 (0.0~1.0)
    public float consumptionRate;      // 소비성향 (0.0~2.0)
    public float riskTolerance;        // 위험 감수도 (투자 성향)
}

// 소비 패턴
public struct ConsumptionComponent : IComponentData
{
    public float housingCost;          // 주거비
    public float foodExpense;          // 식료품비
    public float luxurySpending;       // 사치품 소비
    public float investmentAmount;     // 투자 금액
    public float debtAmount;           // 부채 규모
}

// 인구 분류 열거형
public enum PopulationClass : byte
{
    LowIncome = 0,    // 저소득층 (하위 30%)
    MiddleClass = 1,  // 중산층 (중위 60%) 
    HighIncome = 2    // 고소득층 (상위 10%)
}

public enum EmploymentStatus : byte
{
    Unemployed = 0,   // 실업
    Employed = 1,     // 고용
    SelfEmployed = 2, // 자영업
    Retired = 3       // 은퇴
}
```

#### 회사 (Company) Components
```csharp
// 회사 기본 정보
public struct CompanyComponent : IComponentData
{
    public int companyID;
    public IndustryType industry;      // 업종
    public CompanySize size;           // 기업 규모
    public bool isPubliclyTraded;      // 상장 여부
    public float foundedDate;          // 설립일 (게임 내 시간)
}

// 재무 상태
public struct FinancialComponent : IComponentData
{
    public float revenue;              // 매출
    public float operatingCost;        // 운영비용
    public float netProfit;            // 순이익
    public float totalAssets;          // 총자산
    public float totalLiabilities;     // 총부채
    public float cashFlow;             // 현금흐름
}

// 운영 데이터
public struct OperationComponent : IComponentData
{
    public int employeeCount;          // 직원 수
    public float productivity;         // 생산성 지수
    public float marketShare;          // 시장 점유율
    public float innovationLevel;      // 혁신 수준
    public float customerSatisfaction; // 고객 만족도
}

// 주식 데이터 (상장 기업만)
public struct StockComponent : IComponentData
{
    public float stockPrice;           // 주가
    public long sharesOutstanding;     // 발행 주식 수
    public float dividendYield;        // 배당 수익률
    public float pe_ratio;             // PER
    public float volatility;           // 변동성
}

// 업종 분류
public enum IndustryType : byte
{
    Technology = 0,     // 기술
    Finance = 1,        // 금융
    Manufacturing = 2,  // 제조업
    Retail = 3,         // 소매업
    Healthcare = 4,     // 의료
    Energy = 5,         // 에너지
    RealEstate = 6,     // 부동산
    Agriculture = 7     // 농업
}

public enum CompanySize : byte
{
    StartUp = 0,        // 스타트업 (<50명)
    Small = 1,          // 소기업 (50-250명)
    Medium = 2,         // 중기업 (250-1000명)
    Large = 3           // 대기업 (1000명+)
}
```

#### 시장 (Market) Components
```csharp
// 상품/서비스 시장
public struct MarketComponent : IComponentData
{
    public MarketType marketType;      // 시장 유형
    public float currentPrice;         // 현재 가격
    public float demand;               // 총 수요
    public float supply;               // 총 공급
    public float volatility;           // 가격 변동성
    public float tradingVolume;        // 거래량
}

// 금융 시장 (주식, 채권 등)
public struct FinancialMarketComponent : IComponentData
{
    public float marketIndex;          // 시장 지수
    public float totalMarketCap;       // 총 시가총액
    public float averagePE;            // 평균 PER
    public float interestRate;         // 기준금리
    public MarketSentiment sentiment;  // 시장 심리
}

public enum MarketType : byte
{
    Consumer = 0,       // 소비재
    Industrial = 1,     // 산업재
    Technology = 2,     // 기술
    Financial = 3,      // 금융상품
    Commodity = 4       // 원자재
}

public enum MarketSentiment : byte
{
    VeryBearish = 0,    // 매우 약세
    Bearish = 1,        // 약세
    Neutral = 2,        // 중립
    Bullish = 3,        // 강세
    VeryBullish = 4     // 매우 강세
}
```

### 2.2 글로벌 상태 Components (Singleton)

#### 경제 지표
```csharp
// 거시경제 지표
public struct MacroEconomicsComponent : IComponentData
{
    public float gdp;                  // GDP
    public float gdpGrowthRate;        // GDP 성장률
    public float inflationRate;        // 인플레이션율
    public float unemploymentRate;     // 실업률
    public float interestRate;         // 기준금리
    public float exchangeRate;         // 환율 (기준: USD)
}

// 정부 정책
public struct GovernmentComponent : IComponentData
{
    public float taxRate;              // 세율
    public float governmentSpending;   // 정부 지출
    public float publicDebt;           // 국가 부채
    public float welfareSpending;      // 복지 지출
    public PolicyStance economicPolicy; // 경제 정책 기조
}

public enum PolicyStance : byte
{
    VeryLoose = 0,      // 매우 완화적
    Loose = 1,          // 완화적
    Neutral = 2,        // 중립
    Tight = 3,          // 긴축적
    VeryTight = 4       // 매우 긴축적
}
```

## 3. 핵심 Systems 설계

### 3.1 Population Systems

#### PopulationBehaviorSystem
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateInGroup(typeof(PopulationSystemGroup))]
public partial class PopulationBehaviorSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = Time.DeltaTime;
        
        // Job으로 병렬 처리
        Dependency = new PopulationBehaviorJob
        {
            deltaTime = deltaTime,
            economicIndicators = GetSingleton<MacroEconomicsComponent>(),
            // Read/Write 컴포넌트 핸들러들...
        }.ScheduleParallel(Dependency);
    }
}

[BurstCompile]
public struct PopulationBehaviorJob : IJobEntity
{
    [ReadOnly] public float deltaTime;
    [ReadOnly] public MacroEconomicsComponent economicIndicators;
    
    void Execute(ref EconomicStatusComponent economic, 
                ref ConsumptionComponent consumption,
                in PopulationComponent population)
    {
        // 경제 상황에 따른 소비 패턴 조정
        float consumptionMultiplier = CalculateConsumptionMultiplier(
            economicIndicators.inflationRate,
            economicIndicators.unemploymentRate,
            population.socialClass
        );
        
        // 소비 결정
        consumption.foodExpense = economic.monthlyIncome * 
            GetBaseFoodRate(population.socialClass) * consumptionMultiplier;
        
        consumption.luxurySpending = math.max(0, 
            (economic.monthlyIncome - GetBaseLivingCost(population)) * 
            economic.consumptionRate * consumptionMultiplier
        );
        
        // 저축 및 투자
        float remainingIncome = economic.monthlyIncome - 
            consumption.foodExpense - consumption.housingCost - consumption.luxurySpending;
        
        if (remainingIncome > 0)
        {
            consumption.investmentAmount = remainingIncome * economic.riskTolerance;
            economic.totalWealth += remainingIncome - consumption.investmentAmount;
        }
    }
    
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private float CalculateConsumptionMultiplier(float inflation, float unemployment, PopulationClass socialClass)
    {
        // 경제 불안정성에 따른 소비 조정
        float baseMultiplier = 1.0f;
        
        // 인플레이션 영향 (부정적)
        baseMultiplier -= inflation * 0.5f;
        
        // 실업률 영향 (계층별 차등)
        float unemploymentImpact = socialClass switch
        {
            PopulationClass.LowIncome => unemployment * 1.5f,
            PopulationClass.MiddleClass => unemployment * 1.0f,
            PopulationClass.HighIncome => unemployment * 0.3f,
            _ => unemployment
        };
        
        baseMultiplier -= unemploymentImpact * 0.3f;
        
        return math.clamp(baseMultiplier, 0.1f, 2.0f);
    }
}
```

### 3.2 Company Systems

#### CompanyOperationSystem
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateInGroup(typeof(CompanySystemGroup))]
public partial class CompanyOperationSystem : SystemBase
{
    private EntityQuery marketQuery;
    private EntityQuery populationQuery;
    
    protected override void OnCreate()
    {
        marketQuery = GetEntityQuery(typeof(MarketComponent));
        populationQuery = GetEntityQuery(typeof(ConsumptionComponent));
    }
    
    protected override void OnUpdate()
    {
        // 시장 수요 계산
        var marketDemand = CalculateMarketDemand();
        
        Dependency = new CompanyOperationJob
        {
            marketDemand = marketDemand,
            deltaTime = Time.DeltaTime,
            macroEconomics = GetSingleton<MacroEconomicsComponent>()
        }.ScheduleParallel(Dependency);
    }
    
    private NativeHashMap<IndustryType, float> CalculateMarketDemand()
    {
        var demand = new NativeHashMap<IndustryType, float>(8, Allocator.TempJob);
        
        // 인구의 소비 패턴에서 업종별 수요 집계
        Entities.ForEach((in ConsumptionComponent consumption, in PopulationComponent population) =>
        {
            // 식료품 수요
            demand.TryGetValue(IndustryType.Retail, out float currentRetailDemand);
            demand[IndustryType.Retail] = currentRetailDemand + consumption.foodExpense;
            
            // 사치품 수요 (기술, 제조업)
            demand.TryGetValue(IndustryType.Technology, out float currentTechDemand);
            demand[IndustryType.Technology] = currentTechDemand + consumption.luxurySpending * 0.6f;
            
            // 기타 업종별 수요 계산...
        }).Run();
        
        return demand;
    }
}

[BurstCompile]
public struct CompanyOperationJob : IJobEntity
{
    [ReadOnly] public NativeHashMap<IndustryType, float> marketDemand;
    [ReadOnly] public float deltaTime;
    [ReadOnly] public MacroEconomicsComponent macroEconomics;
    
    void Execute(ref FinancialComponent financial,
                ref OperationComponent operation,
                in CompanyComponent company)
    {
        // 업종별 시장 수요 파악
        marketDemand.TryGetValue(company.industry, out float industryDemand);
        
        // 시장 점유율에 따른 매출 계산
        float potentialRevenue = industryDemand * operation.marketShare;
        
        // 생산성과 혁신 수준에 따른 실제 매출
        financial.revenue = potentialRevenue * 
            (0.7f + operation.productivity * 0.2f + operation.innovationLevel * 0.1f);
        
        // 운영비용 계산 (직원 급여 + 기타 비용)
        float laborCost = operation.employeeCount * GetAverageWage(company.industry) * deltaTime;
        float operationalOverhead = financial.revenue * GetOperationalCostRatio(company.size);
        financial.operatingCost = laborCost + operationalOverhead;
        
        // 순이익
        financial.netProfit = financial.revenue - financial.operatingCost;
        
        // 고용 결정 (수요 증가 시 고용 확대)
        if (financial.netProfit > 0 && industryDemand > financial.revenue * 1.2f)
        {
            operation.employeeCount = (int)(operation.employeeCount * 1.01f); // 1% 증가
        }
        else if (financial.netProfit < 0)
        {
            operation.employeeCount = (int)(operation.employeeCount * 0.99f); // 1% 감소
        }
        
        // 생산성 개선 (R&D 투자 시)
        if (financial.netProfit > 0)
        {
            float rdInvestment = financial.netProfit * 0.05f; // 이익의 5%를 R&D에
            operation.innovationLevel += rdInvestment * 0.001f * deltaTime;
            operation.productivity = math.min(operation.productivity + rdInvestment * 0.0005f * deltaTime, 2.0f);
        }
    }
    
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private float GetAverageWage(IndustryType industry)
    {
        return industry switch
        {
            IndustryType.Technology => 5000f,
            IndustryType.Finance => 4500f,
            IndustryType.Manufacturing => 3000f,
            IndustryType.Retail => 2000f,
            _ => 3000f
        };
    }
    
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private float GetOperationalCostRatio(CompanySize size)
    {
        return size switch
        {
            CompanySize.StartUp => 0.8f,    // 높은 비용 구조
            CompanySize.Small => 0.7f,
            CompanySize.Medium => 0.6f,
            CompanySize.Large => 0.5f,      // 규모의 경제
            _ => 0.6f
        };
    }
}
```

### 3.3 Market Systems

#### StockMarketSystem
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateInGroup(typeof(MarketSystemGroup))]
public partial class StockMarketSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = Time.DeltaTime;
        var macroEconomics = GetSingleton<MacroEconomicsComponent>();
        var marketSentiment = CalculateMarketSentiment(macroEconomics);
        
        Dependency = new StockPriceUpdateJob
        {
            deltaTime = deltaTime,
            marketSentiment = marketSentiment,
            interestRate = macroEconomics.interestRate,
            randomSeed = (uint)UnityEngine.Random.Range(1, int.MaxValue)
        }.ScheduleParallel(Dependency);
        
        // 시장 지수 업데이트
        UpdateMarketIndex();
    }
    
    private MarketSentiment CalculateMarketSentiment(MacroEconomicsComponent macro)
    {
        float sentimentScore = 0f;
        
        // GDP 성장률 영향
        sentimentScore += macro.gdpGrowthRate * 10f;
        
        // 인플레이션 영향 (부정적)
        sentimentScore -= macro.inflationRate * 5f;
        
        // 실업률 영향 (부정적)
        sentimentScore -= macro.unemploymentRate * 3f;
        
        // 금리 영향 (부정적, 주식에 대해)
        sentimentScore -= macro.interestRate * 2f;
        
        return sentimentScore switch
        {
            > 2f => MarketSentiment.VeryBullish,
            > 1f => MarketSentiment.Bullish,
            > -1f => MarketSentiment.Neutral,
            > -2f => MarketSentiment.Bearish,
            _ => MarketSentiment.VeryBearish
        };
    }
}

[BurstCompile]
public struct StockPriceUpdateJob : IJobEntity
{
    [ReadOnly] public float deltaTime;
    [ReadOnly] public MarketSentiment marketSentiment;
    [ReadOnly] public float interestRate;
    [ReadOnly] public uint randomSeed;
    
    void Execute([EntityInQueryIndex] int index, 
                ref StockComponent stock,
                in FinancialComponent financial,
                in OperationComponent operation)
    {
        var random = Random.CreateFromIndex((uint)(randomSeed + index));
        
        // 기본 주가 = 순이익 * PER
        float fundamentalValue = financial.netProfit * stock.pe_ratio;
        
        // 시장 심리에 따른 조정
        float sentimentMultiplier = marketSentiment switch
        {
            MarketSentiment.VeryBullish => 1.2f,
            MarketSentiment.Bullish => 1.1f,
            MarketSentiment.Neutral => 1.0f,
            MarketSentiment.Bearish => 0.9f,
            MarketSentiment.VeryBearish => 0.8f,
            _ => 1.0f
        };
        
        // 회사별 펀더멘털 요소
        float companyMultiplier = 1.0f;
        companyMultiplier *= (0.8f + operation.productivity * 0.4f);        // 생산성
        companyMultiplier *= (0.9f + operation.innovationLevel * 0.2f);     // 혁신성
        companyMultiplier *= (0.9f + operation.marketShare * 0.2f);         // 시장 점유율
        
        // 목표 주가
        float targetPrice = fundamentalValue * sentimentMultiplier * companyMultiplier;
        
        // 현재 주가에서 목표 주가로 점진적 이동 (평균 회귀)
        float priceChange = (targetPrice - stock.stockPrice) * 0.1f * deltaTime;
        
        // 랜덤 변동성 추가
        float randomVariation = random.NextFloat(-stock.volatility, stock.volatility) * stock.stockPrice * deltaTime;
        
        // 최종 주가 업데이트
        stock.stockPrice = math.max(0.01f, stock.stockPrice + priceChange + randomVariation);
        
        // 변동성 조정 (시장 불안정성에 따라)
        float baseVolatility = 0.02f; // 기본 2% 변동성
        float volatilityMultiplier = marketSentiment switch
        {
            MarketSentiment.VeryBullish => 0.8f,
            MarketSentiment.Bullish => 0.9f,
            MarketSentiment.Neutral => 1.0f,
            MarketSentiment.Bearish => 1.2f,
            MarketSentiment.VeryBearish => 1.5f,
            _ => 1.0f
        };
        
        stock.volatility = math.lerp(stock.volatility, baseVolatility * volatilityMultiplier, deltaTime * 0.1f);
        
        // 배당 수익률 계산 (이익의 일정 비율)
        if (financial.netProfit > 0)
        {
            stock.dividendYield = (financial.netProfit * 0.3f) / (stock.stockPrice * stock.sharesOutstanding);
        }
    }
}
```

## 4. 성능 최적화 전략

### 4.1 메모리 레이아웃 최적화

#### Chunk Iteration 최적화
```csharp
[BurstCompile]
public struct OptimizedPopulationJob : IJobChunk
{
    [ReadOnly] public ComponentTypeHandle<PopulationComponent> populationHandle;
    [ReadOnly] public ComponentTypeHandle<EconomicStatusComponent> economicHandle;
    public ComponentTypeHandle<ConsumptionComponent> consumptionHandle;
    
    public void Execute(in ArchetypeChunk chunk, int unfilteredChunkIndex, bool useEnabledMask, in v128 chunkEnabledMask)
    {
        // 청크 단위로 최적화된 처리
        var populations = chunk.GetNativeArray(ref populationHandle);
        var economics = chunk.GetNativeArray(ref economicHandle);
        var consumptions = chunk.GetNativeArray(ref consumptionHandle);
        
        // SIMD 연산을 위한 벡터화
        for (int i = 0; i < populations.Length; i += 4)
        {
            // 4개씩 병렬 처리
            ProcessFourEntities(
                ref consumptions.GetSubArray(i, math.min(4, populations.Length - i)),
                populations.GetSubArray(i, math.min(4, populations.Length - i)),
                economics.GetSubArray(i, math.min(4, populations.Length - i))
            );
        }
    }
    
    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private void ProcessFourEntities(ref NativeArray<ConsumptionComponent> consumptions,
                                   NativeArray<PopulationComponent> populations,
                                   NativeArray<EconomicStatusComponent> economics)
    {
        // SIMD를 활용한 4개 엔티티 동시 처리
        float4 incomes = new float4(
            economics[0].monthlyIncome,
            economics.Length > 1 ? economics[1].monthlyIncome : 0,
            economics.Length > 2 ? economics[2].monthlyIncome : 0,
            economics.Length > 3 ? economics[3].monthlyIncome : 0
        );
        
        float4 consumptionRates = new float4(
            economics[0].consumptionRate,
            economics.Length > 1 ? economics[1].consumptionRate : 0,
            economics.Length > 2 ? economics[2].consumptionRate : 0,
            economics.Length > 3 ? economics[3].consumptionRate : 0
        );
        
        // 벡터화된 소비 계산
        float4 luxurySpending = incomes * consumptionRates * 0.3f; // 30%가 사치품
        
        // 결과 저장
        for (int i = 0; i < math.min(4, consumptions.Length); i++)
        {
            var consumption = consumptions[i];
            consumption.luxurySpending = luxurySpending[i];
            consumptions[i] = consumption;
        }
    }
}
```

### 4.2 동적 LOD 시스템

#### 적응형 시뮬레이션 깊이
```csharp
public class AdaptiveLODSystem : SystemBase
{
    private EntityQuery allEntitiesQuery;
    private float targetFrameTime = 16.67f; // 60fps
    private SimulationLOD currentLOD = SimulationLOD.High;
    
    protected override void OnCreate()
    {
        allEntitiesQuery = GetEntityQuery(ComponentType.ReadOnly<PopulationComponent>());
    }
    
    protected override void OnUpdate()
    {
        int entityCount = allEntitiesQuery.CalculateEntityCount();
        float currentFrameTime = Time.unscaledDeltaTime * 1000f;
        
        // 프레임 시간과 엔티티 수에 따른 LOD 조절
        SimulationLOD newLOD = CalculateOptimalLOD(entityCount, currentFrameTime);
        
        if (newLOD != currentLOD)
        {
            currentLOD = newLOD;
            ApplyLODSettings(newLOD);
        }
        
        // LOD 정보를 싱글톤 엔티티에 저장
        SetSingleton(new SimulationLODComponent { currentLOD = currentLOD });
    }
    
    private SimulationLOD CalculateOptimalLOD(int entityCount, float frameTime)
    {
        // 성능 기반 LOD 선택
        if (frameTime > targetFrameTime * 1.5f || entityCount > 50000)
            return SimulationLOD.Low;
        else if (frameTime > targetFrameTime * 1.2f || entityCount > 25000)
            return SimulationLOD.Medium;
        else if (frameTime > targetFrameTime * 1.1f || entityCount > 10000)
            return SimulationLOD.High;
        else
            return SimulationLOD.Ultra;
    }
    
    private void ApplyLODSettings(SimulationLOD lod)
    {
        var populationSystem = World.GetOrCreateSystemManaged<PopulationBehaviorSystem>();
        var companySystem = World.GetOrCreateSystemManaged<CompanyOperationSystem>();
        var stockSystem = World.GetOrCreateSystemManaged<StockMarketSystem>();
        
        switch (lod)
        {
            case SimulationLOD.Ultra:
                // 모든 시스템 풀 디테일
                populationSystem.Enabled = true;
                companySystem.Enabled = true;
                stockSystem.Enabled = true;
                break;
                
            case SimulationLOD.High:
                // 대부분 시스템 활성화, 일부 간소화
                populationSystem.Enabled = true;
                companySystem.Enabled = true;
                stockSystem.Enabled = true;
                break;
                
            case SimulationLOD.Medium:
                // 핵심 시스템만 활성화
                populationSystem.Enabled = true;
                companySystem.Enabled = false; // 회사는 그룹 단위 처리
                stockSystem.Enabled = true;
                break;
                
            case SimulationLOD.Low:
                // 최소한의 시스템, 통계적 근사
                populationSystem.Enabled = false; // 통계적 처리
                companySystem.Enabled = false;
                stockSystem.Enabled = false;
                break;
        }
    }
}

public struct SimulationLODComponent : IComponentData
{
    public SimulationLOD currentLOD;
}

public enum SimulationLOD : byte
{
    Low = 0,      // 통계적 근사치
    Medium = 1,   // 그룹 단위 처리
    High = 2,     // 대부분 개별 처리
    Ultra = 3     // 모든 개체 개별 처리
}
```

## 5. 데이터 흐름 및 동기화

### 5.1 시스템 간 데이터 의존성

#### 실행 순서 최적화
```csharp
// 의존성 체인 정의
[UpdateInGroup(typeof(SimulationSystemGroup), OrderFirst = true)]
public partial class MacroEconomicsUpdateSystem : SystemBase { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(MacroEconomicsUpdateSystem))]
public partial class PopulationSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(PopulationSystemGroup))]
public partial class PopulationBehaviorSystem : SystemBase { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(PopulationSystemGroup))]
public partial class CompanySystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(CompanySystemGroup))]
public partial class CompanyOperationSystem : SystemBase { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(CompanySystemGroup))]
public partial class MarketSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(MarketSystemGroup))]
public partial class StockMarketSystem : SystemBase { }

[UpdateInGroup(typeof(SimulationSystemGroup), OrderLast = true)]
public partial class StatisticsAggregationSystem : SystemBase { }
```

### 5.2 캐시 및 중간 결과 저장

#### 통계 캐싱 시스템
```csharp
// 집계된 통계 캐시
public struct CachedStatisticsComponent : IComponentData
{
    public float totalGDP;
    public float averageIncome;
    public float totalMarketCap;
    public float unemploymentRate;
    
    public int lastUpdateFrame;
    public bool isDirty;
}

[UpdateInGroup(typeof(SimulationSystemGroup), OrderLast = true)]
public partial class StatisticsAggregationSystem : SystemBase
{
    protected override void OnUpdate()
    {
        var cachedStats = GetSingleton<CachedStatisticsComponent>();
        
        // 캐시가 유효하지 않거나 주기적 업데이트 시에만 재계산
        if (cachedStats.isDirty || Time.frameCount - cachedStats.lastUpdateFrame > 60)
        {
            UpdateCachedStatistics(ref cachedStats);
            SetSingleton(cachedStats);
        }
    }
    
    private void UpdateCachedStatistics(ref CachedStatisticsComponent cache)
    {
        // GDP 계산 (모든 회사의 부가가치 합)
        float totalRevenue = 0f;
        float totalCosts = 0f;
        
        Entities.ForEach((in FinancialComponent financial) =>
        {
            totalRevenue += financial.revenue;
            totalCosts += financial.operatingCost;
        }).Run();
        
        cache.totalGDP = totalRevenue - totalCosts;
        
        // 평균 소득 계산
        float totalIncome = 0f;
        int populationCount = 0;
        
        Entities.ForEach((in EconomicStatusComponent economic) =>
        {
            totalIncome += economic.monthlyIncome;
            populationCount++;
        }).Run();
        
        cache.averageIncome = populationCount > 0 ? totalIncome / populationCount : 0f;
        
        // 실업률 계산
        int employedCount = 0;
        int totalPopulation = 0;
        
        Entities.ForEach((in PopulationComponent population) =>
        {
            totalPopulation++;
            if (population.employment == EmploymentStatus.Employed)
                employedCount++;
        }).Run();
        
        cache.unemploymentRate = totalPopulation > 0 ? 
            1f - ((float)employedCount / totalPopulation) : 0f;
        
        // 총 시가총액
        cache.totalMarketCap = 0f;
        Entities.ForEach((in StockComponent stock) =>
        {
            cache.totalMarketCap += stock.stockPrice * stock.sharesOutstanding;
        }).Run();
        
        cache.lastUpdateFrame = Time.frameCount;
        cache.isDirty = false;
    }
}
```

## 다음 문서
- [데이터 모델 명세](./data-model_KOR.md)
- [UI 시스템 설계](./ui-system_KOR.md) 
- [시스템 통합 가이드](./integration-guide_KOR.md)