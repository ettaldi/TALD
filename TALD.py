# Importation
import re
import os
import csv
from colorama import Fore, Style, init

init()

# Logo TALD
def display_logo():
    logo = f"""
{Fore.LIGHTGREEN_EX}
      ╔══════════════════════════════════════╗
      ║ ████████  █████  ██     ██████       ║
      ║    ██    ██   ██ ██     ██   ██      ║
      ║    ██    ███████ ██     ██   ██      ║
      ║    ██    ██   ██ ██     ██   ██      ║
      ║    ██    ██   ██ ██████ ██████  v1.0 ║
      ╚══════════════════════════════════════╝
        -- {Fore.GREEN}Threat and Anomaly Log Detector {Fore.LIGHTGREEN_EX}--
{Fore.LIGHTGREEN_EX}
       
{Fore.LIGHTCYAN_EX}  
            By {Fore.LIGHTBLUE_EX}Mohamed Rayan Ettaldi
{Fore.LIGHTCYAN_EX} [!] Visit {Fore.LIGHTGREEN_EX}https://github.com/login{Fore.LIGHTCYAN_EX} to update the tool

    """
    print(logo)

# Commands
SUSPICIOUS_PATTERNS = {
    "Dangerous Commands": [
        r"rm\s+-rf\s+\/",                     # Suppression récursive et forcée de la racine
        r"rm\s+-rf\s+\.\*",                   # Suppression de fichiers cachés
        r"rm\s+-rf\s+.*",                     # Suppression de tous les fichiers
        r"wget\s+http",                       # Téléchargement via HTTP
        r"curl\s+http",                       # Téléchargement via HTTP
        r"chmod\s+777",                       # Autorisations non sécurisées
        r"chown\s+-R\s+.*",                   # Modification abusive de propriétaire
        r"mkfs\.\w+",                         # Formatage de disque
        r"shutdown\s+-h",                     # Arrêt de la machine
        r"reboot",                            # Redémarrage
        r"pkill\s+-f",                        # Terminaison de processus par motif
        r"kill\s+-9\s+\d+",                   # Forçage de terminaison
        r"dd\s+if=.*",                        # Manipulation de disques
        r"echo\s+.*>\s+/dev/sda",             # Écriture directe sur un disque
        r"tar\s+.*--to-command",              # Extraction avec commande arbitraire
        r"mktemp\s+.*",                       # Création de fichiers temporaires
        r"find\s+.*\s+-exec\s+.*\|.*",        # Exécution arbitraire avec find
        r"cat\s+.*\|.*",                      # Chaînage avec cat
        r"ps\s+-ef\s+|",                      # Liste des processus avec redirection
        r"dd\s+if=\S+\s+of=/dev/\S+",         # Copie de données sensibles
        r"chattr\s+\+i\s+/etc/passwd",        # Modification des fichiers sensibles
        r"mount\s+.*\s+/dev/sda",             # Montage suspect de périphériques
    ],
    "Obfuscation Patterns": [
        r"base64\s+-d",                       # Décodage base64
        r"eval\(",                            # Exécution dynamique
        r"exec\(",                            # Exécution dynamique
        r"system\(",                          # Exécution de commandes système
        r"xor",                               # Chiffrement XOR
        r"shc\s+-f",                          # Compilation de script shell
        r"perl\s+-e",                         # Exécution Perl
        r"python\s+-c",                       # Exécution Python
        r"php\s+-r",                          # Exécution PHP
        r"gpg\s+--decrypt",                   # Décryptage GPG
        r"openssl\s+enc\s+-d",                # Décryptage OpenSSL
        r"awk\s+'BEGIN",                      # Script awk
        r"sed\s+-e",                          # Script sed
        r"tee\s+.*\|",                        # Redirection combinée
        r"zsh\s+-c",                          # Exécution zsh
        r"obfuscate",                         # Indicateur général d'obfuscation
        r"git\s+clone\s+.*\|.*",               # Clonage et exécution automatique
        r"find\s+.*\s+-exec\s+.*\$(.*)",       # Commande imbriquée avec find
        r"sh\s+-c",                           # Exécution d'une commande avec sh
        r"curl\s+.*\|.*bash",                 # Téléchargement et exécution de script
        r"wget\s+.*\|.*bash",                 # Téléchargement et exécution de script
        r"perl\s+-e\s+'.*=.*'",               # Exécution Perl avec chaîne encodée
        r"base64\s+.*\|base64\s+-d",          # Chaînage de base64
    ],
    "Network Activity": [
        r"nc\s+-e",                           # Netcat avec exécution de commande
        r"bash\s+-i\s+>&",                    # Shell interactif en arrière-plan
        r"reverse_shell",                     # Indicateur général de reverse shell
        r"nmap\s+-s",                         # Scan réseau avec Nmap
        r"tcpdump",                           # Capture de paquets
        r"wireshark",                         # Analyse réseau
        r"wget\s+https:\/\/",                 # Téléchargement via HTTPS
        r"curl\s+https:\/\/",                 # Téléchargement via HTTPS
        r"scp\s+.*@.*:.*",                    # Copie sécurisée distante
        r"ssh\s+-R",                          # Tunnel SSH inversé
        r"telnet\s+.*",                       # Connexion Telnet
        r"ping\s+-c\s+\d+\s+.*",              # Test de connectivité
        r"dig\s+.*",                          # Recherche DNS
        r"whois\s+.*",                        # Recherche d'informations WHOIS
        r"wget\s+.*\|sh",                     # Téléchargement et exécution directe
        r"curl\s+.*\|sh",                     # Téléchargement et exécution directe
        r"telnet\s+.*\|.*",                   # Telnet avec redirection
        r"ssh\s+.*@.*\s+-D",                  # Tunnel SSH sur un port
        r"ncat\s+.*\|.*",                     # Ncat avec redirection
        r"nc\s+-l\s+-p\s+\d+",                # Écouteur Netcat
        r"nmap\s+-sS",                        # Scan de ports avec Nmap (SYN)
        r"nmap\s+-O",                         # Détection de système d'exploitation avec Nmap
        r"tshark\s+-r",                       # Capture de paquets avec tshark
        r"dd\s+if=/dev/urandom\s+of=/dev/sda", # Écriture de données aléatoires sur disque
        r"dd\s+if=/dev/random\s+of=/dev/sda", # Écriture de données aléatoires sur disque
    ],
    "File and Process Manipulation": [
        r"chattr\s+\+i",                      # Modifier les attributs immuables
        r"lsattr",                            # Liste des attributs de fichier
        r"crontab\s+-e",                      # Édition de tâches planifiées
        r"nohup\s+.*&",                       # Exécution persistante en arrière-plan
        r"disown",                            # Détachement de processus
        r"systemctl\s+stop",                  # Arrêt de service système
        r"sudo\s+.*",                         # Commandes avec sudo
        r"find\s+.*\s+-exec",                 # Exécution via find
        r"alias\s+.*=.*",                     # Création d'alias
        r"unset\s+",                          # Suppression de variables d'environnement
        r"cp\s+.*\s+/dev/null",               # Copie silencieuse
        r"mv\s+.*\s+/tmp",                    # Déplacement suspect vers /tmp
        r"grep\s+-q",                         # Recherche silencieuse
        r"ln\s+-s",                           # Création de liens symboliques
        r"umount\s+.*",                       # Démontage de disque
        r"mount\s+.*\s+/dev/sda",             # Montage suspect de périphérique
        r"kill\s+-9\s+\d+",                   # Forçage de terminaison
        r"strace\s+.*",                       # Trace des appels système
        r"lsof\s+.*",                         # Liste des fichiers ouverts
        r"killall\s+.*",                      # Terminaison de tous les processus
        r"ps\s+aux",                          # Liste de processus avec détails
        r"chmod\s+.+\s+.*\.sh",               # Script shell avec droits d'exécution
        r"chown\s+-R\s+.*\s+/etc/passwd",     # Modification des fichiers sensibles
    ],
    "Persistence Mechanisms": [
        r"echo\s+.*>>.*\.bashrc",             # Modification des fichiers de profil
        r"echo\s+.*>>.*\.profile",            # Modification des fichiers de profil
        r"echo\s+.*>>.*\.zshrc",              # Modification des fichiers de profil Zsh
        r"ln\s+-s",                           # Création de liens symboliques
        r"mkfifo",                            # Création de canaux nommés
        r"at\s+.*",                           # Planification de tâches avec at
        r"systemd\s+-edit",                   # Modification des services
        r"rc.local",                          # Utilisation de rc.local pour la persistance
        r"crontab\s+-l",                      # Liste des tâches planifiées
        r"touch\s+.*\.sh",                    # Création de scripts suspects
        r"chmod\s+\+x\s+.*\.sh",              # Ajout d'exécutions sur scripts
        r"echo\s+.*>>.*\.bash_profile",       # Modification de .bash_profile
        r"systemctl\s+enable\s+.*",           # Activation de services persistants
        r"echo\s+.*>>.*\.zprofile",           # Modification de .zprofile
    ],
    "Exploitation Indicators": [
        r"metasploit",                        # Indicateur Metasploit
        r"msfconsole",                        # Console Metasploit
        r"msfvenom",                          # Génération de payloads
        r"exploit\s+",                        # Lancement d'exploit
        r"reverse_tcp",                       # Payload TCP inversé
        r"bind_tcp",                          # Payload TCP direct
        r"powershell\s+-enc",                 # Exécution encodée PowerShell
        r"mimikatz",                          # Utilisation de Mimikatz
        r"secretsdump.py",                    # Dump de secrets via Impacket
        r"crackmapexec",                      # Exploration réseau et brute-force
        r"john\s+--wordlist",                 # Utilisation de John the Ripper
        r"hydra\s+-l",                        # Utilisation d'Hydra
        r"enum4linux",                        # Extraction d'informations avec enum4linux
        r"evilgrade",                         # Exploitation de mises à jour logicielles
        r"smbexec",                           # Exécution de commande via SMB
        r"wmiexec",                           # Exécution via WMI
    ],
}

# Analyze a file
def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    results = []
    for i, line in enumerate(lines, start=1):
        for category, patterns in SUSPICIOUS_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, line):
                    results.append((i, line.strip(), category, pattern))
    return results

# Save results to CSV
def save_to_csv(file_name, results):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Line Number", "Line Content", "Category", "Suspicious Pattern"])
        for line_no, line, category, pattern in results:
            writer.writerow([line_no, line, category, pattern])
    print(f"{Fore.GREEN}[+] Results saved to {file_name}{Style.RESET_ALL}")

# Display the results
def display_results(file_path, results):
    if results:
        print(f"{Fore.RED}\n[!] Risks detected in the file: {file_path}{Style.RESET_ALL}")
        print("-" * 80)
        for line_no, line, category, pattern in results:
            print(f"{Fore.YELLOW}  - Line {line_no}: {line}{Style.RESET_ALL}")
            print(f"    → Category: {Fore.CYAN}{category}{Style.RESET_ALL}")
            print(f"    → Suspicious Pattern: {Fore.MAGENTA}{pattern}{Style.RESET_ALL}")
        print("-" * 80)

# Main function
def main():
    display_logo()
    
    # Prompt user to choose an option
    print(f"{Fore.LIGHTCYAN_EX}1. Analyze a directory                 3. Analyze a directory and save results to CSV") 
    print(f"{Fore.LIGHTCYAN_EX}2. Analyze a specific file             4. Analyze a specific file and save results to CSV")
    print()
    choice = input(f"{Fore.CYAN}Please choose an option : {Style.RESET_ALL}")
    
    if choice == '1':
        directory = input(f"{Fore.LIGHTCYAN_EX}Enter the directory path to analyze: {Style.RESET_ALL}")
        if not os.path.isdir(directory):
            print(f"{Fore.RED}[!] The specified path is not a valid directory: {directory}{Style.RESET_ALL}")
            return

        print(f"{Fore.LIGHTCYAN_EX}Scanning directory: {directory}{Style.RESET_ALL}")
        all_results = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(('.sh', '.py', '.bat', '.ps1')):
                    print(f"{Fore.GREEN}\n[+] Analyzing file: {file_path}{Style.RESET_ALL}")
                    results = analyze_file(file_path)
                    all_results.extend(results)
        if all_results:
            display_results(directory, all_results)
        else:
            print(f"{Fore.RED}[!] No suspicious patterns found in the directory.{Style.RESET_ALL}")

    elif choice == '2':
        file_path = input(f"{Fore.LIGHTCYAN_EX}Enter the file path to analyze: {Style.RESET_ALL}")
        if not os.path.isfile(file_path):
            print(f"{Fore.RED}[!] The specified path is not a valid file: {file_path}{Style.RESET_ALL}")
            return
        results = analyze_file(file_path)
        display_results(file_path, results)
        if results:
            save_to_csv(f'{os.path.basename(file_path)}_results.csv', results)
        else:
            print(f"{Fore.RED}[!] No suspicious patterns found in the file.{Style.RESET_ALL}")

    elif choice == '3':
        directory = input(f"{Fore.LIGHTCYAN_EX}Enter the directory path to analyze: {Style.RESET_ALL}")
        if not os.path.isdir(directory):
            print(f"{Fore.RED}[!] The specified path is not a valid directory: {directory}{Style.RESET_ALL}")
            return

        print(f"{Fore.LIGHTCYAN_EX}Scanning directory: {directory}{Style.RESET_ALL}")
        all_results = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(('.sh', '.py', '.bat', '.ps1')):
                    print(f"{Fore.GREEN}\n[+] Analyzing file: {file_path}{Style.RESET_ALL}")
                    results = analyze_file(file_path)
                    all_results.extend(results)
        if all_results:
            save_to_csv('directory_scan_results.csv', all_results)
        else:
            print(f"{Fore.RED}[!] No suspicious patterns found in the directory.{Style.RESET_ALL}")

    elif choice == '4':
        file_path = input(f"{Fore.LIGHTCYAN_EX}Enter the file path to analyze: {Style.RESET_ALL}")
        if not os.path.isfile(file_path):
            print(f"{Fore.RED}[!] The specified path is not a valid file: {file_path}{Style.RESET_ALL}")
            return
        results = analyze_file(file_path)
        if results:
            save_to_csv(f'{os.path.basename(file_path)}_scan_results.csv', results)
        else:
            print(f"{Fore.RED}[!] No suspicious patterns found in the file.{Style.RESET_ALL}")

    else:
        print(f"{Fore.RED}[!] Invalid option. Please choose 1, 2, 3, or 4.{Style.RESET_ALL}")

# Run the program
if __name__ == "__main__":
    main()