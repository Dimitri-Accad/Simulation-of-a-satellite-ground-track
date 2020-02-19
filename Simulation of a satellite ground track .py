a = 8000;                   #Pre-loaded parameters
e = 0.2;
i = 25;
u = 398600;
wd = 71;
s = 25;
n = 20;
v1 = -240;
L = -111;


# Imput your own data
choix = float(input("Enter 0 if you want to enter your own parameters.\n"));
if choix == 0:
    
    a = float(input("Demi grand axe (a, en km) : "));
    e = float(input("Excentricité (e, compris entre 0 et 1) : "));
    while e > 1:
        print("Attention ! e > 1 ! Veuillez entrer une valeur de e comprise entre 0 et 1")
        e = float(input("Excentricité (e, compris entre 0 et 1) : "));
    i = float(input("Inclinaison du plan orbital, en degrés (i < 180°) : "));
    if i == 90:
        print("Attention ! i = 90° , des erreurs peuvent survenir. \nVoulez vous rentrer une autre valeur ?")
        i = float(input("Inclinaison du plan orbital, en degrés (i < 180°) : "));
    while i >= 180:
        print("Attention ! i >= 180°, veuillez rentrer une valeur inférieure à 180°")
        i = float(input("Inclinaison du plan orbital, en degrés (i < 180°) : "));
        if i == 90:
            print("Attention ! i = 90° , des erreurs peuvent survenir. \nVoulez vous rentrer une autre valeur ?")
            i = float(input("Inclinaison du plan orbital, en degrés (i < 180°) : "));
    u = float(input("G*Mt (u, en km^3/s²) : "));
    w = float(input("argument du périgé (Omega, en degrés) : "));
    s = int(input("nombre de points à calculer : "));
    n = float(input("Angle entre deux anomalie (en degrés) : "));
    v1 = float(input("Première anomalie (en degrés) : "));
    L = float(input("Longitude géographique (en degrés) : "));


import math


# Définitions de fonctions utilisées dans le programme.
def correct_ttp_1(v,e):
    """

    Correction apportée à la formule T-Tp
    v est un angle en radian
    e est l'excentricité
    Ce module donne le paramètre principal (k*Pi) de correction de T
    

    """

    
    vc = math.acos(-e);



    k = v // (2*math.pi);
    r = v % (2*math.pi);


    if r+vc > 2*math.pi:
        k = k+1;
        r = r-2*math.pi;

    if r<vc:
        m = 2*k;
    
    elif r>vc:
         m = 2*k+1;

    m = m*math.pi

    return m;

    
def correct_ttp_2(v,e):
    """
    Correction apportée à la formule T-Tp
    v est un angle en radian
    e est l'excentricité
    Ce module donne le deuxième paramètre de la correction (le signe derrière la correction)
    
    """

    
    vc = math.acos(-e);



    k = v // (2*math.pi);
    r = v % (2*math.pi);


    if r+vc > 2*math.pi:
        k = k+1;
        r = r-2*math.pi;

    if r<vc:

        b=1;

    
    elif r>vc:

        b=-1;


    return b;





def correct_lon_1(v,w,i):
    """
    Module de correction de la longitude en Terre Fixe
    v est l'anomalie
    w est l'argument du périgé
    i est l'inclinaison du plan orbital, comprise entre 0 et 180°
        Celle ci permet de définir si l'orbite du satellite est prograde ou retrograde, voir polaire (90°)
    
    """
    cor = 0 ;
    
    if i > 90 :                         #Retrograde
        while v < (-w-90) or v > (-w+90) :
            if v < (-w-90):
                cor = cor + 180;
                v = v+180;
        
            elif v > (-w+90):
                cor = cor - 180;            
                v = v - 180;
    elif i < 90 :                         #Prograde
        while v < (-w-90) or v > (-w+90) :
            if v < (-w-90):
                cor = cor - 180;
                v = v+180;
        
            elif v > (-w+90):
                cor = cor + 180;            
                v = v - 180;
                
    return cor

def correct_lon_2(cor):
    """
    Module de correction de longitude en Terre Fixe, 2e partie
    Ce module permet de définir le signe derrière la correction.
    
    """
    VarCor = 0
    rr = cor % 360
    if rr == 0:
        VarCor = 1;
        
    elif rr == 180:
        VarCor = -1;



    return VarCor

### Calcul anomalie critique
vc = math.acos(-e);

### Conversion des angles en radians
v1 = math.pi/180*v1;
n = math.pi/180*n;
w = math.pi/180*wd;
irad = math.pi/180*i;
deg = 180/math.pi;       #Pour convertir les radians en degrés

### Calcul 'TP'
TP = -math.sqrt((a**3)/u)*(math.asin(math.sqrt(1-(e**2))*math.sin(-w)/(1+e*math.cos(-w))) - e*(math.sqrt(1-e**2)*math.sin(-w))/(1+e*math.cos(-w)));
           
### Création liste V
ListV = list();     # en radians
ListV.append(v1);   # première anomalie de la liste
for v in range(1,s):
    ListV.append(ListV[v-1]+n);


### Création liste T
T = list();                     # Liste des T, en secondes
Tnc = list();                   # Liste des T non corrigés, sert uniquement à vérifier les résultats
Pt1 = math.sqrt((a**3)/u);      # Première partie du calcul de T, correspond à 1/N (moyen mouvement)
PartSqr = math.sqrt(1-e**2);    # Partie récurrente dans le calcul.
Lm = list();                    # Première liste de correction, sert uniquement à vérifier les résultats
Lb = list();                    # Deuxième liste de correction, sert uniquement à vérifier les résultats
for t in range(0,s):
    m = correct_ttp_1(ListV[t],e);
    Lm.append(m);
    b = correct_ttp_2(ListV[t],e);
    Lb.append(b); 
    Sin = math.sin(ListV[t]);                   # Partie 'Sinus' du calcul
    PCos = 1+e*math.cos(ListV[t]);              # Partie 'Cosinus' du calcul
    PtAsin = math.asin(PartSqr * Sin / PCos);   # Partie 'Arcsin' du calcul  
    Pt2 = -e*PartSqr*Sin/PCos;                  # 2e partie du calcul
    
    T.append(Pt1 * (m + b*PtAsin + Pt2) + TP);  # Composition de la formule avec correction
    Tnc.append(Pt1 * (PtAsin +Pt2) +TP);        # Composition de la formule sans correction
    
### Création liste Phi
LPhi=list();
LPhi.append(w+v1);
for Phi in range(1,s):
    LPhi.append(w+ListV[Phi]);

Slat = math.sin(irad);


### Latitude : arcsin(sin(i)*sin(Phi))
### Création liste latitude
Llat=list();        # en radians
LlatDeg = list();   # en degrés
for lat in range(0,s):
    Llat.append(math.asin(Slat*math.sin(LPhi[lat])));
    LlatDeg.append(Llat[lat]*deg);

### Création liste longitude + correction
Llon=list();        
for lon in range(0,s):
    Llon.append(math.asin(math.tan(Llat[lon])/math.tan(irad)));
    Llon[lon] = Llon[lon]*deg;
    cor = correct_lon_1((ListV[lon]*deg),wd,i);
    VarCor = correct_lon_2(cor)
    if cor != 0:
        Llon[lon] = cor + VarCor * Llon[lon];

    
### Correction rotation Terre
Lls = list();
for ls in range(0,s):
    Lls.append(L+Llon[ls]-(360/86164)*T[ls]);
    Lls[ls] = (Lls[ls])%360;    # --------------------------------------------# 
    if Lls[ls]>180:             # Correction 'modulo' : Sert à garder les     #
        Lls[ls]=Lls[ls]-360;    # coordonnées de longitude entre -180 et +180 #





### Partie affichage
import matplotlib.pyplot as  pp

Mercator = "Mercator.jpg";

Merca = pp.imread(Mercator);
pp.title('GP21 : Traçage Satellite, Groupe 1');
pp.xlabel('Longitude');
pp.ylabel('Latitudes');



pp.axis([-180,180,-90,90]);
pp.imshow(Merca, extent=(-180,180,-90,90));
pp.plot(Lls,LlatDeg,'r.');


print("\nMoyen mouvement :\n", 1/Pt1)
print("\nAnomalie vraie critique :\n", vc)
print("\nTP :\n", TP);
print("\nAnomalies en radians :\n", ListV);
print("\nTemps de passage aux points d'anomalies :\n", T);
print("\nLattitudes :\n", LlatDeg);
print("\nLongitudes, Terre Fixe :\n", Llon);
print("\nLongitudes, Terre Tournante :\n", Lls);