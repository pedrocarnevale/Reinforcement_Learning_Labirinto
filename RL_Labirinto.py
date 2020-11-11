import pygame
import matplotlib.pyplot as plt
from individuo import *
from Labirinto import *
pygame.init()
comprimento=500
altura=600
fonte = pygame.font.SysFont("comicsans", 50)
taxa_aprendizado=0.2
desconto=0.95 #o quao importante sao as acoes futuras
episodios=5000
printar_freq=100
epsilon=0.5
INICIO_DECAIMENTO_EPSILON = 1
FIM_DECAIMENTO_EPSILON = episodios//2
janela = pygame.display.set_mode((comprimento, altura))
pygame.display.set_caption('Chegar ao final do labirinto')
decaimento_epsilon=epsilon/(FIM_DECAIMENTO_EPSILON-INICIO_DECAIMENTO_EPSILON)
tabuleiro = Labirinto()
goal=tabuleiro.quadrados[-1]
NAO_MOVER_PENALIDADE=50*tabuleiro.tam_parede*2
FINAL_TABULEIRO_RECOMPENSA=300000
MOVER_PENALIDADE=1
VISITA_VELHO_PENALIDADE=400*tabuleiro.tam_parede**2
VISITA_NOVO_RECOMPENSA=4*tabuleiro.tam_parede**2
estatisticas={'episodio':[], 'media':[],'minimo':[],'maximo':[],'recompensa':[]}

def gerar_estatisticas():
    estatisticas['episodio'].append(episodio)
    estatisticas['recompensa'].append(recompensa_episodio / 1e7)

def distancia_penalidade(agente):
    return (goal[0]-agente.x) + (goal[1]-agente.y)

def redesenhar_janela(texto_episodio,agente):
    janela.fill((0, 0, 0))
    for parede in tabuleiro.paredes:
        pygame.draw.line(janela, (255, 255, 255), parede[0], parede[1], 3)
    pygame.draw.circle(janela,agente.cor,(agente.x+tabuleiro.tam_parede/2,agente.y+tabuleiro.tam_parede/2),agente.raio)
    pygame.draw.circle(janela, (255, 0, 0), (goal[0] + tabuleiro.tam_parede / 2, goal[1] + tabuleiro.tam_parede / 2),tabuleiro.tam_parede / 4)
    janela.blit(texto_episodio,(20,altura*0.9))
    pygame.display.update()

for episodio in range(episodios):
    texto_episodio = fonte.render(f"Episodio: {episodio}", 1, (255, 255,255))
    fps = 60
    clock = pygame.time.Clock()
    executa = True
    tempo=0
    recompensa_episodio=0
    printar=False
    if episodio%printar_freq==0:
        printar=True
    agente=individuo(tabuleiro.quadrados[0][0],tabuleiro.quadrados[0][1],(0,0,255),tabuleiro,10)
    acabou=False
    conseguiu=False
    while executa:
        if printar:
            clock.tick(fps)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executa=False
                pygame.quit()
                plt.plot(estatisticas['episodio'],estatisticas['recompensa'])
                plt.xlabel('Episodio')
                plt.ylabel('Recompensa')
                plt.title('Recompensas ao longo dos episodios')
                plt.show()
                quit()

        if agente.esta_no_destino():
            tempo += 1
            if np.random.random() > epsilon:
                acao = np.argmax(tabuleiro.tabela_q[(int(agente.x/tabuleiro.tam_parede) - 1,int(agente.y/tabuleiro.tam_parede) - 1)])
            else:
                acao = np.random.randint(0,4)
            if agente.x==goal[0] and agente.y==goal[1]:
                print(f'Conseguiu no episodio: {episodio} / Recompensa: {recompensa_episodio}')
                recompensa_episodio=FINAL_TABULEIRO_RECOMPENSA
                executa=False
                gerar_estatisticas()
                break
            elif tempo>=len(tabuleiro.quadrados)*1.5:
                acabou=True
                executa=False
                gerar_estatisticas()
                break
            else:
                if acao==0:
                    agente.destino = (agente.x, agente.y + tabuleiro.tam_parede)
                elif acao==1:
                    agente.destino = (agente.x, agente.y - tabuleiro.tam_parede)
                elif acao== 2:
                    agente.destino = (agente.x+tabuleiro.tam_parede, agente.y)
                elif acao==3:
                    agente.destino = (agente.x-tabuleiro.tam_parede, agente.y)

                if agente.destino in agente.visitado:
                    recompensa_episodio-=VISITA_VELHO_PENALIDADE
                else:
                    agente.visitado.add(agente.destino)
                    recompensa_episodio+=VISITA_NOVO_RECOMPENSA
                if ((agente.destino not in tabuleiro.visiveis[tabuleiro.quadrados.index(agente.quadrado_atual)])
                        and agente.destino != agente.quadrado_atual):
                    recompensa_episodio -= NAO_MOVER_PENALIDADE
                    agente.destino=(agente.x,agente.y)
                else:
                    recompensa_episodio -= distancia_penalidade(agente)
                if not acabou:
                    q_maximo_futuro = np.max(tabuleiro.tabela_q[(int(agente.destino[0]/tabuleiro.tam_parede) - 1,int(agente.destino[1]/tabuleiro.tam_parede) - 1)])  # maior estado futuro
                    q_atual = tabuleiro.tabela_q[(int(agente.x/tabuleiro.tam_parede) - 1,int(agente.y/tabuleiro.tam_parede) - 1,acao)]
                    novo_q = (1 - taxa_aprendizado) * q_atual + taxa_aprendizado * (recompensa_episodio + desconto * q_maximo_futuro)
                    tabuleiro.tabela_q[(int(agente.x/tabuleiro.tam_parede) - 1,int(agente.y/tabuleiro.tam_parede) - 1,acao)] =novo_q
                agente.mover()
        else:
            agente.mover()
        if FIM_DECAIMENTO_EPSILON >= episodio and episodio >= INICIO_DECAIMENTO_EPSILON:
            epsilon -= decaimento_epsilon
        if printar:
            redesenhar_janela(texto_episodio,agente)
