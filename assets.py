# ===== Carregamento de recursos =====

import os
import pygame
from config import DIR_FNT, DIR_SND


FONTE_G = 'fonte_g'
FONTE_M = 'fonte_m'
FONTE_P = 'fonte_p'
SOM_APITO = 'som_apito'


def carregar_recursos():
    recursos = {}

    ttf = os.path.join(DIR_FNT, 'PressStart2P.ttf')
    recursos[FONTE_G] = pygame.font.Font(ttf, 56)
    recursos[FONTE_M] = pygame.font.Font(ttf, 30)
    recursos[FONTE_P] = pygame.font.Font(ttf, 13)

    recursos[SOM_APITO] = pygame.mixer.Sound(
        os.path.join(DIR_SND, 'apito.wav'))
    recursos[SOM_APITO].set_volume(0.5)

    return recursos
