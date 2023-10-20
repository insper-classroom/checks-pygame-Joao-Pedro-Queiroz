import pygame
from random import randint, random


class Nave():
    def __init__(self, jogador_x, jogador_y, largura_nave, altura_nave):
        self.image_nave = pygame.image.load('assets/img/playerShip1_orange.png')
        self.x_jogador = jogador_x
        self.y_jogador = jogador_y
        self.largura_nave = largura_nave
        self.altura_nave = altura_nave
        self.last_updated = 0


    def atualiza_estado(self, largura_jogo, altura_jogo, velocidade_x, velocidade_y):
        t1 =  pygame.time.get_ticks()
        delta_t = (t1 - self.last_updated) / 1000
        
        self.x_jogador += velocidade_x * delta_t
        self.y_jogador += velocidade_y * delta_t

        if  self.x_jogador < 0:
            self.x_jogador = 0
        elif self.x_jogador + self.largura_nave > largura_jogo:
            self.x_jogador = largura_jogo - self.largura_nave
        
        if  self.y_jogador < 0:
            self.y_jogador = 0
        elif self.y_jogador + self.altura_nave > altura_jogo:
            self.y_jogador = altura_jogo - self.altura_nave


    def desenha(self, window):
        nave = pygame.transform.scale(self.image_nave, (self.largura_nave, self.altura_nave)) # Redefinir dimensão da imagem
        window.blit(nave, (self.x_jogador,  self.y_jogador)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).


class Meteoro():
    def __init__(self, posicao, velocidade, orientação, largura_meteoro, altura_meteoro):
        self.imagem_meteoro = pygame.image.load('assets/img/meteorBrown_med1.png')
        self.posicao = posicao
        self.velocidade = velocidade
        self.orientação = orientação
        self.largura_meteoro = largura_meteoro
        self.altura_meteoro = altura_meteoro
        self.last_updated = 0
    

    def atualiza_estado(self,largura_jogo, altura_jogo):
        t1 =  pygame.time.get_ticks() # Carrega o tempo do frame em milissegundos
        delta_t = (t1 - self.last_updated) / 1000

        if self.orientação == 1:
            self.posicao[0] += self.velocidade[0] * delta_t
            self.posicao[1] += self.velocidade[1]
        elif self.orientação == -1:
            self.posicao[0] -= self.velocidade[0] * delta_t
            self.posicao[1] += self.velocidade[1]
        else:
            self.posicao[1] += self.velocidade[1]

        if  self.posicao[0] < 0:
            self.posicao[0] = largura_jogo
        elif self.posicao[0] > largura_jogo:
            self.posicao[0] = 0

        if self.posicao[1] > altura_jogo:
           self.posicao[1] = -100


    def desenha(self, window):
        window.blit(self.imagem_meteoro, self.posicao) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).


class TelaInicial:
    def __init__(self, largura_jogo, altura_jogo, fonte_padrao):
        self.largura_jogo = largura_jogo
        self.altura_jogo = altura_jogo
        self.font_texto = pygame.font.Font(fonte_padrao, 18)
        self.image_fundo = pygame.image.load('assets/img/starfield.png') # Carrega uma imagem
        self.tamanho_fundo = (largura_jogo, altura_jogo)
    

    def atualiza_estado(self):
        for event in pygame.event.get(): # Retorna uma lista com todos os eventos que ocorreram desde a última vez que essa função foi chamada
            if event.type == pygame.QUIT: 
                return -1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.load('assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg') # Carrega uma música
                pygame.mixer.music.play() # Começa a tocar a MÚSICA
                return 1
        
        return 0
        

    def desenha(self, window):
        window.fill((0, 0, 0))

        fundo = pygame.transform.scale(self.image_fundo, self.tamanho_fundo) # Redefinir dimensão da imagem
        window.blit(fundo, (0, 0)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        texto_inicio = self.font_texto.render(f'CLIQUE "EBTER" PARA INICIAR O JOGO', True, (255, 255, 255)) # Cria uma imagem do texto
        window.blit(texto_inicio, (100, 300)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        pygame.display.update()


class TelaGameOver:
    def __init__(self, largura_jogo, altura_jogo, fonte_padrao):
        self.largura_jogo = largura_jogo
        self.altura_jogo = altura_jogo
        self.font_texto = pygame.font.Font(fonte_padrao, 18)
        self.image_fundo = pygame.image.load('assets/img/starfield.png') # Carrega uma imagem
        self.tamanho_fundo = (largura_jogo, altura_jogo)
    

    def atualiza_estado(self):
        for event in pygame.event.get(): # Retorna uma lista com todos os eventos que ocorreram desde a última vez que essa função foi chamada
            if event.type == pygame.QUIT: 
                return -1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                Jogo.atual.telas[1].vida = 3

                for indice in range(len(Jogo.atual.telas[1].meteoros)):
                    Jogo.atual.telas[1].meteoros[indice].posicao[1] = -100
                    Jogo.atual.telas[1].meteoros[indice].last_updated = 0
                    
                return 0
            
        return 2
        
    
    def desenha(self, window):
        window.fill((0, 0, 0))

        fundo = pygame.transform.scale(self.image_fundo, self.tamanho_fundo) # Redefinir dimensão da imagem
        window.blit(fundo, (0, 0)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        texto_morte2 = self.font_texto.render(f'TODOS OS TRIPILANTES DE SUA NAVE MORRERAM!', True, (255, 0, 0)) # Cria uma imagem do texto
        window.blit(texto_morte2, (40, 265)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).
        
        texto_morte1 = self.font_texto.render(f'SUA NAVE FOI DESTRUÍDA!', True, (255, 0, 0)) # Cria uma imagem do texto
        window.blit(texto_morte1, (150, 240)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        texto_reiniciar = self.font_texto.render(f'CLIQUE "EBTER" PARA REINICIAR O JOGO', True, (255, 255, 255)) # Cria uma imagem do texto
        window.blit(texto_reiniciar, (80, 302)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        pygame.display.update()


class TelaJogo:
    def __init__(self, largura_jogo, altura_jogo, fonte_padrao, largura_nave, altura_nave):
        self.largura_jogo = largura_jogo
        self.altura_jogo = altura_jogo
        self.font_texto = pygame.font.Font(fonte_padrao, 18)
        self.image_fundo = pygame.image.load('assets/img/starfield.png') # Carrega uma imagem
        self.tamanho_fundo = (largura_jogo, altura_jogo)
        self.largura_nave = largura_nave
        self.altura_nave = altura_nave
        self.nave = Nave(largura_jogo // 2 - largura_nave // 2, altura_jogo - altura_nave - 35, largura_nave, altura_nave)
        self.vida_fonte = pygame.font.Font('assets/font/PressStart2P.ttf', 25) # Carrega o texto onde o primeiro argumento é o caminho do arquivo da fonte e o segundo é o tamanho
        self.vida = 3
        self.t0 = -1
        self.som_tiro = pygame.mixer.Sound('assets/snd/pew.wav') # Carrega um som
        self.velocidade_x = 0
        self.velocidade_y = 0

        self.estrelas = []

        for quantidade in range(50):
            center = (randint(0, largura_jogo), randint(0, altura_jogo))
            tamanho = randint(1, 3)
            self.estrelas += [(center, tamanho)]

        self.meteoros = []

        for quantidade in range(12):
            posicao = [randint(0, largura_jogo), -100]
            velocidade = [0.1 , random()]
            orientação = randint(-1, 1)
            largura_meteoro = 50
            altura_meteoro = 40
            self.meteoros.append(Meteoro(posicao, velocidade, orientação, largura_meteoro, altura_meteoro))
    

    def atualiza_estado(self):
        for event in pygame.event.get(): # Retorna uma lista com todos os eventos que ocorreram desde a última vez que essa função foi chamada
            if event.type == pygame.QUIT: 
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.velocidade_x = 0.1
            elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                self.velocidade_x = 0
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.velocidade_x = -0.1
            elif event.type == pygame.KEYUP and event.key == pygame.K_a:
                self.velocidade_x = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.velocidade_y = -0.1
            elif event.type == pygame.KEYUP and event.key == pygame.K_w:
                self.velocidade_y = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.velocidade_y = 0.1
            elif event.type == pygame.KEYUP and event.key == pygame.K_s:
                self.velocidade_y = 0

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.som_tiro.play() # Toca um som
        
        self.nave.atualiza_estado(self.largura_jogo, self.altura_jogo, self.velocidade_x, self.velocidade_y)

        for indice, meteoro in enumerate(self.meteoros):
            meteoro.atualiza_estado(self.largura_jogo, self.altura_jogo)
            
            r1 = pygame.Rect(meteoro.posicao[0], meteoro.posicao[1], meteoro.largura_meteoro, meteoro.altura_meteoro) # Armazena um retângulo
            r2 = pygame.Rect(self.nave.x_jogador, self.nave.y_jogador, self.nave.largura_nave, self.nave.altura_nave) # Armazena um retângulo
            colisão_nave_meteoro = r2.colliderect(r1) # Testa a colisão entre retângulos

            if colisão_nave_meteoro:
                self.vida -= 1
                del(self.meteoros[indice])
                posicao = [randint(0, self.largura_jogo), -100]
                velocidade = [0.1 , random()]
                orientação = randint(-1, 1)
                largura_meteoro = 50
                altura_meteoro = 40
                self.meteoros.append(Meteoro(posicao, velocidade, orientação, largura_meteoro, altura_meteoro))
            
            if self.vida == 0:
                self.velocidade_x = 0
                self.velocidade_y = 0
                self.nave.last_updated = 0
                self.nave.x_jogador = self.largura_jogo // 2 - self.largura_nave // 2
                self.nave.y_jogador = self.altura_jogo - self.altura_nave - 35

                return 2
            
        return 1
    

    def desenha(self, window):
        window.fill((0, 0, 0)) # Prrenche a janela do jogo com a cor preta
    
        fundo = pygame.transform.scale(self.image_fundo, self.tamanho_fundo) # Redefinir dimensão da imagem
        window.blit(fundo, (0, 0)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        self.nave.desenha(window)

        for estrela in self.estrelas:
            cor = (255, 255, 255)
            pygame.draw.circle(window, cor, estrela[0], estrela[1]) # Desenha um círculo na janela window (primeiro argumento), preenchido com a cor (segundo argumento) e com vértices listados como tuplas em vertices (terceiro argumento) com os valores (x,y)

        vida = self.vida_fonte.render(chr(9829) * self.vida , True, (255, 0, 0)) # Cria uma imagem do texto
        window.blit(vida, (20, 0)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        fps = 0
        t1 = pygame.time.get_ticks() # Devolve quanto tempo se passou, em milissegundos, desde que a função pygame.init() foi chamada

        if self.t0 >= 0:
            t = t1 - self.t0
            fps = 1000 / t
            
        self.t0 = t1
        texto_fps = self.font_texto.render(f'FPS: {fps:.2f}', True, (255, 255, 255)) # Cria uma imagem do texto
        window.blit(texto_fps, (425, 580)) # Desenha a imagem já carregada por pygame.image.load em window na posição (x, y).

        for indice, meteoro in enumerate(self.meteoros):
           meteoro.desenha(window)

        pygame.display.update() # Atualiza a janela do jogo


class Jogo:
    def __init__(self):
        pygame.init()
        self.largura_jogo = 550
        self.altura_jogo = 600
        self.fonte_padrao = pygame.font.get_default_font() # Carrega a fonte padrão
        self.largura_nave = 60
        self.altura_nave = 50
        self.window = pygame.display.set_mode((self.largura_jogo, self.altura_jogo))
        pygame.display.set_caption('Space Atari') # Define o título da janela
        self.indice_tela_atual = 0
        self.telas = [TelaInicial(self.largura_jogo, self.altura_jogo, self.fonte_padrao), TelaJogo(self.largura_jogo, self.altura_jogo, self.fonte_padrao, self.largura_nave, self.altura_nave), TelaGameOver(self.largura_jogo, self.altura_jogo, self.fonte_padrao)]

    def game_loop(self):
        tela_atual = self.telas[self.indice_tela_atual]

        rodando = True
        while rodando:
            self.indice_tela_atual = tela_atual.atualiza_estado()

            if self.indice_tela_atual == -1:
                rodando = False
            elif self.indice_tela_atual == 1:
                tela_atual = self.telas[self.indice_tela_atual]
                tela_atual.desenha(self.window)
            else:
                tela_atual = self.telas[self.indice_tela_atual]
                tela_atual.desenha(self.window)
                pygame.mixer.music.pause()