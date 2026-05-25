# ===== Carregamento de recursos =====

import pygame
from os import path
from config import DIR_FNT, DIR_SND, VOLUME_MUSICA


FONTE_G = 'fonte_g'
FONTE_M = 'fonte_m'
FONTE_P = 'fonte_p'
SOM_APITO = 'som_apito'


def carregar_recursos():
    recursos = {}

    ttf = path.join(DIR_FNT, 'PressStart2P.ttf')
    fonte = ttf if path.exists(ttf) else None
    recursos[FONTE_G] = pygame.font.Font(fonte, 56)
    recursos[FONTE_M] = pygame.font.Font(fonte, 30)
    recursos[FONTE_P] = pygame.font.Font(fonte, 13)

    recursos[SOM_APITO] = pygame.mixer.Sound(
        path.join(DIR_SND, 'apito.wav'))
    recursos[SOM_APITO].set_volume(0.5)

    # Música de fundo: recurso global do mixer, não vai no dict
    pygame.mixer.music.load(path.join(DIR_SND, 'musica.mp3'))
    pygame.mixer.music.set_volume(VOLUME_MUSICA)

    return recursos
