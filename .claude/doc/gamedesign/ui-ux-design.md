---
category: gamedesign
tags: [ui, ux, design, interface, dashboard, mobile, accessibility]
related: [capitalism-game-design-doc.md, progression-system.md, economy-balance-model.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# UI/UX Design

[🇰🇷 Korean Version](./ui-ux-design_KOR.md)

## 📍 Navigation

[↩️ Back to Game Design](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../CLAUDE.md)

## 1. Design Philosophy

### 1.1 Core Principles

#### Financial Data Clarity
- **Information Hierarchy**: Most critical data prominently displayed
- **Real-time Updates**: Smooth transitions for changing values
- **Contextual Depth**: Progressive disclosure from overview to details
- **Professional Aesthetics**: Clean, financial industry-inspired design

#### Accessibility and Inclusivity
- **Universal Design**: Usable by users with varying abilities
- **Color Blind Friendly**: Meaningful without color dependencies
- **Scalable Text**: Support for different font sizes
- **Motor Accessibility**: Large touch targets, gesture alternatives

#### Cross-Platform Consistency
- **Responsive Design**: Seamless experience across devices
- **Platform Conventions**: Respect iOS/Android/PC interface guidelines
- **Performance Optimization**: 60 FPS on mobile devices
- **Touch-First Design**: Optimized for finger navigation with mouse/keyboard support

### 1.2 User Experience Pillars

#### Progressive Complexity
- **Guided Discovery**: Features revealed as player advances
- **Contextual Help**: Just-in-time information and tutorials
- **Simplified Onboarding**: Minimal friction for new users
- **Expert Mode**: Advanced features for experienced players

#### Emotional Engagement
- **Achievement Celebration**: Satisfying feedback for milestones
- **Progress Visualization**: Clear advancement indicators
- **Personality Expression**: Customizable interface elements
- **Social Recognition**: Sharing and comparison features

## 2. Information Architecture

### 2.1 Navigation Structure

#### Primary Navigation Hierarchy
```
Main Dashboard
├── Portfolio Overview
│   ├── Asset Allocation
│   ├── Performance Metrics
│   └── Holdings Detail
├── Market Research
│   ├── Market Indices
│   ├── Security Analysis
│   └── Economic Indicators
├── Trading Center
│   ├── Order Management
│   ├── Trade History
│   └── Watchlists
├── Automation Hub
│   ├── Active Strategies
│   ├── Strategy Builder
│   └── Performance Analytics
├── Companies & Economy
│   ├── Company Browser
│   ├── Economic Overview
│   └── Simulation Controls
└── Settings & Profile
    ├── Game Settings
    ├── Achievement Gallery
    └── Tutorial Center
```

#### Tab Navigation System
```csharp
[System.Serializable]
public struct TabNavigationConfig
{
    [Header("Tab Layout")]
    public TabPosition tabPosition;          // Bottom, Top, Left, Right
    public int maxVisibleTabs;              // 5 tabs maximum for mobile
    public bool enableTabScrolling;         // Horizontal scroll for overflow
    
    [Header("Tab Behavior")]
    public float tabSwitchAnimation;        // 0.3s transition time
    public TabSwitchMode switchMode;        // Slide, Fade, Scale
    public bool enableSwipeGestures;        // Touch/trackpad swipe navigation
    
    [Header("Badge System")]
    public bool enableNotificationBadges;   // Red dots for notifications
    public BadgeStyle badgeStyle;          // Dot, Number, Icon
    public Color urgentBadgeColor;         // Red for urgent notifications
}

public enum TabPosition
{
    BottomMobile,    // Bottom tabs for mobile (thumb-friendly)
    TopDesktop,      // Top tabs for desktop
    LeftSidebar,     // Sidebar navigation for desktop
    ContextualFloat  // Floating contextual tabs
}
```

### 2.2 Information Density Management

#### Screen Real Estate Optimization
```csharp
[System.Serializable]
public struct ScreenDensityConfig
{
    [Header("Mobile Layout (320-768px)")]
    public int maxCardsPerRow_Mobile;       // 1-2 cards maximum
    public float cardMinHeight_Mobile;      // 120px minimum
    public float margins_Mobile;            // 16px margins
    
    [Header("Tablet Layout (768-1024px)")]
    public int maxCardsPerRow_Tablet;       // 2-3 cards
    public float cardMinHeight_Tablet;      // 140px minimum
    public float margins_Tablet;            // 24px margins
    
    [Header("Desktop Layout (1024px+)")]
    public int maxCardsPerRow_Desktop;      // 3-4 cards
    public float cardMinHeight_Desktop;     // 160px minimum
    public float margins_Desktop;           // 32px margins
    
    [Header("Information Priority")]
    public InfoPriority[] informationLayers;
    public bool enableDetailCollapse;       // Hide details when space constrained
}

public enum InfoPriority
{
    Critical,        // Always visible (current net worth)
    Important,       // Hide only on smallest screens (portfolio change)
    Contextual,      // Show when relevant (sector breakdown)
    Optional         // Hide unless specifically requested (detailed metrics)
}
```

## 3. Main Dashboard Design

### 3.1 Wealth Overview Section

#### Net Worth Display
```csharp
[System.Serializable]
public struct WealthDisplayConfig
{
    [Header("Primary Metric")]
    public WealthFormat primaryFormat;       // Currency, Scientific, Percentage
    public bool enableAnimatedCounting;     // Count-up animation for changes
    public float countAnimationDuration;    // 2.0s animation time
    
    [Header("Trend Visualization")]
    public TrendDisplayMode trendMode;      // Arrow, Graph, Color, Number
    public Color positiveColor;             // Green #00C851
    public Color negativeColor;             // Red #FF4444
    public Color neutralColor;              // Gray #999999
    
    [Header("Comparison Context")]
    public bool showPercentileRank;         // "Top 15% of players"
    public bool showPeerComparison;         // Compare to similar players
    public bool showHistoricalBest;        // "85% of your all-time high"
}

public enum WealthFormat
{
    Currency,        // $1,234,567
    Abbreviated,     // $1.23M
    Scientific,      // 1.23e6
    Percentage       // +15.2% this month
}

public enum TrendDisplayMode
{
    ArrowIcon,       // ↗️ ↘️ arrows
    MiniGraph,       // Sparkline chart
    ColorBackground, // Green/red background
    NumericChange    // +$125,450 (+12.5%)
}
```

#### Portfolio Allocation Visualization
```csharp
[System.Serializable]
public struct AllocationVisualizationConfig
{
    [Header("Chart Type")]
    public ChartType primaryChart;          // Pie, Donut, Treemap, Bar
    public ChartType mobileChart;           // Simplified for mobile
    public bool enableInteractiveChart;    // Tap to drill down
    
    [Header("Color Scheme")]
    public ColorPalette palette;           // Asset class colors
    public bool enableColorBlindSupport;   // Patterns + colors
    public float saturationLevel;          // 0.8 for professional look
    
    [Header("Detail Level")]
    public int maxVisibleSlices;          // 8 slices before "Others"
    public float minimumSlicePercent;     // 2% minimum to show slice
    public bool enablePercentageLabels;   // Show % on slices
}

public enum ChartType
{
    DonutChart,      // Modern donut with center value
    PieChart,        // Traditional pie chart
    TreemapChart,    // Rectangle sizes for allocation
    HorizontalBar,   // Horizontal bar chart
    StackedBar       // Single stacked bar
}
```

### 3.2 Performance Metrics Panel

#### Key Performance Indicators
```csharp
[System.Serializable]
public struct PerformanceMetricsConfig
{
    [Header("Time Periods")]
    public TimePeriod[] availablePeriods;   // 1D, 1W, 1M, 3M, 1Y, All
    public TimePeriod defaultPeriod;        // 1M default
    public bool enableCustomRange;          // Date picker for custom ranges
    
    [Header("Metrics Display")]
    public MetricCard[] primaryMetrics;     // ROI, Sharpe, Max Drawdown
    public MetricCard[] secondaryMetrics;   // Beta, Alpha, Volatility
    public int maxMetricsOnMobile;         // 4 metrics maximum
    
    [Header("Benchmarking")]
    public string[] benchmarkIndices;      // S&P 500, NASDAQ, etc.
    public bool enableBenchmarkComparison; // Show vs benchmark
    public bool enablePeerComparison;      // Show vs other players
}

public struct MetricCard
{
    public string metricName;              // "Annual Return"
    public string displayFormat;           // "+12.5%"
    public MetricTrend trend;              // Up, Down, Stable
    public string helpText;                // Tooltip explanation
    public bool isGoodWhenHigh;           // True for ROI, false for volatility
}
```

#### Performance Chart Component
```csharp
[System.Serializable]
public struct PerformanceChartConfig
{
    [Header("Chart Style")]
    public ChartStyle chartStyle;          // Line, Candlestick, Area
    public LineStyle lineStyle;            // Solid, Dashed, Smooth
    public bool enableDataPoints;          // Show dots on line
    
    [Header("Interactive Features")]
    public bool enableZoomGestures;        // Pinch to zoom
    public bool enablePanGestures;         // Pan to scroll
    public bool enableCrosshair;           // Crosshair on tap/hover
    public bool enableValueTooltip;        // Show value at point
    
    [Header("Comparison Overlays")]
    public bool enableBenchmarkOverlay;    // Show benchmark line
    public bool enableMultipleAssets;      // Compare multiple holdings
    public int maxComparisonLines;         // 3 lines maximum
    
    [Header("Annotations")]
    public bool enableTradeMarkers;        // Mark buy/sell points
    public bool enableEventMarkers;        // Mark economic events
    public bool enableTrendLines;          // User-drawn trend lines
}
```

### 3.3 Market Overview Section

#### Economic Indicators Dashboard
```csharp
[System.Serializable]
public struct EconomicIndicatorsConfig
{
    [Header("Key Indicators")]
    public IndicatorWidget[] primaryIndicators; // GDP, Inflation, Unemployment
    public IndicatorWidget[] secondaryIndicators; // Interest rates, etc.
    public UpdateFrequency updateFrequency;     // Real-time, Hourly, Daily
    
    [Header("Visualization")]
    public IndicatorStyle displayStyle;        // Gauge, Number, Graph
    public bool enableTrendArrows;             // Up/down arrows
    public bool enableHistoricalContext;      // "Highest in 6 months"
    
    [Header("Alerts")]
    public bool enableThresholdAlerts;         // Alert on significant changes
    public float significantChangeThreshold;   // 0.5% change triggers alert
    public AlertStyle alertStyle;              // Banner, Toast, Badge
}

public struct IndicatorWidget
{
    public string indicatorName;           // "GDP Growth"
    public float currentValue;             // 2.3
    public string units;                   // "%"
    public float changeFromPrevious;       // +0.2
    public IndicatorImportance importance; // High, Medium, Low
}
```

## 4. Portfolio Management Interface

### 4.1 Holdings List Design

#### Asset List Layout
```csharp
[System.Serializable]
public struct HoldingsListConfig
{
    [Header("List Style")]
    public ListViewMode viewMode;              // Card, Table, Compact
    public SortOption[] availableSortOptions;  // By value, %, name, sector
    public SortOption defaultSort;             // By portfolio weight
    
    [Header("Card Design")]
    public CardLayout cardLayout;              // Horizontal, Vertical, Grid
    public bool enableSwipeActions;            // Swipe for quick actions
    public SwipeAction[] leftSwipeActions;     // Buy more, Sell, Analyze
    public SwipeAction[] rightSwipeActions;    // Remove, Edit, Info
    
    [Header("Information Density")]
    public HoldingInfoLevel detailLevel;       // Minimal, Standard, Detailed
    public bool enableExpandableCards;        // Tap to expand for details
    public InfoField[] visibleFields;         // Which data to show
}

public enum ListViewMode
{
    CardView,        // Card-based layout (mobile friendly)
    TableView,       // Traditional table (desktop)
    CompactList,     // Dense list view
    GridView         // Grid of tiles
}

public struct InfoField
{
    public string fieldName;        // "Current Value"
    public string displayFormat;    // "$12,345"
    public FieldImportance priority; // Always, Desktop, Optional
    public bool enableTrendIcon;    // Show trend arrow
}
```

#### Individual Holding Detail
```csharp
[System.Serializable]
public struct HoldingDetailConfig
{
    [Header("Overview Section")]
    public bool showCurrentPrice;             // Real-time price
    public bool showDayChange;                // Today's change
    public bool showTotalReturn;              // Since purchase
    public bool showUnrealizedGainLoss;       // Profit/loss
    
    [Header("Performance Chart")]
    public bool enablePriceChart;             // Price history chart
    public TimePeriod[] chartPeriods;         // Available time ranges
    public bool enableVolumeOverlay;          // Trading volume bars
    public bool enableBenchmarkComparison;   // vs market index
    
    [Header("Action Buttons")]
    public ActionButton[] quickActions;       // Buy, Sell, Analyze
    public bool enableContextualActions;     // Smart suggestions
    public ActionButtonStyle buttonStyle;    // Text, Icon, Both
    
    [Header("Analysis Tools")]
    public bool enableFundamentalData;       // P/E, Dividend, etc.
    public bool enableTechnicalIndicators;   // RSI, MACD, etc.
    public bool enableNewsIntegration;       // Related news articles
}
```

### 4.2 Trading Interface

#### Order Entry Form
```csharp
[System.Serializable]
public struct OrderEntryConfig
{
    [Header("Order Types")]
    public OrderType[] availableOrderTypes;   // Market, Limit, Stop
    public OrderType defaultOrderType;        // Market order
    public bool enableAdvancedOrders;        // Stop-loss, OCO, etc.
    
    [Header("Input Validation")]
    public bool enableRealTimeValidation;    // Validate as user types
    public bool showImpactEstimation;        // Estimated market impact
    public bool enableRiskWarnings;          // Warn about risky trades
    
    [Header("User Experience")]
    public InputMethod preferredInputMethod;  // Slider, Stepper, Keyboard
    public bool enableQuickAmountButtons;     // $100, $500, $1000 buttons
    public bool enablePercentageInput;       // 25%, 50%, 100% of position
    
    [Header("Confirmation Flow")]
    public bool requireOrderConfirmation;     // Confirmation dialog
    public bool showOrderSummary;            // Review before submit
    public bool enableBiometricConfirm;      // Touch ID, Face ID
}

public enum InputMethod
{
    NumericKeyboard,  // Standard number input
    SliderInput,      // Drag slider for amount
    StepperButtons,   // +/- increment buttons
    PercentageWheel   // Circular percentage picker
}
```

#### Order Status and History
```csharp
[System.Serializable]
public struct OrderHistoryConfig
{
    [Header("Status Display")]
    public OrderStatus[] trackableStatuses;   // Pending, Filled, Cancelled
    public StatusIndicator statusIndicator;   // Color, Icon, Text
    public bool enableRealTimeUpdates;       // Live status updates
    
    [Header("History Management")]
    public int defaultHistoryLength;         // 30 days
    public HistoryFilter[] availableFilters; // By status, type, symbol
    public bool enableHistorySearch;         // Search by symbol/date
    
    [Header("Performance Tracking")]
    public bool calculateTradePerformance;   // P&L per trade
    public bool enablePerformanceAnalysis;  // Win rate, avg profit
    public bool showTradingPatterns;         // Time of day analysis
}
```

## 5. Mobile-Specific Design

### 5.1 Touch-Optimized Interface

#### Gesture Navigation
```csharp
[System.Serializable]
public struct TouchGestureConfig
{
    [Header("Navigation Gestures")]
    public bool enableSwipeNavigation;       // Swipe between tabs
    public SwipeDirection tabSwitchDirection; // Horizontal, Vertical
    public float swipeThreshold;             // 50px minimum swipe
    
    [Header("Chart Interactions")]
    public bool enablePinchZoom;             // Pinch to zoom charts
    public bool enableTwoFingerScroll;       // Two finger chart scroll
    public bool enableLongPressDetails;     // Long press for details
    
    [Header("List Interactions")]
    public bool enablePullToRefresh;         // Pull down to refresh
    public bool enableSwipeActions;          // Swipe for quick actions
    public bool enableHapticFeedback;        // Tactile feedback
    
    [Header("Accessibility")]
    public float minimumTouchTarget;         // 44px iOS, 48dp Android
    public bool enableVoiceOver;            // Screen reader support
    public bool enableLargeText;             // Dynamic type support
}
```

#### Responsive Layout System
```csharp
[System.Serializable]
public struct ResponsiveLayoutConfig
{
    [Header("Breakpoints")]
    public DeviceBreakpoint[] breakpoints;   // Phone, Tablet, Desktop
    public OrientationHandling orientation;  // Portrait, Landscape, Adaptive
    
    [Header("Layout Adaptation")]
    public bool enableAutoHideElements;      // Hide less important UI
    public bool enableCollapsibleSections;  // Collapsible detail sections
    public bool enableFloatingActions;      // FAB for primary actions
    
    [Header("Typography Scaling")]
    public FontScaleLevel[] fontScales;      // System font size support
    public float maximumFontScale;           // 200% maximum
    public bool maintainLineHeight;          // Consistent line spacing
}

public struct DeviceBreakpoint
{
    public string breakpointName;      // "Mobile", "Tablet", "Desktop"
    public float minWidth;             // 320px
    public float maxWidth;             // 768px
    public LayoutProfile layoutProfile; // Specific layout configuration
}
```

### 5.2 Performance Optimization

#### Mobile Performance Settings
```csharp
[System.Serializable]
public struct MobilePerformanceConfig
{
    [Header("Rendering Optimization")]
    public int maxSimultaneousCharts;        // 2 charts max on mobile
    public bool enableChartCaching;          // Cache rendered charts
    public float chartUpdateFrequency;       // 1s update frequency
    
    [Header("Data Management")]
    public int maxHistoryDataPoints;         // 100 points max
    public bool enableDataCompression;      // Compress historical data
    public bool enableLazyLoading;          // Load data on demand
    
    [Header("Animation Settings")]
    public bool respectReducedMotion;        // Honor accessibility preference
    public float animationDuration;          // 0.3s standard duration
    public AnimationEasing easingCurve;      // Ease-in-out
    
    [Header("Battery Optimization")]
    public bool enablePowerSaveMode;         // Reduce updates when low battery
    public float backgroundUpdateFrequency;  // 30s when backgrounded
    public bool pauseInBackground;           // Pause when app not visible
}
```

## 6. Accessibility Design

### 6.1 Universal Design Standards

#### WCAG 2.1 Compliance
```csharp
[System.Serializable]
public struct AccessibilityConfig
{
    [Header("Visual Accessibility")]
    public float minimumColorContrast;       // 4.5:1 for normal text
    public bool supportColorBlindness;       // Pattern + color coding
    public bool enableHighContrastMode;     // High contrast theme
    
    [Header("Motor Accessibility")]
    public float minimumTouchTargetSize;     // 44pt minimum
    public bool enableAlternativeNavigation; // Keyboard, switch control
    public bool supportOneHandedUse;        // Bottom-aligned controls
    
    [Header("Cognitive Accessibility")]
    public bool enableSimplifiedMode;       // Reduced complexity UI
    public bool provideTooltips;            // Explanatory tooltips
    public bool enableUndoActions;          // Undo for major actions
    
    [Header("Auditory Accessibility")]
    public bool provideVoiceOverSupport;    // Screen reader compatibility
    public bool enableAudioCues;            // Sound notifications
    public bool provideCaptions;             // Video/audio captions
}
```

#### Screen Reader Support
```csharp
[System.Serializable]
public struct ScreenReaderConfig
{
    [Header("Content Description")]
    public bool enableSemanticLabels;       // Meaningful element labels
    public bool provideLiveRegions;         // Announce dynamic changes
    public bool enableHeadingStructure;     // Proper heading hierarchy
    
    [Header("Navigation Support")]
    public bool enableLandmarkRegions;      // Main, nav, aside regions
    public bool provideFocusManagement;     // Logical focus order
    public bool enableSkipLinks;            // Skip to main content
    
    [Header("Content Formatting")]
    public bool announceDataChanges;        // Speak value changes
    public bool provideSummaryInfo;         // Portfolio summaries
    public bool enableTableHeaders;         // Proper table markup
}
```

### 6.2 Personalization Features

#### Customizable Interface
```csharp
[System.Serializable]
public struct PersonalizationConfig
{
    [Header("Theme Options")]
    public ColorTheme[] availableThemes;     // Light, Dark, High Contrast
    public bool enableDynamicTheming;       // System theme following
    public bool allowCustomColors;          // User color selection
    
    [Header("Layout Customization")]
    public bool enableWidgetReordering;     // Drag to reorder widgets
    public bool allowWidgetHiding;          // Hide unwanted widgets
    public bool enableDashboardLayouts;     // Preset layout options
    
    [Header("Information Display")]
    public bool allowMetricCustomization;   // Choose displayed metrics
    public bool enableUnitPreferences;      // Currency, number format
    public bool allowDateFormatSelection;   // Date/time preferences
    
    [Header("Notification Preferences")]
    public NotificationType[] notificationTypes; // Price alerts, news, etc.
    public bool enableNotificationScheduling;   // Quiet hours
    public DeliveryMethod[] deliveryMethods;     // Push, email, SMS
}
```

## 7. Animation and Micro-Interactions

### 7.1 Animation Framework

#### Smooth Transitions
```csharp
[System.Serializable]
public struct AnimationConfig
{
    [Header("Transition Timing")]
    public float quickTransition;           // 0.15s for quick feedback
    public float standardTransition;        // 0.3s for page transitions
    public float slowTransition;            // 0.5s for complex animations
    
    [Header("Easing Functions")]
    public EasingType defaultEasing;        // Ease-in-out
    public EasingType quickEasing;          // Ease-out for quick actions
    public EasingType dramaticEasing;       // Bounce for celebrations
    
    [Header("Performance")]
    public bool enableHardwareAcceleration; // GPU acceleration
    public bool respectReducedMotion;       // Honor system preference
    public int maxSimultaneousAnimations;   // 3 animations max
    
    [Header("Context-Aware")]
    public bool disableOnLowPerformance;    // Disable on slow devices
    public bool reduceInPowerSaveMode;      // Minimal animations
    public bool pauseWhenBackgrounded;      // Stop when app hidden
}
```

#### Micro-Interaction Design
```csharp
[System.Serializable]
public struct MicroInteractionConfig
{
    [Header("Button Feedback")]
    public bool enableTapScaling;           // Scale on tap
    public float tapScaleAmount;            // 0.95 scale factor
    public bool enableRippleEffect;         // Material Design ripple
    
    [Header("Data Updates")]
    public bool enableCountingAnimation;    // Count up to new values
    public bool enableColorFlash;           // Flash on significant change
    public bool enableShakeOnError;         // Shake invalid inputs
    
    [Header("Loading States")]
    public LoadingAnimationType loadingStyle; // Spinner, Skeleton, Pulse
    public bool enableProgressIndicators;   // Show loading progress
    public bool enableOptimisticUpdates;    // Update UI before confirmation
    
    [Header("Achievement Celebrations")]
    public bool enableConfettiEffect;       // Confetti for milestones
    public bool enableParticleEffects;      // Sparkles for positive events
    public bool enableScreenFlash;          // Subtle flash for achievements
}
```

### 7.2 Feedback Systems

#### Visual Feedback
```csharp
[System.Serializable]
public struct VisualFeedbackConfig
{
    [Header("State Indicators")]
    public StateIndicator[] statusIndicators; // Loading, Success, Error
    public bool enableIconAnimations;        // Animated status icons
    public bool enableColorTransitions;      // Smooth color changes
    
    [Header("Progress Visualization")]
    public ProgressStyle progressBarStyle;   // Linear, Circular, Custom
    public bool enableProgressAnimation;     // Animated progress bars
    public bool showPercentageText;          // Show % complete
    
    [Header("Validation Feedback")]
    public bool enableInlineValidation;      // Real-time input validation
    public bool useColorCoding;              // Red/green for valid/invalid
    public bool enableTooltipErrors;         // Error tooltips
}
```

#### Haptic Feedback
```csharp
[System.Serializable]
public struct HapticFeedbackConfig
{
    [Header("Touch Feedback")]
    public bool enableSelectionFeedback;    // Light tap for selections
    public bool enableSuccessFeedback;      // Success haptic pattern
    public bool enableErrorFeedback;        // Error haptic pattern
    
    [Header("Gesture Feedback")]
    public bool enableSwipeFeedback;        // Feedback for swipe actions
    public bool enableScrollFeedback;       // Subtle scroll feedback
    public bool enableZoomFeedback;         // Pinch zoom feedback
    
    [Header("Intensity Control")]
    public HapticIntensity defaultIntensity; // Medium intensity
    public bool allowUserControl;           // User can disable/adjust
    public bool respectSystemSettings;      // Honor system haptic preference
}
```

## 8. Data Visualization

### 8.1 Chart Design System

#### Chart Library Integration
```csharp
[System.Serializable]
public struct ChartSystemConfig
{
    [Header("Chart Types")]
    public ChartType[] supportedCharts;     // Line, Bar, Pie, Candlestick
    public ChartRenderer renderer;          // Unity UI, Canvas, WebGL
    public bool enableInteractiveCharts;    // Touch/mouse interaction
    
    [Header("Performance")]
    public int maxDataPoints;              // 1000 points maximum
    public bool enableDataDecimation;      // Reduce points for performance
    public bool enableWebWorkerProcessing; // Background processing
    
    [Header("Theming")]
    public ChartTheme lightTheme;          // Light mode colors
    public ChartTheme darkTheme;           // Dark mode colors
    public bool followSystemTheme;         // Auto theme switching
    
    [Header("Accessibility")]
    public bool enableDataTables;          // Table view for screen readers
    public bool provideSonification;       // Audio chart representation
    public bool enablePatternFills;        // Patterns for color blindness
}
```

#### Real-time Data Updates
```csharp
[System.Serializable]
public struct RealTimeChartConfig
{
    [Header("Update Frequency")]
    public float updateInterval;            // 1.0s update frequency
    public bool enableAdaptiveFrequency;   // Slower when unfocused
    public bool pauseWhenBackgrounded;     // Pause background updates
    
    [Header("Animation")]
    public bool enableSmoothUpdates;       // Smooth value transitions
    public float transitionDuration;       // 0.5s transition time
    public bool enableDataPointAnimation;  // Animate new points
    
    [Header("Performance")]
    public bool enableDataStreaming;       // Stream large datasets
    public bool useIncrementalUpdates;     // Only update changed data
    public int maxBufferSize;              // 5000 data point buffer
}
```

### 8.2 Information Dashboard

#### Widget System
```csharp
[System.Serializable]
public struct DashboardWidgetConfig
{
    [Header("Widget Types")]
    public WidgetType[] availableWidgets;   // Chart, Metric, News, etc.
    public bool enableCustomWidgets;       // User-created widgets
    public bool allowWidgetResizing;       // Drag to resize
    
    [Header("Layout Management")]
    public LayoutMode layoutMode;          // Grid, Flexible, Custom
    public bool enableDragAndDrop;         // Reorder widgets
    public bool enableCollapsibleWidgets;  // Minimize widgets
    
    [Header("Data Binding")]
    public bool enableLiveDataBinding;     // Real-time data updates
    public bool allowMultipleDataSources; // Combine data sources
    public bool enableDataFiltering;       // Filter widget data
    
    [Header("Customization")]
    public bool allowColorCustomization;   // Custom widget colors
    public bool enableSizePresets;         // Small, Medium, Large
    public bool allowTitleEditing;         // Custom widget titles
}

public enum WidgetType
{
    MetricCard,          // Single number display
    MiniChart,           // Small chart widget
    NewsFeed,            // News ticker widget
    WatchList,           // Security watchlist
    Calendar,            // Economic calendar
    Alert,               // Alert/notification widget
    Performance,         // Performance summary
    Allocation           // Portfolio allocation chart
}
```

## 9. Settings and Customization

### 9.1 User Preferences

#### Preference Categories
```csharp
[System.Serializable]
public struct UserPreferencesConfig
{
    [Header("Display Preferences")]
    public DisplayPreferences display;
    public NotificationPreferences notifications;
    public SecurityPreferences security;
    public DataPreferences data;
    
    [Header("Trading Preferences")]
    public OrderDefaultsConfig orderDefaults;
    public RiskManagementConfig riskManagement;
    public AutomationPreferences automation;
    
    [Header("Accessibility")]
    public AccessibilityPreferences accessibility;
    public PersonalizationPreferences personalization;
}

[System.Serializable]
public struct DisplayPreferences
{
    public ColorTheme theme;                // Light, Dark, Auto
    public string currency;                 // USD, EUR, GBP, etc.
    public string dateFormat;              // MM/DD/YYYY, DD/MM/YYYY
    public string numberFormat;             // 1,234.56 vs 1.234,56
    public bool show24HourTime;             // 24-hour vs 12-hour
    public bool enableAnimations;           // Enable/disable animations
    public FontSize fontSize;               // Small, Medium, Large
}
```

### 9.2 Advanced Settings

#### Performance Tuning
```csharp
[System.Serializable]
public struct PerformanceSettingsConfig
{
    [Header("Rendering Settings")]
    public int maxFrameRate;               // 60, 30, or adaptive
    public QualityLevel graphicsQuality;   // Low, Medium, High
    public bool enableVSync;               // Vertical sync
    
    [Header("Data Settings")]
    public int historicalDataLimit;        // Days of historical data
    public float refreshRate;              // Data refresh frequency
    public bool enableDataCompression;     // Compress stored data
    
    [Header("Memory Management")]
    public int maxCacheSize;               // MB of cached data
    public bool enableAggressiveCaching;   // More aggressive caching
    public bool clearCacheOnExit;          // Clear cache on app exit
    
    [Header("Network Settings")]
    public bool enableOfflineMode;         // Work without internet
    public int connectionTimeout;          // Network timeout seconds
    public bool enableDataSaver;           // Reduce data usage
}
```

## Next Steps

1. **[Tutorial Onboarding](./tutorial-onboarding.md)** - Learning system design
2. **[Events Crisis System](./events-crisis-system.md)** - Event system design
3. **Implementation Guide** - Technical implementation specifications

## Related Documents

- [Progression System](./progression-system.md) - Player advancement and unlocks
- [AI Behavior Patterns](./ai-behavior-patterns.md) - AI decision algorithms
- [Economy Balance Model](./economy-balance-model.md) - Economic parameters