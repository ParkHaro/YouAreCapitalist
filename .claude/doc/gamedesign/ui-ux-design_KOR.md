---
category: gamedesign
tags: [ui, ux, 디자인, 인터페이스, 대시보드, 모바일, 접근성]
related: [capitalism-game-design-doc_KOR.md, progression-system_KOR.md, economy-balance-model_KOR.md]
parent: INDEX_KOR.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# UI/UX 디자인

[🇺🇸 English Version](./ui-ux-design.md)

## 📍 내비게이션

[↩️ 게임 디자인으로 돌아가기](./INDEX_KOR.md) | [📚 문서 색인](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 디자인 철학

### 1.1 핵심 원칙

#### 금융 데이터 명확성
- **정보 계층**: 가장 중요한 데이터를 눈에 띄게 표시
- **실시간 업데이트**: 변화하는 값에 대한 부드러운 전환
- **맥락적 깊이**: 개요에서 세부사항까지 점진적 공개
- **전문적 미학**: 깔끔하고 금융 업계에서 영감을 받은 디자인

#### 접근성과 포용성
- **범용 디자인**: 다양한 능력의 사용자가 사용 가능
- **색맹 친화적**: 색상 의존성 없이 의미 전달
- **확장 가능한 텍스트**: 다양한 글꼴 크기 지원
- **운동 접근성**: 큰 터치 대상, 제스처 대안

#### 크로스 플랫폼 일관성
- **반응형 디자인**: 기기 간 원활한 경험
- **플랫폼 규칙**: iOS/Android/PC 인터페이스 가이드라인 준수
- **성능 최적화**: 모바일 기기에서 60 FPS
- **터치 우선 디자인**: 손가락 내비게이션에 최적화, 마우스/키보드 지원

### 1.2 사용자 경험 기둥

#### 점진적 복잡성
- **안내된 발견**: 플레이어가 발전함에 따라 기능 공개
- **맥락적 도움**: 적시에 제공되는 정보와 튜토리얼
- **간소화된 온보딩**: 신규 사용자를 위한 최소한의 마찰
- **전문가 모드**: 숙련된 플레이어를 위한 고급 기능

#### 감정적 참여
- **성취 축하**: 마일스톤에 대한 만족스러운 피드백
- **진행 시각화**: 명확한 발전 지표
- **개성 표현**: 커스터마이징 가능한 인터페이스 요소
- **사회적 인정**: 공유 및 비교 기능

## 2. 정보 아키텍처

### 2.1 내비게이션 구조

#### 주요 내비게이션 계층
```
메인 대시보드
├── 포트폴리오 개요
│   ├── 자산 배분
│   ├── 성과 지표
│   └── 보유 세부사항
├── 시장 조사
│   ├── 시장 지수
│   ├── 증권 분석
│   └── 경제 지표
├── 거래 센터
│   ├── 주문 관리
│   ├── 거래 내역
│   └── 관심 목록
├── 자동화 허브
│   ├── 활성 전략
│   ├── 전략 빌더
│   └── 성과 분석
├── 회사 및 경제
│   ├── 회사 브라우저
│   ├── 경제 개요
│   └── 시뮬레이션 제어
└── 설정 및 프로필
    ├── 게임 설정
    ├── 업적 갤러리
    └── 튜토리얼 센터
```

#### 탭 내비게이션 시스템
```csharp
[System.Serializable]
public struct TabNavigationConfig
{
    [Header("탭 레이아웃")]
    public TabPosition tabPosition;          // 하단, 상단, 왼쪽, 오른쪽
    public int maxVisibleTabs;              // 모바일에서 최대 5개 탭
    public bool enableTabScrolling;         // 오버플로우를 위한 가로 스크롤
    
    [Header("탭 동작")]
    public float tabSwitchAnimation;        // 0.3초 전환 시간
    public TabSwitchMode switchMode;        // 슬라이드, 페이드, 스케일
    public bool enableSwipeGestures;        // 터치/트랙패드 스와이프 내비게이션
    
    [Header("배지 시스템")]
    public bool enableNotificationBadges;   // 알림을 위한 빨간 점
    public BadgeStyle badgeStyle;          // 점, 숫자, 아이콘
    public Color urgentBadgeColor;         // 긴급 알림을 위한 빨간색
}

public enum TabPosition
{
    BottomMobile,    // 모바일을 위한 하단 탭 (엄지손가락 친화적)
    TopDesktop,      // 데스크톱을 위한 상단 탭
    LeftSidebar,     // 데스크톱을 위한 사이드바 내비게이션
    ContextualFloat  // 플로팅 맥락적 탭
}
```

### 2.2 정보 밀도 관리

#### 화면 공간 최적화
```csharp
[System.Serializable]
public struct ScreenDensityConfig
{
    [Header("모바일 레이아웃 (320-768px)")]
    public int maxCardsPerRow_Mobile;       // 최대 1-2개 카드
    public float cardMinHeight_Mobile;      // 최소 120px
    public float margins_Mobile;            // 16px 여백
    
    [Header("태블릿 레이아웃 (768-1024px)")]
    public int maxCardsPerRow_Tablet;       // 2-3개 카드
    public float cardMinHeight_Tablet;      // 최소 140px
    public float margins_Tablet;            // 24px 여백
    
    [Header("데스크톱 레이아웃 (1024px+)")]
    public int maxCardsPerRow_Desktop;      // 3-4개 카드
    public float cardMinHeight_Desktop;     // 최소 160px
    public float margins_Desktop;           // 32px 여백
    
    [Header("정보 우선순위")]
    public InfoPriority[] informationLayers;
    public bool enableDetailCollapse;       // 공간이 제한될 때 세부사항 숨김
}

public enum InfoPriority
{
    Critical,        // 항상 표시 (현재 순자산)
    Important,       // 가장 작은 화면에서만 숨김 (포트폴리오 변화)
    Contextual,      // 관련있을 때 표시 (섹터 분석)
    Optional         // 특별히 요청되지 않는 한 숨김 (상세 지표)
}
```

## 3. 메인 대시보드 디자인

### 3.1 부 개요 섹션

#### 순자산 표시
```csharp
[System.Serializable]
public struct WealthDisplayConfig
{
    [Header("주요 지표")]
    public WealthFormat primaryFormat;       // 통화, 과학적, 백분율
    public bool enableAnimatedCounting;     // 변화에 대한 카운트업 애니메이션
    public float countAnimationDuration;    // 2.0초 애니메이션 시간
    
    [Header("트렌드 시각화")]
    public TrendDisplayMode trendMode;      // 화살표, 그래프, 색상, 숫자
    public Color positiveColor;             // 녹색 #00C851
    public Color negativeColor;             // 빨간색 #FF4444
    public Color neutralColor;              // 회색 #999999
    
    [Header("비교 맥락")]
    public bool showPercentileRank;         // "플레이어 상위 15%"
    public bool showPeerComparison;         // 유사한 플레이어와 비교
    public bool showHistoricalBest;        // "역대 최고의 85%"
}

public enum WealthFormat
{
    Currency,        // $1,234,567
    Abbreviated,     // $1.23M
    Scientific,      // 1.23e6
    Percentage       // 이달 +15.2%
}

public enum TrendDisplayMode
{
    ArrowIcon,       // ↗️ ↘️ 화살표
    MiniGraph,       // 스파크라인 차트
    ColorBackground, // 녹색/빨간색 배경
    NumericChange    // +$125,450 (+12.5%)
}
```

#### 포트폴리오 배분 시각화
```csharp
[System.Serializable]
public struct AllocationVisualizationConfig
{
    [Header("차트 유형")]
    public ChartType primaryChart;          // 파이, 도넛, 트리맵, 막대
    public ChartType mobileChart;           // 모바일용 간소화
    public bool enableInteractiveChart;    // 탭하여 드릴다운
    
    [Header("색상 체계")]
    public ColorPalette palette;           // 자산 클래스 색상
    public bool enableColorBlindSupport;   // 패턴 + 색상
    public float saturationLevel;          // 전문적 외관을 위한 0.8
    
    [Header("세부 수준")]
    public int maxVisibleSlices;          // "기타" 전 8개 슬라이스
    public float minimumSlicePercent;     // 슬라이스 표시 최소 2%
    public bool enablePercentageLabels;   // 슬라이스에 % 표시
}

public enum ChartType
{
    DonutChart,      // 중앙 값이 있는 현대적 도넛
    PieChart,        // 전통적인 파이 차트
    TreemapChart,    // 배분을 위한 사각형 크기
    HorizontalBar,   // 수평 막대 차트
    StackedBar       // 단일 누적 막대
}
```

### 3.2 성과 지표 패널

#### 핵심 성과 지표
```csharp
[System.Serializable]
public struct PerformanceMetricsConfig
{
    [Header("시간 기간")]
    public TimePeriod[] availablePeriods;   // 1일, 1주, 1달, 3달, 1년, 전체
    public TimePeriod defaultPeriod;        // 1달 기본값
    public bool enableCustomRange;          // 사용자 정의 범위용 날짜 선택기
    
    [Header("지표 표시")]
    public MetricCard[] primaryMetrics;     // ROI, 샤프, 최대 하락폭
    public MetricCard[] secondaryMetrics;   // 베타, 알파, 변동성
    public int maxMetricsOnMobile;         // 최대 4개 지표
    
    [Header("벤치마킹")]
    public string[] benchmarkIndices;      // S&P 500, NASDAQ 등
    public bool enableBenchmarkComparison; // 벤치마크 대비 표시
    public bool enablePeerComparison;      // 다른 플레이어 대비 표시
}

public struct MetricCard
{
    public string metricName;              // "연간 수익률"
    public string displayFormat;           // "+12.5%"
    public MetricTrend trend;              // 상승, 하락, 안정
    public string helpText;                // 툴팁 설명
    public bool isGoodWhenHigh;           // ROI는 true, 변동성은 false
}
```

#### 성과 차트 컴포넌트
```csharp
[System.Serializable]
public struct PerformanceChartConfig
{
    [Header("차트 스타일")]
    public ChartStyle chartStyle;          // 선, 캔들스틱, 영역
    public LineStyle lineStyle;            // 실선, 점선, 부드러운
    public bool enableDataPoints;          // 선에 점 표시
    
    [Header("대화형 기능")]
    public bool enableZoomGestures;        // 핀치하여 확대
    public bool enablePanGestures;         // 팬하여 스크롤
    public bool enableCrosshair;           // 탭/호버시 십자선
    public bool enableValueTooltip;        // 지점에서 값 표시
    
    [Header("비교 오버레이")]
    public bool enableBenchmarkOverlay;    // 벤치마크 선 표시
    public bool enableMultipleAssets;      // 여러 보유 자산 비교
    public int maxComparisonLines;         // 최대 3개 선
    
    [Header("주석")]
    public bool enableTradeMarkers;        // 매수/매도 지점 표시
    public bool enableEventMarkers;        // 경제 이벤트 표시
    public bool enableTrendLines;          // 사용자 그린 트렌드 선
}
```

### 3.3 시장 개요 섹션

#### 경제 지표 대시보드
```csharp
[System.Serializable]
public struct EconomicIndicatorsConfig
{
    [Header("주요 지표")]
    public IndicatorWidget[] primaryIndicators; // GDP, 인플레이션, 실업률
    public IndicatorWidget[] secondaryIndicators; // 금리 등
    public UpdateFrequency updateFrequency;     // 실시간, 시간별, 일별
    
    [Header("시각화")]
    public IndicatorStyle displayStyle;        // 게이지, 숫자, 그래프
    public bool enableTrendArrows;             // 상승/하락 화살표
    public bool enableHistoricalContext;      // "6개월 최고치"
    
    [Header("알림")]
    public bool enableThresholdAlerts;         // 중요한 변화시 알림
    public float significantChangeThreshold;   // 0.5% 변화가 알림 유발
    public AlertStyle alertStyle;              // 배너, 토스트, 배지
}

public struct IndicatorWidget
{
    public string indicatorName;           // "GDP 성장률"
    public float currentValue;             // 2.3
    public string units;                   // "%"
    public float changeFromPrevious;       // +0.2
    public IndicatorImportance importance; // 높음, 중간, 낮음
}
```

## 4. 포트폴리오 관리 인터페이스

### 4.1 보유 목록 디자인

#### 자산 목록 레이아웃
```csharp
[System.Serializable]
public struct HoldingsListConfig
{
    [Header("목록 스타일")]
    public ListViewMode viewMode;              // 카드, 테이블, 컴팩트
    public SortOption[] availableSortOptions;  // 가치, %, 이름, 섹터별
    public SortOption defaultSort;             // 포트폴리오 가중치별
    
    [Header("카드 디자인")]
    public CardLayout cardLayout;              // 수평, 수직, 격자
    public bool enableSwipeActions;            // 빠른 액션을 위한 스와이프
    public SwipeAction[] leftSwipeActions;     // 추가 매수, 매도, 분석
    public SwipeAction[] rightSwipeActions;    // 제거, 편집, 정보
    
    [Header("정보 밀도")]
    public HoldingInfoLevel detailLevel;       // 최소, 표준, 상세
    public bool enableExpandableCards;        // 탭하여 세부사항 확장
    public InfoField[] visibleFields;         // 표시할 데이터
}

public enum ListViewMode
{
    CardView,        // 카드 기반 레이아웃 (모바일 친화적)
    TableView,       // 전통적인 테이블 (데스크톱)
    CompactList,     // 조밀한 목록 보기
    GridView         // 타일 격자
}

public struct InfoField
{
    public string fieldName;        // "현재 가치"
    public string displayFormat;    // "$12,345"
    public FieldImportance priority; // 항상, 데스크톱, 선택사항
    public bool enableTrendIcon;    // 트렌드 화살표 표시
}
```

#### 개별 보유 세부사항
```csharp
[System.Serializable]
public struct HoldingDetailConfig
{
    [Header("개요 섹션")]
    public bool showCurrentPrice;             // 실시간 가격
    public bool showDayChange;                // 오늘의 변화
    public bool showTotalReturn;              // 구매 이후
    public bool showUnrealizedGainLoss;       // 손익
    
    [Header("성과 차트")]
    public bool enablePriceChart;             // 가격 내역 차트
    public TimePeriod[] chartPeriods;         // 사용 가능한 시간 범위
    public bool enableVolumeOverlay;          // 거래량 막대
    public bool enableBenchmarkComparison;   // vs 시장 지수
    
    [Header("액션 버튼")]
    public ActionButton[] quickActions;       // 매수, 매도, 분석
    public bool enableContextualActions;     // 스마트 제안
    public ActionButtonStyle buttonStyle;    // 텍스트, 아이콘, 둘 다
    
    [Header("분석 도구")]
    public bool enableFundamentalData;       // P/E, 배당 등
    public bool enableTechnicalIndicators;   // RSI, MACD 등
    public bool enableNewsIntegration;       // 관련 뉴스 기사
}
```

### 4.2 거래 인터페이스

#### 주문 입력 양식
```csharp
[System.Serializable]
public struct OrderEntryConfig
{
    [Header("주문 유형")]
    public OrderType[] availableOrderTypes;   // 시장가, 지정가, 손절매
    public OrderType defaultOrderType;        // 시장가 기본값
    public bool enableAdvancedOrders;        // 고급 주문 유형
    
    [Header("입력 검증")]
    public bool enableRealTimeValidation;    // 입력시 유효성 검사
    public bool showBuyingPowerCheck;        // 구매력 확인
    public bool enableWarningMessages;       // 위험 경고
    
    [Header("확인 프로세스")]
    public bool requireOrderConfirmation;    // 주문 전 확인
    public ConfirmationStyle confirmationStyle; // 모달, 슬라이드업, 인라인
    public bool showOrderSummary;            // 주문 요약 표시
    
    [Header("빠른 액션")]
    public bool enableQuickTrade;            // 원클릭 거래
    public float[] quickTradeAmounts;        // [$100, $500, $1000]
    public bool enablePercentageEntry;       // 포트폴리오 %로 입력
}
```

## 5. 모바일 최적화

### 5.1 터치 인터페이스 디자인

#### 터치 대상 최적화
```csharp
[System.Serializable]
public struct TouchTargetConfig
{
    [Header("크기 표준")]
    public float minimumTouchTarget;         // 44px iOS, 48px Android
    public float recommendedTouchTarget;     // 56px 최적 크기
    public float touchTargetSpacing;         // 8px 최소 간격
    
    [Header("제스처 지원")]
    public bool enablePinchZoom;            // 핀치하여 확대/축소
    public bool enableSwipeNavigation;      // 스와이프 내비게이션
    public bool enableLongPress;            // 길게 누르기 메뉴
    public bool enableDoubleTap;            // 더블 탭 액션
    
    [Header("햅틱 피드백")]
    public bool enableHapticFeedback;       // 진동 피드백
    public HapticStyle buttonHaptic;        // 버튼 누름 피드백
    public HapticStyle errorHaptic;         // 오류 피드백
    public HapticStyle successHaptic;       // 성공 피드백
}
```

#### 반응형 레이아웃 시스템
```csharp
[System.Serializable]
public struct ResponsiveLayoutConfig
{
    [Header("브레이크포인트")]
    public int mobileBreakpoint;            // 768px
    public int tabletBreakpoint;            // 1024px
    public int desktopBreakpoint;           // 1440px
    
    [Header("레이아웃 적응")]
    public LayoutStrategy mobileStrategy;    // 단일 컬럼, 스택
    public LayoutStrategy tabletStrategy;    // 2-3 컬럼, 하이브리드
    public LayoutStrategy desktopStrategy;   // 다중 컬럼, 사이드바
    
    [Header("콘텐츠 우선순위")]
    public ContentPriority[] contentLayers; // 화면 크기별 표시 우선순위
    public bool enableContentHiding;        // 작은 화면에서 콘텐츠 숨김
    public bool enableAdaptiveNavigation;   // 적응형 내비게이션
}
```

### 5.2 성능 최적화

#### 렌더링 최적화
```csharp
[System.Serializable]
public struct MobilePerformanceConfig
{
    [Header("프레임률 목표")]
    public int targetFrameRate;             // 60 FPS
    public int minimumFrameRate;            // 30 FPS 최소
    public bool enableAdaptiveQuality;      // 성능에 따른 품질 조정
    
    [Header("메모리 관리")]
    public int maxTextureMemory;            // 256MB 텍스처 메모리
    public bool enableTextureCompression;   // 텍스처 압축
    public bool enableObjectPooling;        // 오브젝트 풀링
    
    [Header("배터리 최적화")]
    public bool enableBatteryOptimization;  // 배터리 절약 모드
    public float idleFrameRate;             // 유휴시 30 FPS
    public bool enableBackgroundThrottling; // 백그라운드 제한
}
```

## 6. 접근성 기능

### 6.1 시각적 접근성

#### 색상 및 대비
```csharp
[System.Serializable]
public struct VisualAccessibilityConfig
{
    [Header("색상 접근성")]
    public bool enableColorBlindSupport;    // 색맹 지원
    public bool enableHighContrast;         // 고대비 모드
    public float minimumContrastRatio;      // 4.5:1 WCAG AA
    
    [Header("텍스트 확장성")]
    public float[] fontSizeOptions;         // [100%, 125%, 150%, 200%]
    public bool enableDynamicType;          // 시스템 글꼴 크기 따름
    public float maxFontScale;              // 200% 최대 확대
    
    [Header("시각적 표시")]
    public bool enableFocusIndicators;      // 포커스 표시기
    public bool enableScreenReader;         // 스크린 리더 지원
    public bool enableVoiceOver;            // VoiceOver/TalkBack
}
```

### 6.2 운동 접근성

#### 대체 입력 방법
```csharp
[System.Serializable]
public struct MotorAccessibilityConfig
{
    [Header("터치 지원")]
    public bool enableAssistiveTouch;       // 보조 터치
    public float touchSensitivity;          // 터치 민감도
    public bool enableStickyDrag;           // 끈적한 드래그
    
    [Header("키보드 내비게이션")]
    public bool enableKeyboardNavigation;   // 키보드 내비게이션
    public bool enableTabOrder;             // 탭 순서
    public bool enableKeyboardShortcuts;    // 키보드 단축키
    
    [Header("음성 제어")]
    public bool enableVoiceCommands;        // 음성 명령
    public string[] voiceCommands;          // 사용 가능한 명령어
    public float voiceConfidenceThreshold;  // 80% 신뢰도 임계값
}
```

## 7. 커스터마이제이션

### 7.1 테마 시스템

#### 색상 테마
```csharp
[System.Serializable]
public struct ThemeConfig
{
    [Header("미리 정의된 테마")]
    public ColorTheme[] availableThemes;     // 라이트, 다크, 고대비
    public ColorTheme defaultTheme;          // 라이트 테마 기본값
    public bool enableAutomaticSwitching;   // 시스템 설정 따름
    
    [Header("사용자 정의 색상")]
    public bool enableCustomColors;          // 사용자 정의 색상
    public ColorCategory[] customizableColors; // 액센트, 배경, 텍스트
    public bool enableColorPresets;          // 색상 프리셋
    
    [Header("다크 모드")]
    public bool enableDarkMode;             // 다크 모드 지원
    public DarkModeStyle darkModeStyle;     // 순수 검정, 진한 회색
    public bool enableAutoSchedule;         // 시간별 자동 전환
}
```

### 7.2 레이아웃 커스터마이제이션

#### 대시보드 위젯
```csharp
[System.Serializable]
public struct DashboardCustomizationConfig
{
    [Header("위젯 시스템")]
    public WidgetType[] availableWidgets;    // 사용 가능한 위젯
    public int maxWidgetsPerScreen;         // 화면당 최대 위젯 수
    public bool enableWidgetReordering;     // 위젯 재정렬
    
    [Header("위젯 크기")]
    public WidgetSize[] supportedSizes;     // 소형, 중형, 대형
    public bool enableResizableWidgets;     // 크기 조정 가능 위젯
    public GridLayout gridSystem;           // 격자 시스템
    
    [Header("위젯 설정")]
    public bool enableWidgetSettings;       // 위젯별 설정
    public bool enableWidgetData;           // 위젯 데이터 소스 선택
    public bool enableWidgetFilters;        // 위젯 필터
}

public enum WidgetType
{
    NetWorthSummary,     // 순자산 요약
    PortfolioAllocation, // 포트폴리오 배분
    MarketOverview,      // 시장 개요
    TopHoldings,         // 주요 보유 자산
    RecentTrades,        // 최근 거래
    EconomicIndicators,  // 경제 지표
    NewsStream,          // 뉴스 스트림
    PerformanceChart     // 성과 차트
}
```

## 다음 단계

1. **[튜토리얼 온보딩](./tutorial-onboarding_KOR.md)** - 학습 시스템 디자인
2. **[이벤트 위기 시스템](./events-crisis-system_KOR.md)** - 동적 이벤트 및 위기 관리
3. **[진행 시스템](./progression-system_KOR.md)** - 플레이어 발전과 잠금 해제

## 관련 문서

- [자본주의 게임 디자인 문서](./capitalism-game-design-doc_KOR.md) - 전체 게임 디자인 개요
- [진행 시스템](./progression-system_KOR.md) - 플레이어 발전 시스템
- [경제 밸런스 모델](./economy-balance-model_KOR.md) - 경제 시스템 세부사항