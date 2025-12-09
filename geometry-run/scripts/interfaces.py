import pygame

class Texto:
    def __init__(self, tela, texto, x, y, cor, tamanho, fonte=None, centralizado=False):
        self.tela = tela
        self.texto = str(texto)
        self.cor = cor
        self.tamanho = tamanho
        self.centralizado = centralizado
        
        # Inicializar fonte
        if fonte is None:
            self.fonte = pygame.font.Font(None, self.tamanho)
        else:
            self.fonte = pygame.font.Font(fonte, self.tamanho)
        
        # Renderizar texto
        self.imagem_texto = self.fonte.render(self.texto, True, self.cor)
        
        # Calcular posição
        if self.centralizado:
            self.posicao = (x - self.imagem_texto.get_width() // 2, 
                           y - self.imagem_texto.get_height() // 2)
        else:
            self.posicao = (x, y)
    
    def desenhar(self, superficie=None):
        """Desenha o texto na tela ou superfície especificada"""
        if superficie is None:
            superficie = self.tela
        superficie.blit(self.imagem_texto, self.posicao)
    
    def atualizar_texto(self, novo_texto):
        """Atualiza o texto mantendo as configurações"""
        self.texto = str(novo_texto)
        self.imagem_texto = self.fonte.render(self.texto, True, self.cor)
        
        # Recalcular posição se centralizado
        if self.centralizado:
            x, y = self.posicao[0] + self.imagem_texto.get_width() // 2, \
                   self.posicao[1] + self.imagem_texto.get_height() // 2
            self.posicao = (x - self.imagem_texto.get_width() // 2, 
                           y - self.imagem_texto.get_height() // 2)


class Botao:
    def __init__(self, tela, texto, x, y, largura, altura, 
                 cor_fundo, cor_texto, cor_hover=None, 
                 fonte=None, tamanho_fonte=36):
        self.tela = tela
        self.texto_obj = Texto(tela, texto, x + largura//2, y + altura//2, 
                              cor_texto, tamanho_fonte, fonte, True)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover if cor_hover else self.ajustar_brightness(cor_fundo, 1.3)
        self.cor_atual = cor_fundo
        self.clicado = False
        
    def ajustar_brightness(self, cor, fator):
        """Ajusta o brilho de uma cor"""
        return tuple(min(255, int(c * fator)) for c in cor)
    
    def desenhar(self):
        """Desenha o botão na tela"""
        # Desenhar fundo
        pygame.draw.rect(self.tela, self.cor_atual, self.rect, border_radius=8)
        pygame.draw.rect(self.tela, (255, 255, 255), self.rect, 2, border_radius=8)
        
        # Desenhar texto
        self.texto_obj.desenhar()
    
    def atualizar(self):
        """Atualiza o estado do botão"""
        pos_mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(pos_mouse)
        
        # Atualizar cor
        self.cor_atual = self.cor_hover if hover else self.cor_fundo
        
        # Verificar clique
        clique = False
        if hover and pygame.mouse.get_pressed()[0]:
            if not self.clicado:
                clique = True
                self.clicado = True
        else:
            self.clicado = False
        
        return clique
    
    def get_rect(self):
        """Retorna o retângulo do botão"""
        return self.rect