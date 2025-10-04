import os
import requests
from flask import Flask, request, abort, render_template_string

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/cousinunited/refs/heads/main/cousins.json"

@app.route("/cousin/<user_id>", methods=["GET", "POST"])
def cousin_profile(user_id):
    # Fetch live JSON
    try:
        resp = requests.get(JSON_URL, timeout=5)
        resp.raise_for_status()
        cousins = resp.json()
    except Exception as e:
        return f"❌ Could not load data: {e}", 500

    data = cousins.get(user_id)
    if not data:
        return abort(404)

    # Defaults
    password_stored = data.get("password", "")
    avatar = data.get("avatar", "")
    banner = data.get("banner", "")
    name = data.get("name", "Unknown")
    cousin_id = data.get("cousin_id", "N/A")
    rank = data.get("rank", "N/A")
    rep = data.get("rep", "N/A")

    # POST: password submitted
    if request.method == "POST":
        password_input = request.form.get("password", "")
        if password_input != password_stored:
            return render_template_string("""
                <h1 style="color:white;text-align:center; text-shadow:0 0 20px white;">❌ Wrong password!</h1>
                <a href="" style="color:white; display:block; text-align:center; margin-top:10px;">Try again</a>
            """)

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{name}'s Profile</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    background:black;
                    color:white;
                    font-family: 'Segoe UI', sans-serif;
                    text-align:center;
                    margin:0;
                    padding:0;
                }}
                .loading {{
                    display:none;
                }}
                .card {{
                    background:#111;
                    color:white;
                    border-radius:1rem;
                    box-shadow:0 0 30px white;
                    padding:30px;
                    max-width:800px;
                    width:90%;
                    margin:50px auto;
                    transition: transform 0.3s, box-shadow 0.3s;
                }}
                .card:hover {{
                    transform: translateY(-10px);
                    box-shadow:0 0 50px white;
                }}
                .avatar {{
                    width:160px;
                    height:160px;
                    border-radius:50%;
                    margin-top:-80px;
                    border:5px solid white;
                    box-shadow:0 0 30px white;
                }}
                .banner {{
                    width:100%;
                    max-height:250px;
                    object-fit:cover;
                    border-top-left-radius:1rem;
                    border-top-right-radius:1rem;
                    transition: transform 0.5s ease;
                }}
                .banner:hover {{
                    transform: scale(1.05);
                }}
                h1 {{
                    margin-top:20px;
                    font-size:3rem;
                    text-shadow:0 0 20px white;
                }}
                p {{
                    font-size:1.5rem;
                    text-shadow:0 0 10px white;
                    margin:8px 0;
                }}
                @media (max-width: 600px) {{
                    h1 {{ font-size:2.2rem; }}
                    p {{ font-size:1.2rem; }}
                    .avatar {{ width:120px; height:120px; margin-top:-60px; }}
                }}
            </style>
        </head>
        <body>
            <div class="loading" id="loading">
                <h1>Loading Cousin Network...</h1>
            </div>
            <div class="card" id="profile" style="display:none;">
                {f"<img src='{banner}' class='banner'>" if banner else ""}
                {f"<img src='{avatar}' class='avatar'>" if avatar else ""}
                <h1>{name}</h1>
                <p>🆔 Cousin ID: <strong>{cousin_id}</strong></p>
                <p>🏅 Rank: <strong>#{rank}</strong></p>
                <p>👀 Reputation: <strong>{rep}/100</strong></p>
            </div>
            <script>
                // Show loading for 5s
                document.getElementById('loading').style.display = 'block';
                setTimeout(() => {{
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('profile').style.display = 'block';
                }}, 5000);
            </script>
        </body>
        </html>
        """
        return html

    # GET: password form
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Login</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    background:black;
                    color:white;
                    font-family: 'Segoe UI', sans-serif;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    height:100vh;
                    flex-direction:column;
                    text-align:center;
                    text-shadow:0 0 20px white;
                }}
                input, button {{
                    padding:12px;
                    margin:6px;
                    border-radius:5px;
                    border:none;
                    font-size:1.2rem;
                }}
                input {{ width:220px; }}
                button {{
                    background:white;
                    color:black;
                    font-weight:bold;
                    cursor:pointer;
                    transition:0.3s;
                }}
                button:hover {{
                    background:#00ffea;
                    color:black;
                }}
            </style>
        </head>
        <body>
            <h1>Enter your password</h1>
            <form method="post">
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Enter</button>
            </form>
        </body>
        </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
