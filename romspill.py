# Importeringer av bibloteker
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
    def __init__(self, fart, bredde, hoyde, bildesti):
        super().__init__()
        self.fart = fart
        self.posisjonsvektor_sentrum = pygame.math.Vector2(vindustorrelse_x/2, vindustorrelse_y/2)
        self.originalt_bilde = pygame.transform.scale(pygame.image.load(bildesti), (bredde, hoyde))
        self.image = self.originalt_bilde
        self.rect = self.image.get_rect(center = (self.posisjonsvektor_sentrum.x, self.posisjonsvektor_sentrum.y))
    def beveg(self, retningsvektor, pekevektor):
        self.posisjonsvektor_sentrum.update(self.posisjonsvektor_sentrum.x + retningsvektor.x * self.fart * dt, self.posisjonsvektor_sentrum.y + retningsvektor.y * self.fart * dt)
        vinkel = pekevektor.angle_to(elementaervektor)
        self.image = pygame.transform.rotozoom(self.originalt_bilde, vinkel, 1)
        self.rect = self.image.get_rect(center = (self.posisjonsvektor_sentrum.x, self.posisjonsvektor_sentrum.y))
    def skyt(self, retningsvektor):
        nytt_skudd = Skudd(400, retningsvektor, pygame.math.Vector2(self.posisjonsvektor_sentrum), 8, 8)
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

# class maal(Objekt):
#     def __init__():
#         tilfeldigTall = random.randint(8, 32)
#         tilfeldigPosisjonX = random.randint(0, vinduStorrelseX - tilfeldigTall)
#         tilfeldigPosisjonY = random.randint(0, vinduStorrelseY - tilfeldigTall)
#         super().__init__("maal.png", tilfeldigPosisjonX, tilfeldigPosisjonY, tilfeldigTall, tilfeldigTall)

# Spillvariabler
siste_tastatur_vektor_med_verdi = pygame.math.Vector2(1, 0)

# Spillgrupper/lister
spiller_gruppe = pygame.sprite.Group()
skudd_gruppe = pygame.sprite.Group()

# Spillobjekter
spiller = Spiller(100, 64, 64, "skip_lite.png")
spiller_gruppe.add(spiller)

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
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_d]:
        tastatur_vektorer.append(pygame.math.Vector2(1, 0))
    if pressed[pygame.K_a]:
        tastatur_vektorer.append(pygame.math.Vector2(-1, 0))
    if pressed[pygame.K_s]:
        tastatur_vektorer.append(pygame.math.Vector2(0, 1))
    if pressed[pygame.K_w]:
        tastatur_vektorer.append(pygame.math.Vector2(0, -1))

    tastatur_vektor = summerVektorer(tastatur_vektorer)
    if tastatur_vektor.x != 0 or tastatur_vektor.y != 0:
        tastatur_vektor.normalize_ip()
        siste_tastatur_vektor_med_verdi = tastatur_vektor

    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            spillKjorer = False
        if hendelse.type == pygame.KEYDOWN:
            if hendelse.key == pygame.K_SPACE:
                spiller.skyt(siste_tastatur_vektor_med_verdi)

    spiller.beveg(tastatur_vektor, siste_tastatur_vektor_med_verdi)
    skudd_gruppe.update()

    skudd_gruppe.draw(vindu)
    spiller_gruppe.draw(vindu)
    pygame.display.update()