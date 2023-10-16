import pygame
from random import randint

def inicializa():
    pygame.init() # Inicia a bibliotaca pygame

    global largura_jogo
    largura_jogo = 550
    global altura_jogo
    altura_jogo = 600

    window = pygame.display.set_mode((largura_jogo, altura_jogo)) # Cria uma janela de 320 pixeis de largura e 240 pixeis de altura
    pygame.display.set_caption('Jogo do João Pedro') # Define o título da janela

    estrelas = []

    for quantidade in range(10):
        center = (randint(0, largura_jogo), randint(0, altura_jogo))
        tamanho = randint(1, 3)
        estrelas += [(center, tamanho)]

    assets = {'nave': pygame.image.load('assets/img/playerShip1_orange.png'), 
              'nave_tamanho': (60, 50),
              'fundo': pygame.image.load('assets/img/starfield.png'), # Carrega uma imagem
              'fundo_tamanho': (550, 600),
              'estrelas': estrelas,
              'vida_fonte': pygame.font.Font('assets/font/PressStart2P.ttf', 25), # Carrega o texto onde o primeiro argumento é o caminho do arquivo da fonte e o segundo é o tamanho
              'vida': 3
              } 

    return window, assets


def recebe_eventos():
    game = True
    
    for event in pygame.event.get(): # Retorna uma lista com todos os eventos que ocorreram desde a última vez que essa função foi chamada
        if event.type == pygame.QUIT: 
            game = False

    return game


def desenha(window, assets):
    window.fill((0, 0, 0)) # Prrenche a janela do jogo com a cor vermelha
    

    fundo = pygame.transform.scale(assets['fundo'], assets['fundo_tamanho']) # Redefinir dimensão da imagem
    window.blit(fundo, (0, 0)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

    nave = pygame.transform.scale(assets['nave'], assets['nave_tamanho']) # Redefinir dimensão da imagem
    window.blit(nave, (largura_jogo // 2 - assets['nave_tamanho'][0] // 2, altura_jogo - assets['nave_tamanho'][1] - 35)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

    for estrela in assets['estrelas']:
        cor = (255, 255, 255)
        pygame.draw.circle(window, cor, estrela[0], estrela[1]) # Desenha um círculo na janela window (primeiro argumento), preenchido com a cor (segundo argumento) e com vértices listados como tuplas em vertices (terceiro argumento) com os valores (x,y)

    vida = assets['vida_fonte'].render(chr(9829) * assets['vida'], True, (255, 0, 0)) # Cria uma imagem do texto
    window.blit(vida, (20, 0))

    pygame.display.update() # Atualiza a janela do jogo

def game_loop(window, assets):
    game = True

    while game:
        game = recebe_eventos()

        if game:
            desenha(window, assets)
        