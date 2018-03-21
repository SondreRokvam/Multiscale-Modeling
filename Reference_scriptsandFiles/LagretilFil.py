
#Lagre parametere til stottefiler
lagreparametere(Q)


def lagreparametere(Q):
    g = open(parameterpath, "w")

    parametere = [Q, r, nf, Vf, wiggle, coordpath, iterasjonsgrense, rtol, gtol, dL]
    print parametere, '\nQ\tr\tnf\tVf\twiggle\t\tcoordpath\t\t\t\titerasjonsgrense\trtol\tgtoL\tdL'
    g.write('Q' + '\t' + 'r' + '\t' + 'nf' + '\t' + 'Vf' + '\t' + 'wiggle' + '\t' + 'coordpath' + '\t' + 'iterasjonsgrense' + '\t' + 'rtol' + '\t' + 'gtol' + '\t' + 'dL' + '\n' +
        str(Q) + '\t' + str(r) + '\t' + str(nf) + '\t' + str(Vf) + '\t' + str(
            wiggle) + '\t' + coordpath + '\t' + str(iterasjonsgrense) + '\t' + str(rtol) + '\t' + str(
            gtol) + '\t' + str(dL))  # til fiber modellering
    g.close()
