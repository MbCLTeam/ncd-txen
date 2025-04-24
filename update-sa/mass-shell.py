import socket
import threading
import time

IP_BASE = "192.168.1."
PORT = 6969
connections = []
LOGS = []

USER = input("Digite o nome de usuário: ").strip()
PASSWORD = input("Digite a senha: ").strip()
show_failed_logs = input("Mostrar logs de falhas? (s/n): ").strip().lower() == 's'

# Conexão com IP alvo
def connect_to_target(ip):
    try:
        time.sleep(0.05)  # pequeno atraso por IP, mas ainda simultâneo com threads

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, PORT))

        banner = s.recv(1024).decode(errors="ignore")
        if "BubbleDash Service" in banner:
            s.sendall((USER + "\n").encode())
            response = s.recv(1024).decode(errors="ignore")

            if "Digite a senha" in response:
                s.sendall((PASSWORD + "\n").encode())
                login_resp = s.recv(1024).decode(errors="ignore")

                if "Acesso concedido" in login_resp:
                    print(f"[+] Acesso concedido: {ip}")
                    connections.append((ip, s))
                    LOGS.append(f"[+] Conectado com sucesso em {ip}")
                    return
                else:
                    LOGS.append(f"[-] Senha incorreta em {ip}")
            else:
                LOGS.append(f"[-] Usuário incorreto ou erro em {ip}")
        else:
            LOGS.append(f"[-] Serviço inválido ou porta errada em {ip}")
        s.close()
    except Exception as e:
        LOGS.append(f"[x] Erro {ip}: {str(e)}")

# Scanner da rede
def scan_ips():
    threads = []
    for i in range(1, 255):
        ip = f"{IP_BASE}{i}"
        t = threading.Thread(target=connect_to_target, args=(ip,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

scan_ips()

if show_failed_logs:
    print("\n[LOG DE FALHAS]")
    for log in LOGS:
        print(log)

print(f"\n[!] Máquinas conectadas: {len(connections)}")

# Shell interativo
def command_shell(connections):
    print("\nDigite comandos. Use 'exit' para sair.")
    while True:
        cmd = input("CMD> ").strip()
        if cmd.lower() in ["exit", "quit"]:
            break
        if not cmd:
            continue

        for ip, conn in connections:
            try:
                conn.sendall((cmd + "\n").encode())
            except Exception as e:
                print(f"[{ip}] erro ao enviar: {str(e)}")

        # Leitura separada por conexão com delay pra sincronizar resposta
        for ip, conn in connections:
            try:
                time.sleep(0.3)  # espera por resposta antes de tentar ler
                conn.settimeout(3)
                output = conn.recv(4096).decode(errors="ignore")
                print(f"[{ip}]:\n{output.strip()}\n{'-'*40}")
            except Exception as e:
                print(f"[{ip}] erro na leitura: {str(e)}")

command_shell(connections)

# Finalizando conexões
for ip, conn in connections:
    try:
        conn.close()
    except:
        pass
