import os
import requests
from flask import Flask, request, abort, render_template_string

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/nenenen/main/cousins.json"

@app.route("/cousin/<user_id>", methods=["GET", "POST"])
def cousin_profile(user_id):
    # Fetch latest JSON from GitHub for live updates
    try:
        resp = requests.get(JSON_URL)
        resp.raise_for_status()
        cousins = resp.json()
    except Exception as e:
        return f"❌ Could not load data: {e}", 500

    data = cousins.get(user_id)
    if not data:
        return abort(404)

    if request.method == "POST":
        password = request.form.get("password")
        if password == data.get("password"):
            # Password correct → show profile page
            return render_template_string(profile_html(data))
        else:
            return render_template_string(login_html(data, error="❌ Wrong password!"))

    # GET request → show password form
    return render_template_string(login_html(data))

def login_html(data, error=""):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Login - {data['name']}'s Profile</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: #f8f9fa;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: 'Segoe UI', sans-serif;
            }}
            .card {{
                width: 100%;
                max-width: 400px;
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
                text-align: center;
                background-color: #fff;
            }}
            .avatar {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                margin-bottom: 1rem;
                border: 4px solid #007bff;
            }}
            input {{
                margin-top: 1rem;
            }}
            .error {{
                color: red;
                margin-top: 0.5rem;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            {"<img src='"+data.get('avatar', '')+"' class='avatar'>" if data.get('avatar') else ""}
            <h2>{data['name']}'s Profile</h2>
            <form method="POST">
                <input type="password" name="password" placeholder="Enter your password" class="form-control" required>
                <button type="submit" class="btn btn-primary mt-3 w-100">Login</button>
            </form>
            {"<p class='error'>"+error+"</p>" if error else ""}
        </div>
    </body>
    </html>
    """

def profile_html(data):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{data['name']}'s Profile</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background-color: #ffffff;
                color: #000000;
                font-family: 'Segoe UI', sans-serif;
            }}
            .card {{
                max-width: 600px;
                margin: 3rem auto;
                border-radius: 1rem;
                padding: 2rem;
                box-shadow: 0 8px 30px rgba(0,0,0,0.1);
                text-align: center;
                background-color: #f8f9fa;
            }}
            .avatar {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                margin-bottom: 1rem;
                border: 5px solid #007bff;
            }}
            .banner {{
                width: 100%;
                border-radius: 1rem;
                max-height: 250px;
                object-fit: cover;
                margin-bottom: 1rem;
                transition: transform 0.5s ease;
            }}
            .banner:hover {{
                transform: scale(1.05);
            }}
            h1 {{
                margin-bottom: 0.5rem;
            }}
            p {{
                font-size: 1.2rem;
                margin: 5px 0;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            {"<img src='"+data.get('banner', '')+"' class='banner'>" if data.get('banner') else ""}
            {"<img src='"+data.get('avatar', '')+"' class='avatar'>" if data.get('avatar') else ""}
            <h1>{data['name']}</h1>
            <p>🆔 Cousin ID: <strong>{data['cousin_id']}</strong></p>
            <p>🏅 Rank: <strong>#{data['rank']}</strong></p>
            <p>👀 Reputation: <strong>{data['rep']}/100</strong></p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
