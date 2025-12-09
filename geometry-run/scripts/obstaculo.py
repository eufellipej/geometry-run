import pygame
import random

class Obstaculo:
    def __init__(self, tela, largura_tela, altura_tela, velocidade_base=4):
        self.tela = tela
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Propriedades do obstáculo
        self.largura = random.randint(30, 80)
        self.altura = random.randint(60, 200)
        self.posicao = [largura_tela, 0]
        self.velocidade = velocidade_base
        
        # Gerar formato (superior ou inferior)
        self.tipo = random.choice(['superior', 'inferior'])
        
        # Definir posição Y baseada no tipo
        if self.tipo == 'superior':
            self.posicao[1] = 0
        else:  # inferior
            self.posicao[1] = altura_tela - self.altura
        
        # Cores
        self.cor_base = (255, 100, 100)
        self.cor_borda = (255, 150, 150)
        
        # Retângulo de colisão
        self.rect = pygame.Rect(self.posicao[0], self.posicao[1], 
                               self.largura, self.altura)
        
    def atualizar(self, multiplicador_velocidade=1.0):
        """Atualiza a posição do obstáculo"""
        self.posicao[0] -= self.velocidade * multiplicador_velocidade
        self.rect.x = self.posicao[0]
    
    def desenhar(self):
        """Desenha o obstáculo na tela"""
        # Desenhar obstáculo principal
        rect_desenho = pygame.Rect(
            self.posicao[0],
            self.posicao[1],
            self.largura,
            self.altura
        )
        
        # Gradiente de cor
        intensidade_cor = min(255, 100 + int((self.posicao[0] / self.largura_tela) * 155))
        cor_atual = (intensidade_cor, 100, 100)
        
        pygame.draw.rect(self.tela, cor_atual, rect_desenho, border_radius=4)
        pygame.draw.rect(self.tela, self.cor_borda, rect_desenho, 2, border_radius=4)
    
    def get_rect(self):
        """Retorna o retângulo de colisão"""
        return self.rect
    
    def esta_fora_tela(self):
        """Verifica se o obstáculo saiu da tela"""
        return self.posicao[0] + self.largura < 0
    
    def aumentar_velocidade(self, incremento=0.1):
        """Aumenta a velocidade do obstáculo"""
        self.velocidade = min(8, self.velocidade + incremento)


class GerenciadorObstaculos:
    def __init__(self, tela, largura_tela, altura_tela):
        self.tela = tela
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        self.obstaculos = []
        self.tempo_ultimo_spawn = 0
        self.intervalo_spawn = 90  # frames
        self.velocidade_base = 4
        
    def atualizar(self, pontuacao, multiplicador_velocidade=1.0):
        """Atualiza todos os obstáculos"""
        # Atualizar obstáculos existentes
        for obstaculo in self.obstaculos[:]:
            obstaculo.atualizar(multiplicador_velocidade)
            
            # Remover obstáculos fora da tela
            if obstaculo.esta_fora_tela():
                self.obstaculos.remove(obstaculo)
        
        # Gerar novos obstáculos
        self.tempo_ultimo_spawn += 1
        if self.tempo_ultimo_spawn >= self.intervalo_spawn:
            self.criar_par_obstaculos()
            self.tempo_ultimo_spawn = 0
        
        # Aumentar dificuldade baseado na pontuação
        self.ajustar_dificuldade(pontuacao)
    
    def criar_par_obstaculos(self):
        """Cria um par de obstáculos (superior e inferior)"""
        # Determinar altura do vão
        altura_vao = random.randint(120, 180)
        posicao_vao = random.randint(100, self.altura_tela - altura_vao - 100)
        
        # Criar obstáculo superior
        obstaculo_superior = Obstaculo(self.tela, self.largura_tela, self.altura_tela, self.velocidade_base)
        obstaculo_superior.tipo = 'superior'
        obstaculo_superior.altura = posicao_vao
        obstaculo_superior.posicao[1] = 0
        obstaculo_superior.rect = pygame.Rect(obstaculo_superior.posicao[0], obstaculo_superior.posicao[1],
                                            obstaculo_superior.largura, obstaculo_superior.altura)
        
        # Criar obstáculo inferior
        obstaculo_inferior = Obstaculo(self.tela, self.largura_tela, self.altura_tela, self.velocidade_base)
        obstaculo_inferior.tipo = 'inferior'
        obstaculo_inferior.altura = self.altura_tela - (posicao_vao + altura_vao)
        obstaculo_inferior.posicao[1] = posicao_vao + altura_vao
        obstaculo_inferior.rect = pygame.Rect(obstaculo_inferior.posicao[0], obstaculo_inferior.posicao[1],
                                             obstaculo_inferior.largura, obstaculo_inferior.altura)
        
        self.obstaculos.append(obstaculo_superior)
        self.obstaculos.append(obstaculo_inferior)
    
    def ajustar_dificuldade(self, pontuacao):
        """Ajusta a dificuldade baseado na pontuação"""
        # Aumentar velocidade a cada 50 pontos
        if pontuacao > 0 and pontuacao % 50 == 0:
            self.velocidade_base = min(8, self.velocidade_base + 0.1)
            for obstaculo in self.obstaculos:
                obstaculo.aumentar_velocidade(0.1)
        
        # Diminuir intervalo de spawn a cada 100 pontos
        if pontuacao > 0 and pontuacao % 100 == 0:
            self.intervalo_spawn = max(40, self.intervalo_spawn - 5)
    
    def desenhar(self):
        """Desenha todos os obstáculos"""
        for obstaculo in self.obstaculos:
            obstaculo.desenhar()
    
    def verificar_colisao(self, rect_jogador):
        """Verifica colisão com qualquer obstáculo"""
        for obstaculo in self.obstaculos:
            if rect_jogador.colliderect(obstaculo.get_rect()):
                return True
        return False
    
    def resetar(self):
        """Reseta o gerenciador de obstáculos"""
        self.obstaculos.clear()
        self.tempo_ultimo_spawn = 0
        self.intervalo_spawn = 90
        self.velocidade_base = 4