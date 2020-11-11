import numpy as np
import pickle
import random
class Labirinto:
    def __init__(self):
        try:
            (self.paredes, self.quadrados) = pickle.load(open("labirinto.pickle", "rb"))
        except:
            "Nao esqueca de rodar o arquivo GeraLabirinto primeiro para criar o labirinto"
        parede = random.sample(self.paredes, 1)
        self.tam_parede = max(abs(parede[0][0][0] - parede[0][1][0]), abs(parede[0][0][1] - parede[0][1][1]))
        self.sucessores=[]
        for i in range(0, len(self.quadrados)):
            self.sucessores.append([])
        for i in range(0,len(self.quadrados)):
            if ((self.quadrados[i][0], self.quadrados[i][1] + self.tam_parede) in self.quadrados) and (
                    ((self.quadrados[i][0], self.quadrados[i][1] + self.tam_parede), (self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1] + self.tam_parede)) not in self.paredes) and (
                    ((self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1] + self.tam_parede), (self.quadrados[i][0], self.quadrados[i][1] + self.tam_parede)) not in self.paredes):
                self.sucessores[i].append((self.quadrados[i][0],self.quadrados[i][1]+self.tam_parede))
            if ((self.quadrados[i][0], self.quadrados[i][1] - self.tam_parede) in self.quadrados) and (
                    ((self.quadrados[i][0], self.quadrados[i][1]), (self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1])) not in self.paredes) and (
                    ((self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1]), (self.quadrados[i][0], self.quadrados[i][1])) not in self.paredes):
                self.sucessores[i].append((self.quadrados[i][0],self.quadrados[i][1]-self.tam_parede))
            if ((self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1]) in self.quadrados) and (
                    ((self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1]), (self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1] + self.tam_parede)) not in self.paredes) and (
                    ((self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1] + self.tam_parede), (self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1])) not in self.paredes):
                self.sucessores[i].append((self.quadrados[i][0]+self.tam_parede,self.quadrados[i][1]))
            if ((self.quadrados[i][0] - self.tam_parede, self.quadrados[i][1]) in self.quadrados) and (
                    ((self.quadrados[i][0], self.quadrados[i][1]), (self.quadrados[i][0], self.quadrados[i][1] + self.tam_parede)) not in self.paredes) and (
                    ((self.quadrados[i][0], self.quadrados[i][1] + self.tam_parede), (self.quadrados[i][0], self.quadrados[i][1])) not in self.paredes):
                self.sucessores[i].append((self.quadrados[i][0]-self.tam_parede,self.quadrados[i][1]))
        self.visiveis=[]
        for i in range(0, len(self.quadrados)):
            self.visiveis.append([])
        for i in range(0, len(self.quadrados)):
            n=1
            while True:
                if ((self.quadrados[i][0], self.quadrados[i][1] + n*self.tam_parede) in self.quadrados) and (((self.quadrados[i][0], self.quadrados[i][1] + n*self.tam_parede), (self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1] + n*self.tam_parede)) not in self.paredes) and (
                    ((self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1] + n*self.tam_parede), (self.quadrados[i][0], self.quadrados[i][1] + n*self.tam_parede)) not in self.paredes):
                        self.visiveis[i].append((self.quadrados[i][0],self.quadrados[i][1]+n*self.tam_parede))
                else:
                    break
                n+=1
            n=1
            while True:
                if ((self.quadrados[i][0], self.quadrados[i][1] - n*self.tam_parede) in self.quadrados) and (((self.quadrados[i][0], self.quadrados[i][1]-(n-1)*self.tam_parede), (self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1]-(n-1)*self.tam_parede)) not in self.paredes) and (
                    ((self.quadrados[i][0] + self.tam_parede, self.quadrados[i][1]-(n-1)*self.tam_parede),(self.quadrados[i][0], self.quadrados[i][1]-(n-1)*self.tam_parede)) not in self.paredes):
                        self.visiveis[i].append((self.quadrados[i][0], self.quadrados[i][1] - n*self.tam_parede))
                else:
                    break
                n+=1
            n=1
            while True:
                if ((self.quadrados[i][0] + n*self.tam_parede, self.quadrados[i][1]) in self.quadrados) and (((self.quadrados[i][0] + n*self.tam_parede, self.quadrados[i][1]),(self.quadrados[i][0] + n*self.tam_parede, self.quadrados[i][1] + self.tam_parede)) not in self.paredes) and (
                    ((self.quadrados[i][0] + n*self.tam_parede, self.quadrados[i][1] + self.tam_parede),(self.quadrados[i][0] + n*self.tam_parede, self.quadrados[i][1])) not in self.paredes):
                        self.visiveis[i].append((self.quadrados[i][0] + n*self.tam_parede, self.quadrados[i][1]))
                else:
                    break
                n+=1
            n=1
            while True:
                if ((self.quadrados[i][0] - n*self.tam_parede, self.quadrados[i][1]) in self.quadrados) and (((self.quadrados[i][0]-(n-1)*self.tam_parede, self.quadrados[i][1]),(self.quadrados[i][0]-(n-1)*self.tam_parede, self.quadrados[i][1] + self.tam_parede)) not in self.paredes) and (
                    ((self.quadrados[i][0]-(n-1)*self.tam_parede, self.quadrados[i][1] + self.tam_parede),(self.quadrados[i][0]-(n-1)*self.tam_parede, self.quadrados[i][1])) not in self.paredes):
                        self.visiveis[i].append((self.quadrados[i][0] - n*self.tam_parede, self.quadrados[i][1]))
                else:
                    break
                n+=1
        num_linhas=int(self.quadrados[-1][1]/self.tam_parede)
        num_colunas=int(self.quadrados[-1][0]/self.tam_parede)
        self.tabela_q=np.random.uniform(low=-1,high=1,size=(num_linhas,num_colunas,4))
        self.tabela_q_pique_esconde = np.random.uniform(low=-1, high=1, size=(num_linhas, num_colunas,num_linhas, num_colunas, 4))