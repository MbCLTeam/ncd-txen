import os
import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def execute_command(command, success_message, error_message):
    print(f"[=]: {command}...")
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print(f"[=]: {success_message}")
    else:
        print(f"[=]: {error_message}")

def request_admin():
    print("Este programa requer permissões de administrador.")
    input("Pressione Enter para solicitar permissão...")

    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except:
        print("Erro ao solicitar permissões. Execute manualmente como administrador.")
        input("Pressione Enter para sair...")
        sys.exit(1)

def main():
    logo = "\033[1;36m" + """
   ________               __  ____        ____
  / ____/ /_  ____  _____/ /_/ __ )__  __/ __ \____ ___________
 / / __/ __ \/ __ \/ ___/ __/ __  / / / / /_/ / __ `/ ___/ ___/
/ /_/ / / / / /_/ (__  ) /_/ /_/ / /_/ / ____/ /_/ (__  |__  )
\____/_/ /_/\____/____/\__/_____/\__, /_/    \__,_/____/____/
                                /____/
""" + "\033[0m"  

    print(logo)

    if not is_admin():
        request_admin()
        sys.exit(0)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(logo)

        print("\n\n\033[1;36m[1]:\033[0m Injetar By Pass")
        print("\033[1;36m[2]:\033[0m Reiniciar PC")
        print("\033[1;36m[0]:\033[0m Sair\n\n")

        choice = input("\033[1;36m>> \033[0m")  

        if choice == '1':
            execute_command("reg add HKCU\\Software\\Microsoft\\Command Processor /v DisableContextualTips /t REG_DWORD /d 0 /f", 
                            "CMD liberado com sucesso!", "Falha ao liberar CMD.")
            execute_command("reg add HKCU\\Software\\Microsoft\\PowerShell\\1\\PowerShellEngine /v ExecutionPolicy /t REG_SZ /d Unrestricted /f", 
                            "PowerShell liberado com sucesso!", "Falha ao liberar PowerShell.")
            execute_command("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Explorer /t REG_SZ /d Explorer.exe /f", 
                            "Menu Run habilitado com sucesso!", "Falha ao habilitar Menu Run.")
            execute_command("reg add HKCU\\Software\\Classes\\*\\shell\\open\\command /ve /t REG_SZ /d \"cmd.exe\" /f", 
                            "Botão direito habilitado com sucesso!", "Falha ao habilitar botão direito.")
            execute_command("icacls %userprofile% /grant:r Users:(OI)(CI)F", 
                            "Acesso a pastas liberado com sucesso!", "Falha ao liberar acesso a pastas.")
            execute_command("sc config cmd start= demand", 
                            "Protegendo CMD e PS para bloqueio com sucesso!", "Falha ao proteger CMD e PS.")
            execute_command("taskkill /F /IM taskmgr.exe", 
                            "Acesso ao TaskManager liberado com sucesso!", "Falha ao liberar acesso ao TaskManager.")
            execute_command("sc config taskmgr start= auto", 
                            "Protegendo TaskManager com sucesso!", "Falha ao proteger TaskManager.")
            execute_command("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 1 /f", 
                            "Editor de Registro habilitado com sucesso!", "Falha ao habilitar Editor de Registro.")

            print("\033[92mByPass concluído, aperte qualquer tecla....\033[0m")
            input()

        elif choice == '2':
            os.system("shutdown /r /t 0")  

        elif choice == '0':
            break

        else:
            print("Opção inválida, tente novamente.")
            input("Pressione qualquer tecla para continuar...")

if __name__ == "__main__":
    main()
