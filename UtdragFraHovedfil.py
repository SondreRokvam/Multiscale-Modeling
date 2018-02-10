def modellereRVEsnitt(coordpath, iterasjonsgrense):  # Lage fiber populasjon
    coord = list()  # liste for aa holde koordinatene, koordinatene lagres til coordpath
    books = list()  # liste for aa vite fremgangen paa iterasjonene i  prosessen

    flag = 0
    fVfforrige = 0
    nplassert = 0.0  # antall fiber plassert
    nkrasj = 0  # antall krasj
    sidepunkt = 0
    hjornepunkt = 0
    senterpunkt = 0
    dodpunkt = 0
    # print("dL =", round(dL, 1), "x,y =", round(dL / 2, 1))  # print storrelse og max x,y
    while nplassert < nf:
        frem = countsjikt(
            coord) / nf  # Forlopig fremdrift - antall fibersenter som finnes i RVE/totalt antall fiber (nf)
        fvf = frem * Vf  # Forlopig volumfraksjon

        # se om fiberutplasseringa har mott iterasjonsgrene for krasj og fibere skal shake up
        if nkrasj > iterasjonsgrense:
            # reset systemet for nytt forsok paa utplassering.
            if fVfforrige == fvf:
                flag = flag + 1
            if flag > 5:
                flag = 0
                # print 'Punktene random forflyttes. npp:', nplassert, 'fnnp:', countsjikt(), 'Vf:', round(fvf,3), ' av tot Vf:', Vf, 'tries:', len( books), 'krasjes:', nkrasj,
                coord = shakeitdown(coord)

            else:
                # print 'Punktene random forflyttes ned. npp:', nplassert, 'fnnp:', countsjikt(),'Vf:', round(fvf,3), ' av tot Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj,'# fremdrift stanget:',flag,
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
        if not krasj(x, y, coord) and (sqrt((dL / 2-abs(x)) ** 2 + (dL / 2- abs(y)) ** 2) > ytredodgrense or sqrt((dL / 2-abs(x)) ** 2 + (dL / 2- abs(y)) ** 2) < indredodgrense):
            if ishjornep(x, y):  # Er koordinatet i hjornesone?
                # Krasjer dette hjornepunktet med fiber i de andre hjornene?
                if x < 0 and y < 0 and not krasj(x, y, coord) and not krasj(x + dL, y, coord) and not krasj(x,y+dL, coord) and not krasj(x + dL, y + dL, coord):
                    coord.append([x, y])
                    coord.append([x + dL, y])
                    coord.append([x, y + dL])
                    coord.append([x + dL, y + dL])
                    # print ("ned, ven")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print
                    "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(coord), round(fvf,
                                                                                     3), ' av Vf:', Vf, 'tries:', len(
                        books), 'krasjes:', nkrasj
                    flag = 0
                elif x >= 0 and y < 0 and not krasj(x, y, coord) and not krasj(x - dL, y, coord) and not krasj(x,
                                                                                                               y + dL,
                                                                                                               coord) and not krasj(
                        x - dL, y + dL, coord):
                    coord.append([x, y])
                    coord.append([x - dL, y])
                    coord.append([x, y + dL])
                    coord.append([x - dL, y + dL])
                    # print ("ned, hoy")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print
                    "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(coord), round(fvf,
                                                                                     3), ' av Vf:', Vf, 'tries:', len(
                        books), 'krasjes:', nkrasj
                    flag = 0
                elif x < 0 and y >= 0 and not krasj(x, y, coord) and not krasj(x + dL, y, coord) and not krasj(x,
                                                                                                               y - dL,
                                                                                                               coord) and not krasj(
                        x + dL, y - dL, coord):
                    coord.append((x, y))
                    coord.append((x + dL, y))
                    coord.append((x, y - dL))
                    coord.append((x + dL, y - dL))
                    # print ("opp, ven")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print
                    "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(coord), round(fvf,
                                                                                     3), ' av Vf:', Vf, 'tries:', len(
                        books), 'krasjes:', nkrasj
                    flag = 0
                elif x >= 0 and y >= 0 and not krasj(x, y, coord) and not krasj(x - dL, y, coord) and not krasj(x,
                                                                                                                y - dL,
                                                                                                                coord) and not krasj(
                        x - dL, y - dL, coord):
                    coord.append([x, y])
                    coord.append([x - dL, y])
                    coord.append([x, y - dL])
                    coord.append([x - dL, y - dL])
                    # print ("opp, hoy")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print
                    "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(coord), round(fvf,
                                                                                     3), ' av Vf:', Vf, 'tries:', len(
                        books), 'krasjes:', nkrasj
                    flag = 0
                else:
                    nkrasj = nkrasj + 1


            # Kan koordinatet vere et sidepunkt? Krasjer det med punkter paa motsatt side?
            elif issidep(x, y):
                # print "sidepunkt"
                if x > dL / 2 - indredodgrense and not krasj(x - dL, y, coord):
                    coord.append([x, y])
                    coord.append([x - dL, y])
                    nplassert = nplassert + 1
                    print
                    "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,
                                                                                           3), ' av Vf:', Vf, 'tries:', len(
                        books), 'krasjes:', nkrasj
                    flag = 0
                    sidepunkt = sidepunkt + 1
                    # print ("hoyreside punkt")

                elif x < -dL / 2 + indredodgrense and not krasj(x + dL, y, coord):
                    coord.append([x, y])
                    coord.append([x + dL, y])
                    nplassert = nplassert + 1
                    print
                    "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,
                                                                                           3), ' av Vf:', Vf, 'tries:', len(
                        books), 'krasjes:', nkrasj
                    flag = 0
                    sidepunkt = sidepunkt + 1
                    # print ("venstreside punkt")

                elif y > dL / 2 - indredodgrense and not krasj(x, y - dL, coord):
                    coord.append([x, y])
                    coord.append([x, y - dL])
                    nplassert = nplassert + 1
                    print
                    "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,
                                                                                           3), ' av Vf:', Vf, 'tries:', len(
                        books), 'krasjes:', nkrasj
                    flag = 0
                    sidepunkt = sidepunkt + 1
                    # print ("topp punkt")

                elif y < -dL / 2 + indredodgrense and not krasj(x, y + dL, coord):
                    coord.append([x, y])
                    coord.append([x, y + dL])
                    nplassert = nplassert + 1
                    print
                    "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,
                                                                                           3), ' av Vf:', Vf, 'tries:', len(
                        books), 'krasjes:', nkrasj
                    flag = 0
                    sidepunkt = sidepunkt + 1
                    # print ("bunn punkt")
                else:
                    nkrasj = nkrasj + 1

            #senterpunkt
            elif abs(y) < dL/2-ytredodgrense and abs(x) < dL/2-ytredodgrense:
                coord.append([x, y])
                nplassert = nplassert + 1
                print
                "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,
                                                                                       3), ' av Vf:', Vf, 'tries:', len(
                    books), 'krasjes:', nkrasj
                flag = 0
        else:
            nkrasj = nkrasj + 1
        books.append(nplassert)  # keeping record of amount of tries
    g = open(coordpath, "w")
    for l in range(0, len(coord)):
        g.write(str(coord[l][0]) + '\t' + str(coord[l][1]))
        if l < (len(coord)-1):
            g.write('\n')
    g.close()
    # print str(countsjikt(coord)), 'av nf '+str(nf)
    del flag
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
def krasj(x, y, coord):
    for c in coord:
        xp, yp = c[0], c[1]
        if sqrt((x - xp) ** 2 + (y - yp) ** 2) < 2 * (r + rtol):
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
    for k in range(0, 20):
        t = 0
        for c in coord:
            i = list()
            i.append([dL * 2, dL * 2])
            x, y = c[0], c[1]
            if dL / 2 - ytredodgrense > abs(x) and dL / 2 - ytredodgrense > abs(y):
                coord[t] = i[0]
                for j in range(0, 100):
                    xp, yp = [x + wiggle * random() - wiggle * 0.5, y + wiggle * random() - wiggle * 0.65]
                    if not krasj(xp, yp, coord) and dL / 2 - ytredodgrense > abs(
                            xp) and dL / 2 - ytredodgrense > abs(yp):
                        coord[t] = [xp, yp]
                        break
                    coord[t] = [x, y]
            t = t + 1
    return coord
def shakeitrand(coord):
    for k in range(0, 20):
        t = 0
        for c in coord:
            i = list()
            i.append([dL * 2, dL * 2])
            x, y = c[0], c[1]
            if dL / 2 - ytredodgrense > abs(x) and dL / 2 - ytredodgrense > abs(y):
                coord[t] = i[0]
                for j in range(0, 100):
                    xp, yp = [x + wiggle * random() - wiggle * 0.5, y + wiggle * random() - wiggle * 0.5]
                    if not krasj(xp, yp, coord) and dL / 2 - ytredodgrense > abs(
                            xp) and dL / 2 - ytredodgrense > abs(yp):
                        coord[t] = [xp, yp]
                        break
                    coord[t] = [x, y]
            t = t + 1  # moves to next fiber no matter moved or not
    return coord
