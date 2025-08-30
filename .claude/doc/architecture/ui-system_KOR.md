# UI 시스템 설계 문서

[🇬🇧 English Version](./ui-system_EN.md)

## 📍 네비게이션

[↩️ 아키텍처 문서로 돌아가기](./INDEX.md) | [📚 문서 인덱스](../INDEX.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. UI 아키텍처 개요

### 1.1 설계 철학

#### 데이터 중심 UI (Data-Driven UI)
- **실시간 데이터 반영**: ECS에서 생성되는 경제 데이터를 즉시 UI에 반영
- **성능 최적화**: 대량의 숫자와 차트를 효율적으로 표시
- **사용자 체험 중심**: 복잡한 경제 데이터를 직관적으로 시각화

#### 반응형 UI (Reactive UI)
```csharp
// 데이터 변화에 자동으로 반응하는 UI
public class ReactiveEconomyPanel : MonoBehaviour
{
    [SerializeField] private EconomyDataBinding dataBinding;
    
    void Start()
    {
        // 데이터 변화 시 자동 업데이트
        dataBinding.OnEconomicDataChanged += UpdateUI;
        dataBinding.OnMarketDataChanged += UpdateCharts;
    }
    
    void UpdateUI(EconomicData data)
    {
        // UI 요소들이 자동으로 새 데이터를 반영
        gdpText.text = $"₩{data.GDP:N0}";
        inflationSlider.value = data.InflationRate;
        unemploymentChart.UpdateData(data.UnemploymentHistory);
    }
}
```

### 1.2 UI 기술 스택

#### 기본 UI 프레임워크
```yaml
Primary UI:
  - UI Toolkit (모던 UI, 성능 최적화)
  - USS 스타일시트 (CSS 유사 스타일링)
  - UXML 마크업 (HTML 유사 구조)

Legacy Support:
  - UGUI Canvas (기존 UI 호환)
  - TextMeshPro (고품질 텍스트)

Data Visualization:
  - XCharts (Unity 차트 라이브러리)
  - Custom Chart Components (특화 차트)
  - Unity Analytics Charts (선택적)
```

### 1.3 UI 레이어 구조

```
┌─────────────────────────────────────┐
│        Presentation Layer           │  ← MonoBehaviour UI Controllers
│   - UI Controllers                  │
│   - Input Handlers                  │
│   - Animation Controllers           │
└─────────────────────────────────────┘
                 ↕️
┌─────────────────────────────────────┐
│         Data Binding Layer          │  ← ECS ↔ UI 변환
│   - Data Bindings                   │
│   - Event Aggregators               │
│   - View Models                     │
└─────────────────────────────────────┘
                 ↕️
┌─────────────────────────────────────┐
│         ECS Data Layer              │  ← 순수 게임 데이터
│   - Economic Components             │
│   - Market Components               │
│   - Statistics Systems              │
└─────────────────────────────────────┘
```

## 2. 핵심 UI 컴포넌트 설계

### 2.1 대시보드 시스템

#### 메인 경제 대시보드
```csharp
// 메인 대시보드 컨트롤러
public class EconomicDashboard : MonoBehaviour
{
    [Header("Data Binding")]
    [SerializeField] private EconomyDataBinding economyBinding;
    [SerializeField] private MarketDataBinding marketBinding;
    
    [Header("UI Elements")]
    [SerializeField] private Label gdpLabel;
    [SerializeField] private Label inflationLabel;
    [SerializeField] private Label unemploymentLabel;
    [SerializeField] private ProgressBar economicHealthBar;
    [SerializeField] private LineChart economicTrendChart;
    
    [Header("Update Settings")]
    [SerializeField] private float updateInterval = 0.5f; // 0.5초마다 업데이트
    
    private float lastUpdateTime;
    
    void Update()
    {
        if (Time.time - lastUpdateTime >= updateInterval)
        {
            UpdateDashboard();
            lastUpdateTime = Time.time;
        }
    }
    
    void UpdateDashboard()
    {
        var economicData = economyBinding.GetCurrentData();
        
        // 주요 지표 업데이트
        gdpLabel.text = FormatCurrency(economicData.GDP);
        inflationLabel.text = FormatPercentage(economicData.InflationRate);
        unemploymentLabel.text = FormatPercentage(economicData.UnemploymentRate);
        
        // 경제 건강도 계산 및 표시
        float healthScore = CalculateEconomicHealth(economicData);
        economicHealthBar.value = healthScore;
        
        // 트렌드 차트 업데이트
        UpdateTrendChart(economicData);
    }
    
    float CalculateEconomicHealth(EconomicData data)
    {
        // 경제 건강도 종합 계산 (0.0 ~ 1.0)
        float gdpScore = Mathf.Clamp01(data.GDPGrowthRate / 0.05f); // 5% 성장률을 만점으로
        float inflationScore = Mathf.Clamp01(1f - data.InflationRate / 0.1f); // 10% 인플레이션을 최악으로
        float employmentScore = Mathf.Clamp01(1f - data.UnemploymentRate / 0.2f); // 20% 실업률을 최악으로
        
        return (gdpScore + inflationScore + employmentScore) / 3f;
    }
}

// 데이터 바인딩 클래스
[System.Serializable]
public class EconomyDataBinding
{
    private EconomicData cachedData;
    private float lastUpdateTime;
    private const float CACHE_DURATION = 0.1f; // 100ms 캐시
    
    public System.Action<EconomicData> OnEconomicDataChanged;
    
    public EconomicData GetCurrentData()
    {
        if (Time.time - lastUpdateTime > CACHE_DURATION)
        {
            RefreshData();
        }
        return cachedData;
    }
    
    private void RefreshData()
    {
        // ECS에서 데이터 읽어오기
        var world = World.DefaultGameObjectInjectionWorld;
        var entityManager = world.EntityManager;
        
        // 싱글톤 엔티티에서 경제 데이터 가져오기
        var query = entityManager.CreateEntityQuery(typeof(MacroEconomicsComponent));
        if (query.TryGetSingleton<MacroEconomicsComponent>(out var macroData))
        {
            var newData = new EconomicData
            {
                GDP = macroData.gdp,
                GDPGrowthRate = macroData.gdpGrowthRate,
                InflationRate = macroData.inflationRate,
                UnemploymentRate = macroData.unemploymentRate,
                InterestRate = macroData.interestRate
            };
            
            // 데이터가 변경되었으면 이벤트 발생
            if (!newData.Equals(cachedData))
            {
                cachedData = newData;
                OnEconomicDataChanged?.Invoke(cachedData);
            }
        }
        
        lastUpdateTime = Time.time;
        query.Dispose();
    }
}

// UI에서 사용할 경제 데이터 구조
[System.Serializable]
public struct EconomicData : System.IEquatable<EconomicData>
{
    public float GDP;
    public float GDPGrowthRate;
    public float InflationRate;
    public float UnemploymentRate;
    public float InterestRate;
    
    public bool Equals(EconomicData other)
    {
        return Mathf.Approximately(GDP, other.GDP) &&
               Mathf.Approximately(GDPGrowthRate, other.GDPGrowthRate) &&
               Mathf.Approximately(InflationRate, other.InflationRate) &&
               Mathf.Approximately(UnemploymentRate, other.UnemploymentRate) &&
               Mathf.Approximately(InterestRate, other.InterestRate);
    }
}
```

### 2.2 차트 및 그래프 시스템

#### 실시간 경제 지표 차트
```csharp
// 실시간 라인 차트 컴포넌트
public class RealTimeLineChart : MonoBehaviour
{
    [Header("Chart Settings")]
    [SerializeField] private int maxDataPoints = 100;
    [SerializeField] private float timeWindow = 60f; // 60초 윈도우
    [SerializeField] private Color lineColor = Color.green;
    [SerializeField] private float lineWidth = 2f;
    
    [Header("Performance")]
    [SerializeField] private bool useDataCompression = true;
    [SerializeField] private float compressionThreshold = 0.01f; // 1% 변화 미만은 압축
    
    private List<DataPoint> dataPoints = new List<DataPoint>();
    private LineRenderer lineRenderer;
    private RectTransform chartArea;
    
    struct DataPoint
    {
        public float timestamp;
        public float value;
        public bool isCompressed;
    }
    
    void Awake()
    {
        SetupChart();
    }
    
    void SetupChart()
    {
        // LineRenderer 설정
        lineRenderer = GetComponent<LineRenderer>();
        if (lineRenderer == null)
            lineRenderer = gameObject.AddComponent<LineRenderer>();
            
        lineRenderer.material = new Material(Shader.Find("Sprites/Default"));
        lineRenderer.color = lineColor;
        lineRenderer.startWidth = lineWidth;
        lineRenderer.endWidth = lineWidth;
        lineRenderer.useWorldSpace = false;
        
        // 차트 영역 설정
        chartArea = GetComponent<RectTransform>();
    }
    
    public void AddDataPoint(float value)
    {
        float currentTime = Time.time;
        
        // 데이터 압축 (성능 최적화)
        if (useDataCompression && dataPoints.Count > 0)
        {
            var lastPoint = dataPoints[dataPoints.Count - 1];
            float percentageChange = Mathf.Abs((value - lastPoint.value) / lastPoint.value);
            
            if (percentageChange < compressionThreshold)
            {
                // 변화가 작으면 마지막 포인트만 업데이트
                dataPoints[dataPoints.Count - 1] = new DataPoint
                {
                    timestamp = currentTime,
                    value = value,
                    isCompressed = true
                };
                UpdateChart();
                return;
            }
        }
        
        // 새 데이터 포인트 추가
        dataPoints.Add(new DataPoint
        {
            timestamp = currentTime,
            value = value,
            isCompressed = false
        });
        
        // 오래된 데이터 제거 (시간 윈도우 기준)
        RemoveOldDataPoints(currentTime - timeWindow);
        
        // 데이터 포인트 수 제한
        if (dataPoints.Count > maxDataPoints)
        {
            dataPoints.RemoveRange(0, dataPoints.Count - maxDataPoints);
        }
        
        UpdateChart();
    }
    
    void RemoveOldDataPoints(float cutoffTime)
    {
        int removeCount = 0;
        for (int i = 0; i < dataPoints.Count; i++)
        {
            if (dataPoints[i].timestamp < cutoffTime)
                removeCount++;
            else
                break;
        }
        
        if (removeCount > 0)
            dataPoints.RemoveRange(0, removeCount);
    }
    
    void UpdateChart()
    {
        if (dataPoints.Count < 2)
        {
            lineRenderer.positionCount = 0;
            return;
        }
        
        // 값의 범위 계산
        float minValue = float.MaxValue;
        float maxValue = float.MinValue;
        float minTime = dataPoints[0].timestamp;
        float maxTime = dataPoints[dataPoints.Count - 1].timestamp;
        
        foreach (var point in dataPoints)
        {
            minValue = Mathf.Min(minValue, point.value);
            maxValue = Mathf.Max(maxValue, point.value);
        }
        
        // 값의 범위가 너무 작으면 인위적으로 확장
        if (maxValue - minValue < 0.001f)
        {
            float center = (maxValue + minValue) / 2f;
            minValue = center - 0.0005f;
            maxValue = center + 0.0005f;
        }
        
        // LineRenderer 포지션 설정
        lineRenderer.positionCount = dataPoints.Count;
        Vector3[] positions = new Vector3[dataPoints.Count];
        
        Rect chartRect = chartArea.rect;
        
        for (int i = 0; i < dataPoints.Count; i++)
        {
            var point = dataPoints[i];
            
            // 정규화된 좌표 계산
            float normalizedX = (point.timestamp - minTime) / (maxTime - minTime);
            float normalizedY = (point.value - minValue) / (maxValue - minValue);
            
            // 차트 영역 좌표로 변환
            positions[i] = new Vector3(
                chartRect.xMin + normalizedX * chartRect.width,
                chartRect.yMin + normalizedY * chartRect.height,
                0f
            );
        }
        
        lineRenderer.SetPositions(positions);
    }
    
    // 차트 스타일 동적 변경
    public void SetChartStyle(Color color, float width, Material material = null)
    {
        lineColor = color;
        lineWidth = width;
        
        lineRenderer.color = color;
        lineRenderer.startWidth = width;
        lineRenderer.endWidth = width;
        
        if (material != null)
            lineRenderer.material = material;
    }
}
```

#### 포트폴리오 파이 차트
```csharp
// 포트폴리오 구성을 보여주는 파이 차트
public class PortfolioPieChart : MonoBehaviour
{
    [Header("Chart Data")]
    [SerializeField] private PortfolioData portfolioData;
    
    [Header("Visual Settings")]
    [SerializeField] private Material pieMaterial;
    [SerializeField] private float chartRadius = 100f;
    [SerializeField] private float holeRadius = 30f; // 도넛 차트용
    [SerializeField] private bool showLabels = true;
    [SerializeField] private Font labelFont;
    
    private List<PieSlice> pieSlices = new List<PieSlice>();
    private Canvas chartCanvas;
    
    [System.Serializable]
    public struct PortfolioItem
    {
        public string name;
        public float value;
        public Color color;
        public float percentage;
    }
    
    struct PieSlice
    {
        public PortfolioItem item;
        public float startAngle;
        public float endAngle;
        public GameObject sliceObject;
        public Text labelText;
    }
    
    void Start()
    {
        SetupChart();
        UpdateChart();
    }
    
    void SetupChart()
    {
        chartCanvas = GetComponentInChildren<Canvas>();
        if (chartCanvas == null)
        {
            GameObject canvasObj = new GameObject("ChartCanvas");
            canvasObj.transform.SetParent(transform);
            chartCanvas = canvasObj.AddComponent<Canvas>();
            chartCanvas.renderMode = RenderMode.WorldSpace;
        }
    }
    
    public void UpdateChart()
    {
        // 기존 슬라이스 제거
        ClearChart();
        
        if (portfolioData == null || portfolioData.items.Length == 0)
            return;
        
        // 총합 계산
        float totalValue = 0f;
        foreach (var item in portfolioData.items)
        {
            totalValue += item.value;
        }
        
        if (totalValue <= 0f) return;
        
        // 각 항목의 각도 계산
        float currentAngle = 0f;
        
        for (int i = 0; i < portfolioData.items.Length; i++)
        {
            var item = portfolioData.items[i];
            item.percentage = item.value / totalValue;
            float sliceAngle = item.percentage * 360f;
            
            // 파이 슬라이스 생성
            CreatePieSlice(item, currentAngle, currentAngle + sliceAngle, i);
            
            currentAngle += sliceAngle;
        }
    }
    
    void CreatePieSlice(PortfolioItem item, float startAngle, float endAngle, int index)
    {
        // 슬라이스 오브젝트 생성
        GameObject sliceObj = new GameObject($"Slice_{item.name}");
        sliceObj.transform.SetParent(chartCanvas.transform);
        
        // 메시 렌더러와 필터 추가
        MeshRenderer meshRenderer = sliceObj.AddComponent<MeshRenderer>();
        MeshFilter meshFilter = sliceObj.AddComponent<MeshFilter>();
        
        // 슬라이스 메시 생성
        Mesh sliceMesh = CreateSliceMesh(startAngle, endAngle);
        meshFilter.mesh = sliceMesh;
        
        // 머티리얼 설정
        Material sliceMaterial = new Material(pieMaterial);
        sliceMaterial.color = item.color;
        meshRenderer.material = sliceMaterial;
        
        // 호버 효과를 위한 콜라이더 추가
        MeshCollider collider = sliceObj.AddComponent<MeshCollider>();
        collider.mesh = sliceMesh;
        
        // 인터랙션 컴포넌트 추가
        SliceInteraction interaction = sliceObj.AddComponent<SliceInteraction>();
        interaction.Initialize(item, this);
        
        // 라벨 생성
        Text labelText = null;
        if (showLabels)
        {
            labelText = CreateSliceLabel(item, startAngle, endAngle);
        }
        
        // 슬라이스 정보 저장
        pieSlices.Add(new PieSlice
        {
            item = item,
            startAngle = startAngle,
            endAngle = endAngle,
            sliceObject = sliceObj,
            labelText = labelText
        });
    }
    
    Mesh CreateSliceMesh(float startAngle, float endAngle)
    {
        Mesh mesh = new Mesh();
        
        // 정점과 삼각형 계산
        int segments = Mathf.Max(3, Mathf.RoundToInt((endAngle - startAngle) / 10f)); // 10도당 1세그먼트
        int vertexCount = (segments + 1) * 2; // 내부 원과 외부 원
        
        Vector3[] vertices = new Vector3[vertexCount];
        Vector2[] uvs = new Vector2[vertexCount];
        int[] triangles = new int[segments * 6]; // 각 세그먼트마다 2개 삼각형
        
        // 정점 생성
        for (int i = 0; i <= segments; i++)
        {
            float angle = Mathf.Lerp(startAngle, endAngle, (float)i / segments) * Mathf.Deg2Rad;
            float cos = Mathf.Cos(angle);
            float sin = Mathf.Sin(angle);
            
            // 외부 정점
            vertices[i * 2] = new Vector3(cos * chartRadius, sin * chartRadius, 0f);
            uvs[i * 2] = new Vector2(cos * 0.5f + 0.5f, sin * 0.5f + 0.5f);
            
            // 내부 정점 (도넛 차트용)
            vertices[i * 2 + 1] = new Vector3(cos * holeRadius, sin * holeRadius, 0f);
            uvs[i * 2 + 1] = new Vector2(cos * 0.2f + 0.5f, sin * 0.2f + 0.5f);
        }
        
        // 삼각형 인덱스 생성
        int triangleIndex = 0;
        for (int i = 0; i < segments; i++)
        {
            int current = i * 2;
            int next = (i + 1) * 2;
            
            // 첫 번째 삼각형 (외부-내부-외부)
            triangles[triangleIndex++] = current;
            triangles[triangleIndex++] = current + 1;
            triangles[triangleIndex++] = next;
            
            // 두 번째 삼각형 (내부-다음내부-다음외부)  
            triangles[triangleIndex++] = current + 1;
            triangles[triangleIndex++] = next + 1;
            triangles[triangleIndex++] = next;
        }
        
        mesh.vertices = vertices;
        mesh.uv = uvs;
        mesh.triangles = triangles;
        mesh.RecalculateNormals();
        
        return mesh;
    }
    
    Text CreateSliceLabel(PortfolioItem item, float startAngle, float endAngle)
    {
        GameObject labelObj = new GameObject($"Label_{item.name}");
        labelObj.transform.SetParent(chartCanvas.transform);
        
        Text labelText = labelObj.AddComponent<Text>();
        labelText.font = labelFont;
        labelText.text = $"{item.name}\n{item.percentage:P1}";
        labelText.fontSize = 12;
        labelText.color = Color.white;
        labelText.alignment = TextAnchor.MiddleCenter;
        
        // 라벨 위치 계산 (슬라이스 중앙)
        float midAngle = (startAngle + endAngle) / 2f * Mathf.Deg2Rad;
        float labelRadius = (chartRadius + holeRadius) / 2f;
        
        Vector3 labelPosition = new Vector3(
            Mathf.Cos(midAngle) * labelRadius,
            Mathf.Sin(midAngle) * labelRadius,
            -0.1f // 약간 앞에 배치
        );
        
        labelObj.transform.localPosition = labelPosition;
        
        return labelText;
    }
    
    void ClearChart()
    {
        foreach (var slice in pieSlices)
        {
            if (slice.sliceObject != null)
                DestroyImmediate(slice.sliceObject);
            if (slice.labelText != null)
                DestroyImmediate(slice.labelText.gameObject);
        }
        pieSlices.Clear();
    }
}

// 슬라이스 인터랙션 처리
public class SliceInteraction : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IPointerClickHandler
{
    private PortfolioPieChart.PortfolioItem item;
    private PortfolioPieChart parentChart;
    private Vector3 originalScale;
    private bool isHovered = false;
    
    public void Initialize(PortfolioPieChart.PortfolioItem portfolioItem, PortfolioPieChart chart)
    {
        item = portfolioItem;
        parentChart = chart;
        originalScale = transform.localScale;
    }
    
    public void OnPointerEnter(PointerEventData eventData)
    {
        isHovered = true;
        // 호버 시 약간 확대
        transform.localScale = originalScale * 1.1f;
        
        // 툴팁 표시
        ShowTooltip();
    }
    
    public void OnPointerExit(PointerEventData eventData)
    {
        isHovered = false;
        transform.localScale = originalScale;
        
        // 툴팁 숨기기
        HideTooltip();
    }
    
    public void OnPointerClick(PointerEventData eventData)
    {
        // 슬라이스 클릭 시 상세 정보 표시
        ShowDetailedView();
    }
    
    void ShowTooltip()
    {
        // 툴팁 UI 표시 구현
        TooltipManager.Instance?.ShowTooltip($"{item.name}: ₩{item.value:N0} ({item.percentage:P1})");
    }
    
    void HideTooltip()
    {
        TooltipManager.Instance?.HideTooltip();
    }
    
    void ShowDetailedView()
    {
        // 상세 정보 패널 열기
        DetailedViewManager.Instance?.ShowPortfolioItemDetails(item);
    }
}
```

### 2.3 데이터 테이블 시스템

#### 가상 스크롤링 테이블
```csharp
// 대량의 데이터를 효율적으로 표시하는 가상 스크롤링 테이블
public class VirtualizedDataTable : MonoBehaviour, IScrollHandler
{
    [Header("Table Settings")]
    [SerializeField] private int visibleRowCount = 20;
    [SerializeField] private float rowHeight = 30f;
    [SerializeField] private ScrollRect scrollRect;
    [SerializeField] private RectTransform content;
    [SerializeField] private RectTransform viewport;
    
    [Header("Row Prefab")]
    [SerializeField] private GameObject rowPrefab;
    
    private List<TableRowData> allData = new List<TableRowData>();
    private List<GameObject> visibleRows = new List<GameObject>();
    private ObjectPool<GameObject> rowPool;
    
    private int firstVisibleIndex = 0;
    private int lastVisibleIndex = 0;
    
    public struct TableRowData
    {
        public string companyName;
        public float stockPrice;
        public float priceChange;
        public float volume;
        public float marketCap;
        public string industry;
    }
    
    void Awake()
    {
        SetupVirtualization();
        InitializeRowPool();
    }
    
    void SetupVirtualization()
    {
        if (scrollRect == null)
            scrollRect = GetComponent<ScrollRect>();
            
        // 스크롤 이벤트 리스너 등록
        scrollRect.onValueChanged.AddListener(OnScrollValueChanged);
        
        // 컨텐트 높이 설정
        float totalHeight = allData.Count * rowHeight;
        content.sizeDelta = new Vector2(content.sizeDelta.x, totalHeight);
    }
    
    void InitializeRowPool()
    {
        rowPool = new ObjectPool<GameObject>(
            () => Instantiate(rowPrefab, content),
            row => row.SetActive(true),
            row => row.SetActive(false),
            row => Destroy(row),
            defaultCapacity: visibleRowCount + 5, // 약간의 버퍼
            maxSize: visibleRowCount * 2
        );
    }
    
    public void SetData(List<TableRowData> data)
    {
        allData = data;
        
        // 컨텐트 높이 업데이트
        float totalHeight = allData.Count * rowHeight;
        content.sizeDelta = new Vector2(content.sizeDelta.x, totalHeight);
        
        // 가시 영역 업데이트
        UpdateVisibleRows();
    }
    
    public void AddData(TableRowData newRow)
    {
        allData.Add(newRow);
        
        // 컨텐트 높이 업데이트
        float totalHeight = allData.Count * rowHeight;
        content.sizeDelta = new Vector2(content.sizeDelta.x, totalHeight);
        
        // 맨 아래로 스크롤된 상태면 새 데이터 표시
        if (IsScrolledToBottom())
        {
            UpdateVisibleRows();
            ScrollToBottom();
        }
    }
    
    void OnScrollValueChanged(Vector2 scrollPosition)
    {
        UpdateVisibleRows();
    }
    
    void UpdateVisibleRows()
    {
        if (allData.Count == 0) return;
        
        // 현재 스크롤 위치에서 보이는 행의 인덱스 계산
        float scrollY = content.anchoredPosition.y;
        int newFirstIndex = Mathf.Max(0, Mathf.FloorToInt(scrollY / rowHeight));
        int newLastIndex = Mathf.Min(allData.Count - 1, newFirstIndex + visibleRowCount);
        
        // 인덱스가 변하지 않았으면 리턴
        if (newFirstIndex == firstVisibleIndex && newLastIndex == lastVisibleIndex)
            return;
        
        // 기존 행들을 풀에 반환
        foreach (var row in visibleRows)
        {
            rowPool.Release(row);
        }
        visibleRows.Clear();
        
        // 새로운 가시 행들 생성
        for (int i = newFirstIndex; i <= newLastIndex; i++)
        {
            GameObject row = rowPool.Get();
            UpdateRowData(row, allData[i], i);
            PositionRow(row, i);
            visibleRows.Add(row);
        }
        
        firstVisibleIndex = newFirstIndex;
        lastVisibleIndex = newLastIndex;
    }
    
    void UpdateRowData(GameObject row, TableRowData data, int index)
    {
        var rowComponent = row.GetComponent<TableRow>();
        if (rowComponent != null)
        {
            rowComponent.SetData(data, index);
        }
        else
        {
            // 레거시 지원: 직접 자식 요소들 업데이트
            var texts = row.GetComponentsInChildren<Text>();
            if (texts.Length >= 5)
            {
                texts[0].text = data.companyName;
                texts[1].text = $"₩{data.stockPrice:N0}";
                texts[2].text = FormatPriceChange(data.priceChange);
                texts[3].text = $"{data.volume:N0}";
                texts[4].text = $"₩{data.marketCap:N0}";
            }
        }
        
        // 홀짝 행 색상 구분
        var image = row.GetComponent<Image>();
        if (image != null)
        {
            image.color = index % 2 == 0 ? Color.white : new Color(0.95f, 0.95f, 0.95f, 1f);
        }
    }
    
    void PositionRow(GameObject row, int index)
    {
        RectTransform rowRect = row.GetComponent<RectTransform>();
        rowRect.anchoredPosition = new Vector2(0, -index * rowHeight);
        rowRect.sizeDelta = new Vector2(content.sizeDelta.x, rowHeight);
    }
    
    string FormatPriceChange(float change)
    {
        string sign = change >= 0 ? "+" : "";
        return $"{sign}{change:F2}%";
    }
    
    bool IsScrolledToBottom()
    {
        return scrollRect.verticalNormalizedPosition <= 0.01f;
    }
    
    void ScrollToBottom()
    {
        scrollRect.verticalNormalizedPosition = 0f;
    }
    
    // IScrollHandler 구현
    public void OnScroll(PointerEventData eventData)
    {
        UpdateVisibleRows();
    }
}

// 테이블 행 컴포넌트
public class TableRow : MonoBehaviour
{
    [SerializeField] private Text companyNameText;
    [SerializeField] private Text stockPriceText;
    [SerializeField] private Text priceChangeText;
    [SerializeField] private Text volumeText;
    [SerializeField] private Text marketCapText;
    [SerializeField] private Button detailButton;
    
    private VirtualizedDataTable.TableRowData currentData;
    private int rowIndex;
    
    void Awake()
    {
        if (detailButton != null)
        {
            detailButton.onClick.AddListener(OnDetailButtonClick);
        }
    }
    
    public void SetData(VirtualizedDataTable.TableRowData data, int index)
    {
        currentData = data;
        rowIndex = index;
        
        // UI 업데이트
        if (companyNameText != null) companyNameText.text = data.companyName;
        if (stockPriceText != null) stockPriceText.text = $"₩{data.stockPrice:N0}";
        if (priceChangeText != null)
        {
            priceChangeText.text = FormatPriceChange(data.priceChange);
            priceChangeText.color = data.priceChange >= 0 ? Color.green : Color.red;
        }
        if (volumeText != null) volumeText.text = $"{data.volume:N0}";
        if (marketCapText != null) marketCapText.text = $"₩{data.marketCap:N0}";
    }
    
    void OnDetailButtonClick()
    {
        // 상세 정보 화면으로 이동
        CompanyDetailManager.Instance?.ShowCompanyDetail(currentData.companyName);
    }
    
    string FormatPriceChange(float change)
    {
        string sign = change >= 0 ? "▲" : "▼";
        return $"{sign} {Mathf.Abs(change):F2}%";
    }
}
```

## 3. 성능 최적화 전략

### 3.1 UI 업데이트 최적화

#### 배치 업데이트 시스템
```csharp
// UI 업데이트를 배치 처리하여 성능 최적화
public class UIUpdateBatcher : MonoBehaviour
{
    private Dictionary<string, List<System.Action>> updateQueues = new Dictionary<string, List<System.Action>>();
    private Dictionary<string, float> lastUpdateTimes = new Dictionary<string, float>();
    private Dictionary<string, float> updateIntervals = new Dictionary<string, float>();
    
    public static UIUpdateBatcher Instance { get; private set; }
    
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
        // 기본 업데이트 간격 설정
        SetUpdateInterval("economy", 0.5f);    // 경제 지표: 0.5초
        SetUpdateInterval("stocks", 0.1f);     // 주식 가격: 0.1초
        SetUpdateInterval("charts", 1.0f);     // 차트: 1초
        SetUpdateInterval("statistics", 2.0f); // 통계: 2초
    }
    
    void Update()
    {
        ProcessUpdateQueues();
    }
    
    public void SetUpdateInterval(string category, float interval)
    {
        updateIntervals[category] = interval;
        if (!lastUpdateTimes.ContainsKey(category))
            lastUpdateTimes[category] = 0f;
        if (!updateQueues.ContainsKey(category))
            updateQueues[category] = new List<System.Action>();
    }
    
    public void QueueUpdate(string category, System.Action updateAction)
    {
        if (!updateQueues.ContainsKey(category))
        {
            Debug.LogWarning($"Update category '{category}' not registered. Adding with default interval.");
            SetUpdateInterval(category, 1.0f);
        }
        
        updateQueues[category].Add(updateAction);
    }
    
    void ProcessUpdateQueues()
    {
        float currentTime = Time.time;
        
        foreach (var category in updateQueues.Keys.ToList())
        {
            if (updateQueues[category].Count == 0) continue;
            
            float lastUpdate = lastUpdateTimes[category];
            float interval = updateIntervals[category];
            
            if (currentTime - lastUpdate >= interval)
            {
                // 이 카테고리의 모든 업데이트 실행
                foreach (var updateAction in updateQueues[category])
                {
                    try
                    {
                        updateAction?.Invoke();
                    }
                    catch (System.Exception e)
                    {
                        Debug.LogError($"Error in UI update for category '{category}': {e.Message}");
                    }
                }
                
                // 큐 비우기 및 시간 업데이트
                updateQueues[category].Clear();
                lastUpdateTimes[category] = currentTime;
            }
        }
    }
    
    // 우선순위 업데이트 (즉시 실행)
    public void ForceUpdate(string category)
    {
        if (updateQueues.ContainsKey(category) && updateQueues[category].Count > 0)
        {
            foreach (var updateAction in updateQueues[category])
            {
                updateAction?.Invoke();
            }
            updateQueues[category].Clear();
            lastUpdateTimes[category] = Time.time;
        }
    }
}

// 사용 예시
public class EconomicIndicatorPanel : MonoBehaviour
{
    [SerializeField] private Text gdpText;
    [SerializeField] private Text inflationText;
    
    void Update()
    {
        // 직접 업데이트하지 않고 배치 시스템에 큐잉
        UIUpdateBatcher.Instance.QueueUpdate("economy", UpdateEconomicIndicators);
    }
    
    void UpdateEconomicIndicators()
    {
        var economicData = EconomyDataBinding.GetCurrentData();
        gdpText.text = $"GDP: ₩{economicData.GDP:N0}";
        inflationText.text = $"인플레이션: {economicData.InflationRate:P2}";
    }
}
```

### 3.2 메모리 및 GC 최적화

#### 오브젝트 풀링 시스템
```csharp
// UI 요소를 위한 오브젝트 풀
public class UIObjectPool<T> where T : Component
{
    private Stack<T> pool = new Stack<T>();
    private T prefab;
    private Transform parentTransform;
    private System.Func<T> createFunction;
    private System.Action<T> onGet;
    private System.Action<T> onRelease;
    
    public UIObjectPool(T prefab, Transform parent, int initialSize = 10)
    {
        this.prefab = prefab;
        this.parentTransform = parent;
        
        // 기본 생성/해제 함수
        createFunction = () => Object.Instantiate(prefab, parentTransform);
        onGet = (item) => item.gameObject.SetActive(true);
        onRelease = (item) => item.gameObject.SetActive(false);
        
        // 초기 풀 생성
        for (int i = 0; i < initialSize; i++)
        {
            T item = createFunction();
            onRelease(item);
            pool.Push(item);
        }
    }
    
    public T Get()
    {
        T item;
        if (pool.Count > 0)
        {
            item = pool.Pop();
        }
        else
        {
            item = createFunction();
        }
        
        onGet(item);
        return item;
    }
    
    public void Release(T item)
    {
        if (item == null) return;
        
        onRelease(item);
        pool.Push(item);
    }
    
    public void Clear()
    {
        while (pool.Count > 0)
        {
            T item = pool.Pop();
            if (item != null)
                Object.Destroy(item.gameObject);
        }
    }
}

// 알림 메시지 관리자
public class NotificationManager : MonoBehaviour
{
    [SerializeField] private NotificationItem notificationPrefab;
    [SerializeField] private Transform notificationParent;
    [SerializeField] private int maxNotifications = 10;
    [SerializeField] private float notificationDuration = 3f;
    
    private UIObjectPool<NotificationItem> notificationPool;
    private List<NotificationItem> activeNotifications = new List<NotificationItem>();
    
    void Awake()
    {
        notificationPool = new UIObjectPool<NotificationItem>(notificationPrefab, notificationParent);
    }
    
    public void ShowNotification(string message, NotificationType type = NotificationType.Info)
    {
        // 최대 알림 수 제한
        if (activeNotifications.Count >= maxNotifications)
        {
            RemoveOldestNotification();
        }
        
        NotificationItem notification = notificationPool.Get();
        notification.SetContent(message, type);
        notification.transform.SetAsLastSibling(); // 맨 위에 표시
        
        activeNotifications.Add(notification);
        
        // 자동 제거 코루틴 시작
        StartCoroutine(RemoveNotificationAfterDelay(notification, notificationDuration));
    }
    
    System.Collections.IEnumerator RemoveNotificationAfterDelay(NotificationItem notification, float delay)
    {
        yield return new WaitForSeconds(delay);
        
        if (notification != null && activeNotifications.Contains(notification))
        {
            RemoveNotification(notification);
        }
    }
    
    void RemoveNotification(NotificationItem notification)
    {
        if (activeNotifications.Contains(notification))
        {
            activeNotifications.Remove(notification);
            notificationPool.Release(notification);
        }
    }
    
    void RemoveOldestNotification()
    {
        if (activeNotifications.Count > 0)
        {
            RemoveNotification(activeNotifications[0]);
        }
    }
}

public enum NotificationType
{
    Info,
    Warning,
    Error,
    Success
}
```

## 다음 문서
- [시스템 통합 가이드](./integration-guide.md)