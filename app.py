from flask import Flask, request, render_template_string
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Automation</title>
</head>
<body>
    <h1>Login Automation</h1>
    <form action="/login" method="post">
        <label for="url">URL:</label>
        <input type="text" id="url" name="url" required><br><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    url = request.form['url']
    email = request.form['email']
    password = request.form['password']

    with sync_playwright() as p:
        browser_type = p.chromium
        browser_args = []
        is_vercel = os.environ.get('VERCEL_ENV')
        
        if is_vercel:
            browser_args.append('--no-sandbox')
            headless = True
        else:
            headless = False  # Show browser locally

        browser = browser_type.launch(headless=headless, args=browser_args)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Wait for and click the "Email" button
            page.wait_for_selector("div.choose-btn:text('Email')", timeout=30000)
            page.click("div.choose-btn:text('Email')")

            # Fill in the email
            email_input = page.wait_for_selector("input[type='text'][placeholder='Please enter your email address']", timeout=30000)
            email_input.fill(email)

            # Fill in the password
            password_input = page.wait_for_selector("input[type='password'][placeholder='Please enter your password']", timeout=30000)
            password_input.fill(password)

            # Click the login button
            page.click("div.login-btn")

            # Wait for navigation or a specific element that indicates successful login
            page.wait_for_load_state('networkidle', timeout=30000)

            # Check if login was successful (you might need to adjust this check)
            if page.url != url:
                # If login successful, perform additional actions
                trade_url = "https://2139.online/pc/#/contractTransaction"
                page.goto(trade_url, wait_until="networkidle", timeout=30000)

                # Click "invited me" button
                invited_me_button = page.wait_for_selector("div:text('invited me')", timeout=30000)
                invited_me_button.click()
                page.wait_for_timeout(3000)

                try:
                    confirm_order = page.wait_for_selector("div:text(' Confirm to follow the order')", timeout=30000)
                    confirm_order.click()
                    page.wait_for_timeout(3000)

                    confirm_button = page.wait_for_selector("button > span:text('Confirm')", timeout=30000)
                    confirm_button.click()
                    page.wait_for_timeout(50000)
                    return "Successfully completed the transaction!"

                except PlaywrightTimeoutError:
                    return "No transaction found or buttons were not available."

            else:
                return "Login may have failed. Please check the credentials."

        except PlaywrightTimeoutError as e:
            return f"Timeout error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            if not is_vercel:
                input("Press Enter to close the browser...")
            browser.close()

if __name__ == '__main__':
    app.run(debug=True)