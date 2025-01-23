const fs = require("fs");
const path = require("path");
const https = require("https");
const readline = require("readline");
const { spawn } = require("child_process");

// Variáveis ANSI para cores
const colors = {
  bold_yellow: "\x1b[1;33m",
  bold_green: "\x1b[1;32m",
  bold_red: "\x1b[1;31m",
  reset: "\x1b[0m",
};

// Versão atual
const CH_VERSION = "1.3.0";

// Função de erro customizada
function logError(errorMessage) {
  if (!errorMessage) {
    console.log(`${colors.bold_red}[!]:${colors.reset} Algum erro ocorreu, tente mais tarde...`);
  } else {
    console.log(`${colors.bold_red}[!]:${colors.reset}`);
  }
}

// Função de log normal
function log(message, color = colors.reset) {
  console.log(`${color}${message}${colors.reset}`);
}

// Função para obter dados via HTTPS
function httpsGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = "";
      res.on("data", (chunk) => {
        data += chunk;
      });
      res.on("end", () => {
        if (res.statusCode === 200) resolve(data);
        else reject(`HTTP ${res.statusCode}`);
      });
    }).on("error", (err) => {
      reject(err.message);
    });
  });
}

// Função para exibir o menu de ajuda
function showHelp() {
  console.log(`
${colors.bold_green}CoffeeHub - Ajuda${colors.reset}

Comandos disponíveis:
  ${colors.bold_green}update${colors.reset}      Verifica e instala atualizações da última versão.
  ${colors.bold_green}help${colors.reset}        Exibe este menu de ajuda.
`);
}

// Função para salvar arquivos diretamente na pasta atual
async function saveFiles(uMap, latestVersion) {
  for (const file of uMap) {
    const fileUrl = `https://gh-next-cdn.moonhorizon.xyz/coffeehub/${latestVersion}/files/${file}`;
    const filePath = path.join(__dirname, file); // Salva diretamente na pasta atual

    try {
      const fileContent = await httpsGet(fileUrl);
      fs.writeFileSync(filePath, fileContent, "utf8");
    } catch (error) {
      throw new Error(`Falha ao baixar o arquivo ${file}.`);
    }
  }
}

// Verificação de argumentos
const args = process.argv.slice(2);

if (args.length === 0) {
  require("../app");
} else if (["update", "--update", "-u", "--u"].includes(args[0])) {
  (async () => {
    log("[UPDATE]: Procurando atualizações...", colors.bold_yellow);

    try {
      const latestVersion = await httpsGet("https://coffeehub-rest.moonhorizon.xyz/api/latest-version");

      if (CH_VERSION === latestVersion.trim()) {
        log("[UPDATE]: Seu CoffeeHub já está atualizado.", colors.bold_green);
        return;
      }

      log(`[UPDATE]: Nova versão encontrada (v${latestVersion.trim()}).`, colors.bold_green);

      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
      });

      rl.question(`${colors.bold_yellow}[?]:${colors.reset} Deseja atualizar para versão mais recente? [s/n]: `, async (response) => {
        rl.close();

        if (!["s", "S", "y", "Y"].includes(response.trim())) {
          log("[!]: Abortando...", colors.bold_yellow);
          return;
        }

        log("[!]: Iniciando atualização...", colors.bold_yellow);

        // Inicia o spinner de atualização
        const spinnerChars = ["|", "/", "-", "\\"];
        let spinnerIndex = 0;
        const spinnerInterval = setInterval(() => {
          process.stdout.write(`\r${colors.bold_yellow}[${spinnerChars[spinnerIndex]}]:${colors.reset} Atualizando... `);
          spinnerIndex = (spinnerIndex + 1) % spinnerChars.length;
        }, 300);

        try {
          const filesData = await httpsGet(`https://coffeehub-rest.moonhorizon.xyz/api/version/${latestVersion.trim()}`);
          const { uMap } = JSON.parse(filesData);

          await saveFiles(uMap, latestVersion.trim());

          clearInterval(spinnerInterval);
          log("\n[UPDATE]: Todos os arquivos foram baixados.", colors.bold_green);

          const packageCommandsUrl = `https://coffeehub-rest.moonhorizon.xyz/api/packages/${latestVersion.trim()}`;
          try {
            const packageCommands = await httpsGet(packageCommandsUrl);
            log("[UPDATE]: Executando comandos de atualização...", colors.bold_green);

            const exec = require("child_process").exec;
            const commandList = packageCommands.trim().split("\n");
            for (const command of commandList) {
              exec(command, (err) => {
                if (err) {
                  logError(`Falha ao executar comando: ${command}`);
                }
              });
            }

            log(`[UPDATE]: Atualizado com sucesso para v${latestVersion.trim()}.`, colors.bold_green);
          } catch {
            logError("Falha ao obter comandos de atualização, mas o CoffeeHub foi atualizado.");
          }
        } catch (err) {
          clearInterval(spinnerInterval);
          logError(err.message || "Falha ao atualizar arquivos. Verifique sua conexão com a internet.");
        }
      });
    } catch (err) {
      logError("Não foi possível acessar o servidor de atualização.");
    }
  })();
} else if (args[0] === "recovery") {
  const recoveryProcess = spawn("node", ["coffee-loader/xch", "tufecAD9"], {
    stdio: "inherit",
  });

  recoveryProcess.on("close", (code) => {
    // log(`[RECOVERY]: Processo encerrado com código ${code}.`, colors.bold_green);
  });

} else if (["help", "--help", "-h", "--h"].includes(args[0])) {
  showHelp();
} else {
  logError("Comando inválido. Use 'help' para obter ajuda.");
}