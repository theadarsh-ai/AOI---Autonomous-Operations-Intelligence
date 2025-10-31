# Design Guidelines: Autonomous MSP AI Management System

## Design Approach

**System**: Hybrid Enterprise Dashboard Pattern  
Drawing from AWS Console's information architecture, Datadog's monitoring excellence, and Linear's modern data presentation. This is a professional, information-dense operations dashboard optimized for continuous monitoring and rapid decision-making.

**Core Principles**:
- Information clarity over visual flair
- Scannable layouts for quick situational awareness
- Real-time data visibility without overwhelming cognitive load
- Professional enterprise aesthetic with modern refinement
- Efficient space utilization for multi-monitor setups

---

## Typography System

**Primary Font**: Inter (via Google Fonts CDN)  
**Monospace Font**: JetBrains Mono (for metrics, timestamps, IDs)

**Hierarchy**:
- Dashboard Title: text-2xl font-semibold (32px)
- Section Headers: text-lg font-semibold (18px)
- Card Titles: text-base font-medium (16px)
- Body Text: text-sm font-normal (14px)
- Metrics/Data: text-base font-mono font-medium (16px monospace)
- Labels/Captions: text-xs font-medium uppercase tracking-wide (12px)
- Timestamps: text-xs font-mono (12px monospace)

---

## Layout System

**Spacing Scale**: Tailwind units of **2, 3, 4, 6, 8, 12, 16**

- Component padding: p-4 to p-6
- Section spacing: space-y-6 to space-y-8
- Card gaps: gap-4 to gap-6
- Tight spacing (labels to values): gap-2
- Page margins: p-6 to p-8

**Grid Structure**:
- Main container: max-w-[1920px] mx-auto (supports wide monitors)
- Dashboard grid: grid-cols-12 for flexible layouts
- Agent cards: grid-cols-1 md:grid-cols-2 xl:grid-cols-4
- Metrics panels: grid-cols-2 lg:grid-cols-4
- Two-column splits: grid-cols-1 lg:grid-cols-2

---

## Component Library

### Navigation Structure
**Top Navigation Bar** (fixed, h-16):
- Logo/brand (left)
- Primary navigation tabs: Dashboard, Agents, Predictions, Decisions, Analytics, Settings
- Real-time status indicator (connection status icon)
- User profile + notification bell (right)

**Secondary Navigation** (when applicable):
- Breadcrumb trail for deep navigation
- View toggles (grid/list, time ranges)

### Agent Cards (8 specialized agents)
**Structure** (each agent has distinct visual identity through icons):
- Agent icon + name (header with status dot indicator)
- Current status badge (Idle/Active/Processing)
- Active tasks count + recent activity preview
- Key metrics (2-3 data points: uptime, decisions/hour, accuracy)
- Quick action button ("View Details")
- Use elevated card style with subtle border treatment

**Layout**: 4-column grid on xl screens, 2-column on md, single column on mobile

### Decision Log Feed
**Real-time scrolling feed** (right sidebar or dedicated section):
- Entry structure: timestamp + agent icon + decision summary
- Visual hierarchy: Decision type (bold) → Details (normal) → Outcome metrics
- Auto-approved items: checkmark indicator
- Escalated items: warning indicator with "Requires Approval" badge
- Entry spacing: divide-y with py-3 per item
- Limit visible items to 20, with "Load More" infinite scroll

### Predictive Timeline
**Horizontal timeline visualization**:
- Time axis: next 72 hours marked in 12-hour increments
- Event cards positioned along timeline
- Card contents: Predicted issue title, confidence score, scheduled action, impact assessment
- Visual connectors showing cause-effect relationships
- Color-coded by severity (visual treatment, not specific colors)
- Current time indicator (vertical line)

### Metrics Dashboard Panels
**Grid of metric cards** (4 columns on large screens):
- Large number display (text-3xl font-mono font-bold)
- Metric label (text-xs uppercase)
- Trend indicator (arrow + percentage change)
- Mini sparkline chart (optional for key metrics)
- Card height: h-32 for consistency

### Financial Impact Tracker
**Multi-section layout**:
- Summary cards row: Total Savings, ROI Average, Cost Avoidance, Revenue Impact
- Agent ROI comparison: horizontal bar chart showing ROI by agent
- Time-series chart: prevention savings over time (line chart)
- Breakdown table: detailed cost/benefit by action type

### Escalation Queue (Level 3 Decisions)
**Card-based queue layout**:
- Each escalation: elevated card with alert visual treatment
- Header: Decision type + timestamp + urgency level
- Context section: Why escalated, risk assessment, business impact
- Action preview: What will be executed
- Approval controls: Approve (primary) + Reject (secondary) + Request More Info
- Auto-timeout indicator if decision has deadline

### Learning Analytics Panel
**Dashboard section with charts**:
- Accuracy trend line chart (weekly/monthly view)
- Agent performance comparison (radar chart or grouped bars)
- False positive rate tracker (area chart)
- Model improvement metrics grid
- Recent optimizations feed (list format)

### Data Visualization Standards
**Charts** (use Chart.js or Recharts):
- Line charts: prediction accuracy, financial trends
- Bar charts: agent comparisons, ROI analysis
- Area charts: cumulative metrics over time
- Donut charts: decision distribution by type
- All charts: consistent axis labeling, legend placement, tooltip formatting

---

## Page Layouts

### Main Dashboard (Default View)
**3-column asymmetric layout**:
- Left column (8 cols): Agent status grid (8 cards in 2x4) + Predictive timeline below
- Right column (4 cols): Decision log feed (scrollable) + Key metrics summary

### Agent Detail View
**Full-width layout**:
- Agent header: Icon, name, overall status, uptime
- Metrics row: 4 key performance indicators
- Activity feed: Recent decisions and actions (chronological)
- Performance charts: 2-column grid with accuracy, response time, workload
- Action groups table: Available functions with execution counts

### Predictions View
**Timeline-focused**:
- Large horizontal timeline (primary focus)
- Filter controls: Time range, agent filter, severity filter
- Prediction cards below timeline in grid layout
- Confidence scoring visualization for each prediction

### Analytics View
**Multi-dashboard layout**:
- Tab navigation: Overview, Agent Performance, Financial, Learning
- Each tab: 2-3 chart sections in responsive grid
- Export controls in top-right
- Date range selector

---

## Interactive Elements

### Buttons
- Primary action: px-4 py-2 text-sm font-medium rounded-md
- Secondary action: Similar size, different visual treatment
- Icon buttons: p-2 rounded-md (for compact actions)
- Danger actions: Same structure, distinct visual treatment

### Status Indicators
- Dots: w-2 h-2 rounded-full (agent status, connection status)
- Badges: px-2 py-1 text-xs font-medium rounded-full
- Pills: px-3 py-1 text-sm rounded-full (for categories)

### Form Controls (Settings, Filters)
- Input fields: px-3 py-2 text-sm rounded-md border
- Dropdowns: Same sizing as inputs
- Toggles: Standard switch component (h-6 w-11)
- Checkboxes/Radio: Standard size with label spacing

### Tooltips & Popovers
- Tooltips: Max-width 200px, text-xs, px-2 py-1
- Info popovers: For metric definitions, triggered by info icon
- Context menus: Right-click on agent cards for quick actions

---

## Real-Time Updates

### Visual Feedback
- New decision entries: Subtle slide-in animation from top (300ms)
- Agent status changes: Pulsing dot animation on status indicator (1s)
- Metric updates: Number count-up animation for significant changes
- Live data badge: "LIVE" indicator with subtle pulse in dashboard header
- WebSocket connection status: Persistent indicator in top nav

### Loading States
- Card skeletons: Animated gradient placeholder matching card structure
- Chart loading: Spinner centered in chart container
- Inline loaders: Small spinner for action execution feedback

---

## Responsive Behavior

**Breakpoints**:
- Mobile (< 768px): Single column, stacked cards, simplified nav (hamburger)
- Tablet (768px - 1024px): 2-column grids, condensed spacing
- Desktop (1024px - 1440px): 3-column layouts, full feature set
- Wide (> 1440px): 4-column agent grid, expanded timeline view

**Mobile Optimizations**:
- Bottom tab navigation for primary sections
- Collapsible decision feed (drawer from bottom)
- Simplified metrics (show top 4 only)
- Timeline becomes vertical scroll

---

## Icons

**Library**: Heroicons (via CDN)  
**Usage**:
- Agent type icons: Unique icon per agent (8 total) - e.g., ChartBarIcon, ShieldCheckIcon, CurrencyDollarIcon
- Status icons: CheckCircleIcon, ExclamationTriangleIcon, ClockIcon
- Navigation: HomeIcon, BellIcon, CogIcon, UserCircleIcon
- Actions: PlayIcon, PauseIcon, ArrowPathIcon, EyeIcon

---

## Accessibility

- Semantic HTML: proper heading hierarchy, ARIA labels for charts
- Keyboard navigation: All interactive elements focusable, logical tab order
- Status communication: Text labels accompany visual indicators
- Contrast: All text meets WCAG AA standards against backgrounds
- Screen reader: Live region announcements for real-time updates

---

## Images

**No hero images** - This is a data-focused enterprise dashboard. All visuals are functional (charts, graphs, icons, agent visualization diagrams).

**Optional visual elements**:
- Empty states: Illustration or icon when no data (e.g., "No predictions in next 48 hours")
- Agent architecture diagram: SVG flowchart showing agent relationships (in documentation/about section)