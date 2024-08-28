from flask import Flask, request, render_template_string
import asyncio
import logging
import traceback
from pyppeteer import launch
from pyppeteer.errors import TimeoutError

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
    try:
        browser = await launch(args=['--no-sandbox', '--disable-setuid-sandbox'])
        page = await browser.newPage()

        logger.info(f"Navigating to URL: {url}")
        await page.goto(url, waitUntil='networkidle0', timeout=60000)
        
        # Wait for and click the "Email" button
        logger.info("Waiting for 'Email' button")
        await page.waitForSelector("div.choose-btn:text('Email')", timeout=30000)
        await page.click("div.choose-btn:text('Email')")

        # Fill in the email
        logger.info("Filling in email")
        email_input = await page.waitForSelector("input[type='text'][placeholder='Please enter your email address']", timeout=30000)
        await email_input.type(email)

        # Fill in the password
        logger.info("Filling in password")
        password_input = await page.waitForSelector("input[type='password'][placeholder='Please enter your password']", timeout=30000)
        await password_input.type(password)

        # Click the login button
        logger.info("Clicking login button")
        await page.click("div.login-btn")

        # Wait for navigation or a specific element that indicates successful login
        logger.info("Waiting for navigation after login")
        await page.waitForNavigation(timeout=30000)

        # Check if login was successful
        if page.url != url:
            logger.info("Login successful, performing additional actions")
            # If login successful, perform additional actions
            trade_url = "https://2139.online/pc/#/contractTransaction"
            await page.goto(trade_url, waitUntil='networkidle0', timeout=30000)

            # Click "invited me" button
            logger.info("Clicking 'invited me' button")
            invited_me_button = await page.waitForSelector("div:text('invited me')", timeout=30000)
            await invited_me_button.click()
            await page.waitFor(3000)

            try:
                logger.info("Attempting to confirm order")
                confirm_order = await page.waitForSelector("div:text(' Confirm to follow the order')", timeout=30000)
                await confirm_order.click()
                await page.waitFor(3000)

                confirm_button = await page.waitForSelector("button > span:text('Confirm')", timeout=30000)
                await confirm_button.click()
                await page.waitFor(50000)
                logger.info("Transaction completed successfully")
                return "Successfully completed the transaction!"

            except TimeoutError:
                logger.warning("No transaction found or buttons were not available")
                return "No transaction found or buttons were not available."

        else:
            logger.warning("Login may have failed")
            return "Login may have failed. Please check the credentials."

    except TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
        return f"Timeout error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return f"Error: {str(e)}\n\nStacktrace: {traceback.format_exc()}"
    finally:
        if browser:
            await browser.close()
            logger.info("Browser closed")

if __name__ == '__main__':
    app.run(debug=True)