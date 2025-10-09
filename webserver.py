import os
import requests
from flask import Flask, request, abort, render_template_string, redirect, url_for

app = Flask(__name__)
JSON_URL = "https://raw.githubusercontent.com/professerXisonCRACK/cousinunited/refs/heads/main/cousins.json"

# --- Templates ---
LOADING_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Loading Cousin Network...</title>
<style>
:root{
  --bg:#000;
  --neon:#00fff7;
  --accent:#61f3ff;
  --muted:rgba(255,255,255,0.08);
  --glass: rgba(255,255,255,0.03);
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  background:var(--bg);
  color:#fff;
  font-family:Inter, "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  overflow:hidden;
}
.container{
  width:100%;
  max-width:520px;
  padding:28px;
}
.title{
  font-size:1.6rem;
  letter-spacing:0.06em;
  margin-bottom:22px;
  text-shadow: 0 0 22px rgba(0,255,255,0.08);
}
.ring{
  width:110px;
  height:110px;
  margin:0 auto 22px;
  border-radius:50%;
  position:relative;
  box-shadow: 0 0 40px rgba(0,255,247,0.12);
  display:flex;
  align-items:center;
  justify-content:center;
}
.ring::before{
  content:"";
  position:absolute;
  inset:6px;
  border-radius:50%;
  border:6px solid rgba(255,255,255,0.03);
}
.spinner {
  width:72px;
  height:72px;
  border-radius:50%;
  border:6px solid rgba(255,255,255,0.06);
  border-top-color:var(--neon);
  animation:spin 1s linear infinite;
  box-shadow: 0 0 20px var(--neon);
}
@keyframes spin{to{transform:rotate(360deg)}}

/* small floating particles like in design */
.particles{position:fixed; inset:0; pointer-events:none; z-index:0}
.particle{
  width:8px;height:8px;border-radius:50%; background:var(--muted);
  position:absolute; opacity:.9; animation: drift 8s linear infinite;
}
@keyframes drift{
  0%{transform:translateY(0) translateX(0) scale(1); opacity:.9}
  50%{transform:translateY(-40px) translateX(20px) scale(.8); opacity:.5}
  100%{transform:translateY(0) translateX(0) scale(1); opacity:.9}
}

/* small helper */
.hint{margin-top:12px;font-size:.95rem;color:rgba(255,255,255,0.7)}
</style>
</head>
<body>
<div class="particles" aria-hidden="true">
  <div class="particle" style="left:10%; top:18%; animation-duration:10s;"></div>
  <div class="particle" style="left:80%; top:10%; animation-duration:12s;"></div>
  <div class="particle" style="left:35%; top:75%; animation-duration:9s;"></div>
  <div class="particle" style="left:92%; top:62%; animation-duration:11s;"></div>
  <div class="particle" style="left:6%; top:82%; animation-duration:14s;"></div>
</div>

<div class="container">
  <div class="title">Loading Cousin Network...</div>
  <div class="ring">
    <div class="spinner" role="status" aria-label="loading"></div>
  </div>
  <div class="hint">Syncing profile data — this takes a sec</div>
</div>

<script>
// After 3 seconds redirect to same path with verified=1
setTimeout(function(){
    var redirectUrl = window.location.pathname + "?verified=1";
    window.location.href = redirectUrl;
}, 3000);
</script>
</body>
</html>
"""

LOGIN_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Enter password</title>
<style>
:root{
  --bg:#000;
  --neon:#00fff7;
  --glass: rgba(255,255,255,0.03);
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  background: linear-gradient(180deg,#000 0%, #050505 60%);
  color:#fff;
  font-family:Inter, "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
  display:flex;
  align-items:center;
  justify-content:center;
}
.card{
  width:100%;
  max-width:420px;
  background:var(--glass);
  border-radius:14px;
  padding:28px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.7), 0 0 20px rgba(0,255,247,0.03);
  text-align:center;
}
h1{margin:0 0 12px; font-size:1.4rem; text-shadow:0 0 10px rgba(0,255,247,0.04)}
form{display:flex; flex-direction:column; align-items:center}
input[type="password"]{
  width:100%;
  padding:12px 14px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,0.06);
  background:rgba(255,255,255,0.02);
  color:#fff;
  margin-bottom:12px;
  font-size:1rem;
  outline:none;
}
button{
  padding:11px 18px;
  border-radius:10px;
  border:none;
  background:linear-gradient(90deg,var(--neon), #61f3ff);
  color:#000;
  font-weight:700;
  cursor:pointer;
  width:100%;
}
small{display:block; margin-top:10px; color:rgba(255,255,255,0.6)}
</style>
</head>
<body>
<div class="card">
  <h1>Enter your password to view profile</h1>
  <form method="post">
    <input type="password" name="password" placeholder="Password" required autocomplete="current-password" />
    <button type="submit">Enter</button>
  </form>
  <small>Protected profile</small>
</div>
</body>
</html>
"""

PROFILE_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{{ data.name }} — Cousin</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#000;
  --card:#0f0f10;
  --neon:#00fff7;
  --accent:#61f3ff;
  --muted:rgba(255,255,255,0.08);
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0;
  background: radial-gradient(1200px 600px at 20% 10%, rgba(0,255,247,0.04), transparent 6%),
              radial-gradient(1000px 500px at 85% 90%, rgba(97,243,255,0.03), transparent 6%),
              var(--bg);
  color:#fff;
  font-family:Inter, "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  padding:36px;
  display:flex;
  align-items:flex-start;
  justify-content:center;
}

/* container card */
.wrapper{
  width:100%;
  max-width:900px;
  position:relative;
}

/* card */
.card{
  background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border-radius:18px;
  padding:28px;
  box-shadow: 0 10px 50px rgba(0,0,0,0.7);
  overflow:hidden;
  position:relative;
}

/* banner area */
.banner{
  width:100%;
  height:240px;
  border-radius:12px;
  object-fit:cover;
  display:block;
  filter:brightness(.55);
  background: linear-gradient(90deg, rgba(0,0,0,0.5), rgba(0,0,0,0.2));
}

/* avatar */
.avatar-wrap{
  position:absolute;
  left:40px;
  top:170px;
  transform:translateY(-50%);
  display:flex;
  align-items:center;
  gap:18px;
}
.avatar{
  width:140px;
  height:140px;
  border-radius:50%;
  border:6px solid rgba(255,255,255,0.06);
  box-shadow: 0 6px 30px rgba(0,255,247,0.06), 0 0 30px rgba(0,255,247,0.06);
  object-fit:cover;
  background:linear-gradient(180deg,#111,#0a0a0a);
}

/* neon username */
.title-wrap{
  margin-left:210px;
  padding-top:6px;
}
.username{
  font-size:2.2rem;
  font-weight:700;
  letter-spacing:0.03em;
  color:#fff;
  text-shadow: 0 0 18px rgba(0,255,247,0.18), 0 2px 8px rgba(0,0,0,0.6);
  display:flex;
  align-items:center;
  gap:12px;
}
.verified-badge{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  background:linear-gradient(90deg,var(--neon),var(--accent));
  color:#001;
  font-weight:700;
  padding:6px 8px;
  border-radius:8px;
  font-size:0.85rem;
  box-shadow:0 6px 24px rgba(0,255,247,0.06);
}

/* subtitle text */
.subtitle{
  margin-top:6px;
  font-size:0.95rem;
  color:rgba(255,255,255,0.85);
  text-shadow: 0 0 10px rgba(255,255,255,0.03);
}

/* info row */
.info-row{
  display:flex;
  gap:18px;
  margin-top:18px;
  margin-left:210px;
  align-items:center;
}
.info-pill{
  background: rgba(255,255,255,0.03);
  padding:8px 12px;
  border-radius:12px;
  font-weight:600;
  font-size:0.95rem;
  box-shadow: 0 6px 20px rgba(0,0,0,0.6);
}

/* little status card lower */
.status-card{
  margin-top:30px;
  display:flex;
  align-items:center;
  gap:12px;
  background:linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.02));
  padding:12px;
  border-radius:12px;
  width:380px;
  box-shadow: 0 6px 30px rgba(0,0,0,0.6);
}
.status-avatar{
  width:52px;height:52px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,0.04)
}
.status-text{font-weight:600;font-size:0.95rem}
.status-sub{font-size:0.85rem;color:rgba(255,255,255,0.6);margin-top:4px}

/* decorative small dots */
.dot{
  position:absolute;
  width:8px;height:8px;border-radius:50%; background:rgba(255,255,255,0.08);
}
.dot.a{right:48px; top:46px}
.dot.b{right:22px; top:120px}
.dot.c{left:18px; top:40px}

/* responsive */
@media (max-width:720px){
  .avatar-wrap{left:50%; transform:translate(-50%,-50%); top:140px}
  .title-wrap{margin-left:0; margin-top:90px; text-align:center}
  .info-row{margin-left:0; justify-content:center; flex-wrap:wrap}
  .status-card{margin:18px auto 0}
}
</style>
</head>
<body>
<div class="wrapper">
  <div class="card">
    {% if data.banner %}
      <img src="{{ data.banner }}" alt="banner" class="banner">
    {% else %}
      <div class="banner" style="background:linear-gradient(90deg,#001219,#001b22)"></div>
    {% endif %}

    <!-- floating decorative dots -->
    <div class="dot a"></div>
    <div class="dot b"></div>
    <div class="dot c"></div>

    <!-- avatar & top info -->
    <div class="avatar-wrap" aria-hidden="false">
      {% if data.avatar %}
        <img src="{{ data.avatar }}" alt="avatar" class="avatar">
      {% else %}
        <div class="avatar"></div>
      {% endif %}
      <div class="title-wrap">
        <div class="username">
          {{ data.name }}
          {% if data.verified %}
            <span class="verified-badge">VERIFIED</span>
          {% endif %}
        </div>
        <div class="subtitle">hello my name is {{ data.display_name or data.name }}!!!</div>

        <div class="info-row" role="list">
          <div class="info-pill">🆔 Cousin ID: <strong style="margin-left:6px">{{ data.cousin_id }}</strong></div>
          <div class="info-pill">🏅 Rank: <strong style="margin-left:6px">#{{ data.rank }}</strong></div>
          <div class="info-pill">👀 Rep: <strong style="margin-left:6px">{{ data.rep }}/100</strong></div>
        </div>
      </div>
    </div>

    <!-- small status area -->
    <div style="margin-top:220px; display:flex; justify-content:center;">
      <div class="status-card">
        {% if data.small_avatar %}
          <img src="{{ data.small_avatar }}" alt="" class="status-avatar">
        {% elif data.avatar %}
          <img src="{{ data.avatar }}" alt="" class="status-avatar">
        {% else %}
          <div class="status-avatar" style="background:#111"></div>
        {% endif %}
        <div>
          <div class="status-text">{{ data.status_name or data.name }} <span style="opacity:.8">•</span></div>
          <div class="status-sub">{{ data.status_text or 'currently doing nothing' }}</div>
        </div>
      </div>
    </div>

  </div>
</div>
</body>
</html>
"""

# --- End templates ---


@app.route("/cousin/<user_id>", methods=["GET", "POST"])
def cousin_profile(user_id):
    # Fetch latest JSON from GitHub for live updates
    try:
        resp = requests.get(JSON_URL, timeout=6)
        resp.raise_for_status()
        cousins = resp.json()
    except Exception as e:
        return f"❌ Could not load data: {e}", 500

    data = cousins.get(user_id)
    if not data:
        return abort(404)

    verified = request.args.get("verified") == "1"

    if request.method == "POST":
        password = request.form.get("password", "")
        if password == data.get("password"):
            # Correct password → show loading page first, then redirect with verified=1
            return render_template_string(LOADING_HTML)
        else:
            return render_template_string("""
                <!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"/></head>
                <body style="background:black;color:white;font-family:Inter,Arial;text-align:center;padding:40px;">
                <h1>❌ Wrong password!</h1>
                <p><a href="" style="color:#61f3ff;text-decoration:none;font-weight:700">Try again</a></p>
                </body></html>
            """)

    # GET request with verified=1 → show profile
    if verified:
        # allow template to show a verified badge if the profile data has a 'verified' boolean
        # also populate small_avatar/status fields gracefully
        # render profile
        return render_template_string(PROFILE_HTML, data=data)

    # GET request → show password form
    return render_template_string(LOGIN_HTML)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
