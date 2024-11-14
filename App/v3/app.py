from flask import Flask, render_template_string, request, redirect, url_for
import socket
import os

app = Flask(__name__)

DATA_FILE_PATH = "/data/messages.txt"

@app.route('/', methods=['GET', 'POST'])
def greeting():
    # Get the hostname to show node or pod instance information
    hostname = socket.gethostname()
    
    # Handle form submission
    if request.method == 'POST':
        # Get the text input from the form
        new_message = request.form.get('message')
        # Append the new message to the file in /data
        with open(DATA_FILE_PATH, "a") as file:
            file.write(new_message + "\n")
        # Redirect to GET request to display the updated table
        return redirect(url_for('greeting'))
    
    # Read all messages from the file
    messages = []
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, "r") as file:
            messages = [line.strip() for line in file.readlines()]

    # HTML template with a green background
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kubernetes App</title>
        <style>
            body {
                background-color: #32CD32; /* Lime green */
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

    # Render the HTML template with hostname and messages
    return render_template_string(html_template, hostname=hostname, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
