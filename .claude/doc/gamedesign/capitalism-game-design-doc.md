---
category: gamedesign
tags: [game-design, capitalism, simulation, economy, sandbox]
related: []
parent: INDEX.md
created: 2025-08-28
updated: 2025-08-28
priority: high
---

# Capitalism Market Simulation Game - Design Document

[🇰🇷 한국어 버전](./capitalism-game-design-doc_KOR.md)

## 📍 Navigation

[↩️ Back to Game Design](./INDEX.md) | [📚 Documentation Index](../INDEX.md) | [🏠 Home](../../../CLAUDE.md)

## 1. Game Overview

### 1.1 Core Concept
An immersive sandbox simulation game where players become capitalists and experience the logic of capital within an autonomous market economy system. Players influence the world indirectly through capital allocation and strategic decision-making rather than direct manipulation.

### 1.2 Game Philosophy
- **"A game you don't have to play"**: A fully automatable system that ultimately provides the true capitalist experience of capital making money by itself
- **"The Invisible Hand"**: Players don't manage directly but intervene indirectly through capital and influence
- **Balance of educational value and fun**: Learning real capitalist market economy principles step by step while pursuing entertainment as a game

### 1.3 Target Experience
- Early Stage: Learning basic market economy as a small-scale capitalist making direct investment decisions
- Mid Stage: Managing efficient portfolios using automation systems
- Late Stage: Establishing macroscopic strategies while observing a fully automated capital empire
- Final Stage: Experiencing the essential mechanism of capitalism where capital begets capital

## 2. Core System Structure

### 2.1 Basic Economic Units

#### Capitalist
- **Player**: The capitalist directly controlled by the user
- **AI Capitalists**: Competition/cooperation partners with their own tendencies and strategies
- Capitalists don't manage directly but only perform capital allocation and decision-making

#### Pop
- Autonomous citizen groups
- Automatically perform economic activities like labor, consumption, and savings
- Make decisions by analyzing their status and market conditions
- Different behavior patterns by class (low income/middle class/high income)

#### Company
- Economic entities that hire pops and produce goods/services
- Can automatically establish, grow, bankrupt, and merge
- Tradable shares (listed/unlisted distinction)
- Indirect management system through CEOs

### 2.2 Automation System

#### Capital Allocation Mechanism
- When players allocate capital to each area, that part becomes automated
- Real-time switching between automation ON/OFF
- Intervention possible when important events occur even during automation

#### Automatable Areas
- **Investment Management**: Automatic portfolio rebalancing
- **Company Management**: Autonomous management through CEOs
- **Financial Trading**: Automatic trading, hedging, arbitrage
- **Political Lobbying**: Regular lobbying fund execution
- **R&D Investment**: Automatic investment in technological innovation fields

#### Event-Based Intervention
- **Daily Events**: Automatic processing (quarterly results, dividends, etc.)
- **Important Events**: Optional intervention (recalls, strikes, etc.)
- **Major Events**: Required intervention (hostile M&A, financial crisis, etc.)
- **Black Swan**: Unpredictable large events

## 3. Major Game Systems

### 3.1 Financial System

#### Banking and Credit Creation
- Leverage investment through loans
- Differentiated loan conditions based on credit rating
- Chain reaction of loans and bubble formation mechanism
- Ripple effects of central bank interest rate policy

#### Stock Market
- IPO (Initial Public Offering) participation
- Real-time stock price fluctuations and trading
- Management rights exercise based on shareholding ratio
- Hostile M&A and defense strategies
- Insider trading and market manipulation (with risks)

#### Derivatives
- Hedging and speculation through futures/options
- High-risk high-return strategies using leverage
- Complex financial products like Credit Default Swaps (CDS)
- Derivative bubbles and systemic risk

### 3.2 Indirect Control System

#### CEO System
- Authority to appoint/dismiss CEOs based on shareholding ratio
- Different management styles by CEO characteristics
- Relationship management with CEOs (loyalty, independence)
- Securing management rights through shareholder alliances

#### Technological Innovation
- Capital input increases innovation probability (no guarantee)
- Different base innovation probability and investment efficiency by sector
- Prerequisite technology requirements
- Market preemption effect upon successful innovation

#### Government Policy
- Influence policy direction with lobbying funds (probabilistic)
- Lobbying competition with other stakeholders
- Market changes according to regulatory relaxation/strengthening
- Risks and rewards of political-business collusion

#### Global Economy
- Unpredictable external shocks
- Indirect prediction through economic indicators
- International trade and exchange rate fluctuations
- Global financial crisis scenarios

### 3.3 Market Dynamics System

#### Supply-Demand Mechanism
- Demand changes according to pop income and consumption patterns
- Automatic adjustment of company production volume and prices
- Overproduction and inventory problems
- Monopoly formation and price collusion

#### Economic Cycles
- Natural cycle of boom-slowdown-recession-recovery
- Differentiated optimal investment strategies for each phase
- Leading/coincident/lagging economic indicators
- Choice between contrarian and momentum investing

#### Bubbles and Crashes
- Speculative psychology and herd behavior
- Excessive leverage and credit crunch
- Bank runs and chain bankruptcies
- Government bailouts and moral hazard

## 4. Game Progression Structure

### 4.1 Starting Conditions

#### Initial Capital Settings
- 10 million won (Extreme difficulty)
- 100 million won (Hard)
- 1 billion won (Normal)
- 10 billion won (Easy)
- Custom settings

#### Scenario Mode
- Before 1997 IMF Crisis
- Before 2008 Financial Crisis
- Before 2020 Pandemic
- Before 202X AI Revolution
- Random economic situation

### 4.2 Progression Phases

#### Phase 1: Small Investor (Assets ~1 billion)
- Basic stock investment
- Small-scale startup
- Simple financial product utilization

#### Phase 2: Mid-tier Capitalist (Assets 1-10 billion)
- Multiple company shareholdings
- Beginning to use derivatives
- Elementary lobbying activities

#### Phase 3: Major Capitalist (Assets 10 billion-1 trillion)
- M&A and corporate control
- Complex financial engineering utilization
- Exercising political influence

#### Phase 4: Conglomerate (Assets over 1 trillion)
- Industrial ecosystem dominance
- Systemic influence
- Controlling economic policy

### 4.3 Victory Conditions

#### Various Endings
- **Capital Empire**: Achieving specific asset scale
- **Industrial Dominance**: Monopolizing specific industries
- **Shadow Government**: Maximizing political influence
- **System Collapse**: Destroying the economic system itself
- **Complete Automation**: Achieving 100% automation

## 5. Balancing and Check Systems

### 5.1 Dynamic Difficulty Adjustment

#### Economic Checks
- Competitor alliances during monopoly
- Price competition during excessive profits
- New entrants when abusing market power

#### Political Checks
- Political scandals from excessive lobbying
- Strengthened antitrust regulations
- Spread of anti-corporate sentiment

#### Social Checks
- Strikes during labor exploitation
- Boycotts during environmental destruction
- Social unrest from wealth inequality

#### Systemic Checks
- Financial crisis from excessive leverage
- Collapse when bubbles form
- Revolution during extreme inequality

### 5.2 AI Capitalist Behavior Patterns

#### Strategy by Tendency
- **Conservative**: Stable dividend stocks, low leverage
- **Aggressive**: High-risk speculation, hostile M&A
- **Innovative**: New technology investment, startup nurturing
- **Political**: Utilizing lobbying and regulations

#### Cooperation and Competition
- Consortium formation
- Collusion and betrayal
- Information sharing and concealment
- Temporary alliances and dissolution

## 6. Educational Design

### 6.1 Learning Objectives by Stage

#### Beginner (Tutorial~Early Game)
- Concepts of stocks, bonds, dividends
- Principles of supply and demand
- Interest and compound effect

#### Intermediate (Mid Game)
- Leverage and risk
- Understanding economic cycles
- Portfolio theory

#### Advanced (Late Game)
- Derivatives and hedging
- Credit creation mechanism
- Systemic risk

#### Expert (End Game)
- Reality of financial engineering
- Essence of the capitalist system
- Structural causes of economic crises

### 6.2 Learning Support System

#### Economic News
- Real-time market situation commentary
- Cause and effect relationship explanations
- Historical case comparisons

#### AI Advisor
- Guide for beginners
- Decision outcome predictions
- Alternative strategy suggestions

#### Analysis Reports
- Monthly/annual performance analysis
- Success and failure factor diagnosis
- Improvement suggestions

## 7. Technical Considerations

### 7.1 Simulation Depth
- Individual simulation of tens of thousands of Pops
- Real-time market price formation
- Complex economic indicator linkage
- Chain effects and feedback loops

### 7.2 UI/UX Design Direction
- Intuitive visualization of complex information
- At-a-glance automation status
- Important event notification system
- Multi-layered information depth (simple~detailed)

### 7.3 Performance Optimization
- Simplified calculations for automated parts
- Abstraction of non-critical calculations
- Omitting detailed simulation during time acceleration
- Seamless play through asynchronous processing

## 8. Expandability

### 8.1 Additional Content
- New financial products
- Additional industry sectors
- Historical scenarios
- Multiplayer mode

### 8.2 Modding Support
- Economic parameter adjustment
- Custom event creation
- AI behavior pattern modification
- Adding new industries/products

## 9. The Game's Message

This game goes beyond simple economic simulation, allowing players to experience the operating principles of the modern capitalist system and the power and limitations individuals have within it. Players become capitalists who utilize the system while simultaneously experiencing the process of becoming part of that system.

Ultimately, at the moment it becomes "a game you don't have to play," players will naturally understand the essential mechanism of capitalism where capital begets capital, and the social implications it creates.