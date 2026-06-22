/**
 * McswazSting AI Manager - Frontend Logic Layer
 * Integrated with Flask Backend API
 */

class AIManagerInterface {
    constructor(backendUrl = 'http://localhost:5000') {
        this.connectionStatus = 'Offline';
        this.backendUrl = backendUrl;
        this.apiEndpoints = {
            status: '/api/status',
            process: '/api/process',
            health: '/api/health',
            logs: '/api/logs'
        };
    }

    /**
     * Initialize dashboard and establish connection to backend
     */
    async initializeDashboard() {
        this.connectionStatus = 'Connecting';
        console.log(`[UI] Dashboard initializing. Attempting connection to ${this.backendUrl}...`);
        
        try {
            const health = await this.checkHealth();
            if (health) {
                this.connectionStatus = 'Active';
                console.log(`[UI] Dashboard initialized. Status: ${this.connectionStatus}`);
                this.logEvent(`Dashboard connected to backend at ${this.backendUrl}`);
            }
        } catch (error) {
            this.connectionStatus = 'Connection Failed';
            console.error(`[UI] Failed to connect to backend: ${error.message}`);
            this.logEvent(`Connection error: ${error.message}`, 'error');
        }
    }

    /**
     * Check backend health status
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.backendUrl}${this.apiEndpoints.health}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            return response.ok;
        } catch (error) {
            console.error(`[API] Health check failed: ${error.message}`);
            return false;
        }
    }

    /**
     * Retrieve system status from backend
     */
    async getSystemStatus() {
        try {
            const response = await fetch(`${this.backendUrl}${this.apiEndpoints.status}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log(`[API] System Status Retrieved:`, data);
            this.logEvent(`Status retrieved: ${data.status}`);
            return data;
        } catch (error) {
            console.error(`[API] Status retrieval failed: ${error.message}`);
            this.logEvent(`Status error: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * Send data payload to backend for processing
     */
    async sendDataToBackend(payload) {
        try {
            console.log(`[API] Transmitting data payload to Python core:`, payload);
            
            const response = await fetch(`${this.backendUrl}${this.apiEndpoints.process}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task: payload })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const result = await response.json();
            console.log(`[API] Processing result:`, result);
            this.logEvent(`Task processed: ${payload}`);
            return result;
        } catch (error) {
            console.error(`[API] Data transmission failed: ${error.message}`);
            this.logEvent(`Processing error: ${error.message}`, 'error');
            throw error;
        }
    }

    /**
     * Retrieve API logs from backend
     */
    async retrieveLogs() {
        try {
            const response = await fetch(`${this.backendUrl}${this.apiEndpoints.logs}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log(`[API] Logs retrieved:`, data.logs.length, 'entries');
            return data.logs;
        } catch (error) {
            console.error(`[API] Log retrieval failed: ${error.message}`);
            return [];
        }
    }

    /**
     * Internal logging method
     */
    logEvent(message, level = 'info') {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`);
    }

    /**
     * Get current connection status
     */
    getConnectionStatus() {
        return {
            status: this.connectionStatus,
            backend: this.backendUrl,
            timestamp: new Date().toISOString()
        };
    }
}

// Instantiate interface on load
const appInterface = new AIManagerInterface();
appInterface.initializeDashboard();

// Export for external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIManagerInterface;
}
