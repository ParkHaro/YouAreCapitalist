---
category: architecture
tags: [unity, ecs, integration, bridge, data-flow]
related: [ecs-design.md, technical-architecture.md, ui-system.md]
parent: INDEX.md
created: 2025-08-30
updated: 2025-08-30
priority: high
---

# System Integration Guide

[🇰🇷 Korean Version](./integration-guide_KOR.md)

## 📍 Navigation

[↩️ Back to Architecture](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Integration Architecture Overview

### 1.1 Inter-System Communication Structure

```
┌─────────────────────────────────────────┐
│          UI Layer (MonoBehaviour)       │
│                                         │
│  ┌─────────────┐  ┌─────────────────────┐│
│  │  Dashboard  │  │    Chart System    ││
│  │   Panels    │  │                     ││
│  └─────────────┘  └─────────────────────┘│
└─────────────┬───────────────┬───────────┘
              │               │
              ▼               ▼
┌─────────────────────────────────────────┐
│        Bridge Layer (Event System)      │
│                                         │
│  ┌─────────────┐  ┌─────────────────────┐│
│  │    Event    │  │   Data Conversion   ││
│  │  Aggregator │  │     Manager        ││
│  └─────────────┘  └─────────────────────┘│
└─────────────┬───────────────┬───────────┘
              │               │
              ▼               ▼
┌─────────────────────────────────────────┐
│         ECS Layer (Data Processing)     │
│                                         │
│  ┌─────────────┐  ┌─────────────────────┐│
│  │ Population  │  │     Market         ││
│  │  Systems    │  │    Systems         ││
│  └─────────────┘  └─────────────────────┘│
└─────────────────────────────────────────┘
```

### 1.2 Data Flow Patterns

#### Unidirectional Data Flow
```csharp
// ECS → Event → UI unidirectional flow
public class DataFlowManager : MonoBehaviour
{
    // 1. ECS에서 데이터 변화 감지
    // 2. 이벤트 시스템으로 변화 알림
    // 3. UI가 이벤트를 받아 자동 업데이트
    
    public static System.Action<EconomicData> OnEconomicDataChanged;
    public static System.Action<MarketData> OnMarketDataChanged;
    public static System.Action<CompanyData> OnCompanyDataChanged;
    
    // 데이터 업데이트 파이프라인
    void ProcessDataFlow()
    {
        // ECS 시스템에서 계산된 데이터 읽기
        var economicData = ReadEconomicDataFromECS();
        
        // 이벤트 발생으로 UI에 알림
        OnEconomicDataChanged?.Invoke(economicData);
        
        // 필요시 로컬 캐싱
        CacheDataForPerformance(economicData);
    }
}
```

## 2. ECS ↔ MonoBehaviour 브리지 시스템

### 2.1 데이터 브리지 아키텍처

#### 핵심 브리지 클래스
```csharp
// ECS와 MonoBehaviour 간 데이터 브리지
public class ECSDataBridge : MonoBehaviour
{
    [Header("ECS Integration")]
    [SerializeField] private bool autoUpdate = true;
    [SerializeField] private float updateInterval = 0.1f;
    
    // ECS World 참조
    private World ecsWorld;
    private EntityManager entityManager;
    
    // 캐시된 데이터
    private EconomicDataSnapshot cachedEconomicData;
    private MarketDataSnapshot cachedMarketData;
    private CompanyDataSnapshot[] cachedCompanyData;
    
    // 이벤트 시스템
    public static System.Action<EconomicDataSnapshot> OnEconomicDataUpdated;
    public static System.Action<MarketDataSnapshot> OnMarketDataUpdated;
    public static System.Action<CompanyDataSnapshot[]> OnCompanyDataUpdated;
    
    void Start()
    {
        InitializeBridge();
        
        if (autoUpdate)
        {
            StartCoroutine(UpdateDataCoroutine());
        }
    }
    
    void InitializeBridge()
    {
        // ECS World 참조 획득
        ecsWorld = World.DefaultGameObjectInjectionWorld;
        entityManager = ecsWorld.EntityManager;
        
        // 초기 데이터 로드
        RefreshAllData();
    }
    
    System.Collections.IEnumerator UpdateDataCoroutine()
    {
        while (enabled)
        {
            RefreshAllData();
            yield return new WaitForSeconds(updateInterval);
        }
    }
    
    void RefreshAllData()
    {
        // 경제 지표 데이터 가져오기
        RefreshEconomicData();
        
        // 시장 데이터 가져오기
        RefreshMarketData();
        
        // 회사 데이터 가져오기
        RefreshCompanyData();
    }
    
    void RefreshEconomicData()
    {
        var query = entityManager.CreateEntityQuery(typeof(MacroEconomicsComponent));
        if (query.TryGetSingleton<MacroEconomicsComponent>(out var macroEcon))
        {
            var newData = new EconomicDataSnapshot
            {
                GDP = macroEcon.gdp,
                GDPGrowthRate = macroEcon.gdpGrowthRate,
                InflationRate = macroEcon.inflationRate,
                UnemploymentRate = macroEcon.unemploymentRate,
                InterestRate = macroEcon.interestRate,
                Timestamp = Time.time
            };
            
            // 데이터가 변경되었으면 이벤트 발생
            if (!newData.Equals(cachedEconomicData))
            {
                cachedEconomicData = newData;
                OnEconomicDataUpdated?.Invoke(cachedEconomicData);
            }
        }
        query.Dispose();
    }
    
    void RefreshMarketData()
    {
        var query = entityManager.CreateEntityQuery(typeof(StockMarketComponent));
        if (query.TryGetSingleton<StockMarketComponent>(out var marketComp))
        {
            var newData = new MarketDataSnapshot
            {
                MarketIndex = marketComp.marketIndex,
                TotalMarketCap = marketComp.totalMarketCap,
                AveragePE = marketComp.averagePE,
                TotalVolume = marketComp.totalVolume,
                MarketSentiment = marketComp.sentiment,
                Timestamp = Time.time
            };
            
            if (!newData.Equals(cachedMarketData))
            {
                cachedMarketData = newData;
                OnMarketDataUpdated?.Invoke(cachedMarketData);
            }
        }
        query.Dispose();
    }
    
    void RefreshCompanyData()
    {
        var query = entityManager.CreateEntityQuery(
            typeof(CompanyComponent),
            typeof(FinancialComponent),
            typeof(StockComponent)
        );
        
        var companies = new List<CompanyDataSnapshot>();
        
        Entities.With(query).ForEach((Entity entity, ref CompanyComponent company, 
                                     ref FinancialComponent financial, ref StockComponent stock) =>
        {
            companies.Add(new CompanyDataSnapshot
            {
                CompanyID = company.companyID,
                Name = company.companyName.ToString(),
                Industry = company.industry,
                Revenue = financial.revenue,
                NetProfit = financial.netProfit,
                StockPrice = stock.stockPrice,
                MarketCap = stock.stockPrice * stock.sharesOutstanding,
                Timestamp = Time.time
            });
        });
        
        // 데이터 정렬 (시가총액 기준)
        companies.Sort((a, b) => b.MarketCap.CompareTo(a.MarketCap));
        
        var newCompanyData = companies.ToArray();
        
        // 변경사항 감지 (간단한 해시 비교)
        if (!CompareCompanyData(cachedCompanyData, newCompanyData))
        {
            cachedCompanyData = newCompanyData;
            OnCompanyDataUpdated?.Invoke(cachedCompanyData);
        }
        
        query.Dispose();
    }
    
    bool CompareCompanyData(CompanyDataSnapshot[] oldData, CompanyDataSnapshot[] newData)
    {
        if (oldData == null || newData == null) return oldData == newData;
        if (oldData.Length != newData.Length) return false;
        
        for (int i = 0; i < oldData.Length; i++)
        {
            if (!oldData[i].Equals(newData[i])) return false;
        }
        
        return true;
    }
    
    // 외부에서 수동으로 데이터 요청
    public EconomicDataSnapshot GetEconomicData() => cachedEconomicData;
    public MarketDataSnapshot GetMarketData() => cachedMarketData;
    public CompanyDataSnapshot[] GetCompanyData() => cachedCompanyData;
    
    // 강제 업데이트
    public void ForceRefresh()
    {
        RefreshAllData();
    }
}

// 데이터 스냅샷 구조체들
[System.Serializable]
public struct EconomicDataSnapshot : System.IEquatable<EconomicDataSnapshot>
{
    public float GDP;
    public float GDPGrowthRate;
    public float InflationRate;
    public float UnemploymentRate;
    public float InterestRate;
    public float Timestamp;
    
    public bool Equals(EconomicDataSnapshot other)
    {
        return Mathf.Approximately(GDP, other.GDP) &&
               Mathf.Approximately(GDPGrowthRate, other.GDPGrowthRate) &&
               Mathf.Approximately(InflationRate, other.InflationRate) &&
               Mathf.Approximately(UnemploymentRate, other.UnemploymentRate) &&
               Mathf.Approximately(InterestRate, other.InterestRate);
    }
}

[System.Serializable]
public struct MarketDataSnapshot : System.IEquatable<MarketDataSnapshot>
{
    public float MarketIndex;
    public float TotalMarketCap;
    public float AveragePE;
    public long TotalVolume;
    public MarketSentiment MarketSentiment;
    public float Timestamp;
    
    public bool Equals(MarketDataSnapshot other)
    {
        return Mathf.Approximately(MarketIndex, other.MarketIndex) &&
               Mathf.Approximately(TotalMarketCap, other.TotalMarketCap) &&
               Mathf.Approximately(AveragePE, other.AveragePE) &&
               TotalVolume == other.TotalVolume &&
               MarketSentiment == other.MarketSentiment;
    }
}

[System.Serializable]
public struct CompanyDataSnapshot : System.IEquatable<CompanyDataSnapshot>
{
    public int CompanyID;
    public string Name;
    public IndustryType Industry;
    public float Revenue;
    public float NetProfit;
    public float StockPrice;
    public float MarketCap;
    public float Timestamp;
    
    public bool Equals(CompanyDataSnapshot other)
    {
        return CompanyID == other.CompanyID &&
               Name == other.Name &&
               Industry == other.Industry &&
               Mathf.Approximately(Revenue, other.Revenue) &&
               Mathf.Approximately(NetProfit, other.NetProfit) &&
               Mathf.Approximately(StockPrice, other.StockPrice);
    }
}
```

### 2.2 명령 패턴을 통한 UI → ECS 통신

#### 명령 시스템
```csharp
// UI에서 ECS로 명령을 전달하는 시스템
public interface IECSCommand
{
    void Execute(EntityManager entityManager);
}

public class ECSCommandProcessor : MonoBehaviour
{
    private Queue<IECSCommand> commandQueue = new Queue<IECSCommand>();
    private EntityManager entityManager;
    
    void Start()
    {
        var world = World.DefaultGameObjectInjectionWorld;
        entityManager = world.EntityManager;
    }
    
    void LateUpdate()
    {
        // 프레임 끝에 모든 명령 처리
        ProcessCommands();
    }
    
    public void EnqueueCommand(IECSCommand command)
    {
        commandQueue.Enqueue(command);
    }
    
    void ProcessCommands()
    {
        while (commandQueue.Count > 0)
        {
            var command = commandQueue.Dequeue();
            try
            {
                command.Execute(entityManager);
            }
            catch (System.Exception e)
            {
                Debug.LogError($"Error executing ECS command: {e.Message}");
            }
        }
    }
}

// 플레이어 투자 명령
public class PlayerInvestCommand : IECSCommand
{
    public int companyID;
    public float investmentAmount;
    public InvestmentType type;
    
    public PlayerInvestCommand(int companyId, float amount, InvestmentType investmentType)
    {
        companyID = companyId;
        investmentAmount = amount;
        type = investmentType;
    }
    
    public void Execute(EntityManager entityManager)
    {
        // 플레이어 포트폴리오 엔티티 찾기
        var query = entityManager.CreateEntityQuery(typeof(PlayerPortfolioComponent));
        if (query.TryGetSingleton<PlayerPortfolioComponent>(out var portfolio))
        {
            // 투자 실행
            switch (type)
            {
                case InvestmentType.Stock:
                    ExecuteStockInvestment(entityManager, portfolio);
                    break;
                case InvestmentType.Bond:
                    ExecuteBondInvestment(entityManager, portfolio);
                    break;
                default:
                    Debug.LogWarning($"Unknown investment type: {type}");
                    break;
            }
        }
        query.Dispose();
    }
    
    void ExecuteStockInvestment(EntityManager entityManager, PlayerPortfolioComponent portfolio)
    {
        // 회사 엔티티 찾기
        var companyQuery = entityManager.CreateEntityQuery(
            typeof(CompanyComponent), 
            typeof(StockComponent)
        );
        
        var companies = companyQuery.ToEntityArray(Allocator.TempJob);
        var companyComponents = companyQuery.ToComponentDataArray<CompanyComponent>(Allocator.TempJob);
        var stockComponents = companyQuery.ToComponentDataArray<StockComponent>(Allocator.TempJob);
        
        for (int i = 0; i < companies.Length; i++)
        {
            if (companyComponents[i].companyID == companyID)
            {
                var stock = stockComponents[i];
                
                // 주식 구매 가능 여부 확인
                if (portfolio.liquidAssets >= investmentAmount && stock.stockPrice > 0)
                {
                    // 주식 구매 실행
                    float shareCount = investmentAmount / stock.stockPrice;
                    
                    // 플레이어 포트폴리오 업데이트
                    var newPortfolio = portfolio;
                    newPortfolio.liquidAssets -= investmentAmount;
                    newPortfolio.stockInvestments += investmentAmount;
                    newPortfolio.netWorth = newPortfolio.totalAssets - newPortfolio.totalLiabilities;
                    
                    // 포트폴리오 엔티티 업데이트
                    entityManager.SetComponentData(companyQuery.GetSingletonEntity(), newPortfolio);
                    
                    // 투자 히스토리 기록
                    RecordInvestmentHistory(entityManager, companyID, investmentAmount, InvestmentType.Stock);
                    
                    Debug.Log($"주식 투자 완료: {companyComponents[i].companyName} {shareCount:F2}주 구매");
                }
                break;
            }
        }
        
        companies.Dispose();
        companyComponents.Dispose();
        stockComponents.Dispose();
        companyQuery.Dispose();
    }
    
    void RecordInvestmentHistory(EntityManager entityManager, int companyId, float amount, InvestmentType type)
    {
        // 투자 히스토리 엔티티 생성
        var historyEntity = entityManager.CreateEntity();
        entityManager.AddComponentData(historyEntity, new PlayerInvestmentHistory
        {
            companyID = companyId,
            investmentAmount = amount,
            investmentType = type,
            timestamp = Time.time,
            expectedReturn = 0f // 추후 계산
        });
    }
}

// 자동화 설정 명령
public class SetAutomationCommand : IECSCommand
{
    public AutomationType automationType;
    public bool enabled;
    public float[] parameters;
    
    public void Execute(EntityManager entityManager)
    {
        var query = entityManager.CreateEntityQuery(typeof(AutomationComponent));
        if (query.TryGetSingleton<AutomationComponent>(out var automation))
        {
            var newAutomation = automation;
            
            switch (automationType)
            {
                case AutomationType.PortfolioRebalancing:
                    newAutomation.portfolioRebalancing = enabled;
                    if (parameters != null && parameters.Length > 0)
                        newAutomation.riskTolerance = parameters[0];
                    break;
                    
                case AutomationType.DividendReinvestment:
                    newAutomation.dividendReinvestment = enabled;
                    break;
                    
                case AutomationType.TaxOptimization:
                    newAutomation.taxOptimization = enabled;
                    break;
                    
                case AutomationType.RiskManagement:
                    newAutomation.riskManagement = enabled;
                    if (parameters != null && parameters.Length > 1)
                    {
                        newAutomation.riskTolerance = parameters[0];
                        newAutomation.targetReturn = parameters[1];
                    }
                    break;
            }
            
            entityManager.SetComponentData(query.GetSingletonEntity(), newAutomation);
            Debug.Log($"자동화 설정 변경: {automationType} = {enabled}");
        }
        query.Dispose();
    }
}

// 열거형 정의
public enum InvestmentType
{
    Stock,
    Bond,
    RealEstate,
    Alternative
}

public enum AutomationType
{
    PortfolioRebalancing,
    DividendReinvestment,
    TaxOptimization,
    RiskManagement
}
```

### 2.3 UI 컨트롤러와 브리지 통합

#### UI 컨트롤러 예시
```csharp
// 투자 패널 UI 컨트롤러
public class InvestmentPanelController : MonoBehaviour
{
    [Header("UI References")]
    [SerializeField] private Button buyStockButton;
    [SerializeField] private InputField investmentAmountInput;
    [SerializeField] private Dropdown companyDropdown;
    [SerializeField] private Text currentPortfolioText;
    
    [Header("Dependencies")]
    [SerializeField] private ECSCommandProcessor commandProcessor;
    [SerializeField] private ECSDataBridge dataBridge;
    
    private CompanyDataSnapshot[] availableCompanies;
    private EconomicDataSnapshot currentEconomicData;
    
    void Start()
    {
        InitializeUI();
        SubscribeToEvents();
    }
    
    void InitializeUI()
    {
        buyStockButton.onClick.AddListener(OnBuyStockClicked);
        
        // 초기 데이터 로드
        UpdateCompanyDropdown();
        UpdatePortfolioDisplay();
    }
    
    void SubscribeToEvents()
    {
        // ECS 데이터 변화 이벤트 구독
        ECSDataBridge.OnCompanyDataUpdated += OnCompanyDataUpdated;
        ECSDataBridge.OnEconomicDataUpdated += OnEconomicDataUpdated;
    }
    
    void OnDestroy()
    {
        // 이벤트 구독 해제
        ECSDataBridge.OnCompanyDataUpdated -= OnCompanyDataUpdated;
        ECSDataBridge.OnEconomicDataUpdated -= OnEconomicDataUpdated;
    }
    
    void OnCompanyDataUpdated(CompanyDataSnapshot[] companies)
    {
        availableCompanies = companies;
        UpdateCompanyDropdown();
    }
    
    void OnEconomicDataUpdated(EconomicDataSnapshot economicData)
    {
        currentEconomicData = economicData;
        UpdateEconomicIndicators();
    }
    
    void UpdateCompanyDropdown()
    {
        if (availableCompanies == null) return;
        
        companyDropdown.ClearOptions();
        var options = new List<string>();
        
        foreach (var company in availableCompanies)
        {
            options.Add($"{company.Name} (₩{company.StockPrice:N0})");
        }
        
        companyDropdown.AddOptions(options);
    }
    
    void UpdatePortfolioDisplay()
    {
        var portfolioData = dataBridge.GetEconomicData(); // 포트폴리오 데이터 가져오기
        if (portfolioData.Timestamp > 0)
        {
            currentPortfolioText.text = $"현금: ₩{portfolioData.GDP:N0}"; // 임시로 GDP 표시
        }
    }
    
    void UpdateEconomicIndicators()
    {
        // 경제 지표에 따른 투자 조언 표시
        if (currentEconomicData.InflationRate > 0.05f) // 5% 이상 인플레이션
        {
            ShowInvestmentAdvice("높은 인플레이션! 실물 자산 투자를 고려하세요.", Color.yellow);
        }
        else if (currentEconomicData.GDPGrowthRate < -0.02f) // 2% 이상 마이너스 성장
        {
            ShowInvestmentAdvice("경기 침체 징후. 방어적 투자를 권장합니다.", Color.red);
        }
        else if (currentEconomicData.GDPGrowthRate > 0.03f) // 3% 이상 성장
        {
            ShowInvestmentAdvice("경기 호조! 성장주 투자 기회입니다.", Color.green);
        }
    }
    
    void ShowInvestmentAdvice(string message, Color color)
    {
        // 투자 조언 UI 표시 (토스트 메시지 등)
        NotificationManager.Instance?.ShowNotification(message, NotificationType.Info);
    }
    
    void OnBuyStockClicked()
    {
        // 입력 값 검증
        if (!float.TryParse(investmentAmountInput.text, out float amount) || amount <= 0)
        {
            ShowError("올바른 투자 금액을 입력하세요.");
            return;
        }
        
        if (companyDropdown.value < 0 || availableCompanies == null || 
            companyDropdown.value >= availableCompanies.Length)
        {
            ShowError("투자할 회사를 선택하세요.");
            return;
        }
        
        // 선택된 회사 정보 가져오기
        var selectedCompany = availableCompanies[companyDropdown.value];
        
        // ECS 명령 생성 및 전송
        var investCommand = new PlayerInvestCommand(
            selectedCompany.CompanyID,
            amount,
            InvestmentType.Stock
        );
        
        commandProcessor.EnqueueCommand(investCommand);
        
        // UI 피드백
        ShowSuccess($"{selectedCompany.Name}에 ₩{amount:N0} 투자 주문이 접수되었습니다.");
        
        // 입력 필드 초기화
        investmentAmountInput.text = "";
    }
    
    void ShowError(string message)
    {
        NotificationManager.Instance?.ShowNotification(message, NotificationType.Error);
    }
    
    void ShowSuccess(string message)
    {
        NotificationManager.Instance?.ShowNotification(message, NotificationType.Success);
    }
}
```

## 3. 이벤트 시스템 설계

### 3.1 중앙집중식 이벤트 관리자

#### 이벤트 매니저
```csharp
// 게임 전체 이벤트를 관리하는 중앙 시스템
public class GameEventManager : MonoBehaviour
{
    public static GameEventManager Instance { get; private set; }
    
    // 이벤트 딕셔너리 (성능 최적화)
    private Dictionary<System.Type, System.Delegate> eventDictionary = 
        new Dictionary<System.Type, System.Delegate>();
    
    // 이벤트 큐 (프레임 끝에 일괄 처리)
    private Queue<System.Action> eventQueue = new Queue<System.Action>();
    
    // 이벤트 통계 (디버깅용)
    private Dictionary<System.Type, int> eventStats = new Dictionary<System.Type, int>();
    
    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    
    void LateUpdate()
    {
        // 프레임 끝에 큐된 이벤트 모두 처리
        ProcessEventQueue();
    }
    
    // 이벤트 구독
    public void Subscribe<T>(System.Action<T> handler) where T : struct
    {
        System.Type eventType = typeof(T);
        
        if (eventDictionary.TryGetValue(eventType, out System.Delegate existingHandler))
        {
            eventDictionary[eventType] = System.Delegate.Combine(existingHandler, handler);
        }
        else
        {
            eventDictionary[eventType] = handler;
        }
    }
    
    // 이벤트 구독 해제
    public void Unsubscribe<T>(System.Action<T> handler) where T : struct
    {
        System.Type eventType = typeof(T);
        
        if (eventDictionary.TryGetValue(eventType, out System.Delegate existingHandler))
        {
            var newHandler = System.Delegate.Remove(existingHandler, handler);
            if (newHandler == null)
            {
                eventDictionary.Remove(eventType);
            }
            else
            {
                eventDictionary[eventType] = newHandler;
            }
        }
    }
    
    // 이벤트 발생 (즉시 실행)
    public void TriggerEvent<T>(T eventData) where T : struct
    {
        System.Type eventType = typeof(T);
        
        if (eventDictionary.TryGetValue(eventType, out System.Delegate handler))
        {
            try
            {
                ((System.Action<T>)handler)?.Invoke(eventData);
                
                // 통계 업데이트
                if (eventStats.ContainsKey(eventType))
                    eventStats[eventType]++;
                else
                    eventStats[eventType] = 1;
            }
            catch (System.Exception e)
            {
                Debug.LogError($"Error triggering event {eventType.Name}: {e.Message}");
            }
        }
    }
    
    // 이벤트 큐에 추가 (지연 실행)
    public void QueueEvent<T>(T eventData) where T : struct
    {
        eventQueue.Enqueue(() => TriggerEvent(eventData));
    }
    
    void ProcessEventQueue()
    {
        while (eventQueue.Count > 0)
        {
            var eventAction = eventQueue.Dequeue();
            try
            {
                eventAction.Invoke();
            }
            catch (System.Exception e)
            {
                Debug.LogError($"Error processing queued event: {e.Message}");
            }
        }
    }
    
    // 이벤트 통계 조회 (디버깅)
    public Dictionary<System.Type, int> GetEventStats()
    {
        return new Dictionary<System.Type, int>(eventStats);
    }
    
    // 모든 이벤트 핸들러 정리
    public void ClearAllEvents()
    {
        eventDictionary.Clear();
        eventQueue.Clear();
        eventStats.Clear();
    }
}

// 게임 이벤트 구조체들
public struct EconomicCrisisEvent
{
    public float severity;          // 0.0 ~ 1.0
    public CrisisType crisisType;
    public float duration;
    public string description;
}

public struct CompanyBankruptcyEvent
{
    public int companyID;
    public string companyName;
    public IndustryType industry;
    public float marketCapLoss;
    public int layoffs;
}

public struct MarketVolatilityEvent
{
    public float volatilityIndex;   // 0.0 ~ 1.0
    public MarketSentiment sentiment;
    public float indexChange;       // 퍼센트 변화
    public string cause;
}

public struct PlayerAchievementEvent
{
    public AchievementType achievementType;
    public float value;             // 달성 값
    public string description;
    public bool isNewRecord;
}

public enum CrisisType
{
    FinancialCrisis,
    RecessionWarning,
    InflationSpike,
    CurrencyDevaluation,
    DebtCrisis,
    BankingCrisis
}

public enum AchievementType
{
    NetWorthMilestone,
    InvestmentReturn,
    MarketTiming,
    DiversificationMaster,
    AutomationExpert
}
```

### 3.2 도메인별 이벤트 시스템

#### 경제 이벤트 시스템
```csharp
// 경제 관련 이벤트를 처리하는 특화 시스템
public class EconomicEventSystem : MonoBehaviour
{
    [Header("Event Settings")]
    [SerializeField] private float eventCheckInterval = 5f;  // 5초마다 이벤트 체크
    [SerializeField] private AnimationCurve eventProbability; // 경제 상태에 따른 이벤트 확률
    
    private ECSDataBridge dataBridge;
    private System.Random randomGenerator;
    
    void Start()
    {
        dataBridge = FindObjectOfType<ECSDataBridge>();
        randomGenerator = new System.Random();
        
        // 주기적으로 경제 이벤트 체크
        InvokeRepeating(nameof(CheckForEconomicEvents), eventCheckInterval, eventCheckInterval);
        
        // 경제 데이터 변화 구독
        ECSDataBridge.OnEconomicDataUpdated += OnEconomicDataChanged;
    }
    
    void OnDestroy()
    {
        ECSDataBridge.OnEconomicDataUpdated -= OnEconomicDataChanged;
    }
    
    void OnEconomicDataChanged(EconomicDataSnapshot economicData)
    {
        // 급격한 경제 지표 변화 감지
        DetectEconomicAnomalies(economicData);
    }
    
    void CheckForEconomicEvents()
    {
        var economicData = dataBridge.GetEconomicData();
        if (economicData.Timestamp <= 0) return;
        
        // 현재 경제 상황에 따른 이벤트 확률 계산
        float crisisRisk = CalculateCrisisRisk(economicData);
        
        // 이벤트 발생 여부 결정
        if (randomGenerator.NextDouble() < crisisRisk * Time.deltaTime)
        {
            GenerateEconomicEvent(economicData, crisisRisk);
        }
        
        // 긍정적 이벤트도 체크
        float growthOpportunity = CalculateGrowthOpportunity(economicData);
        if (randomGenerator.NextDouble() < growthOpportunity * Time.deltaTime)
        {
            GeneratePositiveEvent(economicData);
        }
    }
    
    float CalculateCrisisRisk(EconomicDataSnapshot data)
    {
        float riskScore = 0f;
        
        // 높은 인플레이션 (위험 요소)
        if (data.InflationRate > 0.05f) // 5% 이상
            riskScore += (data.InflationRate - 0.05f) * 10f;
        
        // 높은 실업률 (위험 요소)
        if (data.UnemploymentRate > 0.1f) // 10% 이상
            riskScore += (data.UnemploymentRate - 0.1f) * 5f;
        
        // 음의 GDP 성장 (위험 요소)
        if (data.GDPGrowthRate < 0f)
            riskScore += Mathf.Abs(data.GDPGrowthRate) * 15f;
        
        // 극단적 금리 (위험 요소)
        if (data.InterestRate > 0.15f || data.InterestRate < 0f)
            riskScore += 0.02f;
        
        return Mathf.Clamp01(riskScore);
    }
    
    float CalculateGrowthOpportunity(EconomicDataSnapshot data)
    {
        float opportunityScore = 0f;
        
        // 안정적인 성장
        if (data.GDPGrowthRate > 0.02f && data.GDPGrowthRate < 0.06f) // 2-6% 성장
            opportunityScore += 0.01f;
        
        // 낮은 인플레이션
        if (data.InflationRate > 0f && data.InflationRate < 0.03f) // 0-3% 인플레이션
            opportunityScore += 0.005f;
        
        // 적정 실업률
        if (data.UnemploymentRate > 0.03f && data.UnemploymentRate < 0.08f) // 3-8% 실업률
            opportunityScore += 0.005f;
        
        return Mathf.Clamp01(opportunityScore);
    }
    
    void GenerateEconomicEvent(EconomicDataSnapshot data, float severity)
    {
        // 경제 상황에 맞는 위기 이벤트 생성
        CrisisType crisisType = DetermineCrisisType(data);
        
        var crisisEvent = new EconomicCrisisEvent
        {
            severity = severity,
            crisisType = crisisType,
            duration = UnityEngine.Random.Range(30f, 300f), // 30초~5분
            description = GetCrisisDescription(crisisType, severity)
        };
        
        // 이벤트 발생
        GameEventManager.Instance.TriggerEvent(crisisEvent);
        
        Debug.Log($"경제 위기 발생: {crisisType} (강도: {severity:P1})");
    }
    
    void GeneratePositiveEvent(EconomicDataSnapshot data)
    {
        // 긍정적 경제 이벤트 생성 (기술 혁신, 무역 협정 등)
        var events = new[]
        {
            "신기술 혁신으로 생산성 대폭 향상!",
            "새로운 무역 협정 체결로 수출 증대!",
            "정부 규제 완화로 기업 활동 활성화!",
            "해외 투자 유치 성공으로 자본 유입!"
        };
        
        string selectedEvent = events[randomGenerator.Next(events.Length)];
        
        // 긍정적 이벤트 효과를 ECS에 전달하는 명령 생성
        var positiveEventCommand = new EconomicBoostCommand
        {
            boostType = EconomicBoostType.Innovation,
            magnitude = UnityEngine.Random.Range(0.01f, 0.05f), // 1-5% 부스트
            duration = UnityEngine.Random.Range(60f, 600f), // 1-10분
            description = selectedEvent
        };
        
        FindObjectOfType<ECSCommandProcessor>()?.EnqueueCommand(positiveEventCommand);
        
        // UI에 알림
        NotificationManager.Instance?.ShowNotification(selectedEvent, NotificationType.Success);
    }
    
    CrisisType DetermineCrisisType(EconomicDataSnapshot data)
    {
        // 경제 지표에 따라 가장 적합한 위기 유형 결정
        if (data.InflationRate > 0.1f) // 10% 이상 인플레이션
            return CrisisType.InflationSpike;
        else if (data.GDPGrowthRate < -0.05f) // 5% 이상 마이너스 성장
            return CrisisType.RecessionWarning;
        else if (data.UnemploymentRate > 0.15f) // 15% 이상 실업률
            return CrisisType.FinancialCrisis;
        else if (data.InterestRate > 0.2f) // 20% 이상 금리
            return CrisisType.CurrencyDevaluation;
        else
            return CrisisType.FinancialCrisis; // 기본값
    }
    
    string GetCrisisDescription(CrisisType crisisType, float severity)
    {
        string intensityDescription = severity switch
        {
            > 0.8f => "심각한",
            > 0.6f => "중대한",
            > 0.4f => "상당한",
            > 0.2f => "경미한",
            _ => "약간의"
        };
        
        return crisisType switch
        {
            CrisisType.InflationSpike => $"{intensityDescription} 물가 급등이 발생했습니다.",
            CrisisType.RecessionWarning => $"{intensityDescription} 경기 침체 징후가 나타났습니다.",
            CrisisType.FinancialCrisis => $"{intensityDescription} 금융 위기가 시작되었습니다.",
            CrisisType.CurrencyDevaluation => $"{intensityDescription} 통화 가치 하락이 발생했습니다.",
            CrisisType.DebtCrisis => $"{intensityDescription} 부채 위기가 발생했습니다.",
            CrisisType.BankingCrisis => $"{intensityDescription} 은행 시스템 위기가 발생했습니다.",
            _ => $"{intensityDescription} 경제 위기가 발생했습니다."
        };
    }
    
    void DetectEconomicAnomalies(EconomicDataSnapshot data)
    {
        // TODO: 이전 데이터와 비교하여 급격한 변화 감지
        // 예: GDP가 한 프레임에 10% 이상 변동, 급격한 인플레이션 등
    }
}

// 경제 부양 명령
public class EconomicBoostCommand : IECSCommand
{
    public EconomicBoostType boostType;
    public float magnitude;
    public float duration;
    public string description;
    
    public void Execute(EntityManager entityManager)
    {
        // ECS에 경제 부양 이벤트 엔티티 생성
        var boostEntity = entityManager.CreateEntity();
        entityManager.AddComponentData(boostEntity, new EconomicBoostComponent
        {
            boostType = boostType,
            magnitude = magnitude,
            remainingDuration = duration,
            isActive = true
        });
        
        Debug.Log($"경제 부양 효과 적용: {description} ({magnitude:P1}, {duration}초)");
    }
}

public enum EconomicBoostType
{
    Innovation,      // 기술 혁신
    TradeAgreement, // 무역 협정
    Deregulation,   // 규제 완화
    Investment      // 투자 유치
}

// ECS에서 사용할 경제 부양 컴포넌트
public struct EconomicBoostComponent : IComponentData
{
    public EconomicBoostType boostType;
    public float magnitude;
    public float remainingDuration;
    public bool isActive;
}
```

## 4. 세이브/로드 시스템 통합

### 4.1 통합 세이브 시스템

#### 세이브 매니저
```csharp
// ECS와 MonoBehaviour 데이터를 통합 관리하는 세이브 시스템
public class IntegratedSaveManager : MonoBehaviour
{
    [Header("Save Settings")]
    [SerializeField] private string saveFileName = "YouAreCapitalist_Save";
    [SerializeField] private bool useCompression = true;
    [SerializeField] private bool encryptSaveFile = false;
    
    private string saveFilePath;
    
    void Awake()
    {
        saveFilePath = Path.Combine(Application.persistentDataPath, saveFileName + ".json");
    }
    
    public void SaveGame()
    {
        try
        {
            var saveData = GatherAllSaveData();
            string jsonData = JsonUtility.ToJson(saveData, true);
            
            if (useCompression)
            {
                jsonData = CompressString(jsonData);
            }
            
            if (encryptSaveFile)
            {
                jsonData = EncryptString(jsonData);
            }
            
            File.WriteAllText(saveFilePath, jsonData);
            
            Debug.Log($"게임 저장 완료: {saveFilePath}");
            ShowSaveNotification("게임이 저장되었습니다.", true);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"게임 저장 실패: {e.Message}");
            ShowSaveNotification("게임 저장에 실패했습니다.", false);
        }
    }
    
    public void LoadGame()
    {
        try
        {
            if (!File.Exists(saveFilePath))
            {
                Debug.LogWarning("세이브 파일이 존재하지 않습니다.");
                return;
            }
            
            string jsonData = File.ReadAllText(saveFilePath);
            
            if (encryptSaveFile)
            {
                jsonData = DecryptString(jsonData);
            }
            
            if (useCompression)
            {
                jsonData = DecompressString(jsonData);
            }
            
            var saveData = JsonUtility.FromJson<GameSaveData>(jsonData);
            ApplyLoadedData(saveData);
            
            Debug.Log("게임 로드 완료");
            ShowSaveNotification("게임이 로드되었습니다.", true);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"게임 로드 실패: {e.Message}");
            ShowSaveNotification("게임 로드에 실패했습니다.", false);
        }
    }
    
    GameSaveData GatherAllSaveData()
    {
        var saveData = new GameSaveData();
        
        // ECS 데이터 수집
        saveData.ecsData = GatherECSData();
        
        // MonoBehaviour 데이터 수집
        saveData.uiSettings = GatherUISettings();
        saveData.gameSettings = GatherGameSettings();
        
        // 메타데이터
        saveData.saveTime = System.DateTime.Now.ToBinary();
        saveData.gameVersion = Application.version;
        saveData.playTime = Time.realtimeSinceStartup;
        
        return saveData;
    }
    
    ECSSaveData GatherECSData()
    {
        var entityManager = World.DefaultGameObjectInjectionWorld.EntityManager;
        var ecsData = new ECSSaveData();
        
        // 플레이어 데이터 저장
        var playerQuery = entityManager.CreateEntityQuery(typeof(PlayerPortfolioComponent));
        if (playerQuery.TryGetSingleton<PlayerPortfolioComponent>(out var portfolio))
        {
            ecsData.playerPortfolio = portfolio;
        }
        
        // 경제 상태 저장
        var economicQuery = entityManager.CreateEntityQuery(typeof(MacroEconomicsComponent));
        if (economicQuery.TryGetSingleton<MacroEconomicsComponent>(out var economics))
        {
            ecsData.macroEconomics = economics;
        }
        
        // 시장 상태 저장
        var marketQuery = entityManager.CreateEntityQuery(typeof(StockMarketComponent));
        if (marketQuery.TryGetSingleton<StockMarketComponent>(out var market))
        {
            ecsData.stockMarket = market;
        }
        
        // 회사 데이터 저장
        SaveCompanies(entityManager, ref ecsData);
        
        // 인구 데이터 저장 (샘플링)
        SavePopulationSample(entityManager, ref ecsData);
        
        playerQuery.Dispose();
        economicQuery.Dispose();
        marketQuery.Dispose();
        
        return ecsData;
    }
    
    void SaveCompanies(EntityManager entityManager, ref ECSSaveData ecsData)
    {
        var companyQuery = entityManager.CreateEntityQuery(
            typeof(CompanyComponent),
            typeof(FinancialComponent),
            typeof(StockComponent)
        );
        
        var companies = new List<CompanySaveData>();
        
        Entities.With(companyQuery).ForEach((Entity entity, ref CompanyComponent company,
                                           ref FinancialComponent financial, ref StockComponent stock) =>
        {
            companies.Add(new CompanySaveData
            {
                company = company,
                financial = financial,
                stock = stock
            });
        });
        
        ecsData.companies = companies.ToArray();
        companyQuery.Dispose();
    }
    
    void SavePopulationSample(EntityManager entityManager, ref ECSSaveData ecsData)
    {
        // 모든 인구를 저장하면 용량이 너무 크므로 대표 샘플만 저장
        var populationQuery = entityManager.CreateEntityQuery(typeof(PopulationComponent));
        var entities = populationQuery.ToEntityArray(Allocator.TempJob);
        
        if (entities.Length > 0)
        {
            // 10%만 샘플링
            int sampleSize = Mathf.Max(100, entities.Length / 10);
            var samples = new List<PopulationSaveData>();
            
            for (int i = 0; i < sampleSize && i < entities.Length; i++)
            {
                var entity = entities[i];
                if (entityManager.HasComponent<PopulationComponent>(entity) &&
                    entityManager.HasComponent<EconomicStatusComponent>(entity))
                {
                    samples.Add(new PopulationSaveData
                    {
                        population = entityManager.GetComponentData<PopulationComponent>(entity),
                        economic = entityManager.GetComponentData<EconomicStatusComponent>(entity)
                    });
                }
            }
            
            ecsData.populationSample = samples.ToArray();
            ecsData.totalPopulationCount = entities.Length;
        }
        
        entities.Dispose();
        populationQuery.Dispose();
    }
    
    UISettingsSaveData GatherUISettings()
    {
        return new UISettingsSaveData
        {
            masterVolume = AudioListener.volume,
            windowSize = new Vector2(Screen.width, Screen.height),
            fullscreen = Screen.fullScreen,
            // 추가 UI 설정들...
        };
    }
    
    GameSettingsSaveData GatherGameSettings()
    {
        return new GameSettingsSaveData
        {
            timeScale = Time.timeScale,
            difficulty = GetCurrentDifficulty(),
            autoSaveInterval = GetAutoSaveInterval(),
            // 추가 게임 설정들...
        };
    }
    
    void ApplyLoadedData(GameSaveData saveData)
    {
        // ECS 데이터 적용
        ApplyECSData(saveData.ecsData);
        
        // UI 설정 적용
        ApplyUISettings(saveData.uiSettings);
        
        // 게임 설정 적용
        ApplyGameSettings(saveData.gameSettings);
    }
    
    void ApplyECSData(ECSSaveData ecsData)
    {
        var entityManager = World.DefaultGameObjectInjectionWorld.EntityManager;
        
        // 기존 데이터 정리
        ClearECSData(entityManager);
        
        // 플레이어 데이터 복원
        var playerEntity = entityManager.CreateEntity();
        entityManager.AddComponentData(playerEntity, ecsData.playerPortfolio);
        
        // 경제 데이터 복원
        var economicEntity = entityManager.CreateEntity();
        entityManager.AddComponentData(economicEntity, ecsData.macroEconomics);
        
        // 시장 데이터 복원
        var marketEntity = entityManager.CreateEntity();
        entityManager.AddComponentData(marketEntity, ecsData.stockMarket);
        
        // 회사 데이터 복원
        RestoreCompanies(entityManager, ecsData.companies);
        
        // 인구 데이터 복원 (확장)
        RestorePopulation(entityManager, ecsData.populationSample, ecsData.totalPopulationCount);
    }
    
    void RestoreCompanies(EntityManager entityManager, CompanySaveData[] companies)
    {
        foreach (var companyData in companies)
        {
            var entity = entityManager.CreateEntity();
            entityManager.AddComponentData(entity, companyData.company);
            entityManager.AddComponentData(entity, companyData.financial);
            entityManager.AddComponentData(entity, companyData.stock);
        }
    }
    
    void RestorePopulation(EntityManager entityManager, PopulationSaveData[] samples, int totalCount)
    {
        // 샘플 데이터를 기반으로 전체 인구 생성
        // 실제 게임에서는 더 정교한 인구 재생성 알고리즘 필요
        
        foreach (var sample in samples)
        {
            var entity = entityManager.CreateEntity();
            entityManager.AddComponentData(entity, sample.population);
            entityManager.AddComponentData(entity, sample.economic);
        }
        
        // 나머지 인구는 통계적 분포를 기반으로 생성
        int remainingCount = totalCount - samples.Length;
        GeneratePopulationFromStatistics(entityManager, samples, remainingCount);
    }
    
    void GeneratePopulationFromStatistics(EntityManager entityManager, PopulationSaveData[] samples, int count)
    {
        if (samples.Length == 0) return;
        
        // 샘플의 통계적 특성 분석
        var incomeDistribution = AnalyzeIncomeDistribution(samples);
        var classDistribution = AnalyzeClassDistribution(samples);
        
        // 분석된 분포를 기반으로 새 인구 생성
        for (int i = 0; i < count; i++)
        {
            var entity = entityManager.CreateEntity();
            
            var newPopulation = GeneratePopulationFromDistribution(classDistribution);
            var newEconomic = GenerateEconomicFromDistribution(incomeDistribution);
            
            entityManager.AddComponentData(entity, newPopulation);
            entityManager.AddComponentData(entity, newEconomic);
        }
    }
    
    // 압축/암호화 헬퍼 메서드들
    string CompressString(string text)
    {
        byte[] data = System.Text.Encoding.UTF8.GetBytes(text);
        using (var memory = new MemoryStream())
        using (var gzip = new System.IO.Compression.GZipStream(memory, System.IO.Compression.CompressionMode.Compress))
        {
            gzip.Write(data, 0, data.Length);
            gzip.Close();
            return System.Convert.ToBase64String(memory.ToArray());
        }
    }
    
    string DecompressString(string compressedText)
    {
        byte[] data = System.Convert.FromBase64String(compressedText);
        using (var memory = new MemoryStream(data))
        using (var gzip = new System.IO.Compression.GZipStream(memory, System.IO.Compression.CompressionMode.Decompress))
        using (var reader = new StreamReader(gzip))
        {
            return reader.ReadToEnd();
        }
    }
    
    // 간단한 XOR 암호화 (실제 게임에서는 더 강력한 암호화 사용 권장)
    string EncryptString(string text)
    {
        var key = "YouAreCapitalist2024"; // 실제로는 더 복잡한 키 생성
        var result = new System.Text.StringBuilder();
        
        for (int i = 0; i < text.Length; i++)
        {
            result.Append((char)(text[i] ^ key[i % key.Length]));
        }
        
        return System.Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(result.ToString()));
    }
    
    string DecryptString(string encryptedText)
    {
        var data = System.Convert.FromBase64String(encryptedText);
        var text = System.Text.Encoding.UTF8.GetString(data);
        
        var key = "YouAreCapitalist2024";
        var result = new System.Text.StringBuilder();
        
        for (int i = 0; i < text.Length; i++)
        {
            result.Append((char)(text[i] ^ key[i % key.Length]));
        }
        
        return result.ToString();
    }
    
    void ShowSaveNotification(string message, bool success)
    {
        var notificationType = success ? NotificationType.Success : NotificationType.Error;
        NotificationManager.Instance?.ShowNotification(message, notificationType);
    }
    
    // 헬퍼 메서드들
    float GetCurrentDifficulty() => 1.0f; // 임시
    float GetAutoSaveInterval() => 300f; // 5분
    void ClearECSData(EntityManager entityManager) { /* 기존 데이터 정리 */ }
    void ApplyUISettings(UISettingsSaveData settings) { /* UI 설정 적용 */ }
    void ApplyGameSettings(GameSettingsSaveData settings) { /* 게임 설정 적용 */ }
    
    // 통계 분석 메서드들
    float[] AnalyzeIncomeDistribution(PopulationSaveData[] samples) => new float[0]; // 구현 필요
    PopulationClass[] AnalyzeClassDistribution(PopulationSaveData[] samples) => new PopulationClass[0]; // 구현 필요
    PopulationComponent GeneratePopulationFromDistribution(PopulationClass[] distribution) => new PopulationComponent(); // 구현 필요
    EconomicStatusComponent GenerateEconomicFromDistribution(float[] distribution) => new EconomicStatusComponent(); // 구현 필요
}

// 세이브 데이터 구조체들
[System.Serializable]
public struct GameSaveData
{
    public ECSSaveData ecsData;
    public UISettingsSaveData uiSettings;
    public GameSettingsSaveData gameSettings;
    
    // 메타데이터
    public long saveTime;
    public string gameVersion;
    public float playTime;
}

[System.Serializable]
public struct ECSSaveData
{
    public PlayerPortfolioComponent playerPortfolio;
    public MacroEconomicsComponent macroEconomics;
    public StockMarketComponent stockMarket;
    public CompanySaveData[] companies;
    public PopulationSaveData[] populationSample;
    public int totalPopulationCount;
}

[System.Serializable]
public struct CompanySaveData
{
    public CompanyComponent company;
    public FinancialComponent financial;
    public StockComponent stock;
}

[System.Serializable]
public struct PopulationSaveData
{
    public PopulationComponent population;
    public EconomicStatusComponent economic;
}

[System.Serializable]
public struct UISettingsSaveData
{
    public float masterVolume;
    public Vector2 windowSize;
    public bool fullscreen;
}

[System.Serializable]
public struct GameSettingsSaveData
{
    public float timeScale;
    public float difficulty;
    public float autoSaveInterval;
}
```

## 5. 성능 모니터링 및 최적화

### 5.1 실시간 성능 모니터

#### 성능 모니터링 시스템
```csharp
// 통합 성능 모니터링 시스템
public class IntegratedPerformanceMonitor : MonoBehaviour
{
    [Header("Monitoring Settings")]
    [SerializeField] private bool enableMonitoring = true;
    [SerializeField] private float updateInterval = 1f;
    [SerializeField] private int sampleCount = 60; // 1분간 샘플
    
    [Header("Performance Targets")]
    [SerializeField] private float targetFPS = 60f;
    [SerializeField] private float maxFrameTime = 16.67f; // 60fps = 16.67ms
    [SerializeField] private int maxMemoryMB = 2048; // 2GB
    
    [Header("UI References")]
    [SerializeField] private Text fpsText;
    [SerializeField] private Text memoryText;
    [SerializeField] private Text entityCountText;
    [SerializeField] private Slider performanceSlider;
    
    // 성능 데이터 수집
    private Queue<float> frameTimes = new Queue<float>();
    private Queue<float> memoryUsage = new Queue<float>();
    private Queue<int> entityCounts = new Queue<int>();
    
    // 통계
    private float averageFPS;
    private float averageFrameTime;
    private float averageMemory;
    private float peakMemory;
    private int averageEntityCount;
    
    // ECS 관련
    private World ecsWorld;
    private EntityManager entityManager;
    
    public static IntegratedPerformanceMonitor Instance { get; private set; }
    
    // 성능 이벤트
    public static System.Action<PerformanceData> OnPerformanceDataUpdated;
    public static System.Action<PerformanceAlert> OnPerformanceAlert;
    
    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    
    void Start()
    {
        if (enableMonitoring)
        {
            ecsWorld = World.DefaultGameObjectInjectionWorld;
            entityManager = ecsWorld.EntityManager;
            
            InvokeRepeating(nameof(CollectPerformanceData), 0f, updateInterval);
            InvokeRepeating(nameof(UpdateUI), 0f, updateInterval);
        }
    }
    
    void CollectPerformanceData()
    {
        // 프레임 시간 수집
        float currentFrameTime = Time.unscaledDeltaTime * 1000f; // ms
        frameTimes.Enqueue(currentFrameTime);
        if (frameTimes.Count > sampleCount)
            frameTimes.Dequeue();
        
        // 메모리 사용량 수집
        float currentMemory = System.GC.GetTotalMemory(false) / (1024f * 1024f); // MB
        memoryUsage.Enqueue(currentMemory);
        if (memoryUsage.Count > sampleCount)
            memoryUsage.Dequeue();
        
        // ECS 엔티티 수 수집
        int currentEntityCount = entityManager.GetAllEntities().Length;
        entityCounts.Enqueue(currentEntityCount);
        if (entityCounts.Count > sampleCount)
            entityCounts.Dequeue();
        
        // 통계 계산
        CalculateStatistics();
        
        // 성능 데이터 이벤트 발생
        var performanceData = new PerformanceData
        {
            averageFPS = averageFPS,
            averageFrameTime = averageFrameTime,
            averageMemoryMB = averageMemory,
            peakMemoryMB = peakMemory,
            entityCount = averageEntityCount,
            timestamp = Time.time
        };
        
        OnPerformanceDataUpdated?.Invoke(performanceData);
        
        // 성능 경고 체크
        CheckPerformanceAlerts();
    }
    
    void CalculateStatistics()
    {
        // FPS 및 프레임 시간 통계
        if (frameTimes.Count > 0)
        {
            averageFrameTime = frameTimes.Average();
            averageFPS = averageFrameTime > 0 ? 1000f / averageFrameTime : 0f;
        }
        
        // 메모리 통계
        if (memoryUsage.Count > 0)
        {
            averageMemory = memoryUsage.Average();
            peakMemory = memoryUsage.Max();
        }
        
        // 엔티티 수 통계
        if (entityCounts.Count > 0)
        {
            averageEntityCount = (int)entityCounts.Average();
        }
    }
    
    void CheckPerformanceAlerts()
    {
        // FPS 저하 경고
        if (averageFPS < targetFPS * 0.8f) // 80% 미만
        {
            TriggerAlert(PerformanceAlertType.LowFPS, 
                        $"FPS 저하: {averageFPS:F1} (목표: {targetFPS})");
        }
        
        // 메모리 사용량 경고
        if (averageMemory > maxMemoryMB * 0.9f) // 90% 초과
        {
            TriggerAlert(PerformanceAlertType.HighMemory, 
                        $"메모리 과다 사용: {averageMemory:F1}MB (한계: {maxMemoryMB}MB)");
        }
        
        // 엔티티 수 경고
        if (averageEntityCount > 100000) // 10만개 초과
        {
            TriggerAlert(PerformanceAlertType.HighEntityCount, 
                        $"엔티티 과다: {averageEntityCount:N0}개");
        }
        
        // 프레임 시간 불안정성 경고
        if (frameTimes.Count > 10)
        {
            float frameTimeVariance = CalculateVariance(frameTimes.ToArray());
            if (frameTimeVariance > 100f) // 높은 분산
            {
                TriggerAlert(PerformanceAlertType.FrameTimeSpikes, 
                            $"프레임 시간 불안정 (분산: {frameTimeVariance:F1})");
            }
        }
    }
    
    void TriggerAlert(PerformanceAlertType alertType, string message)
    {
        var alert = new PerformanceAlert
        {
            alertType = alertType,
            message = message,
            severity = GetAlertSeverity(alertType),
            timestamp = Time.time,
            performanceData = new PerformanceData
            {
                averageFPS = averageFPS,
                averageFrameTime = averageFrameTime,
                averageMemoryMB = averageMemory,
                entityCount = averageEntityCount
            }
        };
        
        OnPerformanceAlert?.Invoke(alert);
        
        Debug.LogWarning($"성능 경고: {message}");
        
        // UI 알림 (선택적)
        if (alert.severity >= AlertSeverity.High)
        {
            NotificationManager.Instance?.ShowNotification(message, NotificationType.Warning);
        }
    }
    
    AlertSeverity GetAlertSeverity(PerformanceAlertType alertType)
    {
        return alertType switch
        {
            PerformanceAlertType.LowFPS => AlertSeverity.High,
            PerformanceAlertType.HighMemory => AlertSeverity.Critical,
            PerformanceAlertType.HighEntityCount => AlertSeverity.Medium,
            PerformanceAlertType.FrameTimeSpikes => AlertSeverity.Medium,
            _ => AlertSeverity.Low
        };
    }
    
    void UpdateUI()
    {
        if (fpsText != null)
            fpsText.text = $"FPS: {averageFPS:F1}";
        
        if (memoryText != null)
            memoryText.text = $"메모리: {averageMemory:F1}MB";
        
        if (entityCountText != null)
            entityCountText.text = $"엔티티: {averageEntityCount:N0}";
        
        if (performanceSlider != null)
        {
            // 전체 성능 점수 (0-1)
            float performanceScore = CalculatePerformanceScore();
            performanceSlider.value = performanceScore;
        }
    }
    
    float CalculatePerformanceScore()
    {
        float fpsScore = Mathf.Clamp01(averageFPS / targetFPS);
        float memoryScore = Mathf.Clamp01(1f - (averageMemory / maxMemoryMB));
        float entityScore = Mathf.Clamp01(1f - (averageEntityCount / 100000f));
        
        return (fpsScore + memoryScore + entityScore) / 3f;
    }
    
    float CalculateVariance(float[] values)
    {
        float mean = values.Average();
        float sumSquaredDiffs = values.Sum(val => (val - mean) * (val - mean));
        return sumSquaredDiffs / values.Length;
    }
    
    // 공개 API
    public PerformanceData GetCurrentPerformanceData()
    {
        return new PerformanceData
        {
            averageFPS = averageFPS,
            averageFrameTime = averageFrameTime,
            averageMemoryMB = averageMemory,
            peakMemoryMB = peakMemory,
            entityCount = averageEntityCount,
            timestamp = Time.time
        };
    }
    
    public void SetPerformanceTargets(float fps, float memoryMB)
    {
        targetFPS = fps;
        maxMemoryMB = (int)memoryMB;
        maxFrameTime = 1000f / fps;
    }
    
    public float[] GetFrameTimeHistory() => frameTimes.ToArray();
    public float[] GetMemoryHistory() => memoryUsage.ToArray();
    public int[] GetEntityCountHistory() => entityCounts.ToArray();
}

// 성능 데이터 구조체들
public struct PerformanceData
{
    public float averageFPS;
    public float averageFrameTime;
    public float averageMemoryMB;
    public float peakMemoryMB;
    public int entityCount;
    public float timestamp;
}

public struct PerformanceAlert
{
    public PerformanceAlertType alertType;
    public string message;
    public AlertSeverity severity;
    public float timestamp;
    public PerformanceData performanceData;
}

public enum PerformanceAlertType
{
    LowFPS,
    HighMemory,
    HighEntityCount,
    FrameTimeSpikes,
    SystemOverload
}

public enum AlertSeverity
{
    Low,
    Medium,
    High,
    Critical
}
```

## 결론

이 통합 가이드는 ECS와 MonoBehaviour 시스템을 효율적으로 연결하여 데이터 중심의 자본주의 시뮬레이션 게임을 구축하는 방법을 제시합니다. 핵심은 각 시스템의 강점을 살리면서도 명확한 경계와 통신 방법을 정의하는 것입니다.

**핵심 원칙**:
- **단방향 데이터 플로우**: ECS → Event → UI
- **명령 패턴**: UI → Command → ECS
- **성능 최적화**: 배치 처리, 캐싱, 모니터링
- **확장성**: 모듈화된 구조와 플러그인 시스템

이러한 아키텍처를 통해 수십만 개의 경제 주체를 실시간으로 시뮬레이션하면서도 직관적인 UI를 제공하는 게임을 개발할 수 있습니다.

---

## 관련 문서
- [기술 아키텍처 개요](./technical-architecture.md)
- [ECS 시스템 설계](./ecs-design.md)
- [데이터 모델 명세](./data-model.md)
- [UI 시스템 설계](./ui-system.md)