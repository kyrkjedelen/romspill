# Importeringer av bibloteker
from math import isclose
import pygame, time, random

# Farger
svart = (0, 0, 0)
hvit = (255, 255, 255)
rod = (255, 0, 0)
gronn = (0, 255, 0)
bla = (0, 0, 255)

# Elementærvinkler
elementaervektor = pygame.math.Vector2(0, -1)

# Initiering
start_vindu_tittel = "Romspill"
start_vindu_storrelse = (800, 800)

vindu = pygame.display.set_mode(start_vindu_storrelse)
(vindustorrelse_x, vindustorrelse_y) = pygame.display.get_surface().get_size()

pygame.display.set_caption(start_vindu_tittel)

pygame.display.update()

# Spillfunksjoner
def int_er_omtrent_like(int1, int2, toleranse):
    return abs(int1 - int2) <= toleranse
def finn_retningsvektor_til_mus(posisjonsvektor):
    musepeker_posisjon = pygame.mouse.get_pos()
    retningsvektor = pygame.math.Vector2(musepeker_posisjon[0] - posisjonsvektor.x, musepeker_posisjon[1] - posisjonsvektor.y)
    retningsvektor.normalize_ip()
    return retningsvektor
def roter(posisjonsvektor_sentrum, overflate, vinkel):
    rotert_overflate = pygame.transform.rotozoom(overflate, vinkel, 1)
    rotert_rect = rotert_overflate.get_rect(center = (posisjonsvektor_sentrum.x, posisjonsvektor_sentrum.y))
    return (rotert_overflate, rotert_rect)
def lastInnBilde(bildeSti, oppløsning):
    return pygame.transform.scale(pygame.image.load(bildeSti).convert_alpha(), oppløsning)
def bildeneErLike(bilder):
    return bilder.count(bilder[0]) == len(bilder)
def summerVektorer(vektorer):
    resultatvektor = pygame.math.Vector2(0, 0)
    for vektor in vektorer:
        resultatvektor.x += vektor.x
        resultatvektor.y += vektor.y
    return resultatvektor


# Spillklasser
class Spiller(pygame.sprite.Sprite):
    def __init__(self, top_fart, akserelasjon, bredde, hoyde, bildesti):
        super().__init__()
        self.tid_akserelasjonstart = 0
        self.tid_akserelasjonslutt = 0
        self.top_fart = top_fart
        self.akserelasjon = akserelasjon
        self.posisjonsvektor_sentrum = pygame.math.Vector2(vindustorrelse_x/2, vindustorrelse_y/2)
        self.retningsvektor = finn_retningsvektor_til_mus(self.posisjonsvektor_sentrum)
        self.originalt_bilde = pygame.transform.scale(pygame.image.load(bildesti), (bredde, hoyde))
        self.image = self.originalt_bilde
        self.rect = self.image.get_rect(center = (self.posisjonsvektor_sentrum.x, self.posisjonsvektor_sentrum.y))
    def startAkserelasjon(self):
        self.tid_akserelasjonstart = time.time()
        self.tid_akserelasjonslutt = 0
    def sluttAkserelasjon(self):
        self.tid_akserelasjonstart = 0
        self.tid_akserelasjonslutt = time.time()
    def beveg(self):
        if int_er_omtrent_like(pygame.mouse.get_pos()[0], self.rect.centerx, 5) and int_er_omtrent_like(pygame.mouse.get_pos()[1], self.rect.centery, 5):
            self.startAkserelasjon()
            return
        tid_naa = time.time()
        t = tid_naa - self.tid_akserelasjonstart
        a = self. akserelasjon
        v = min(a * t, self.top_fart)

        self.posisjonsvektor_sentrum.update(self.posisjonsvektor_sentrum.x + self.retningsvektor.x * v * dt, self.posisjonsvektor_sentrum.y + self.retningsvektor.y * v * dt)

    def pek(self):
        self.retningsvektor = finn_retningsvektor_til_mus(self.posisjonsvektor_sentrum)

        vinkel = self.retningsvektor.angle_to(elementaervektor)
        self.image = pygame.transform.rotozoom(self.originalt_bilde, vinkel, 1)
        self.rect = self.image.get_rect(center = (self.posisjonsvektor_sentrum.x, self.posisjonsvektor_sentrum.y))
    def skyt(self):
        nytt_skudd = Skudd(500, self.retningsvektor, pygame.math.Vector2(self.posisjonsvektor_sentrum), 8, 8)
        skudd_gruppe.add(nytt_skudd)
class Skudd(pygame.sprite.Sprite):
    def __init__(self, fart , retningsvektor, posisjonsvektor_sentrum, bredde, hoyde):
        super().__init__()
        self.fart = fart
        self.posisjonsvektor_sentrum = posisjonsvektor_sentrum
        self.retnignsvektor = retningsvektor
        self.image = pygame.Surface((bredde, hoyde))
        self.image.fill(hvit)
        self.rect = self.image.get_rect(center = (self.posisjonsvektor_sentrum.x, self.posisjonsvektor_sentrum.y))
    def update(self):
        if self.rect.x <= -200 or self.rect.x >= vindustorrelse_x + 200 or self.rect.y <= -200 or self.rect.y >= vindustorrelse_y + 200:
            self.kill()
        else:
            self.posisjonsvektor_sentrum.update(self.posisjonsvektor_sentrum.x + self.retnignsvektor.x * self.fart * dt, self.posisjonsvektor_sentrum.y + self.retnignsvektor.y * self.fart * dt)
            self.rect.centerx = self.posisjonsvektor_sentrum.x
            self.rect.centery = self.posisjonsvektor_sentrum.y
class Maal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
        self.bredde = random.randrange(8, 64)
        self.hoyde = random.randrange(8, 64)
        pos_x = random.randrange(0, vindustorrelse_x - self.bredde)
        pos_y = random.randrange(0, vindustorrelse_x - self.hoyde)
        self.posisjonsvektor = pygame.math.Vector2(pos_x, pos_y)
        self.image = pygame.Surface((self.bredde, self.hoyde))
        self.image.fill(rod)
        self.rect = self.image.get_rect(x = self.posisjonsvektor.x, y = self.posisjonsvektor.y)



# Spillvariabler
siste_tastatur_vektor_med_verdi = pygame.math.Vector2(0, 1)

# Spillgrupper/lister
spiller_gruppe = pygame.sprite.Group()
skudd_gruppe = pygame.sprite.Group()
maal_gruppe = pygame.sprite.Group()
# Spillobjekter
spiller = Spiller(250, 50, 64, 64, "bilder/skip.png")
spiller_gruppe.add(spiller)

for _ in range(20):
    maal_gruppe.add(Maal())

# Tid
clock = pygame.time.Clock()
fps = 60
forrige_tid = time.time()

# Simuleringsløkke
spillKjorer = True
while spillKjorer:
    # Tid
    clock.tick(fps)
    naa = time.time()
    dt = naa - forrige_tid
    forrige_tid = naa

    vindu.fill(svart)
    tastatur_vektorer = []
    tastaturknapper_status = pygame.key.get_pressed()
    if tastaturknapper_status[pygame.K_d]:
        tastatur_vektorer.append(pygame.math.Vector2(1, 0))
    if tastaturknapper_status[pygame.K_a]:
        tastatur_vektorer.append(pygame.math.Vector2(-1, 0))
    if tastaturknapper_status[pygame.K_s]:
        tastatur_vektorer.append(pygame.math.Vector2(0, 1))
    if tastaturknapper_status[pygame.K_w]:
        tastatur_vektorer.append(pygame.math.Vector2(0, -1))

    tastatur_vektor = summerVektorer(tastatur_vektorer)
    if tastatur_vektor.x != 0 or tastatur_vektor.y != 0:
        tastatur_vektor.normalize_ip()
        siste_tastatur_vektor_med_verdi = tastatur_vektor

    spiller.pek()
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            spillKjorer = False
        if hendelse.type == pygame.MOUSEBUTTONDOWN:
            if hendelse.button == pygame.BUTTON_LEFT:
                spiller.skyt()
            if hendelse.button == pygame.BUTTON_RIGHT:
                spiller.startAkserelasjon()
        if hendelse.type == pygame.MOUSEBUTTONUP:
            if hendelse.button == pygame.BUTTON_RIGHT:
                spiller.sluttAkserelasjon()

    museknapper_status = pygame.mouse.get_pressed()
    if museknapper_status[2]:
        spiller.beveg()


    if len(skudd_gruppe.sprites()) > 0 and len(maal_gruppe.sprites()) > 0:
        for maal in maal_gruppe.sprites():
            for skudd in skudd_gruppe.sprites():
                if maal.rect.colliderect(skudd.rect):
                    skudd.kill()
                    maal.kill()

    skudd_gruppe.update()
    skudd_gruppe.draw(vindu)
    maal_gruppe.draw(vindu)
    spiller_gruppe.draw(vindu)
    pygame.display.update()