---
category: reference
tags: [domain-knowledge, unity, ecs, capitalism-simulation, technical-guide]
related: [../architecture/technical-architecture_KOR.md, ../architecture/ecs-design_KOR.md]
parent: INDEX_KOR.md
created: 2025-09-13
updated: 2025-09-13
priority: critical
---

# 도메인 지식 참조서 - YouAreCapitalist

[🇺🇸 English Version](./DOMAIN_KNOWLEDGE.md)

## 📍 네비게이션

[↩️ 참조로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../../CLAUDE_KOR.md)

## 🚨 필독 사항

**⚠️ 코딩 작업 전 반드시 읽어주세요 ⚠️**

이 문서는 YouAreCapitalist 프로젝트의 코드 변경 작업 전에 반드시 이해해야 하는 핵심 도메인 지식을 포함합니다. 이 지침을 따르지 않으면 성능 저하나 아키텍처 불일치가 발생할 수 있습니다.

## 1. 프로젝트 개요

### 1.1 핵심 기술 스택
```yaml
게임 엔진: Unity 6000.2.0f1
아키텍처: Unity DOTS (Data-Oriented Technology Stack)
주요 프레임워크: ECS (Entity Component System)
성능: Job System + Burst Compiler
플랫폼: 모바일/PC 크로스 플랫폼
렌더링: Universal Render Pipeline (URP)
언어: C# (.NET Standard 2.1)
```

### 1.2 프로젝트 특성
- **시각적 게임이 아님**: 주로 데이터 처리 및 시각화
- **시뮬레이션 중심**: 100,000+ 경제 주체 처리
- **성능 중요**: 실시간 경제 계산
- **데이터 중심**: 그래픽보다 숫자, 차트, 통계가 핵심

## 2. 아키텍처 원칙

### 2.1 데이터 지향 설계 (DOD)
```csharp
// ✅ 올바름: ECS 컴포넌트 (순수 데이터)
public struct PopulationData : IComponentData
{
    public float income;
    public float consumptionRate;
    public EducationLevel education;
    public int age;
}

// ❌ 잘못됨: 시뮬레이션 데이터에 MonoBehaviour 사용
public class Population : MonoBehaviour
{
    public float income;  // 시뮬레이션에 MonoBehaviour 사용하지 말 것
}
```

### 2.2 3계층 아키텍처
```
┌─────────────────────────────────────────┐
│         UI 계층 (MonoBehaviour)         │  ← 차트, 대시보드, UI
│  - UGUI/UI Toolkit                      │
│  - 데이터 시각화                        │
└─────────────────────────────────────────┘
                    ↕️
┌─────────────────────────────────────────┐
│      브릿지 계층 (Event System)         │  ← 데이터 동기화
│  - ECS ↔ UI 통신                        │
└─────────────────────────────────────────┘
                    ↕️
┌─────────────────────────────────────────┐
│    ECS 계층 (순수 데이터 처리)          │  ← 게임 로직, 계산
│  - 경제 시뮬레이션                      │
│  - Job System + Burst                   │
└─────────────────────────────────────────┘
```

### 2.3 성능 우선 사고방식
- **목표**: 100,000+ 엔티티를 60fps에서 처리
- **ECS 사용**: 경제 계산, 시장 시뮬레이션, 인구 행동
- **MonoBehaviour 사용**: UI, 입력 처리, 시각 효과만
- **항상 고려**: 메모리 레이아웃, 캐시 친화성, 병렬 처리

## 3. ECS 구현 가이드라인

### 3.1 컴포넌트 설계 패턴

#### ✅ 순수 데이터 컴포넌트
```csharp
// 시장 참가자 데이터
public struct MarketParticipant : IComponentData
{
    public float netWorth;
    public float liquidCash;
    public Entity portfolio;  // 포트폴리오 엔티티 참조
}

// 회사 재무 데이터
public struct CompanyFinancials : IComponentData
{
    public float revenue;
    public float expenses;
    public float marketCap;
    public int employeeCount;
}
```

#### ✅ 그룹핑을 위한 공유 컴포넌트
```csharp
// 경제 계층별 엔티티 그룹화
public struct EconomicClass : ISharedComponentData
{
    public ClassType type;  // LowerClass, MiddleClass, UpperClass
}

// 산업별 회사 그룹화
public struct Industry : ISharedComponentData
{
    public IndustryType type;  // Technology, Finance, Manufacturing 등
}
```

#### ✅ 컬렉션을 위한 버퍼 컴포넌트
```csharp
// 주식 보유 현황 (동적 배열)
[InternalBufferCapacity(8)]
public struct StockHolding : IBufferElementData
{
    public Entity stockEntity;
    public int shares;
    public float averageCost;
}

// 거래 기록
[InternalBufferCapacity(16)]
public struct TransactionHistory : IBufferElementData
{
    public TransactionType type;
    public float amount;
    public DateTime timestamp;
}
```

### 3.2 시스템 설계 패턴

#### ✅ Job 기반 시스템
```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
public class PopulationConsumptionSystem : SystemBase
{
    protected override void OnUpdate()
    {
        // Burst 컴파일된 병렬 Job
        var job = new ConsumptionCalculationJob
        {
            deltaTime = Time.DeltaTime,
            economicData = GetComponentDataFromEntity<EconomicData>(true)
        };
        
        Dependency = job.ScheduleParallel(Dependency);
    }
}

[BurstCompile]
public struct ConsumptionCalculationJob : IJobEntityBatch
{
    [ReadOnly] public float deltaTime;
    [ReadOnly] public ComponentDataFromEntity<EconomicData> economicData;
    
    public void Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
    {
        // 고성능 벌크 처리
        var populations = chunk.GetNativeArray(populationHandle);
        // ... SIMD 최적화된 계산
    }
}
```

#### ✅ 시스템 업데이트 그룹
```csharp
// 실행 순서 정의
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateBefore(typeof(MarketSystemGroup))]
public class PopulationSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(PopulationSystemGroup))]
public class MarketSystemGroup : ComponentSystemGroup { }
```

### 3.3 데이터 관리 패턴

#### ✅ 성능을 위한 Native Collections
```csharp
public class MarketDataSystem : SystemBase
{
    private NativeHashMap<Entity, float> stockPrices;
    private NativeArray<float> marketIndices;
    
    protected override void OnCreate()
    {
        stockPrices = new NativeHashMap<Entity, float>(10000, Allocator.Persistent);
        marketIndices = new NativeArray<float>(100, Allocator.Persistent);
    }
    
    protected override void OnDestroy()
    {
        if (stockPrices.IsCreated) stockPrices.Dispose();
        if (marketIndices.IsCreated) marketIndices.Dispose();
    }
}
```

## 4. 게임 특화 도메인 로직

### 4.1 경제 시뮬레이션 핵심
```csharp
// 핵심 경제 엔티티
public enum EntityTypes
{
    Population,     // 개별 경제 행위자 (Pop)
    Company,        // 기업 엔티티
    Stock,          // 거래 가능한 증권
    Market,         // 시장 세그먼트
    Government,     // 정책 결정자
    Bank           // 금융 기관
}

// 시뮬레이션 시간 스케일
public enum TimeScale
{
    Paused = 0,
    Normal = 1,      // 1x 실시간
    Fast = 10,       // 10x 가속
    VeryFast = 100,  // 100x 가속
    Ultra = 1000     // 1000x 초고속
}
```

### 4.2 시장 메커닉
```csharp
// 주식 시장 시뮬레이션
public struct StockData : IComponentData
{
    public float currentPrice;
    public float previousPrice;
    public float marketCap;
    public int totalShares;
    public float dividendYield;
    public float peRatio;
}

// 시장 이벤트
public struct MarketEvent : IComponentData
{
    public EventType type;    // 실적, 합병, 스캔들 등
    public float impact;      // 가격 영향 배수
    public DateTime expiry;   // 이벤트 만료 시점
}
```

### 4.3 자동화 시스템
```csharp
// 플레이어 자동화 수준
public enum AutomationLevel
{
    Manual = 0,        // 완전 플레이어 통제
    Assisted = 1,      // AI 추천
    SemiAuto = 2,      // AI가 승인 후 실행
    FullAuto = 3       // 완전 AI 통제
}

// AI 의사결정
public struct AIDecision : IComponentData
{
    public DecisionType type;
    public float confidence;
    public Entity targetEntity;
    public bool requiresApproval;
}
```

## 5. 성능 최적화 가이드라인

### 5.1 엔티티 관리
```csharp
// ✅ 성능을 위한 엔티티 풀링
public class EntityPool : SystemBase
{
    private NativeQueue<Entity> pooledPopulation;
    private NativeQueue<Entity> pooledCompanies;
    
    public Entity GetPooledPopulation()
    {
        if (pooledPopulation.Count > 0)
            return pooledPopulation.Dequeue();
        
        return EntityManager.CreateEntity(populationArchetype);
    }
}
```

### 5.2 LOD (Level of Detail) 시스템
```csharp
// 동적 품질 스케일링
public enum SimulationLOD
{
    Ultra,    // 개별 엔티티 시뮬레이션
    High,     // 중요 엔티티는 개별, 나머지는 그룹
    Medium,   // 대부분 엔티티 그룹화
    Low       // 통계적 근사치
}

// 성능 기반 LOD 조정
public class PerformanceManager : SystemBase
{
    private float targetFrameTime = 16.67f; // 60fps
    
    protected override void OnUpdate()
    {
        if (Time.unscaledDeltaTime > targetFrameTime * 1.2f)
            ReduceLOD();
        else if (Time.unscaledDeltaTime < targetFrameTime * 0.8f)
            IncreaseLOD();
    }
}
```

### 5.3 메모리 관리
```csharp
// 캐시 효율성을 위한 청크 기반 처리
[BurstCompile]
public struct OptimizedMarketJob : IJobEntityBatch
{
    public void Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
    {
        // 메모리 지역성을 위한 전체 청크 처리
        var prices = chunk.GetNativeArray(priceHandle);
        var volumes = chunk.GetNativeArray(volumeHandle);
        
        // SIMD를 위한 벡터화된 연산
        for (int i = 0; i < chunk.Count; i++)
        {
            // 벌크 계산
        }
    }
}
```

## 6. UI 통합 패턴

### 6.1 ECS-UI 브릿지
```csharp
// 이벤트 기반 통신
public class MarketDataBridge : MonoBehaviour
{
    public event System.Action<float[]> OnStockPricesUpdated;
    
    private EntityQuery stockQuery;
    
    void Start()
    {
        var world = World.DefaultGameObjectInjectionWorld;
        stockQuery = world.EntityManager.CreateEntityQuery(typeof(StockData));
    }
    
    void Update()
    {
        // ECS 데이터를 폴링하고 UI에 브로드캐스트
        var stockData = stockQuery.ToComponentDataArray<StockData>(Allocator.TempJob);
        var prices = ExtractPrices(stockData);
        OnStockPricesUpdated?.Invoke(prices);
        stockData.Dispose();
    }
}
```

### 6.2 데이터 시각화
```csharp
// 차트 데이터 준비
public class EconomicChartController : MonoBehaviour
{
    [SerializeField] private LineChart gdpChart;
    [SerializeField] private BarChart sectorChart;
    
    private void UpdateGDPChart(float[] gdpData)
    {
        // ECS 데이터를 차트 형식으로 변환
        var chartData = new List<Vector2>();
        for (int i = 0; i < gdpData.Length; i++)
        {
            chartData.Add(new Vector2(i, gdpData[i]));
        }
        gdpChart.UpdateData(chartData);
    }
}
```

## 7. 일반적인 함정과 안티패턴

### 7.1 ❌ 하지 말아야 할 것
```csharp
// ❌ 시뮬레이션 데이터에 MonoBehaviour 사용하지 말 것
public class PopulationMonoBehaviour : MonoBehaviour
{
    public float income; // 이것은 ECS 성능을 망침
}

// ❌ Update 루프에서 ECS에 접근하지 말 것
public class BadUIController : MonoBehaviour
{
    void Update()
    {
        // 매 프레임마다 이것은 비쌈!
        var entities = World.DefaultGameObjectInjectionWorld.EntityManager
                           .GetAllEntities();
    }
}

// ❌ 성능 데이터에 Managed 컴포넌트 사용하지 말 것
public class ManagedData : IComponentData
{
    public List<float> expensiveList; // 관리형 메모리!
}
```

### 7.2 ✅ 올바른 대안
```csharp
// ✅ 시뮬레이션에 ECS 컴포넌트 사용
public struct PopulationECS : IComponentData
{
    public float income;
    public float consumption;
}

// ✅ UI 쿼리를 캐시하고 주기적으로 업데이트
public class GoodUIController : MonoBehaviour
{
    private float updateInterval = 0.1f; // 10fps UI 업데이트
    private float lastUpdate;
    
    void Update()
    {
        if (Time.time - lastUpdate >= updateInterval)
        {
            UpdateUI();
            lastUpdate = Time.time;
        }
    }
}

// ✅ 성능을 위해 NativeCollections 사용
public struct OptimizedData : IComponentData
{
    public BlobAssetReference<BlobArray<float>> efficientArray;
}
```

## 8. 개발 워크플로우

### 8.1 작업 시작 전
1. **이 문서를 완전히 읽기**
2. **관련 아키텍처 문서 검토**
3. **프로젝트의 기존 ECS 패턴 확인**
4. **성능 영향 이해**
5. **ECS vs MonoBehaviour 분리 계획**

### 8.2 코드 리뷰 체크리스트
- [ ] 시뮬레이션 데이터에 ECS 사용?
- [ ] 3계층 아키텍처 준수?
- [ ] 적절한 곳에 Job System 구현?
- [ ] 성능을 위한 Burst 컴파일 사용?
- [ ] Native Collections 적절히 관리?
- [ ] UI와 시뮬레이션 로직 분리?
- [ ] 메모리 레이아웃과 캐시 효율성 고려?

### 8.3 테스트 접근법
- **단위 테스트**: 개별 시스템 로직
- **성능 테스트**: 프레임 시간과 메모리 사용량
- **스케일 테스트**: 100K+ 엔티티 시나리오
- **통합 테스트**: ECS-UI 통신

## 9. 주요 참조자료

### 9.1 필수 문서
- [기술 아키텍처](../architecture/technical-architecture_KOR.md) - 전체 시스템 설계
- [ECS 시스템 설계](../architecture/ecs-design_KOR.md) - ECS 구현 세부사항
- [시뮬레이션 시스템](../architecture/simulation-system_KOR.md) - 경제 시뮬레이션 로직

### 9.2 Unity DOTS 리소스
- [Unity DOTS 공식 문서](https://docs.unity3d.com/Packages/com.unity.entities@latest)
- [Job System 가이드](https://docs.unity3d.com/Manual/JobSystem.html)
- [Burst Compiler](https://docs.unity3d.com/Packages/com.unity.burst@latest)

---

## 🎯 기억하세요

**이것은 데이터 처리 게임이지, 그래픽 게임이 아닙니다. 모든 결정은 다음을 우선해야 합니다:**
1. 시각적 품질보다 **데이터 처리량**
2. 그래픽 효과보다 **시뮬레이션 정확성**  
3. 기능 복잡성보다 **성능 확장성**
4. 전통적 MonoBehaviour 접근법보다 **ECS 패턴**

**확실하지 않을 때는, 100,000+ 엔티티를 효율적으로 처리할 수 있는 솔루션을 선택하세요.**