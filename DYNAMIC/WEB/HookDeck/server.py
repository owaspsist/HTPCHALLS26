import os
import uuid
import re
import threading
import time
from flask import Flask, request, render_template, redirect, url_for, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)
FLAG = os.environ.get("GZCTF_FLAG", "flag{webhook_data_flow_hijack_success}")

storage = {}

def filter_xss(html_content):
    if not html_content:
        return ""
    sanitized = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', html_content, flags=re.IGNORECASE|re.DOTALL)
    sanitized = re.sub(r'(?i)on[a-z]+\s*=', 'data-blocked=', sanitized)
    sanitized = re.sub(r'(?i)href\s*=\s*["\']javascript:', 'href="#', sanitized)
    return sanitized

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    user_markup = request.form.get('markup', '')
    template_id = str(uuid.uuid4())
    storage[template_id] = filter_xss(user_markup)
    return redirect(url_for('preview', template_id=template_id))

@app.route('/preview/<template_id>')
def preview(template_id):
    if template_id not in storage:
        return "Template configuration not found", 404
    return render_template('preview.html', markup=storage[template_id], template_id=template_id)

def execute_browser_bot(template_id):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--single-process') # PROD FIX: Prevents Docker memory exhaustion crashes
    chrome_options.add_argument('--ignore-certificate-errors')
    
    chrome_service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    try:
        # PROD FIX: Using localhost ensures explicit domain binding for the cookie
        driver.get("http://localhost:9992/")
        driver.add_cookie({
            "name": "FLAG",
            "value": FLAG,
            "domain": "localhost",
            "path": "/"
        })
        
        driver.get(f"http://localhost:9992/preview/{template_id}")
        
        # PROD FIX: Increased wait time to 8 seconds to allow fetch() to complete over network
        time.sleep(8) 
        
    except Exception as error:
        print(f"Automation engine exception: {error}")
    finally:
        driver.quit()

@app.route('/verify/<template_id>', methods=['POST'])
def verify(template_id):
    if template_id not in storage:
        return jsonify({"error": "Invalid target deployment context"}), 404
    
    threading.Thread(target=execute_browser_bot, args=(template_id,)).start()
    return jsonify({"status": "Verification worker dispatched to template context."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9992)
