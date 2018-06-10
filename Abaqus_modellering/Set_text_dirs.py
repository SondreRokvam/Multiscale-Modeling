"""Iterasjons parameter og data"""

global coordpath, Lagrestiffpathprop, lagrestiffpathmod,Envelope,Sigmapaths


coordpath = Tekstfiler + 'RVEcoordinatsandRadiuses' + str(
    int(ParameterSweep)) + '_' + str(Q) + '.txt'  # Skriver ned generert fiberPop for reference.

Lagrestiffpathprop = Tekstfiler + 'Stiffness__InY-' + str(int(ParameterSweep*9973)) + '.txt'  # Skrives ned statistikk til ett annet script

lagrestiffpathmod = Tekstfiler + 'StiffnessM' + str(int(ParameterSweep*scsc)) + '_' + str(
                            Q) +'.npy'  # Lagrer ned Stiffnessmatrix

Envelope = Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn i funksjonen

Sigmapaths = Tekstfiler + 'Sigmas' + str(int(ParameterSweep*scsc)) + '_' + str(Q) + '.txt'


global wiggle, RVEmodellpath

wiggle = random() * rmean  # Omplasseringsgrenser for fiberomplassering

RVEmodellpath = workpath + 'RVEmodel__Parameter-' + str(int(ParameterSweep*scsc)) + '__RandKey-' + str(Q)