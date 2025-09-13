---
category: gamedesign
tags: [game-design, investment, mechanics, portfolio, trading, automation]
related: [core-gameplay-loop.md, capitalism-game-design-doc.md]
parent: INDEX.md
created: 2025-09-13
updated: 2025-09-13
priority: high
---

# Investment Loop Mechanics - Detailed Design

[🇰🇷 한국어 버전](./investment-loop-mechanics_KOR.md)

## 📍 Navigation

[↩️ Back to Game Design](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## 1. Investment Loop Overview

The Investment Loop is the primary economic engine of YouAreCapitalist, representing the core mechanism through which players interact with financial markets and grow their capital. This loop evolves from hands-on trading to fully automated capital allocation as players progress.

### 1.1 Loop Flow Diagram

```
💰 CAPITAL ALLOCATION
    ↓ (Decision: Where to invest available capital)
📊 MARKET ANALYSIS
    ├── Technical Analysis (Charts, patterns, indicators)
    ├── Fundamental Analysis (Company financials, economics)
    ├── Sentiment Analysis (News, social media, market mood)
    └── AI Advisor Input (Algorithm recommendations)
    ↓ (Decision: Which assets to target)
🎯 INVESTMENT DECISION
    ├── Asset Selection (Stocks, bonds, derivatives, alternatives)
    ├── Position Sizing (How much to invest)
    ├── Risk Management (Stop-losses, hedging)
    └── Timeline Setting (Short, medium, long-term)
    ↓ (Execution: Place orders, manage positions)
📈 POSITION MANAGEMENT
    ├── Performance Monitoring (Real-time P&L tracking)
    ├── Rebalancing Triggers (Automated adjustments)
    ├── Exit Strategy Execution (Profit-taking, loss-cutting)
    └── Optimization (Tax efficiency, cost reduction)
    ↓ (Outcome: Realize gains/losses)
💵 CAPITAL GROWTH/LOSS
    ├── Reinvestment Decisions (Compound vs. withdraw)
    ├── Leverage Adjustment (Risk appetite changes)
    ├── Portfolio Diversification (Risk distribution)
    └── Strategy Evolution (Learning from results)
    ↓ (Return to start with modified capital base)
```

## 2. Market Analysis System

### 2.1 Technical Analysis Engine

#### Price Pattern Recognition
- **Chart Patterns**: Head and shoulders, triangles, channels, flags
- **Candlestick Patterns**: Doji, hammer, engulfing, shooting star
- **Support/Resistance**: Dynamic levels based on historical price action
- **Trend Analysis**: Moving averages, trend lines, momentum indicators

#### Technical Indicators
```yaml
Momentum Indicators:
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Stochastic Oscillator
  - Williams %R

Trend Indicators:
  - Moving Averages (SMA, EMA, WMA)
  - Bollinger Bands
  - Parabolic SAR
  - Ichimoku Cloud

Volume Indicators:
  - On-Balance Volume (OBV)
  - Volume Weighted Average Price (VWAP)
  - Accumulation/Distribution Line
  - Chaikin Money Flow

Volatility Indicators:
  - Average True Range (ATR)
  - Volatility Index (VIX equivalent)
  - Standard Deviation
  - Donchian Channels
```

#### Algorithm Scoring System
- **Signal Strength**: 0-100 scale for each indicator
- **Confluence**: Multiple indicator agreement weighting
- **Reliability**: Historical accuracy tracking per indicator
- **Market Regime**: Bull/bear/sideways market adjustments

### 2.2 Fundamental Analysis Framework

#### Company-Level Analysis
```yaml
Financial Health:
  - Revenue Growth: YoY and QoQ trends
  - Profitability: Gross/Operating/Net margins
  - Debt Management: Debt-to-equity, interest coverage
  - Cash Flow: Operating/Free cash flow generation
  - Return Metrics: ROE, ROA, ROIC

Valuation Metrics:
  - Price Ratios: P/E, P/B, P/S, PEG
  - Enterprise Value: EV/EBITDA, EV/Sales
  - Dividend Yield: Current and projected
  - Intrinsic Value: DCF, DDM calculations

Competitive Position:
  - Market Share: Industry positioning
  - Moat Strength: Competitive advantages
  - Management Quality: Leadership effectiveness
  - Innovation Pipeline: R&D investment, patents
```

#### Macro-Economic Analysis
```yaml
Economic Indicators:
  - GDP Growth: National economic health
  - Inflation: CPI, PPI trends
  - Interest Rates: Central bank policy
  - Employment: Unemployment, job creation

Market Conditions:
  - Sector Rotation: Industry performance cycles
  - Risk Appetite: Safe haven vs. risk assets
  - Liquidity: Money supply, credit conditions
  - Geopolitical: Trade, conflicts, sanctions

Currency & International:
  - Exchange Rates: Currency strength impacts
  - International Trade: Import/export dynamics
  - Global Markets: Correlation analysis
  - Commodity Prices: Resource cost impacts
```

### 2.3 Sentiment Analysis System

#### News Impact Engine
- **Source Credibility**: Weight news by source reliability
- **Sentiment Scoring**: Natural language processing for mood
- **Event Classification**: Earnings, M&A, regulatory, scandal
- **Market Reaction Prediction**: Historical response patterns

#### Social Media Integration
- **Influencer Tracking**: Key opinion leaders in finance
- **Retail Sentiment**: Social media buzz analysis
- **Viral Trends**: Meme stock phenomena simulation
- **Contrarian Signals**: Crowd sentiment reversals

#### Market Psychology Indicators
- **Fear & Greed Index**: Market emotion measurement
- **Options Flow**: Put/call ratios, unusual activity
- **Insider Trading**: Corporate insider buy/sell patterns
- **Analyst Upgrades/Downgrades**: Professional sentiment shifts

## 3. Investment Decision Framework

### 3.1 Asset Classification System

#### Traditional Securities
```yaml
Equities:
  Large Cap: Established companies, stable returns
  Mid Cap: Growth potential, moderate risk
  Small Cap: High growth, high volatility
  Micro Cap: Speculative, extreme volatility

Fixed Income:
  Government Bonds: Risk-free rate benchmarks
  Corporate Bonds: Credit risk vs. yield
  Municipal Bonds: Tax advantages
  International Bonds: Currency exposure

Preferred Stock:
  Dividend Priority: Income focus
  Conversion Features: Equity upside potential
  Credit Quality: Corporate stability
```

#### Alternative Investments
```yaml
Real Estate:
  REITs: Liquid real estate exposure
  Direct Property: Illiquid, leverage opportunities
  Real Estate Development: High risk/reward

Commodities:
  Precious Metals: Gold, silver inflation hedges
  Energy: Oil, gas supply/demand dynamics
  Agriculture: Food price inflation exposure
  Industrial Metals: Economic cycle sensitivity

Private Equity:
  Buyouts: Mature company improvements
  Venture Capital: Early-stage technology
  Growth Capital: Expansion financing
  Distressed: Turnaround opportunities
```

#### Derivatives & Structured Products
```yaml
Options:
  Call Options: Bullish speculation, leverage
  Put Options: Bearish speculation, hedging
  Complex Strategies: Spreads, straddles, collars

Futures:
  Index Futures: Market exposure, hedging
  Commodity Futures: Price speculation/hedging
  Currency Futures: Exchange rate plays

Structured Products:
  Market-Linked CDs: Principal protection
  Equity-Linked Notes: Customized exposure
  Synthetic Products: Engineering returns
```

### 3.2 Position Sizing Algorithm

#### Risk-Based Sizing
```python
# Kelly Criterion Implementation
def kelly_criterion(win_probability, avg_win, avg_loss):
    if avg_loss == 0:
        return 0
    win_loss_ratio = avg_win / avg_loss
    kelly_percentage = win_probability - ((1 - win_probability) / win_loss_ratio)
    return max(0, min(kelly_percentage, 0.25))  # Cap at 25% per position

# Risk Parity Approach
def risk_parity_sizing(portfolio_volatility_target, asset_volatility, correlation_matrix):
    # Equal risk contribution across positions
    risk_budget = portfolio_volatility_target / len(assets)
    position_size = risk_budget / (asset_volatility * correlation_adjustment)
    return position_size

# Dynamic Sizing Based on Market Conditions
def adaptive_position_sizing(base_size, market_volatility, account_size, drawdown_level):
    volatility_adjustment = 1 / (1 + market_volatility)
    drawdown_adjustment = 1 - (drawdown_level * 0.5)
    size_modifier = volatility_adjustment * drawdown_adjustment
    return base_size * size_modifier
```

#### Capital Allocation Rules
- **Maximum Single Position**: 10% of portfolio (early game) → 25% (late game)
- **Sector Concentration**: No more than 30% in single sector
- **Correlation Limits**: Avoid highly correlated positions
- **Liquidity Requirements**: Maintain 5-15% cash buffer

### 3.3 Risk Management Framework

#### Stop-Loss Strategies
```yaml
Fixed Percentage:
  Conservative: 5% below entry
  Moderate: 10% below entry
  Aggressive: 15% below entry

Technical Stops:
  Support Levels: Below key support
  Moving Averages: Below 20/50/200 MA
  Volatility-Based: ATR multiple stops

Time-Based Stops:
  Earnings Windows: Exit before earnings
  Economic Events: Fed meetings, GDP releases
  Position Age: Automatic review after X days
```

#### Hedging Mechanisms
```yaml
Portfolio Hedging:
  Index Puts: Market crash protection
  VIX Calls: Volatility spike insurance
  Currency Hedging: International exposure protection

Position Hedging:
  Protective Puts: Individual stock protection
  Collar Strategies: Upside/downside limits
  Pair Trading: Long/short related stocks

Dynamic Hedging:
  Delta Hedging: Options portfolio neutrality
  Gamma Hedging: Convexity risk management
  Vega Hedging: Volatility risk control
```

## 4. Automation System Design

### 4.1 Automation Levels

#### Level 0: Manual Trading
```yaml
Player Control: 100%
Characteristics:
  - Every trade requires explicit approval
  - Real-time market monitoring necessary
  - High learning curve, maximum engagement
  - Suitable for: Tutorial, early game, learning phase

Features:
  - Order entry confirmation dialogs
  - Real-time P&L alerts
  - News notification system
  - Basic charting tools
```

#### Level 1: Assisted Trading
```yaml
Player Control: 80%
Characteristics:
  - AI provides recommendations with rationale
  - Player makes final decisions
  - Risk warnings and position sizing suggestions
  - Suitable for: Early to mid-game transition

Features:
  - Signal alerts with confidence scores
  - Automated stop-loss placement
  - Position sizing recommendations
  - Risk metrics dashboard
```

#### Level 2: Algorithmic Trading
```yaml
Player Control: 50%
Characteristics:
  - Predefined rules execute automatically
  - Player sets parameters and constraints
  - Intervention possible on major decisions
  - Suitable for: Mid-game portfolio management

Features:
  - Rule-based strategy deployment
  - Automated rebalancing
  - Risk-based position scaling
  - Performance attribution analysis
```

#### Level 3: AI Portfolio Management
```yaml
Player Control: 20%
Characteristics:
  - Machine learning optimizes decisions
  - Player provides high-level objectives
  - Automatic adaptation to market conditions
  - Suitable for: Late-game capital allocation

Features:
  - Multi-factor model optimization
  - Dynamic strategy switching
  - Cross-asset arbitrage
  - Alternative data integration
```

#### Level 4: Autonomous Capital Allocation
```yaml
Player Control: 5%
Characteristics:
  - Fully autonomous investment decisions
  - Player only sets risk tolerance
  - Self-improving through reinforcement learning
  - Suitable for: End-game passive income

Features:
  - Unsupervised learning algorithms
  - Multi-timeframe optimization
  - Cross-market opportunity scanning
  - Systemic risk monitoring
```

### 4.2 Algorithm Development Progression

#### Strategy Template System
```yaml
Template Categories:
  Momentum: Trend-following strategies
  Mean Reversion: Contrarian approaches
  Value: Fundamental analysis based
  Growth: Growth stock identification
  Income: Dividend/yield focused
  Arbitrage: Price discrepancy exploitation

Customization Options:
  - Entry/exit criteria modification
  - Risk parameter adjustment
  - Timeframe selection
  - Asset universe definition
  - Correlation constraints
```

#### Machine Learning Integration
```python
# Strategy Performance Prediction
class StrategyPerformanceML:
    def __init__(self):
        self.features = [
            'market_volatility', 'economic_cycle', 'sector_rotation',
            'interest_rate_environment', 'geopolitical_risk'
        ]
    
    def predict_strategy_success(self, strategy_type, market_conditions):
        # Random Forest for strategy selection
        model = RandomForestRegressor()
        prediction = model.predict(market_conditions)
        confidence = model.feature_importances_
        return prediction, confidence

# Portfolio Optimization Engine
class PortfolioOptimizer:
    def optimize_allocation(self, expected_returns, covariance_matrix, risk_tolerance):
        # Modern Portfolio Theory implementation
        # Black-Litterman model for return estimates
        # Risk parity adjustments
        optimal_weights = self.solve_optimization(expected_returns, covariance_matrix)
        return optimal_weights
```

## 5. Performance Monitoring & Feedback

### 5.1 Real-Time Performance Metrics

#### Portfolio Dashboard
```yaml
Core Metrics:
  Total Portfolio Value: Real-time mark-to-market
  Daily P&L: Absolute and percentage changes
  Unrealized P&L: Paper gains/losses
  Realized P&L: Booked profits/losses

Risk Metrics:
  Portfolio Beta: Market sensitivity
  Value at Risk (VaR): Downside risk estimate
  Maximum Drawdown: Peak-to-trough decline
  Sharpe Ratio: Risk-adjusted returns

Performance Attribution:
  Asset Allocation: Strategy contribution
  Security Selection: Stock picking skill
  Market Timing: Entry/exit effectiveness
  Currency Impact: FX contribution
```

#### Benchmark Comparison
```yaml
Index Benchmarks:
  Broad Market: S&P 500, Total Stock Market
  Sector Specific: Technology, Healthcare, Financials
  Style Boxes: Large Growth, Small Value, etc.
  International: MSCI World, Emerging Markets

Peer Comparison:
  Other AI Capitalists: Relative performance
  Investment Funds: Mutual fund/ETF comparison
  Hedge Fund Strategies: Alternative benchmarks

Alpha Generation:
  Active Return: Excess return vs. benchmark
  Information Ratio: Active return per unit risk
  Tracking Error: Volatility of active returns
  Hit Rate: Percentage of winning trades
```

### 5.2 Learning & Adaptation System

#### Performance Analysis Engine
```python
class PerformanceAnalyzer:
    def analyze_trade_performance(self, trades_history):
        metrics = {
            'win_rate': self.calculate_win_rate(trades_history),
            'avg_win_loss_ratio': self.calculate_win_loss_ratio(trades_history),
            'profit_factor': self.calculate_profit_factor(trades_history),
            'maximum_drawdown': self.calculate_max_drawdown(trades_history),
            'sharpe_ratio': self.calculate_sharpe_ratio(trades_history),
            'calmar_ratio': self.calculate_calmar_ratio(trades_history)
        }
        return metrics
    
    def identify_performance_patterns(self, trades_history):
        # Time-based patterns
        time_analysis = self.analyze_by_time_periods(trades_history)
        
        # Market condition patterns
        market_analysis = self.analyze_by_market_conditions(trades_history)
        
        # Strategy patterns
        strategy_analysis = self.analyze_by_strategy_type(trades_history)
        
        return {
            'time_patterns': time_analysis,
            'market_patterns': market_analysis,
            'strategy_patterns': strategy_analysis
        }
```

#### Adaptive Strategy Tuning
```yaml
Parameter Optimization:
  Entry Thresholds: Signal strength requirements
  Exit Rules: Profit-taking and stop-loss levels
  Position Sizing: Risk-based allocation adjustments
  Timeframes: Holding period optimization

Market Regime Detection:
  Bull Markets: Momentum strategies favored
  Bear Markets: Defensive positioning
  Sideways Markets: Range-trading strategies
  High Volatility: Reduced position sizes

Strategy Switching:
  Performance Triggers: Underperformance thresholds
  Market Triggers: Regime change detection
  Time Triggers: Periodic strategy review
  Risk Triggers: Drawdown limits exceeded
```

## 6. Integration with Other Game Systems

### 6.1 Corporate Control Integration
- **Shareholder Rights**: Voting power based on shareholdings
- **Dividend Income**: Regular income stream from holdings
- **M&A Opportunities**: Takeover bids and defenses
- **Information Advantage**: Insider access to company data

### 6.2 Market Influence Integration
- **Policy Impact**: Regulatory changes affect portfolio
- **Lobbying ROI**: Political investments create market opportunities
- **Industry Influence**: Sector manipulation capabilities
- **Crisis Exploitation**: Profit from market instability

### 6.3 Capital Growth Integration
- **Reinvestment Decisions**: Compound growth vs. consumption
- **Leverage Utilization**: Debt financing for larger positions
- **Tax Optimization**: Strategies to minimize tax burden
- **Estate Planning**: Generational wealth transfer

## 7. Educational Elements

### 7.1 Concept Introduction
- **Risk vs. Return**: Fundamental investment principle
- **Diversification**: Portfolio theory basics
- **Market Efficiency**: Information flow and pricing
- **Behavioral Finance**: Psychology of investing

### 7.2 Advanced Concepts
- **Options Strategies**: Complex derivative use
- **Portfolio Theory**: Modern portfolio optimization
- **Alternative Investments**: Beyond traditional assets
- **Quantitative Finance**: Mathematical modeling

### 7.3 Real-World Application
- **Historical Simulations**: Famous market events
- **Contemporary Issues**: Current market dynamics
- **Regulatory Environment**: Rules and compliance
- **Global Markets**: International investing

## 8. Balancing & Difficulty Scaling

### 8.1 Market Response to Player Actions
- **Large Position Impact**: Price movement from big trades
- **Front-Running**: Information leakage on large orders
- **Market Manipulation**: Detection and penalties
- **Liquidity Constraints**: Size limitations on trades

### 8.2 Competitive Elements
- **AI Capitalist Behavior**: Sophisticated opponent strategies
- **Information Asymmetry**: Different access to data
- **Resource Competition**: Limited opportunities
- **Alliance Formation**: Collaborative strategies

### 8.3 Economic Realism
- **Transaction Costs**: Brokerage fees and spreads
- **Tax Implications**: Capital gains and dividend taxes
- **Regulatory Constraints**: Investment restrictions
- **Market Cycles**: Bull/bear market alternation

---

*This investment loop forms the foundation of the capitalist experience, evolving from hands-on trading education to passive wealth accumulation through automated systems.*