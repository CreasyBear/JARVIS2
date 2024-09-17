# JARVIS Data Diagram

Last updated: [Current Date]

## Knowledge Base Structure

mermaid
graph TD
User[User Input] --> TaskPlanner[Task Planner Agent]
TaskPlanner --> AgentSelector[Agent Selector]
AgentSelector --> |Task Type| SpecializedAgent[Specialized Agent]
SpecializedAgent --> |Results| ResponseGenerator[Response Generator]
ResponseGenerator --> User
subgraph Knowledge Base
KB[Vector Store Index]
RawData[Raw Data]
RawData --> |Indexing| KB
end
subgraph Specialized Agents
InfoRetrieval[Info Retrieval Agent]
EnhancedInfoRetrieval[Enhanced Info Retrieval Agent]
Calculation[Calculation Agent]
Summarization[Summarization Agent]
WebScraping[Web Scraping Agent]
end
SpecializedAgent -.-> InfoRetrieval
SpecializedAgent -.-> EnhancedInfoRetrieval
SpecializedAgent -.-> Calculation
SpecializedAgent -.-> Summarization
SpecializedAgent -.-> WebScraping
InfoRetrieval --> |Query| KB
EnhancedInfoRetrieval --> |Query| KB
Calculation --> |Data Retrieval| KB
Summarization --> |Content Retrieval| KB
WebScraping --> |Store Data| KB


## Agents and Their Functions

| Agent | Status | Function |
|-------|--------|----------|
| Task Planner | Implemented | Analyzes user input and determines required tasks |
| Info Retrieval | Implemented | Basic information retrieval from knowledge base |
| Enhanced Info Retrieval | Implemented | Advanced retrieval using OpenAI Agent with Query Engine |
| Calculation | Implemented | Performs calculations using PandasQueryEngine |
| Summarization | Implemented | Summarizes content using transformers library |
| Web Scraping | In Development | Will scrape web content to update knowledge base |

## Process Flow

1. User Input → Task Planner
2. Task Planner → Agent Selector
3. Agent Selector → Appropriate Specialized Agent(s)
4. Specialized Agent(s) → Knowledge Base (if needed)
5. Specialized Agent(s) → Response Generator
6. Response Generator → User

## Checks and Evaluations

- Task Classification Accuracy
- Information Retrieval Relevance
- Calculation Precision
- Summarization Quality
- Overall Response Coherence

## Current Focus Areas

1. Testing and refining EnhancedInfoRetrievalAgent and SummarizationAgent
2. Developing WebScrapingAgent
3. Optimizing for local deployment
4. Populating initial knowledge base

## Planned Improvements

1. Implement advanced agent capabilities
2. Develop more sophisticated task planning
3. Set up continuous learning system
4. Implement security and privacy measures
5. Fine-tune agent selection and task delegation

## Integration Points

- LlamaIndex: Used for knowledge base implementation (VectorStoreIndex, SimpleDirectoryReader)
- OpenAI: Integrated with EnhancedInfoRetrievalAgent
- Pandas: Used with CalculationAgent
- Transformers: Used with SummarizationAgent

This document will be updated as the project progresses to reflect the current state of JARVIS's architecture and information flow.