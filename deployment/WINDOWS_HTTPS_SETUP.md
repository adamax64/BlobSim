# Windows HTTPS Setup Guide for BlobSim Backend

This guide walks through setting up HTTPS on Windows using Nginx + win-acme (Let's Encrypt) with environment variable configuration.

## Prerequisites

1. **Domain name** pointing to your Windows machine's IP
2. **Nginx for Windows** installed in `C:\nginx\` (or WSL/Docker)
3. **win-acme** for automated Let's Encrypt certificate management

## Step 1: Install Nginx on Windows

Download Nginx for Windows from https://nginx.org/en/download.html and extract to `C:\nginx\`.

Alternatively, use WSL (Windows Subsystem for Linux) and install Nginx there:

```powershell
wsl --install -d Ubuntu
# Inside WSL:
sudo apt update && sudo apt install nginx certbot certbot-nginx -y
```

## Step 2: Obtain Let's Encrypt Certificate with win-acme

### Option A: win-acme (Recommended on Windows)

1. Download win-acme from https://www.win-acme.com/
2. Extract and navigate to the folder
3. Run the CLI or interactive mode:

```powershell
# Interactive mode (easier)
.\wacs.exe

# Or CLI mode (example - adjust YOUR_DOMAIN):
.\wacs.exe `
  --target manual `
  --host YOUR_DOMAIN `
  --validation http `
  --validationmode http-01 `
  --webroot C:\nginx\html `
  --store pemfiles `
  --pemfilespath C:\certs `
  --certificatestore My `
  --run
```

This will:

- Validate domain ownership via HTTP-01 challenge
- Generate certificate files in `C:\certs\`
- Save `fullchain.pem` and `privkey.pem`

**Note:** win-acme can also auto-renew certificates on a schedule. Configure auto-renewal during setup or in the GUI.

### Option B: WSL + Certbot (if using WSL Nginx)

```bash
# Inside WSL:
sudo certbot certonly --standalone -d YOUR_DOMAIN -d www.YOUR_DOMAIN
# Certificates saved to: /etc/letsencrypt/live/YOUR_DOMAIN/

# Create PEM files (if needed):
sudo cat /etc/letsencrypt/live/YOUR_DOMAIN/fullchain.pem > ~/fullchain.pem
sudo cat /etc/letsencrypt/live/YOUR_DOMAIN/privkey.pem > ~/privkey.pem
```

## Step 3: Set Environment Variables

Before running the startup script, set these environment variables:

```powershell
# Required
$env:NGINX_DOMAIN = "api.example.com"
$env:NGINX_CERT_PATH = "C:/certs/fullchain.pem"
$env:NGINX_KEY_PATH = "C:/certs/privkey.pem"
$env:FRONTEND_ROOT = "d:/SoftwareDevelopement/BlobSim/web-ui/dist"

# Optional (defaults shown)
$env:BACKEND_HOST = "127.0.0.1"
$env:BACKEND_PORT = "8000"
$env:ORIGIN_URL = "https://api.example.com"
```

Or add to your deployment `.env` file or system environment.

**Note on FRONTEND_ROOT:** This should point to your built frontend directory:

- If using Vite (default for web-ui): run `npm run build` in web-ui folder first → creates `web-ui/dist`
- If using a different build tool: update path to your build output directory

## Step 4: Build Frontend (if not already built)

If your frontend hasn't been built yet, build it now:

```powershell
cd d:\SoftwareDevelopement\BlobSim\web-ui
npm install
npm run build
# Output goes to: web-ui/dist
```

This creates the static files that nginx will serve.

## Step 5: Generate nginx.conf from Environment Variables

The `generate_nginx_config.ps1` script reads environment variables and generates the final `nginx.conf`:

```powershell
cd d:\SoftwareDevelopement\BlobSim\deployment
.\generate_nginx_config.ps1
```

This will create `C:\nginx\conf\nginx.conf` with your configured domain, certificate paths, and backend settings.

## Step 5: Generate nginx.conf from Environment Variables

The `generate_nginx_config.ps1` script reads environment variables and generates the final `nginx.conf`:

```powershell
cd d:\SoftwareDevelopement\BlobSim\deployment
.\generate_nginx_config.ps1
```

This will create `C:\nginx\conf\nginx.conf` with your configured domain, certificate paths, frontend root, and backend settings.

## Step 6: Start Services

Run the startup script which will:

1. Verify environment variables
2. Generate nginx.conf from the template
3. Start uvicorn backend
4. Start Nginx (serving frontend + proxying API)

```powershell
cd d:\SoftwareDevelopement\BlobSim\deployment
.\start_https_windows.bat
```

Or manually run it with custom environment variables:

```powershell
$env:NGINX_DOMAIN = "api.example.com"
$env:NGINX_CERT_PATH = "C:/certs/fullchain.pem"
$env:NGINX_KEY_PATH = "C:/certs/privkey.pem"
$env:FRONTEND_ROOT = "d:/SoftwareDevelopement/BlobSim/web-ui/dist"
cd d:\SoftwareDevelopement\BlobSim\deployment
.\start_https_windows.bat
```

## Step 7: Verify HTTPS

1. Navigate to `https://YOUR_DOMAIN` in your browser
2. Check that the certificate is valid (green padlock)
3. Verify frontend loads and API responses work
4. Check API docs at `https://YOUR_DOMAIN/docs` (FastAPI Swagger UI)

Test redirect:

```powershell
curl -I http://YOUR_DOMAIN
# Should return: 301 Moved Permanent to https://YOUR_DOMAIN
```

Verify API is accessible (assuming you have GET /api/health or similar):

```powershell
curl https://YOUR_DOMAIN/api/health
```

## Step 8: Auto-Renewal

### win-acme Auto-Renewal

win-acme can create a Windows Task Scheduler job to auto-renew. During setup, choose "Install as Windows service" or "Create a scheduled task".

After certificates are renewed, reload Nginx:

```powershell
cd C:\nginx
.\nginx.exe -s reload
```

### WSL + Certbot Auto-Renewal

```bash
# Inside WSL, certbot auto-renewal is enabled by default via systemd timer
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Environment Variable Configuration Examples

### Single domain (Frontend + API):

```powershell
$env:NGINX_DOMAIN = "myapp.com"
$env:NGINX_CERT_PATH = "C:/certs/fullchain.pem"
$env:NGINX_KEY_PATH = "C:/certs/privkey.pem"
$env:FRONTEND_ROOT = "d:/SoftwareDevelopement/BlobSim/web-ui/dist"
$env:BACKEND_PORT = "8000"
```

### Multiple domains with custom backend:

```powershell
$env:NGINX_DOMAIN = "myapp.com staging.myapp.com"
$env:NGINX_CERT_PATH = "C:/certs/wildcard/fullchain.pem"
$env:NGINX_KEY_PATH = "C:/certs/wildcard/privkey.pem"
$env:FRONTEND_ROOT = "d:/Projects/blobsim/web-ui/dist"
$env:BACKEND_HOST = "192.168.1.100"
$env:BACKEND_PORT = "9000"
```

### With custom CORS origin:

```powershell
$env:NGINX_DOMAIN = "api.example.com"
$env:NGINX_CERT_PATH = "C:/certs/fullchain.pem"
$env:NGINX_KEY_PATH = "C:/certs/privkey.pem"
$env:FRONTEND_ROOT = "d:/SoftwareDevelopement/BlobSim/web-ui/dist"
$env:ORIGIN_URL = "https://api.example.com"
```

## Troubleshooting

- **nginx.conf generation fails:** Ensure all required env vars are set (`NGINX_DOMAIN`, `NGINX_CERT_PATH`, `NGINX_KEY_PATH`, `FRONTEND_ROOT`)
- **Nginx won't start:** Run `C:\nginx\nginx.exe -t` to check config syntax
- **Frontend doesn't load:** Check that `FRONTEND_ROOT` points to a valid directory with `index.html`
- **API calls fail:** Verify `BACKEND_HOST` and `BACKEND_PORT` are correct and backend is running
- **Certificate validation fails:** Ensure port 80 is open and your domain DNS resolves correctly
- **Mixed content warnings:** Ensure all API calls use `https://` and update CORS origin to HTTPS URL
- **HSTS warnings:** These are normal; they improve security. Your browser will cache HTTPS-only policy

## File Structure

```
deployment/
  nginx.conf.template         - Template with ${VAR} placeholders (domain, certs, frontend, backend)
  generate_nginx_config.ps1   - PowerShell script to generate nginx.conf
  start_https_windows.bat     - Batch script to start services
  WINDOWS_HTTPS_SETUP.md      - This file
```

## Architecture

```
Internet (HTTPS)
    ↓
Nginx (port 443, TLS termination)
    ├─→ Static Files (Frontend SPA) → web-ui/dist/index.html
    ├─→ /api/* → Backend (uvicorn, localhost:8000)
    └─→ /docs, /redoc → Backend API Docs
```

## Next Steps

1. Run SSL Labs test (https://www.ssllabs.com/ssltest/) on your domain for security audit
2. Monitor certificate expiration (set calendar reminder ~30 days before)
3. For production, consider:
   - Running Nginx as a Windows Service (use NSSM: https://nssm.cc/)
   - Running in Docker on Windows (Docker Desktop with NGINX + Caddy for easier TLS)
   - Using Azure or AWS load balancers for managed TLS termination
   - Setting up automated certificate renewal with win-acme Task Scheduler

---

For more details on deployment architecture, see the main README.md.
