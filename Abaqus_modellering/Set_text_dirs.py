"""Iterasjons parameter og data"""

global coordpath, Lagrestiffpathprop, lagrestiffpathmod,Envelope,Sigmapaths


coordpath = Tekstfiler+ 'RVE_Coords/RVEcoordinatsandRadiuses' + str(
    int(ParameterSweep)) + '_' + str(Q) + '.txt'  # Skriver ned generert fiberPop for reference.

Lagrestiffpathprop = Tekstfiler + 'Stiffness__InPST-' + str(int(ParameterSweep*9973)) + '.txt'  # Skrives ned statistikk til ett annet script

lagrestiffpathmod = Tekstfiler + 'StiffMat_np/StiffnessM' + str(int(ParameterSweep*scsc)) + '_' + str(
                            Q) +'.npy'  # Lagrer ned Stiffnessmatrix

Envelope = Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn i funksjonen



global wiggle, RVEmodellpath

wiggle = random() * rmean  # Omplasseringsgrenser for fiberomplassering

RVEmodellpath = workpath + 'RVEmodel__Parameter-' + str(key) + '__RandKey-' + str(Q)