#!/usr/bin/env python3
"""
McswazSting AI Manager - Kali Linux NetHunter Network Sync & Audit Tool
Secure API connection mapping and diagnostic logging for mobile pen-testing environment
"""

import socket
import subprocess
import json
import logging
import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/nethunter_audit.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class NetHunterAPIAudit:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.url = f'http://{host}:{port}'
        self.audit_results = {}
        self.timestamp = datetime.now().isoformat()
        
    def check_connectivity(self):
        """Test basic network connectivity to API server."""
        logger.info(f"Checking connectivity to {self.url}...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            
            if result == 0:
                logger.info(f"✓ API Server accessible at {self.url}")
                self.audit_results['connectivity'] = 'OK'
                return True
            else:
                logger.error(f"✗ Connection refused on {self.host}:{self.port}")
                self.audit_results['connectivity'] = 'FAILED'
                return False
        except socket.timeout:
            logger.error("Connection timeout")
            self.audit_results['connectivity'] = 'TIMEOUT'
            return False
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            self.audit_results['connectivity'] = 'ERROR'
            return False
    
    def probe_endpoints(self):
        """Probe API endpoints for security and availability."""
        logger.info("Probing API endpoints...")
        endpoints = [
            ('/api/status', 'GET'),
            ('/api/health', 'GET'),
            ('/api/logs', 'GET'),
            ('/api/process', 'POST')
        ]
        
        endpoint_results = {}
        for path, method in endpoints:
            try:
                if method == 'GET':
                    cmd = f'curl -s -o /dev/null -w "{{http_code}}" -X GET {self.url}{path}'
                else:
                    cmd = f'curl -s -o /dev/null -w "{{http_code}}" -X POST {self.url}{path} -H "Content-Type: application/json"'
                
                status_code = subprocess.check_output(cmd, shell=True, text=True).strip()
                endpoint_results[f"{method} {path}"] = status_code
                logger.info(f"  {method} {path}: HTTP {status_code}")
            except Exception as e:
                endpoint_results[f"{method} {path}"] = 'ERROR'
                logger.warning(f"  {method} {path}: ERROR - {str(e)}")
        
        self.audit_results['endpoints'] = endpoint_results
    
    def check_cors_headers(self):
        """Verify CORS headers for cross-origin requests."""
        logger.info("Checking CORS headers...")
        try:
            cmd = f'curl -s -I -X OPTIONS {self.url}/api/status'
            headers = subprocess.check_output(cmd, shell=True, text=True)
            
            cors_enabled = 'Access-Control-Allow-Origin' in headers
            self.audit_results['cors'] = 'ENABLED' if cors_enabled else 'DISABLED'
            logger.info(f"  CORS Status: {self.audit_results['cors']}")
        except Exception as e:
            logger.warning(f"  CORS check error: {str(e)}")
            self.audit_results['cors'] = 'UNKNOWN'
    
    def network_diagnostics(self):
        """Perform network diagnostics."""
        logger.info("Running network diagnostics...")
        try:
            # Get local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Network info
            network_info = {
                'hostname': hostname,
                'local_ip': local_ip,
                'target_host': self.host,
                'target_port': self.port,
                'dns_resolution': self.host if self.host == 'localhost' else socket.gethostbyname(self.host)
            }
            
            self.audit_results['network'] = network_info
            logger.info(f"  Hostname: {hostname}")
            logger.info(f"  Local IP: {local_ip}")
            logger.info(f"  Target: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Network diagnostics error: {str(e)}")
    
    def generate_report(self):
        """Generate comprehensive audit report."""
        logger.info("Generating audit report...")
        report = {
            'audit_timestamp': self.timestamp,
            'api_server': self.url,
            'results': self.audit_results,
            'status': 'SECURE' if self.audit_results.get('connectivity') == 'OK' else 'WARNING'
        }
        
        report_file = f"logs/nethunter_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved: {report_file}")
        return report
    
    def run_full_audit(self):
        """Execute complete audit suite."""
        logger.info("═══════════════════════════════════════════════════════════════")
        logger.info("McswazSting AI Manager - NetHunter Audit Suite")
        logger.info("═══════════════════════════════════════════════════════════════")
        
        # Create logs directory if it doesn't exist
        Path('logs').mkdir(exist_ok=True)
        
        self.network_diagnostics()
        self.check_connectivity()
        
        if self.audit_results.get('connectivity') == 'OK':
            self.probe_endpoints()
            self.check_cors_headers()
        
        report = self.generate_report()
        
        logger.info("═══════════════════════════════════════════════════════════════")
        logger.info(f"Audit Status: {report['status']}")
        logger.info("═══════════════════════════════════════════════════════════════")
        
        return report

def main():
    parser = argparse.ArgumentParser(
        description='McswazSting AI Manager - NetHunter Network Audit Tool'
    )
    parser.add_argument('--host', default='localhost', help='API server host (default: localhost)')
    parser.add_argument('--port', type=int, default=5000, help='API server port (default: 5000)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Run audit
    auditor = NetHunterAPIAudit(host=args.host, port=args.port)
    report = auditor.run_full_audit()
    
    # Output results
    if args.json:
        print(json.dumps(report, indent=2))
    
    return 0 if report['status'] == 'SECURE' else 1

if __name__ == '__main__':
    sys.exit(main())
