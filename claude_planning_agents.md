# Simplified 3-Agent Crime Investigation System
## Using SAP AI Tools + CrewAI Framework

---

## 🎯 Streamlined Architecture

```
Evidence Collection → Alibi Collection → Analysis & Deduction
        ↓                    ↓                    ↓
    Agent 1              Agent 2              Agent 3
   (Detective)          (Interviewer)        (Analyst)
```

---

## 👥 Three-Agent Roster

### **Agent 1: Detective Morgan (Evidence Collector)**
**Role**: Collects and catalogs ALL physical evidence from crime scene

**Personality**: Methodical, observant, thorough, "leaves no stone unturned"

**Backstory**: *"20-year veteran of forensics. Solved the Riverside Case by finding a single fiber. Believes physical evidence never lies."*

**Tools**:
1. **`EvidenceCollectionTool`** - Documents physical items (E-1 to E-7)
2. **`SAP_VectorStore_Writer`** - Stores evidence in HANA Vector Store with embeddings
3. **`SAP_Classification_RPT1`** - Classifies evidence type (textile, chemical, trace)
4. **`ForensicAnalysisTool`** - Analyzes fingerprints, materials, footprints

**Primary Task**:
```python
Task(
    description="""
    Investigate the music room crime scene and collect ALL physical evidence:
    1. Document the torn silk glove near the piano (E-1)
    2. Analyze smudged fingerprints on the candelabra (E-2)
    3. Photograph and measure muddy footprints from garden to dining room (E-3)
    4. Collect the cigar stub from library ashtray (E-4)
    5. Document red leather dye smear on dining room doorframe (E-5)
    6. Note air quality: floral perfume + cigar smoke traces in music room (E-6)
    7. Retrieve handwritten note from Victor's pocket (E-7)
    
    For each piece of evidence:
    - Classify its type using RPT-1
    - Determine potential owner based on suspect traits
    - Store in Vector Store with metadata (location, time found, description)
    - Note any connections between evidence pieces
    
    Provide a structured evidence catalog with forensic analysis.
    """,
    agent=detective_morgan,
    expected_output="Complete evidence catalog with 7 items analyzed and stored in Vector Store"
)
```

**SAP Tech Used**:
- **HANA Vector Store**: Store evidence descriptions as embeddings for semantic search
- **Classification RPT-1**: Classify evidence (silk/textile, chemical/perfume, organic/cigar)

---

### **Agent 2: Inspector Chen (Alibi & Witness Collector)**
**Role**: Interviews all witnesses and suspects; builds timeline; documents alibis

**Personality**: Empathetic but skeptical, patient listener, timeline-obsessed

**Backstory**: *"Former interrogation specialist. Can spot a lie in three questions. Once cleared an innocent man by finding a 2-minute alibi gap."*

**Tools**:
1. **`WitnessInterviewTool`** - Conducts structured interviews (W-A to W-F)
2. **`SuspectStatementTool`** - Records suspect claims (S-1 to S-4)
3. **`SAP_VectorStore_Writer`** - Stores statements as embeddings
4. **`TimelineBuilderTool`** - Creates minute-by-minute timeline
5. **`SAP_KnowledgeGraph_Writer`** - Builds temporal graph of movements

**Primary Task**:
```python
Task(
    description="""
    Interview ALL witnesses and suspects to build complete timeline and document alibis:
    
    WITNESS INTERVIEWS (record exact quotes):
    - W-A (Butler Martin): What did he see 8:50-9:10? Julian's cigar? Evelyn's exit?
    - W-B (Chef Sofia): When did she hear the thud? (Critical: 9:12 PM)
    - W-C (Groundskeeper Lars): When/where did he see Clara in garden? Mud on her hem?
    - W-D (Sommelier Niklas): Perfume timing? Cigar smoke locations?
    - W-E (Housemaid Greta): Candelabra polish timing? Fresh smudges later?
    - W-F (Paramedic): Time of death estimate? (9:12-9:18 PM)
    
    SUSPECT STATEMENTS (document claims and contradictions):
    - S-1 (Clara): "Went straight to library" - verify timing
    - S-2 (Julian): "In library with cigar" - cross-check with Butler
    - S-3 (Evelyn): "Didn't go near music room after 8:50" - check perfume evidence
    - S-4 (Samuel): "Checking windows, moved candelabra after discovery" - validate
    
    BUILD TIMELINE:
    - Map every person's location from 9:00-9:20 PM
    - Identify the critical 9:12-9:18 PM murder window
    - Flag anyone with NO WITNESSED ALIBI during murder window
    - Note contradictions between statements and witness accounts
    
    Store all statements in Vector Store and create Knowledge Graph of:
    - (Person)-[:LOCATED_AT {time}]->(Room)
    - (Person)-[:CLAIMS]->(Statement)
    - (Witness)-[:SAW]->(Person) at specific times
    """,
    agent=inspector_chen,
    expected_output="Complete timeline (9:00-9:20 PM), 6 witness statements, 4 suspect statements, alibi validation matrix showing who has NO ALIBI for 9:12-9:18 PM"
)
```

**SAP Tech Used**:
- **HANA Vector Store**: Semantic search across statements for contradictions
- **Knowledge Graph**: Temporal nodes (events) and relationships (Person → Location @ Time)

---

### **Agent 3: Chief Analyst Reeves (The Resolver)**
**Role**: Cross-references ALL evidence + alibis; performs deductive reasoning; identifies killer

**Personality**: Brilliant, confident, logical, "Sherlock Holmes" energy

**Backstory**: *"Youngest chief analyst in department history. PhD in forensic psychology. Famous for the 'Reeves Method': match evidence to opportunity to motive. 97% solve rate."*

**Tools**:
1. **`SAP_VectorStore_Query`** - Semantic search over ALL evidence and statements
2. **`SAP_Grounding_Service`** - RAG-based fact-checking (validates theories against corpus)
3. **`SAP_KnowledgeGraph_Query`** - Queries temporal/spatial relationships
4. **`ContradictionAnalysisTool`** - Compares suspect claims vs. evidence
5. **`DeductiveReasoningTool`** - Builds logical proof chains
6. **`ReportGenerationTool`** - Creates final case report

**Primary Task**:
```python
Task(
    description="""
    You are the lead analyst. Solve the murder by synthesizing ALL evidence and alibis.
    
    STEP 1: CROSS-REFERENCE EVIDENCE WITH SUSPECTS
    Use Vector Store to semantically search:
    - "Who wears silk gloves?" → Query statements about Clara
    - "Who was in the garden?" → Match E-3 footprints to Lars's witness account
    - "Who has small shoe size?" → Compare to suspect descriptions
    - "Who touches red leather items?" → Match E-5 to Evelyn's handbag
    - "Who smokes cigars?" → Match E-4 to Julian
    
    STEP 2: VALIDATE ALIBIS FOR 9:12-9:18 PM MURDER WINDOW
    Query Knowledge Graph:
    - Julian: Was he in library? (YES - Butler confirms, cigar stub at 9:10)
    - Evelyn: Was she at powder room? (YES - Butler saw her leave at 9:08, dye mark timing)
    - Samuel: Was he in east hall? (YES - but admits touching candelabra AFTER discovery)
    - Clara: WHERE WAS SHE? (NO ALIBI - last seen in garden at 9:07 by Lars)
    
    STEP 3: MATCH EVIDENCE TO CLARA
    Use Grounding Service to validate:
    - E-1 (torn glove): "Clara claims she kept gloves on all night" 
      → CONTRADICTION: Her glove is at crime scene
    - E-3 (muddy footprints): "Clara was in garden with muddy hem"
      → MATCHES: Small footprints lead from garden → dining room (where candelabra was)
    - Timeline gap: "Clara claims she went straight to library"
      → CONTRADICTION: No witness places her there 9:07-9:20
    
    STEP 4: BUILD DEDUCTIVE PROOF
    1. Motive: Victor publicly humiliated Clara at 8:35 PM (witness confirmed)
    2. Opportunity: Clara has NO ALIBI for 9:12-9:18 PM murder window
    3. Means: Muddy footprints show her path: garden → dining room (took candelabra) → music room
    4. Physical evidence: HER torn glove at crime scene, despite claiming she never removed it
    5. Contradictions: Claims "went straight to library" but NO witness saw her there
    
    STEP 5: ELIMINATE OTHER SUSPECTS
    - Julian: Solid alibi (library, cigar stub, Butler witness) - ELIMINATED
    - Evelyn: Dye mark proves she left BEFORE murder window - ELIMINATED  
    - Samuel: Admits touching candelabra AFTER discovery (explains smudges) - ELIMINATED
    
    CONCLUSION: Clara Beaumont is the murderer.
    
    Generate final report with:
    - Executive summary (who, what, when, where, why, how)
    - Evidence explanation (E-1 to E-7)
    - Timeline reconstruction
    - Contradiction analysis
    - Confidence score (should be 95%+)
    - Arrest warrant recommendation
    """,
    agent=chief_reeves,
    expected_output="Final investigation report identifying Clara Beaumont as murderer with complete reasoning chain, evidence mapping, and 95%+ confidence score"
)
```

**SAP Tech Used**:
- **HANA Vector Store**: Semantic search ("who wears gloves?")
- **Grounding Service**: RAG to validate Clara's claims against evidence
- **Knowledge Graph**: Query temporal gaps, spatial paths

---

## 🛠️ Tool Implementations

### 1. Evidence Collection Tool
```python
from langchain.tools import Tool

class EvidenceCollectionTool(Tool):
    name = "evidence_collection"
    description = "Documents physical evidence with location, description, and photos"
    
    def _run(self, evidence_id: str, location: str, description: str):
        return {
            "id": evidence_id,
            "location": location,
            "description": description,
            "timestamp": "9:20 PM",
            "collected_by": "Detective Morgan"
        }
```

### 2. SAP HANA Vector Store Writer
```python
class HANAVectorStoreWriter(Tool):
    name = "hana_vector_writer"
    description = "Stores evidence/statements as embeddings in SAP HANA Vector Store"
    
    def _run(self, text: str, metadata: dict):
        # Pseudocode
        # embedding = generate_embedding(text)  # Using SAP Embedding model
        # hana_connection.execute(
        #     "INSERT INTO evidence_vectors (id, embedding, metadata, text) VALUES (?, ?, ?, ?)",
        #     metadata['id'], embedding, json.dumps(metadata), text
        # )
        return f"Stored in Vector Store: {metadata['id']}"
```

### 3. SAP Classification RPT-1
```python
class RPT1Classifier(Tool):
    name = "rpt1_classifier"
    description = "Classifies evidence using SAP RPT-1 model"
    
    def _run(self, evidence_description: str):
        # POST to SAP AI Core RPT-1 endpoint
        # response = sap_ai_core.classify(evidence_description)
        return {
            "type": "textile",
            "subtype": "silk",
            "confidence": 0.94,
            "tags": ["fabric", "luxury", "torn"]
        }
```

### 4. SAP Vector Store Query
```python
class HANAVectorStoreQuery(Tool):
    name = "hana_vector_query"
    description = "Semantic search over evidence and statements"
    
    def _run(self, query: str, top_k: int = 5):
        # query_embedding = generate_embedding(query)
        # results = hana_connection.execute(
        #     "SELECT text, metadata FROM evidence_vectors ORDER BY COSINE_SIMILARITY(embedding, ?) DESC LIMIT ?",
        #     query_embedding, top_k
        # )
        return [
            {"text": "Clara wears long silk gloves", "source": "Suspect traits", "similarity": 0.92},
            {"text": "Torn silk glove found near piano", "source": "E-1", "similarity": 0.89}
        ]
```

### 5. SAP Grounding Service
```python
class GroundingServiceTool(Tool):
    name = "grounding_service"
    description = "Validates claims against evidence corpus using RAG"
    
    def _run(self, claim: str):
        # POST to SAP Grounding Service
        # response = sap_grounding.check(claim, evidence_corpus)
        return {
            "claim": claim,
            "supported": False,
            "contradictions": ["E-1: Torn glove found at scene", "W-A: No witness saw Clara in library"],
            "confidence": 0.91
        }
```

### 6. SAP Knowledge Graph Query
```python
class KnowledgeGraphQuery(Tool):
    name = "kg_query"
    description = "Queries temporal/spatial relationships"
    
    def _run(self, cypher_query: str):
        # Example: Find who has no alibi in murder window
        # MATCH (s:Suspect) WHERE NOT EXISTS {
        #   MATCH (s)-[:LOCATED_AT {time: "9:12-9:18"}]->(l:Location)
        #   WHERE (l)-[:WITNESSED_BY]->(:Witness)
        # } RETURN s.name
        return [{"name": "Clara Beaumont", "last_seen": "9:07 PM in garden"}]
```

---

## 📋 Complete CrewAI Implementation

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# === INITIALIZE LLM ===
llm = ChatOpenAI(model="gpt-4", temperature=0.2)

# === TOOLS ===
evidence_tool = EvidenceCollectionTool()
vector_writer = HANAVectorStoreWriter()
rpt1_classifier = RPT1Classifier()
forensic_tool = ForensicAnalysisTool()

witness_tool = WitnessInterviewTool()
suspect_tool = SuspectStatementTool()
timeline_tool = TimelineBuilderTool()
kg_writer = KnowledgeGraphWriter()

vector_query = HANAVectorStoreQuery()
grounding_service = GroundingServiceTool()
kg_query = KnowledgeGraphQuery()
contradiction_tool = ContradictionAnalysisTool()
deduction_tool = DeductiveReasoningTool()
report_tool = ReportGenerationTool()

# === AGENT 1: DETECTIVE MORGAN ===
detective_morgan = Agent(
    role="Evidence Collection Detective",
    goal="Collect and analyze ALL physical evidence from the crime scene",
    backstory="""You are Detective Morgan, a 20-year forensics veteran. 
    You solved the Riverside Case by finding a single fiber. 
    You believe physical evidence never lies. You are methodical, observant, and thorough.""",
    tools=[evidence_tool, vector_writer, rpt1_classifier, forensic_tool],
    llm=llm,
    verbose=True
)

task_evidence = Task(
    description="""
    Investigate the music room crime scene and collect ALL physical evidence:
    
    1. E-1: Torn silk glove near piano (left-hand, fresh tear)
    2. E-2: Smudged fingerprints on candelabra (partial, hurried wiping)
    3. E-3: Muddy footprints (small shoe) from garden → dining room → sideboard
    4. E-4: Cigar stub in library ashtray (recent, warm at 9:10 PM)
    5. E-5: Red leather dye smear on dining room doorframe (hip level)
    6. E-6: Air analysis - faint floral perfume + trace cigar smoke in music room
    7. E-7: Handwritten note in Victor's pocket: "Meet me after dinner. We need to talk about the money."
    
    For EACH piece of evidence:
    - Use RPT-1 to classify its type (textile/chemical/organic)
    - Perform forensic analysis (fingerprints, material composition, freshness)
    - Match to suspect traits (who wears gloves? who smokes cigars? who uses perfume?)
    - Store in HANA Vector Store with metadata
    
    Create a structured evidence catalog showing:
    - Evidence ID
    - Location found
    - Forensic analysis results
    - Potential owner (based on suspect traits)
    - Connections to other evidence
    """,
    agent=detective_morgan,
    expected_output="Complete evidence catalog with 7 items analyzed, classified, and stored in Vector Store with potential owners identified"
)

# === AGENT 2: INSPECTOR CHEN ===
inspector_chen = Agent(
    role="Witness & Alibi Investigator",
    goal="Interview all witnesses and suspects; build complete timeline; document alibis",
    backstory="""You are Inspector Chen, former interrogation specialist. 
    You can spot a lie in three questions. You once cleared an innocent man by finding a 2-minute alibi gap.
    You are empathetic but skeptical, patient, and timeline-obsessed.""",
    tools=[witness_tool, suspect_tool, timeline_tool, vector_writer, kg_writer],
    llm=llm,
    verbose=True
)

task_alibis = Task(
    description="""
    Interview ALL witnesses and suspects to build timeline and verify alibis:
    
    WITNESS INTERVIEWS (document exact quotes and times):
    - W-A (Butler Martin): In library 8:50-9:10. Saw Julian stub cigar at 9:10. Watched Evelyn leave at 9:08, touch doorframe with hip. Did NOT see Clara after 8:50.
    - W-B (Chef Sofia): At 9:12 PM, heard single heavy thud from music room while passing gallery.
    - W-C (Groundskeeper Lars): 9:00-9:07 saw Clara pacing in garden near hedges, hem had mud. At 9:09 saw small footprints from garden → dining room.
    - W-D (Sommelier Niklas): At 8:52 smelled Evelyn's perfume in music room (residual from earlier). At 9:06 in library, Julian's cigar smoke was strong there.
    - W-E (Housemaid Greta): At 6 PM watched Samuel polish candelabra, return to dining room. After 9:20 PM found fresh smudges (not her shine).
    - W-F (Paramedic): Arrived 9:25 PM. Time of death estimate: 9:12-9:18 PM based on body temp and lividity.
    
    SUSPECT STATEMENTS (record claims):
    - S-1 (Clara): "After dinner I walked the garden, then went STRAIGHT to library. Never entered dining room. Kept gloves on all night."
    - S-2 (Julian): "I was in library with my cigar until I heard the scream. Money talk was postponed."
    - S-3 (Evelyn): "I went to powder room, then paused in gallery to text. Didn't go near music room after 8:50."
    - S-4 (Samuel): "I was checking east hall windows at 9:10. Heard shout, ran to music room, instinctively moved candelabra away from blood."
    
    BUILD TIMELINE focusing on 9:00-9:20 PM:
    9:00 - Julian lights cigar (library)
    9:00-9:07 - Clara in garden (witnessed by Lars)
    9:05 - Victor goes to music room
    9:08 - Evelyn leaves library for powder room (Butler saw)
    9:09 - Small footprints garden → dining room (Lars saw)
    9:10 - Julian stubs cigar (Butler confirms)
    9:10 - Samuel in east hall
    9:12 - MURDER (Chef heard thud)
    9:20 - Body discovered
    
    CRITICAL: Identify who has NO WITNESSED ALIBI for 9:12-9:18 PM murder window.
    
    Store all statements in Vector Store and create Knowledge Graph with:
    - Nodes: People, Locations, Times, Statements
    - Edges: (Person)-[:AT_LOCATION {time}]->(Room), (Witness)-[:SAW]->(Person)
    """,
    agent=inspector_chen,
    expected_output="Complete timeline (9:00-9:20), 6 witness transcripts, 4 suspect statements, alibi matrix showing Clara has NO ALIBI for 9:12-9:18 PM, all data in Vector Store and Knowledge Graph"
)

# === AGENT 3: CHIEF ANALYST REEVES ===
chief_reeves = Agent(
    role="Lead Crime Analyst & Resolver",
    goal="Cross-reference all evidence and alibis to identify the killer with 95%+ confidence",
    backstory="""You are Chief Analyst Reeves, youngest chief in department history. PhD in forensic psychology.
    Famous for the 'Reeves Method': match evidence to opportunity to motive. 97% solve rate.
    You are brilliant, confident, logical, with Sherlock Holmes energy.""",
    tools=[vector_query, grounding_service, kg_query, contradiction_tool, deduction_tool, report_tool],
    llm=llm,
    verbose=True
)

task_solve = Task(
    description="""
    You are the lead analyst. Solve the murder using the Reeves Method.
    
    STEP 1: EVIDENCE-TO-SUSPECT MATCHING
    Query Vector Store semantically:
    - "Who wears silk gloves?" → Should return Clara (from suspect traits)
    - "Who was in the garden with muddy shoes?" → Should return Clara (from Lars's witness)
    - "Who has small shoe size?" → Match to footprints E-3
    - "Who uses floral perfume?" → Evelyn (but check timing)
    - "Who smokes cigars?" → Julian (but verify alibi)
    
    STEP 2: ALIBI VALIDATION FOR 9:12-9:18 PM
    Query Knowledge Graph:
    - Julian: (Julian)-[:AT_LOCATION {time: "9:10"}]->(Library) + (Butler)-[:SAW]->(Julian) → SOLID ALIBI
    - Evelyn: (Evelyn)-[:AT_LOCATION {time: "9:08"}]->(Powder Room) + dye mark at 9:08 → LEFT BEFORE MURDER
    - Samuel: (Samuel)-[:AT_LOCATION {time: "9:10"}]->(East Hall) + admits touching candelabra AFTER → NOT DURING
    - Clara: NO NODES showing (Clara)-[:AT_LOCATION {time: "9:12-9:18"}]->() with witnesses → NO ALIBI
    
    STEP 3: CONTRADICTION ANALYSIS
    Use Grounding Service to check Clara's statements:
    
    Claim 1: "I went straight to library after garden"
    → Ground against: W-A (Butler saw everyone EXCEPT Clara), timeline shows no Clara 9:07-9:20
    → Result: CONTRADICTION - No witness places her in library
    
    Claim 2: "I kept my gloves on all night"
    → Ground against: E-1 (torn silk glove found at crime scene)
    → Result: CONTRADICTION - Her glove is at murder scene
    
    Claim 3: "Never entered dining room"
    → Ground against: E-3 (muddy footprints garden → dining room), W-C (Lars saw her with muddy hem)
    → Result: CONTRADICTION - Footprints match her garden visit
    
    STEP 4: BUILD DEDUCTIVE PROOF CHAIN
    
    MOTIVE:
    - Victor publicly criticized Clara at 8:35 PM (witnessed at dinner)
    - Clara has "quick temper when criticized" (suspect trait)
    - She left to "cool down" in garden (emotional response)
    
    OPPORTUNITY:
    - Clara was last seen at 9:07 PM in garden by Lars
    - Murder occurred 9:12-9:18 PM (medical estimate)
    - Clara has NO ALIBI for this window (no witness saw her)
    - She was NOT in library (Butler confirms)
    
    MEANS:
    - Muddy footprints (small shoe, matches Clara) lead: garden → dining room → sideboard
    - Candelabra was on sideboard at 8:55 PM (Chef saw it)
    - Footprints show someone took weapon from dining room at ~9:09-9:12
    - Weapon used to strike Victor from behind at piano
    
    PHYSICAL EVIDENCE:
    - E-1: Clara's torn LEFT silk glove at crime scene (she wears "long silk gloves")
    - E-3: Her muddy footprints show path to weapon
    - Timeline: She had 5 minutes (9:07 garden → 9:12 murder) to go: garden → dining room → get candelabra → music room → strike
    
    ELIMINATE OTHER SUSPECTS:
    - Julian: Solid alibi (library + cigar + Butler witness) ✗
    - Evelyn: Left dining room at 9:08, BEFORE murder window ✗
    - Samuel: East hall at 9:10 + touched candelabra AFTER discovery (explains smudges) ✗
    
    STEP 5: FINAL CONCLUSION
    
    MURDERER: Clara Beaumont
    
    REASONING:
    1. She had MOTIVE (public humiliation at 8:35 PM)
    2. She had OPPORTUNITY (no alibi for 9:12-9:18 PM murder window)
    3. She had MEANS (muddy footprints show her path to retrieve candelabra)
    4. Physical evidence places her at scene (torn glove E-1)
    5. Her statements contain THREE contradictions proven by evidence
    6. All other suspects have verified alibis
    
    CONFIDENCE: 96%
    
    Generate final report with:
    - Executive summary (Clara Beaumont killed Victor with candelabra at ~9:12 PM)
    - Evidence breakdown (E-1 to E-7 explained)
    - Timeline reconstruction
    - Contradiction analysis of Clara's statements
    - Alibi validation for all suspects
    - Motive-Opportunity-Means analysis
    - Recommendation: Issue arrest warrant for Clara Beaumont, charge: Murder in the First Degree
    """,
    agent=chief_reeves,
    expected_output="Final investigation report identifying Clara Beaumont as murderer with complete evidence chain, contradiction analysis, alibi validation, and 96% confidence score. Arrest warrant recommended."
)

# === CREATE CREW ===
investigation_crew = Crew(
    agents=[detective_morgan, inspector_chen, chief_reeves],
    tasks=[task_evidence, task_alibis, task_solve],
    process=Process.sequential,  # Each agent completes before next starts
    verbose=2
)

# === EXECUTE INVESTIGATION ===
if __name__ == "__main__":
    print("🔍 Starting Murder Investigation...\n")
    result = investigation_crew.kickoff()
    print("\n" + "="*80)
    print("📋 FINAL INVESTIGATION REPORT")
    print("="*80)
    print(result)
```

---

## 🎓 Developer Workshop Structure (2-Day Format)

### **Day 1: Setup & Agent 1+2**

**Morning (9 AM - 12 PM): Environment Setup**
- Provision SAP HANA Cloud with Vector Engine
- Set up SAP AI Core (RPT-1 model)
- Install CrewAI, LangChain
- Load crime scene data (E-1 to E-7, W-A to W-F, S-1 to S-4)

**Afternoon (1 PM - 5 PM): Build Detective Morgan & Inspector Chen**
- Implement `EvidenceCollectionTool`
- Implement `HANAVectorStoreWriter`
- Test evidence ingestion into Vector Store
- Build `WitnessInterviewTool` and `TimelineBuilderTool`
- Create Knowledge Graph schema
- Run Agents 1 & 2, verify outputs

---

### **Day 2: Agent 3 & Integration**

**Morning (9 AM - 12 PM): Build Chief Reeves**
- Implement `HANAVectorStoreQuery` (semantic search)
- Set up SAP Grounding Service connection
- Build `ContradictionAnalysisTool`
- Test semantic queries ("who wears gloves?")

**Afternoon (1 PM - 5 PM): Full Investigation Run**
- Run complete 3-agent crew
- Validate Clara is identified as murderer
- Debug any reasoning gaps
- Generate final report PDF
- Presentation: Each team shows their crew's deduction process

---

## 📊 Success Metrics

| Metric | Target | Validation |
|--------|--------|------------|
| **Evidence Collected** | 7/7 items (E-1 to E-7) | Detective Morgan's output |
| **Witnesses Interviewed** | 6/6 (W-A to W-F) | Inspector Chen's output |
| **Alibis Documented** | 4/4 suspects | Knowledge Graph query |
| **Contradictions Found** | 3 (Clara's claims) | Grounding Service results |
| **Correct Murderer** | Clara Beaumont | Chief Reeves' conclusion |
| **Confidence Score** | ≥95% | Final report |

---

## 🚀 What Developers Learn

✅ **SAP HANA Vector Store**: Embeddings, semantic search  
✅ **SAP Classification RPT-1**: Evidence categorization  
✅ **SAP Grounding Service**: RAG-based fact-checking  
✅ **Knowledge Graph**: Temporal/spatial reasoning  
✅ **CrewAI**: Multi-agent task orchestration  
✅ **Prompt Engineering**: Detailed task descriptions  
✅ **Deductive Logic**: Building reasoning chains  

---

## 💡 Simplified Tool Summary

| Tool | Agent | SAP Component | Purpose |
|------|-------|---------------|---------|
| `EvidenceCollectionTool` | Detective Morgan | - | Documents E-1 to E-7 |
| `HANAVectorStoreWriter` | Detective, Inspector | HANA Vector Store | Stores evidence/statements as embeddings |
| `RPT1Classifier` | Detective Morgan | Classification RPT-1 | Classifies evidence types |
| `WitnessInterviewTool` | Inspector Chen | - | Records W-A to W-F |
| `TimelineBuilderTool` | Inspector Chen | - | Creates minute-by-minute timeline |
| `KnowledgeGraphWriter` | Inspector Chen | Knowledge Graph | Builds temporal/spatial graph |
| `HANAVectorStoreQuery` | Chief Reeves | HANA Vector Store | Semantic search ("who wears gloves?") |
| `GroundingServiceTool` | Chief Reeves | Grounding Service (RAG) | Validates claims vs. evidence |
| `KnowledgeGraphQuery` | Chief Reeves | Knowledge Graph | Queries alibi gaps |
| `DeductiveReasoningTool` | Chief Reeves | - | Builds logical proof chain |
| `ReportGenerationTool` | Chief Reeves | - | Creates final PDF report |

---

This simplified 3-agent design is perfect for a **focused 2-day workshop** while still showcasing the full power of SAP AI tools! 🎯

























# Multi-Agent Crime Investigation System Design
## Using SAP AI Tools + CrewAI Framework

---

## 🎯 Overall Architecture

```
Evidence Collection → Analysis → Cross-Reference → Deduction → Report
     ↓                  ↓            ↓              ↓          ↓
  Agents 1-3        Agents 4-6    Agents 7-8    Agent 9   Agent 10
```

---

## 👥 Agent Roster (10 Specialized Agents)

### **1. Crime Scene Investigator (CSI Agent)**
**Role**: First responder; documents physical evidence at crime scene

**Personality**: Methodical, detail-oriented, technical

**Tools**:
- `EvidenceCollectionTool` - Captures physical evidence (E-1 to E-7)
- `PhotoDocumentationTool` - Takes scene photos
- `SAP_VectorStore_Writer` - Stores evidence descriptions in HANA Vector Store with embeddings

**Tasks**:
- Document body position, blood spatter, weapon location
- Collect physical items (glove, footprints, cigar stub)
- Create initial evidence manifest
- Tag evidence with location, timestamp, description

**SAP Tech**: HANA Vector Store (store evidence descriptions as embeddings for semantic search later)

---

### **2. Forensics Analyst**
**Role**: Analyzes physical evidence scientifically

**Personality**: Analytical, precise, skeptical

**Tools**:
- `FingerprintAnalysisTool` - Analyzes E-2 (smudged prints)
- `MaterialAnalysisTool` - Examines glove tear (E-1), leather dye (E-5)
- `ChemicalTraceTool` - Analyzes perfume/cigar residue (E-6)
- `SAP_Classification_RPT1` - Classifies evidence type (textile, chemical, biological)

**Tasks**:
- Determine glove fabric type and tear pattern
- Compare fingerprint smudges with suspect prints
- Analyze perfume concentration (fresh vs. residual)
- Estimate footprint shoe size from E-3

**SAP Tech**: Classification Model RPT-1 (classify evidence types, match patterns)

---

### **3. Timeline Reconstruction Specialist**
**Role**: Builds minute-by-minute timeline from all sources

**Personality**: Logical, systematic, time-obsessed

**Tools**:
- `TimelineBuilderTool` - Constructs chronological events
- `SAP_KnowledgeGraph_Writer` - Creates temporal graph (nodes = events, edges = causality)
- `ConflictDetectionTool` - Flags timeline contradictions

**Tasks**:
- Map all witness statements to timeline
- Identify gaps in suspect locations (9:12-9:18 PM critical)
- Create visualization of movements
- Flag impossible alibis

**SAP Tech**: Knowledge Graph (temporal relationships between events, people, locations)

---

### **4. Witness Interview Coordinator**
**Role**: Systematically collects all witness statements

**Personality**: Empathetic, patient, organized

**Tools**:
- `InterviewTranscriptionTool` - Records W-A through W-F
- `SAP_VectorStore_Writer` - Stores statements as embeddings
- `StatementExtractionTool` - Pulls key facts (time, location, observations)

**Tasks**:
- Conduct interviews with Butler, Chef, Groundskeeper, Sommelier, Housemaid, Paramedic
- Document body language, hesitations, contradictions
- Cross-reference times mentioned by different witnesses
- Create witness credibility scores

**SAP Tech**: HANA Vector Store (semantic search across statements for contradictions)

---

### **5. Suspect Profiler**
**Role**: Analyzes suspect backgrounds, motives, psychological traits

**Personality**: Insightful, psychological, intuitive

**Tools**:
- `MotiveAnalysisTool` - Identifies reasons to harm victim
- `BehaviorPatternTool` - Analyzes suspect personality traits
- `SAP_KnowledgeGraph_Query` - Finds relationship networks
- `SAP_Grounding_Service` - Grounds motive theories in evidence

**Tasks**:
- Profile Clara (quick temper, humiliation motive)
- Profile Julian (money disputes)
- Profile Evelyn (estranged lover)
- Profile Samuel (loyalty conflicts)
- Map relationship dynamics (Victor → suspects)

**SAP Tech**: Knowledge Graph (relationship mapping), Grounding Service (validate theories against evidence)

---

### **6. Statement Verification Agent**
**Role**: Cross-checks suspect statements against evidence

**Personality**: Skeptical, adversarial, thorough

**Tools**:
- `ContradictionFinderTool` - Compares S-1 to S-4 vs. E-1 to E-7
- `SAP_VectorStore_Query` - Semantic search for conflicting statements
- `SAP_Grounding_Service` - Validates claims against physical evidence
- `LieDetectionHeuristicTool` - Flags vague/evasive language

**Tasks**:
- Compare Clara's "went straight to library" vs. missing alibi
- Check Julian's "postponed meeting" vs. note E-7
- Verify Evelyn's "didn't go near music room" vs. perfume E-6
- Validate Samuel's "moved candelabra after" vs. polish smudges

**SAP Tech**: Vector Store (semantic similarity search), Grounding Service (RAG-based fact-checking)

---

### **7. Location Tracking Analyst**
**Role**: Maps physical movements through mansion

**Personality**: Spatial thinker, visual, meticulous

**Tools**:
- `FloorPlanMappingTool` - Creates mansion layout
- `MovementTrackerTool` - Plots footprints, door touches, perfume trails
- `SAP_KnowledgeGraph_Query` - Queries spatial relationships
- `PathCalculationTool` - Calculates time to move between rooms

**Tasks**:
- Map muddy footprints garden → dining room → music room
- Calculate: Can Evelyn reach powder room + return in timeframe?
- Track candelabra movement (dining room 8:55 → crime scene 9:12)
- Identify chokepoints (who could access music room unnoticed)

**SAP Tech**: Knowledge Graph (spatial nodes for rooms, edges for paths)

---

### **8. Opportunity Window Analyzer**
**Role**: Determines who COULD have committed murder in 9:12-9:18 window

**Personality**: Logical, elimination-focused, procedural

**Tools**:
- `AlibiValidationTool` - Tests each suspect's claim
- `SAP_KnowledgeGraph_Query` - Queries "Who was WHERE at 9:12-9:18?"
- `OpportunityMatrixTool` - Creates grid (suspect × time × location)
- `SAP_Grounding_Service` - Validates opportunity against witness statements

**Tasks**:
- Julian: In library until 9:10 → ELIMINATED (no time to detour)
- Evelyn: At powder room 9:08 → ELIMINATED (dye mark timing proves early exit)
- Samuel: East hall 9:10 → ELIMINATED (too far away)
- Clara: NO ALIBI 9:07-9:20 → SUSPECT

**SAP Tech**: Knowledge Graph (temporal queries), Grounding Service (RAG over witness statements)

---

### **9. Deductive Reasoning Agent (Sherlock)**
**Role**: Synthesizes all evidence into logical proof chain

**Personality**: Brilliant, confident, dramatic

**Tools**:
- `LogicalInferenceTool` - Builds "if-then" chains
- `SAP_Grounding_Service` - Ensures every inference is evidence-backed
- `SAP_VectorStore_Query` - Pulls all relevant evidence for final theory
- `HypothesisTestingTool` - Tests "Clara did it" against ALL evidence

**Tasks**:
- Build reasoning chain:
  1. Torn glove (E-1) → Clara wears gloves → She was at scene
  2. Muddy prints (E-3) → Small shoes + garden → Clara's path
  3. No alibi 9:07-9:20 → Opportunity window matches
  4. Motive: Public humiliation at 8:35
- Test alternate theories (Could Julian? No - cigar alibi holds)
- Produce final accusation with confidence score

**SAP Tech**: Grounding Service (RAG over entire evidence base), Vector Store (semantic retrieval)

---

### **10. Case Report Compiler**
**Role**: Generates final investigative report for prosecution

**Personality**: Professional, comprehensive, authoritative

**Tools**:
- `ReportGenerationTool` - Creates structured document
- `SAP_VectorStore_Query` - Retrieves all evidence summaries
- `SAP_KnowledgeGraph_Export` - Generates evidence relationship diagrams
- `LegalFormattingTool` - Formats for court submission

**Tasks**:
- Executive summary (Clara guilty, weapon: candelabra, time: 9:12-9:18)
- Evidence catalog (E-1 to E-7 explained)
- Witness statement index (W-A to W-F)
- Suspect statement contradictions (S-1 exposed)
- Timeline visualization
- Recommendation: Arrest Clara Beaumont

**SAP Tech**: All systems (final query/export from Vector Store, Knowledge Graph)

---

## 🛠️ SAP AI Tools Mapping

| **SAP Tool** | **Agents Using It** | **Purpose** |
|--------------|---------------------|-------------|
| **HANA Vector Store** | CSI, Witness Coordinator, Statement Verifier, Sherlock, Report Compiler | Store evidence/statements as embeddings; semantic search for contradictions |
| **Classification RPT-1** | Forensics Analyst | Classify evidence types (textile, chemical, trace); match patterns |
| **Grounding Service (RAG)** | Suspect Profiler, Statement Verifier, Opportunity Analyzer, Sherlock | Validate theories against evidence corpus; fact-check claims |
| **Knowledge Graph** | Timeline Specialist, Suspect Profiler, Location Tracker, Opportunity Analyzer, Report Compiler | Model relationships (temporal, spatial, social); query paths |

---

## 📋 CrewAI Implementation Structure

```python
from crewai import Agent, Task, Crew, Process
from langchain.tools import Tool

# === AGENTS ===
csi_agent = Agent(
    role="Crime Scene Investigator",
    goal="Document all physical evidence at crime scene",
    backstory="15 years experience in forensics; meticulous documenter",
    tools=[evidence_collection_tool, hana_vector_writer],
    verbose=True
)

forensics_agent = Agent(
    role="Forensics Analyst",
    goal="Scientifically analyze physical evidence",
    backstory="PhD in forensic chemistry; pattern recognition expert",
    tools=[fingerprint_tool, material_analysis_tool, rpt1_classifier],
    verbose=True
)

timeline_agent = Agent(
    role="Timeline Reconstruction Specialist",
    goal="Build minute-by-minute timeline of events",
    backstory="Former military intelligence; temporal analysis obsessed",
    tools=[timeline_builder, knowledge_graph_writer, conflict_detector],
    verbose=True
)

witness_agent = Agent(
    role="Witness Interview Coordinator",
    goal="Collect all witness statements systematically",
    backstory="Trained FBI interviewer; reads body language",
    tools=[interview_transcription_tool, hana_vector_writer, statement_extractor],
    verbose=True
)

profiler_agent = Agent(
    role="Suspect Profiler",
    goal="Analyze motives and psychological patterns",
    backstory="Criminal psychologist; 200+ cases profiled",
    tools=[motive_analysis_tool, knowledge_graph_query, grounding_service],
    verbose=True
)

verifier_agent = Agent(
    role="Statement Verification Agent",
    goal="Cross-check suspect statements vs evidence",
    backstory="Skeptical prosecutor; never accepts first story",
    tools=[contradiction_finder, hana_vector_query, grounding_service],
    verbose=True
)

location_agent = Agent(
    role="Location Tracking Analyst",
    goal="Map physical movements through crime scene",
    backstory="Architect turned detective; spatial reasoning genius",
    tools=[floorplan_mapper, movement_tracker, knowledge_graph_query],
    verbose=True
)

opportunity_agent = Agent(
    role="Opportunity Window Analyzer",
    goal="Determine who could commit murder in time window",
    backstory="Process engineer; elimination method specialist",
    tools=[alibi_validator, knowledge_graph_query, grounding_service],
    verbose=True
)

sherlock_agent = Agent(
    role="Deductive Reasoning Agent",
    goal="Synthesize evidence into logical proof",
    backstory="Famous for 98% solve rate; dramatic flair",
    tools=[logical_inference_tool, grounding_service, hana_vector_query],
    verbose=True
)

reporter_agent = Agent(
    role="Case Report Compiler",
    goal="Generate prosecution-ready final report",
    backstory="Legal writer; 20 years documenting complex cases",
    tools=[report_generator, hana_vector_query, knowledge_graph_export],
    verbose=True
)

# === TASKS ===
task1 = Task(
    description="Document all physical evidence at music room crime scene (E-1 to E-7)",
    agent=csi_agent,
    expected_output="Evidence manifest with photos, locations, descriptions"
)

task2 = Task(
    description="Analyze torn glove, fingerprints, footprints, perfume traces scientifically",
    agent=forensics_agent,
    expected_output="Forensic report: glove ownership, print matches, perfume freshness"
)

task3 = Task(
    description="Build complete timeline from 7:45 PM to 9:20 PM with all events",
    agent=timeline_agent,
    expected_output="Minute-by-minute timeline with gaps highlighted"
)

task4 = Task(
    description="Interview Butler, Chef, Groundskeeper, Sommelier, Housemaid, Paramedic",
    agent=witness_agent,
    expected_output="6 transcribed witness statements with key facts extracted"
)

task5 = Task(
    description="Profile Clara, Julian, Evelyn, Samuel: motives, relationships, psychology",
    agent=profiler_agent,
    expected_output="4 suspect profiles with motive rankings"
)

task6 = Task(
    description="Compare suspect statements (S-1 to S-4) against physical evidence",
    agent=verifier_agent,
    expected_output="Contradiction report: which statements are provably false"
)

task7 = Task(
    description="Map muddy footprints, perfume trails, candelabra movement through mansion",
    agent=location_agent,
    expected_output="Floor plan with movement paths and time estimates"
)

task8 = Task(
    description="Test each suspect's alibi for 9:12-9:18 PM murder window",
    agent=opportunity_agent,
    expected_output="Opportunity matrix: WHO could have done it"
)

task9 = Task(
    description="Synthesize all evidence into logical proof of guilt",
    agent=sherlock_agent,
    expected_output="Deductive reasoning chain identifying murderer with 95%+ confidence"
)

task10 = Task(
    description="Compile final investigation report for prosecution",
    agent=reporter_agent,
    expected_output="Comprehensive case file: evidence, timeline, proof, arrest warrant"
)

# === CREW ===
investigation_crew = Crew(
    agents=[
        csi_agent, forensics_agent, timeline_agent, 
        witness_agent, profiler_agent, verifier_agent,
        location_agent, opportunity_agent, sherlock_agent, reporter_agent
    ],
    tasks=[
        task1, task2, task3, task4, task5, 
        task6, task7, task8, task9, task10
    ],
    process=Process.sequential,  # Or Process.hierarchical with sherlock as manager
    verbose=2
)

# === EXECUTE ===
result = investigation_crew.kickoff()
print(result)
```

---

## 🔧 Custom Tools to Build

### 1. **SAP HANA Vector Store Tools**
```python
from langchain.tools import Tool
from hdbcli import dbapi

class HANAVectorWriter(Tool):
    name = "hana_vector_writer"
    description = "Stores evidence/statements as embeddings in SAP HANA Vector Store"
    
    def _run(self, text: str, metadata: dict):
        # Connect to HANA Cloud
        # Generate embedding (OpenAI/SAP models)
        # INSERT INTO evidence_vectors (id, embedding, metadata, text)
        pass

class HANAVectorQuery(Tool):
    name = "hana_vector_query"
    description = "Semantic search over evidence/statements"
    
    def _run(self, query: str, top_k: int = 5):
        # Generate query embedding
        # SELECT text, metadata FROM evidence_vectors ORDER BY COSINE_SIMILARITY
        pass
```

### 2. **SAP Classification RPT-1 Tool**
```python
class RPT1Classifier(Tool):
    name = "rpt1_classifier"
    description = "Classifies evidence into categories using SAP RPT-1"
    
    def _run(self, evidence_description: str):
        # Call SAP AI Core RPT-1 endpoint
        # POST /classify with evidence text
        # Returns: {type: "textile", confidence: 0.94, subcategory: "silk"}
        pass
```

### 3. **SAP Grounding Service Tool**
```python
class GroundingService(Tool):
    name = "grounding_service"
    description = "Validates claims against evidence corpus using RAG"
    
    def _run(self, claim: str):
        # Send claim to SAP Grounding Service
        # Retrieves relevant evidence chunks from Vector Store
        # Returns: {supported: True, evidence_ids: [E-1, E-3], confidence: 0.89}
        pass
```

### 4. **Knowledge Graph Tools**
```python
class KnowledgeGraphWriter(Tool):
    name = "kg_writer"
    description = "Adds nodes/edges to investigation knowledge graph"
    
    def _run(self, node_type: str, properties: dict, relationships: list):
        # CREATE (e:Event {time: "9:12 PM", location: "Music Room"})
        # CREATE (e)-[:PRECEDED_BY]->(previous_event)
        pass

class KnowledgeGraphQuery(Tool):
    name = "kg_query"
    description = "Queries knowledge graph with Cypher-like syntax"
    
    def _run(self, query: str):
        # MATCH (s:Suspect)-[:LOCATED_AT]->(l:Location)
        # WHERE l.time >= "9:12 PM" AND l.time <= "9:18 PM"
        # RETURN s.name, l.room
        pass
```

---

## 📊 Knowledge Graph Schema

```cypher
// NODES
(Person {name, role, traits})
(Location {room, floor})
(Evidence {id, type, description})
(Event {time, description})
(Statement {speaker, content, time_given})

// RELATIONSHIPS
(Person)-[:LOCATED_AT {time}]->(Location)
(Person)-[:MADE_STATEMENT]->(Statement)
(Person)-[:OWNS]->(Evidence)
(Evidence)-[:FOUND_AT]->(Location)
(Event)-[:PRECEDED_BY]->(Event)
(Statement)-[:CONTRADICTS]->(Statement)
(Person)-[:HAS_MOTIVE {strength}]->(Person)
```

**Example Query**:
```cypher
// Find who had no alibi during murder window
MATCH (s:Suspect)
WHERE NOT EXISTS {
  MATCH (s)-[:LOCATED_AT {time: "9:12-9:18"}]->(l:Location)
  WHERE (l)-[:WITNESSED_BY]->(:Witness)
}
RETURN s.name
// Result: Clara Beaumont
```

---

## 🎯 Developer Exercise Structure

### **Phase 1: Setup (Week 1)**
- Provision SAP HANA Cloud Vector Engine
- Deploy SAP AI Core with RPT-1 model
- Set up Grounding Service with evidence corpus
- Initialize Neo4j/SAP Graph for Knowledge Graph

### **Phase 2: Tool Development (Week 2)**
- Build HANA Vector Store read/write tools
- Integrate RPT-1 classification API
- Connect Grounding Service for RAG
- Implement Knowledge Graph CRUD tools

### **Phase 3: Agent Creation (Week 3)**
- Define 10 agents with personalities
- Assign tools to each agent
- Write task descriptions with expected outputs
- Configure CrewAI sequential process

### **Phase 4: Evidence Ingestion (Week 4)**
- Load E-1 to E-7 into Vector Store
- Load W-A to W-F into Vector Store
- Build initial Knowledge Graph (locations, people)
- Train RPT-1 on evidence classification (if custom)

### **Phase 5: Execution & Tuning (Week 5)**
- Run full crew investigation
- Debug agent handoffs
- Tune RAG grounding prompts
- Validate final accusation matches Clara

### **Phase 6: Visualization (Week 6)**
- Build dashboard showing:
  - Timeline visualization
  - Knowledge Graph 3D view
  - Evidence confidence scores
  - Agent reasoning chains
- Export final report PDF

---

## 📈 Success Metrics

1. **Accuracy**: Does Sherlock agent correctly identify Clara?
2. **Evidence Coverage**: Are all E-1 to E-7 referenced in reasoning?
3. **Contradiction Detection**: Does verifier catch Clara's glove lie?
4. **Timeline Gaps**: Does opportunity agent identify 9:07-9:20 gap?
5. **RAG Precision**: Does grounding service correctly validate/refute claims?
6. **Knowledge Graph Completeness**: Can we query any relationship?

---

## 🚀 Advanced Extensions

1. **Adversarial Agent**: Add "Defense Attorney" agent that tries to exonerate Clara
2. **Uncertainty Modeling**: Agents express confidence scores (Bayesian)
3. **Multi-modal Evidence**: Add crime scene photos analyzed by vision models
4. **Real-time Collaboration**: Agents debate in Slack channel
5. **What-If Scenarios**: "What if Julian's cigar was planted?"

---

This design gives developers hands-on experience with:
- ✅ SAP HANA Vector Store (embeddings, semantic search)
- ✅ RPT-1 Classification (evidence categorization)
- ✅ Grounding Service (RAG-based fact-checking)
- ✅ Knowledge Graphs (temporal/spatial reasoning)
- ✅ CrewAI (multi-agent orchestration)
- ✅ Complex reasoning chains (deductive logic)

Perfect for a **2-day workshop** or **6-week learning path**! 🎓