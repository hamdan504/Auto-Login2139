from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <form action="/login" method="post">
            <label for="url">URL:</label>
            <input type="text" id="url" name="url"><br>
            <label for="email">Email:</label>
            <input type="text" id="email" name="email"><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    url = request.form['url']
    email = request.form['email']
    password = request.form['password']
    
    chrome_driver_path = ".wdm\chromedriver-win64\chromedriver.exe"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    try:
        driver = webdriver.Chrome(service=ChromeService(executable_path=chrome_driver_path), options=options)
        driver.get(url)
        
        email_login_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Email')]")
        email_login_button.click()
        
        email_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'][placeholder='Please enter your email address']")
        email_field.send_keys(email)
        
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='Please enter your password']")
        password_field.send_keys(password)
        
        login_button = driver.find_element(By.CSS_SELECTOR, "div.login-btn")
        login_button.click()
        time.sleep(2)
        
        # Check if the user is logged in by looking for an element that's only present when logged in
        if driver.current_url != url:
            trade_url = "https://2139.online/pc/#/contractTransaction"
            driver.get(trade_url)
            time.sleep(1)
            
            invited_me_button = driver.find_element(By.XPATH, "//div[contains(text(), 'invited me')]")
            invited_me_button.click()
            time.sleep(3)


            try:
                confirm_order = driver.find_element(By.XPATH, "//div[contains(text(), ' Confirm to follow the order')]")
                confirm_order.click()
                time.sleep(3)

                confirm_button = driver.find_element(By.XPATH, "//button/span[contains(text(), 'Confirm')]")
                confirm_button.click()
                time.sleep(50)
                return "Successfully completed the transaction!"
                        
            except NoSuchElementException:
                # If the "confirm order" button is not found, wait before closing
                time.sleep(50)
                return "No transaction found or buttons were not available."
                        
        else:
            return "Login failed or session not maintained properly."

    except Exception as e:
        return f"Error: {e}"

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
