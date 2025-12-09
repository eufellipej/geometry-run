import pygame
from scripts.jogador import Jogador
from scripts.obstaculo import GerenciadorObstaculos
from scripts.interfaces import Texto, Botao

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
        
        self.subtitulo = Texto(
            tela, "ESCOLHA SUA FASE",
            largura // 2, altura // 4 + 60,
            cores['texto'], 24, centralizado=True
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
            return ('selecao_fase', None)
        
        if self.botao_sair.atualizar():
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        
        return None
    
    def desenhar(self):
        """Desenha o menu"""
        self.titulo.desenhar()
        self.subtitulo.desenhar()
        self.botao_jogar.desenhar()
        self.botao_sair.desenhar()

class SelecaoFase:
    def __init__(self, tela, largura, altura, cores_fases):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.cores_fases = cores_fases
        
        # Interface
        self.titulo = Texto(
            tela, "SELECIONE A FASE",
            largura // 2, altura // 6,
            (240, 240, 240), 48, centralizado=True
        )
        
        # Botões para cada fase
        self.botoes_fase = []
        
        # FASE 1 - Velocidade Normal (1.0x)
        botao_fase1 = Botao(
            tela, "FASE 1 - NORMAL",
            largura // 2 - 150, altura // 3,
            300, 70,
            cores_fases[0]['botao'], cores_fases[0]['texto'],
            cores_fases[0]['botao_hover']
        )
        botao_fase1.fase = 1
        botao_fase1.descricao = "Fase 1 - Velocidade Normal"
        botao_fase1.detalhes = "Velocidade: 1.0x - Dificuldade para iniciantes"
        self.botoes_fase.append(botao_fase1)
        
        # FASE 2 - Velocidade Rápida (1.5x)
        botao_fase2 = Botao(
            tela, "FASE 2 - RÁPIDA",
            largura // 2 - 150, altura // 3 + 100,
            300, 70,
            cores_fases[1]['botao'], cores_fases[1]['texto'],
            cores_fases[1]['botao_hover']
        )
        botao_fase2.fase = 2
        botao_fase2.descricao = "Fase 2 - Velocidade Rápida"
        botao_fase2.detalhes = "Velocidade: 1.5x - Para jogadores experientes"
        self.botoes_fase.append(botao_fase2)
        
        # FASE 3 - Velocidade Extrema (2.0x)
        botao_fase3 = Botao(
            tela, "FASE 3 - EXTREMA",
            largura // 2 - 150, altura // 3 + 200,
            300, 70,
            cores_fases[2]['botao'], cores_fases[2]['texto'],
            cores_fases[2]['botao_hover']
        )
        botao_fase3.fase = 3
        botao_fase3.descricao = "Fase 3 - Velocidade Extrema"
        botao_fase3.detalhes = "Velocidade: 2.0x - Apenas para os mais corajosos!"
        self.botoes_fase.append(botao_fase3)
        
        # Botão voltar
        self.botao_voltar = Botao(
            tela, "VOLTAR",
            largura // 2 - 100, altura - 100,
            200, 50,
            (100, 100, 120), (240, 240, 240),
            (120, 120, 140)
        )
        
        # Detalhes da seleção
        self.fase_selecionada = 1
        self.descricao_selecionada = "Fase 1 - Velocidade Normal"
        self.detalhes_selecionados = "Velocidade: 1.0x - Dificuldade para iniciantes"
    
    def atualizar(self):
        """Atualiza a tela de seleção de fase"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Verificar hover sobre os botões
        for botao in self.botoes_fase:
            if botao.rect.collidepoint(mouse_pos):
                self.fase_selecionada = botao.fase
                self.descricao_selecionada = botao.descricao
                self.detalhes_selecionados = botao.detalhes
        
        # Verificar cliques nos botões
        for botao in self.botoes_fase:
            if botao.atualizar():
                return ('partida', {'fase': botao.fase})
        
        # Verificar botão voltar
        if self.botao_voltar.atualizar():
            return ('menu', None)
        
        return None
    
    def desenhar(self):
        """Desenha a tela de seleção de fase"""
        # Fundo com gradiente
        for i in range(self.altura):
            cor_r = int(15 + (i / self.altura) * 20)
            cor_g = int(20 + (i / self.altura) * 15)
            cor_b = int(35 + (i / self.altura) * 10)
            pygame.draw.line(self.tela, (cor_r, cor_g, cor_b), (0, i), (self.largura, i))
        
        self.titulo.desenhar()
        
        # Instruções
        instrucoes = Texto(
            self.tela, "Escolha o nível de dificuldade do jogo:",
            self.largura // 2, self.altura // 6 + 60,
            (200, 200, 200), 22, centralizado=True
        )
        instrucoes.desenhar()
        
        # Desenhar botões de fase
        for botao in self.botoes_fase:
            botao.desenhar()
            
            # Adicionar indicador visual de velocidade
            indicador_x = botao.rect.x + botao.rect.width + 10
            indicador_y = botao.rect.y + botao.rect.height // 2
            
            # Desenhar indicador de velocidade da fase
            if botao.fase == 1:
                num_circulos = 3
                cor = (100, 200, 255)
                velocidade_texto = "1.0x"
            elif botao.fase == 2:
                num_circulos = 4
                cor = (255, 200, 100)
                velocidade_texto = "1.5x"
            else:
                num_circulos = 5
                cor = (255, 100, 100)
                velocidade_texto = "2.0x"
            
            # Desenhar texto da velocidade
            texto_velocidade = Texto(
                self.tela, velocidade_texto,
                indicador_x + 40, indicador_y,
                cor, 20, centralizado=False
            )
            texto_velocidade.desenhar()
        
        # Mostrar detalhes da seleção atual
        detalhes_bg = pygame.Rect(50, self.altura - 180, self.largura - 100, 120)
        pygame.draw.rect(self.tela, (40, 40, 60, 180), detalhes_bg, border_radius=10)
        pygame.draw.rect(self.tela, (100, 100, 140), detalhes_bg, 2, border_radius=10)
        
        texto_desc = Texto(
            self.tela, self.descricao_selecionada,
            self.largura // 2, self.altura - 160,
            (255, 255, 200), 28, centralizado=True
        )
        texto_desc.desenhar()
        
        texto_detalhes = Texto(
            self.tela, self.detalhes_selecionados,
            self.largura // 2, self.altura - 130,
            (200, 200, 200), 20, centralizado=True
        )
        texto_detalhes.desenhar()
        
        texto_info = Texto(
            self.tela, "Pressione ESPAÇO durante o jogo para turbo!",
            self.largura // 2, self.altura - 100,
            (150, 200, 255), 18, centralizado=True
        )
        texto_info.desenhar()
        
        # Desenhar botão voltar
        self.botao_voltar.desenhar()
        
        # Texto de ajuda
        ajuda = Texto(
            self.tela, "Pressione ESC a qualquer momento para voltar ao menu",
            self.largura // 2, self.altura - 30,
            (150, 150, 150), 16, centralizado=True
        )
        ajuda.desenhar()

class Partida:
    def __init__(self, tela, largura, altura, cores_fases, fase=1):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.cores_fases = cores_fases
        
        # Configurações da partida
        self.fase = fase  # 1, 2 ou 3
        self.velocidade_base = 1.0  # Será ajustado baseado na fase
        
        # Ajustar velocidade base conforme a fase
        if fase == 1:
            self.velocidade_base = 1.0  # Normal
            self.pontos_para_progresso = 30
        elif fase == 2:
            self.velocidade_base = 1.5  # Rápido
            self.pontos_para_progresso = 40
        else:  # fase == 3
            self.velocidade_base = 2.0  # Extremo
            self.pontos_para_progresso = 50
        
        # Elementos do jogo
        self.jogador = Jogador(tela, largura, altura)
        self.velocidade_obstaculos = 4.0 * self.velocidade_base
        self.gerenciador_obstaculos = GerenciadorObstaculos(tela, largura, altura, self.velocidade_obstaculos)
        
        # Pontuação
        self.pontuacao = 0
        self.multiplicador_turbo = 1.0
        self.tempo_jogo = 0
        
        # Progresso
        self.progresso_atual = 0
        self.nivel_atual = 1
        
        # Estado
        self.game_over = False
        
        # Atualizar cores do jogador para a fase atual
        self.jogador.cor = cores_fases[fase - 1]['jogador']
    
    def verificar_progresso(self):
        """Verifica se deve subir de nível dentro da mesma fase"""
        if self.pontuacao >= self.progresso_atual + self.pontos_para_progresso:
            self.progresso_atual = self.pontuacao
            self.nivel_atual += 1
            # Aumentar dificuldade
            self.velocidade_obstaculos += 0.2
            self.gerenciador_obstaculos.velocidade_base = self.velocidade_obstaculos
            # Ativar invencibilidade temporária
            self.jogador.ativar_invencibilidade(90)  # 1.5 segundos
            return True
        return False
    
    def atualizar(self):
        """Atualiza o estado da partida"""
        if self.game_over:
            return ('game_over', {'pontuacao': self.pontuacao, 'fase': self.fase})
        
        # Atualizar tempo
        self.tempo_jogo += 1
        
        # Verificar turbo (tecla espaço)
        teclas = pygame.key.get_pressed()
        self.velocidade_turbo = teclas[pygame.K_SPACE]
        self.multiplicador_turbo = 1.5 if self.velocidade_turbo else 1.0
        
        # Verificar progresso
        if self.verificar_progresso():
            print(f"Subiu para nível {self.nivel_atual} na fase {self.fase}")
        
        # Atualizar elementos do jogo
        self.jogador.atualizar()
        self.gerenciador_obstaculos.atualizar(self.pontuacao, self.multiplicador_turbo)
        
        # Atualizar pontuação (1 ponto por segundo)
        if self.tempo_jogo % 60 == 0:
            self.pontuacao += 1
        
        # Verificar colisões
        if self.gerenciador_obstaculos.verificar_colisao(self.jogador.get_rect()):
            if not self.jogador.invencivel:
                self.game_over = True
                return None
        
        # Manter jogador na tela
        if self.jogador.posicao[1] < 0 or self.jogador.posicao[1] > self.altura - self.jogador.tamanho:
            if not self.jogador.invencivel:
                self.game_over = True
                return None
        
        return None
    
    def desenhar(self):
        """Desenha todos os elementos da partida"""
        # O fundo já é desenhado no main.py
        # Desenhar elementos do jogo
        self.gerenciador_obstaculos.desenhar()
        self.jogador.desenhar()
        
        # Obter cores da fase atual
        cores_fase = self.cores_fases[self.fase - 1]
        
        # Desenhar interface
        texto_pontuacao = Texto(
            self.tela, f"Score: {self.pontuacao}", 
            20, 20, cores_fase['texto'], 36
        )
        texto_pontuacao.desenhar()
        
        texto_fase = Texto(
            self.tela, f"Fase: {self.fase} - Nível: {self.nivel_atual}",
            self.largura // 2, 60, cores_fase['texto'], 24, centralizado=True
        )
        texto_fase.desenhar()
        
        # Mostrar velocidade da fase
        texto_velocidade = Texto(
            self.tela, f"Velocidade: {self.velocidade_base:.1f}x",
            self.largura - 200, 20, cores_fase['texto'], 20
        )
        texto_velocidade.desenhar()
        
        texto_multiplicador = Texto(
            self.tela, f"Turbo: {self.multiplicador_turbo:.1f}x",
            self.largura // 2, 20, cores_fase['texto'], 24, centralizado=True
        )
        texto_multiplicador.desenhar()
        
        # Indicador de invencibilidade
        if self.jogador.invencivel:
            texto_invencivel = Texto(
                self.tela, "INVENCIBILIDADE!",
                self.largura // 2, 90,
                (255, 255, 100), 20, centralizado=True
            )
            texto_invencivel.desenhar()
        
        # Instruções
        texto_instrucoes = Texto(
            self.tela, "Espaço: Turbo | ESC: Selecionar Fase",
            self.largura // 2, self.altura - 20,
            (150, 150, 150), 16, centralizado=True
        )
        texto_instrucoes.desenhar()
        
        # Indicador de progresso para próximo nível
        pontos_restantes = max(0, self.pontos_para_progresso - (self.pontuacao - self.progresso_atual))
        progresso = min((self.pontuacao - self.progresso_atual) / self.pontos_para_progresso, 1.0)
        
        # Barra de progresso
        barra_largura = 200
        barra_altura = 10
        barra_x = self.largura // 2 - barra_largura // 2
        barra_y = 100
        
        # Fundo da barra
        pygame.draw.rect(self.tela, (50, 50, 50), 
                       (barra_x, barra_y, barra_largura, barra_altura))
        
        # Barra de progresso
        cor_progresso = (
            int(255 * (1 - progresso)),
            int(255 * progresso),
            100
        )
        pygame.draw.rect(self.tela, cor_progresso, 
                       (barra_x, barra_y, int(barra_largura * progresso), barra_altura))
        
        # Texto do próximo nível
        texto_proximo_nivel = Texto(
            self.tela, f"Próximo nível: {pontos_restantes} pontos",
            self.largura // 2, barra_y + 20,
            cores_fase['texto'], 16, centralizado=True
        )
        texto_proximo_nivel.desenhar()
        
        # Se game over, mostrar mensagem
        if self.game_over:
            overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.tela.blit(overlay, (0, 0))
            
            texto_game_over = Texto(
                self.tela, "GAME OVER",
                self.largura // 2, self.altura // 2 - 50,
                (255, 80, 80), 64, centralizado=True
            )
            texto_game_over.desenhar()
            
            texto_continuar = Texto(
                self.tela, "Aguarde para continuar...",
                self.largura // 2, self.altura // 2 + 20,
                (200, 200, 200), 24, centralizado=True
            )
            texto_continuar.desenhar()

class GameOver:
    def __init__(self, tela, largura, altura, cores, dados):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.cores = cores
        
        # Dados da partida
        self.pontuacao = dados.get('pontuacao', 0)
        self.high_score = dados.get('high_score', 0)
        self.fase = dados.get('fase', 1)
        
        # Determinar nome da fase
        if self.fase == 1:
            self.nome_fase = "Fase 1 - Normal"
            self.velocidade_texto = "1.0x"
        elif self.fase == 2:
            self.nome_fase = "Fase 2 - Rápida"
            self.velocidade_texto = "1.5x"
        else:
            self.nome_fase = "Fase 3 - Extrema"
            self.velocidade_texto = "2.0x"
        
        # Criar botões (REMOVIDO botão de nova velocidade)
        self.botao_reiniciar = Botao(
            tela, "JOGAR NOVAMENTE",
            largura // 2 - 150, altura // 2 + 50,
            300, 50,
            cores['botao'], cores['texto'],
            cores['botao_hover']
        )
        
        self.botao_menu = Botao(
            tela, "SELECIONAR OUTRA FASE",
            largura // 2 - 150, altura // 2 + 120,
            300, 50,
            (100, 100, 120), cores['texto'],
            (120, 120, 140)
        )
        
        # Timer para evitar clique acidental
        self.timer = 30  # 0.5 segundos
    
    def atualizar(self):
        """Atualiza a tela de game over"""
        # Evitar clique acidental imediato
        if self.timer > 0:
            self.timer -= 1
            return None
            
        if self.botao_reiniciar.atualizar():
            return ('partida', {'fase': self.fase})
        
        if self.botao_menu.atualizar():
            return ('selecao_fase', None)
        
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
            self.largura // 2, self.altura // 2 - 60,
            self.cores['texto'], 36, centralizado=True
        )
        texto_pontuacao.desenhar()
        
        texto_fase = Texto(
            self.tela, f"Fase: {self.nome_fase}",
            self.largura // 2, self.altura // 2 - 30,
            (255, 220, 100), 28, centralizado=True
        )
        texto_fase.desenhar()
        
        texto_velocidade = Texto(
            self.tela, f"Velocidade: {self.velocidade_texto}",
            self.largura // 2, self.altura // 2,
            (255, 255, 100), 30, centralizado=True
        )
        texto_velocidade.desenhar()
        
        texto_high_score = Texto(
            self.tela, f"High Score: {self.high_score}",
            self.largura // 2, self.altura // 2 + 30,
            (255, 255, 100), 30, centralizado=True
        )
        texto_high_score.desenhar()
        
        # Desenhar botões
        self.botao_reiniciar.desenhar()
        self.botao_menu.desenhar()
        
        # Indicador de timer
        if self.timer > 0:
            texto_aguarde = Texto(
                self.tela, f"Aguarde... {self.timer/60:.1f}s",
                self.largura // 2, self.altura // 2 + 180,
                (200, 200, 200), 20, centralizado=True
            )
            texto_aguarde.desenhar()
        
        # Novo recorde
        if self.pontuacao == self.high_score and self.pontuacao > 0:
            novo_record = Texto(
                self.tela, "NOVO RECORD!",
                self.largura // 2, self.altura // 2 + 210,
                (255, 255, 100), 28, centralizado=True
            )
            novo_record.desenhar()