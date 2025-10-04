import os
import requests
from flask import Flask, request, abort, render_template_string

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/cousinunited/refs/heads/main/cousins.json"

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

    # POST = password submitted
    if request.method == "POST":
        password = request.form.get("password")
        if password == data.get("password"):
            # Show 5-second loading screen with spinner
            return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Loading Cousin Network...</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    background:black;
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    height:100vh;
    font-family:'Segoe UI', sans-serif;
    text-align:center;
}
h1 {
    font-size:2rem;
    margin-bottom:40px;
    text-shadow: 0 0 15px white, 0 0 30px white;
}
/* Spinner */
.spinner {
    border: 8px solid #f3f3f3; /* Light grey */
    border-top: 8px solid #ffffff; /* White */
    border-radius: 50%;
    width: 80px;
    height: 80px;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
<script>
// Redirect to profile after 5 seconds
setTimeout(function() {
    window.location.href = window.location.href + "?show_profile=1";
}, 5000);
</script>
</head>
<body>
<h1>Loading Cousin Network...</h1>
<div class="spinner"></div>
</body>
</html>
""")

    # GET request = show password form OR direct to profile if show_profile=1
    if request.args.get("show_profile") == "1":
        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ data.name }}'s Profile</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body { background:black; color:white; font-family:'Segoe UI', sans-serif; text-align:center; margin:0; padding:0; }
.container { max-width: 800px; margin:50px auto; }
.card { background:#1a1a1a; border-radius:1rem; box-shadow:0 4px 20px rgba(255,255,255,0.2); padding:30px; transition:0.3s; }
.card:hover { transform: translateY(-8px); box-shadow:0 10px 40px rgba(255,255,255,0.4); }
.avatar { width:150px; height:150px; border-radius:50%; border:5px solid white; margin-top:-75px; }
.banner { width:100%; border-radius:1rem 1rem 0 0; max-height:250px; object-fit:cover; transition: transform 0.5s ease; }
.banner:hover { transform: scale(1.05); }
h1 { margin-top:20px; font-size:2.5rem; text-shadow:0 0 15px white; }
p { font-size:1.2rem; margin:5px 0; text-shadow:0 0 10px white; }
</style>
</head>
<body>
<div class="container">
    <div class="card">
        {% if data.banner %}
        <img src="{{ data.banner }}" class="banner">
        {% endif %}
        {% if data.avatar %}
        <img src="{{ data.avatar }}" class="avatar">
        {% endif %}
        <h1>{{ data.name }}</h1>
        <p>🆔 Cousin ID: <strong>{{ data.cousin_id }}</strong></p>
        <p>🏅 Rank: <strong>#{{ data.rank }}</strong></p>
        <p>👀 Reputation: <strong>{{ data.rep }}/100</strong></p>
    </div>
</div>
</body>
</html>
""", data=data)

    # Show password form
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Login</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body { background:black; color:white; font-family:'Segoe UI', sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; text-align:center; text-shadow:0 0 15px white; }
input, button { padding:12px; margin:6px; border-radius:5px; border:none; font-size:1.2rem; }
input { width:220px; }
button { background:white; color:black; font-weight:bold; cursor:pointer; transition:0.3s; }
button:hover { background:#00ffea; color:black; }
h1 { margin-bottom:20px; }
</style>
</head>
<body>
<form method="post">
    <h1>Enter your password to view profile</h1>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Enter</button>
</form>
</body>
</html>
""")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
