import pygame
from random import randint, random

def inicializa():
    pygame.init() # Inicia a bibliotaca pygame

    global largura_jogo
    largura_jogo = 550
    global altura_jogo
    altura_jogo = 600

    window = pygame.display.set_mode((largura_jogo, altura_jogo)) # Cria uma janela de 320 pixeis de largura e 240 pixeis de altura
    pygame.display.set_caption('Jogo do João Pedro') # Define o título da janela
    fonte_padrao = pygame.font.get_default_font() # Carrega a fonte padrão
    pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg') # Carrega uma música
    pygame.mixer.music.play() # Começa a tocar a música

    estrelas = []

    for quantidade in range(50):
        center = (randint(0, largura_jogo), randint(0, altura_jogo))
        tamanho = randint(1, 3)
        estrelas += [(center, tamanho)]

    meteoros = []

    for quantidade in range(12):
        meteoros.append({
            'posicao': [randint(0, largura_jogo), -100],
            'velocidade': [0.1 , random()],
            'orientação': randint(-1, 1)
            })

    assets = {'nave': pygame.image.load('assets/img/playerShip1_orange.png'), 
              'nave_tamanho': (60, 50),
              'fundo': pygame.image.load('assets/img/starfield.png'), # Carrega uma imagem
              'fundo_tamanho': (550, 600),
              'estrelas': estrelas,
              'vida_fonte': pygame.font.Font('assets/font/PressStart2P.ttf', 25), # Carrega o texto onde o primeiro argumento é o caminho do arquivo da fonte e o segundo é o tamanho
              'vida': 3,
              'fps_fonte': pygame.font.Font(fonte_padrao, 18),
              'meteoros_imagem': pygame.image.load('assets/img/meteorBrown_med1.png'), # Carrega uma imagem
              'meteoro_tamanho': (50, 40),
              'som_tiro': pygame.mixer.Sound('assets/snd/pew.wav')
              } 
    
    state = {
        'jogador_x': largura_jogo // 2 - assets['nave_tamanho'][0] // 2,
        'jogador_y': altura_jogo - assets['nave_tamanho'][1] - 35,
        'velocidade_x': 0,
        'velocidade_y': 0,
        't0': -1,
        'last_updated': 0,
        'meteoros': meteoros
    }

    return window, assets, state


def recebe_eventos(state, assets):
    game = True
    t1 =  pygame.time.get_ticks()
    delta_t = (t1 - state['last_updated']) / 1000
    
    for event in pygame.event.get(): # Retorna uma lista com todos os eventos que ocorreram desde a última vez que essa função foi chamada
        if event.type == pygame.QUIT: 
            game = False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            state['velocidade_x'] = 0.1
        elif event.type == pygame.KEYUP and event.key == pygame.K_d:
            state['velocidade_x'] = 0
    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            state['velocidade_x'] = -0.1
        elif event.type == pygame.KEYUP and event.key == pygame.K_a:
            state['velocidade_x'] = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            state['velocidade_y'] = -0.1
        elif event.type == pygame.KEYUP and event.key == pygame.K_w:
            state['velocidade_y'] = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
             state['velocidade_y'] = 0.1
        elif event.type == pygame.KEYUP and event.key == pygame.K_s:
            state['velocidade_y'] = 0
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            assets['som_tiro'].play()

    state['jogador_x'] += state['velocidade_x'] * delta_t
    state['jogador_y'] += state['velocidade_y'] * delta_t

    if  state['jogador_x'] < 0:
        state['jogador_x'] = 0
    elif state['jogador_x'] + assets['nave_tamanho'][0] > largura_jogo:
        state['jogador_x'] = largura_jogo - assets['nave_tamanho'][0]
    
    if  state['jogador_y'] < 0:
        state['jogador_y'] = 0
    elif state['jogador_y'] + assets['nave_tamanho'][1] > altura_jogo:
        state['jogador_y'] = altura_jogo - assets['nave_tamanho'][1]

    for índice, meteoro in enumerate(state['meteoros']):
        if meteoro['orientação'] == 1:
            state['meteoros'][índice]['posicao'][0] += meteoro['velocidade'][0] * delta_t
            state['meteoros'][índice]['posicao'][1] += meteoro['velocidade'][1]
        elif meteoro['orientação'] == -1:
            state['meteoros'][índice]['posicao'][0] -= meteoro['velocidade'][0] * delta_t
            state['meteoros'][índice]['posicao'][1] += meteoro['velocidade'][1]
        else:
            state['meteoros'][índice]['posicao'][1] += meteoro['velocidade'][1]

        if  meteoro['posicao'][0] < 0:
            state['meteoros'][índice]['posicao'][0] = largura_jogo
        elif meteoro['posicao'][0] > largura_jogo:
            state['meteoros'][índice]['posicao'][0] = 0

        if meteoro['posicao'][1] > altura_jogo:
            state['meteoros'][índice]['posicao'][1] = -100

        r1 = pygame.Rect(meteoro['posicao'][0], meteoro['posicao'][1], assets['meteoro_tamanho'][0], assets['meteoro_tamanho'][1]) # Armazena um retângulo
        r2 = pygame.Rect(state['jogador_x'], state['jogador_y'], assets['nave_tamanho'][0], assets['nave_tamanho'][1]) # Armazena um retângulo
        colisão_nave_meteoro = r2.colliderect(r1) # Testa a colisão entre retângulos

        if colisão_nave_meteoro:
            assets['vida'] -= 1
            del(state['meteoros'][índice])
        
        if assets['vida'] == 0:
            game = False

    return game


def desenha(window, assets, state):
    window.fill((0, 0, 0)) # Prrenche a janela do jogo com a cor preta
    

    fundo = pygame.transform.scale(assets['fundo'], assets['fundo_tamanho']) # Redefinir dimensão da imagem
    window.blit(fundo, (0, 0)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

    nave = pygame.transform.scale(assets['nave'], assets['nave_tamanho']) # Redefinir dimensão da imagem
    window.blit(nave, (state['jogador_x'],  state['jogador_y'])) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

    for estrela in assets['estrelas']:
        cor = (255, 255, 255)
        pygame.draw.circle(window, cor, estrela[0], estrela[1]) # Desenha um círculo na janela window (primeiro argumento), preenchido com a cor (segundo argumento) e com vértices listados como tuplas em vertices (terceiro argumento) com os valores (x,y)

    vida = assets['vida_fonte'].render(chr(9829) * assets['vida'], True, (255, 0, 0)) # Cria uma imagem do texto
    window.blit(vida, (20, 0)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

    fps = 0
    t1 = pygame.time.get_ticks() # Devolve quanto tempo se passou, em milissegundos, desde que a função pygame.init() foi chamada

    if state['t0'] >= 0:
        t = t1 - state['t0']
        fps = 1000 / t
        
    state['t0'] = t1
    texto_fps = assets['fps_fonte'].render(f'FPS: {fps:.2f}', True, (255, 255, 255)) # Cria uma imagem do texto
    window.blit(texto_fps, (425, 580)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

    for meteoro in state['meteoros']:
        nave = pygame.transform.scale(assets['meteoros_imagem'], assets['meteoro_tamanho']) # Redefinir dimensão da imagem
        window.blit(assets['meteoros_imagem'], meteoro['posicao']) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

    pygame.display.update() # Atualiza a janela do jogo

def game_loop(window, assets, state):
    game = True

    while game:
        game = recebe_eventos(state, assets)

        if game:
            desenha(window, assets, state)
        