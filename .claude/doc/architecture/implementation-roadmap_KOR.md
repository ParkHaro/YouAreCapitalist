---
category: architecture
tags: [implementation, roadmap, development, phases, milestone]
related: [simulation-system_KOR.md, entity-generation_KOR.md, ecs-design_KOR.md]
parent: INDEX_KOR.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# 구현 로드맵

[🇬🇧 English Version](./implementation-roadmap.md)

## 📍 네비게이션

[↩️ 아키텍처 문서로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 개발 개요

### 1.1 구현 전략

#### 점진적 개발 접근법
- **MVP 우선**: 가능한 한 빠르게 기본 시뮬레이션을 실행
- **반복적 개선**: 관리 가능한 단위로 복잡성 추가
- **데이터 중심 설계**: ECS 데이터 흐름이 올바르게 작동하도록 집중
- **조기 테스트**: 다음 단계로 넘어가기 전에 각 단계를 검증

#### 목표 일정
- **1단계**: 1-2주 - 기본 엔티티 생성
- **2단계**: 2-3주 - 자율 행동 시스템
- **3단계**: 2-3주 - 경제적 상호작용
- **4단계**: 3-4주 - 고급 기능 및 완성도

### 1.2 성공 지표

#### 1단계 성공 기준
- 1,000개 Pop + 100개 회사 성공적 생성
- 모든 엔티티가 유효한 컴포넌트 데이터 보유
- 엔티티 수와 통계를 보여주는 기본 UI

#### 최종 성공 기준
- **"1000개 Pop + 100개 Company 자동 시뮬레이션"**
- 엔티티들이 자율적 의사결정 수행
- 기본 경제 사이클 작동 (고용, 소비, 생산)
- 실시간 통계 및 모니터링 작동

## 2. 1단계: 기반 설정

### 2.1 Unity 프로젝트 설정

#### 패키지 요구사항
```json
{
  "dependencies": {
    "com.unity.entities": "1.0.16",
    "com.unity.entities.graphics": "1.0.16", 
    "com.unity.jobs": "0.70.0",
    "com.unity.collections": "2.2.1",
    "com.unity.mathematics": "1.2.6",
    "com.unity.burst": "1.8.12",
    "com.unity.ui.toolkit": "1.0.0-preview.11"
  }
}
```

#### 프로젝트 구조 설정
```
Assets/
├── Scripts/
│   ├── Components/
│   │   ├── PopulationComponents.cs
│   │   ├── CompanyComponents.cs
│   │   └── MarketComponents.cs
│   ├── Systems/
│   │   ├── Generation/
│   │   ├── Simulation/
│   │   └── Statistics/
│   ├── Configuration/
│   │   └── ScriptableObjects/
│   └── UI/
├── Data/
│   └── Configurations/
└── UI/
    └── Toolkit/
```

#### 구현 체크리스트 - 프로젝트 설정
- [ ] Unity DOTS 패키지 설치
- [ ] 폴더 구조 생성
- [ ] 어셈블리 정의 설정
- [ ] ECS World가 있는 기본 씬 생성
- [ ] DOTS 작동 확인 (테스트 엔티티 생성)

### 2.2 핵심 데이터 컴포넌트

#### 필수 컴포넌트 구현
```csharp
// 파일: Assets/Scripts/Components/PopulationComponents.cs
using Unity.Entities;
using Unity.Mathematics;

// 기본 인구 신원
public struct PopulationComponent : IComponentData
{
    public int populationID;
    public PopulationClass socialClass;
    public float age;
    public EmploymentStatus employment;
}

// 경제적 지위와 자원  
public struct EconomicStatusComponent : IComponentData
{
    public float monthlyIncome;
    public float totalWealth;
    public float savingsRate;
    public float consumptionRate;
    public float riskTolerance;
}

// 인구통계 정보
public struct DemographicsComponent : IComponentData
{
    public Gender gender;
    public EducationLevel education;
    public Region residence;
    public FamilyStatus familyStatus;
    public int dependents;
}

// 행동 특성
public struct BehaviorComponent : IComponentData
{
    public float optimismLevel;      
    public float conformityLevel;    
    public float loyaltyLevel;       
    public float informationLevel;   
}

// 의사결정 상태
public struct PopulationDecisionComponent : IComponentData
{
    public DecisionType pendingDecision;
    public float decisionConfidence;
    public float decisionDeadline;
    public Entity targetEntity;
}
```

#### 구현 체크리스트 - 컴포넌트
- [ ] 모든 구조체가 포함된 PopulationComponents.cs 생성
- [ ] 비즈니스 엔티티가 포함된 CompanyComponents.cs 생성
- [ ] 시장 데이터가 포함된 MarketComponents.cs 생성
- [ ] 싱글톤용 ConfigurationComponents.cs 생성
- [ ] 컴포넌트가 오류 없이 컴파일되는지 테스트

### 2.3 설정 시스템

#### ScriptableObject 설정
```csharp
// 파일: Assets/Scripts/Configuration/EconomicConfiguration.cs
[CreateAssetMenu(fileName = "EconomicConfig", menuName = "Capitalism/Economic Configuration")]
public class EconomicConfiguration : ScriptableObject
{
    [Header("인구 생성")]
    public int initialPopulationCount = 1000;
    public AnimationCurve ageDistribution;
    public AnimationCurve incomeDistribution;
    public float genderRatio = 0.5f;
    
    [Header("회사 생성")]
    public int initialCompanyCount = 100;
    public IndustryDistribution[] industryDistributions;
    
    [Header("시뮬레이션 매개변수")]
    public float timeScale = 1.0f;
    public float economicUpdateRate = 1.0f; // 초당 업데이트 수
}

[System.Serializable]
public struct IndustryDistribution
{
    public IndustryType industry;
    public float weight;
    public float averageRevenue;
}
```

#### 구현 체크리스트 - 설정
- [ ] EconomicConfiguration ScriptableObject 생성
- [ ] 기본 설정 에셋 생성
- [ ] 설정 곡선 추가 (연령, 소득 분포)
- [ ] 설정 싱글톤 컴포넌트 생성
- [ ] 게임에서 설정 로딩 테스트

### 2.4 기본 엔티티 생성

#### 인구 생성 시스템
```csharp
// 파일: Assets/Scripts/Systems/Generation/PopulationSpawnSystem.cs
public partial struct PopulationSpawnSystem : ISystem
{
    private Unity.Mathematics.Random random;
    private bool hasSpawnedInitial;
    
    public void OnCreate(ref SystemState state)
    {
        random = Unity.Mathematics.Random.CreateFromIndex((uint)System.DateTime.Now.Millisecond);
        hasSpawnedInitial = false;
    }
    
    public void OnUpdate(ref SystemState state)
    {
        if (!hasSpawnedInitial)
        {
            SpawnInitialPopulation(ref state);
            hasSpawnedInitial = true;
        }
    }
    
    private void SpawnInitialPopulation(ref SystemState state)
    {
        // 싱글톤 설정 가져오기
        if (!SystemAPI.TryGetSingleton<EconomicConfigurationData>(out var config))
            return;
            
        var commandBuffer = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                                   .CreateCommandBuffer(state.WorldUnmanaged);
        
        for (int i = 0; i < config.initialPopulationCount; i++)
        {
            Entity newPop = commandBuffer.CreateEntity();
            
            // 랜덤 인구통계 생성
            var demographics = GenerateRandomDemographics();
            var economics = GenerateRandomEconomics(demographics);
            var behavior = GenerateRandomBehavior();
            
            // 기본 인구 데이터
            commandBuffer.AddComponent(newPop, new PopulationComponent 
            {
                populationID = i,
                socialClass = DetermineClass(economics.monthlyIncome),
                age = demographics.age,
                employment = DetermineEmployment(demographics)
            });
            
            commandBuffer.AddComponent(newPop, economics);
            commandBuffer.AddComponent(newPop, demographics);
            commandBuffer.AddComponent(newPop, behavior);
        }
    }
}
```

#### 구현 체크리스트 - 기본 생성
- [ ] PopulationSpawnSystem 생성
- [ ] 기본 랜덤 생성 메서드 구현
- [ ] CompanySpawnSystem 생성 (비슷한 패턴)
- [ ] 엔티티 생성 테스트 (1000 + 100개 엔티티 생성해야 함)
- [ ] 모든 컴포넌트가 유효한 데이터를 가지는지 확인

### 2.5 기본 통계 및 UI

#### 통계 시스템
```csharp
// 파일: Assets/Scripts/Systems/Statistics/StatisticsSystem.cs
public partial struct StatisticsSystem : SystemBase
{
    protected override void OnUpdate()
    {
        // 계층별 인구 수 계산
        int totalPop = 0;
        int lowIncome = 0, middleClass = 0, highIncome = 0;
        
        Entities.ForEach((in PopulationComponent pop) => {
            totalPop++;
            switch(pop.socialClass)
            {
                case PopulationClass.LowIncome: lowIncome++; break;
                case PopulationClass.MiddleClass: middleClass++; break;
                case PopulationClass.HighIncome: highIncome++; break;
            }
        }).Run();
        
        // 회사 수 계산
        int totalCompanies = 0;
        Entities.ForEach((in CompanyComponent company) => {
            totalCompanies++;
        }).Run();
        
        // 싱글톤 통계 업데이트
        if (SystemAPI.TryGetSingleton<GameStatistics>(out var stats))
        {
            stats.totalPopulation = totalPop;
            stats.totalCompanies = totalCompanies;
            stats.lowIncomeCount = lowIncome;
            stats.middleClassCount = middleClass;
            stats.highIncomeCount = highIncome;
            
            SystemAPI.SetSingleton(stats);
        }
    }
}
```

#### 구현 체크리스트 - 통계 및 UI
- [ ] 실시간 집계를 위한 StatisticsSystem 생성
- [ ] GameStatistics 싱글톤 컴포넌트 생성
- [ ] UI Toolkit을 사용한 기본 UI 생성
- [ ] 표시 항목: 총 인구, 총 회사 수, 계층별 분류
- [ ] 통계가 실시간으로 업데이트되는지 테스트

## 3. 2단계: 자율 행동

### 3.1 기본 의사결정 시스템

#### 인구 의사결정 프레임워크
```csharp
// 파일: Assets/Scripts/Systems/Simulation/PopulationBehaviorSystem.cs
public partial struct PopulationBehaviorSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (population, economic, decision) in 
                 SystemAPI.Query<PopulationComponent, EconomicStatusComponent, PopulationDecisionComponent>())
        {
            // 결정 마감시간 업데이트
            if (decision.decisionDeadline > 0)
            {
                decision.decisionDeadline -= deltaTime;
            }
            
            // 필요시 새로운 결정 생성
            if (decision.decisionDeadline <= 0)
            {
                decision.pendingDecision = ChooseRandomDecision(population, economic);
                decision.decisionConfidence = UnityEngine.Random.Range(0.5f, 1.0f);
                decision.decisionDeadline = UnityEngine.Random.Range(5f, 30f); // 5-30초
            }
        }
    }
    
    private DecisionType ChooseRandomDecision(PopulationComponent pop, EconomicStatusComponent econ)
    {
        // 2단계용 간단한 의사결정 로직
        if (econ.monthlyIncome < 200f)
            return DecisionType.SeekJob;
        else if (econ.totalWealth > econ.monthlyIncome * 10f)
            return DecisionType.Invest;
        else
            return DecisionType.Consume;
    }
}
```

#### 구현 체크리스트 - 기본 행동
- [ ] 간단한 의사결정이 포함된 PopulationBehaviorSystem 생성
- [ ] 기본 비즈니스 로직이 포함된 CompanyOperationSystem 생성
- [ ] 의사결정 타이머 및 랜덤 의사결정 추가
- [ ] 엔티티가 시간에 따라 의사결정을 변경하는지 테스트
- [ ] 디버깅용 의사결정 로깅 추가

### 3.2 고용 시스템

#### 구인 매칭 시스템
```csharp
// 파일: Assets/Scripts/Systems/Simulation/EmploymentSystem.cs
public partial struct EmploymentMatchingSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // 일자리를 찾는 실업자 찾기
        var jobSeekers = new NativeList<Entity>(Allocator.Temp);
        var jobOpenings = new NativeList<Entity>(Allocator.Temp);
        
        // 구직자 수집
        foreach (var (entity, pop, decision) in 
                 SystemAPI.Query<Entity, PopulationComponent, PopulationDecisionComponent>()
                         .WithAll<RefRO<PopulationComponent>>())
        {
            if (pop.employment == EmploymentStatus.Unemployed && 
                decision.pendingDecision == DecisionType.SeekJob)
            {
                jobSeekers.Add(entity);
            }
        }
        
        // 채용 기회가 있는 회사 수집  
        foreach (var (entity, company, operation) in 
                 SystemAPI.Query<Entity, CompanyComponent, OperationComponent>())
        {
            if (operation.employeeCount < GetMaxEmployees(company))
            {
                jobOpenings.Add(entity);
            }
        }
        
        // 구직자와 채용 기회 매칭 (간단한 랜덤 매칭)
        int matches = math.min(jobSeekers.Length, jobOpenings.Length);
        for (int i = 0; i < matches; i++)
        {
            MatchEmployeeWithCompany(jobSeekers[i], jobOpenings[i], ref state);
        }
        
        jobSeekers.Dispose();
        jobOpenings.Dispose();
    }
}
```

#### 구현 체크리스트 - 고용 시스템
- [ ] EmploymentMatchingSystem 생성
- [ ] 기본 구직자 식별 구현
- [ ] 회사 채용 로직 생성
- [ ] 시간에 따른 실업률 변화 테스트
- [ ] 고용 통계 추적 추가

### 3.3 기본 경제적 상호작용

#### 소비 시스템
```csharp
// 파일: Assets/Scripts/Systems/Simulation/ConsumptionSystem.cs
public partial struct ConsumptionSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (population, economic, decision) in 
                 SystemAPI.Query<RefRO<PopulationComponent>, RefRW<EconomicStatusComponent>, 
                                RefRO<PopulationDecisionComponent>>())
        {
            if (decision.ValueRO.pendingDecision == DecisionType.Consume)
            {
                // 간단한 소비: 주기적으로 돈 지출
                float consumptionAmount = economic.ValueRO.monthlyIncome * 0.1f * deltaTime; // 초당 10%
                economic.ValueRW.totalWealth = math.max(0, economic.ValueRO.totalWealth - consumptionAmount);
                
                // TODO: 돈을 쓸 회사 찾기
                // TODO: 회사 수익 업데이트
            }
        }
    }
}
```

#### 구현 체크리스트 - 경제적 상호작용
- [ ] 돈 지출용 ConsumptionSystem 생성
- [ ] 소비로부터 기본 회사 수익 생성
- [ ] 간단한 투자 시스템 구현
- [ ] Pop과 회사 간 돈의 흐름 테스트
- [ ] 부의 분포 통계 추가

## 4. 3단계: 시장 역학

### 4.1 공급과 수요

#### 시장 가격 시스템
```csharp
// 파일: Assets/Scripts/Systems/Simulation/MarketDynamicsSystem.cs
public partial struct MarketDynamicsSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (market, dynamics) in 
                 SystemAPI.Query<RefRO<MarketComponent>, RefRW<MarketDynamicsComponent>>())
        {
            // 공급 계산 (이 산업 내 회사들로부터)
            float totalSupply = CalculateIndustrySupply(market.ValueRO.industry);
            
            // 수요 계산 (인구 소비로부터)
            float totalDemand = CalculateIndustryDemand(market.ValueRO.industry);
            
            // 간단한 가격 발견: 가격이 균형점을 향해 이동
            float equilibriumPrice = totalDemand / totalSupply;
            float currentPrice = dynamics.ValueRO.currentPrice;
            float priceChange = (equilibriumPrice - currentPrice) * 0.1f; // 10% 조정
            
            dynamics.ValueRW.currentPrice = math.max(0.1f, currentPrice + priceChange);
            dynamics.ValueRW.demandLevel = totalDemand;
            dynamics.ValueRW.supplyLevel = totalSupply;
        }
    }
}
```

#### 구현 체크리스트 - 시장 역학
- [ ] MarketDynamicsSystem 생성
- [ ] 공급/수요 계산 구현
- [ ] 가격 발견 메커니즘 생성
- [ ] 시장 가격이 시간에 따라 변화하는지 테스트
- [ ] 시장 통계 및 모니터링 추가

### 4.2 회사 운영

#### 생산 및 수익 시스템
```csharp
// 파일: Assets/Scripts/Systems/Simulation/CompanyOperationSystem.cs
public partial struct CompanyOperationSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (company, financial, operation) in 
                 SystemAPI.Query<RefRO<CompanyComponent>, RefRW<FinancialComponent>, 
                                RefRO<OperationComponent>>())
        {
            // 직원에 기반한 간단한 생산
            float productionCapacity = operation.ValueRO.employeeCount * operation.ValueRO.productivity;
            
            // 시장 수요로부터 수익
            float marketDemand = GetIndustryDemand(company.ValueRO.industry);
            float actualRevenue = math.min(productionCapacity, marketDemand) * deltaTime;
            
            // 운영비용 (직원 급여 등)
            float operatingCosts = operation.ValueRO.employeeCount * 300f * deltaTime; // 직원당 일일 $300
            
            // 재무 상태 업데이트
            financial.ValueRW.revenue += actualRevenue;
            financial.ValueRW.operatingCost += operatingCosts;
            financial.ValueRW.netProfit = financial.ValueRO.revenue - financial.ValueRO.operatingCost;
            financial.ValueRW.cashFlow = financial.ValueRO.netProfit;
        }
    }
}
```

#### 구현 체크리스트 - 회사 운영
- [ ] CompanyOperationSystem 생성
- [ ] 생산 능력 계산 구현
- [ ] 시장 수요로부터 수익 생성 생성
- [ ] 운영비용 계산 추가
- [ ] 시간에 따른 회사 수익성 테스트

## 5. 4단계: 고급 기능

### 5.1 랜덤 이벤트

#### 이벤트 시스템 프레임워크
```csharp
// 파일: Assets/Scripts/Systems/Events/RandomEventSystem.cs
public partial struct RandomEventSystem : ISystem
{
    private Unity.Mathematics.Random random;
    private float eventTimer;
    
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        eventTimer -= deltaTime;
        
        if (eventTimer <= 0)
        {
            // 랜덤 이벤트 발생
            if (random.NextFloat() < 0.1f) // 10% 확률
            {
                TriggerRandomEvent(ref state);
            }
            
            eventTimer = 60f; // 매분마다 체크
        }
    }
    
    private void TriggerRandomEvent(ref SystemState state)
    {
        EventType eventType = (EventType)random.NextInt(0, 5);
        
        switch(eventType)
        {
            case EventType.EconomicBoom:
                ApplyEconomicBoost();
                break;
            case EventType.Recession:
                ApplyEconomicRecession();  
                break;
            // ... 다른 이벤트들
        }
    }
}
```

#### 구현 체크리스트 - 랜덤 이벤트
- [ ] RandomEventSystem 생성
- [ ] 기본 이벤트 유형 구현 (호황, 불황 등)
- [ ] 이벤트 효과 적용 생성
- [ ] 이벤트가 인구와 회사에 영향을 주는지 테스트
- [ ] 이벤트 알림 UI 추가

### 5.2 고급 UI 및 시각화

#### 실시간 대시보드
```csharp
// 파일: Assets/Scripts/UI/EconomicDashboard.cs
public class EconomicDashboard : MonoBehaviour
{
    [SerializeField] private Label populationLabel;
    [SerializeField] private Label companyLabel;
    [SerializeField] private Label unemploymentLabel;
    [SerializeField] private Label averageWealthLabel;
    
    void Update()
    {
        if (World.DefaultGameObjectInjectionWorld != null)
        {
            var statsSystem = World.DefaultGameObjectInjectionWorld.GetExistingSystemManaged<StatisticsSystem>();
            if (statsSystem != null && SystemAPI.TryGetSingleton<GameStatistics>(out var stats))
            {
                populationLabel.text = $"인구: {stats.totalPopulation}";
                companyLabel.text = $"회사: {stats.totalCompanies}";
                unemploymentLabel.text = $"실업률: {stats.unemploymentRate:P1}";
                averageWealthLabel.text = $"평균 자산: ${stats.averageWealth:N0}";
            }
        }
    }
}
```

#### 구현 체크리스트 - 고급 UI
- [ ] 포괄적 통계 대시보드 생성
- [ ] 경제 지표용 실시간 차트 추가
- [ ] 엔티티 검사 패널 생성
- [ ] 시뮬레이션 속도 컨트롤 추가
- [ ] 저장/로드 기능 구현

### 5.3 성능 최적화

#### Job System 구현
```csharp
// 파일: Assets/Scripts/Jobs/PopulationUpdateJob.cs
[BurstCompile]
public struct PopulationUpdateJob : IJobChunk
{
    public float deltaTime;
    
    [ReadOnly] public ComponentTypeHandle<PopulationComponent> PopulationHandle;
    public ComponentTypeHandle<EconomicStatusComponent> EconomicHandle;
    
    public void Execute(in ArchetypeChunk chunk, int unfilteredChunkIndex, 
                       bool useEnabledMask, in v128 chunkEnabledMask)
    {
        var populations = chunk.GetNativeArray(ref PopulationHandle);
        var economics = chunk.GetNativeArray(ref EconomicHandle);
        
        for (int i = 0; i < chunk.Count; i++)
        {
            var economic = economics[i];
            
            // 소득에 따른 자산 업데이트
            economic.totalWealth += economic.monthlyIncome * (deltaTime / 30f); // 월 소득
            
            economics[i] = economic;
        }
    }
}
```

#### 구현 체크리스트 - 최적화
- [ ] 주요 시스템을 Job System 사용으로 변환
- [ ] 성능이 중요한 코드에 Burst 컴파일 추가
- [ ] 원거리 엔티티용 LOD 시스템 구현
- [ ] 성능 프로파일링 및 모니터링 추가
- [ ] 메모리 할당 최적화

## 6. 테스트 및 검증

### 6.1 단위 테스트

#### 시스템 테스트 프레임워크
```csharp
// 파일: Assets/Scripts/Tests/PopulationSpawnTest.cs
[TestFixture]
public class PopulationSpawnSystemTests
{
    private World testWorld;
    private PopulationSpawnSystem spawnSystem;
    
    [SetUp]
    public void Setup()
    {
        testWorld = new World("TestWorld");
        spawnSystem = testWorld.GetOrCreateSystem<PopulationSpawnSystem>();
    }
    
    [Test]
    public void SpawnSystem_CreatesCorrectNumberOfEntities()
    {
        // 준비
        var config = new EconomicConfigurationData { initialPopulationCount = 100 };
        testWorld.EntityManager.CreateSingleton(config);
        
        // 실행
        spawnSystem.Update();
        
        // 검증
        var query = testWorld.EntityManager.CreateEntityQuery(typeof(PopulationComponent));
        Assert.AreEqual(100, query.CalculateEntityCount());
    }
}
```

### 6.2 통합 테스트

#### 전체 시뮬레이션 테스트
```csharp
[Test]
public void FullSimulation_RunsFor60Seconds_WithoutErrors()
{
    // 완전한 시뮬레이션 설정
    var world = CreateTestWorld();
    var systems = CreateAllSystems(world);
    
    // 60초간 시뮬레이션 실행
    float totalTime = 0f;
    while (totalTime < 60f)
    {
        UpdateAllSystems(systems, 0.016f); // 60 FPS
        totalTime += 0.016f;
    }
    
    // 시뮬레이션 상태가 유효한지 확인
    AssertSimulationHealthy(world);
}
```

#### 구현 체크리스트 - 테스트
- [ ] 모든 주요 시스템용 단위 테스트 생성
- [ ] 전체 시뮬레이션용 통합 테스트 추가
- [ ] 성능 벤치마크 생성
- [ ] 엔티티 데이터용 자동 검증 추가
- [ ] 시간에 따른 시뮬레이션 안정성 테스트

## 7. 마일스톤 검증

### 7.1 단계 완료 기준

#### 1단계 완료 조건:
- [ ] 유효한 데이터를 가진 1000개 인구 엔티티 생성
- [ ] 유효한 데이터를 가진 100개 회사 엔티티 생성
- [ ] 기본 UI에서 정확한 엔티티 수 표시
- [ ] 모든 시스템이 오류 없이 실행
- [ ] 성능: 모든 엔티티와 함께 >30 FPS

#### 2단계 완료 조건:
- [ ] 엔티티가 5-30초마다 의사결정 수행
- [ ] 고용 시스템이 Pop과 회사를 매칭
- [ ] 기본 소비가 Pop 자산을 감소시킴
- [ ] 소비로부터 회사 수익 증가
- [ ] 실업률이 현실적으로 변동 (3-10%)

#### 3단계 완료 조건:
- [ ] 시장 가격이 공급/수요에 따라 변화
- [ ] 회사가 시장 수요로부터 수익 생성
- [ ] 인구 소비가 시장 가격에 영향
- [ ] 기본 경제 사이클 가시적 (호황/불황 주기)
- [ ] 경제 통계가 의미 있는 변화 추적

#### 4단계 완료 조건:
- [ ] 랜덤 이벤트가 시뮬레이션에 의미 있게 영향
- [ ] 고급 UI가 포괄적 통계 표시
- [ ] Job System + Burst로 성능 최적화
- [ ] 저장/로드 기능 작동
- [ ] 전체 시뮬레이션이 10분+ 안정적 실행

### 7.2 최종 성공 지표

#### **"1000개 Pop + 100개 Company 자동 시뮬레이션"** 달성 조건:
- [ ] 모든 엔티티가 플레이어 입력 없이 자율 운영
- [ ] 경제적 상호작용이 현실적 패턴 생성
- [ ] 고용, 소비, 생산 사이클 기능
- [ ] 통계가 의미 있는 경제 지표 표시
- [ ] 시뮬레이션이 창발적 경제 행동 시연
- [ ] 성능이 전체적으로 >30 FPS 유지

## 다음 단계

이 로드맵 완료 후:
1. **완성도 및 개선** - UI 개선, 더 많은 이벤트 유형 추가, 매개변수 미세 조정
2. **플레이어 상호작용** - 투자 및 정책 영향 메커니즘 추가  
3. **고급 경제학** - 주식시장, 은행, 정부 정책 시스템
4. **확장성** - 고급 최적화로 10,000+ 엔티티 지원

## 관련 문서

- [시뮬레이션 시스템](./simulation-system_KOR.md) - 완전한 시스템 아키텍처
- [엔티티 생성](./entity-generation_KOR.md) - 상세한 생성 알고리즘
- [ECS 설계](./ecs-design_KOR.md) - 핵심 ECS 패턴과 관행