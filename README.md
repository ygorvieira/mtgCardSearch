# 🃏 mtgCardSearch

Um buscador de cartas de **Magic: The Gathering (MTG)** direto no terminal, utilizando a API oficial do **Scryfall**. Este projeto foi desenvolvido e otimizado para rodar em ambientes minimalistas e de baixo consumo de recursos, como o **Raspberry Pi 3** rodando o **Alpine OS (Alpine Linux)**.

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura no Raspberry Pi 3 + Alpine](#-arquitetura-no-raspberry-pi-3--alpine)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
  - [Método 1: Usando pacotes nativos do Alpine (Recomendado)](#método-1-usando-pacotes-nativos-do-alpine-recomendado)
  - [Método 2: Usando Ambiente Virtual (venv + pip)](#método-2-usando-ambiente-virtual-venv--pip)
- [Como Usar](#-como-usar)
- [Funcionalidades](#-funcionalidades)
- [Dicas de Desempenho e Solução de Problemas no Alpine](#-dicas-de-desempenho-e-solução-de-problemas-no-alpine)

---

## 🔍 Sobre o Projeto

O `mtgCardSearch` é uma ferramenta CLI (Interface de Linha de Comando) simples e rápida. Ela consome o endpoint de busca aproximada (fuzzy search) do Scryfall para obter informações detalhadas sobre cartas de Magic, incluindo:
- Atributos básicos (custo de mana, tipo, raridade, coleção).
- Descrição oficial da carta (Oracle Text).
- Poder e Resistência (se aplicável).
- Formatos de jogo nos quais a carta é válida (Legalities).
- Regras e anotações oficiais de juízes (Rulings).

---

## 🛠️ Arquitetura no Raspberry Pi 3 + Alpine

Rodar aplicações em hardware limitado como o **Raspberry Pi 3** requer eficiência. O **Alpine Linux** é a escolha ideal para isso devido ao seu tamanho extremamente reduzido, uso de biblioteca `musl libc` e gerenciador de pacotes ultra veloz (`apk`).

Para manter o consumo de memória RAM sob controle e evitar compilações demoradas no Raspberry Pi, a instalação ideal deste projeto faz uso de pacotes Python pré-compilados fornecidos diretamente pelos repositórios do Alpine.

---

## 📌 Pré-requisitos

Antes de iniciar, certifique-se de que o seu Raspberry Pi tem:
1. **Alpine Linux** instalado e configurado.
2. Conexão ativa com a internet (necessária para consultar a API do Scryfall).
3. Acesso à conta de superusuário (`root` ou privilégios de `sudo`).

---

## 🚀 Instalação

Como o Alpine Linux preza pela estabilidade e leveza, você tem duas abordagens principais para instalar as dependências de rede necessárias (`requests`):

### Método 1: Usando pacotes nativos do Alpine (Recomendado)

Esta é a abordagem mais rápida e eficiente para o Raspberry Pi 3. Em vez de baixar o `pip` e compilar/instalar dependências na memória, instalamos a biblioteca `requests` pré-compilada direto do gerenciador `apk`.

1. Atualize o repositório de pacotes do Alpine:
   ```bash
   sudo apk update
   ```

2. Instale o Python 3 e a biblioteca `requests` nativa:
   ```bash
   sudo apk add python3 py3-requests
   ```

Pronto! As dependências estão instaladas de forma global e com performance otimizada para o sistema.

---

### Método 2: Usando Ambiente Virtual (venv + pip)

Se preferir isolar o projeto em um ambiente Python específico (`venv`), siga os passos abaixo. *Nota: Este processo pode demorar um pouco mais para inicializar no RPi 3 devido à criação dos diretórios isolados.*

1. Instale o Python 3, o gerenciador de pacotes `pip` e ferramentas básicas:
   ```bash
   sudo apk add python3 py3-pip
   ```

2. Crie o ambiente virtual dentro do diretório do projeto:
   ```bash
   python3 -m venv .venv
   ```

3. Ative o ambiente virtual:
   ```bash
   source .venv/bin/activate
   ```

4. Instale a biblioteca `requests`:
   ```bash
   pip install requests
   ```

*(Lembre-se de sempre ativar o ambiente virtual com `source .venv/bin/activate` antes de rodar o script usando este método).*

---

## 💻 Como Usar

O script recebe o nome da carta diretamente como argumento de linha de comando.

1. **Execução direta com Python**:
   ```bash
   python3 mtgCardSearch.py "Black Lotus"
   ```

2. **Tornando o script executável**:
   Você pode dar permissão de execução ao script para rodá-lo como um utilitário nativo:
   ```bash
   chmod +x mtgCardSearch.py
   ```
   E rodar diretamente:
   ```bash
   ./mtgCardSearch.py "Lightning Bolt"
   ```

### Exemplos de Busca

- Cartas com nomes compostos ou espaços (use aspas):
  ```bash
  ./mtgCardSearch.py "Jace, the Mind Sculptor"
  ```
- Buscas aproximadas (fuzzy search):
  ```bash
  ./mtgCardSearch.py "sol ring"
  ```

---

## ✨ Funcionalidades

- **Fuzzy Search**: Encontra a carta correta mesmo se você digitar o nome parcialmente ou com pequenas variações.
- **Formatação de Saída Clara**: Informações organizadas no terminal por meio de separadores visuais.
- **Rulings Integrados**: Exibe as últimas 5 regras da carta para tirar dúvidas rápidas durante as partidas.
- **Baixo Overhead**: Consumo de RAM inferior a 15MB durante a execução no Alpine OS.

---

## 💡 Dicas de Desempenho e Solução de Problemas no Alpine

### ⚠️ Ajustes e Correções no Código
Caso você encontre problemas ao rodar o script no Alpine Linux, verifique se a linha do `shebang` (a primeira linha do arquivo) está apontando para o interpretador correto:
- O padrão em alguns sistemas é `#!/usr/bin/env python3`. Verifique se não há erros de digitação como `pyython3` no cabeçalho do arquivo `mtgCardSearch.py`.

### 🌐 Resolução de DNS no Alpine
O Alpine OS utiliza a biblioteca `musl libc` no lugar da tradicional `glibc`. Em alguns cenários raros no Raspberry Pi, a resolução de nomes de DNS pode falhar ao consultar a API externa. Caso receba erros de conexão, verifique se o seu arquivo `/etc/resolv.conf` está configurado com um DNS válido (como o do Google `8.8.8.8` ou Cloudflare `1.1.1.1`).

### 🔒 User-Agent na API
A API do Scryfall exige que as requisições enviem um cabeçalho `User-Agent` descritivo e limpo para evitar bloqueios de taxa de requisição (Rate Limit). O script já está configurado com `User-Agent: mtg-cli-app/1.0`, garantindo a conformidade com as diretrizes do Scryfall.
