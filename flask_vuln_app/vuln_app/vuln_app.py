from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)

# ── Public pages ───────────────────────────────────────

@app.route('/')
def home():
    return render_template('home.html', active_page='home')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

# ── robots.txt (don't publish hidden path) ─────────────────

@app.route('/robots.txt')
def robots():
    content = "User-agent: *\nDisallow: /api/\nDisallow: /api/v1/internal/healthcheck\n"
    return content, 200, {'Content-Type': 'text/plain'}

# ── Hidden vulnerable endpoint ─────────────────────────

@app.route('/api/v1/internal/healthcheck')
def healthcheck():
    cmd = request.args.get('cmd')
    if not cmd:
        return {'status': 'ok', 'message': 'Provide a diagnostic command via ?cmd='}, 200
    try:
        # VULNERABILITY: User input is passed directly to the shell
        raw = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=30)
        output = raw.decode(errors='replace')
    except subprocess.TimeoutExpired:
        output = 'Command timed out.'
    except Exception as e:
        output = f'Error: {e}'

    return {'status': 'ok', 'output': output}, 200

if __name__ == '__main__':
    # certificate paths
    home_dir = os.path.expanduser('../')
    cert_path = os.path.join(home_dir, 'certs', 'fullchain.pem')
    key_path = os.path.join(home_dir, 'certs', 'privkey.pem')
    
    if not os.path.exists(cert_path) or not os.path.exists(key_path):
        print(f"[-] Error: Certificates not found in {home_dir}/certs/, starting server without HTTPS.")
        app.run(host='0.0.0.0', port=4443)        
    else:
           
        print(f"[+] Starting secure server on https://0.0.0.0:4443")
        print(f"[+] Using certificate: {cert_path}")
        
        # Run the application on an unprivileged port with HTTPS enabled
        app.run(host='0.0.0.0', port=4443, ssl_context=(cert_path, key_path))
