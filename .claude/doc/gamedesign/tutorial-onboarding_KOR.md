---
category: gamedesign
tags: [튜토리얼, 온보딩, 교육, 학습, 가이드]
related: [progression-system_KOR.md, ui-ux-design_KOR.md, capitalism-game-design-doc_KOR.md]
parent: INDEX_KOR.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# 튜토리얼 및 온보딩 시스템

[🇺🇸 English Version](./tutorial-onboarding.md)

## 📍 내비게이션

[↩️ 게임 디자인으로 돌아가기](./INDEX_KOR.md) | [📚 문서 색인](../INDEX_KOR.md) | [🏠 홈](../../CLAUDE_KOR.md)

## 1. 온보딩 철학

### 1.1 교육 프레임워크

#### 점진적 학습 모델
- **단계적 발견**: 학습자가 이해를 구축할 때 지원 제공
- **적시 학습**: 개념이 관련성을 갖게 될 때 도입
- **실습 학습**: 실제 경험이 이론적 지식을 강화
- **실패 안전 환경**: 실제 결과 없이 실험 허용

#### 금융 문해력 목표
- **투자 기초**: 위험, 수익, 다변화, 돈의 시간 가치
- **시장 이해**: 시장 작동 방식, 가격 발견, 경제 주기
- **행동 인식**: 인지 편향, 감정적 의사결정
- **전략적 사고**: 장기 계획, 포트폴리오 관리, 자동화

### 1.2 사용자 여정 매핑

#### 온보딩 단계
```csharp
[System.Serializable]
public enum OnboardingStage
{
    FirstImpression,     // 0-30초: 사용자 후킹
    CoreConcepts,        // 1-5분: 기본 투자 원칙  
    FirstActions,        // 5-15분: 첫 투자 실행
    SystemExploration,   // 15-60분: 인터페이스 탐색
    StrategyDevelopment, // 1-7일: 투자 접근법 개발
    AutomationMastery,   // 1-4주: 자동화 기능 숙련
    AdvancedStrategies   // 1-3개월: 복잡한 금융 상품
}

[System.Serializable]
public struct OnboardingMetrics
{
    [Header("완료율")]
    public float[] stageCompletionRates;     // 목표 90%, 80%, 70%, 60%, 50%, 30%, 15%
    public float overallCompletionRate;      // 모든 단계 완료 목표 15%
    
    [Header("가치 실현 시간")]
    public float timeToFirstInvestment;      // 목표 5분 미만
    public float timeToFirstProfit;          // 목표 30분 미만
    public float timeToAutomationSetup;      // 목표 7일 미만
    
    [Header("참여도")]
    public float dailyActiveUsers;           // 다음날 돌아오는 %
    public float weeklyRetention;            // 일주일 후 돌아오는 %
    public float monthlyRetention;           // 한 달 후 돌아오는 %
}
```

## 2. 첫 사용자 경험

### 2.1 환영 시퀀스

#### 오프닝 후크 (0-30초)
```csharp
[System.Serializable]
public struct WelcomeSequenceConfig
{
    [Header("오프닝 애니메이션")]
    public float introAnimationLength;       // 최대 10초
    public bool enableSkipIntro;            // 애니메이션 건너뛰기 허용
    public AnimationStyle animationStyle;   // 영화적, 간단함, 없음
    
    [Header("가치 제안")]
    public string[] keyBenefits;            // "투자 학습", "부 구축"
    public float benefitDisplayTime;        // 혜택당 3초
    public bool enableInteractiveBenefits;  // 탭하여 진행
    
    [Header("캐릭터 소개")]  
    public bool useCharacterGuide;          // 친근한 AI 가이드 캐릭터
    public CharacterPersonality personality; // 전문적, 캐주얼, 열정적
    public string characterName;            // "알렉스" 또는 "금융 비서"
}

// 환영 시퀀스 예시
private WelcomeMessage[] welcomeMessages = {
    new WelcomeMessage {
        title = "자본주의 시뮬레이터에 오신 것을 환영합니다",
        content = "가상 부를 구축하며 실제 투자를 배우세요",
        callToAction = "여정 시작하기",
        duration = 4.0f
    },
    new WelcomeMessage {
        title = "당신의 목표: 백만 달러",
        content = "1만 달러로 시작하여 스마트한 투자를 통해 늘려보세요",
        callToAction = "준비됐습니다",
        duration = 3.0f
    }
};
```

#### 계정 설정 (30초 - 2분)
```csharp
[System.Serializable]
public struct AccountSetupConfig
{
    [Header("필수 정보")]
    public bool requireDisplayName;         // 플레이어 표시 이름
    public bool requireInvestmentGoals;     // 부 구축 목표
    public bool requireRiskTolerance;       // 위험 선호도 평가
    public bool requireExperience;          // 투자 경험 수준
    
    [Header("선택 정보")]
    public bool offerAgeRange;             // 연령대 (선택사항)
    public bool offerEducation;            // 교육 배경
    public bool offerIncome;               // 소득 수준 (시뮬레이션 기준)
    
    [Header("개인정보 설정")]
    public bool requirePrivacyConsent;     // GDPR/CCPA 준수
    public bool enableDataMinimization;    // 필요한 데이터만 수집
    public bool offerAnonymousMode;        // 개인 데이터 없이 플레이
    
    [Header("게임화")]
    public bool enableStartingBonuses;     // 완료 시 보너스
    public bool showProgressBar;           // 설정 진행 표시기
    public float setupTimeTarget;          // 목표 90초
}
```

### 2.2 위험 허용도 평가

#### 대화형 위험 설문
```csharp
[System.Serializable]
public struct RiskAssessmentConfig
{
    [Header("질문 유형")]
    public RiskQuestion[] questions;        // 최대 5-7개 질문
    public QuestionFormat format;          // 객관식, 슬라이더, 시나리오
    public bool enableScenarioMode;        // 대화형 시나리오
    
    [Header("채점 시스템")]
    public float conservativeThreshold;     // 0-30점
    public float moderateThreshold;         // 31-60점
    public float aggressiveThreshold;       // 61-100점
    
    [Header("결과 표시")]
    public bool showRiskProfile;           // 위험 프로필 결과 표시
    public bool explainImplications;       // 프로필의 의미 설명
    public bool allowProfileChange;        // 나중에 설정에서 변경 가능
}

// 위험 평가 질문 예시
private RiskQuestion[] riskQuestions = {
    new RiskQuestion {
        questionText = "당신의 투자가 첫 달에 20% 손실을 봤습니다. 어떻게 하시겠습니까?",
        answers = new[] {
            new Answer { text = "즉시 매도", riskScore = 0 },
            new Answer { text = "보유하며 기다림", riskScore = 50 },
            new Answer { text = "더 낮은 가격에 추가 매수", riskScore = 100 }
        }
    },
    new RiskQuestion {
        questionText = "주요 투자 목표는 무엇입니까?",
        answers = new[] {
            new Answer { text = "자금 보존", riskScore = 0 },
            new Answer { text = "시간에 걸쳐 꾸준히 성장", riskScore = 50 },
            new Answer { text = "성장 잠재력 극대화", riskScore = 100 }
        }
    }
};
```

### 2.3 시작 포트폴리오 설정

#### 안내된 포트폴리오 생성
```csharp
[System.Serializable]
public struct PortfolioSetupConfig
{
    [Header("시작 자본")]
    public float defaultStartingAmount;     // $10,000 시작 자금
    public bool allowCustomAmount;          // 시작 금액 선택
    public float[] presetAmounts;          // $5K, $10K, $25K 옵션
    
    [Header("초기 배분")]
    public AssetAllocation conservativeAllocation; // 주식 60%, 채권 40%
    public AssetAllocation moderateAllocation;     // 주식 70%, 채권 30%  
    public AssetAllocation aggressiveAllocation;   // 주식 90%, 채권 10%
    
    [Header("안내 경험")]
    public bool enableAllocationWizard;     // 단계별 배분
    public bool showAllocationExplanation; // 이러한 배분의 이유 설명
    public bool allowManualOverride;       // 고급 사용자 커스터마이징 가능
    
    [Header("교육 통합")]
    public bool explainDiversification;    // 다변화 개념 교육
    public bool showRiskReturnTradeoff;    // 위험 vs 수익 시각화
    public bool demonstrateRebalancing;    // 리밸런싱 개념 시연
}
```

## 3. 핵심 튜토리얼 모듈

### 3.1 투자 기초

#### 모듈 1: 첫 투자하기
```csharp
[System.Serializable]
public struct FirstInvestmentTutorial
{
    [Header("학습 목표")]
    public string[] learningObjectives = {
        "주식이 무엇을 나타내는지 이해",
        "회사를 조사하는 방법 학습", 
        "첫 주식 구매 실행",
        "투자 성과 모니터링"
    };
    
    [Header("대화형 요소")]
    public bool enableCompanyResearch;      // 튜토리얼 회사 조사
    public bool useRealMarketData;         // 실제 vs 시뮬레이션 데이터
    public bool enablePaperTrading;        // 실제 돈 없이 연습
    
    [Header("가이드 수준")]
    public GuidanceMode guidanceMode;       // 강력한 가이드 vs 탐색적
    public bool enableHints;               // 막힐 때 힌트 표시
    public bool allowMistakes;             // 사용자가 차선책 선택하도록 허용
    
    [Header("성공 기준")]
    public float minimumInvestmentAmount;   // 첫 투자 최소 $100
    public bool requireResearchCompletion; // 매수 전 반드시 조사
    public float timeLimit;                // 선택적 시간 압박
}

public void StartFirstInvestmentTutorial(Player player)
{
    var tutorial = firstInvestmentTutorial;
    
    // 1단계: 주식 소개
    ShowTutorialStep(new TutorialStep {
        title = "주식이란 무엇인가요?",
        content = "주식은 회사의 소유권 지분을 나타냅니다. 주식을 사면 그 사업의 작은 부분을 소유하게 됩니다.",
        visualAid = TutorialVisual.StockOwnershipDiagram,
        interaction = TutorialInteraction.TapToContinue
    });
    
    // 2단계: 회사 조사
    ShowTutorialStep(new TutorialStep {
        title = "매수 전 조사하기",
        content = "스마트한 투자자는 투자 전에 회사를 조사합니다. 함께 TechCorp를 살펴보겠습니다.",
        visualAid = TutorialVisual.CompanyProfileDemo,
        interaction = TutorialInteraction.GuidedResearch
    });
    
    // 3단계: 구매 실행
    ShowTutorialStep(new TutorialStep {
        title = "첫 주식 매수하기",
        content = "이제 TechCorp 주식 10주를 사보겠습니다. 시작 자금 $10,000에서 $500이 들 것입니다.",
        visualAid = TutorialVisual.OrderFormDemo,
        interaction = TutorialInteraction.GuidedPurchase
    });
    
    // 4단계: 성과 모니터링
    ShowTutorialStep(new TutorialStep {
        title = "투자 추적하기",
        content = "축하합니다! 이제 TechCorp 주식을 보유하고 있습니다. 성과를 모니터링하는 방법을 알아보겠습니다.",
        visualAid = TutorialVisual.PortfolioDemo,
        interaction = TutorialInteraction.ExploreInterface
    });
}
```

#### 모듈 2: 위험과 수익 이해
```csharp
[System.Serializable]
public struct RiskReturnTutorial
{
    [Header("개념 소개")]
    public bool useInteractiveSimulation;   // 대화형 위험/수익 데모
    public bool enableHistoricalExamples;  // 실제 시장 예시 표시
    public bool includeVolatilityDemo;      // 가격 변동성 시연
    
    [Header("학습 활동")]
    public RiskExercise[] practiceExercises; // 실습 위험 평가
    public bool enableRiskCalculator;       // 대화형 위험 계산기
    public bool showCorrelationDemo;        // 자산 상관관계 시각화
    
    [Header("평가")]
    public int minimumScore;                // 통과를 위한 80%
    public bool enableRetakes;              // 재시도 허용
    public bool provideDetailedFeedback;   // 상세 피드백 제공
}
```

### 3.2 포트폴리오 관리

#### 모듈 3: 다변화 원칙
```csharp
[System.Serializable]
public struct DiversificationTutorial
{
    [Header("시각적 데모")]
    public bool enableEggBasketAnalogy;     // "달걀을 한 바구니에" 비유
    public bool showCorrelationMatrix;     // 자산 간 상관관계 매트릭스
    public bool demonstrateVolatilityReduction; // 변동성 감소 시연
    
    [Header("실습 구성요소")]
    public bool enablePortfolioBuilder;    // 대화형 포트폴리오 빌더
    public AssetClass[] availableAssets;   // 다변화를 위한 자산 클래스
    public bool showOptimizationResults;   // 최적화 결과 표시
    
    [Header("실무 적용")]
    public bool requireRebalancingDemo;    // 리밸런싱 데모 필수
    public float targetAllocation;         // 목표 배분 (예: 60/40)
    public bool enableCustomAllocation;    // 사용자 정의 배분
}
```

#### 모듈 4: 자산 배분 전략
```csharp
[System.Serializable]
public struct AssetAllocationTutorial
{
    [Header("배분 모델")]
    public AllocationModel[] modelPortfolios; // 연령별/목표별 모델
    public bool enableAgeBasedAllocation;   // 연령 기반 배분
    public bool showLifecycleChanges;       // 생애 주기 변화
    
    [Header("재조정 교육")]
    public bool teachRebalancingFrequency;  // 재조정 빈도 교육
    public bool demonstrateRebalancingBenefit; // 재조정 이점 시연
    public bool enableAutomaticRebalancing; // 자동 재조정 소개
    
    [Header("고급 주제")]
    public bool introduceTacticalAllocation; // 전술적 배분 소개
    public bool discussMarketTiming;        // 시장 타이밍 논의
    public bool showBehavioralPitfalls;     // 행동적 함정
}
```

### 3.3 자동화 시스템

#### 모듈 5: 투자 자동화
```csharp
[System.Serializable]
public struct AutomationTutorial
{
    [Header("자동화 유형")]
    public AutomationType[] automationTypes; // DCA, 재조정, 손절매
    public bool enableDollarCostAveraging;  // 달러 비용 평균법
    public bool showRebalancingAutomation;  // 자동 재조정
    
    [Header("전략 빌더")]
    public bool enableStrategyBuilder;      // 시각적 전략 빌더
    public StrategyTemplate[] templates;    // 미리 만든 전략 템플릿
    public bool allowCustomStrategies;     // 사용자 정의 전략
    
    [Header("백테스팅")]
    public bool enableBacktesting;          // 백테스팅 도구
    public int backtestYears;              // 백테스트 기간 년수
    public bool showPerformanceComparison; // 성과 비교
    
    [Header("위험 관리")]
    public bool teachStopLossOrders;       // 손절매 주문 교육
    public bool introduceTakeProfitOrders; // 익절 주문 소개
    public bool explainPositionSizing;     // 포지션 사이징 설명
}
```

## 4. 적응형 학습 시스템

### 4.1 개인화된 학습 경로

#### 학습 스타일 분석
```csharp
[System.Serializable]
public struct LearningStyleAnalysis
{
    [Header("학습 선호도")]
    public LearningStyle detectedStyle;     // 시각적, 청각적, 실습
    public float visualLearningWeight;      // 0.4 - 차트와 그래프 선호
    public float auditoryLearningWeight;    // 0.3 - 설명과 토론 선호
    public float kinestheticLearningWeight; // 0.3 - 실습 경험 선호
    
    [Header("콘텐츠 적응")]
    public bool enableAdaptiveContent;      // 스타일에 맞춘 콘텐츠
    public bool adjustExplanationDepth;     // 설명 깊이 조정
    public bool customizeVisualElements;    // 시각적 요소 커스터마이징
    
    [Header("진행 속도")]
    public LearningPace preferredPace;      // 빠름, 중간, 느림
    public bool enableSelfPacing;           // 자체 속도 조절
    public bool allowSkippingBasics;        // 기초 건너뛰기 허용
}

public enum LearningStyle
{
    Visual,          // 차트, 다이어그램, 인포그래픽 선호
    Auditory,        // 설명, 토론, 음성 가이드 선호
    Kinesthetic,     // 실습, 상호작용, 시뮬레이션 선호
    Reading,         // 텍스트, 문서, 상세 설명 선호
    Mixed            // 여러 스타일의 조합
}
```

#### 적응형 난이도 조정
```csharp
[System.Serializable]
public struct AdaptiveDifficultyConfig
{
    [Header("성과 추적")]
    public float comprehensionThreshold;    // 85% 이해도 목표
    public float strugglingThreshold;       // 60% 미만 시 도움 제공
    public int consecutiveErrors;           // 3회 연속 오류 시 개입
    
    [Header("지원 시스템")]
    public bool enableHintSystem;           // 점진적 힌트 시스템
    public bool offerAdditionalExamples;    // 추가 예시 제공
    public bool simplifyExplanations;       // 설명 단순화
    public bool provideAlternativeApproach; // 대안적 접근법
    
    [Header("고급 학습자")]
    public bool enableAcceleratedPath;      // 가속화된 경로
    public bool offerAdvancedChallenges;    // 고급 도전 과제
    public bool unlockBonusContent;        // 보너스 콘텐츠 잠금 해제
}
```

### 4.2 지식 평가 시스템

#### 형성 평가
```csharp
[System.Serializable]
public struct FormativeAssessmentConfig
{
    [Header("평가 유형")]
    public AssessmentType[] assessmentTypes; // 퀴즈, 시뮬레이션, 프로젝트
    public bool enableMicroAssessments;     // 작은 단위 평가
    public bool useGameBasedAssessment;     // 게임 기반 평가
    
    [Header("피드백 시스템")]
    public bool provideImmediateFeedback;   // 즉시 피드백
    public bool explainCorrectAnswers;      // 정답 설명
    public bool suggestImprovementAreas;    // 개선 영역 제안
    
    [Header("진행 추적")]
    public bool trackKnowledgeGaps;         // 지식 격차 추적
    public bool recommendRemediation;       // 보충 학습 추천
    public bool enableMasteryLearning;      // 숙련 학습 모델
}
```

#### 최종 평가
```csharp
[System.Serializable]
public struct SummativeAssessmentConfig
{
    [Header("평가 구조")]
    public AssessmentModule[] finalAssessments; // 모듈별 최종 평가
    public int passingScore;                // 합격 점수 80%
    public int maxAttempts;                 // 최대 3회 시도
    
    [Header("인증 시스템")]
    public bool enableCertification;        // 완료 인증서
    public bool issueBadges;               // 성취 배지
    public bool trackProgress;             // 진행도 추적
    
    [Header("성과 분석")]
    public bool provideDetailedResults;     // 상세 결과 제공
    public bool compareToOthers;           // 타인과 비교
    public bool suggestNextSteps;          // 다음 단계 제안
}
```

## 5. 게임화 요소

### 5.1 진행 시스템

#### 업적 및 배지
```csharp
[System.Serializable]
public struct TutorialAchievementConfig
{
    [Header("학습 업적")]
    public Achievement[] learningAchievements; // 완료, 숙련도, 속도
    public bool enableProgressBadges;       // 진행 배지
    public bool trackLearningStreaks;       // 학습 연속 일수
    
    [Header("실용 업적")]
    public Achievement[] practicalAchievements; // 첫 투자, 수익 등
    public bool rewardRealWorldApplication; // 실제 적용 보상
    public bool trackPerformanceMetrics;    // 성과 지표 추적
    
    [Header("사회적 인정")]
    public bool enableLeaderboards;         // 리더보드
    public bool allowAchievementSharing;    // 업적 공유
    public bool provideMentorRole;          // 멘토 역할 제공
}
```

#### 점수 및 포인트 시스템
```csharp
[System.Serializable]
public struct PointsSystemConfig
{
    [Header("포인트 획득")]
    public int tutorialCompletionPoints;    // 튜토리얼 완료 시 100점
    public int perfectScoreBonus;           // 만점 보너스 50점
    public int helpingOthersPoints;         // 타인 도움 시 25점
    
    [Header("포인트 사용")]
    public bool enablePointsStore;          // 포인트 상점
    public RewardItem[] availableRewards;   // 사용 가능한 보상
    public bool allowCustomization;         // 커스터마이징 항목
    
    [Header("레벨 시스템")]
    public int[] levelThresholds;          // 레벨업 임계값
    public string[] levelTitles;           // 레벨 타이틀
    public Reward[] levelRewards;          // 레벨별 보상
}
```

### 5.2 도전과 경쟁

#### 주간 도전
```csharp
[System.Serializable]
public struct WeeklyChallengeConfig
{
    [Header("도전 유형")]
    public ChallengeType[] challengeTypes;  // 학습, 성과, 창의성
    public bool rotateChallengeFocus;       // 주제 순환
    public bool enableTeamChallenges;       // 팀 도전
    
    [Header("난이도 조정")]
    public bool adaptToSkillLevel;          // 기술 수준에 맞춤
    public bool offerMultipleDifficulties;  // 여러 난이도 제공
    public bool enableBonusObjectives;      // 보너스 목표
    
    [Header("보상 구조")]
    public Reward[] completionRewards;      // 완료 보상
    public Reward[] leaderboardRewards;     // 순위 보상
    public bool enableSpecialRecognition;   // 특별 인정
}
```

## 6. 지원 시스템

### 6.1 도움말 및 FAQ

#### 맥락적 도움말
```csharp
[System.Serializable]
public struct ContextualHelpConfig
{
    [Header("도움말 시스템")]
    public bool enableInlineHelp;           // 인라인 도움말
    public bool showTooltips;              // 툴팁 표시
    public bool enableSearchableHelp;      // 검색 가능한 도움말
    
    [Header("FAQ 통합")]
    public FAQCategory[] faqCategories;     // FAQ 카테고리
    public bool enableSmartFAQ;            // 스마트 FAQ 추천
    public bool trackHelpRequests;         // 도움 요청 추적
    
    [Header("라이브 지원")]
    public bool enableChatSupport;          // 채팅 지원
    public bool connectToCommunity;         // 커뮤니티 연결
    public bool provideMentorshipProgram;   // 멘토십 프로그램
}
```

## 다음 단계

1. **[이벤트 위기 시스템](./events-crisis-system_KOR.md)** - 동적 이벤트 및 위기 관리
2. **[AI 행동 패턴](./ai-behavior-patterns_KOR.md)** - AI 의사결정 알고리즘
3. **[경제 밸런스 모델](./economy-balance-model_KOR.md)** - 경제 밸런스 매개변수

## 관련 문서

- [진행 시스템](./progression-system_KOR.md) - 플레이어 발전과 잠금 해제
- [UI/UX 디자인](./ui-ux-design_KOR.md) - 인터페이스 디자인 사양
- [자본주의 게임 디자인 문서](./capitalism-game-design-doc_KOR.md) - 전체 게임 디자인 개요