# Auto-Logger2139

Logger2139 is a Flask-based web application that automates the login process and navigation actions on the 2139 Exchange platform. The application uses Selenium to fill in login credentials, navigate to specific pages, and execute actions such as confirming transactions.

## Project Purpose

The purpose of this project is to demonstrate a basic use of Flask integrated with Selenium WebDriver to automate web interactions. The app automates the login process on the 2139 Exchange platform, navigates to a specific transaction page, and attempts to confirm a transaction.

## How to Run the Project

### Prerequisites

Before running the project, make sure you have the following installed on your machine:

- **Python 3.x**: You can download it from [python.org](https://www.python.org/downloads/).
- **Pip**: This usually comes with Python. If not, you can install it [here](https://pip.pypa.io/en/stable/installation/).
- **Google Chrome**: Ensure you have Chrome installed on your machine.
- **ChromeDriver**: Ensure that ChromeDriver is installed and its version matches your Chrome browser version. You can download it from [ChromeDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads).
- **Flask**: Install Flask using pip: `pip install Flask`.
- **Selenium**: Install Selenium using pip: `pip install selenium`.

### Installation


1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Logger2139.git
   cd Logger2139

2. **Install Required Python Packages**:
Install the necessary packages using pip:

  ```bash
  Copy code
  pip install -r requirements.txt
  ```
If there is no requirements.txt file, install Flask and Selenium manually:
  
  ```bash
  Copy code
  pip install Flask selenium
  ```


3. **Download ChromeDriver and place it in a directory**.
Update the chrome_driver_path in the login function in app.py to point to your ChromeDriver executable.
Running the Application
To run the Flask application:

Run the Flask App:

bash
Copy code
python app.py
Access the App:

4.**Open your web browser and go to http://127.0.0.1:5000/**.
Fill in the login form with the URL, email, and password.
Watch the Automation

Troubleshooting
Error: Chromedriver executable needs to be in PATH:
Ensure the chrome_driver_path in the code points to the correct location of your ChromeDriver executable.
Selenium version mismatch:
Make sure your Selenium version is compatible with your ChromeDriver and Chrome browser versions.
