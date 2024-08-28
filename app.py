from flask import Flask, request, jsonify, render_template_string
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BROWSERLESS_API_KEY = os.getenv('BROWSERLESS_API_KEY')
BROWSERLESS_ENDPOINT = f"https://chrome.browserless.io/function?token={BROWSERLESS_API_KEY}"

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

    script = f"""
    module.exports = async ({{
        browser
    }}) => {{
        const page = await browser.newPage();
        await page.goto('{url}', {{waitUntil: 'networkidle0'}});

        await page.click("div.choose-btn:text('Email')");
        await page.type("input[type='text'][placeholder='Please enter your email address']", '{email}');
        await page.type("input[type='password'][placeholder='Please enter your password']", '{password}');
        await page.click("div.login-btn");

        await page.waitForNavigation({{waitUntil: 'networkidle0'}});

        if (page.url() !== '{url}') {{
            await page.goto('https://2139.online/pc/#/contractTransaction', {{waitUntil: 'networkidle0'}});

            await page.click("div:text('invited me')");
            await page.waitForTimeout(3000);

            try {{
                await page.click("div:text(' Confirm to follow the order')");
                await page.click("button > span:text('Confirm')");
                await page.waitForTimeout(3000);
                return "Successfully completed the transaction!";
            }} catch (error) {{
                return "No transaction found or buttons were not available.";
            }}
        }} else {{
            return "Login may have failed. Please check the credentials.";
        }}

        await browser.close();
    }};
    """

    payload = {
        'code': script,
    }

    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(BROWSERLESS_ENDPOINT, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
