# 🎯 Workflow Diagrams

Visual representations of all workflows and CI/CD processes in the n8n-cursor-integration project.

## 🔄 CI/CD Pipeline Flow

```mermaid
graph TD
    A[Code Push/PR] --> B{Lint & Format}
    B -->|Pass| C[Unit Tests]
    B -->|Fail| B1[Fix Code Quality]
    B1 --> B
    
    C -->|Pass| D[Integration Tests]
    C -->|Fail| C1[Fix Unit Tests]
    C1 --> C
    
    D -->|Pass| E[Docker Tests]
    D -->|Fail| D1[Fix Integration]
    D1 --> D
    
    E -->|Pass| F[Security Scan]
    E -->|Fail| E1[Fix Docker Issues]
    E1 --> E
    
    F -->|Pass| G{Branch Check}
    F -->|Fail| F1[Fix Security Issues]
    F1 --> F
    
    G -->|Main Branch| H[Deploy to Staging]
    G -->|Other Branch| I[End - PR Review]
    
    H -->|Success| J{Tag Check}
    H -->|Fail| H1[Rollback Staging]
    
    J -->|Tagged Release| K[Deploy to Production]
    J -->|No Tag| L[End - Staging Only]
    
    K -->|Success| M[Post-Deploy Health Check]
    K -->|Fail| K1[Rollback Production]
    
    M -->|Pass| N[Success - Notify Team]
    M -->|Fail| M1[Alert & Investigate]
    
    classDef success fill:#d4edda,stroke:#155724,color:#155724
    classDef failure fill:#f8d7da,stroke:#721c24,color:#721c24
    classDef process fill:#cce5ff,stroke:#004085,color:#004085
    classDef decision fill:#fff3cd,stroke:#856404,color:#856404
    
    class N success
    class B1,C1,D1,E1,F1,H1,K1,M1 failure
    class A,C,D,E,F,H,K,M process
    class B,G,J decision
```

## 🏠 Estate Planning Workflow

```mermaid
graph TD
    A[Manual Trigger] --> B[Get Transcript Files]
    B --> C[Split File List]
    C --> D[Process Each File]
    D --> E[Read Content]
    E --> F[BMAD Analysis]
    F --> G[Extract Client Data]
    G --> H[Validate Data]
    H --> I[Save to Baserow CRM]
    I --> J[Generate Report]
    J --> K[Create Follow-up Email]
    K --> L[Send Notifications]
    L --> M[Archive File]
    
    %% Error handling paths
    E -->|Read Error| E1[Log Error & Continue]
    F -->|Analysis Error| F1[Use Fallback Analysis]
    H -->|Validation Error| H1[Flag for Manual Review]
    I -->|CRM Error| I1[Queue for Retry]
    
    E1 --> D
    F1 --> G
    H1 --> I
    I1 --> N[Error Queue]
    
    classDef trigger fill:#e1f5fe,stroke:#01579b,color:#01579b
    classDef process fill:#f3e5f5,stroke:#4a148c,color:#4a148c
    classDef data fill:#e8f5e8,stroke:#1b5e20,color:#1b5e20
    classDef error fill:#ffebee,stroke:#b71c1c,color:#b71c1c
    classDef output fill:#fff8e1,stroke:#e65100,color:#e65100
    
    class A trigger
    class B,C,D,E,F,G,H process
    class I,J,K data
    class E1,F1,H1,I1,N error
    class L,M output
```

## 📦 Batch Processing Workflow

```mermaid
graph TD
    A[Manual Batch Trigger] --> B[Find All Files]
    B --> C[File Type Detection]
    C --> D[Split into Batches]
    D --> E[Process Batch]
    E --> F[Read File Content]
    F --> G{File Type}
    
    G -->|TXT| H[Text Processing]
    G -->|MD| I[Markdown Processing]
    G -->|DOCX| J[Document Processing]
    
    H --> K[Extract Metadata]
    I --> K
    J --> K
    
    K --> L[Data Validation]
    L --> M[Transform Data]
    M --> N[Save to Dashboard]
    N --> O[Update Progress]
    O --> P{More Batches?}
    
    P -->|Yes| E
    P -->|No| Q[Generate Summary]
    Q --> R[Archive Processed Files]
    R --> S[Send Completion Report]
    
    %% Progress and monitoring
    O --> T[Update Progress Bar]
    T --> U[Log Processing Stats]
    
    classDef trigger fill:#e3f2fd,stroke:#0d47a1,color:#0d47a1
    classDef fileprocess fill:#f1f8e9,stroke:#33691e,color:#33691e
    classDef decision fill:#fff3e0,stroke:#e65100,color:#e65100
    classDef data fill:#fce4ec,stroke:#880e4f,color:#880e4f
    classDef monitor fill:#f3e5f5,stroke:#4a148c,color:#4a148c
    
    class A trigger
    class B,C,D,E,F,H,I,J fileprocess
    class G,P decision
    class K,L,M,N,Q,R data
    class T,U monitor
```

## 💼 Sales Processing Workflow

```mermaid
graph TD
    A[Webhook Trigger] --> B[Validate Payload]
    B --> C[Extract Lead Data]
    C --> D[Enrich Lead Info]
    D --> E[Score Lead]
    E --> F{Lead Score}
    
    F -->|High| G[Priority Processing]
    F -->|Medium| H[Standard Processing]
    F -->|Low| I[Basic Processing]
    
    G --> J[Immediate CRM Update]
    H --> K[Scheduled CRM Update]
    I --> L[Batch CRM Update]
    
    J --> M[Create Hot Lead Alert]
    K --> N[Create Follow-up Task]
    L --> O[Add to Nurture Campaign]
    
    M --> P[Notify Sales Team]
    N --> Q[Schedule Follow-up]
    O --> R[Add to Email List]
    
    P --> S[Update Dashboard]
    Q --> S
    R --> S
    
    S --> T[Log Activity]
    T --> U[Generate Analytics]
    
    %% Error handling
    B -->|Invalid| V[Error Response]
    C -->|Extract Error| W[Fallback Extraction]
    D -->|Enrich Error| X[Use Basic Data]
    
    W --> D
    X --> E
    
    classDef trigger fill:#e8eaf6,stroke:#283593,color:#283593
    classDef process fill:#e0f2f1,stroke:#00695c,color:#00695c
    classDef decision fill:#fff8e1,stroke:#f57c00,color:#f57c00
    classDef priority fill:#ffebee,stroke:#c62828,color:#c62828
    classDef standard fill:#e3f2fd,stroke:#1565c0,color:#1565c0
    classDef basic fill:#f9fbe7,stroke:#689f38,color:#689f38
    classDef error fill:#fce4ec,stroke:#ad1457,color:#ad1457
    
    class A trigger
    class B,C,D,E process
    class F decision
    class G,J,M,P priority
    class H,K,N,Q standard
    class I,L,O,R basic
    class V,W,X error
```

## 🐳 Docker Services Architecture

```mermaid
graph TB
    subgraph "Docker Network"
        subgraph "n8n Container"
            N1[n8n Application]
            N2[Workflow Engine]
            N3[Node Executor]
        end
        
        subgraph "Baserow Container"
            B1[Baserow API]
            B2[Database Engine]
            B3[Web Interface]
        end
        
        subgraph "External Services"
            O1[Ollama LLM]
            Q1[Qdrant Vector DB]
        end
    end
    
    subgraph "Host System"
        H1[File System]
        H2[Network Ports]
        H3[Docker Volumes]
    end
    
    subgraph "External Integrations"
        E1[GitHub Webhooks]
        E2[Email Services]
        E3[Cloud Storage]
    end
    
    %% Internal connections
    N1 <--> N2
    N2 <--> N3
    B1 <--> B2
    B2 <--> B3
    
    %% Service connections
    N1 <--> B1
    N1 <--> O1
    N1 <--> Q1
    
    %% Host connections
    N1 <--> H1
    B1 <--> H1
    N1 --> H2
    B1 --> H2
    N1 <--> H3
    B1 <--> H3
    
    %% External connections
    N1 <--> E1
    N1 <--> E2
    B1 <--> E3
    
    classDef container fill:#e1f5fe,stroke:#01579b,color:#01579b
    classDef service fill:#f3e5f5,stroke:#4a148c,color:#4a148c
    classDef host fill:#e8f5e8,stroke:#1b5e20,color:#1b5e20
    classDef external fill:#fff3e0,stroke:#e65100,color:#e65100
    
    class N1,N2,N3,B1,B2,B3 container
    class O1,Q1 service
    class H1,H2,H3 host
    class E1,E2,E3 external
```

## 🔄 Error Handling Flow

```mermaid
graph TD
    A[Workflow Execution] --> B{Error Occurred?}
    B -->|No| C[Continue Execution]
    B -->|Yes| D[Capture Error]
    
    D --> E{Error Type}
    E -->|Network| F[Retry Logic]
    E -->|Data| G[Validation Fallback]
    E -->|System| H[Service Recovery]
    E -->|Critical| I[Emergency Stop]
    
    F --> J{Retry Count}
    J -->|< Max| K[Wait & Retry]
    J -->|>= Max| L[Mark as Failed]
    
    K --> A
    L --> M[Log Error]
    
    G --> N[Use Default Values]
    N --> O[Continue with Warning]
    O --> C
    
    H --> P[Restart Service]
    P --> Q{Service OK?}
    Q -->|Yes| A
    Q -->|No| R[Alert Admin]
    
    I --> S[Save State]
    S --> T[Send Alert]
    T --> U[Manual Intervention]
    
    M --> V[Update Metrics]
    V --> W[Generate Report]
    
    classDef normal fill:#e8f5e8,stroke:#1b5e20,color:#1b5e20
    classDef decision fill:#fff3e0,stroke:#e65100,color:#e65100
    classDef retry fill:#e3f2fd,stroke:#1565c0,color:#1565c0
    classDef fallback fill:#f3e5f5,stroke:#7b1fa2,color:#7b1fa2
    classDef critical fill:#ffebee,stroke:#c62828,color:#c62828
    
    class A,C,O normal
    class B,E,J,Q decision
    class F,K retry
    class G,N fallback
    class I,S,T,U critical
```

## 📊 Monitoring & Observability

```mermaid
graph TB
    subgraph "Application Layer"
        A1[n8n Workflows]
        A2[BMAD Agents]
        A3[Python Scripts]
    end
    
    subgraph "Service Layer"
        S1[Docker Services]
        S2[Health Checks]
        S3[API Endpoints]
    end
    
    subgraph "Infrastructure Layer"
        I1[Docker Engine]
        I2[Network Stack]
        I3[File System]
    end
    
    subgraph "Monitoring Stack"
        M1[Log Aggregation]
        M2[Metrics Collection]
        M3[Alert Manager]
    end
    
    subgraph "Observability"
        O1[Dashboards]
        O2[Reports]
        O3[Notifications]
    end
    
    %% Data flow
    A1 --> M1
    A2 --> M1
    A3 --> M1
    
    S1 --> M2
    S2 --> M2
    S3 --> M2
    
    I1 --> M2
    I2 --> M2
    I3 --> M2
    
    M1 --> O1
    M2 --> O1
    M3 --> O3
    
    M1 --> M3
    M2 --> M3
    
    O1 --> O2
    
    classDef app fill:#e8eaf6,stroke:#3f51b5,color:#3f51b5
    classDef service fill:#e0f2f1,stroke:#00695c,color:#00695c
    classDef infra fill:#fff3e0,stroke:#ff6f00,color:#ff6f00
    classDef monitor fill:#fce4ec,stroke:#ad1457,color:#ad1457
    classDef observe fill:#f3e5f5,stroke:#7b1fa2,color:#7b1fa2
    
    class A1,A2,A3 app
    class S1,S2,S3 service
    class I1,I2,I3 infra
    class M1,M2,M3 monitor
    class O1,O2,O3 observe
```

## 🔐 Security Flow

```mermaid
graph TD
    A[Code Commit] --> B[Security Scan]
    B --> C[Dependency Check]
    C --> D[Secret Detection]
    D --> E{Vulnerabilities Found?}
    
    E -->|Yes| F[Block Deployment]
    E -->|No| G[Continue Pipeline]
    
    F --> H[Generate Report]
    H --> I[Notify Developers]
    I --> J[Fix Issues]
    J --> A
    
    G --> K[Runtime Security]
    K --> L[Access Control]
    L --> M[Audit Logging]
    M --> N[Compliance Check]
    
    N --> O{Compliant?}
    O -->|Yes| P[Deploy to Production]
    O -->|No| Q[Flag for Review]
    
    Q --> R[Manual Review]
    R --> S{Approved?}
    S -->|Yes| P
    S -->|No| F
    
    P --> T[Monitor Runtime]
    T --> U[Security Alerts]
    U --> V[Incident Response]
    
    classDef security fill:#ffebee,stroke:#c62828,color:#c62828
    classDef check fill:#fff3e0,stroke:#f57c00,color:#f57c00
    classDef process fill:#e8f5e8,stroke:#1b5e20,color:#1b5e20
    classDef decision fill:#e3f2fd,stroke:#1565c0,color:#1565c0
    classDef monitor fill:#f3e5f5,stroke:#7b1fa2,color:#7b1fa2
    
    class B,C,D,K,L,M security
    class H,I,R,V check
    class A,G,P process
    class E,O,S decision
    class T,U monitor
```

## 🔗 Integration Points

```mermaid
graph LR
    subgraph "Internal Services"
        N[n8n] 
        B[Baserow]
        P[Python Scripts]
    end
    
    subgraph "AI Services"
        O[Ollama]
        Q[Qdrant]
        BM[BMAD Agents]
    end
    
    subgraph "External APIs"
        G[GitHub]
        E[Email Services]
        W[Webhooks]
    end
    
    subgraph "File Systems"
        T[Transcripts]
        R[Reports]
        L[Logs]
    end
    
    %% Connections
    N <--> B
    N <--> P
    N <--> BM
    
    P <--> O
    P <--> Q
    P <--> BM
    
    N <--> G
    N <--> E
    N <--> W
    
    N <--> T
    P <--> T
    N <--> R
    P <--> L
    
    classDef internal fill:#e8f5e8,stroke:#1b5e20,color:#1b5e20
    classDef ai fill:#e8eaf6,stroke:#3f51b5,color:#3f51b5
    classDef external fill:#fff3e0,stroke:#f57c00,color:#f57c00
    classDef storage fill:#f3e5f5,stroke:#7b1fa2,color:#7b1fa2
    
    class N,B,P internal
    class O,Q,BM ai
    class G,E,W external
    class T,R,L storage
```

---

## 📝 Diagram Legend

- **🔄 Process Flow**: Sequential steps in a workflow
- **🔀 Decision Points**: Conditional branches based on criteria
- **⚠️ Error Handling**: Recovery and fallback mechanisms
- **📊 Data Flow**: Information movement between components
- **🔐 Security Gates**: Security checkpoints and validations
- **🔗 Integration**: Service connections and dependencies

## 🎯 Key Insights

1. **Resilience**: Multiple error handling paths ensure robustness
2. **Scalability**: Batch processing and service isolation support growth
3. **Security**: Multiple security gates protect against vulnerabilities
4. **Observability**: Comprehensive monitoring enables proactive management
5. **Integration**: Well-defined connection points enable extensibility

---

**Last Updated:** December 2024  
**Version:** 1.0  
**Maintainer:** Development Team