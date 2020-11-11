import pygame
import random
import pickle
pygame.init()
comprimento=500
altura=600
NUM_LINHAS_LABIRINTO=10
NUM_COLUNAS_LABIRINTO=10
TAMANHO_LADO_PAREDE=40
janela=pygame.display.set_mode((comprimento,altura))
pygame.display.set_caption('Labirinto')
clock=pygame.time.Clock()
quadrados=[]
paredes=set()
def grid(num_linhas,num_colunas,delta):
    x=0
    y=0
    for i in range(0,num_linhas):
        x = delta
        y+=delta
        for j in range(0,num_colunas):
            if ((x,y+delta),(x,y)) not in paredes:
                paredes.add(((x,y),(x,y+delta)))
            if((x+delta,y+delta),(x,y+delta)) not in paredes:
                paredes.add(((x, y+delta), (x+delta, y + delta)))
            if((x+delta,y),(x+delta,y+delta)) not in paredes:
                paredes.add(((x+delta, y+delta), (x+delta,y)))
            if((x,y),(x+delta,y)) not in paredes:
                paredes.add(((x+delta, y), (x, y)))
            quadrados.append((x,y))
            x += delta
    visitado=set()
    labirinto(delta,delta,delta,visitado)

def labirinto(x,y,delta,visitado):
    visitado.add((x,y))
    possibilidades=[1,2,3,4]
    while len(possibilidades)!=0:
        escolha=random.choice(possibilidades)
        if escolha==1:
            possibilidades.remove(1)
            if ((x,y+delta) in quadrados) and ((x,y+delta) not in visitado):
                try:
                    paredes.remove(((x,y+delta),(x+delta,y+delta)))
                except:
                    paredes.remove(((x+delta,y+delta),(x,y+delta)))
                labirinto(x,y+delta,delta,visitado)
        elif escolha==2:
            possibilidades.remove(2)
            if ((x,y-delta) in quadrados) and ((x,y-delta) not in visitado):
                try:
                    paredes.remove(((x, y), (x+delta, y)))
                except:
                    paredes.remove(((x+delta,y),(x,y)))
                labirinto(x,y-delta,delta,visitado)
        elif escolha==3:
            possibilidades.remove(3)
            if ((x+delta,y) in quadrados) and ((x+delta,y) not in visitado):
                try:
                    paredes.remove(((x+delta, y), (x+delta, y + delta)))
                except:
                    paredes.remove(((x + delta, y+delta), (x + delta,y)))
                labirinto(x+delta,y,delta,visitado)
        elif escolha==4:
            possibilidades.remove(4)
            if ((x-delta,y) in quadrados) and ((x-delta,y) not in visitado):
                try:
                    paredes.remove(((x, y), (x, y + delta)))
                except:
                    paredes.remove(((x,y+delta),(x,y)))
                labirinto(x-delta,y,delta,visitado)
def desenha_labirinto():
    for parede in paredes:
        pygame.draw.line(janela,(255,255,255),parede[0],parede[1])
def main():
    run=True
    janela.fill((0,0,0))
    grid(NUM_LINHAS_LABIRINTO,NUM_COLUNAS_LABIRINTO,TAMANHO_LADO_PAREDE)
    desenha_labirinto()
    pickle.dump((paredes,quadrados), open("labirinto.pickle", "wb"))
    while run:
        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                print(quadrados)
                run=False
                pygame.quit()
                quit()
        pygame.display.update()
main()


