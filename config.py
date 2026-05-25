# ===== Configurações gerais do jogo =====

from os import path

DIR_FNT = path.join(path.dirname(__file__), 'assets', 'font')
DIR_SND = path.join(path.dirname(__file__), 'assets', 'snd')

# ----- Tela
LARGURA = 1000
ALTURA = 560
FPS = 60

# ----- Campo
ALTURA_CHAO = 70
Y_CHAO = ALTURA - ALTURA_CHAO
ALTURA_GOL = 190
LARGURA_GOL = 26
ESPESSURA_TRAVE = 10

# ----- Física (valores por frame, pensados para FPS = 60)
GRAVIDADE = 0.8
VEL_JOGADOR = 6
VEL_PULO = -16
RAIO_JOGADOR = 46

RAIO_BOLA = 15
RESTITUICAO_BOLA = 0.72
ATRITO_BOLA = 0.992
VEL_MAX_BOLA = 23

FORCA_CHUTE = 16
ALTURA_CHUTE = 11
ALCANCE_CHUTE = 82
INTERVALO_CHUTE = 280

# ----- Poder especial (chute forte)
RECARGA_PODER_MS = 30000
FORCA_CHUTE_PODER = 28
ALTURA_CHUTE_PODER = 17

# ----- Tempos da partida
CONTAGEM_MS = 3000
PARTIDA_MS = 120000
PAUSA_GOL_MS = 1600

# ----- Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (231, 76, 60)
AZUL = (52, 152, 219)
VERDE = (46, 139, 56)
VERDE_ESCURO = (38, 115, 47)
AMARELO = (241, 196, 15)
CEU = (135, 206, 235)
REDE = (210, 210, 210)

# ----- Estados do fluxo da aplicação
JOGO = 1
SAIR = 2
