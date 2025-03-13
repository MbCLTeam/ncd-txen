import os
import subprocess
import ctypes
import sys
import shutil

# Verifica se o script está sendo executado como administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Função para executar comandos e retornar mensagens
def execute_command(command, action_name):
    print("\033[1;36m[\033[0m\033[1;37m=\033[0m\033[1;36m]\033[0m Tentando", action_name, "...")
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("\033[1;36m[\033[0m\033[1;32m✔\033[0m\033[1;36m]\033[0m", action_name, "concluído com sucesso!")
    else:
        print("\033[1;36m[\033[0m\033[1;31m✖\033[0m\033[1;36m]\033[0m Falha ao", action_name, ".")

# Função para configurar a inicialização do script
def setup_startup(script_path):
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    destination_path = os.path.join(startup_folder, "BubbleDash.lnk")

    # Criar um atalho para o script na pasta de inicialização
    command = f'Start "" "{script_path}"'
    subprocess.call(['powershell', '-Command', f'$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut("{destination_path}"); $s.TargetPath = "{script_path}"; $s.Save()'])
    print("\033[1;36m[\033[0m\033[1;32m✔\033[0m\033[1;36m]\033[0m BubbleDash configurado para iniciar com o sistema.")

# Função principal
def main():
    # Logo em ciano bold
    logo = "\033[1;36m" + """
   ________               __  ____        ____
  / ____/ /_  ____  _____/ /_/ __ )__  __/ __ \____ ___________
 / / __/ __ \/ __ \/ ___/ __/ __  / / / / /_/ / __ `/ ___/ ___/
/ /_/ / / / / /_/ (__  ) /_/ /_/ / /_/ / ____/ /_/ (__  |__  )
\____/_/ /_/\____/____/\__/_____/\__, /_/    \__,_/____/____/
                                /____/
""" + "\033[0m"  # Reset color

    print(logo)

    if not is_admin():
        print("Este programa requer permissões de administrador.")
        input("Pressione qualquer tecla para solicitar permissão...")

        # Solicita permissão de administrador
        if not ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1):
            print("Permissão negada, aperte qualquer tecla para sair...")
            input()
            sys.exit(0)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(logo)

        print("\n\n\033[1;36m[\033[0m\033[1;37m1\033[0m\033[1;36m]\033[0m Injetar By Pass")
        print("\033[1;36m[\033[0m\033[1;37m2\033[0m\033[1;36m]\033[0m Reiniciar")
        print("\033[1;36m[\033[0m\033[1;37m0\033[0m\033[1;36m]\033[0m Sair\n\n")

        choice = input("\033[1;36m>> \033[0m")  # Prompt em ciano

        if choice == '1':
            execute_command("reg add HKCU\\Software\\Microsoft\\Command Processor /v DisableContextualTips /t REG_DWORD /d 0 /f", 
                            "liberar o CMD")
            execute_command("reg add HKCU\\Software\\Microsoft\\PowerShell\\1\\PowerShellEngine /v ExecutionPolicy /t REG_SZ /d Unrestricted /f", 
                            "liberar o PowerShell")
            execute_command("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Explorer /t REG_SZ /d Explorer.exe /f", 
                            "habilitar o Menu Executar")
            execute_command("reg add HKCU\\Software\\Classes\\*\\shell\\open\\command /ve /t REG_SZ /d \"cmd.exe\" /f", 
                            "habilitar o botão direito")
            execute_command("icacls %userprofile% /grant:r Users:(OI)(CI)F", 
                            "liberar acesso às pastas")
            execute_command("sc config cmd /start= demand", 
                            "proteger CMD e PowerShell contra bloqueio")
            execute_command("taskkill /F /IM taskmgr.exe", 
                            "liberar o Gerenciador de Tarefas")
            execute_command("sc config taskmgr start= auto", 
                            "proteger o Gerenciador de Tarefas contra bloqueio")
            execute_command("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 1 /f", 
                            "habilitar o Editor de Registro")

            # Copiar BubbleDash.py para uma pasta de inicialização
            script_path = os.path.join(os.getcwd(), "BubbleDash.py")
            shutil.copy(script_path, os.path.join(os.getenv("APPDATA"), "BubbleDash.py"))  # Colocar na pasta AppData

            # Configurar inicialização do BubbleDash
            setup_startup(os.path.join(os.getenv("APPDATA"), "BubbleDash.py"))

            # Iniciar o BubbleDash em segundo plano
            subprocess.Popen(['python', os.path.join(os.getenv("APPDATA"), "BubbleDash.py")])
            print("\033[1;36m[\033[0m\033[1;32m✔\033[0m\033[1;36m]\033[0m BubbleDash iniciado em segundo plano.")

            print("\033[92mByPass concluído, aperte qualquer tecla....\033[0m")
            input()

        elif choice == '2':
            os.system("shutdown /r /t 0")  # Reiniciar sistema instantaneamente

        elif choice == '0':
            break

        else:
            print("\033[1;36m[\033[0m\033[1;31m✖\033[0m\033[1;36m]\033[0m Opção inválida, tente novamente.")
            input("Pressione qualquer tecla para continuar...")

if __name__ == "__main__":
    main()
