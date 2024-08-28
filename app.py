from flask import Flask, request, render_template_string
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import os
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
async def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
async def login():
    url = request.form['url']
    email = request.form['email']
    password = request.form['password']

    logger.info(f"Attempting login for URL: {url}")

    browser = None
    async with async_playwright() as p:
        browser_type = p.chromium
        browser_args = ['--no-sandbox', '--disable-setuid-sandbox', '--single-process']

        try:
            # Use a custom browser path for Vercel environment
            custom_browser_path = '/tmp/chromium/chrome'
            logger.info(f"Launching browser with custom path: {custom_browser_path}")
            
            browser = await browser_type.launch(
                headless=True,
                args=browser_args,
                executable_path=custom_browser_path
            )
            logger.info("Browser launched successfully")

            context = await browser.new_context()
            page = await context.new_page()

            logger.info(f"Navigating to URL: {url}")
            await page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Wait for and click the "Email" button
            logger.info("Waiting for 'Email' button")
            await page.wait_for_selector("div.choose-btn:text('Email')", timeout=30000)
            await page.click("div.choose-btn:text('Email')")

            # Fill in the email
            logger.info("Filling in email")
            email_input = await page.wait_for_selector("input[type='text'][placeholder='Please enter your email address']", timeout=30000)
            await email_input.fill(email)

            # Fill in the password
            logger.info("Filling in password")
            password_input = await page.wait_for_selector("input[type='password'][placeholder='Please enter your password']", timeout=30000)
            await password_input.fill(password)

            # Click the login button
            logger.info("Clicking login button")
            await page.click("div.login-btn")

            # Wait for navigation or a specific element that indicates successful login
            logger.info("Waiting for navigation after login")
            await page.wait_for_load_state('networkidle', timeout=30000)

            # Check if login was successful
            if page.url != url:
                logger.info("Login successful, performing additional actions")
                # If login successful, perform additional actions
                trade_url = "https://2139.online/pc/#/contractTransaction"
                await page.goto(trade_url, wait_until="networkidle", timeout=30000)

                # Click "invited me" button
                logger.info("Clicking 'invited me' button")
                invited_me_button = await page.wait_for_selector("div:text('invited me')", timeout=30000)
                await invited_me_button.click()
                await page.wait_for_timeout(3000)

                try:
                    logger.info("Attempting to confirm order")
                    confirm_order = await page.wait_for_selector("div:text(' Confirm to follow the order')", timeout=30000)
                    await confirm_order.click()
                    await page.wait_for_timeout(3000)

                    confirm_button = await page.wait_for_selector("button > span:text('Confirm')", timeout=30000)
                    await confirm_button.click()
                    await page.wait_for_timeout(50000)
                    logger.info("Transaction completed successfully")
                    return "Successfully completed the transaction!"

                except PlaywrightTimeoutError:
                    logger.warning("No transaction found or buttons were not available")
                    return "No transaction found or buttons were not available."

            else:
                logger.warning("Login may have failed")
                return "Login may have failed. Please check the credentials."

        except PlaywrightTimeoutError as e:
            logger.error(f"Timeout error: {str(e)}")
            return f"Timeout error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return f"Error: {str(e)}"
        finally:
            if browser:
                await browser.close()
                logger.info("Browser closed")
                
if __name__ == '__main__':
    app.run(debug=True)