import pygame
import math
import matplotlib.pyplot as plt
from individuo import *
from Labirinto import *
pygame.init()
comprimento=500
altura=600
fps = 60
fonte = pygame.font.SysFont("comicsans", 50)
taxa_aprendizado=0.8
desconto=0.95
episodios=5000
printar_freq=500
epsilon=0.95
INICIO_DECAIMENTO_EPSILON = 1
FIM_DECAIMENTO_EPSILON = episodios
janela = pygame.display.set_mode((comprimento, altura))
pygame.display.set_caption('Chegar ao final do labirinto')
decaimento_epsilon=epsilon/(FIM_DECAIMENTO_EPSILON-INICIO_DECAIMENTO_EPSILON)
tabuleiro = Labirinto()
meta=tabuleiro.quadrados[-1]
BATER_PAREDE_PENALIDADE=500*(int(math.sqrt(len(tabuleiro.quadrados))))
FINAL_TABULEIRO_RECOMPENSA=300*int(math.sqrt(len(tabuleiro.quadrados)))
VISITA_VELHO_PENALIDADE=40000*int(math.sqrt(len(tabuleiro.quadrados)))
VISITA_NOVO_RECOMPENSA=40000*int(math.sqrt(len(tabuleiro.quadrados)))
LIMITE_EPISODIO=len(tabuleiro.quadrados)*1.5
estatisticas={'episodio':[],'recompensa':[]}

#funcao para gerar as estatisticas no final da execucao do programa
def gerar_estatisticas():
    estatisticas['episodio'].append(episodio)
    estatisticas['recompensa'].append(recompensa_episodio / 1e7)

#funcao da penalidade da distancia ate a saida do labirinto
def distancia_penalidade(agente):
    return ((meta[0]-agente.x) + (meta[1]-agente.y))*int(math.sqrt(len(tabuleiro.quadrados)))

def valor_tabela_q(x,y,acao=None):
    return tabuleiro.tabela_q[(int(x/tabuleiro.tam_parede) - 1,int(y/tabuleiro.tam_parede) - 1,acao)]

def bater_parede(printar,agente,texto_episodio):
    if printar:
        for p in range(0, int(agente.vel/4)):
            agente.mover()
            redesenhar_janela(texto_episodio, agente)
            pygame.time.delay(1000 // fps)
    agente.destino = (agente.quadrado_atual[0], agente.quadrado_atual[1])
    if printar:
        for p in range(0, int(agente.vel/4)):
            agente.mover()
            redesenhar_janela(texto_episodio, agente)
            pygame.time.delay(1000 // fps)

#funcao para gerar a interface grafica
def redesenhar_janela(texto_episodio,agente):
    janela.fill((0, 0, 0))
    for parede in tabuleiro.paredes:
        pygame.draw.line(janela, (255, 255, 255), parede[0], parede[1], 3)
    pygame.draw.circle(janela,agente.cor,(agente.x+tabuleiro.tam_parede/2,agente.y+tabuleiro.tam_parede/2),agente.raio)
    pygame.draw.circle(janela, (255, 0, 0), (meta[0] + tabuleiro.tam_parede / 2, meta[1] + tabuleiro.tam_parede / 2),tabuleiro.tam_parede / 4)
    janela.blit(texto_episodio,(20,altura*0.9))
    pygame.display.update()

def encerrar_programa(executa):
    executa = False
    pygame.quit()
    plt.plot(estatisticas['episodio'], estatisticas['recompensa'])
    plt.xlabel('Episodio')
    plt.ylabel('Recompensa')
    plt.title('Recompensas ao longo dos episodios')
    plt.show()
    quit()

#main
for episodio in range(episodios):
    print(episodio)
    texto_episodio = fonte.render(f"Episodio: {episodio}", 1, (255, 255,255))
    clock = pygame.time.Clock()
    executa = True
    printar=False
    if episodio%printar_freq==0 and episodio!=0:
        printar=True
    tempo=0
    recompensa_episodio=0
    agente=individuo(tabuleiro.quadrados[0][0],tabuleiro.quadrados[0][1],(0,0,255),tabuleiro,10)
    acabou=False
    conseguiu=False

    while executa:
        if printar:
            clock.tick(fps)
        for evento in pygame.event.get():
            #se a janela da interface grafica for fechada
            if evento.type == pygame.QUIT:
                encerrar_programa(executa)

        #se o agente chegou na localizacao que estava se deslocando
        if agente.esta_no_destino():
            tempo += 1
            #verifica se o agente tomara um movimento aleatorio ou baseado no aprendizado
            numero= np.random.random()
            if  numero > epsilon:
                acao = np.argmax(tabuleiro.tabela_q[(int(agente.x/tabuleiro.tam_parede) - 1,int(agente.y/tabuleiro.tam_parede) - 1)])
            else:
                acao = np.random.randint(0,4)

            #verifica se chegou na saida do labirinto
            if agente.x==meta[0] and agente.y==meta[1]:
                recompensa_episodio+=FINAL_TABULEIRO_RECOMPENSA
                print(f'Conseguiu no episodio: {episodio} / Recompensa: {recompensa_episodio}')
                executa=False
                gerar_estatisticas()
                break

            #verifica se chegou ao limite do episodio
            elif tempo>=LIMITE_EPISODIO:
                acabou=True
                executa=False
                gerar_estatisticas()
                break

            #caso nao tenha chegado nem no fim do labirinto nem no fim do episodio, o agente se movimenta
            else:
                if acao==0:
                    agente.destino = (agente.x, agente.y + tabuleiro.tam_parede)
                elif acao==1:
                    agente.destino = (agente.x, agente.y - tabuleiro.tam_parede)
                elif acao== 2:
                    agente.destino = (agente.x+tabuleiro.tam_parede, agente.y)
                elif acao==3:
                    agente.destino = (agente.x-tabuleiro.tam_parede, agente.y)

                #penalidade por visitar uma posicao ja visitada anteriormente
                if agente.destino in agente.visitado:
                    recompensa_episodio-=VISITA_VELHO_PENALIDADE

                #recompensa por visitar uma nova posicao
                else:
                    agente.visitado.add(agente.destino)
                    recompensa_episodio+=VISITA_NOVO_RECOMPENSA

                #penalidade por se deslocar a uma posicao bloqueada por uma parede
                if ((agente.destino not in tabuleiro.visiveis[tabuleiro.quadrados.index(agente.quadrado_atual)])
                        and agente.destino != agente.quadrado_atual):
                    recompensa_episodio -= BATER_PAREDE_PENALIDADE
                    bater_parede(printar,agente,texto_episodio)
                else:
                    recompensa_episodio -= distancia_penalidade(agente)

                #equacao para atualizar os valores da tabela do algoritmo q_learning
                if not acabou:
                    q_maximo_futuro = np.max(valor_tabela_q(agente.destino[0],agente.destino[1]))
                    q_atual = valor_tabela_q(agente.x,agente.y,acao) 
                    novo_q = (1 - taxa_aprendizado) * q_atual + taxa_aprendizado * (recompensa_episodio + desconto * q_maximo_futuro)
                    tabuleiro.tabela_q[(int(agente.x/tabuleiro.tam_parede) - 1,int(agente.y/tabuleiro.tam_parede) - 1,acao)] =novo_q
                agente.mover()
        else:
            agente.mover()

        #altera o valor de epsilon
        if FIM_DECAIMENTO_EPSILON >= episodio and episodio >= INICIO_DECAIMENTO_EPSILON:
            epsilon -= decaimento_epsilon

        if printar:
            redesenhar_janela(texto_episodio,agente)
