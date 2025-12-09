import pygame
from pygame.locals import *
import numpy as np
from sys import exit
import os

pygame.init()

xdoclique,ydoclique = -1,-1
largura_janela, altura_janela = 600, 600
tamanho_celula = 40
largura_rede = largura_janela // tamanho_celula
altura_rede = altura_janela // tamanho_celula
numbombas = 10
clicados = []
bombas = []
bandeiras = []
gameover = False
win = False
FPS = 10
d1 = 0
e2 = 0
xbomb,ybomb = 100,100
xbandeira,ybandeira = 100,100
xnum,ynum = 100,100
redor = 1
mode = 1

tela = pygame.display.set_mode((largura_janela, altura_janela))
clock = pygame.time.Clock()
explosão = pygame.mixer.Sound('explosion-42132 (online-audio-converter.com).wav')

pasta_principal = os.path.dirname(__file__)
bombasheet = pygame.image.load(os.path.join(pasta_principal, 'bombasheet.png')).convert_alpha()
class bomba(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bombasheet.subsurface((0,0), (25,25))
        self.image = pygame.transform.scale(self.image, (25*(tamanho_celula/25),25*(tamanho_celula/25)))
        self.rect = self.image.get_rect()
        self.rect.center = (xbomb +(tamanho_celula/2),ybomb +(tamanho_celula/2))

class bandeira(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bombasheet.subsurface((25,0), (25,25))
        self.image = pygame.transform.scale(self.image, (25*(tamanho_celula/25),25*(tamanho_celula/25)))
        self.rect = self.image.get_rect()
        self.rect.center = (xbandeira +(tamanho_celula/2),ybandeira +(tamanho_celula/2))
        
class numeros(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bombasheet.subsurface(((25*redor)+25,0), (25,25))
        self.image = pygame.transform.scale(self.image, (25*(tamanho_celula/25),25*(tamanho_celula/25)))
        self.rect = self.image.get_rect()
        self.rect.center = (xnum +(tamanho_celula/2),ynum +(tamanho_celula/2))

def atualizar(x,y):
    global gameover,clicados,d1,e2,xdoclique,ydoclique,bombas,bandeiras,xbomb,ybomb,allsprites,mode,tamanho_celula,numbombas,altura_rede,largura_rede
    global rede
    if rede[y][x] == 1:
        fonte2 = pygame.font.SysFont('Arial', 20, True, True)
        mensagem = 'Game over! clique para voltar a jogar'
        texto_formatado = fonte2.render(mensagem, True, (200,0,0))
        ret_texto = texto_formatado.get_rect()
        explosão.play()
        allsprites = pygame.sprite.Group()
        for i in range(largura_rede):
            for j in range(altura_rede):
                if rede[j][i] == 1:
                    xbomb = i*tamanho_celula
                    ybomb = j*tamanho_celula
                    bombaclass = bomba()
                    allsprites.add(bombaclass)

        gameover = True
        while gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if gameover:
                        gameover = False
                        clicados = []
                        d1 = 0
                        e2 = 1
                        xdoclique = -1  
                        ydoclique = -1
                        bombas = []
                        bandeiras = []
                        numbombas = 10
                        tamanho_celula = 40
                        mode = 1
                        altura_rede = altura_janela//tamanho_celula
                        largura_rede = largura_janela//tamanho_celula
                        rede = criar_rede(altura_rede,largura_rede)
            ret_texto.center = (largura_janela//2,altura_janela//2)
            tela.blit(texto_formatado, ret_texto)       
            allsprites.draw(tela)
            allsprites.update()          
            pygame.display.update()

    bandeiras2 = []
    for i in range(0,len(bandeiras)):
        bandeiras2.append(bandeiras[i][0])
        bandeiras2.append(bandeiras[i][1])

    #print(bandeiras2)
    #print(bombas)
    if len(bandeiras2) == len(bombas) or ydoclique == altura_rede-1:
        if sorted(bandeiras2) == sorted(bombas) or (ydoclique == altura_rede-1 and xdoclique == largura_rede-1):
            fonte2 = pygame.font.SysFont('Arial', 20, True, True)
            mensagem = 'veceste o jogo! clique para voltar a jogar'
            texto_formatado = fonte2.render(mensagem, True, (0,150,0))
            ret_texto = texto_formatado.get_rect()

            win = True
            while win:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if win:
                            win = False
                            clicados = []
                            d1 = 0
                            e2 = 1
                            xdoclique = -1  
                            ydoclique = -1
                            bombas = []
                            bandeiras = []
                            numbombas = numbombas*(1+max(0.5**mode,0.2))
                            mode += 1
                            tamanho_celula = max(tamanho_celula-10,25)
                            altura_rede = altura_janela//tamanho_celula
                            largura_rede = largura_janela//tamanho_celula
                            rede = criar_rede(altura_rede,largura_rede)
                ret_texto.center = (largura_janela//2,altura_janela//2)
                tela.blit(texto_formatado, ret_texto)               
                pygame.display.update()

def contarbombas(rede,x,y):
    contar = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= y + i < altura_rede and 0 <= x + j < largura_rede:
                contar += rede[y + i][x + j]
    return contar


def desenhar(tela, rede):
    global xdoclique, ydoclique,d1,xbandeira,ybandeira,xnum,ynum,redor
    tela.fill((255, 255, 255))
    for i in range(0,len(clicados),2):
        pygame.draw.rect(tela, (128,128,128), pygame.Rect(clicados[i]*tamanho_celula,clicados[i+1]*tamanho_celula,tamanho_celula,tamanho_celula))
    if (rede[ydoclique][xdoclique] != 1 and 0 <= xdoclique <largura_rede and 0 <= ydoclique < altura_rede and e2 == 0) or d1 == 1:
        for i in range(largura_rede):
            for j in range(altura_rede):
                if rede[j][i] == 1:
                    continue
                if contarbombas(rede,xdoclique,ydoclique) == 0 or d1 ==1:
                    if contarbombas(rede,i,j) == 0:
                        pygame.draw.rect(tela, (128,128,128), pygame.Rect((i)*tamanho_celula,(j)*tamanho_celula,tamanho_celula,tamanho_celula))
                        d1 = 1

    
    spritesbandeira = pygame.sprite.Group()
    for i in range(len(bandeiras)):
        xbandeira = bandeiras[i][0] *tamanho_celula
        ybandeira = bandeiras[i][1] *tamanho_celula
        bandeiraclass = bandeira()
        spritesbandeira.add(bandeiraclass)
    spritesbandeira.draw(tela)
    spritesbandeira.update()

    spritesnum = pygame.sprite.Group()
    for i in range(0,len(clicados),2):
        xnum = clicados[i] *tamanho_celula
        ynum = clicados[i+1] *tamanho_celula
        redor = min(contarbombas(rede,clicados[i],clicados[i+1]),5)
        if redor != 0:
            numerosclass = numeros()
            spritesnum.add(numerosclass)
    spritesnum.draw(tela)
    spritesnum.update()

    for x in range(0, largura_janela, tamanho_celula):
        pygame.draw.line(tela, (128, 128, 128), (x, 0), (x, altura_janela))
    
    for y in range(0, altura_janela, tamanho_celula):
        pygame.draw.line(tela, (128, 128, 128), (0, y), (largura_janela, y))


    #xdoclique,ydoclique = -1,-1          

def criar_rede(altura_rede, largura_rede):
    rede = np.zeros((altura_rede, largura_rede))
    contar = 0
    valor = 0
    for i in range(altura_rede):
        for j in range(largura_rede):
            if contar >= numbombas:
                rede[i, j] = 0
            else:
                valor = np.random.choice([0, 1], p=[0.9,0.1])
                if valor == 1:
                    contar += 1
                    bombas.append(j),bombas.append(i)
                rede[i, j] = valor
    return rede

rede = criar_rede(altura_rede,largura_rede) 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    xdoclique = event.pos[0]//tamanho_celula
                    ydoclique = event.pos[1]//tamanho_celula
                    clicados.append(xdoclique),clicados.append(ydoclique)
                    atualizar(xdoclique,ydoclique)
                    #print(contarbombas(rede,xdoclique,ydoclique))
                    e2 = 0
                if event.button == 3:
                    if (event.pos[0]//tamanho_celula, event.pos[1]//tamanho_celula) not in bandeiras:
                        bandeiras.append((event.pos[0]//tamanho_celula, event.pos[1]//tamanho_celula))
                        #print(bandeiras)
                    else:
                        bandeiras.remove((event.pos[0]//tamanho_celula, event.pos[1]//tamanho_celula))                    
   
    #print(rede)
    desenhar(tela, rede)
    clock.tick(FPS)
    pygame.display.flip()