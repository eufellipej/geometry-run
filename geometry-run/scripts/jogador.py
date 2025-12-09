import pygame

class Jogador:
    def __init__(self, tela, largura_tela, altura_tela):
        self.tela = tela
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Propriedades do jogador
        self.tamanho = 40
        self.posicao = [100, altura_tela // 2]
        self.velocidade = 5
        self.rect = pygame.Rect(self.posicao[0], self.posicao[1], 
                               self.tamanho, self.tamanho)
        
        # Cores
        self.cor = (0, 200, 255)
        self.cor_borda = (255, 255, 255)
        
        # Estado
        self.invencivel = False
    
    def atualizar(self):
        """Atualiza a posição do jogador"""
        # Obter teclas pressionadas
        teclas = pygame.key.get_pressed()
        
        # Movimento
        movimento = [0, 0]
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            movimento[1] -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            movimento[1] += self.velocidade
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimento[0] -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimento[0] += self.velocidade
        
        # Normalizar movimento diagonal
        if movimento[0] != 0 and movimento[1] != 0:
            movimento[0] *= 0.7071  # 1/√2
            movimento[1] *= 0.7071
        
        # Atualizar posição
        self.posicao[0] += movimento[0]
        self.posicao[1] += movimento[1]
        
        # Manter dentro da tela
        self.posicao[0] = max(0, min(self.largura_tela - self.tamanho, self.posicao[0]))
        self.posicao[1] = max(0, min(self.altura_tela - self.tamanho, self.posicao[1]))
        
        # Atualizar retângulo
        self.rect.x = self.posicao[0]
        self.rect.y = self.posicao[1]
    
    def desenhar(self):
        """Desenha o jogador na tela"""
        # Criar superfície para efeitos
        surf_jogador = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)
        
        # Desenhar jogador com efeito de invencibilidade
        if self.invencivel:
            # Piscar quando invencível
            import time
            piscar = int(time.time() * 10) % 2
            if piscar == 0:
                cor_atual = self.cor
            else:
                cor_atual = (255, 255, 255)
        else:
            cor_atual = self.cor
        
        # Desenhar quadrado principal
        pygame.draw.rect(surf_jogador, cor_atual, 
                        (0, 0, self.tamanho, self.tamanho), 
                        border_radius=6)
        pygame.draw.rect(surf_jogador, self.cor_borda, 
                        (0, 0, self.tamanho, self.tamanho), 
                        3, border_radius=6)
        
        # Desenhar na tela
        self.tela.blit(surf_jogador, self.posicao)
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return self.rect
    
    def ativar_invencibilidade(self, tempo=None):
        """Ativa invencibilidade temporária"""
        self.invencivel = True
    
    def resetar(self):
        """Reseta o jogador para a posição inicial"""
        self.posicao = [100, self.altura_tela // 2]
        self.invencivel = False