# ===== Inicialização =====
import pygame
from config import LARGURA, ALTURA, JOGO, SAIR
from game_screen import tela_jogo


pygame.init()
pygame.mixer.init()

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Head Soccer - 2 Players')

# ===== Máquina de estados =====
estado = JOGO
while estado != SAIR:
    if estado == JOGO:
        estado = tela_jogo(janela)
    else:
        estado = SAIR

pygame.quit()
