# Running Addict Plan Extractor

## Description

Running Addict Plan Extractor is a tool designed to help you extract running training plans from [Running Addict](https://www.running-addict.fr/), and to create Garmin workouts from these plans without the need for manual intervention.

## Installation

1. Clone the repository:

   **Linux/macOS:**

   ```bash
   git clone https://github.com/OscarBrugne/running-addict-plan-extractor.git
   cd running-addict-plan-extractor
   ```

   **Windows:**

   ```cmd
   git clone https://github.com/OscarBrugne/running-addict-plan-extractor.git
   cd running-addict-plan-extractor
   ```

2. Create a virtual environment and activate it:

   **Linux/macOS:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows:**

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the required dependencies:

   **Linux/macOS:**

   ```bash
   pip install -r requirements.txt
   ```

   **Windows:**

   ```cmd
   pip install -r requirements.txt
   ```

## Usage

**Linux/macOS:**

```bash
python3 -m running_addict_plan_extractor
```

**Windows:**

```cmd
python -m running_addict_plan_extractor
```
