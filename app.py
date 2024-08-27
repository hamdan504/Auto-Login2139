from flask import Flask, request, render_template_string
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
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
async def login():
    url = request.form['url']
    email = request.form['email']
    password = request.form['password']

    async with async_playwright() as p:
        browser_type = p.chromium
        browser_args = ['--no-sandbox', '--disable-gpu']
        is_vercel = os.environ.get('VERCEL_ENV')

        if is_vercel:
            headless = True
        else:
            headless = False  # Show browser locally

        browser = await browser_type.launch(headless=headless, args=browser_args)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            # Rest of the code remains the same
        except PlaywrightTimeoutError as e:
            return f"Timeout error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            if not is_vercel:
                input("Press Enter to close the browser...")
            await browser.close()

if __name__ == '__main__':
    app.run(debug=True)