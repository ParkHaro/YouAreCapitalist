# 시뮬레이션 시스템 아키텍처

[🇬🇧 English Version](./simulation-system.md)

## 📍 네비게이션

[↩️ 아키텍처 문서로 돌아가기](./INDEX_KOR.md) | [📚 문서 인덱스](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 시뮬레이션 개요

### 1.1 핵심 철학

#### 자율 운영 경제 생태계
- **자율적 엔티티**: 인구와 회사가 독립적으로 운영
- **창발적 행동**: 단순한 규칙에서 복잡한 경제 패턴이 출현
- **실시간 역학**: 플레이어 개입 없이 지속적 시뮬레이션
- **확장 가능한 아키텍처**: 수천 개의 엔티티를 동시에 지원

#### 설계 원칙
```csharp
// 예시: 인구의 자율적 의사결정
public struct PopulationDecisionComponent : IComponentData
{
    public DecisionType pendingDecision;    // 하려는 행동
    public float decisionConfidence;        // 확신 정도
    public float decisionDeadline;          // 결정해야 하는 시간
    public Entity targetEntity;             // 대상 엔티티
}
```

### 1.2 시뮬레이션 범위

#### 경제 엔티티
- **인구(Pops)**: 1,000-10,000개의 개별 경제 행위자
- **회사들**: 100-1,000개의 사업체 엔티티
- **시장들**: 부문별 경제 공간
- **정부**: 정책 결정 및 규제 엔티티

#### 시간 척도
- **게임 시간**: 1일 = 10초 (조정 가능)
- **경제 주기**: 월간/분기/연간 이벤트
- **업데이트 빈도**: 60 FPS 시뮬레이션, 1 FPS 경제 결정

## 2. 시스템 아키텍처

### 2.1 ECS 시스템 계층 구조

#### 핵심 시뮬레이션 시스템들
```
SimulationSystemGroup (FixedStepSimulationSystemGroup)
├── 초기화 단계
│   ├── EntitySpawningSystemGroup
│   │   ├── PopulationSpawnSystem (인구 생성)
│   │   ├── CompanySpawnSystem (회사 생성)
│   │   └── MarketInitializationSystem (시장 초기화)
│   └── ConfigurationSystemGroup (설정)
├── 경제 시뮬레이션 단계  
│   ├── PopulationSystemGroup (인구 시스템군)
│   │   ├── PopulationBehaviorSystem (인구 행동)
│   │   ├── ConsumptionDecisionSystem (소비 결정)
│   │   ├── EmploymentSeekingSystem (구직)
│   │   └── InvestmentDecisionSystem (투자 결정)
│   ├── CompanySystemGroup (회사 시스템군)
│   │   ├── CompanyOperationSystem (회사 운영)
│   │   ├── HiringDecisionSystem (채용 결정)
│   │   ├── ProductionPlanningSystem (생산 계획)
│   │   └── PricingStrategySystem (가격 전략)
│   ├── MarketSystemGroup (시장 시스템군)
│   │   ├── SupplyDemandSystem (공급수요)
│   │   ├── PriceDiscoverySystem (가격 발견)
│   │   ├── TradingExecutionSystem (거래 실행)
│   │   └── MarketClearingSystem (시장 청산)
│   └── InteractionSystemGroup (상호작용군)
│       ├── EmploymentMatchingSystem (고용 매칭)
│       ├── ConsumerCompanyTransactionSystem (소비-회사 거래)
│       └── B2BTransactionSystem (기업간 거래)
├── 통계 단계
│   ├── DataAggregationSystemGroup (데이터 집계군)
│   │   ├── PopulationStatisticsSystem (인구 통계)
│   │   ├── CompanyStatisticsSystem (회사 통계)
│   │   └── MarketStatisticsSystem (시장 통계)
│   └── HistoryTrackingSystem (이력 추적)
└── 이벤트 시스템군
    ├── RandomEventGenerationSystem (랜덤 이벤트 생성)
    ├── CyclicalEventSystem (주기적 이벤트)
    └── CrisisSimulationSystem (위기 시뮬레이션)
```

### 2.2 시스템 실행 순서

#### 고정 업데이트 루프 (60 FPS)
1. **엔티티 상태 업데이트**: 건강 체크, 노화, 기본 상태 전환
2. **시장 가격 업데이트**: 실시간 가격 변동
3. **통계 수집**: 실시간 데이터 집계

#### 경제 결정 루프 (1-5 FPS)
1. **결정 평가**: 엔티티들이 선택지를 평가
2. **행동 계획**: 의도된 행동을 대기열에 추가
3. **충돌 해결**: 경쟁하는 요구사항 처리
4. **행동 실행**: 계획된 행동 실행
5. **상태 전파**: 영향받는 엔티티들 업데이트

#### 이벤트 루프 (가변)
1. **예정된 이벤트**: 시간 기반 이벤트 실행
2. **랜덤 이벤트**: 랜덤 이벤트 생성 및 처리
3. **위기 감지**: 경제 위기 상황 모니터링

### 2.3 데이터 흐름 아키텍처

#### 정보 흐름
```
[엔티티 내부 상태] 
    ↓ (읽기)
[결정 시스템들] 
    ↓ (계획)
[행동 대기열 시스템들] 
    ↓ (실행)
[시장/거래 시스템들] 
    ↓ (업데이트)
[통계 시스템들] 
    ↓ (집계)
[UI 브리지 레이어] 
    ↓ (표시)
[플레이어 인터페이스]
```

## 3. 자율 행동 시스템

### 3.1 인구 행동 시스템

#### 의사결정 프레임워크
```csharp
public struct PopulationDecisionSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // 1. 현재 필요와 욕구 평가
        foreach (var (population, economic, decision) in 
                 SystemAPI.Query<PopulationComponent, EconomicStatusComponent, PopulationDecisionComponent>())
        {
            // 2. 성격과 상황을 바탕으로 가능한 행동들 생성
            DecisionOption[] options = GenerateDecisionOptions(population, economic);
            
            // 3. 효용 함수를 사용하여 각 선택지 평가
            float bestUtility = float.MinValue;
            DecisionType bestDecision = DecisionType.DoNothing;
            
            foreach (var option in options)
            {
                float utility = CalculateUtility(option, population, economic);
                if (utility > bestUtility)
                {
                    bestUtility = utility;
                    bestDecision = option.decisionType;
                }
            }
            
            // 4. 실행을 위한 결정 대기열에 추가
            decision.pendingDecision = bestDecision;
            decision.decisionConfidence = bestUtility;
        }
    }
}
```

#### 행동 원형들
```csharp
public enum PopulationArchetype : byte
{
    Conservative,    // 위험 회피형, 저축형, 안정적 직업
    Ambitious,      // 위험 추구형, 성장 추구형, 기업가
    Hedonistic,     // 현재 중심형, 고소비
    Analytical,     // 데이터 중심, 합리적
    Impulsive,      // 감정 중심, 일관성 없음
    Conformist      // 군중 추종, 트렌드 추종자
}
```

### 3.2 회사 행동 시스템

#### 비즈니스 전략 프레임워크
```csharp
public struct CompanyStrategyComponent : IComponentData
{
    public BusinessStrategy primaryStrategy;
    public float aggressiveness;        // 위험 허용도 (0.0 = 보수적, 1.0 = 공격적)
    public float marketFocus;          // 시장 점유율 vs 이익 중심
    public float innovationTendency;   // R&D 투자 성향
    public float growthAmbition;       // 확장 vs 통합
}

public enum BusinessStrategy : byte
{
    CostLeadership,     // 가격 경쟁
    Differentiation,    // 품질/기능 경쟁
    FocusNiche,        // 특정 시장 세그먼트 서비스
    Innovation,        // 선발주자 우위
    FastFollower,      // 성공한 혁신 모방
    Consolidation      // 경쟁사 인수
}
```

## 4. 성능 최적화

### 4.1 Job System 통합

#### 병렬 처리 전략
```csharp
[BurstCompile]
public struct PopulationDecisionJob : IJobChunk
{
    public ComponentTypeHandle<PopulationComponent> PopulationHandle;
    public ComponentTypeHandle<EconomicStatusComponent> EconomicHandle;
    [ReadWrite] public ComponentTypeHandle<PopulationDecisionComponent> DecisionHandle;
    
    public void Execute(in ArchetypeChunk chunk, int unfilteredChunkIndex, 
                       bool useEnabledMask, in v128 chunkEnabledMask)
    {
        var populations = chunk.GetNativeArray(ref PopulationHandle);
        var economics = chunk.GetNativeArray(ref EconomicHandle);
        var decisions = chunk.GetNativeArray(ref DecisionHandle);
        
        for (int i = 0; i < chunk.Count; i++)
        {
            // 청크의 각 엔티티에 대해 병렬 결정 계산
            decisions[i] = CalculateOptimalDecision(populations[i], economics[i]);
        }
    }
}
```

### 4.2 설정 시스템

#### 경제 설정
```csharp
[CreateAssetMenu(fileName = "EconomicConfig", menuName = "Capitalism/Economic Configuration")]
public class EconomicConfiguration : ScriptableObject
{
    [Header("인구 설정")]
    public int initialPopulationCount = 1000;
    public AnimationCurve incomeDistribution;
    public float populationGrowthRate = 0.02f;
    
    [Header("회사 설정")]
    public int initialCompanyCount = 100;
    public AnimationCurve industryDistribution;
    public float companyBirthRate = 0.05f;
    public float companyDeathRate = 0.03f;
    
    [Header("시뮬레이션 속도")]
    public float timeScale = 1.0f;
    public int economicUpdateFrequency = 1; // 초당 업데이트 수
}
```

## 5. 구현 단계

### 1단계: 기본 엔티티 생성
- 인구 및 회사 생성
- 기본 컴포넌트 초기화
- 단순한 랜덤 매개변수 할당

### 2단계: 자율 행동
- 인구 의사결정 시스템
- 회사 운영 시스템
- 기본 시장 상호작용

### 3단계: 경제 역학
- 공급과 수요 메커니즘
- 고용 시스템
- 시장 가격 발견

### 4단계: 고급 기능
- 랜덤 이벤트
- 위기 시뮬레이션
- 플레이어 상호작용 시스템

## 다음 단계

1. **[엔티티 생성 시스템](./entity-generation_KOR.md)** - 랜덤 엔티티 생성 알고리즘
2. **[구현 로드맵](./implementation-roadmap_KOR.md)** - 단계별 개발 가이드

## 관련 문서

- [ECS 설계](./ecs-design_KOR.md) - 핵심 ECS 아키텍처
- [데이터 모델](./data-model_KOR.md) - 컴포넌트 명세
- [기술 아키텍처](./technical-architecture_KOR.md) - 전체 시스템 설계