# CorTEA

Exergame da plataforma T-TEA para crianças com TEA, baseado no artigo
*"CorTea: Proposta de um Exergame para Crianças com Transtorno do Espectro
Autista"* (IFSC Jaraguá do Sul, Projeto Integrador I, 2026).

## Como se joga

1. O sistema mostra uma grade 4x3 de quadrados coloridos.
2. Um **caminho** de quadrados vizinhos (da linha de baixo até a de cima) é
   exibido aceso, um quadrado de cada vez, cada um com uma nota musical.
3. O jogador reproduz o caminho com a mão (webcam) ou com o mouse. Pela
   webcam, basta **manter a mão parada** sobre o quadrado por ~0,7 s: o anel
   ao redor do quadrado vai se completando. Só atravessar a grade com a mão
   não conta como erro.
4. Todos os quadrados do caminho têm a mesma cor (a cor aparece no círculo
   de baixo). Nas fases avançadas há quadrados "isca" da mesma cor fora do
   caminho, então é preciso lembrar a **ordem** exibida.
5. Cada fase tem 2 caminhos. Ao fim, o **índice de desempenho** decide:
   - `ID = (A x 2) - (E x 1) + (C x 1,5)` (Equação 1 do artigo; A = acertos,
     E = erros, C = maior sequência de acertos seguidos);
   - se `ID >= 60%` do ID máximo da fase, avança (ícones verdes, som de
     conquista, +1 ajuda); senão, repete a mesma fase (ícones escuros e
     mensagem "Vamos tentar de novo!").
6. Errar nunca tira pontos nem mostra mensagem de punição. Se o jogador
   ficar parado por 6 s, o próximo quadrado pisca (usa 1 das 3 ajudas, com
   custo pequeno de pontos).
7. Depois da fase 8, aparece a tela de conclusão (pontos, tempo total,
   tempo médio).

## Controles

| Tecla | Função |
|-------|--------|
| ESC | Pausar / continuar / voltar |
| ENTER ou ESPAÇO | Iniciar, continuar ou reiniciar |
| C | Abre/fecha a janela da webcam, separada do jogo (mostra as mãos detectadas e a área útil em verde) |
| E | Liga/desliga o espelhamento da webcam (`espelhar_camera` no `cortea.ini`) |
| H | Painel do terapeuta (acertos, erros, ID, ajudas, tempo) |
| M | Liga/desliga o som |
| F11 | Tela cheia (use no projetor) |

Menu de pausa: Continuar, Retroceder, Avançar (muda de fase), Sair (pede
confirmação), Som e volume. Os botões também funcionam com a mão.

O botão Sair (da pausa e da tela de conclusão) salva a sessão e volta para a
tela inicial; o jogo só fecha pelo X da janela.

## Execução

```bash
uv run dev        # pela plataforma T-TEA
# ou, direto (opções: --lang pt_BR --player_id 1 --phase 3 --camera 0):
uv run python src/ttea/games/CorTEA/cortea.py
```

Sem webcam (ou sem MediaPipe) o jogo funciona só com o mouse.

Os relatórios CSV ficam na pasta de exportações da plataforma
(`relatorio_cortea_<id_jogador>_<data>.csv`), com os campos da Tabela 2 do
artigo (`id_sessao;nome_usuario;data_hora;acertos;erros;
acertos_consecutivos;fase;tempo_medio_resposta`), uma linha por tentativa de
fase. O arquivo é regravado a cada tentativa, então nada se perde se o jogo
fechar.

## Configuração (`cortea.ini`)

Fase inicial, rodadas por fase, fração mínima do ID, tempo limite da rodada,
ajudas, tempo de permanência da mão, ponto da mão (`palma` ou `indicador`),
som. A tabela de fases (tamanho do caminho, velocidade, nº de cores, iscas)
fica em `gameutil/gamesettings.py` (`GameSettings.FASES`).

## Estrutura (diagrama de classes do artigo → código)

| Classe do artigo | Código |
|------------------|--------|
| SistemaCorTea | `gamecontroller/gamecontroller.py` (`GameController`) + `cortea.py` |
| Sessao, Usuario | `gamemodel/sessao.py` |
| Atividade | `gamemodel/atividade.py` |
| SistemaAjuda | `gamemodel/sistemaajuda.py` |
| Desempenho | `gamemodel/desempenho.py` |
| Rastreamento | `gamecore/rastreamento.py` (thread: webcam + MediaPipe) |
| GerenciadorCSV | `gameutil/gerenciadorcsv.py` |
| (extra) seleção por permanência | `gamecore/seletor.py` |
| (extra) janela da webcam | `gamecore/janelacamera.py` |
| (extra) fundo 3D animado da tela inicial | `gameview/fundoinicio.py` |
| (extra) ícone (`CorTea.ico` / `.png`) e o script que o gera | `resources/icons/gerar_icone.py` |
| (extra) sons gerados por código | `gamecore/audio.py` |
| (extra) textos pt_BR / en_US / es_ES | `gameutil/textos.py` |

## Requisitos do artigo

| Requisito | Situação |
|-----------|----------|
| RF01 iniciar sessão | Feito (jogador/idioma/fase vêm da plataforma; botão Jogar) |
| RF02 grade projetada | Feito na tela; para o projetor, F11 numa saída de vídeo do projetor |
| RF03 sequências de cores | Feito (caminho aceso em ordem) |
| RF04 e RF05 movimento e posição por visão computacional | Feito para as **mãos**; falta calibração câmera→projetor e pés |
| RF06 validar sequência | Feito |
| RF07 e RF08 feedback e reforço positivo | Feito (visual, sonoro, pontos, +1 ajuda) |
| RF09 e RF12 ajuste automático / manter na fase | Feito (ID mínimo) |
| RF10, RF11 e RF14 registro e CSV | Feito |
| RF13 encerrar sessão | Feito (com confirmação e salvamento) |
| RNF01 feedback < 1 s | Feedback imediato após a seleção (a seleção em si leva 0,7 s de permanência) |
| RNF03 sem dispositivos físicos | Feito |
| RNF04 sessão contínua de 60 min | CSV incremental e sem acúmulo de dados; **ainda não testado por 60 min reais** |
| RNF06 Windows 10 | Backend DirectShow para a webcam; **testar no Windows** |
| RNF08 versões (Python 3.8.3, Pygame 2.1.2, OpenCV 4.5.4.60, Pandas 1.5.1) | **Diferente do repositório**: ele usa Python >= 3.10, Pygame 2.6.1, OpenCV 4.11 e não usa Pandas. O código segue o `pyproject.toml` da plataforma |
| RN03 a RN05 ABA, sem punição, sem sobrecarga | Sem perda de pontos por erro, feedback neutro, sons suaves |
| RN08 deslocamento físico | Mãos agora; pés é o próximo passo |

## Testes

```bash
uv run python -m unittest tests.test_cortea
```

Cobrem o gerador de caminhos, a Equação 1, as ajudas, a seleção por
permanência, o CSV, o fluxo completo das 8 fases, a pausa, o desenho de todas
as telas e a classe principal (mouse, teclado, mão e webcam simuladas).
