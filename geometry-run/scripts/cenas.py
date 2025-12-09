import pygame
from scripts.jogador import Jogador
from scripts.obstaculo import GerenciadorObstaculos
from scripts.interfaces import Texto, Botao

class Partida:
    def __init__(self, tela, largura, altura, cores):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.cores = cores
        
        # Elementos do jogo
        self.jogador = Jogador(tela, largura, altura)
        self.gerenciador_obstaculos = GerenciadorObstaculos(tela, largura, altura)
        
        # Pontuação
        self.pontuacao = 0
        self.multiplicador = 1.0
        self.tempo_jogo = 0
        
        # Estado
        self.game_over = False
        
    def atualizar(self):
        """Atualiza o estado da partida"""
        if self.game_over:
            # Já está em game over, retornar para mudar de estado
            return ('game_over', {'pontuacao': self.pontuacao})
        
        # Atualizar tempo
        self.tempo_jogo += 1
        
        # Verificar turbo (tecla espaço)
        teclas = pygame.key.get_pressed()
        self.velocidade_turbo = teclas[pygame.K_SPACE]
        self.multiplicador = 1.5 if self.velocidade_turbo else 1.0
        
        # Atualizar elementos do jogo
        self.jogador.atualizar()
        self.gerenciador_obstaculos.atualizar(self.pontuacao, self.multiplicador)
        
        # Atualizar pontuação (1 ponto por segundo)
        if self.tempo_jogo % 60 == 0:
            self.pontuacao += 1
        
        # Verificar colisões
        if self.gerenciador_obstaculos.verificar_colisao(self.jogador.get_rect()):
            if not self.jogador.invencivel:
                self.game_over = True
                return None  # Retorna None para continuar nesta cena por mais um frame
        
        # Manter jogador na tela
        if self.jogador.posicao[1] < 0 or self.jogador.posicao[1] > self.altura - self.jogador.tamanho:
            if not self.jogador.invencivel:
                self.game_over = True
                return None  # Retorna None para continuar nesta cena por mais um frame
        
        return None
    
    def desenhar(self):
        """Desenha todos os elementos da partida"""
        # Desenhar elementos do jogo
        self.gerenciador_obstaculos.desenhar()
        self.jogador.desenhar()
        
        # Desenhar interface
        texto_pontuacao = Texto(
            self.tela, f"Score: {self.pontuacao}", 
            20, 20, self.cores['texto'], 36
        )
        texto_pontuacao.desenhar()
        
        texto_multiplicador = Texto(
            self.tela, f"Speed: {self.multiplicador:.1f}x",
            self.largura // 2, 20, self.cores['texto'], 24, centralizado=True
        )
        texto_multiplicador.desenhar()
        
        # Se game over, mostrar mensagem
        if self.game_over:
            overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.tela.blit(overlay, (0, 0))
            
            texto_game_over = Texto(
                self.tela, "GAME OVER",
                self.largura // 2, self.altura // 2,
                (255, 80, 80), 64, centralizado=True
            )
            texto_game_over.desenhar()


class Menu:
    def __init__(self, tela, largura, altura, cores):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.cores = cores
        
        # Interface
        self.titulo = Texto(
            tela, "GEOMETRY RUN",
            largura // 2, altura // 4,
            cores['texto'], 64, centralizado=True
        )
        
        # Botões
        self.botao_jogar = Botao(
            tela, "JOGAR",
            largura // 2 - 100, altura // 2,
            200, 60,
            cores['botao'], cores['texto'],
            cores['botao_hover']
        )
        
        self.botao_sair = Botao(
            tela, "SAIR",
            largura // 2 - 100, altura // 2 + 80,
            200, 60,
            (100, 100, 120), cores['texto'],
            (120, 120, 140)
        )
    
    def atualizar(self):
        """Atualiza o menu"""
        if self.botao_jogar.atualizar():
            return ('partida', None)
        
        if self.botao_sair.atualizar():
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        
        return None
    
    def desenhar(self):
        """Desenha o menu"""
        self.titulo.desenhar()
        self.botao_jogar.desenhar()
        self.botao_sair.desenhar()


class GameOver:
    def __init__(self, tela, largura, altura, cores, dados):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.cores = cores
        
        # Dados da partida
        self.pontuacao = dados.get('pontuacao', 0)
        self.high_score = dados.get('high_score', 0)
        
        # Criar botões aqui no init para evitar recriação a cada frame
        self.botao_reiniciar = Botao(
            tela, "JOGAR NOVAMENTE",
            largura // 2 - 100, altura // 2 + 50,
            200, 50,
            cores['botao'], cores['texto'],
            cores['botao_hover']
        )
        
        self.botao_menu = Botao(
            tela, "VOLTAR AO MENU",
            largura // 2 - 100, altura // 2 + 120,
            200, 50,
            (100, 100, 120), cores['texto'],
            (120, 120, 140)
        )
    
    def atualizar(self):
        """Atualiza a tela de game over"""
        # Verificar botões
        if self.botao_reiniciar.atualizar():
            return ('partida', None)
        
        if self.botao_menu.atualizar():
            return ('menu', None)
        
        return None
    
    def desenhar(self):
        """Desenha a tela de game over"""
        # Fundo escurecido
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.tela.blit(overlay, (0, 0))
        
        # Textos
        texto_game_over = Texto(
            self.tela, "GAME OVER",
            self.largura // 2, self.altura // 3,
            (255, 80, 80), 72, centralizado=True
        )
        texto_game_over.desenhar()
        
        texto_pontuacao = Texto(
            self.tela, f"Score: {self.pontuacao}",
            self.largura // 2, self.altura // 2 - 30,
            self.cores['texto'], 36, centralizado=True
        )
        texto_pontuacao.desenhar()
        
        texto_high_score = Texto(
            self.tela, f"High Score: {self.high_score}",
            self.largura // 2, self.altura // 2,
            (255, 255, 100), 30, centralizado=True
        )
        texto_high_score.desenhar()
        
        # Desenhar botões
        self.botao_reiniciar.desenhar()
        self.botao_menu.desenhar()
        
        # Novo recorde
        if self.pontuacao == self.high_score and self.pontuacao > 0:
            novo_record = Texto(
                self.tela, "NOVO RECORD!",
                self.largura // 2, self.altura // 2 + 170,
                (255, 255, 100), 28, centralizado=True
            )
            novo_record.desenhar()