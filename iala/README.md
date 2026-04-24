# Intelligent Adaptive Learning Assistant (IALA)

This is the core infrastructure for the Intelligent Adaptive Learning Assistant, a system that personalizes education using a Socratic teaching approach, Knowledge Graphs, and stateful multi-turn learning loops.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database:**
   The SQLite database (`iala.db`) will be automatically created on application startup. SQLAlchemy is used as the ORM.

3. **Knowledge Graph Simulation:**
   For Phase 1, the Knowledge Graph is manually simulated using a Python dictionary-based adjacency list in `services/knowledge_graph.py`. No external Neo4j setup is required for the MVP.

4. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`. 
   Swagger docs are available at `http://127.0.0.1:8000/docs`.

## API Endpoints

- `POST /session/start`: Initializes a new learning path.
- `POST /session/respond`: Submits user input and retrieves the next Socratic response (instruction, assessment, or remediation).
