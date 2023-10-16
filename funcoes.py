import pygame

def inicializa():
    pygame.init() # Inicia a bibliotaca pygame

    window = pygame.display.set_mode((550, 600)) # Cria uma janela de 320 pixeis de largura e 240 pixeis de altura
    pygame.display.set_caption('Jogo do João Pedro') # Define o título da janela

    return window


def recebe_eventos():
    game = True
    
    for event in pygame.event.get(): # Retorna uma lista com todos os eventos que ocorreram desde a última vez que essa função foi chamada
        if event.type == pygame.QUIT: 
            game = False

    return game


def desenha(window):
    window.fill((0, 0, 0)) # Prrenche a janela do jogo com a cor vermelha
    pygame.display.update() # Atualiza a janela do jogo


def game_loop(window):
    game = True

    while game:
        game = recebe_eventos()

        if game:
            desenha(window)
        