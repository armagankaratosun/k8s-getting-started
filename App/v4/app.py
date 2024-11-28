from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import socket
import os
import time
import logging
import json

app = Flask(__name__)

DATA_FILE_PATH = "/data/messages.txt"
start_time = time.time()
app_health = "unhealthy"  # Initial assumption of health

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

@app.route('/', methods=['GET', 'POST'])
def greeting():
    # Check health status
    if app_health != "healthy":
        return jsonify(message="Loading..."), 503

    hostname = socket.gethostname()
    
    if request.method == 'POST':
        new_message = request.form.get('message')
        with open(DATA_FILE_PATH, "a") as file:
            file.write(new_message + "\n")
        return redirect(url_for('greeting'))
    
    messages = []
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, "r") as file:
            messages = [line.strip() for line in file.readlines()]

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kubernetes App</title>
        <style>
            body {
                background-color: #32CD32;
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                font-family: Arial, sans-serif;
            }
            .container {
                text-align: center;
                margin-top: 50px;
            }
            h1 {
                font-size: 2em;
            }
            table {
                margin-top: 20px;
                border-collapse: collapse;
                width: 50%;
            }
            table, th, td {
                border: 1px solid white;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #228B22;
            }
            td {
                background-color: #3CB371;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello, welcome to our Kubernetes app!</h1>
            <p>Hostname: {{ hostname }}</p>
            <form method="POST">
                <input type="text" name="message" placeholder="Enter your message" required>
                <button type="submit">Submit</button>
            </form>
            <table>
                <tr><th>Messages</th></tr>
                {% for message in messages %}
                <tr><td>{{ message }}</td></tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, hostname=hostname, messages=messages), 200

@app.route('/healthz', methods=['GET'])
def healthz():
    current_time = time.time()
    global app_health
    if current_time - start_time >= 15:
        app_health = "healthy"
        return jsonify(status="healthy"), 200
    else:
        app_health = "unhealthy"
        log_message = {"message": "The application requires 15 seconds to start."}
        logging.info(json.dumps(log_message))
        return jsonify(status="unhealthy"), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
