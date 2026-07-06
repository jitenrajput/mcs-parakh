# 03 — Flowcharts

Mermaid — renders directly on GitHub. These four flows ARE the demo script; QA walks them daily.

## 1. Demo user flow (the 3-persona storyline)

```mermaid
flowchart TD
    A[RM opens Parakh<br/>lender dashboard] --> B[Enter GSTIN]
    B --> C[AA-style consent screen<br/>purpose 103/104 · FI types · range · duration<br/>DPDP plain-language notice]
    C -->|Approve OTP mock| D[Adapters fetch in parallel<br/>AA-bank · GST · UPI · EPFO · Bureau]
    C -->|Reject| C2[No data pulled<br/>consent declined recorded]
    D --> E{All sources OK?}
    E -->|Yes| F[Health Card assembles<br/>animated 300-900 gauge<br/>5 dimensions · HIGH confidence ±15]
    E -->|Some failed / partial| G[Card renders anyway<br/>wider band · missing-source badge<br/>GRACEFUL DEGRADATION moment]
    F --> H[Reason codes panel<br/>+ CGTMSE flag + product propensity]
    G --> H
    H --> I[Flip card → MSME self-view<br/>strengths · improve-your-score actions<br/>loan-readiness meter]
    I --> J[Portfolio view<br/>book ranked by trend<br/>early-warning alerts w/ reasons]
    J --> K{Persona}
    K -->|P1 Rajkot manufacturer ~780| L[Term-loan-ready · CGTMSE-eligible<br/>Rs 75L expansion lead]
    K -->|P2 Surat NTC seller ~690| M[No bureau file, still scored<br/>INCLUSION hero-moment]
    K -->|P3 Stressed trader ~410| N[Deterioration alert fired<br/>improvement path on MSME side]
```

## 2. Scoring pipeline (engine internals)

```mermaid
flowchart LR
    subgraph Adapters
        A1[AA-bank mock<br/>ReBIT deposit.xsd] --> R1[FetchResult]
        A2[GST mock<br/>GSTR1_3B] --> R2[FetchResult]
        A3[UPI mock<br/>txn mode=UPI] --> R3[FetchResult]
        A4[EPFO mock<br/>employer-consented ECR] --> R4[FetchResult]
        A5[Bureau mock<br/>CMR-style, nullable] --> R5[FetchResult]
    end
    R1 & R2 & R3 & R4 & R5 --> CV[Coverage vector<br/>per-source status + coverage]
    R1 & R2 & R3 & R4 & R5 --> FE[FeatureExtractor per source<br/>CoV inflows · balance floor · filing delays<br/>EMI/inflow · bounces · vintage · headcount]
    FE --> SC[Scorecard<br/>bins → points → 5 dimension scores 0-100]
    SC --> W[Weighted composite<br/>30/20/15/20/15 config-driven]
    W --> SCALE[Affine log-odds scaling<br/>PDO method → 300-900]
    SC --> RC[Reason codes<br/>top ± point contributions → sentences]
    CV --> CB[Confidence band<br/>High ±15 · Med ±35 · Low ±60<br/>missing → neutral prior]
    SCALE & RC & CB --> OUT[ScoreResponse + audit log row<br/>engine version · consent ref · coverage]
    OUT -.stretch.-> GBM[LightGBM monotonic + SHAP<br/>corroborating reason codes]
```

## 3. Early-warning loop (continuous monitoring)

```mermaid
flowchart TD
    S[Monthly windowed snapshots<br/>24 mo synthetic history] --> RS[Re-score each window<br/>score time-series per MSME]
    RS --> T{Alert rules}
    T -->|drop > 40 pts in 1 mo| AL[Alert raised]
    T -->|negative slope 3 consecutive mo| AL
    T -->|trip-wire: bounces up / GST lapse /<br/>EMI-to-inflow crosses threshold| AL
    T -->|none| OK[Healthy — ranked in portfolio]
    AL --> P[Portfolio dashboard<br/>sorted by deterioration<br/>alert + reason codes]
    P --> RM[RM acts: review · restructure ·<br/>early engagement]
    RM -.-> MSME[MSME view shows same trend<br/>+ corrective actions]
```

## 4. Submission-week decision flow (process, not product)

```mermaid
flowchart TD
    D0[Jul 6: engine + data] -->|gate: 3 personas score correctly| D1[Jul 7: API + UI end-to-end]
    D1 -->|gate: full flow clickable locally| D2[Jul 8: deploy + deck + QA]
    D1 -->|gate missed| CUT1[Cut: GBM stretch, propensity panel<br/>keep MUSTs only]
    D2 -->|gate: public URL works on phone<br/>deck PDF ≤ 5 MB, stats verified| D3[Jul 9 AM: SUBMIT<br/>deck + demo link + repo<br/>+ team formation confirmed]
    D2 -->|deploy stalls > 3 hrs| FB[Fallback: Render/Railway<br/>architecture slide unchanged]
    D3 --> DONE[Confirmation screenshot<br/>→ wait for Jul 21 shortlist]
```
