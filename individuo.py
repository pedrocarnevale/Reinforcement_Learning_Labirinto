class individuo:
    def __init__(self,x,y,cor,labirinto,vel):
        self.x=x
        self.y=y
        self.labirinto = labirinto
        self.raio=self.labirinto.tam_parede/4
        self.cor=cor
        self.vel=vel
        self.caminho=[(self.x,self.y)]
        self.visitado=set()
        self.destino=(self.x,self.y)
        self.quadrado_atual=(self.x,self.y)
        self.batendo=False
        self.bater_deslocamento=0

    def atualiza_quadrado_atual(self):
        if self.destino[0] == self.x and self.destino[1] > self.y:
            if self.destino[1]-self.y<self.labirinto.tam_parede/2:
                self.quadrado_atual=self.destino
            else:
                self.quadrado_atual=(self.destino[0],self.destino[1]-self.labirinto.tam_parede)
        elif self.destino[0] == self.x and self.destino[1] < self.y:
            if self.y-self.destino[1]<self.labirinto.tam_parede/2:
                self.quadrado_atual=self.destino
            else:
                self.quadrado_atual=(self.destino[0],self.destino[1]+self.labirinto.tam_parede)
        elif self.destino[0] > self.x and self.destino[1] == self.y:
            if self.destino[0]-self.x<self.labirinto.tam_parede/2:
                self.quadrado_atual=self.destino
            else:
                self.quadrado_atual=(self.destino[0]-self.labirinto.tam_parede,self.destino[1])
        elif self.destino[0] < self.x and self.destino[1] == self.y:
            if self.x-self.destino[0]<self.labirinto.tam_parede/2:
                self.quadrado_atual=self.destino
            else:
                self.quadrado_atual=(self.destino[0]+self.labirinto.tam_parede,self.destino[1])

    def esta_no_destino(self):
        if (self.x < self.destino[0] and self.x + 0.0001 > self.destino[0]) or (self.y < self.destino[1] and self.y + 0.0001 > self.destino[1]):
            self.x=round(self.x)
            self.y=round(self.y)
        if (self.x > self.destino[0] and self.x - 0.0001 < self.destino[0]) or (self.y > self.destino[1] and self.y - 0.0001 < self.destino[1]):
            self.x=round(self.x)
            self.y=round(self.y)
        self.atualiza_quadrado_atual()
        return (self.x==self.destino[0] and self.y==self.destino[1])

    def mover(self):
        delta=self.labirinto.tam_parede / self.vel
        if self.destino[0] == self.x and self.destino[1] > self.y:
            self.y += delta
        elif self.destino[0] == self.x and self.destino[1] < self.y:
            self.y -= delta
        elif self.destino[0] > self.x and self.destino[1] == self.y:
            self.x += delta
        elif self.destino[0] < self.x and self.destino[1] == self.y:
            self.x -= delta
        return delta






