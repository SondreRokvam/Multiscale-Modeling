#Lage modeller
def modellereRVEsnitt():  # Lage fiber populasjon
    coord = list()  # liste for aa holde koordinatene, koordinatene lagres til coordpath
    books = list()  # liste for aa vite fremgangen paa iterasjonene i  prosessen
    Iterasjonsflag = 0
    fVfforrige = 0
    nplassert = 0.0  # antall fiber plassert
    nkrasj = 0  # antall krasj
    sidepunkt = 0
    hjornepunkt = 0
    senterpunkt = 0
    while nplassert < nf:
        if Fibervariation:  # Radiusene fordeles med variasjoner
            r= radiuser[int(nplassert)]
            gtol = Rclearing * r  # Dodsone klaring toleranse
            ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene
            indredodgrense = r - gtol  # Dodzone avstand, naermest kantene

        frem = countsjikt(coord) / nf  # Forlopig fremdrift - antall fibersenter som finnes i RVE/totalt antall fiber (nf)
        fvf = frem * Vf  # Forlopig volumfraksjon

        # se om fiberutplasseringa har mott iterasjonsgrene for krasj og fibere skal shake up
        if nkrasj > iterasjonsgrense:
            # reset systemet for nytt forsok paa utplassering.
            if fVfforrige == fvf:
                Iterasjonsflag = Iterasjonsflag + 1
            if Iterasjonsflag > 5:
                Iterasjonsflag = 0
                coord = shakeitdown(coord)

            else:
                coord = shakeitdown(coord)
            fVfforrige = fvf
            nkrasj = 0

        # genererer nye fiberkoordinater"
        if nf <= 1:
            x = 0.0
            y = 0.0
        else:
            x = dL * random() - dL * 0.5
            y = dL * random() - dL * 0.5
        # sjekke krasj mot tidligere fiber, at avstand mot hjornet er utenfor eller innenfor doedsonegrensene for hjornet og at avstand fra sidene er over og under doedsonegrensene for kantene.
        if not krasj(x, y,r, coord) and (sqrt((dL / 2-abs(x)) ** 2 + (dL / 2- abs(y)) ** 2) > ytredodgrense or sqrt((dL / 2-abs(x)) ** 2 + (dL / 2- abs(y)) ** 2) < indredodgrense) and (abs(x)>dL/2-indredodgrense or abs(x)<dL/2-ytredodgrense):
            if ishjornep(x, y):  # Er koordinatet i hjornesone?
                # Krasjer dette hjornepunktet med fiber i de andre hjornene?
                if x < 0 and y < 0 and not krasj(x, y,r, coord) and not krasj(x + dL, y,r, coord) and not krasj(x,y+dL,r, coord) and not krasj(x + dL, y + dL,r, coord):
                    coord.append([x, y,r])
                    coord.append([x + dL, y,r])
                    coord.append([x, y + dL,r])
                    coord.append([x + dL, y + dL,r])
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    printprog(coord, fvf, nkrasj, books)
                    Iterasjonsflag = 0
                elif x >= 0 and y < 0 and not krasj(x, y,r, coord) and not krasj(x - dL, y,r, coord) and not krasj(x,y + dL,r,coord) and not krasj(x - dL, y + dL,r, coord):
                    coord.append([x, y,r])
                    coord.append([x - dL, y,r])
                    coord.append([x, y + dL,r])
                    coord.append([x - dL, y + dL,r])
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    printprog(coord, fvf, nkrasj, books)
                    Iterasjonsflag = 0
                elif x < 0 and y >= 0 and not krasj(x, y,r, coord) and not krasj(x + dL, y,r, coord) and not krasj(x,y - dL,r,coord) and not krasj(x + dL, y - dL,r, coord):
                    coord.append([x, y,r])
                    coord.append([x + dL, y,r])
                    coord.append([x, y - dL,r])
                    coord.append([x + dL, y - dL,r])
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    printprog(coord, fvf, nkrasj, books)
                    Iterasjonsflag = 0
                elif x >= 0 and y >= 0 and not krasj(x, y,r, coord) and not krasj(x - dL, y,r, coord) and not krasj(x,y - dL,r,coord) and not krasj(x - dL, y - dL,r, coord):
                    coord.append([x, y,r])
                    coord.append([x - dL, y,r])
                    coord.append([x, y - dL,r])
                    coord.append([x - dL, y - dL,r])
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    printprog(coord, fvf, nkrasj, books)
                    Iterasjonsflag = 0
                else:
                    nkrasj = nkrasj + 1

            # Kan koordinatet vere et sidepunkt? Krasjer det med punkter paa motsatt side?
            elif issidep(x, y):
                if x > dL / 2 - indredodgrense and not krasj(x - dL, y,r, coord):
                    coord.append([x, y,r])
                    coord.append([x - dL, y,r])
                    nplassert = nplassert + 1
                    printprog(coord, fvf, nkrasj, books)
                    Iterasjonsflag = 0
                    sidepunkt = sidepunkt + 1

                elif x < -dL / 2 + indredodgrense and not krasj(x + dL, y,r, coord):
                    coord.append([x, y,r])
                    coord.append([x + dL, y,r])
                    nplassert = nplassert + 1
                    printprog(coord, fvf, nkrasj, books)
                    Iterasjonsflag = 0
                    sidepunkt = sidepunkt + 1

                elif y > dL / 2 - indredodgrense and not krasj(x, y - dL,r, coord):
                    coord.append([x, y,r])
                    coord.append([x, y - dL,r])
                    nplassert = nplassert + 1
                    printprog(coord, fvf, nkrasj, books)
                    Iterasjonsflag = 0
                    sidepunkt = sidepunkt + 1

                elif y < -dL / 2 + indredodgrense and not krasj(x, y + dL,r, coord):
                    coord.append([x, y,r])
                    coord.append([x, y + dL,r])
                    nplassert = nplassert + 1
                    printprog(coord, fvf, nkrasj, books)
                    Iterasjonsflag = 0
                    sidepunkt = sidepunkt + 1
                else:
                    nkrasj = nkrasj + 1

            #senterpunkt
            elif abs(y) < dL/2-ytredodgrense and abs(x) < dL/2-ytredodgrense:
                coord.append([x, y,r])
                nplassert = nplassert + 1
                senterpunkt = senterpunkt + 1
                printprog(coord, fvf, nkrasj, books)
                Iterasjonsflag = 0
        else:
            nkrasj = nkrasj + 1
        books.append(nplassert)  # keeping record of amount of tries
    g = open(coordpath, "w")
    for l in range(0, len(coord)):
        g.write(str(coord[l][0]) + '\t' + str(coord[l][1]) + '\t' + str(coord[l][2]))
        if l < (len(coord)-1):
            g.write('\n')
    g.close()
    del Iterasjonsflag
    del fVfforrige
    del nplassert  # antall fiber plassert
    del nkrasj  # antall krasj
    del coord
    del books

#Stotte funsjoner til modellere RVE
def countsjikt(coord):
    i_sjikt = 0.0
    for i in range(len(coord)):
        if abs(coord[i][0]) <= dL / 2 and abs(coord[i][1]) <= dL / 2:
            i_sjikt = i_sjikt + 1.0
    return i_sjikt

def krasj(x, y,rf, coord):
    for c in coord:
        xp, yp,r = c[0], c[1],rmean
        rtol = Rclearing * r  # Mellomfiber toleranse
        if Fibervariation:  # Radiusene fordeles med variasjoner
            xp, yp, r=c[0], c[1], (c[2]+rf)/2
            rtol = Rclearing * r  # Mellomfiber toleranse
        if sqrt((x - xp) ** 2 + (y - yp) ** 2) < 2 * r + rtol:
            return True

    return False
def issidep(x, y):
    if abs(x) > dL / 2 - indredodgrense and abs(y) < dL / 2 - ytredodgrense:
        return True
    elif abs(x) < dL / 2 - ytredodgrense and abs(y) > dL / 2 - indredodgrense:
        return True
    return False
def ishjornep(x, y):
    if abs(x) > dL / 2 - indredodgrense and abs(y) > dL / 2 - indredodgrense:
        return True
    else:
        return False
def shakeitdown(coord):
    for k in range(0, 10):
        t = 0
        for c in coord:
            i = list()
            i.append([dL * 2, dL * 2])
            x, y = c[0], c[1]
            r =rmean
            gtol = Rclearing * r  # Dodsone klaring toleranse
            ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene
            if Fibervariation:  # Radiusene fordeles med variasjoner
                r = c[2]
                gtol = Rclearing * r  # Dodsone klaring toleranse
                ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene

            if dL / 2 - ytredodgrense > abs(x) and dL / 2 - ytredodgrense > abs(y):
                coord[t] = [i[0][0],i[0][1],rmean]
                for j in range(0, 50):
                    xp, yp = [x + wiggle * random() - wiggle * 0.5, y + wiggle * random() - wiggle * 0.65]
                    if not krasj(xp, yp,r, coord) and dL / 2 - ytredodgrense > abs(xp) and dL / 2 - ytredodgrense > abs(yp):
                        coord[t] = [xp, yp,r]
                        break
                    coord[t] = [x, y,r]
            t = t + 1
    return coord
def shakeitrand(coord):
    for k in range(0, 10):
        t = 0
        for c in coord:
            i = list()
            i.append([dL * 2, dL * 2])
            x, y = c[0], c[1]
            r =rmean
            gtol = Rclearing * r  # Dodsone klaring toleranse
            ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene
            if Fibervariation:  # Radiusene fordeles med variasjoner
                r = c[2]
                gtol = Rclearing * r  # Dodsone klaring toleranse
                ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene

            if dL / 2 - ytredodgrense > abs(x) and dL / 2 - ytredodgrense > abs(y):
                coord[t] = i[0]
                for j in range(0, 50):
                    xp, yp = [x + wiggle * random() - wiggle * 0.5, y + wiggle * random() - wiggle * 0.5]
                    if not krasj(xp, yp,r, coord) and dL / 2 - ytredodgrense > abs(
                            xp) and dL / 2 - ytredodgrense > abs(yp):
                        coord[t] = [xp, yp,r]
                        break
                    coord[t] = [x, y,r]
            t = t + 1
    return coord
def printprog(coord,fvf,nkrasj,books):
    print 'Fiber added! Fiber =', countsjikt(coord), 'av nf = ', nf, 'Koordinater = ', len(coord),' Vf = ',round(
        fvf, 3), ' av ', Vf, ' Krasjes:', nkrasj, 'Tries:', len(books)

    # Radiusene fordeles med variasjoner
if Fibervariation:
    radiuser = []
    for fib in range(0, nf):
        radiuser.append(gauss(rmean, Rstdiv))
modellereRVEsnitt()
fA = []
for radius in radiuser:
    fA.append(pi * radius ** 2)
print 'Modelled Vf = '+str(round(float(np.sum(fA) / dL ** 2),4))