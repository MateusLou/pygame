# ===== Sprites do jogo =====

import math
import pygame
from config import (
    LARGURA, Y_CHAO, GRAVIDADE, VEL_PULO, RAIO_JOGADOR,
    RAIO_BOLA, RESTITUICAO_BOLA, ATRITO_BOLA, VEL_MAX_BOLA,
    INTERVALO_CHUTE, RECARGA_PODER_MS, PRETO, BRANCO, AMARELO,
)


class Jogador(pygame.sprite.Sprite):
    """Jogador "cabeçudo". A colisão é um círculo (a cabeça)."""

    def __init__(self, x, direcao, cor, controles):
        pygame.sprite.Sprite.__init__(self)

        self.raio = RAIO_JOGADOR
        self.cor = cor
        self.direcao = direcao            # +1 olha p/ direita, -1 p/ esquerda
        self.controles = controles        # dict: esquerda, direita, pular, chutar, poder

        # (x, y) é o CENTRO da cabeça
        self.x = float(x)
        self.y = float(Y_CHAO - self.raio)
        self.velx = 0
        self.vely = 0

        self.ultimo_chute = pygame.time.get_ticks()
        self.intervalo_chute = INTERVALO_CHUTE
        self.fim_anim_chute = 0

        # Recarga do poder: começa pronto (subtrai a recarga do tick inicial)
        self.intervalo_poder = RECARGA_PODER_MS
        self.ultimo_poder = pygame.time.get_ticks() - self.intervalo_poder

    def no_chao(self):
        return self.y >= Y_CHAO - self.raio - 0.5

    def pe(self):
        # Ponto do "pé", à frente e um pouco abaixo do centro da cabeça
        return (self.x + self.direcao * self.raio * 0.75,
                self.y + self.raio * 0.55)

    def pular(self):
        if self.no_chao():
            self.vely = VEL_PULO

    def chutar(self):
        agora = pygame.time.get_ticks()
        decorrido = agora - self.ultimo_chute
        if decorrido > self.intervalo_chute:
            self.ultimo_chute = agora
            self.fim_anim_chute = agora + 150
            return True
        return False

    def esta_chutando(self):
        return pygame.time.get_ticks() < self.fim_anim_chute

    def poder_pronto(self):
        agora = pygame.time.get_ticks()
        return agora - self.ultimo_poder > self.intervalo_poder

    def usar_poder(self):
        if self.poder_pronto():
            agora = pygame.time.get_ticks()
            self.ultimo_poder = agora
            self.fim_anim_chute = agora + 220
            return True
        return False

    def poder_restante_ms(self):
        agora = pygame.time.get_ticks()
        restante = self.intervalo_poder - (agora - self.ultimo_poder)
        return max(0, restante)

    def update(self):
        self.vely += GRAVIDADE
        self.x += self.velx
        self.y += self.vely

        if self.x < self.raio:
            self.x = self.raio
        if self.x > LARGURA - self.raio:
            self.x = LARGURA - self.raio

        if self.y > Y_CHAO - self.raio:
            self.y = Y_CHAO - self.raio
            self.vely = 0

    def desenhar(self, janela):
        cx, cy, r = int(self.x), int(self.y), self.raio

        # Sombra
        pygame.draw.ellipse(janela, (30, 90, 38),
                            (cx - r, Y_CHAO - 10, r * 2, 18))

        # Perninha: estende para frente quando está chutando
        fx, fy = self.pe()
        if self.esta_chutando():
            fx += self.direcao * 22
            fy += 6
        fx, fy = int(fx), int(fy)
        pygame.draw.line(janela, PRETO, (cx, int(cy + r * 0.4)), (fx, fy), 9)
        pygame.draw.circle(janela, PRETO, (fx, fy), 8)

        # Cabeçona
        pygame.draw.circle(janela, self.cor, (cx, cy), r)
        pygame.draw.circle(janela, PRETO, (cx, cy), r, 3)

        # Aro amarelo sinaliza que o poder está pronto
        if self.poder_pronto():
            pygame.draw.circle(janela, AMARELO, (cx, cy), r + 5, 3)

        # Bonezinho: faixa no topo + aba na direção em que olha
        pygame.draw.rect(janela, PRETO,
                         (cx - r + 4, cy - r, (r - 4) * 2, 14))
        if self.direcao > 0:
            pygame.draw.rect(janela, PRETO, (cx + r - 6, cy - r + 2, 20, 9))
        else:
            pygame.draw.rect(janela, PRETO,
                             (cx - r - 14, cy - r + 2, 20, 9))

        # Olho
        ex = int(cx + self.direcao * r * 0.35)
        ey = int(cy - r * 0.05)
        pygame.draw.circle(janela, BRANCO, (ex, ey), 9)
        pygame.draw.circle(janela, PRETO, (ex + self.direcao * 3, ey), 4)


class Bola(pygame.sprite.Sprite):
    """Bola: gravidade, quica nas paredes/chão e bate na cabeça do jogador."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.raio = RAIO_BOLA
        self.reiniciar()

    def reiniciar(self):
        self.x = LARGURA / 2
        self.y = Y_CHAO - 220
        self.velx = 0.0
        self.vely = 0.0

    def limitar_velocidade(self):
        v = math.hypot(self.velx, self.vely)
        if v > VEL_MAX_BOLA:
            f = VEL_MAX_BOLA / v
            self.velx *= f
            self.vely *= f

    def update(self):
        self.vely += GRAVIDADE
        self.velx *= ATRITO_BOLA
        self.x += self.velx
        self.y += self.vely

        # Quica no chão
        if self.y > Y_CHAO - self.raio:
            self.y = Y_CHAO - self.raio
            self.vely = -self.vely * RESTITUICAO_BOLA
            self.velx *= 0.98

        # Quica no teto
        if self.y < self.raio:
            self.y = self.raio
            self.vely = -self.vely * RESTITUICAO_BOLA

        self.limitar_velocidade()

    def desenhar(self, janela):
        cx, cy, r = int(self.x), int(self.y), self.raio

        pygame.draw.ellipse(janela, (30, 90, 38),
                            (cx - r, Y_CHAO - 7, r * 2, 10))

        pygame.draw.circle(janela, BRANCO, (cx, cy), r)
        pygame.draw.circle(janela, PRETO, (cx, cy), r, 2)
        for ang in range(0, 360, 72):
            px = int(cx + r * 0.5 * math.cos(math.radians(ang)))
            py = int(cy + r * 0.5 * math.sin(math.radians(ang)))
            pygame.draw.circle(janela, PRETO, (px, py), 3)
