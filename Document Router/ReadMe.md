# Document Router

This automated two-stage data ingestion pipeline iterates through text files that contain content with email, legal, and a review and categorizes and summarizes the contents using a local LLM, and then generates files containing the respective summaries with the respective category names as file names. 

Following this, a CSV summary file is created summarizing the contents into "Category", "Total Files", and "Average Summary Length". 

## Built with: 
- Python
- Ollama
- Llama3

## Key Features
* **Defensive Token Parsing:** Isolates non-deterministic LLM structural text generation from brittle string index dependencies.
* **Multi-Tier Directory Traversal:** Systematically processes local file storage blocks while filtering operating-system-level hidden files (e.g., `.DS_Store`).
* **Fault-Tolerant Schema Enforcement:** Employs explicit containment guards to handle unexpected categorical buckets without throwing runtime `KeyErrors`.

## Set-up: 

1. Clone the repository. Make sure you have Ollama installed on your desktop/PC and the Ollama runtime running in the background.

   `https://ollama.com/download/mac`.

2. Run the file `router.py` to create the subfolders with the summary text files from the files contained in the `documents` directory:

   ```bash
   python router.py
   ```

3. Run the file `metrics_engine.py` to create the CSV file containing the aggregated data:

   ```bash
   python metrics_engine.py
   ```

To make sure that the CSV file is generated, ensure that the folder names the LLM generates in the `storage` subfolder match the keys in `category_stats` in `metrics_engine.py`. (At the time of initiating this project, the key names were the names of the subfolders that the LLM generated which are "Intellectual Property", "Service Complaint", and "TECH". Unexpected categories are intercepted and skipped safely to protect report generation from `KeyErrors` or `ZeroDivisionErrors`.).

## Sample output: 

Report.csv:

Category,Total Files,Average Summary Length

Intellectual Property,1,198.0

Service Complaint,1,210.0

TECH,1,182.0
