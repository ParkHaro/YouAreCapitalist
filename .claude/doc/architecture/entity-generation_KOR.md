---
category: architecture
tags: [entity-generation, random, population, company, spawning]
related: [simulation-system_KOR.md, data-model.md, ecs-design_KOR.md]
parent: INDEX_KOR.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# 엔티티 생성 시스템

[🇬🇧 English Version](./entity-generation.md)

## 📍 네비게이션

[↩️ 아키텍처 문서로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 생성 개요

### 1.1 핵심 원칙

#### 현실적 분포 패턴
- **소득 불평등**: 현실 세계의 파레토 분포 (80/20 법칙) 준수
- **산업 균형**: 현실적 경제 섹터 비율 반영
- **연령 인구통계**: 자연스러운 인구 피라미드와 생산가능인구 중심
- **지역 변화**: 지리적, 문화적 다양성 요인

#### 절차적 생성 전략
```csharp
// 예시: 현실적 분포를 가진 인구 생성
public struct PopulationGenerationConfig
{
    public AnimationCurve ageDistribution;      // 인구 피라미드 곡선
    public AnimationCurve incomeDistribution;   // 소득을 위한 파레토 분포
    public AnimationCurve educationDistribution; // 교육 수준 곡선
    public float genderRatio;                   // 남성/여성 비율 (0.5 = 50/50)
}
```

### 1.2 생성 목표

#### 초기 인구: 1,000개 엔티티
- **저소득층 (60%)**: 600개 엔티티
- **중산층 (35%)**: 350개 엔티티  
- **고소득층 (5%)**: 50개 엔티티

#### 초기 회사: 100개 엔티티
- **소규모 기업 (70%)**: 70개 회사
- **중간 규모 기업 (25%)**: 25개 회사
- **대기업 (5%)**: 5개 회사

## 2. 인구 생성 시스템

### 2.1 인구 생성 시스템

#### 핵심 생성 로직
```csharp
public partial struct PopulationSpawnSystem : ISystem
{
    private Unity.Mathematics.Random random;
    
    public void OnCreate(ref SystemState state)
    {
        random = Unity.Mathematics.Random.CreateFromIndex((uint)System.DateTime.Now.Millisecond);
    }
    
    public void OnUpdate(ref SystemState state)
    {
        // 싱글톤에서 설정 가져오기
        var config = SystemAPI.GetSingleton<EconomicConfiguration>();
        
        // 필요시 초기 인구 생성
        if (ShouldSpawnInitialPopulation())
        {
            SpawnInitialPopulation(ref state, config);
        }
        
        // 동적 인구 증가 처리
        HandlePopulationGrowth(ref state, config);
    }
    
    private void SpawnInitialPopulation(ref SystemState state, EconomicConfiguration config)
    {
        var commandBuffer = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                                   .CreateCommandBuffer(state.WorldUnmanaged);
        
        for (int i = 0; i < config.initialPopulationCount; i++)
        {
            Entity newPop = commandBuffer.CreateEntity();
            
            // 기본 인구통계 생성
            var demographics = GenerateDemographics(config);
            var economics = GenerateEconomicStatus(demographics, config);
            var behavior = GenerateBehaviorProfile(demographics);
            
            // 컴포넌트 추가
            commandBuffer.AddComponent(newPop, new PopulationComponent 
            {
                populationID = i,
                socialClass = DetermineClass(economics.monthlyIncome),
                age = demographics.age,
                employment = DetermineEmployment(demographics, economics)
            });
            
            commandBuffer.AddComponent(newPop, economics);
            commandBuffer.AddComponent(newPop, demographics);
            commandBuffer.AddComponent(newPop, behavior);
        }
    }
}
```

### 2.2 인구통계 생성 알고리즘

#### 연령 분포
```csharp
private DemographicsComponent GenerateDemographics(EconomicConfiguration config)
{
    // 현실적 인구 피라미드를 사용한 연령 생성
    float ageRandom = random.NextFloat();
    float age = config.ageDistribution.Evaluate(ageRandom) * 80f + 18f; // 18-98세
    
    // 성별 분포
    Gender gender = random.NextFloat() < config.genderRatio ? Gender.Male : Gender.Female;
    
    // 연령대별 교육 수준
    EducationLevel education = GenerateEducationLevel(age);
    
    // 지역 분포
    Region region = GenerateRegion();
    
    return new DemographicsComponent
    {
        gender = gender,
        education = education,
        residence = region,
        age = (int)age,
        familyStatus = GenerateFamilyStatus(age, gender),
        dependents = GenerateDependents(age)
    };
}

private EducationLevel GenerateEducationLevel(float age)
{
    // 젊은 세대일수록 교육 수준이 높음
    float educationBonus = math.max(0, (60f - age) / 60f); // 젊은 사람에게 0-1 보너스
    float educationRoll = random.NextFloat() + educationBonus * 0.3f;
    
    if (educationRoll > 0.95f) return EducationLevel.Graduate;
    if (educationRoll > 0.75f) return EducationLevel.University;
    if (educationRoll > 0.50f) return EducationLevel.College;
    if (educationRoll > 0.30f) return EducationLevel.HighSchool;
    if (educationRoll > 0.15f) return EducationLevel.MiddleSchool;
    return EducationLevel.Elementary;
}
```

#### 경제적 지위 생성
```csharp
private EconomicStatusComponent GenerateEconomicStatus(DemographicsComponent demo, 
                                                     EconomicConfiguration config)
{
    // 교육과 연령에 따른 기본 소득
    float baseIncome = CalculateBaseIncome(demo.education, demo.age);
    
    // 소득 불평등을 위한 파레토 분포 적용
    float incomeMultiplier = SampleParetoDistribution(1.16f); // 현실적 파레토 매개변수
    float monthlyIncome = baseIncome * incomeMultiplier;
    
    // 연령과 저축 패턴에 기반한 총 자산
    float wealthMultiplier = math.max(0.1f, (demo.age - 18f) / 50f); // 시간이 지나면서 자산 축적
    float totalWealth = monthlyIncome * 12f * wealthMultiplier * random.NextFloat(0.5f, 2.0f);
    
    // 연령과 교육에 따른 위험 허용도
    float riskTolerance = GenerateRiskTolerance(demo.age, demo.education);
    
    return new EconomicStatusComponent
    {
        monthlyIncome = monthlyIncome,
        totalWealth = math.max(0, totalWealth),
        savingsRate = random.NextFloat(0.05f, 0.30f),
        consumptionRate = random.NextFloat(0.70f, 1.20f),
        riskTolerance = riskTolerance
    };
}

private float SampleParetoDistribution(float alpha)
{
    // 파레토 분포 랜덤 변수 생성
    // 20%가 80%의 부를 소유
    float uniform = random.NextFloat(0.001f, 0.999f); // 극값 방지
    return math.pow(1f - uniform, -1f / alpha);
}

private float CalculateBaseIncome(EducationLevel education, float age)
{
    // 교육 수준별 기본 급여 (월, 천 단위)
    float baseSalary = education switch
    {
        EducationLevel.Elementary => 150f,
        EducationLevel.MiddleSchool => 180f,
        EducationLevel.HighSchool => 220f,
        EducationLevel.College => 280f,
        EducationLevel.University => 350f,
        EducationLevel.Graduate => 450f,
        _ => 200f
    };
    
    // 연령 요인: 40-50대에 소득 정점
    float ageFactor = math.sin(math.PI * math.clamp((age - 20f) / 50f, 0f, 1f)) * 0.5f + 0.75f;
    
    return baseSalary * ageFactor * random.NextFloat(0.8f, 1.2f);
}
```

### 2.3 행동 프로필 생성

#### 성격 특성
```csharp
private BehaviorComponent GenerateBehaviorProfile(DemographicsComponent demo)
{
    // 상관관계 있는 성격 특성 생성
    float baseOptimism = random.NextFloat(0.3f, 0.7f);
    
    // 교육이 정보 수준과 합리성에 영향
    float informationLevel = (float)demo.education / 6f + random.NextFloat(-0.2f, 0.2f);
    informationLevel = math.clamp(informationLevel, 0f, 1f);
    
    // 연령이 동조성과 보수성에 영향
    float conformityLevel = (demo.age / 80f) * 0.6f + random.NextFloat(0.2f, 0.8f);
    conformityLevel = math.clamp(conformityLevel, 0f, 1f);
    
    // 충성도는 정규 분포
    float loyaltyLevel = SampleNormalDistribution(0.5f, 0.2f);
    
    return new BehaviorComponent
    {
        optimismLevel = baseOptimism,
        conformityLevel = conformityLevel,
        loyaltyLevel = loyaltyLevel,
        informationLevel = informationLevel
    };
}

private float SampleNormalDistribution(float mean, float stdDev)
{
    // 정규 분포를 위한 Box-Muller 변환
    float u1 = random.NextFloat(0.001f, 0.999f);
    float u2 = random.NextFloat(0.001f, 0.999f);
    
    float z0 = math.sqrt(-2f * math.log(u1)) * math.cos(2f * math.PI * u2);
    return math.clamp(mean + z0 * stdDev, 0f, 1f);
}
```

## 3. 회사 생성 시스템

### 3.1 회사 생성 시스템

#### 핵심 회사 생성
```csharp
public partial struct CompanySpawnSystem : ISystem
{
    private Unity.Mathematics.Random random;
    
    private void SpawnInitialCompanies(ref SystemState state, EconomicConfiguration config)
    {
        var commandBuffer = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                                   .CreateCommandBuffer(state.WorldUnmanaged);
        
        for (int i = 0; i < config.initialCompanyCount; i++)
        {
            Entity newCompany = commandBuffer.CreateEntity();
            
            // 회사 프로필 생성
            var company = GenerateCompanyProfile(i);
            var financial = GenerateFinancialProfile(company);
            var operation = GenerateOperationProfile(company, financial);
            var strategy = GenerateStrategyProfile(company);
            
            // 컴포넌트 추가
            commandBuffer.AddComponent(newCompany, company);
            commandBuffer.AddComponent(newCompany, financial);
            commandBuffer.AddComponent(newCompany, operation);
            commandBuffer.AddComponent(newCompany, strategy);
            
            // 상장 회사의 경우 주식 컴포넌트 추가
            if (company.isPubliclyTraded)
            {
                var stock = GenerateStockProfile(company, financial);
                commandBuffer.AddComponent(newCompany, stock);
            }
        }
    }
}
```

### 3.2 회사 프로필 생성

#### 산업 분포
```csharp
private CompanyComponent GenerateCompanyProfile(int companyID)
{
    // 현실적 경제 구성에 기반한 산업 분포
    IndustryType industry = SelectIndustryByWeight();
    CompanySize size = SelectCompanySize();
    CompanyStage stage = SelectCompanyStage(size);
    
    // 규모에 따른 상장 확률
    bool isPublic = ShouldBePubliclyTraded(size);
    
    // 산업에 기반한 회사명 생성
    FixedString64Bytes companyName = GenerateCompanyName(industry, companyID);
    
    return new CompanyComponent
    {
        companyID = companyID,
        companyName = companyName,
        industry = industry,
        size = size,
        stage = stage,
        isPubliclyTraded = isPublic,
        foundedDate = GenerateFoundedDate()
    };
}

private IndustryType SelectIndustryByWeight()
{
    float roll = random.NextFloat();
    
    // 현실적 산업 분포
    if (roll < 0.25f) return IndustryType.Retail;           // 25% - 서비스업
    if (roll < 0.45f) return IndustryType.Manufacturing;    // 20% - 제조업
    if (roll < 0.60f) return IndustryType.Technology;       // 15% - 기술업
    if (roll < 0.70f) return IndustryType.Construction;     // 10% - 건설업
    if (roll < 0.80f) return IndustryType.Finance;         // 10% - 금융 서비스
    if (roll < 0.85f) return IndustryType.Healthcare;      // 5% - 의료업
    if (roll < 0.90f) return IndustryType.Education;       // 5% - 교육업
    if (roll < 0.95f) return IndustryType.Transportation;   // 5% - 운송업
    return IndustryType.Agriculture;                        // 5% - 기타 업종
}

private CompanySize SelectCompanySize()
{
    float roll = random.NextFloat();
    
    // 현실적 회사 규모 분포 (소상공인 경제)
    if (roll < 0.70f) return CompanySize.Small;        // 70% - 소기업
    if (roll < 0.90f) return CompanySize.Medium;       // 20% - 중기업
    if (roll < 0.98f) return CompanySize.Large;        // 8% - 대기업
    return CompanySize.Conglomerate;                    // 2% - 대기업 집단
}
```

### 3.3 재무 프로필 생성

#### 매출과 수익성
```csharp
private FinancialComponent GenerateFinancialProfile(CompanyComponent company)
{
    // 규모와 산업별 기본 매출
    float baseRevenue = CalculateBaseRevenue(company.size, company.industry);
    
    // 산업별 승수와 단계 조정 적용
    float stageMultiplier = company.stage switch
    {
        CompanyStage.Seed => random.NextFloat(0.1f, 0.3f),
        CompanyStage.StartUp => random.NextFloat(0.2f, 0.8f),
        CompanyStage.Growth => random.NextFloat(0.8f, 2.0f),
        CompanyStage.Mature => random.NextFloat(0.9f, 1.2f),
        CompanyStage.Decline => random.NextFloat(0.4f, 0.8f),
        _ => 1.0f
    };
    
    float revenue = baseRevenue * stageMultiplier;
    
    // 운영비용 (매출의 70-90% 일반적)
    float operatingCost = revenue * random.NextFloat(0.70f, 0.90f);
    float netProfit = revenue - operatingCost;
    
    // 매출 기반 자산과 부채
    float totalAssets = revenue * random.NextFloat(0.8f, 2.5f);
    float totalLiabilities = totalAssets * random.NextFloat(0.30f, 0.70f);
    
    // 현금 흐름 변화
    float cashFlow = netProfit * random.NextFloat(0.8f, 1.2f);
    
    return new FinancialComponent
    {
        revenue = revenue,
        operatingCost = operatingCost,
        netProfit = netProfit,
        totalAssets = totalAssets,
        totalLiabilities = totalLiabilities,
        cashFlow = cashFlow,
        retainedEarnings = netProfit * random.NextFloat(0.5f, 0.9f)
    };
}

private float CalculateBaseRevenue(CompanySize size, IndustryType industry)
{
    // 회사 규모별 기본 월매출 (천 단위)
    float sizeMultiplier = size switch
    {
        CompanySize.Micro => random.NextFloat(10f, 50f),
        CompanySize.Small => random.NextFloat(50f, 500f),
        CompanySize.Medium => random.NextFloat(500f, 5000f),
        CompanySize.Large => random.NextFloat(5000f, 50000f),
        CompanySize.Conglomerate => random.NextFloat(50000f, 500000f),
        _ => 100f
    };
    
    // 산업별 매출 승수
    float industryMultiplier = industry switch
    {
        IndustryType.Technology => random.NextFloat(1.2f, 2.0f),    // 고마진
        IndustryType.Finance => random.NextFloat(1.1f, 1.8f),       // 금융 서비스
        IndustryType.Healthcare => random.NextFloat(1.0f, 1.5f),    // 안정적 수요
        IndustryType.Manufacturing => random.NextFloat(0.8f, 1.2f), // 자본집약적
        IndustryType.Retail => random.NextFloat(0.7f, 1.1f),        // 저마진
        IndustryType.Agriculture => random.NextFloat(0.6f, 0.9f),   // 원자재 가격
        _ => 1.0f
    };
    
    return sizeMultiplier * industryMultiplier;
}
```

### 3.4 운영 특성

#### 직원과 생산성 생성
```csharp
private OperationComponent GenerateOperationProfile(CompanyComponent company, FinancialComponent financial)
{
    // 회사 규모와 산업에 따른 직원 수
    int employeeCount = CalculateEmployeeCount(company.size, company.industry);
    
    // 단계와 산업에 따른 생산성 지수
    float productivity = GenerateProductivityIndex(company.stage, company.industry);
    
    // 시장 점유율 (대부분 회사는 소규모)
    float marketShare = CalculateMarketShare(company.size, financial.revenue);
    
    // 혁신과 고객 만족도
    float innovation = GenerateInnovationLevel(company.industry, company.stage);
    float customerSatisfaction = random.NextFloat(2.5f, 4.5f);
    
    // 규모와 연령과 관련된 브랜드 가치
    float brandValue = CalculateBrandValue(company, financial);
    
    return new OperationComponent
    {
        employeeCount = employeeCount,
        productivity = productivity,
        marketShare = marketShare,
        innovationLevel = innovation,
        customerSatisfaction = customerSatisfaction,
        brandValue = brandValue
    };
}

private int CalculateEmployeeCount(CompanySize size, IndustryType industry)
{
    // 규모별 기본 직원 수
    int baseEmployees = size switch
    {
        CompanySize.Micro => random.NextInt(1, 10),
        CompanySize.Small => random.NextInt(10, 50),
        CompanySize.Medium => random.NextInt(50, 300),
        CompanySize.Large => random.NextInt(300, 1000),
        CompanySize.Conglomerate => random.NextInt(1000, 10000),
        _ => 25
    };
    
    // 산업 노동집약도 승수
    float industryMultiplier = industry switch
    {
        IndustryType.Manufacturing => 1.3f,      // 노동집약적
        IndustryType.Retail => 1.2f,            // 서비스집약적
        IndustryType.Technology => 0.8f,         // 자본집약적
        IndustryType.Finance => 0.9f,           // 지식집약적
        _ => 1.0f
    };
    
    return (int)(baseEmployees * industryMultiplier);
}
```

## 4. 시장 초기화

### 4.1 시장 엔티티 생성

#### 산업 시장 설정
```csharp
public partial struct MarketInitializationSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        if (ShouldInitializeMarkets())
        {
            InitializeIndustryMarkets(ref state);
            InitializeFinancialMarkets(ref state);
        }
    }
    
    private void InitializeIndustryMarkets(ref SystemState state)
    {
        var commandBuffer = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                                   .CreateCommandBuffer(state.WorldUnmanaged);
        
        // 각 산업별 시장 생성
        var industries = System.Enum.GetValues<IndustryType>();
        foreach (var industry in industries)
        {
            Entity marketEntity = commandBuffer.CreateEntity();
            
            var market = new MarketComponent
            {
                marketID = (int)industry,
                marketType = DetermineMarketType(industry),
                industry = industry,
                marketSize = CalculateMarketSize(industry),
                growthRate = CalculateGrowthRate(industry),
                structure = DetermineMarketStructure(industry)
            };
            
            var dynamics = new MarketDynamicsComponent
            {
                currentPrice = CalculateInitialPrice(industry),
                demandLevel = random.NextFloat(0.7f, 1.3f),
                supplyLevel = random.NextFloat(0.7f, 1.3f),
                elasticity = CalculatePriceElasticity(industry),
                seasonalFactor = 1.0f,
                trendFactor = 1.0f
            };
            
            commandBuffer.AddComponent(marketEntity, market);
            commandBuffer.AddComponent(marketEntity, dynamics);
        }
    }
}
```

## 5. 설정 시스템

### 5.1 생성 매개변수

#### ScriptableObject 설정
```csharp
[CreateAssetMenu(fileName = "GenerationConfig", menuName = "Capitalism/Generation Configuration")]
public class GenerationConfiguration : ScriptableObject
{
    [Header("인구 생성")]
    public int targetPopulation = 1000;
    public AnimationCurve ageDistribution;
    public AnimationCurve incomeDistribution;
    public float genderRatio = 0.5f;
    
    [Header("회사 생성")]  
    public int targetCompanyCount = 100;
    public IndustryWeight[] industryWeights;
    public CompanySizeWeight[] sizeWeights;
    
    [Header("경제 매개변수")]
    public float baseInflationRate = 0.02f;
    public float unemploymentRate = 0.05f;
    public float economicGrowthRate = 0.03f;
    
    [Header("랜덤 시드")]
    public bool useRandomSeed = true;
    public uint fixedSeed = 12345;
}

[System.Serializable]
public struct IndustryWeight
{
    public IndustryType industry;
    public float weight;
    public float revenueMultiplier;
}

[System.Serializable]
public struct CompanySizeWeight  
{
    public CompanySize size;
    public float probability;
    public float publicTradingChance;
}
```

## 6. 검증과 테스트

### 6.1 생성 검증

#### 통계적 검증
```csharp
public static class GenerationValidator
{
    public static ValidationResult ValidatePopulationDistribution(NativeArray<PopulationComponent> population)
    {
        var result = new ValidationResult();
        
        // 소득 분포가 파레토 원리를 따르는지 검증
        float totalWealth = CalculateTotalWealth(population);
        float top20Wealth = CalculateTop20Wealth(population);
        float paretoRatio = top20Wealth / totalWealth;
        
        if (paretoRatio < 0.70f || paretoRatio > 0.90f)
        {
            result.AddWarning($"소득 분포 비율: {paretoRatio:P1} (예상: 70-90%)");
        }
        
        // 연령 분포 검증
        ValidateAgeDistribution(population, ref result);
        
        // 고용률 검증
        ValidateEmploymentRates(population, ref result);
        
        return result;
    }
    
    public static ValidationResult ValidateCompanyDistribution(NativeArray<CompanyComponent> companies)
    {
        var result = new ValidationResult();
        
        // 산업 분포 검증
        ValidateIndustryBalance(companies, ref result);
        
        // 규모 분포 검증
        ValidateSizeDistribution(companies, ref result);
        
        return result;
    }
}
```

## 다음 단계

1. **[구현 로드맵](./implementation-roadmap_KOR.md)** - 단계별 개발 가이드
2. **[시뮬레이션 시스템](./simulation-system_KOR.md)** - 생성된 엔티티들의 상호작용

## 관련 문서

- [데이터 모델](./data-model.md) - 컴포넌트 명세
- [ECS 설계](./ecs-design_KOR.md) - 시스템 아키텍처
- [기술 아키텍처](./technical-architecture_KOR.md) - 전체 시스템 설계