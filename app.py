from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 8px;
            margin-bottom: 12px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <form action="/login" method="post">
        <label for="url">URL:</label>
        <input type="text" id="url" name="url" required><br>
        <label for="email">Email:</label>
        <input type="text" id="email" name="email" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
    '''

@app.route('/login', methods=['POST'])
def login():
    url = request.form['url']
    email = request.form['email']
    password = request.form['password']

    chrome_options = Options()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--headless')  # Optional: Run Chrome in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        # Wait for the email login button to be present
        email_login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Email')]"))
        )
        email_login_button.click()

        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][placeholder='Please enter your email address']"))
        )
        email_field.send_keys(email)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'][placeholder='Please enter your password']"))
        )
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.login-btn"))
        )
        login_button.click()
        time.sleep(2)

        if driver.current_url != url:
            trade_url = "https://2139.online/pc/#/contractTransaction"
            driver.get(trade_url)
            time.sleep(1)

            invited_me_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'invited me')]"))
            )
            invited_me_button.click()
            time.sleep(3)

            try:
                confirm_order = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Confirm to follow the order')]"))
                )
                confirm_order.click()
                time.sleep(3)

                confirm_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button/span[contains(text(), 'Confirm')]"))
                )
                confirm_button.click()
                time.sleep(50)
                return "Successfully completed the transaction!"

            except NoSuchElementException:
                return "No transaction found or buttons were not available."

        else:
            return "Login failed or session not maintained properly."

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        if driver is not None:
            driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
