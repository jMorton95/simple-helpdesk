# simple-kanban
DJango Web-Application for my Software Engineering &amp; Agile module of a degree apprenticeship

# User Manual for Running and Debugging the Application

## 1.2.2 User Manual  
This user manual provides guidance to set up, run, and debug the application locally.

### 1.2.2.1 Prerequisites  
Ensure the following software is installed on your machine:  
- **Python 3**: Check the installed version using:  
  `python3 version`
- **PIP**: Install it if necessary:  
  `python -m ensurepip --upgrade`
- Install the **Virtual Environment** package using:  
  `pip install virtualenv`

### 1.2.2.2 Repository Setup  
After verifying the prerequisites:  
1. Open a terminal (e.g., PowerShell or Git Bash).  
2. Clone the repository:  
   `git clone git@github.com:jMorton95/simple-kanban.git`
3. Navigate to the project directory:  
   `cd simple-kanban`

### 1.2.2.3 Create and Activate Python Virtual Environment  
1. Create a virtual environment:  
   `python -m venv .simple-kanban`
2. Activate the virtual environment:  
   - For Windows:  
     `.simple-kanban\Scripts\activate`
3. Navigate to the project directory:  
   `cd app`
4. Install the project dependencies:  
   `pip install requirements.txt`

### 1.2.2.4 Running the Website  
Start the development server:  
   `python manage.py runserver`
   Once the server is running, open your web browser and navigate to: http://127.0.0.1:8000

### 1.2.2.5 Instructions for Visual Studio Code IDE  
1. After completing the steps above, open the command palette in VS Code with `Control + Shift + P`.  
2. Select the "Python: Select Interpreter" command and choose the virtual environment created earlier.  
3. Use the VS Code Debugger to run the server and set breakpoints throughout the codebase.

### 1.2.2.6 Instructions for JetBrains PyCharm IDE  
1. Open Run/Debug Configurations from the menu (`Run > Edit Configurations`).  
2. Add a new configuration by clicking the `+` icon and selecting "Django Server".  
3. Configure the following:
   - **Host**: `127.0.0.1`
   - **Port**: `8000`
   - **Environment Variables**: Ensure `DJANGO_SETTINGS_MODULE` is set to `simple_kanban.settings`.  
4. Save the configuration and use PyCharm's debugger to run the development server.
