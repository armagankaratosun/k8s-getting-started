from flask import Flask, render_template_string
import socket

app = Flask(__name__)

@app.route('/')
def greeting():
    # Get the hostname to show node or pod instance information
    hostname = socket.gethostname()

    # HTML template with green background
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
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: Arial, sans-serif;
            }
            .container {
                text-align: center;
            }
            h1 {
                font-size: 2em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello, welcome to our Kubernetes app!</h1>
            <p>Hostname: {{ hostname }}</p>
        </div>
    </body>
    </html>
    """

    # Render the HTML template with hostname
    return render_template_string(html_template, hostname=hostname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
