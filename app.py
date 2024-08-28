from flask import Flask, request, render_template_string
import requests
import json
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

BROWSERLESS_API_KEY = os.getenv('BROWSERLESS_API_KEY')
BROWSERLESS_ENDPOINT = f'https://chrome.browserless.io/content?token={BROWSERLESS_API_KEY}'

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

    logger.info(f"Attempting login for URL: {url}")

    script = f"""
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('{url}', {{waitUntil: 'networkidle0'}});
    
    await page.waitForSelector("div.choose-btn:text('Email')");
    await page.click("div.choose-btn:text('Email')");
    
    await page.waitForSelector("input[type='text'][placeholder='Please enter your email address']");
    await page.type("input[type='text'][placeholder='Please enter your email address']", '{email}');
    
    await page.waitForSelector("input[type='password'][placeholder='Please enter your password']");
    await page.type("input[type='password'][placeholder='Please enter your password']", '{password}');
    
    await page.click("div.login-btn");
    
    await page.waitForNavigation({{waitUntil: 'networkidle0'}});
    
    if (page.url() !== '{url}') {{
        await page.goto('https://2139.online/pc/#/contractTransaction', {{waitUntil: 'networkidle0'}});
        
        await page.waitForSelector("div:text('invited me')");
        await page.click("div:text('invited me')");
        await page.waitForTimeout(3000);
        
        try {{
            await page.waitForSelector("div:text(' Confirm to follow the order')", {{timeout: 30000}});
            await page.click("div:text(' Confirm to follow the order')");
            await page.waitForTimeout(3000);
            
            await page.waitForSelector("button > span:text('Confirm')", {{timeout: 30000}});
            await page.click("button > span:text('Confirm')");
            await page.waitForTimeout(50000);
            
            return "Successfully completed the transaction!";
        }} catch (error) {{
            return "No transaction found or buttons were not available.";
        }}
    }} else {{
        return "Login may have failed. Please check the credentials.";
    }}
    """

    payload = {
        'code': script
    }

    try:
        response = requests.post(BROWSERLESS_ENDPOINT, json=payload)
        result = response.text
        logger.info(f"Browserless.io response: {result}")
        return result
    except Exception as e:
        logger.error(f"Error during Browserless.io request: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)