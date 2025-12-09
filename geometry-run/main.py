import pygame
import sys
from scripts.cenas import Menu, Partida, GameOver

class GeometryRun:
    def __init__(self):
        pygame.init()
        
        # Configurações da tela
        self.LARGURA = 800
        self.ALTURA = 600
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Geometry Run")
        
        # Cores
        self.CORES = {
            'fundo': (15, 20, 35),
            'jogador': (0, 200, 255),
            'obstaculo': (255, 100, 100),
            'texto': (240, 240, 240),
            'ui_bg': (30, 40, 60),
            'botao': (40, 120, 180),
            'botao_hover': (60, 160, 220)
        }
        
        # Estados do jogo
        self.estados = {
            'menu': Menu(self.tela, self.LARGURA, self.ALTURA, self.CORES),
            'partida': None,
            'game_over': None
        }
        
        self.estado_atual = 'menu'
        self.relogio = pygame.time.Clock()
        self.FPS = 60
        
        # Dados persistentes
        self.high_score = 0
        
    def executar(self):
        """Loop principal do jogo"""
        rodando = True
        
        while rodando:
            # Processar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        # ESC volta para o menu de qualquer estado
                        if self.estado_atual != 'menu':
                            self.estado_atual = 'menu'
                            self.estados['menu'] = Menu(self.tela, self.LARGURA, self.ALTURA, self.CORES)
            
            # Limpar tela
            self.tela.fill(self.CORES['fundo'])
            
            try:
                # Atualizar estado atual
                if self.estado_atual == 'partida' and self.estados['partida'] is None:
                    self.estados['partida'] = Partida(self.tela, self.LARGURA, self.ALTURA, self.CORES)
                
                resultado = self.estados[self.estado_atual].atualizar()
                
                # Processar resultado da atualização
                if resultado is not None:
                    novo_estado, dados = resultado
                    
                    # Atualizar high score se for game over
                    if novo_estado == 'game_over':
                        pontuacao = dados.get('pontuacao', 0)
                        if pontuacao > self.high_score:
                            self.high_score = pontuacao
                        dados['high_score'] = self.high_score
                    
                    # Mudar para novo estado
                    self.estado_atual = novo_estado
                    
                    # Recriar a cena necessária
                    if novo_estado == 'partida':
                        self.estados['partida'] = Partida(self.tela, self.LARGURA, self.ALTURA, self.CORES)
                        self.estados['game_over'] = None
                    elif novo_estado == 'game_over':
                        self.estados['game_over'] = GameOver(self.tela, self.LARGURA, self.ALTURA, self.CORES, dados)
                        self.estados['partida'] = None
                    elif novo_estado == 'menu':
                        self.estados['menu'] = Menu(self.tela, self.LARGURA, self.ALTURA, self.CORES)
                        self.estados['partida'] = None
                        self.estados['game_over'] = None
                
                # Desenhar estado atual
                self.estados[self.estado_atual].desenhar()
                
            except Exception as e:
                print(f"Erro no jogo: {e}")
                import traceback
                traceback.print_exc()
                rodando = False
            
            # Atualizar tela
            pygame.display.flip()
            
            # Controlar FPS
            self.relogio.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jogo = GeometryRun()
    jogo.executar()