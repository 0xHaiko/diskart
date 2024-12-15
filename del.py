import winreg

def remove_startup_entries(entries):
    try:
        # Ouvre la clé de registre où les programmes de démarrage sont listés
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0, winreg.KEY_SET_VALUE)
        for entry in entries:
            try:
                winreg.DeleteValue(key, entry)
                print(f"L'entrée '{entry}' a été supprimée du démarrage.")
            except FileNotFoundError:
                print(f"L'entrée '{entry}' n'existe pas dans le registre.")
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")

# Liste des entrées à supprimer
entries_to_remove = ["KeyLogger", "DataLogger"]

# Appel de la fonction
remove_startup_entries(entries_to_remove)

# Ou faire : Win + R > regedit > HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run > Supprimer l'entrée "Keylogger"
