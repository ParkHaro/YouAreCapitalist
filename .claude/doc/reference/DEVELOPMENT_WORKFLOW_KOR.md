---
category: reference
tags: [workflow, guidelines, development, best-practices, mandatory]
related: [DOMAIN_KNOWLEDGE_KOR.md]
parent: INDEX_KOR.md
created: 2025-09-13
updated: 2025-09-13
priority: critical
---

# 개발 워크플로우 가이드라인

[🇺🇸 English Version](./DEVELOPMENT_WORKFLOW.md)

## 📍 네비게이션

[↩️ 참조로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../../CLAUDE_KOR.md)

## 🚨 필수 워크플로우

**코드 변경을 포함한 모든 개발 작업에서 이 워크플로우를 반드시 따라야 합니다.**

## 1. 개발 전 단계

### 1.1 필수 읽기 (의무사항)
**모든 코딩 작업 전에 반드시:**

```yaml
1단계: 도메인 지식 읽기
  파일: .claude/doc/reference/DOMAIN_KNOWLEDGE_KOR.md
  목적: Unity ECS 아키텍처와 프로젝트 제약사항 이해
  시간: 10-15분
  중요사항: 성능과 아키텍처 원칙

2단계: 관련 아키텍처 검토
  파일: 
    - .claude/doc/architecture/technical-architecture_KOR.md
    - .claude/doc/architecture/ecs-design_KOR.md
  목적: 시스템 통합 패턴 이해
  시간: 문서당 5-10분

3단계: 게임 디자인 컨텍스트 확인
  파일: 
    - .claude/doc/gamedesign/core-gameplay-loop_KOR.md
    - 관련 게임플레이 메커닉 문서들
  목적: 비즈니스 로직과 게임 규칙 이해
  시간: 작업 범위에 따라 가변
```

### 1.2 작업 분석 프레임워크
```python
# 코딩 전 이 사고 프레임워크 사용:
def analyze_task(task_description):
    analysis = {
        'data_scale': '얼마나 많은 엔티티가 영향을 받을까?',
        'performance_critical': '이것이 핫패스에 있는가?',
        'ecs_vs_mono': '이것이 ECS나 MonoBehaviour를 사용해야 하는가?',
        'ui_integration': 'UI 통신이 필요한가?',
        'automation_impact': '게임 자동화에 어떤 영향을 주는가?'
    }
    
    # 결정 매트릭스:
    if analysis['data_scale'] > 1000:
        use_ecs = True
        use_job_system = True
        use_burst = True
    
    if analysis['performance_critical']:
        optimize_for_cache = True
        use_native_collections = True
    
    return analysis
```

## 2. 개발 표준

### 2.1 코드 구조 규칙

#### ✅ ECS 코드 구조
```csharp
// 파일: Assets/Scripts/ECS/Systems/Economic/PopulationConsumptionSystem.cs
[UpdateInGroup(typeof(EconomicSimulationGroup))]
public class PopulationConsumptionSystem : SystemBase
{
    protected override void OnUpdate()
    {
        // >1000 엔티티에는 Job 기반 구현 필수
        var job = new ConsumptionJob { /* ... */ };
        Dependency = job.ScheduleParallel(Dependency);
    }
}

// 파일: Assets/Scripts/ECS/Jobs/PopulationJobs.cs
[BurstCompile]
public struct ConsumptionJob : IJobEntityBatch
{
    // 성능을 위한 Burst 컴파일
}

// 파일: Assets/Scripts/ECS/Components/Economic/PopulationData.cs
public struct PopulationData : IComponentData
{
    // 순수 데이터만 - 메서드 없음
}
```

#### ✅ UI 코드 구조
```csharp
// 파일: Assets/Scripts/UI/Controllers/MarketChartController.cs
public class MarketChartController : MonoBehaviour
{
    // UI 로직만 - 시뮬레이션 데이터 처리 없음
    private void UpdateChart(float[] marketData)
    {
        // 시각화 로직
    }
}

// 파일: Assets/Scripts/UI/Bridges/MarketDataBridge.cs
public class MarketDataBridge : MonoBehaviour
{
    // ECS ↔ UI 통신
    private EntityQuery marketQuery;
    public event Action<MarketData> OnMarketDataUpdated;
}
```

### 2.2 성능 요구사항

#### 필수 성능 검사
```csharp
// 모든 ECS 시스템에 성능 검증 포함:
public class YourEconomicSystem : SystemBase
{
    protected override void OnUpdate()
    {
        #if UNITY_EDITOR
        using var marker = new ProfilerMarker("YourSystem.Update").Auto();
        #endif
        
        // 구현 내용
        var job = new YourJob();
        Dependency = job.ScheduleParallel(Dependency);
        
        #if UNITY_EDITOR
        // 엔티티 수가 목표를 초과하지 않는지 검증
        var entityCount = m_EntityQuery.CalculateEntityCount();
        if (entityCount > 10000)
        {
            Debug.LogWarning($"High entity count in {nameof(YourEconomicSystem)}: {entityCount}");
        }
        #endif
    }
}
```

#### 메모리 관리 체크리스트
```csharp
public class EconomicDataSystem : SystemBase
{
    private NativeHashMap<Entity, float> dataMap;
    
    protected override void OnCreate()
    {
        // ✅ 알려진 크기에 대해 항상 용량 지정
        dataMap = new NativeHashMap<Entity, float>(10000, Allocator.Persistent);
    }
    
    protected override void OnDestroy()
    {
        // ✅ 필수: 모든 네이티브 컬렉션 해제
        if (dataMap.IsCreated) 
            dataMap.Dispose();
    }
    
    protected override void OnUpdate()
    {
        // ✅ 임시 데이터에 TempJob 할당자 사용
        var tempArray = new NativeArray<float>(100, Allocator.TempJob);
        
        // 데이터 처리...
        
        // ✅ 임시 할당 해제
        tempArray.Dispose();
    }
}
```

## 3. 코드 리뷰 과정

### 3.1 자체 리뷰 체크리스트
코드 제출 전 확인사항:

#### ECS 구현
- [ ] **순수 데이터 컴포넌트** 사용 (IComponentData에 메서드 없음)
- [ ] **Job System 통합** (>1000 엔티티)
- [ ] **Burst 컴파일** (성능 중요 경로)
- [ ] **적절한 시스템 그룹 속성** ([UpdateInGroup])
- [ ] **네이티브 컬렉션 해제** (OnDestroy에서)
- [ ] **관리형 참조 없음** (컴포넌트에서)
- [ ] **청크 기반 처리** (해당되는 경우)

#### 성능 검증
- [ ] **프로파일러 마커** 추가 (타이밍용)
- [ ] **엔티티 수 경고** (스케일 검증용)
- [ ] **메모리 할당** 패턴 검토
- [ ] **캐시 친화적** 데이터 접근 패턴
- [ ] **Update() 루프 없음** (ECS 데이터 접근용)

#### 아키텍처 준수
- [ ] **3계층 분리** 유지 (ECS/Bridge/UI)
- [ ] **이벤트 기반 UI 통신** (UI에서 직접 ECS 접근 없음)
- [ ] **ScriptableObject 설정** (게임 데이터용)
- [ ] **일관된 명명 규칙** (EconomicSystem, PopulationJob 등)

### 3.2 아키텍처 검증
```csharp
// 아키텍처 준수 검증에 이 패턴 사용:

// ❌ 잘못됨: UI가 직접 ECS 접근
public class BadUIController : MonoBehaviour
{
    void Update()
    {
        var world = World.DefaultGameObjectInjectionWorld;
        var entities = world.EntityManager.GetAllEntities(); // 절대 하지 말 것
    }
}

// ✅ 올바름: 이벤트 기반 브릿지 패턴
public class EconomicUIController : MonoBehaviour
{
    [SerializeField] private MarketDataBridge dataBridge;
    
    void Start()
    {
        dataBridge.OnMarketDataUpdated += UpdateMarketUI;
    }
    
    private void UpdateMarketUI(MarketData data)
    {
        // UI 업데이트 로직만
    }
}
```

## 4. 테스트 요구사항

### 4.1 필수 테스트

#### 성능 테스트
```csharp
// >1000 엔티티를 처리하는 모든 ECS 시스템에 필요
[Test]
public void PopulationSystem_HandlesLargeScale_WithinFrameTarget()
{
    // 준비: 100,000 인구 엔티티 생성
    var entities = CreatePopulationEntities(100000);
    
    // 실행: 시스템 업데이트 실행
    var stopwatch = Stopwatch.StartNew();
    World.GetOrCreateSystem<PopulationConsumptionSystem>().Update();
    stopwatch.Stop();
    
    // 검증: 16ms(60fps 목표) 내에 완료되어야 함
    Assert.That(stopwatch.ElapsedMilliseconds, Is.LessThan(16));
}
```

#### 메모리 테스트
```csharp
[Test]
public void EconomicSystem_DoesNotLeakMemory_AfterManyUpdates()
{
    // 이전 메모리 측정
    var initialMemory = GC.GetTotalMemory(true);
    
    // 많은 업데이트 실행
    for (int i = 0; i < 1000; i++)
    {
        system.Update();
    }
    
    // 강제 정리 및 측정
    GC.Collect();
    var finalMemory = GC.GetTotalMemory(true);
    
    // 상당한 메모리 증가가 없어야 함
    var memoryGrowth = finalMemory - initialMemory;
    Assert.That(memoryGrowth, Is.LessThan(1024 * 1024)); // <1MB 증가
}
```

### 4.2 통합 테스트
```csharp
// ECS-UI 브릿지 통신 테스트
[Test]
public void MarketDataBridge_UpdatesUI_WhenMarketChanges()
{
    // 준비
    var bridge = CreateMarketDataBridge();
    var uiUpdated = false;
    bridge.OnMarketDataUpdated += _ => uiUpdated = true;
    
    // 실행: ECS에서 시장 데이터 변경 시뮬레이션
    CreateMarketEntity(initialPrice: 100f);
    UpdateMarketPrice(newPrice: 150f);
    bridge.UpdateFromECS(); // 브릿지 업데이트 트리거
    
    // 검증
    Assert.IsTrue(uiUpdated, "UI should be notified of market changes");
}
```

## 5. 성능 모니터링

### 5.1 지속적인 성능 검증
```csharp
// 모든 경제 시스템에 추가:
public class MarketSimulationSystem : SystemBase
{
    private static readonly ProfilerMarker s_UpdateMarker = 
        new ProfilerMarker("MarketSimulation.Update");
    
    private MovingAverage frameTimeAverage = new MovingAverage(60);
    
    protected override void OnUpdate()
    {
        using (s_UpdateMarker.Auto())
        {
            var startTime = Time.realtimeSinceStartup;
            
            // 시스템 로직
            var job = new MarketCalculationJob();
            Dependency = job.ScheduleParallel(Dependency);
            
            // 성능 추적
            var frameTime = Time.realtimeSinceStartup - startTime;
            frameTimeAverage.Add(frameTime * 1000f); // ms로 변환
            
            #if UNITY_EDITOR
            // 성능 저하시 경고
            if (frameTimeAverage.Average > 5.0f) // 5ms 경고 임계값
            {
                Debug.LogWarning($"{GetType().Name} average frame time: {frameTimeAverage.Average:F2}ms");
            }
            #endif
        }
    }
}
```

### 5.2 자동화된 성능 경고
```csharp
// 성능 중요 시스템에 포함:
public static class PerformanceValidator
{
    private static readonly Dictionary<Type, float> SystemThresholds = new()
    {
        { typeof(PopulationBehaviorSystem), 8.0f },    // 8ms 최대
        { typeof(MarketSimulationSystem), 5.0f },      // 5ms 최대
        { typeof(CompanyOperationsSystem), 6.0f }      // 6ms 최대
    };
    
    public static void ValidateSystemPerformance(Type systemType, float frameTimeMs)
    {
        if (SystemThresholds.TryGetValue(systemType, out float threshold))
        {
            if (frameTimeMs > threshold)
            {
                Debug.LogError($"PERFORMANCE VIOLATION: {systemType.Name} took {frameTimeMs:F2}ms (threshold: {threshold}ms)");
                
                #if UNITY_EDITOR
                // 조사를 위해 에디터에서 일시정지
                UnityEditor.EditorApplication.isPaused = true;
                #endif
            }
        }
    }
}
```

## 6. 문서화 요구사항

### 6.1 코드 문서화 표준
```csharp
/// <summary>
/// 소득과 경제 조건을 바탕으로 인구 엔티티의 소비 패턴을 계산합니다.
/// Job System + Burst를 사용하여 프레임당 최대 100,000 엔티티를 처리합니다.
/// </summary>
/// <remarks>
/// 성능: 60fps에서 50,000 엔티티에 대해 8ms 프레임 시간 목표.
/// 메모리: 청크 처리를 위해 2MB 네이티브 배열 사용.
/// 종속성: EconomicData와 PopulationClass 컴포넌트 필요.
/// </remarks>
[UpdateInGroup(typeof(EconomicSimulationGroup))]
[UpdateAfter(typeof(IncomeCalculationSystem))]
public class PopulationConsumptionSystem : SystemBase
{
    /// <summary>
    /// 병렬 소비 계산을 위한 Job 구조체.
    /// SIMD 최적화를 위해 Burst 컴파일됨.
    /// </summary>
    [BurstCompile]
    public struct ConsumptionJob : IJobEntityBatch
    {
        // 구현...
    }
}
```

### 6.2 성능 문서화
```csharp
// 시스템 주석에 성능 특성 포함:
/*
 * 성능 프로필:
 * - 엔티티 규모: 10,000 - 100,000 엔티티
 * - 목표 프레임 시간: 8ms (60fps)
 * - 메모리 사용량: ~2MB 네이티브 배열
 * - 병렬화: 8방향 병렬 Job 실행
 * - 캐시 효율성: 데이터 지역성을 위한 청크 기반 처리
 * - Burst 최적화: 완전 SIMD 벡터화
 * 
 * 스케일링 동작:
 * - 엔티티 수와 선형적 스케일링
 * - 메모리 사용량: 엔티티당 20바이트
 * - CPU 스케일링: 사용 가능한 모든 코어 활용
 * 
 * 종속성:
 * - 다음 이후 실행: IncomeCalculationSystem
 * - 다음 이전 실행: MarketDemandSystem
 * - 필수 컴포넌트: PopulationData, EconomicClass
 */
```

## 7. 응급 절차

### 7.1 성능 회귀 대응
```yaml
프레임율이 30fps 아래로 떨어지는 경우:
  1. Unity Profiler 즉시 확인
  2. 병목 시스템 식별
  3. 일시적으로 엔티티 수 50% 감소
  4. LOD 시스템 폴백 활성화
  5. 프로파일러 데이터와 함께 성능 회귀 보고

메모리 사용량이 1.5GB를 초과하는 경우:
  1. 네이티브 컬렉션 누수 확인
  2. 가비지 컬렉션 강제 실행
  3. 메모리 프로파일링 활성화
  4. 할당 소스 식별
  5. 즉시 정리 구현
```

### 7.2 빌드 실패 프로토콜
```yaml
ECS 오류로 빌드가 실패하는 경우:
  1. 누락된 [BurstCompile] 속성 확인
  2. 모든 네이티브 컬렉션이 해제되었는지 확인
  3. 시스템 업데이트 그룹 종속성 검증
  4. IComponentData의 관리형 참조 확인
  5. Job 종속성과 안전 시스템 검토
```

---

## 🎯 성공 기준

**구현이 준비된 상태:**
- ✅ **모든 성능 테스트 통과** (엔티티 규모 + 프레임 시간)
- ✅ **메모리 누수 없음** (프로파일러에서 감지)
- ✅ **아키텍처 준수 검증** (3계층 분리)
- ✅ **문서화 완료** (성능 특성 기록)
- ✅ **통합 테스트 통과** (ECS-UI 통신 작동)

**기억하세요: 이것은 데이터 처리 게임입니다. 모든 코드 라인은 100,000+ 엔티티를 효율적으로 처리하도록 최적화되어야 합니다.**