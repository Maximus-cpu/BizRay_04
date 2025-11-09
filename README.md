# BizRay_04

## Setup Instructions
#### Prerequisites
- Python ≥ 3.7
- `git`

### 1. Clone the repository
```bash
git clone <repository_url>
cd <repository_directory_locally>
```

### 2. Set up a virtual environment
#### Linux/Mac:
```bash
py -m venv venv
source .venv/bin/activate
```
#### Windows (cmd):
```bash
py -m venv venv
venv\Scripts\activate
```
#### Windows (PowerShell):
```bash
py -m venv venv
venv\Scripts\Activate.ps1
```

#### !!! Important: If you get an error for unauthorized access while trying to activate the virtual environment, please run the following command to allow for script execution for the current session:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### !!! Important: If you are using Pycharm, it is usually necessary to navigate to:
- Settings → Project: your_project → Python Interpreter
- Click the ⚙️ icon (top right of the interpreter list).
- Select Add Interpreter → Add Local Interpreter.
- Create an environment from your local python installation.
- Navigate to your virtual environment’s Python executable
  - Windows: venv\Scripts\python.exe
  - macOS/Linux: venv/bin/python
- Click OK and apply the changes.

### 4. Initialize the database (only required once)
```bash
flask db upgrade
```
- Whenever you pull new commits that include updates to the models or migration scripts (models and migrations folders), run this command again.

### 5. Run the Flask application
```bash
py run.py
```

### 6. Open the web application
- Open http://127.0.0.1:5000 in your browser

### 7. Deactivate virtual environment
```bash
deactivate
```
