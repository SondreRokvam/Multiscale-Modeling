"""Iterasjons parameter og data"""

global coordpath, Lagrestiffpathprop, lagrestiffpathmod,Envelope,Sigmapaths


coordpath = Tekstfiler + 'RVEcoordinatsandRadiuses' + str(
    int(ParameterSweep[ItraPara])) + '_' + str(Q) + '.txt'  # Skriver ned generert fiberPop for reference.

Lagrestiffpathprop = Tekstfiler + 'Stiffness__NF-' + str( int(nf)) + '.txt'  # Skrives ned statistikk til ett annet script

lagrestiffpathmod = Tekstfiler + 'StiffnessM' + str(int(ParameterSweep[ItraPara])) + '_' + str(
                            Q) + '.txt'  # Lagrer ned Stiffnessmatrix

Envelope = Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn i funksjonen

Sigmapaths = Tekstfiler + 'Sigmas' + str(  int(ParameterSweep[ItraPara])) + '_' + str(Q) + '.txt'



global wiggle, RVEmodellpath

wiggle = random() * rmean  # Omplasseringsgrenser for fiberomplassering

RVEmodellpath = workpath + 'RVEmodel__Parameter-' + str(ParameterSweep[ItraPara]) + '__RandKey-' + str(Q)