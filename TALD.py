import os
import re
import time
from colorama import Fore, Style, init
from TALDCommands import TALDCommands
init(autoreset=True)

def gradient_text(text, start_color, end_color):
    start_rgb = start_color
    end_rgb = end_color
    gradient_steps = len(text)
    
    result = ""
    for i, char in enumerate(text):
        ratio = i / (gradient_steps - 1) if gradient_steps > 1 else 0
        r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
        g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
        b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
        result += f"\033[38;2;{r};{g};{b}m{char}"
    return result + Style.RESET_ALL

def display_logo():
    logo_lines = [
        r"                              __________________   ______            ",
        r"                             /__   ___/  __  |  |  \     \           ",
        r"                               /  /  /  __   |  |   |  |  \          ",
        r"                              /  /  /  / /  /|  |___|     /          ",
        r"                             /__/  /__/ /__/ |_____/|____/  v1.0     ",
        "                                                                    ",
        "                           -- Outil d'analyse de scripts --          ",
    ]
    logo_footer = f"""
      {Fore.LIGHTCYAN_EX}                        Par {Style.DIM + Fore.LIGHTCYAN_EX} Mohamed Rayan Ettaldi{Style.NORMAL}
      {Fore.LIGHTGREEN_EX + Style.BRIGHT}  [!] {Style.NORMAL + Fore.LIGHTCYAN_EX}Visitez {Style.DIM + Fore.LIGHTCYAN_EX}https://github.com/ettaldi/TALD{Style.NORMAL + Fore.LIGHTCYAN_EX} pour mettre à jour l'outil
"""
    start_color = (0, 255, 0)
    end_color = (135, 206, 250)

    for line in logo_lines:
        print(Style.BRIGHT + gradient_text(line, start_color, end_color))
        time.sleep(0.2)
    print(logo_footer)

def analyze_file(file_path):
    try: 
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"{Fore.RED+ Style.BRIGHT}[!]{Fore.RED+ Style.NORMAL}  Erreur lors de la lecture du fichier {file_path}: {e}{Style.RESET_ALL}")
        return []

    results = []
    for i, line in enumerate(lines, start=1):
        for patterns in TALDCommands.values():
            for pattern in patterns:
                if re.search(pattern, line):
                    results.append((i, line.strip(), pattern))
    return results

def display_results(file_path, results):
    if results:
        print(f"{Fore.RED + Style.BRIGHT}\n[!]{Fore.RED + Style.NORMAL} Risques détectés dans le fichier : {file_path}{Style.RESET_ALL}")
        print("=" * 80)
        print(f"{'Numéro de ligne':<20}{'Motif':<30}{'Extrait de code':<40}")
        print("=" * 80)
        for line_no, line, pattern in results:
            print(f"{line_no:<20}{pattern:<30}{line:<40}")
        print("=" * 80)

def analyze_directory(directory):
    if not os.path.isdir(directory):
        print(f"{Fore.RED+ Style.BRIGHT}[!]{Fore.RED+ Style.NORMAL}  Le chemin spécifié n'est pas un répertoire valide. {Style.RESET_ALL}")
        return

    print(f"{Fore.LIGHTCYAN_EX}     Analyse du répertoire : {directory}{Style.RESET_ALL}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.sh', '.py', '.bat', '.ps1')):
                results = analyze_file(file_path)
                if results:
                    print(f"{Fore.LIGHTGREEN_EX + Style.BRIGHT}\n[+]  {Style.NORMAL + Fore.LIGHTCYAN_EX}Analyse du fichier : {file_path}")
                    display_results(file_path, results)

def main():
    display_logo()
    while True:
        print(f"{Fore.LIGHTGREEN_EX + Style.BRIGHT}    1.{Style.NORMAL + Fore.LIGHTCYAN_EX} Analyser un répertoire                     {Fore.LIGHTGREEN_EX + Style.BRIGHT}2.{Style.NORMAL + Fore.LIGHTCYAN_EX} Analyser un fichier spécifique") 
        print()
        print(f"{Fore.LIGHTRED_EX + Style.BRIGHT}                                   3. Quitter")
        print()
        choice = input(f"{Fore.LIGHTGREEN_EX}➤ {Fore.LIGHTCYAN_EX}   Choisissez une option : {Fore.LIGHTWHITE_EX} ")

        if choice == '1':
            directory = input(f"{Fore.LIGHTCYAN_EX}     Entrez le chemin du répertoire à analyser : {Fore.LIGHTWHITE_EX}")
            analyze_directory(directory)

        elif choice == '2':
            file_path = input(f"{Fore.LIGHTCYAN_EX}     Entrez le chemin du fichier à analyser : {Fore.LIGHTWHITE_EX}")
            if not os.path.isfile(file_path):
                print(f"{Fore.RED+ Style.BRIGHT}[!]{Fore.RED+ Style.NORMAL}  Le chemin spécifié n'est pas un fichier valide. {Style.RESET_ALL}")
                continue
            results = analyze_file(file_path)
            display_results(file_path, results)

        elif choice == '3':
            print(f"{Fore.LIGHTGREEN_EX}Fermeture de l'outil. {Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED+ Style.BRIGHT}[!]{Fore.RED+ Style.NORMAL}  Veuillez choisir une option valide.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
