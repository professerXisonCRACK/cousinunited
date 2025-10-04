import os
import requests
from flask import Flask, request, abort

app = Flask(__name__)

# Replace this with your GitHub JSON raw URL
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

    # Login form for token/password
    if request.method == "POST":
        token = request.form.get("token")
        if token != data.get("token"):
            return """
            <html>
            <body style='text-align:center; font-family:sans-serif; margin-top:100px;'>
                <h2>❌ Incorrect token!</h2>
                <a href="">Try again</a>
            </body>
            </html>
            """, 403
    else:
        # Show login form
        return f"""
        <html>
        <body style='text-align:center; font-family:sans-serif; margin-top:100px;'>
            <h2>Enter your profile token/password</h2>
            <form method='POST'>
                <input type='password' name='token' placeholder='Token' style='padding:10px; font-size:16px;'/>
                <button type='submit' style='padding:10px 20px; font-size:16px;'>View Profile</button>
            </form>
        </body>
        </html>
        """

    # Profile HTML
    html = f"""
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
                background-color: #f5f5f5;
                border-radius: 1rem;
                padding-top: 70px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                max-width: 600px;
                margin: auto;
            }}
            .avatar {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                border:5px solid #fff;
                object-fit: cover;
                position: relative;
                top: -60px;
                margin-bottom: -60px;
            }}
            .banner {{
                width: 100%;
                max-height: 300px;
                object-fit: cover;
                border-top-left-radius: 1rem;
                border-top-right-radius: 1rem;
                margin-bottom: 20px;
            }}
            h1 {{
                font-size: 2rem;
                margin-bottom: 1rem;
            }}
            p {{
                font-size: 1.2rem;
            }}
        </style>
    </head>
    <body>
        <div class="container my-5">
            <div class="card text-center">
                {"<img src='"+data['banner']+"' class='banner'>" if data.get('banner') else ""}
                {"<img src='"+data.get('avatar', '')+"' class='avatar'>" if data.get('avatar') else ""}
                <div class="card-body">
                    <h1>{data['name']}</h1>
                    <p>🆔 <strong>{data['cousin_id']}</strong></p>
                    <p>🏅 Rank: <strong>#{data['rank']}</strong></p>
                    <p>👀 Reputation: <strong>{data['rep']}/100</strong></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
