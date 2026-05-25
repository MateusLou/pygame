# Head Soccer - 2 Players

Jogo de futebol de cabeça para dois jogadores no mesmo teclado, feito em Python com Pygame.

## Integrantes

- Mateus Loureiro
- Francisco Chebib
- Victor Benneti

## Vídeo de apresentação

https://youtu.be/WjJgSuL07iU

## Descrição

Head Soccer é uma releitura simples do clássico jogo de futebol de cabeçudos. Dois jogadores disputam uma partida de 2 minutos: cada um controla um boneco que pode andar, pular e chutar a bola, tentando marcar gol no adversário. A bola tem física própria (gravidade, atrito e quique), e cada jogador tem um "poder especial" — um chute reforçado — que recarrega a cada 30 segundos. Ao final do tempo, vence quem tiver mais gols.

## Controles

| Ação      | Jogador 1 (azul) | Jogador 2 (vermelho) |
|-----------|------------------|----------------------|
| Esquerda  | A                | Seta esquerda        |
| Direita   | D                | Seta direita         |
| Pular     | W                | Seta para cima       |
| Chutar    | S                | Seta para baixo      |
| Poder     | Shift esquerdo   | Shift direito        |

Durante a tela final: `ENTER` recomeça a partida, `ESC` encerra o jogo.

## Instalação das dependências

O projeto usa apenas o Pygame. Recomenda-se Python 3.10 ou superior.

```bash
pip install pygame
```

Se preferir usar um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install pygame
```

## Como rodar o jogo

A partir da pasta raiz do projeto, execute:

```bash
python headsoccer.py
```


## Estrutura do projeto

- `headsoccer.py` — ponto de entrada e máquina de estados da aplicação.
- `game_screen.py` — loop principal da partida, física de colisão e desenho do campo.
- `sprites.py` — classes `Jogador` e `Bola`.
- `config.py` — constantes de tela, física, tempos e cores.
- `assets.py` — carregamento de fontes e sons.
- `assets/` e `referencia/assets/` — sons e fontes usados no jogo.
