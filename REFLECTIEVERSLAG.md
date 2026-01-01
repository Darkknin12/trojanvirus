# Reflectieverslag - Trojan Agent Project
**Vak:** Ethical Hacking  
**Datum:** Januari 2026  
**Student:** Grigor Mkrttsjan

---

## 1. Inleiding

Voor dit project heb ik een modulaire Trojan-agent ontwikkeld die communiceert met een GitHub repository. Het doel was om inzicht te krijgen in hoe aanvallers te werk gaan en welke technieken zij gebruiken voor Command & Control (C2) infrastructuur.

---

## 2. Projectoverzicht

### Wat ik heb gebouwd
- Een Trojan framework dat verbindt met GitHub als C2 server
- Custom module importer die code dynamisch laadt
- Drie werkende modules: System Enumeration, Portscan, en Screenshot
- Configuratiesysteem met JSON voor flexibele aansturing

### Gebruikte technologieën
- Python 3.x
- PyGithub library voor API communicatie
- Socket library voor netwerk operaties
- Pillow/mss voor screenshots
- Threading voor performance

---

## 3. Technische Keuzes en Uitdagingen

### Waarom GitHub als C2?
Ik koos voor GitHub omdat:
- Het verkeer lijkt op normaal ontwikkelaars-verkeer
- HTTPS encryptie maakt inspectie moeilijker
- GitHub wordt zelden geblokkeerd door firewalls
- Gratis en betrouwbare infrastructuur

### Custom Module Importer
Een van de lastigste onderdelen was het dynamisch laden van modules van GitHub. De uitdaging was om Python code te downloaden en uit te voeren zonder lokale bestanden. Dit loste ik op met `exec()` en een custom module namespace.

### Random Polling Interval
Om detectie te voorkomen gebruik ik een willekeurig interval tussen 30-90 seconden. Dit maakt het patroon minder voorspelbaar voor security tools die op regelmatige "beacons" letten.

### Unieke Client ID's
Elke trojan genereert een unieke ID gebaseerd op systeem eigenschappen (hostname, gebruikersnaam). Dit maakt botnet-achtige functionaliteit mogelijk waarbij elke client apart aangestuurd kan worden.

---

## 4. De Modules

### Module 1: System Enumeration
**Doel:** Verzamel informatie over het geinfecteerde systeem

**Wat het verzamelt:**
- OS type en versie
- Netwerk configuratie en IP adressen
- Huidige gebruiker en admin rechten
- Draaiende processen
- Environment variabelen

**Ethical Hacking context:** Dit is typisch de eerste stap in een aanval - reconnaissance. Met deze info kan een aanvaller bepalen welke exploits bruikbaar zijn.

### Module 2: Portscan
**Doel:** Ontdek open poorten op een target

**Features:**
- Multi-threaded scanning voor snelheid
- Configureerbare poorten lijst
- Service detectie (welke dienst draait op de poort)

**Ethical Hacking context:** Port scanning is essentieel voor het vinden van aanvalsvectoren. Open poorten kunnen kwetsbare services onthullen.

### Module 3: Screenshot
**Doel:** Maak screenshot van het bureaublad

**Features:**
- Werkt met meerdere libraries (Pillow, mss, pyautogui)
- Output in base64 voor makkelijke transmissie
- Instelbare kwaliteit

**Ethical Hacking context:** Screenshots kunnen gevoelige informatie bevatten zoals wachtwoorden, emails, of documenten.

---

## 5. Ethische Reflectie

### Hoe dit misbruikt kan worden
Deze technieken worden door echte aanvallers gebruikt voor:
- **Spionage:** System enum en screenshots lekken gevoelige data
- **Laterale beweging:** Portscans helpen nieuwe targets vinden
- **Persistentie:** C2 via GitHub is moeilijk te detecteren
- **Data exfiltratie:** Resultaten worden automatisch geupload

### Hoe je je hiertegen beschermt
1. **Network monitoring:** Let op ongewoon GitHub API verkeer
2. **Endpoint Detection:** Tools zoals EDR kunnen verdacht gedrag herkennen
3. **Process monitoring:** Onbekende Python processen met netwerk activiteit
4. **Least privilege:** Limiteer wat gebruikers kunnen installeren
5. **Segmentatie:** Beperk welke systemen naar GitHub kunnen connecten

### Mijn ethische grenzen
- Ik heb alleen getest op mijn eigen virtuele machine
- Geen echte credentials of gevoelige data verzameld
- Code niet gedeeld buiten educatieve context
- Repository is private

---

## 6. Logboek - Ethical Hacking Proces

### Python Basics
- Gevolgd Python labo's over sockets en HTTP
- Geoefend met basis netwerk programming

### Reconnaissance Technieken
- Geleerd over OSINT en information gathering
- Experiments met port scanning (nmap, eigen scripts)

### C2 Concepten
- Bestudeerd hoe botnets werken
- Onderzoek naar verschillende C2 channels (HTTP, DNS, GitHub)

### Project Development
- Opgezet trojan framework
- Ontwikkeld eerste modules
- Testing in VirtualBox


---

## 7. Wat ik heb geleerd

### Technisch
- Hoe GitHub API werkt en hoe je er mee communiceert
- Dynamisch laden van Python code
- Multi-threading voor netwerk operaties
- Base64 encoding voor data transmissie

### Security perspectief
- Hoe aanvallers "living off the land" gebruiken (legitieme diensten misbruiken)
- Waarom detectie van moderne malware zo moeilijk is
- Het belang van defense in depth

### Persoonlijk
- Beter begrip van de "andere kant" helpt bij verdediging
- Ethical hacking vereist discipline en verantwoordelijkheid
- De grens tussen research en misbruik is soms dun

---

## 8. Conclusie

Dit project heeft me laten zien hoe relatief eenvoudig het is om een werkende C2 infrastructuur op te zetten met legitieme diensten. De technieken die ik heb geleerd zijn krachtig maar ook gevaarlijk in verkeerde handen.

Het belangrijkste inzicht is dat verdediging begint bij begrip van de aanval. Door zelf een trojan te bouwen snap ik nu beter waar security teams op moeten letten en waarom bepaalde security maatregelen belangrijk zijn.

---

## 9. Bronnen

- Black Hat Python - Justin Seitz
- GitHub API Documentatie
- Python socket programming tutorials
- MITRE ATT&CK Framework (T1567 - Exfiltration Over Web Service)

---

**Let op:** Dit project is puur educatief. Gebruik deze kennis alleen ethisch en legaal.
