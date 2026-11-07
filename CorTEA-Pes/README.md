<h1>T-TEA</h1>

<img src="resources/images/tteahardware.jpg" alt="Estrutura física do T-TEA" width="16%" align="left">

<h3>Console para Exergames de Chão Interativo</h3>
<p align="justify">Software para um console de Chão Interativo desenvolvido pelo doutorando André Bonetto Trindade e Gabriel Brunelli Pereira, orientado pelo Prof. Marcelo da Silva Hounsell (UDESC), o projeto Torre para crianças com Transtorno do Espectro Autista (T-TEA) tem o objetivo de auxiliar na terapia do processamento sensorial de autistas, utilizando uma plataforma interativa de baixo custo e móvel provida de jogos sérios.</p>
<p align="justify">O hardware é composto por projetor de vídeo, câmera webcam e computador convencionais. A webcam é um dispositivo relativamente barato e pode ser encontrado com facilidade, o que pode ser visto como fator positivo para adoção do jogo em instituições públicas.</p>
<p align="justify">Sendo que o projetor e o computador são convencionais, pode-se utilizar os que já se tem dísponíveis nas instituições. Desta forma, reutilizando equipamento, o custo final da plataforma T-TEA é significamente reduzido.</p>
<p align="justify">Estes equipamentos são instalados em uma estrutura física de montagem simples e de fácil portabilidade.</p>

<br clear="all">

## Desenvolvimento

### Requisitos

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) >= 0.11.32
- Computador com arquitetura x86-64 ou ARM.

### Instalar o uv

O uv baixa e gerencia automaticamente a versão correta do Python e as dependências do projeto.

macOS:

```bash
brew install uv
```

Windows (PowerShell):

```powershell
winget install --id=astral-sh.uv -e
```

Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Executar

Na raiz do projeto, em qualquer sistema:

```bash
uv run dev
```

Esse comando baixa a versão correta do Python, cria o `.venv`, sincroniza as dependências e inicia o T-TEA.

### Importante

No primeiro uso, permita o acesso à câmera nas configurações de privacidade do sistema.

<br clear="all">

<h1 align="center">Realização</h1>
<p align="center">
  <a href="https://github.com/larvattea"><img height="100" hspace="10" alt="image" src="https://github.com/user-attachments/assets/cd3acfdc-6d5a-45cf-a2aa-5259c1be0cb7" /></a><a href="https://github.com/larvattea"><img height="100" hspace="10" alt="image" src="https://github.com/user-attachments/assets/9b388bc5-bc1f-467a-a674-0ee4a239b9d4" /></a><a href="https://github.com/larvattea"><img height="100" hspace="10" alt="image" src="https://github.com/user-attachments/assets/e4517a7b-de3e-4c8d-baf9-2ea0326aa1e4" /></a>
</p>

