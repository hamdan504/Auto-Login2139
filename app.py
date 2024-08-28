from flask import Flask, request, render_template_string
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import os
import asyncio

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
        <input type="password" id="password" name="password" value="farm1pass" required><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route('/')
async def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
async def login():
    url = request.form['url']
    email = request.form['email']
    password = request.form['password']

    browser = None
    async with async_playwright() as p:
        browser_type = p.chromium
        browser_args = ['--no-sandbox', '--disable-setuid-sandbox', '--single-process']

        try:
            # Use a custom browser path for Vercel environment
            custom_browser_path = '/tmp/chromium/chrome'
            
            browser = await browser_type.launch(
                headless=True,
                args=browser_args,
                executable_path=custom_browser_path
            )
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Wait for and click the "Email" button
            await page.wait_for_selector("div.choose-btn:text('Email')", timeout=30000)
            await page.click("div.choose-btn:text('Email')")

            # Fill in the email
            email_input = await page.wait_for_selector("input[type='text'][placeholder='Please enter your email address']", timeout=30000)
            await email_input.fill(email)

            # Fill in the password
            password_input = await page.wait_for_selector("input[type='password'][placeholder='Please enter your password']", timeout=30000)
            await password_input.fill(password)

            # Click the login button
            await page.click("div.login-btn")

            # Wait for navigation or a specific element that indicates successful login
            await page.wait_for_load_state('networkidle', timeout=30000)

            # Check if login was successful
            if page.url != url:
                # If login successful, perform additional actions
                trade_url = "https://2139.online/pc/#/contractTransaction"
                await page.goto(trade_url, wait_until="networkidle", timeout=30000)

                # Click "invited me" button
                invited_me_button = await page.wait_for_selector("div:text('invited me')", timeout=30000)
                await invited_me_button.click()
                await page.wait_for_timeout(3000)

                try:
                    confirm_order = await page.wait_for_selector("div:text(' Confirm to follow the order')", timeout=30000)
                    await confirm_order.click()
                    await page.wait_for_timeout(3000)

                    confirm_button = await page.wait_for_selector("button > span:text('Confirm')", timeout=30000)
                    await confirm_button.click()
                    await page.wait_for_timeout(50000)
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
            if browser:
                await browser.close()
                
if __name__ == '__main__':
    app.run(debug=True)