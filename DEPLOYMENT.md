# McswazSting AI Manager - Deployment Guide

## Full-Stack Architecture

This project implements a secure, production-ready full-stack AI management system with Flask backend and JavaScript frontend, optimized for mobile Termux/NetHunter environments.

## Backend Setup (Python Flask)

### Installation

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Create logs directory
mkdir -p logs
```

### Running the Server

**Development Mode:**
```bash
cd backend
python server.py
```

**Production Mode with Gunicorn:**
```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 server:app
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|----------|
| `/api/status` | GET | Retrieve system status |
| `/api/health` | GET | Health check (load balancer compatible) |
| `/api/process` | POST | Process AI tasks |
| `/api/logs` | GET | Retrieve recent API logs |

### Example API Calls

**Get Status:**
```bash
curl http://localhost:5000/api/status
```

**Process Task:**
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"task": "Sample AI Processing Task"}'
```

## Frontend Setup (JavaScript)

### Configuration

Update the backend URL in `frontend/app.js`:

```javascript
const appInterface = new AIManagerInterface('http://localhost:5000');
```

### Integration

The frontend provides:
- Asynchronous API communication
- Connection status monitoring
- Error handling and logging
- Real-time data synchronization

### Usage Example

```javascript
// Initialize dashboard
await appInterface.initializeDashboard();

// Get system status
const status = await appInterface.getSystemStatus();

// Send task for processing
const result = await appInterface.sendDataToBackend('Your AI Task');

// Retrieve logs
const logs = await appInterface.retrieveLogs();
```

## Mobile Environment Setup

### Termux Installation

Run the automated setup script:

```bash
chmod +x scripts/setup_termux.sh
./scripts/setup_termux.sh
```

This script automatically:
- Updates package repositories
- Installs Python 3, Node.js, and build tools
- Configures storage permissions
- Installs Python dependencies
- Creates required directories

### Kali Linux NetHunter Setup

Run the network audit tool:

```bash
chmod +x scripts/nethunter_sync.py
python3 scripts/nethunter_sync.py --host localhost --port 5000
```

This tool:
- Tests API connectivity
- Probes all endpoints
- Verifies CORS configuration
- Performs network diagnostics
- Generates security audit reports

## Configuration Files

### `config.json`

Centralized configuration for:
- Application settings
- Backend/frontend parameters
- Logging configuration
- Security settings
- Deployment parameters

### `requirements.txt`

Python dependencies:
- Flask 2.3.3
- Flask-CORS 4.0.0
- Gunicorn 21.2.0

## Directory Structure

```
.
├── backend/
│   ├── app.py              # AI Core Logic
│   ├── server.py           # Flask API Server
│   └── requirements.txt    # Python Dependencies
├── frontend/
│   └── app.js              # JavaScript Dashboard
├── scripts/
│   ├── setup_termux.sh     # Termux Setup Script
│   └── nethunter_sync.py   # NetHunter Audit Tool
├── logs/                   # Generated Logs
├── config.json             # Configuration
├── README.md               # Project Documentation
└── DEPLOYMENT.md          # This file
```

## Troubleshooting

### Connection Issues

**Problem:** Frontend cannot connect to backend

**Solution:**
1. Verify backend is running: `python backend/server.py`
2. Check firewall: `netstat -an | grep 5000`
3. Confirm URL in frontend matches backend address
4. Check CORS is enabled in `config.json`

### Port Already in Use

**Problem:** "Address already in use" error

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
python backend/server.py --port 5001
```

### Permission Denied (Scripts)

```bash
chmod +x scripts/setup_termux.sh
chmod +x scripts/nethunter_sync.py
```

## Security Best Practices

1. **CORS Configuration:** Restrict origins in production
2. **API Keys:** Implement authentication for `/api/process`
3. **HTTPS:** Use SSL/TLS in production
4. **Logging:** Monitor logs/api_server.log for anomalies
5. **Firewall:** Restrict port 5000 to trusted networks

## Performance Optimization

1. Use Gunicorn with multiple workers
2. Enable caching headers
3. Monitor logs/api_server.log for bottlenecks
4. Scale horizontally with load balancer

## Support & Maintenance

- Review logs regularly: `tail -f logs/api_server.log`
- Run NetHunter audit: `python3 scripts/nethunter_sync.py`
- Update dependencies: `pip install --upgrade -r backend/requirements.txt`

---

**Version:** 1.0.0  
**Last Updated:** 2026-06-22
