import pygame

def inicializa():
    pygame.init() # Inicia a bibliotaca pygame

    global largura_jogo
    largura_jogo = 550
    global altura_jogo
    altura_jogo = 600

    window = pygame.display.set_mode((largura_jogo, altura_jogo)) # Cria uma janela de 320 pixeis de largura e 240 pixeis de altura
    pygame.display.set_caption('Jogo do João Pedro') # Define o título da janela

    assets = {'nave': pygame.image.load('assets/img/playerShip1_orange.png'), 
              'nave_tamanho': (50, 38),
              'fundo': pygame.image.load('assets/img/starfield.png'), # Carrega uma imagem
              'fundo_tamanho': (550, 600),
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

    pygame.display.update() # Atualiza a janela do jogo

def game_loop(window, assets):
    game = True

    while game:
        game = recebe_eventos()

        if game:
            desenha(window, assets)
        