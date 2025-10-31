# MSP AI Orchestrator - Autonomous Multi-Agent Management System

## Overview

A fully autonomous AI-powered MSP (Managed Service Provider) management system that operates 24/7 without human intervention. The system uses AWS Bedrock and the Strands Agents framework to create 8 specialized AI agents that predict IT problems 24-48 hours in advance, make autonomous business decisions, and optimize MSP operations.

The application features a hybrid architecture combining a Python FastAPI backend (with Strands Agents for autonomous decision-making) and a React TypeScript frontend (with real-time dashboard visualizations). The system can run in simulation mode without AWS credentials or with full AWS Bedrock integration using Claude Sonnet.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- React 18 with TypeScript
- Vite as build tool and development server
- Tailwind CSS for styling with custom design system
- Wouter for client-side routing
- TanStack Query for data fetching and caching

**UI Framework:**
- Radix UI primitives for accessible components
- shadcn/ui component library (New York style variant)
- Custom design guidelines following enterprise dashboard patterns (AWS Console, Datadog, Linear)
- Recharts for data visualization and analytics charts

**Component Architecture:**
- Modular component design with TypeScript interfaces
- Reusable UI components in `/client/src/components/ui/`
- Feature components for agents, decisions, predictions, and metrics
- Real-time WebSocket integration for live updates
- Theme support (light/dark mode with localStorage persistence)

**State Management:**
- WebSocket manager for real-time backend communication
- Local state with React hooks (useState, useEffect)
- Mock data fallback when backend is unavailable
- TanStack Query for API data synchronization

### Backend Architecture

**Technology Stack:**
- Python FastAPI for REST API and WebSocket server
- Strands Agents framework (AWS official SDK) for multi-agent orchestration
- Uvicorn ASGI server
- AWS Bedrock integration (optional, falls back to simulation mode)

**Multi-Agent System:**
The system implements 8 specialized AI agents using the Strands framework:

1. **Master Orchestrator Agent** - Coordinates all sub-agents, maintains global state, resolves conflicts
2. **Predictive Monitoring Agent** - Analyzes metrics, predicts failures 24-48 hours ahead
3. **Autonomous Decision Agent** - Makes business decisions within defined autonomy levels
4. **Client Lifecycle Agent** - Automates onboarding, health monitoring, renewals
5. **Resource Optimization Agent** - Assigns technicians, optimizes schedules
6. **Financial Intelligence Agent** - Analyzes profitability, adjusts pricing
7. **Security & Compliance Agent** - Monitors security, auto-remediates vulnerabilities
8. **Learning & Adaptation Agent** - Analyzes outcomes, improves models

**Agent Tools:**
- Monitoring tools: system analysis, failure prediction, risk assessment
- Decision tools: approval evaluation, ROI calculation, execution
- Resource tools: technician assignment, schedule optimization
- Security tools: vulnerability scanning, auto-remediation

**API Architecture:**
- RESTful endpoints for agents, decisions, predictions, metrics
- WebSocket endpoint (`/ws`) for real-time bidirectional communication
- CORS middleware configured for React frontend
- Automatic mock/simulation mode when AWS credentials unavailable

**Autonomy Levels:**
- Level 1 (Full Autonomy): <$2K actions auto-approved
- Level 2 (Conditional): <$10K actions auto-approved
- Level 3 (Human Required): >$10K actions escalated

### Data Storage Solutions

**Current Implementation:**
- In-memory storage for demonstration/simulation mode
- Database schema defined using Drizzle ORM with PostgreSQL dialect
- Schema includes user table with username/password fields
- Storage interface (`IStorage`) designed for CRUD operations

**Database Configuration:**
- Drizzle Kit configured for PostgreSQL migrations
- Schema location: `/shared/schema.ts`
- Migration output: `/migrations`
- Database URL expected via `DATABASE_URL` environment variable

**Note:** While Drizzle schema is configured for PostgreSQL, the application currently uses in-memory storage. Database integration can be added by implementing the storage interface with Drizzle queries.

### Authentication and Authorization

**Current State:**
- User schema defined with username/password fields
- No active authentication implementation in current codebase
- Storage interface includes user creation and lookup methods
- Ready for authentication layer implementation

**Agent Autonomy System:**
- Three-tier autonomy levels for decision-making
- Cost-based approval thresholds
- ROI calculation for preventive actions
- Escalation queue for human review of high-risk decisions

### Real-Time Communication

**WebSocket Implementation:**
- Custom WebSocket manager class (`/client/src/lib/websocket.ts`)
- Automatic reconnection with exponential backoff
- Message type routing for different update types
- Connection status monitoring
- Broadcast capability for multiple connected clients

**Message Types:**
- `system_update`: Agent status, metrics, decisions
- Real-time agent activity updates
- Live decision log entries
- Prediction timeline updates
- Performance metrics streaming

## External Dependencies

### Third-Party Services

**AWS Bedrock (Optional):**
- Claude 3.5 Sonnet model for AI agent intelligence
- Requires AWS account with Bedrock access enabled
- Credentials: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
- Falls back to simulation mode when unavailable

**Strands Agents Framework:**
- AWS official SDK for autonomous agent orchestration
- Provides @tool decorator for agent action groups
- Manages agent coordination and decision-making logic

### Frontend Dependencies

**Core Libraries:**
- React 18 with TypeScript
- Vite for development and bundling
- Wouter for routing
- TanStack Query for data management

**UI Components:**
- @radix-ui/* components (18+ packages for primitives)
- class-variance-authority for component variants
- tailwind-merge and clsx for className utilities
- lucide-react for icons
- recharts for data visualization
- embla-carousel-react for carousels

**Form Handling:**
- react-hook-form for form management
- @hookform/resolvers for validation
- zod for schema validation

### Backend Dependencies

**Python Packages:**
- FastAPI for web framework
- Uvicorn for ASGI server
- Strands SDK for agent framework
- AWS Bedrock integration (optional)

### Development Tools

**Build Tools:**
- esbuild for server bundling
- TypeScript compiler for type checking
- PostCSS with Tailwind and Autoprefixer

**Replit Integration:**
- @replit/vite-plugin-runtime-error-modal
- @replit/vite-plugin-cartographer (dev only)
- @replit/vite-plugin-dev-banner (dev only)

### Database & ORM

**Drizzle ORM:**
- drizzle-orm for database operations
- drizzle-kit for migrations
- drizzle-zod for schema validation
- @neondatabase/serverless for PostgreSQL connection
- Configured but not actively used (in-memory storage currently)

### Fonts

**External Resources:**
- Google Fonts: Inter (primary UI font, weights 400-700)
- Google Fonts: JetBrains Mono (monospace for metrics/data, weights 400-600)