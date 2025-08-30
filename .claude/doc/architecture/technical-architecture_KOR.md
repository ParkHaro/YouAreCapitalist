# 자본주의 시뮬레이션 게임 - 기술 아키텍처 문서

[🇬🇧 English Version](./technical-architecture.md)

## 📍 네비게이션

[↩️ 아키텍처 문서로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 시스템 개요

### 1.1 아키텍처 철학

#### 데이터 중심 설계 (Data-Oriented Design)
- **핵심 원칙**: 렌더링보다 데이터 처리에 집중
- **게임 특성**: 시각적 오브젝트가 아닌 숫자, 차트, 통계 데이터가 핵심
- **성능 목표**: 수십만 개의 경제 주체 실시간 시뮬레이션

#### 3-Layer 아키텍처
```
┌─────────────────────────────────────────┐
│         UI Layer (MonoBehaviour)        │  ← 데이터 시각화, 사용자 상호작용
│  - UGUI/UI Toolkit                      │
│  - 차트, 그래프, 대시보드               │
│  - 이벤트 처리                          │
└─────────────────────────────────────────┘
                    ↕️ 이벤트 & 데이터
┌─────────────────────────────────────────┐
│      Bridge Layer (Event System)        │  ← 데이터 동기화, 통신 계층
│  - ECS ↔ UI 데이터 변환                 │
│  - 이벤트 브로드캐스팅                  │
│  - 상태 관리                            │
└─────────────────────────────────────────┘
                    ↕️ 데이터 스트림
┌─────────────────────────────────────────┐
│    ECS Layer (순수 데이터 처리)         │  ← 게임 로직, 계산 엔진
│  - 경제 시뮬레이션                      │
│  - Job System 병렬 처리                 │
│  - Burst Compiler 최적화                │
└─────────────────────────────────────────┘
```

### 1.2 기술 스택

#### 핵심 기술
```yaml
Data Processing:
  - Unity DOTS (Data-Oriented Technology Stack)
  - ECS (Entity Component System)
  - Job System + Burst Compiler
  - Native Collections (NativeArray, NativeHashMap)

UI & Visualization:
  - UI Toolkit (모던 UI)
  - UGUI (레거시 지원)
  - XCharts/Chart.js (데이터 시각화)
  - TextMeshPro (고품질 텍스트)

Data Management:
  - ScriptableObject (게임 설정)
  - JSON (세이브/로드)
  - SQLite (히스토리 데이터)
  - Binary Serialization (성능 최적화)

Platform:
  - Unity 6000.2.0f1+
  - .NET Standard 2.1
  - Universal Render Pipeline (URP)
  - Mobile/PC Cross-platform
```

### 1.3 성능 목표 및 제약사항

#### 성능 목표
```yaml
Simulation Scale:
  - 경제 주체 수: 100,000+ 개체
  - 시뮬레이션 속도: 1x~1000x 가변
  - 프레임레이트: 60fps (1x), 30fps (100x+)
  - 메모리 사용량: < 2GB (모바일 호환)

Processing Performance:
  - Pop 시뮬레이션: 50,000/frame @60fps
  - 시장 계산: 실시간 가격 형성
  - 통계 집계: < 1ms/frame
  - UI 업데이트: < 16ms/frame
```

#### 설계 제약사항
```yaml
Hardware Constraints:
  - 최소 사양: 4GB RAM, Quad-core CPU
  - 모바일 지원: Android API 24+, iOS 12+
  - 배터리 최적화: < 500mA 전력 소비

Software Constraints:
  - Unity 6000.2.0f1 호환성
  - .NET Standard 2.1 제한
  - URP 17.2.0 기반 렌더링
```

## 2. 데이터 처리 파이프라인

### 2.1 시뮬레이션 루프 설계

#### 게임 시간 관리
```csharp
// 시뮬레이션 시간 관리
public class SimulationTimeManager : SystemBase
{
    public enum TimeScale
    {
        Paused = 0,
        Normal = 1,      // 1x 실시간
        Fast = 10,       // 10x 가속
        VeryFast = 100,  // 100x 가속
        Ultra = 1000     // 1000x 초고속
    }
    
    private float gameTimePerSecond;
    private DateTime currentGameDate;
    private TimeScale currentScale;
}
```

#### 시뮬레이션 실행 순서
```
1. Input Processing (사용자 입력)
   ↓
2. Economic Simulation (경제 시뮬레이션)
   ├── Population Behavior (인구 행동)
   ├── Company Operations (기업 운영) 
   ├── Market Dynamics (시장 역학)
   └── Government Policy (정부 정책)
   ↓
3. Statistics Calculation (통계 계산)
   ├── Aggregate Statistics (집계 통계)
   ├── Market Indices (시장 지수)
   └── Economic Indicators (경제 지표)
   ↓
4. Event Processing (이벤트 처리)
   ├── Random Events (랜덤 이벤트)
   ├── Policy Changes (정책 변화)
   └── Market Shocks (시장 충격)
   ↓
5. UI Update (UI 업데이트)
```

### 2.2 병렬 처리 전략

#### Job System 활용
```csharp
// 인구 행동 병렬 처리
[BurstCompile]
public struct PopulationBehaviorJob : IJobEntityBatch
{
    [ReadOnly] public float deltaTime;
    [ReadOnly] public ComponentTypeHandle<PopulationData> populationHandle;
    public ComponentTypeHandle<EconomicActivity> activityHandle;
    
    public void Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
    {
        // 수만 개 Pop의 경제 활동을 병렬로 계산
        var populations = chunk.GetNativeArray(populationHandle);
        var activities = chunk.GetNativeArray(activityHandle);
        
        for (int i = 0; i < populations.Length; i++)
        {
            // SIMD 최적화된 경제 계산
            CalculateConsumption(ref activities.ElementAt(i), populations[i]);
        }
    }
}
```

#### 시스템 그룹 최적화
```csharp
// 시뮬레이션 시스템 그룹
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(PopulationSystemGroup))]
public class MarketSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(MarketSystemGroup))]
public class StockMarketSystem : SystemBase { }

[UpdateInGroup(typeof(MarketSystemGroup))]
[UpdateAfter(typeof(StockMarketSystem))]
public class CommodityMarketSystem : SystemBase { }
```

### 2.3 캐싱 및 최적화

#### 다단계 캐싱 전략
```csharp
public class EconomicDataCache : SystemBase
{
    // Level 1: 프레임 캐시 (매 프레임 갱신)
    private NativeArray<float> frameGDPCache;
    
    // Level 2: 주기적 캐시 (초당 갱신)
    private Dictionary<string, float> periodicCache;
    
    // Level 3: 장기 캐시 (분당 갱신)
    private SQLiteDataCache longTermCache;
    
    protected override void OnUpdate()
    {
        // 캐시 레벨에 따른 선택적 업데이트
        if (Time.frameCount % 60 == 0) // 1초마다
        {
            UpdatePeriodicCache();
        }
        
        if (Time.frameCount % 3600 == 0) // 1분마다
        {
            UpdateLongTermCache();
        }
    }
}
```

#### LOD (Level of Detail) 시스템
```csharp
// 시뮬레이션 세밀도 조절
public enum SimulationLOD
{
    Ultra,    // 모든 개체 개별 시뮬레이션
    High,     // 중요한 개체만 개별, 나머지 그룹핑
    Medium,   // 대부분 그룹 단위 처리
    Low       // 통계적 근사치 사용
}

[BurstCompile]
public struct LODPopulationJob : IJob
{
    public SimulationLOD currentLOD;
    public NativeArray<PopulationData> populations;
    
    public void Execute()
    {
        switch (currentLOD)
        {
            case SimulationLOD.Ultra:
                ProcessIndividualBehavior();
                break;
            case SimulationLOD.High:
                ProcessGroupedBehavior();
                break;
            // ...
        }
    }
}
```

## 3. 확장성 고려사항

### 3.1 모듈식 시스템 설계

#### 플러그인 아키텍처
```csharp
// 확장 가능한 시스템 인터페이스
public interface IEconomicModule
{
    string ModuleName { get; }
    Version Version { get; }
    void Initialize(World world);
    void Update(float deltaTime);
    void Shutdown();
}

// 모듈 관리자
public class EconomicModuleManager : MonoBehaviour
{
    private List<IEconomicModule> loadedModules;
    
    public void LoadModule(IEconomicModule module)
    {
        module.Initialize(World.DefaultGameObjectInjectionWorld);
        loadedModules.Add(module);
    }
}
```

#### 설정 기반 시스템
```csharp
// ScriptableObject 기반 설정
[CreateAssetMenu(fileName = "EconomicSettings", menuName = "Game/Economic Settings")]
public class EconomicSettings : ScriptableObject
{
    [Header("Population Settings")]
    public int initialPopulation = 10000;
    public float baseConsumptionRate = 0.7f;
    
    [Header("Market Settings")]
    public float marketVolatility = 0.1f;
    public int numberOfCompanies = 1000;
    
    [Header("Performance Settings")]
    public SimulationLOD defaultLOD = SimulationLOD.High;
    public int maxEntitiesPerChunk = 128;
}
```

### 3.2 성능 스케일링 전략

#### 동적 LOD 조절
```csharp
public class PerformanceManager : SystemBase
{
    private float targetFrameTime = 16.67f; // 60fps
    private float currentFrameTime;
    private SimulationLOD currentLOD = SimulationLOD.High;
    
    protected override void OnUpdate()
    {
        currentFrameTime = Time.unscaledDeltaTime * 1000f;
        
        // 성능에 따른 동적 LOD 조절
        if (currentFrameTime > targetFrameTime * 1.2f)
        {
            ReduceLOD();
        }
        else if (currentFrameTime < targetFrameTime * 0.8f)
        {
            IncreaseLOD();
        }
    }
}
```

#### 메모리 풀링
```csharp
public class EntityPool : SystemBase
{
    private NativeQueue<Entity> pooledEntities;
    
    public Entity GetPooledEntity()
    {
        if (pooledEntities.Count > 0)
        {
            return pooledEntities.Dequeue();
        }
        
        return EntityManager.CreateEntity();
    }
    
    public void ReturnEntity(Entity entity)
    {
        // 컴포넌트 초기화 후 풀에 반환
        pooledEntities.Enqueue(entity);
    }
}
```

## 4. 개발 도구 및 디버깅

### 4.1 프로파일링 도구
```csharp
// 커스텀 프로파일러 마커
public static class EconomyProfiler
{
    public static readonly ProfilerMarker PopulationUpdate = 
        new ProfilerMarker("Economy.Population.Update");
    
    public static readonly ProfilerMarker MarketCalculation = 
        new ProfilerMarker("Economy.Market.Calculate");
}

// 사용 예시
using (EconomyProfiler.PopulationUpdate.Auto())
{
    // 인구 시뮬레이션 코드
}
```

### 4.2 실시간 디버깅 UI
```csharp
public class EconomyDebugUI : MonoBehaviour
{
    public bool showDebugInfo = false;
    
    void OnGUI()
    {
        if (!showDebugInfo) return;
        
        GUILayout.BeginArea(new Rect(10, 10, 300, 400));
        GUILayout.Label($"Active Entities: {GetEntityCount()}");
        GUILayout.Label($"Frame Time: {Time.deltaTime * 1000:F1}ms");
        GUILayout.Label($"Current LOD: {GetCurrentLOD()}");
        GUILayout.EndArea();
    }
}
```

## 5. 배포 및 운영

### 5.1 플랫폼별 최적화
```yaml
Mobile (Android/iOS):
  - Texture Compression: ASTC/ETC2
  - Audio Compression: Vorbis
  - Scripting Backend: IL2CPP
  - CPU Architecture: ARM64

Desktop (Windows/Mac/Linux):
  - Texture Compression: DXT/BC
  - Audio: Uncompressed
  - Scripting Backend: Mono/.NET
  - CPU Architecture: x64
```

### 5.2 데이터 관리
```csharp
// 세이브/로드 시스템
public class SaveSystem : MonoBehaviour
{
    public void SaveGame(string filename)
    {
        var saveData = new GameSaveData
        {
            gameDate = TimeManager.CurrentDate,
            playerData = GetPlayerData(),
            economicState = GetEconomicState(),
            // 압축된 엔티티 데이터
            compressedEntities = CompressEntityData()
        };
        
        File.WriteAllText(filename, JsonUtility.ToJson(saveData));
    }
}
```

---

## 다음 문서
- [ECS 시스템 설계](./ecs-design_KOR.md)
- [데이터 모델 명세](./data-model_KOR.md) 
- [UI 시스템 설계](./ui-system_KOR.md)
- [시스템 통합 가이드](./integration-guide_KOR.md)