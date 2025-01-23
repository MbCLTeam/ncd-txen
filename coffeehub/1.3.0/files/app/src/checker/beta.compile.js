#!/bin/coffeehub.js
require("../../").global();
/**
 * Compile: false
**/

// Variável 'b' e mapeamento
let b;
spawn.b(compile);

set.defaults = [
    'x86',
    'x64',
    'nodejs',
    'env.node'
];

// Carregar as configurações padrão
load d from set.defaults;
const compile = d.loadMap();

// Executar o script de compilação
compile.script(`./coffeehub --compile ${u.sys} ${this.platform} -node-mem 512M --no-cache`);