# ===== Tela de jogo =====

import math
import pygame
from config import (
    FPS, LARGURA, ALTURA, Y_CHAO, ALTURA_GOL, LARGURA_GOL, ESPESSURA_TRAVE,
    VEL_JOGADOR, FORCA_CHUTE, ALTURA_CHUTE, ALCANCE_CHUTE, RESTITUICAO_BOLA,
    FORCA_CHUTE_PODER, ALTURA_CHUTE_PODER,
    CONTAGEM_MS, PARTIDA_MS, PAUSA_GOL_MS,
    BRANCO, PRETO, VERMELHO, AZUL, VERDE, VERDE_ESCURO, AMARELO, CEU, REDE,
    JOGO, SAIR,
)
from assets import carregar_recursos, FONTE_G, FONTE_M, FONTE_P, SOM_APITO
from sprites import Jogador, Bola


def _resolver_colisao_jogador(bola, jogador):
    """Colisão círculo-círculo entre a bola e a cabeça do jogador."""
    dx = bola.x - jogador.x
    dy = bola.y - jogador.y
    dist = math.hypot(dx, dy)
    dist_min = bola.raio + jogador.raio
    if dist == 0 or dist >= dist_min:
        return

    nx, ny = dx / dist, dy / dist
    bola.x = jogador.x + nx * dist_min
    bola.y = jogador.y + ny * dist_min

    rvx = bola.velx - jogador.velx
    rvy = bola.vely - jogador.vely
    vn = rvx * nx + rvy * ny
    if vn < 0:
        j = -(1 + RESTITUICAO_BOLA) * vn
        bola.velx = bola.velx + j * nx + jogador.velx * 0.6
        bola.vely = bola.vely + j * ny + jogador.vely * 0.6 - 1.5
        bola.limitar_velocidade()


def _aplicar_chute(bola, jogador, potencia=False):
    """Se a bola estiver no alcance do pé, aplica chute direcionado.

    Quando `potencia=True`, usa os valores reforçados do poder especial.
    Retorna True se o chute foi efetivamente aplicado.
    """
    fx, fy = jogador.pe()
    if math.hypot(bola.x - fx, bola.y - fy) <= ALCANCE_CHUTE + bola.raio:
        if potencia:
            bola.velx = jogador.direcao * FORCA_CHUTE_PODER + jogador.velx * 0.5
            bola.vely = -ALTURA_CHUTE_PODER
        else:
            bola.velx = jogador.direcao * FORCA_CHUTE + jogador.velx * 0.5
            bola.vely = -ALTURA_CHUTE
        bola.limitar_velocidade()
        return True
    return False


def _desenhar_gol(janela, lado):
    """Desenha um gol (lado = 'L' esquerda, 'R' direita)."""
    topo = Y_CHAO - ALTURA_GOL
    x0 = 0 if lado == 'L' else LARGURA - LARGURA_GOL

    # Rede
    for gx in range(x0, x0 + LARGURA_GOL + 1, 8):
        pygame.draw.line(janela, REDE, (gx, topo), (gx, Y_CHAO), 1)
    for gy in range(topo, Y_CHAO + 1, 8):
        pygame.draw.line(janela, REDE, (x0, gy), (x0 + LARGURA_GOL, gy), 1)

    # Travessão
    pygame.draw.rect(janela, BRANCO,
                     (x0, topo - ESPESSURA_TRAVE, LARGURA_GOL, ESPESSURA_TRAVE))
    pygame.draw.rect(janela, PRETO,
                     (x0, topo - ESPESSURA_TRAVE, LARGURA_GOL, ESPESSURA_TRAVE), 2)


def _desenhar_campo(janela):
    janela.fill(CEU)
    pygame.draw.rect(janela, VERDE,
                     (0, Y_CHAO - 90, LARGURA, ALTURA - (Y_CHAO - 90)))
    for i in range(0, LARGURA, 80):
        cor = VERDE_ESCURO if (i // 80) % 2 == 0 else VERDE
        pygame.draw.rect(janela, cor, (i, Y_CHAO, 80, ALTURA - Y_CHAO))
    pygame.draw.line(janela, BRANCO, (0, Y_CHAO), (LARGURA, Y_CHAO), 3)
    pygame.draw.line(janela, BRANCO, (LARGURA // 2, Y_CHAO - 90),
                     (LARGURA // 2, Y_CHAO), 2)
    pygame.draw.circle(janela, BRANCO, (LARGURA // 2, Y_CHAO), 60, 2)


def _texto(janela, fonte, txt, cor, centro):
    """Renderiza texto centralizado em `centro`."""
    s = fonte.render(txt, True, cor)
    r = s.get_rect()
    r.center = centro
    janela.blit(s, r)


def tela_jogo(janela):
    relogio = pygame.time.Clock()
    recursos = carregar_recursos()

    # ----- Cria jogadores, bola e grupo de sprites
    p1 = Jogador(LARGURA * 0.28, +1, AZUL, {
        'esquerda': pygame.K_a, 'direita': pygame.K_d,
        'pular': pygame.K_w, 'chutar': pygame.K_s,
        'poder': pygame.K_LSHIFT,
    })
    p2 = Jogador(LARGURA * 0.72, -1, VERMELHO, {
        'esquerda': pygame.K_LEFT, 'direita': pygame.K_RIGHT,
        'pular': pygame.K_UP, 'chutar': pygame.K_DOWN,
        'poder': pygame.K_RSHIFT,
    })
    bola = Bola()
    jogadores = [p1, p2]

    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(p1)
    todos_sprites.add(p2)
    todos_sprites.add(bola)

    placar = [0, 0]

    # Sub-estados da partida
    CONTAGEM, JOGANDO, GOL, FIM, ENCERRAR = 0, 1, 2, 3, 4
    estado = CONTAGEM
    saida = JOGO

    tempo_jogado_ms = 0
    tick_partida = pygame.time.get_ticks()
    fase_tick = pygame.time.get_ticks()
    quem_fez_gol = 0
    teclas_pressionadas = {}

    # ===== Loop principal =====
    while estado != ENCERRAR:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()

        # Relógio só anda em JOGANDO
        if estado == JOGANDO:
            tempo_restante = max(0, PARTIDA_MS
                                 - (tempo_jogado_ms + (agora - tick_partida)))
        else:
            tempo_restante = max(0, PARTIDA_MS - tempo_jogado_ms)

        # ----- Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado = ENCERRAR
                saida = SAIR

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = ENCERRAR
                    saida = SAIR

                if estado in (CONTAGEM, JOGANDO):
                    teclas_pressionadas[evento.key] = True
                    for p in jogadores:
                        if evento.key == p.controles['esquerda']:
                            p.velx -= VEL_JOGADOR
                        if evento.key == p.controles['direita']:
                            p.velx += VEL_JOGADOR
                        if evento.key == p.controles['pular']:
                            p.pular()
                        if (evento.key == p.controles['chutar']
                                and estado == JOGANDO):
                            if p.chutar():
                                _aplicar_chute(bola, p)
                        if (evento.key == p.controles['poder']
                                and estado == JOGANDO):
                            # Só consome o poder se a bola estava no alcance
                            if (p.poder_pronto()
                                    and _aplicar_chute(bola, p, potencia=True)):
                                p.usar_poder()

                if estado == FIM:
                    if evento.key in (pygame.K_RETURN, pygame.K_r,
                                      pygame.K_SPACE):
                        estado = ENCERRAR
                        saida = JOGO
                    if evento.key == pygame.K_q:
                        estado = ENCERRAR
                        saida = SAIR

            if evento.type == pygame.KEYUP:
                if (evento.key in teclas_pressionadas
                        and teclas_pressionadas[evento.key]):
                    teclas_pressionadas[evento.key] = False
                    for p in jogadores:
                        if evento.key == p.controles['esquerda']:
                            p.velx += VEL_JOGADOR
                        if evento.key == p.controles['direita']:
                            p.velx -= VEL_JOGADOR

        # ----- Atualiza estado
        todos_sprites.update()

        if estado == CONTAGEM:
            # Bola congelada no centro até o "vai"
            bola.x, bola.y = LARGURA / 2, Y_CHAO - 220
            bola.velx = bola.vely = 0
            if agora - fase_tick >= CONTAGEM_MS:
                estado = JOGANDO
                fase_tick = agora
                tick_partida = agora
                recursos[SOM_APITO].play()

        elif estado == JOGANDO:
            for p in jogadores:
                _resolver_colisao_jogador(bola, p)

            topo = Y_CHAO - ALTURA_GOL

            # Travessão dos dois gols
            for x0 in (0, LARGURA - LARGURA_GOL):
                dentro_x = x0 <= bola.x <= x0 + LARGURA_GOL
                if (dentro_x
                        and topo - ESPESSURA_TRAVE - bola.raio <= bola.y <= topo + bola.raio):
                    if bola.y < topo - ESPESSURA_TRAVE / 2:
                        bola.y = topo - ESPESSURA_TRAVE - bola.raio
                    else:
                        bola.y = topo + bola.raio
                    bola.vely = -bola.vely * RESTITUICAO_BOLA

            # Paredes: só quicam ACIMA da boca do gol; dentro vira gol
            if bola.x < bola.raio:
                if bola.y < topo:
                    bola.x = bola.raio
                    bola.velx = -bola.velx * RESTITUICAO_BOLA
                elif bola.x < LARGURA_GOL - bola.raio:
                    placar[1] += 1
                    quem_fez_gol = 2
                    tempo_jogado_ms += (agora - tick_partida)
                    estado = GOL
                    fase_tick = agora
                    recursos[SOM_APITO].play()
            if bola.x > LARGURA - bola.raio:
                if bola.y < topo:
                    bola.x = LARGURA - bola.raio
                    bola.velx = -bola.velx * RESTITUICAO_BOLA
                elif bola.x > LARGURA - LARGURA_GOL + bola.raio:
                    placar[0] += 1
                    quem_fez_gol = 1
                    tempo_jogado_ms += (agora - tick_partida)
                    estado = GOL
                    fase_tick = agora
                    recursos[SOM_APITO].play()

            # Guarda: só termina se ainda estiver em JOGANDO (um gol no mesmo
            # frame já pode ter mudado o estado para GOL)
            if estado == JOGANDO and tempo_restante == 0:
                tempo_jogado_ms = PARTIDA_MS
                estado = FIM
                fase_tick = agora
                recursos[SOM_APITO].play()

        elif estado == GOL:
            # Pausa de comemoração; depois reposiciona tudo
            if agora - fase_tick >= PAUSA_GOL_MS:
                p1.x, p1.y = LARGURA * 0.28, Y_CHAO - p1.raio
                p2.x, p2.y = LARGURA * 0.72, Y_CHAO - p2.raio
                for p in jogadores:
                    p.velx = p.vely = 0
                bola.reiniciar()
                teclas_pressionadas = {}
                estado = CONTAGEM
                fase_tick = agora

        # ----- Desenho
        _desenhar_campo(janela)
        _desenhar_gol(janela, 'L')
        _desenhar_gol(janela, 'R')
        p1.desenhar(janela)
        p2.desenhar(janela)
        bola.desenhar(janela)

        # Placar e tempo no topo
        seg_relogio = tempo_restante // 1000
        texto_relogio = "{:01d}:{:02d}".format(seg_relogio // 60, seg_relogio % 60)
        _texto(janela, recursos[FONTE_M],
               "{}  -  {}".format(placar[0], placar[1]),
               BRANCO, (LARGURA // 2, 30))
        _texto(janela, recursos[FONTE_P], texto_relogio, AMARELO, (LARGURA // 2, 64))
        _texto(janela, recursos[FONTE_P], "P1", AZUL, (40, 26))
        _texto(janela, recursos[FONTE_P], "P2", VERMELHO, (LARGURA - 40, 26))

        # Contador do poder de cada jogador
        for idx, jog in enumerate(jogadores):
            px = 70 if idx == 0 else LARGURA - 70
            if jog.poder_pronto():
                _texto(janela, recursos[FONTE_P], "PODER!", AMARELO, (px, 56))
            else:
                seg_poder = int(math.ceil(jog.poder_restante_ms() / 1000))
                _texto(janela, recursos[FONTE_P],
                       "{}s".format(seg_poder), BRANCO, (px, 56))

        if estado == CONTAGEM:
            falta = CONTAGEM_MS - (agora - fase_tick)
            n = max(1, int(math.ceil(falta / 1000)))
            _texto(janela, recursos[FONTE_G], str(n), BRANCO,
                   (LARGURA // 2, ALTURA // 2))
            _texto(janela, recursos[FONTE_P], "P1: A D / W / S / LSHIFT",
                   BRANCO, (170, ALTURA - 22))
            _texto(janela, recursos[FONTE_P], "P2: setas / RSHIFT",
                   BRANCO, (LARGURA - 170, ALTURA - 22))

        elif estado == GOL:
            _texto(janela, recursos[FONTE_G],
                   "GOL P{}".format(quem_fez_gol),
                   AMARELO, (LARGURA // 2, ALTURA // 2))

        elif estado == FIM:
            janela.fill(PRETO)
            if placar[0] > placar[1]:
                msg = "P1 VENCEU"
            elif placar[1] > placar[0]:
                msg = "P2 VENCEU"
            else:
                msg = "EMPATE"
            _texto(janela, recursos[FONTE_M], msg, BRANCO,
                   (LARGURA // 2, ALTURA // 2 - 70))
            _texto(janela, recursos[FONTE_G],
                   "{} - {}".format(placar[0], placar[1]),
                   AMARELO, (LARGURA // 2, ALTURA // 2))
            _texto(janela, recursos[FONTE_P],
                   "ENTER = recomecar      ESC = encerrar",
                   BRANCO, (LARGURA // 2, ALTURA // 2 + 80))

        pygame.display.update()

    return saida