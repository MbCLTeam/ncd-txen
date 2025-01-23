const fs = require('fs');
const readline = require('readline');
const { spawn } = require('child_process');

// Versão da aplicação e controle do conteúdo beta
const CH_VERSION = '1.3.0';
const BETA_CONTENT = `${CH_VERSION}/BETA-COFFEEHUB-FILE_XD3EKC99VB7`;

// Códigos ANSI para cores e estilos
const COLORS = {
  RESET: '\x1b[0m',
  BOLD_YELLOW: '\x1b[1;33m',
  DARK_YELLOW: '\x1b[33m',
  WHITE: '\x1b[37m',
  BLUE_BG: '\x1b[44m',
  BLACK_BG: '\x1b[40m',
};

let menuOptions = ['Iniciar sistema', 'Limpar Key', 'Reparar CoffeeHub', 'Sair'];
let selectedIndex = 0;
const betaFilePath = './beta/ch.beta';
const betaFolderPath = './beta';
let betaMessage = '';
let messageTimeout;
let betaOptionVisible = true; // Controla se a opção de desbloquear a beta deve ser visível
let isRepairing = false; // Controle de estado de reparo para desabilitar o menu enquanto está reparando

// Verifica se o conteúdo beta já está habilitado e válido
let betaEnabled = fs.existsSync(betaFilePath) && fs.readFileSync(betaFilePath, 'utf-8').trim() === BETA_CONTENT;
if (betaEnabled) {
  menuOptions.splice(1, 0, 'Desabilitar conteúdo beta'); // Insere no índice correto
  betaOptionVisible = false; // Esconde a opção de desbloquear após ativar
}

// Variáveis para detectar 5 pressionamentos da tecla 'C'
let cPresses = [];
const MAX_C_TIME = 2000; // 2 segundos

// Cria interface de leitura
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: true,
});

// Função para exibir o menu
function displayMenu() {
  console.clear();
  console.log(`${COLORS.BOLD_YELLOW}CoffeeHub Recovery${COLORS.RESET}`);
  console.log(`${COLORS.DARK_YELLOW}coffeehub/${CH_VERSION}/recovery${COLORS.RESET}`);
  console.log(`${COLORS.DARK_YELLOW}NEXT.C0FF33HUB-releases/global.br${COLORS.RESET}`);
  console.log(`${COLORS.DARK_YELLOW}coffee-loader/bios-recovery/1.1${COLORS.RESET}`);
  console.log(`${COLORS.DARK_YELLOW}Teclas: cima/baixo e enter${COLORS.RESET}`);
  console.log('');

  menuOptions.forEach((option, index) => {
    if (index === selectedIndex) {
      console.log(`${COLORS.BLUE_BG}${COLORS.WHITE} ${option} ${COLORS.RESET}`);
    } else {
      console.log(`${COLORS.BLACK_BG}${COLORS.WHITE} ${option} ${COLORS.RESET}`);
    }
  });

  // Exibe mensagem abaixo do menu, se houver
  if (betaMessage) {
    console.log('\n');
    console.log(`${COLORS.DARK_YELLOW}${betaMessage}${COLORS.RESET}`);
  }
}

// Função para exibir mensagem temporária
function showMessage(message) {
  betaMessage = message;
  displayMenu();
  clearTimeout(messageTimeout);
  messageTimeout = setTimeout(() => {
    betaMessage = '';
    displayMenu();
  }, 5000);
}

// Função para reparar o CoffeeHub
function repairCoffeeHub() {
  showMessage("Iniciando reparo...");

  // Desabilita o menu enquanto está reparando
  isRepairing = true;
  menuOptions = []; // Remove as opções do menu

  const repairProcess = spawn('npm', ['i', '--no-bin-links'], { stdio: 'ignore' });

  repairProcess.on('exit', (code) => {
    isRepairing = false;
    if (code === 0) {
      showMessage('CoffeeHub possivelmente reparado, tente rodar normalmente.');
    } else {
      showMessage('Não foi possível reparar o CoffeeHub, tente mais tarde');
    }

    // Reabilita o menu após o reparo
    menuOptions = ['Iniciar sistema', 'Limpar Key', 'Reparar CoffeeHub', 'Sair'];
    if (betaEnabled) {
      menuOptions.splice(1, 0, 'Desabilitar conteúdo beta'); // Insere no índice correto se beta estiver habilitado
    }
    displayMenu();
  });
}

// Função para manipular ações
function handleAction() {
  const selectedOption = menuOptions[selectedIndex];

  switch (selectedOption) {
    case 'Iniciar sistema':
      console.clear();
      console.log('Iniciando o sistema...');
      rl.close(); // Fecha a interface de leitura
      process.stdin.setRawMode(false); // Desativa o modo raw para capturar teclas
      const child = spawn('node', ['app'], { stdio: 'inherit' });

      // Encerra o processo atual ao fechar o app
      child.on('exit', (code) => {
      //  console.log(`Sistema encerrado com código ${code}.`);
        process.exit(0);
      });
      break;

    case 'Limpar Key':
      try {
        fs.writeFileSync('./KEY.txt', ''); // Limpa ou cria o arquivo
        showMessage('Key resetada com sucesso');
      } catch (err) {
        showMessage('Erro ao manipular KEY.txt');
      }
      break;

    case 'Reparar CoffeeHub':
      if (!isRepairing) {
        repairCoffeeHub();
      }
      break;

    case 'Desabilitar conteúdo beta':
      try {
        if (fs.existsSync(betaFilePath)) {
          fs.unlinkSync(betaFilePath);
        }
        if (fs.existsSync(betaFolderPath)) {
          fs.rmdirSync(betaFolderPath, { recursive: true });
        }
        betaEnabled = false;
        menuOptions = menuOptions.filter((opt) => opt !== 'Desabilitar conteúdo beta');
        showMessage('Conteúdo beta desabilitado com sucesso');
        betaOptionVisible = true; // Reabilita a opção de ativar a beta
      } catch (err) {
        showMessage('Erro ao desabilitar conteúdo beta');
      }
      break;

    case 'Desbloquear funções beta (Instável)':
      try {
        if (!fs.existsSync(betaFolderPath)) {
          fs.mkdirSync(betaFolderPath, { recursive: true });
        }
        fs.writeFileSync(betaFilePath, BETA_CONTENT);
        betaEnabled = true;
        menuOptions.splice(1, 0, 'Desabilitar conteúdo beta'); // Insere no índice correto
        menuOptions = menuOptions.filter((opt) => opt !== 'Desbloquear funções beta (Instável)');
        showMessage('Funções beta ativadas com sucesso');
      } catch (err) {
        showMessage('Não foi possível desbloquear as funções beta');
      }
      break;

    case 'Sair':
      console.clear();
      // console.log('Sistema desligado.');
      rl.close();
      process.exit(0);
      break;

    default:
      console.log('Ação desconhecida.');
      break;
  }

  if (selectedOption !== 'Iniciar sistema') setTimeout(displayMenu, 1000);
}

// Manipula a navegação do menu
function handleKeyPress(_, key) {
  const now = Date.now();

  if (key.name === 'up') {
    selectedIndex = (selectedIndex - 1 + menuOptions.length) % menuOptions.length;
  } else if (key.name === 'down') {
    selectedIndex = (selectedIndex + 1) % menuOptions.length;
  } else if (key.name === 'return') {
    handleAction();
  } else if (key.name === 'c') {
    // Registro de pressionamento da tecla C
    cPresses.push(now);
    cPresses = cPresses.filter((time) => now - time < MAX_C_TIME); // Remove pressionamentos antigos

    if (cPresses.length >= 5 && betaOptionVisible) {
      if (!menuOptions.includes('Desbloquear funções beta (Instável)')) {
        menuOptions.splice(1, 0, 'Desbloquear funções beta (Instável)'); // Adiciona a opção no índice correto
      }
      betaOptionVisible = false; // Evita reaparecer a opção
      displayMenu();
    }
  } else if (key.name === 'escape') {
    console.clear();
    rl.close();
    process.exit(0);
  }

  displayMenu();
}

// Captura o evento de Ctrl+C para limpar o console e sair
process.on('SIGINT', () => {
  console.clear();
  rl.close();
  process.exit(0);
});

// Configura eventos para capturar teclas
readline.emitKeypressEvents(process.stdin);
if (process.stdin.isTTY) {
  process.stdin.setRawMode(true);
}

process.stdin.on('keypress', handleKeyPress);

// Exibe o menu inicial
displayMenu();