import winreg

def remove_from_startupW():
    try:
        # Ouvre la clé de registre où les programmes de démarrage sont listés
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0, winreg.KEY_SET_VALUE)
        
        # Supprime l'entrée associée au fichier
        winreg.DeleteValue(key, "KeyLogger")  # Remplacez "KeyLogger" par le nom utilisé dans le script original
        winreg.CloseKey(key)
        print("Entrée supprimée du démarrage.")
    except FileNotFoundError:
        print("L'entrée n'existe pas dans le registre.")
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")


def remove_from_startupX():
    try:
        # Ouvre la clé de registre où les programmes de démarrage sont listés
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0, winreg.KEY_SET_VALUE)
        
        # Supprime l'entrée associée au fichier
        winreg.DeleteValue(key, "DataLogger")  # Remplacez "Datalogger" par le nom utilisé dans le script original
        winreg.CloseKey(key)
        print("Entrée supprimée du démarrage.")
    except FileNotFoundError:
        print("L'entrée n'existe pas dans le registre.")
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")

# Appeler la fonction
remove_from_startupW()
remove_from_startupX()


# Ou faire : Win + R > regedit > HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run > Supprimer l'entrée "KeyLogger" ou "DataLogger"
