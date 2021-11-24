import pylhe
import vector as v
import numpy as np

class id:
    def __init__(self):
        #Quarks
        self.d = 1
        self.u = 2
        self.s = 3
        self.c = 4
        self.b = 5
        self.t = 6
        #Leptons
        self.e = 11
        self.ve = 12
        self.mu = 13
        self.vmu = 14
        self.tau = 15
        self.vtau = 18
        #Gauge and Higgs bosons
        self.g = 21
        self.gamma = 22
        self.Z = 23
        self.Wp = 24
        self.H = 25
        pass

    @property
    def electron(self):
        return self.e

    @property
    def muon(self):
        return self.mu

    @property
    def photon(self):
        return self.gamma

    @property
    def y(self):
        return self.gamma

    @property
    def gluon(self):
        return self.g

    @property
    def gl(self):
        return self.g

    @property
    def quarks(self):
        return [self.d, self.u, self.s, self.c, self.b, self.t]

    @property
    def leptons(self):
        return [self.e, self.mu, self.tau]

    @property
    def antileptons(self):
        return [-1*l for l in self.leptons]

    @property
    def antiquarks(self):
        return [-1*q for q in self.quarks]

    @property
    def neutrinos(self):
        return [self.ve, self.vmu, self.vtau]

    @property
    def antineutrinos(self):
        return [-1*v for v in self.neutrinos]

    def isQuark(self, id):
        return any(id == x for x in (self.quarks+self.antiquarks))

    def isLepton(self, id):
        return any(id == x for x in (self.leptons+self.antileptons))

    def isNeutrino(self, id):
        return any(id == x for x in (self.neutrinos+self.antineutrinos))

    def isB(self, id):
        return any(id == x for x in (self.b, -1*self.b))

    def isHiggs(self, id):
        return id == self.H

    def isGluon(self, id):
        return id == self.gluon

ID = id()

def get_4vect(p):
    return v.obj(e=p.e, px=p.px, py=p.py, pz=p.pz)

def getQuantities(evt):
    ret_dict = {
        'vbf_vmu_pt': [],
        'vbf_vmu_pz': [],
        'MET': [],
        'MEL': [],
        'nb': [],
        'ngluons': [],
        'ne': [],
        'nmu': [],
        'ntau': [],
        'nlep': [],
        'mtautau': [],
        'mee': [],
        'mmumu': [],
    }

    #Other event-level quantities to fill
    vs_fvec = []
    nb = 0
    ngluons=0
    ne,nmu,ntau,nlep=0,0,0,0
    tautau_fvec=None
    ee_fvec=None
    mumu_fvec=None

    #Looping over particles
    for p in evt.particles:
        id, st, mother1, mother2, fvec = int(p.id), int(
            p.status), int(p.mother1), int(p.mother2), get_4vect(p)

        ##########
        #Filling final state particles
        ##########
        if int(st) == 1:
            #Compute quantities here
            if abs(id) == ID.vmu:
                ret_dict['vbf_vmu_pz'] += [abs(fvec.pz)]
                ret_dict['vbf_vmu_pt'] += [fvec.pt]
            if ID.isNeutrino(id):
                vs_fvec += [fvec]
            if ID.isB(id):
                nb += 1
            if ID.isGluon(id):
                ngluons += 1
            if ID.isLepton(id):
                nlep += 1
                if id in [ID.e,-1*ID.e]:
                    ne+=1
                    if    ee_fvec is None: ee_fvec=fvec
                    else: ee_fvec = ee_fvec+fvec
                if id in [ID.muon,-1*ID.muon]:
                    nmu+=1
                    if    mumu_fvec is None: mumu_fvec=fvec
                    else: mumu_fvec = mumu_fvec+fvec
                if id in [ID.tau,-1*ID.tau]:
                    ntau+=1
                    if    tautau_fvec is None: tautau_fvec=fvec
                    else: tautau_fvec = tautau_fvec+fvec

    #Fill event-level quantities
    if len(vs_fvec) > 0:
        # Missing Momentum quantities
        _met_fvec = vs_fvec[0]
        for i in range(1, len(vs_fvec)):
            _met_fvec = _met_fvec+vs_fvec[i]
        ret_dict['MET'] += [_met_fvec.pt]
        ret_dict['MEL'] += [abs(_met_fvec.pz)]
    ret_dict['nb'] += [nb]
    ret_dict['ngluons'] += [ngluons]
    ret_dict['nlep'] += [nlep]
    ret_dict['ne'] += [ne]
    ret_dict['nmu'] += [nmu]
    ret_dict['ntau'] += [ntau]
    if ntau==2:  ret_dict['mtautau'] += [tautau_fvec.mass]
    if ne==2:    ret_dict['mee']     += [ee_fvec.mass]
    if nmu == 2: ret_dict['mmumu']   += [mumu_fvec.mass]

    return ret_dict

def fillHistograms(values, lhe_file):
    if isinstance(lhe_file,str):
        lhe_file = pylhe.readLHE(lhe_file)
    for evt in lhe_file:
        qs = getQuantities(evt)
        for name, v_dict in values.items():
            v_dict['vals'] += qs[name]
    pass
