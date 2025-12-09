import pygame
import sys
from scripts.cenas import Menu, SelecaoFase, Partida, GameOver

class GeometryRun:
    def __init__(self):
        pygame.init()
        
        # Configurações da tela
        self.LARGURA = 800
        self.ALTURA = 600
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Geometry Run - Escolha sua Fase")
        
        # Cores para diferentes fases (cada fase tem sua própria paleta)
        self.CORES_FASES = [
            {  # FASE 1 - Velocidade Normal (1.0x)
                'fundo': (15, 20, 35),      # Azul escuro
                'jogador': (0, 200, 255),
                'obstaculo': (255, 100, 100),
                'texto': (240, 240, 240),
                'ui_bg': (30, 40, 60),
                'botao': (40, 120, 180),
                'botao_hover': (60, 160, 220)
            },
            {  # FASE 2 - Velocidade Rápida (1.5x)
                'fundo': (35, 15, 20),      # Vermelho escuro
                'jogador': (100, 255, 200),
                'obstaculo': (255, 200, 100),
                'texto': (240, 240, 240),
                'ui_bg': (50, 30, 40),
                'botao': (180, 80, 100),
                'botao_hover': (200, 100, 120)
            },
            {  # FASE 3 - Velocidade Extrema (2.0x)
                'fundo': (15, 35, 20),      # Verde escuro
                'jogador': (255, 150, 50),
                'obstaculo': (150, 100, 255),
                'texto': (240, 240, 240),
                'ui_bg': (30, 50, 40),
                'botao': (80, 160, 100),
                'botao_hover': (100, 180, 120)
            }
        ]
        
        # Estados do jogo
        self.estados = {
            'menu': Menu(self.tela, self.LARGURA, self.ALTURA, self.CORES_FASES[0]),
            'selecao_fase': None,
            'partida': None,
            'game_over': None
        }
        
        self.estado_atual = 'menu'
        self.relogio = pygame.time.Clock()
        self.FPS = 60
        
        # Dados persistentes
        self.high_score = 0
        self.fase_selecionada = 1  # Fase padrão (1 = 1.0x)
        
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
                        if self.estado_atual == 'partida':
                            self.estado_atual = 'selecao_fase'
                            self.estados['selecao_fase'] = SelecaoFase(self.tela, self.LARGURA, self.ALTURA, self.CORES_FASES)
                        elif self.estado_atual == 'game_over':
                            self.estado_atual = 'selecao_fase'
                            self.estados['selecao_fase'] = SelecaoFase(self.tela, self.LARGURA, self.ALTURA, self.CORES_FASES)
                        elif self.estado_atual == 'selecao_fase':
                            self.estado_atual = 'menu'
                            self.estados['menu'] = Menu(self.tela, self.LARGURA, self.ALTURA, self.CORES_FASES[0])
            
            # Limpar tela
            if self.estado_atual == 'partida' and self.estados['partida'] is not None:
                # Usar cores da fase selecionada
                fase_index = self.fase_selecionada - 1
                self.tela.fill(self.CORES_FASES[fase_index]['fundo'])
            elif self.estado_atual == 'selecao_fase' and self.estados['selecao_fase'] is not None:
                # Fundo neutro para tela de seleção
                self.tela.fill((20, 25, 40))
            elif self.estado_atual == 'game_over' and self.estados['game_over'] is not None:
                # Fundo da fase que estava jogando
                fase_index = self.fase_selecionada - 1
                self.tela.fill(self.CORES_FASES[fase_index]['fundo'])
            else:
                self.tela.fill(self.CORES_FASES[0]['fundo'])
            
            try:
                # Inicializar estado se necessário
                if self.estado_atual == 'selecao_fase' and self.estados['selecao_fase'] is None:
                    self.estados['selecao_fase'] = SelecaoFase(self.tela, self.LARGURA, self.ALTURA, self.CORES_FASES)
                
                if self.estado_atual == 'partida' and self.estados['partida'] is None:
                    self.estados['partida'] = Partida(self.tela, self.LARGURA, self.ALTURA, 
                                                     self.CORES_FASES, self.fase_selecionada)
                
                # Atualizar estado atual
                if self.estado_atual in self.estados and self.estados[self.estado_atual] is not None:
                    resultado = self.estados[self.estado_atual].atualizar()
                    
                    # Processar resultado da atualização
                    if resultado is not None:
                        novo_estado, dados = resultado
                        
                        # Verificar se há dados de fase selecionada
                        if dados is not None and 'fase' in dados:
                            self.fase_selecionada = dados['fase']
                        
                        # Atualizar high score se for game over
                        if novo_estado == 'game_over':
                            pontuacao = dados.get('pontuacao', 0)
                            fase = dados.get('fase', 1)
                            # Separar high score por fase
                            if fase == 1:
                                if pontuacao > self.high_score:
                                    self.high_score = pontuacao
                            elif fase == 2:
                                # Para fase 2, high score é diferente
                                if pontuacao > self.high_score:
                                    self.high_score = pontuacao
                            elif fase == 3:
                                # Para fase 3, high score é diferente
                                if pontuacao > self.high_score:
                                    self.high_score = pontuacao
                            dados['high_score'] = self.high_score
                        
                        # Mudar para novo estado
                        self.estado_atual = novo_estado
                        
                        # Recriar a cena necessária
                        if novo_estado == 'selecao_fase':
                            self.estados['selecao_fase'] = SelecaoFase(self.tela, self.LARGURA, self.ALTURA, self.CORES_FASES)
                            self.estados['partida'] = None
                            self.estados['game_over'] = None
                        elif novo_estado == 'partida':
                            self.estados['partida'] = Partida(self.tela, self.LARGURA, self.ALTURA, 
                                                             self.CORES_FASES, self.fase_selecionada)
                            self.estados['game_over'] = None
                        elif novo_estado == 'game_over':
                            self.estados['game_over'] = GameOver(self.tela, self.LARGURA, self.ALTURA, 
                                                                self.CORES_FASES[self.fase_selecionada-1], dados)
                            self.estados['partida'] = None
                        elif novo_estado == 'menu':
                            self.estados['menu'] = Menu(self.tela, self.LARGURA, self.ALTURA, self.CORES_FASES[0])
                            self.estados['partida'] = None
                            self.estados['game_over'] = None
                            self.estados['selecao_fase'] = None
                    
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