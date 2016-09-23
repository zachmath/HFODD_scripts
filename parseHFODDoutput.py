# Keep this copy around as a backup, and to show you what modifications you had to 
# make to get it to work in one particular case. You had to eliminate a file where 
# the classical energy surface(?) was not formatted correctly, you had to reindex 
# the lines that the energies were found on, and you had to comment out the inertia-
# related quantities because you didn't use the inertia package when you ran that 
# particular calculation.

# I just commented out almost every line with the word 'dispersion' or 'dis_Q' 
# because that was giving me trouble.

# If your files seem to be processed correctly but they still don't appear in the XML 
# tree, it's probably because they fail the Estability < convergenceCriterion test at 
# the end. Look for "#TEST #FILTER" to see the tests that have most commonly failed 
# you or given you problems so far.

# Making useful modules available for the script
import sys
import os           # operating system module
import subprocess   # fine-grain control of processes
import shutil       # import shell functions
import re           # string manipulation
import math         # math library
import time
import difflib
import glob

from numpy import * # Array functions
from collections import deque
from lxml import etree as ET

#---------------------------------------------------------------#
#                   CUSTOMIZATION                               #
#---------------------------------------------------------------#

current_directory = os.getcwd()
root_name = current_directory.rpartition('/')

verbose               = False
version               = 'git'
lipkin                = 0 # Is Lipkin turned on? 1=yes, 0=no
lambda_max            = 4
number_constraints    = 2
convergenceCriterion  = 1.e-1
outputFiles_directory = current_directory + '/out/'
fichier_PES           = root_name[2] + '_PES.xml'
dico_units = { 0: '', 1: 'b-1/2', 2: 'b-1', 3: 'b-3/2',  4: 'b-2',  5: 'b-5/2',   6: 'b-3', \
	              7: 'b-7/2', 8: 'b-4', 9: 'b-9/2', 10: 'b-5', 11: 'b-11/2', 12: 'b-6'}
dico_inertia = {}
dico_inertia['-3_0'] = ('xi', 'xi', 0)
dico_inertia['-2_0'] = ('D',  'D',  1)
for l in range(1,9):
	for m in range(0,9):
		key = str(l)+'_'+str(m)
		dico_inertia[key] = ('q'+str(l)+str(m), 'i', l)

#---------------------------------------------------------------#
#                   INITIALIZATIONS                             #
#---------------------------------------------------------------#

nucleus = []
force, Vn_pair, Vp_pair, cut_off = [], [], [], []
beta2, omega, basis_HFODD = [], [], []
Gauss, shells, states = [], [], []

l_value, m_value, q_value = [], [], []

Ekin_n, Ekin_p, Ekin_t = [], [], []
Esin_n, Esin_p, Esin_t = [], [], []
Epai_n, Epai_p, Epai_t = [], [], []
Erea_n, Erea_p, Erea_t = [], [], []
Efer_n, Efer_p, delta_n, delta_p = [], [], [], []

ECouDir, ECouExc = [], []
EskyrmeEven, EskyrmeOdd, EsoEven, EsoOdd, Erear, Etotal = [], [], [], [], [], []
Estability = []
interaction_skyrme, interaction_Coulomb, interaction_CoulDirExact, interaction_CoulExcExact = [], [], [], []
Etot_1, Tkin_1, Vnuc_1, Vpai_1, CouD_1, CouE_1, PCM_1 = [], [], [], [], [], [], []
Etot_2, Tkin_2, Vnuc_2, Vpai_2, CouD_2, CouE_2, PCM_2 = [], [], [], [], [], [], []

Temperature, Entropy, fluctuations_quantum, fluctuations_statistical, dispersion = [], [], [], [], []

neck_position, neck_size, neck_distance, neck_protons, CM_positions = [], [], [], [], []
Z_1, A_1, Z_2, A_2 = [], [], [], []
Q20_1, Q22_1, Q30_1, Q40_1, Q50_1, Q60_1, Q70_1, Q80_1 = [], [], [], [], [], [], [], []
Q20_2, Q22_2, Q30_2, Q40_2, Q50_2, Q60_2, Q70_2, Q80_2 = [], [], [], [], [], [], [], []

liste_Bij, liste_Gij, liste_zpe = [], [], []

# Rename all append calls to lists
append_nucleus = nucleus.append
append_force, append_Vn_pair, append_Vp_pair, append_cut_off = force.append, Vn_pair.append, Vp_pair.append, cut_off.append
append_beta2, append_omega, append_basis_HFODD = beta2.append, omega.append, basis_HFODD.append
append_Gauss, append_shells, append_states = Gauss.append, shells.append, states.append

append_qlm_l, append_qlm_m, append_qlm_q = l_value.append, m_value.append, q_value.append

append_energy_kinN, append_energy_kinP, append_energy_kinT = Ekin_n.append, Ekin_p.append, Ekin_t.append
append_energy_sinN, append_energy_sinP, append_energy_sinT = Esin_n.append, Esin_p.append, Esin_t.append
append_energy_paiN, append_energy_paiP, append_energy_paiT = Epai_n.append, Epai_p.append, Epai_t.append
append_energy_reaN, append_energy_reaP, append_energy_reaT = Erea_n.append, Erea_p.append, Erea_t.append
append_energy_ferN, append_energy_ferP = Efer_n.append, Efer_p.append
append_deltaN, append_deltaP = delta_n.append, delta_p.append

append_energy_CouD, append_energy_CouE = ECouDir.append, ECouExc.append
append_energy_skyE, append_energy_skyO = EskyrmeEven.append, EskyrmeOdd.append
append_energy_spoE, append_energy_spoO = EsoEven.append, EsoOdd.append
append_energy_rear, energy_append_stab, energy_append_tota = Erear.append, Estability.append, Etotal.append

append_fthfb_temp, append_fthfb_entr = Temperature.append, Entropy.append
append_fthfb_quan, append_fthfb_stat = fluctuations_quantum.append, fluctuations_statistical.append
append_dispersion = dispersion.append

append_frag_couP, append_frag_couS, append_frag_couD, append_frag_couZ, append_frag_CM = neck_position.append, neck_size.append, neck_distance.append, neck_protons.append, CM_positions.append
append_frag_intS, append_frag_intC = interaction_skyrme.append, interaction_Coulomb.append
append_frag_intCDex, append_frag_intCXex = interaction_CoulDirExact.append, interaction_CoulExcExact.append
append_frag_lefA, append_frag_lefZ, append_frag_rigA, append_frag_rigZ = A_1.append, Z_1.append, A_2.append, Z_2.append
append_frag_lefEtot, append_frag_rigEtot = Etot_1.append, Etot_2.append
append_frag_lefEkin, append_frag_rigEkin = Tkin_1.append, Tkin_2.append
append_frag_lefVnuc, append_frag_rigVnuc = Vnuc_1.append, Vnuc_2.append
append_frag_lefVpai, append_frag_rigVpai = Vpai_1.append, Vpai_2.append
append_frag_lefVcoD, append_frag_rigVcoD = CouD_1.append, CouD_2.append
append_frag_lefVcoE, append_frag_rigVcoE = CouE_1.append, CouE_2.append
append_frag_lefCOM, append_frag_rigCOM = PCM_1.append, PCM_2.append

append_frag_lQ20, append_frag_lQ22 = Q20_1.append, Q22_1.append
append_frag_lQ30, append_frag_lQ40 = Q30_1.append, Q40_1.append
append_frag_lQ50, append_frag_lQ60 = Q50_1.append, Q60_1.append
append_frag_lQ70, append_frag_lQ80 = Q70_1.append, Q80_1.append
append_frag_rQ20, append_frag_rQ22 = Q20_2.append, Q22_2.append
append_frag_rQ30, append_frag_rQ40 = Q30_2.append, Q40_2.append
append_frag_rQ50, append_frag_rQ60 = Q50_2.append, Q60_2.append
append_frag_rQ70, append_frag_rQ80 = Q70_2.append, Q80_2.append

append_col_mass, append_metric, append_zpe = liste_Bij.append, liste_Gij.append, liste_zpe.append

#---------------------------------------------------------------#
#                 USER-DEFINED FUNCTIONS                        #
#---------------------------------------------------------------#

# Function used to strip a line from its blank spaces

def not_empty(chaine): return chaine != ''

def kineticEnergy():
	append_energy_kinN(ligneFormattee[3])
	append_energy_kinP(ligneFormattee[5])
	append_energy_kinT(ligneFormattee[7])

def spEnergy():
	if len(ligneFormattee)>8:
		append_energy_sinN(ligneFormattee[4])
		append_energy_sinP(ligneFormattee[6])
		append_energy_sinT(ligneFormattee[8])
	else:
		append_energy_sinN(9999.99)
		append_energy_sinP(9999.99)
		append_energy_sinT(9999.99)

def pairingEnergy():
	append_energy_paiN(ligneFormattee[3])
	append_energy_paiP(ligneFormattee[5])
	append_energy_paiT(ligneFormattee[7])

def pairingRearrangementEnergy():
	append_energy_reaN(ligneFormattee[3])
	append_energy_reaP(ligneFormattee[5])
	append_energy_reaT(ligneFormattee[7])

def pairingGap():
	append_deltaN(ligneFormattee[3])
	append_deltaP(ligneFormattee[5])

def fermiEnergy():
	append_energy_ferN(ligneFormattee[3])
	append_energy_ferP(ligneFormattee[5])

def CoulombEnergy():
	append_energy_CouD(ligneFormattee[3])
	append_energy_CouE(ligneFormattee[5])

def rearrangementEnergy():
	append_energy_rear(ligneFormattee[8])

def soEnergy():
	append_energy_spoE(ligneFormattee[3])
	append_energy_spoO(ligneFormattee[5])

def skyrmeEnergy():
	append_energy_skyE(ligneFormattee[3])
	append_energy_skyO(ligneFormattee[5])

def stability():
	if len(ligneFormattee) == 9:
		energy_append_stab(ligneFormattee[3])
		energy_append_tota(ligneFormattee[7])
	else:
		energy_append_stab(9999.99)
		energy_append_tota(9999.99)

def getStringFromList_safe(liste, position):
	try:
		string_value = str(liste[position])
	except IndexError:
		string_value = '9999.99'
	return string_value

def getTupleFromList_safe(liste, position, format_output):
	def conversion(number, f):
		if f.find('d') > -1:
			func = int
		if f.find('f') > -1 or f.find('e') > -1:
			func = float
		return func(number)
	try:
		l = [ format_output.format( conversion(i,format_output) ) for i in list(liste[position]) ]
		tuple_value = tuple(l)
	except IndexError:
		tuple_value = ( '9999.99' )
	return tuple_value

def getNumberFromList_safe(liste, position, format_output):
	def conversion(number, f):
		if f.find('d') > -1:
			func = int
		if f.find('f') > -1 or f.find('e') > -1:
			func = float
		return func(number)
	try:
		string_value = format_output.format(conversion(liste[position],format_output))
	except IndexError:
		string_value = format_output.format(9999.9)
	return string_value

def getNumberFromList_1_safe(liste, position, new_index, format_output):
	def conversion(number, f):
		if f.find('d') > -1:
			func = int
		if f.find('f') > -1 or f.find('e') > -1:
			func = float
		return func(number)
	try:
		string_value = format_output.format(conversion(liste[position][new_index],format_output))
	except IndexError:
		string_value = format_output.format(9999.9)
	return string_value

def extractValues(input_ligne, position_in_line):
	ligneFormattee = breakLine(input_ligne)
	try:
		number_value = float(ligneFormattee[position_in_line])
	except Exception as ex:
		template = "In extractValues, an exception of type {0} occured. Arguments:\n{1!r}"
		message = template.format(type(ex).__name__, ex.args)
		print message
		number_value = 0.0
	return number_value

def formatValues(input_ligne, liste_append, position_in_line):
	total_value  = extractValues(input_ligne, position_in_line)
	value = "{0:> 9.3e}".format(total_value)
	liste_append(total_value)

def temperatureValues(input_ligne, liste_append, pos1, pos2):
	proton_value  = extractValues(input_ligne, pos1)
	neutron_value = extractValues(input_ligne, pos2)
	total_value   = proton_value + neutron_value
	value = "{0:> 9.3e}".format(total_value)
	liste_append(total_value)

def dispersionQ(input_ligne, liste_append, pos, number_constraints):
	l_l, l_m, l_QF, l_SF = [], [], [], []
	dic = { "xi_A": (-3,0), "D": (-2,0), "Q_10": (1,0), "Q_20": (2,0), "Q_30": (3,0), \
	        "Q_40": (4,0), "Q_50": (5,0),"Q_60": (6,0), "Q_70": (7,0), "Q_80": (8,0)}
	for n in range(0,number_constraints):
		ligneFormattee = breakLine(input_ligne[n])
		try:
			(l,m) = dic[ligneFormattee[1]]
		except Exception as ex:
			template = "In dispersionQ, an exception of type {0} occured. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			print message
			l, m = '0', '0'
		l_l.append(str(l)), l_m.append(str(m))
		Q_QF_proton_value  = extractValues(input_ligne[n], pos[0])
		Q_QF_neutron_value = extractValues(input_ligne[n], pos[1])
		QF_value = Q_QF_proton_value + Q_QF_neutron_value
		Q_SF_proton_value  = extractValues(input_ligne[n], pos[2])
		Q_SF_neutron_value = extractValues(input_ligne[n], pos[3])
		SF_value = Q_SF_proton_value + Q_SF_neutron_value
		QF, SF = "{0:> 8.3f}".format(QF_value), "{0:> 8.3}".format(SF_value)
		l_QF.append(QF), l_SF.append(SF)
	liste_append( (l_l, l_m, l_QF, l_SF) )

def collectiveInertia(debut, liste_1_append, liste_2_append, liste_3_append):
	# Position cursor where data begins
	position = debut + 3
	ligne = allLines[position]
	# Get the components of the inertia tensor
	collective = []
	while ligne.find('MeV') > -1:
		[ l, m, lp, mp, m_ATDHF, m_GCM ] = [ extractValues(ligne, i) for i in range(1,7) ]
		key_bra, key_ket, m_ATDHF, m_GCM = str(int(l))+'_'+str(int(m)), str(int(lp))+'_'+str(int(mp)), float(m_ATDHF), float(m_GCM)
		(bra, type_bra, units_bra) = dico_inertia[key_bra]
		(ket, type_ket, units_ket) = dico_inertia[key_ket]
		collective.append( { 'type_bra': type_bra, 'bra': bra, 'units_bra': units_bra,\
			             'type_ket': type_ket, 'ket': ket, 'units_ket': units_ket,\
				     'mass': ( m_ATDHF, m_GCM ) } )
		position = position + 1
		ligne    = allLines[position]
	liste_1_append(collective)
	n = position - debut - 3
	# Get the components of the metric tensor
	position = position + 4
	ligne = allLines[position]
	collective = []
	for k in range(0,n):
		[ l, m, lp, mp, G_GCM ] = [ extractValues(ligne, i) for i in range(1,6) ]
		key_bra, key_ket, G_GCM = str(int(l))+'_'+str(int(m)), str(int(lp))+'_'+str(int(mp)), float(G_GCM)
		(bra, type_bra, units_bra) = dico_inertia[key_bra]
		(ket, type_ket, units_ket) = dico_inertia[key_ket]
		collective.append( { 'type_bra': type_bra, 'bra': bra, 'units_bra': units_bra,\
			             'type_ket': type_ket, 'ket': ket, 'units_ket': units_ket,\
			             'G': G_GCM } )
		position = position + 1
		ligne    = allLines[position]
	liste_2_append(collective)
	# Get ZPE
	position = position + 1
	ligne = allLines[position]
	zpe_atdhf = extractValues(ligne, 6)
	position = position + 1
	ligne = allLines[position]
	zpe_gcm = extractValues(ligne, 7)
	liste_3_append( (zpe_atdhf, zpe_gcm ) )

def breakLine(element):
	currentLine  = re.split("\n",element)
	brokenLine   = re.split(" ",currentLine[0])
	strippedLine = filter(not_empty, brokenLine)
	return strippedLine

def removeZEROS(chaine):
	new_chaine = chaine.replace("ZERO"," 0.0")
	return new_chaine

# Function adding a point to the PES XML file
def point_xml(dictionnaire, number_constraints):
	point = ET.SubElement(PES, "point")
	point.attrib["id"] = dictionnaire["id"]
	neighborsID = ET.SubElement(point, "neighborsID")
	neighborsID.text = dictionnaire["neighborsID"]
	stability = ET.SubElement(point, "stability")
	stability.attrib["dE"] = dictionnaire["dE"]
	fichier = ET.SubElement(point, "fichier")
	fichier.attrib["nom"] = dictionnaire["nom"]
	fichier.attrib["dir"] = dictionnaire["dir"]
	# Basis characteristics
	basis = ET.SubElement(point, "basis")
	basis.attrib["beta2"] = dictionnaire["beta2"]
	basis.attrib["omega"] = dictionnaire["omega0"]
	basis.attrib["FCHOM0"] = dictionnaire["FCHOM0"]
	frequencies = ET.SubElement(basis, "HOfrequencies")
	frequencies.attrib["omega_x"] = dictionnaire["omega_x"]
	frequencies.attrib["omega_y"] = dictionnaire["omega_y"]
	frequencies.attrib["omega_z"] = dictionnaire["omega_z"]
	Nshells = ET.SubElement(basis, "number_of_shells")
	Nshells.attrib["Nx"] = dictionnaire["Nx_HO"]
	Nshells.attrib["Ny"] = dictionnaire["Ny_HO"]
	Nshells.attrib["Nz"] = dictionnaire["Nz_HO"]
	GH = ET.SubElement(basis, "Gauss_Hermite")
	GH.attrib["Ng_x"] = dictionnaire["Ng_x"]
	GH.attrib["Ng_y"] = dictionnaire["Ng_y"]
	GH.attrib["Ng_z"] = dictionnaire["Ng_z"]
	Nstate = ET.SubElement(basis, "number_of_states")
	Nstate.attrib["LDBASE"] = dictionnaire["LDBASE"]
	# Global nuclear properties
	constraints = ET.SubElement(point, "constraints")
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "q20"
	constraint.attrib["val"]  = dictionnaire["q20"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "q22"
	constraint.attrib["val"]  = dictionnaire["q22"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "q30"
	constraint.attrib["val"]  = dictionnaire["q30"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "q40"
	constraint.attrib["val"]  = dictionnaire["q40"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "q50"
	constraint.attrib["val"]  = dictionnaire["q50"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "q60"
	constraint.attrib["val"]  = dictionnaire["q60"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "q70"
	constraint.attrib["val"]  = dictionnaire["q70"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "q80"
	constraint.attrib["val"]  = dictionnaire["q80"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "D"
	constraint.attrib["val"]  = dictionnaire["D"]
	constraint = ET.SubElement(constraints, "constraint")
	constraint.attrib["type"] = "xi"
	constraint.attrib["val"]  = dictionnaire["xi"]
	energies = ET.SubElement(point, "energies")
	energies.attrib["EHFB"] = dictionnaire["EHFB"]
	corrections = ET.SubElement(point, "corrections")
	zpe = ET.SubElement(corrections, "goaZpe")
	zpe.attrib["inertiaType"] = "ATDHF"
	zpe.attrib["value"] = dictionnaire["E0_ATDHF"] + " MeV"
	zpe = ET.SubElement(corrections, "goaZpe")
	zpe.attrib["inertiaType"] = "GCM"
	zpe.attrib["value"] = dictionnaire["E0_GCM"] + " MeV"
	pairing = ET.SubElement(point, "pairing")
	pairing.attrib["deltaN"] = dictionnaire["deltaN"]
	pairing.attrib["deltaP"] = dictionnaire["deltaP"]
	pairing.attrib["EpairN"] = dictionnaire["EpairN"]
	pairing.attrib["EpairP"] = dictionnaire["EpairP"]
	Fermi = ET.SubElement(point, "Fermi")
	Fermi.attrib["lambdaN"] = dictionnaire["lambdaN"]
	Fermi.attrib["lambdaP"] = dictionnaire["lambdaP"]
	temperature = ET.SubElement(point, "temperature")
	temperature.attrib["T"] = dictionnaire["T"]
	temperature.attrib["S"] = dictionnaire["S"]
	dispersion_N = ET.SubElement(temperature, "dispersion_N")
	dispersion_N.attrib["quantum"] = dictionnaire["N_QF"]
	dispersion_N.attrib["statistical"] = dictionnaire["N_SF"]
# OPTION #TEST #FILTER
# Something to do with temperature, but it's giving me an error and it's only outputting zeros anyway.
#	for i in range(0,number_constraints):
#		dispersion_Q = ET.SubElement(temperature, "dispersion_Q")
#		dispersion_Q.attrib["l"] = dictionnaire["lambda"][i]
#		dispersion_Q.attrib["m"] = dictionnaire["mu"][i]
#		dispersion_Q.attrib["quantum"] = dictionnaire["Q_QF"][i]
#		dispersion_Q.attrib["statistical"] = dictionnaire["Q_SF"][i]
	neck = ET.SubElement(point, "neck")
	neck.attrib["zN"] = dictionnaire["zN"]
	neck.attrib["D"]  = dictionnaire["D"]
	neck.attrib["qN"] = dictionnaire["qN"]
	neck.attrib["Nz"] = dictionnaire["Nz"]
	# Fission fragment properties
	fragments = ET.SubElement(point, "fragments")
	identity = ET.SubElement(fragments, "identity")
	identity.attrib["Z1"] = dictionnaire["Z1"]
	identity.attrib["A1"] = dictionnaire["A1"]
	identity.attrib["Z2"] = dictionnaire["Z2"]
	identity.attrib["A2"] = dictionnaire["A2"]
	interaction = ET.SubElement(fragments, "interaction")
	interaction.attrib["Enuc"] = dictionnaire["Enuc"]
	interaction.attrib["ECou"] = dictionnaire["ECou"]
	interaction.attrib["ECouDir_exact"] = dictionnaire["ECouDir_exact"]
	interaction.attrib["ECouExc_exact"] = dictionnaire["ECouExc_exact"]
	deformation1 = ET.SubElement(fragments, "deformation1")
	deformation1.attrib["q20_1"] = dictionnaire["q20_1"]
	deformation1.attrib["q22_1"] = dictionnaire["q22_1"]
	deformation1.attrib["q30_1"] = dictionnaire["q30_1"]
	deformation1.attrib["q40_1"] = dictionnaire["q40_1"]
	deformation1.attrib["q50_1"] = dictionnaire["q50_1"]
	deformation1.attrib["q60_1"] = dictionnaire["q60_1"]
	deformation1.attrib["q70_1"] = dictionnaire["q70_1"]
	deformation1.attrib["q80_1"] = dictionnaire["q80_1"]
	deformation2 = ET.SubElement(fragments, "deformation2")
	deformation2.attrib["q20_2"] = dictionnaire["q20_2"]
	deformation2.attrib["q22_2"] = dictionnaire["q22_2"]
	deformation2.attrib["q30_2"] = dictionnaire["q30_2"]
	deformation2.attrib["q40_2"] = dictionnaire["q40_2"]
	deformation2.attrib["q50_2"] = dictionnaire["q50_2"]
	deformation2.attrib["q60_2"] = dictionnaire["q60_2"]
	deformation2.attrib["q70_2"] = dictionnaire["q70_2"]
	deformation2.attrib["q80_2"] = dictionnaire["q80_2"]
	properties1 = ET.SubElement(fragments, "properties1")
	properties1.attrib["Ekin_1"]  = dictionnaire["Ekin_1"]
	properties1.attrib["Enuc_1"]  = dictionnaire["Enuc_1"]
	properties1.attrib["Epair_1"] = dictionnaire["Epair_1"]
	properties1.attrib["ECouD_1"] = dictionnaire["ECouD_1"]
	properties1.attrib["ECouE_1"] = dictionnaire["ECouE_1"]
	properties1.attrib["ECM_1"]   = dictionnaire["ECM_1"]
	properties2 = ET.SubElement(fragments, "properties2")
	properties2.attrib["Ekin_2"]  = dictionnaire["Ekin_2"]
	properties2.attrib["Enuc_2"]  = dictionnaire["Enuc_2"]
	properties2.attrib["Epair_2"] = dictionnaire["Epair_2"]
	properties2.attrib["ECouD_2"] = dictionnaire["ECouD_2"]
	properties2.attrib["ECouE_2"] = dictionnaire["ECouE_2"]
	properties2.attrib["ECM_2"]   = dictionnaire["ECM_2"]
	# Collective inertia
	size_inertia = len(dictionnaire["type_bra"])
	inertia = ET.SubElement(point, "inertia")
	inertia.attrib["size"] = str(size_inertia)
	for i in range(0,size_inertia):
		element = ET.SubElement(inertia, "element")
		element.attrib["i"] = dictionnaire["bra"][i]
		element.attrib["j"] = dictionnaire["ket"][i]
		li, lj = dictionnaire["units_bra"][i], dictionnaire["units_ket"][i]
		element.attrib["value"] = str(dictionnaire["M_ATDHF"][i]) + " MeV-1." + dico_units[li+lj]
		element.attrib["type"]  = "ATDHF"
	for i in range(0,size_inertia):
		element = ET.SubElement(inertia, "element")
		element.attrib["i"] = dictionnaire["bra"][i]
		element.attrib["j"] = dictionnaire["ket"][i]
		li, lj = dictionnaire["units_bra"][i], dictionnaire["units_ket"][i]
		element.attrib["value"] = str(dictionnaire["M_GCM"][i]) + " MeV-1." + dico_units[li+lj]
		element.attrib["type"]  = "GCM"
	# GCM metric tensor
	size_metric = len(dictionnaire["type_bra"])
	metric = ET.SubElement(point, "metric")
	metric.attrib["size"] = str(size_metric)
	for i in range(0,size_metric):
		element = ET.SubElement(metric, "element")
		element.attrib["i"] = dictionnaire["bra"][i]
		element.attrib["j"] = dictionnaire["ket"][i]
		li, lj = dictionnaire["units_bra"][i], dictionnaire["units_ket"][i]
		element.attrib["value"] = str(dictionnaire["G"][i]) + " " + dico_units[li+lj]
		element.attrib["type"]  = "G"

	return 0

#---------------------------------------------------------------#
#                    READING THE FILES                          #
#---------------------------------------------------------------#

line_max = { 0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 12, 6: 16, 7: 20, 8: 24, 9: 28}

liste_beg = [  8, 23, 38, 53, 68 ]
liste_end = [ 16, 31, 46, 61, 77 ]

dict_qlm = {  0: (liste_beg[0:1],liste_end[0:1]),  2: (liste_beg[0:2],liste_end[0:2]),  4: (liste_beg[0:3],liste_end[0:3]), \
	      6: (liste_beg[0:4],liste_end[0:4]),  8: (liste_beg[0:5],liste_end[0:5]), 10: (liste_beg[0:5],liste_end[0:5]), \
	     12: (liste_beg[4:5],liste_end[4:5]), 14: (liste_beg[0:5],liste_end[0:5]), 16: (liste_beg[3:5],liste_end[3:5]), \
	     18: (liste_beg[0:5],liste_end[0:5]), 20: (liste_beg[2:5],liste_end[2:5]), 22: (liste_beg[0:5],liste_end[0:5]), \
	     24: (liste_beg[1:5],liste_end[1:5]), 26: (liste_beg[0:5],liste_end[0:5]), 28: (liste_beg[0:5],liste_end[0:5]) }

dict_lm = { 2: 0, 2: 1, 4: 2, 6: 3, 8: 4, 12: 5, 16: 6, 20: 7, 24: 8, 28: 9}

# Starting the clock
time_all = []
start_total = time.time()

# Listing all files to be processed, sorting the list and creating a dictionary to store bad files
os.chdir(outputFiles_directory)
listeFichier = sorted(glob.glob('hfodd_0*.out'))
listeFlags = [ 1 for i in range(0,len(listeFichier)) ]
dico_fichier = dict(zip(listeFichier,listeFlags))
listeFichier_good = [ fichier for fichier in listeFichier if dico_fichier[fichier]==1 ]

# Looping over all files
count_fichier = -1
for fichier in listeFichier:

	count_fichier = count_fichier + 1
	if verbose:
		print 'fichier: ', fichier

	# Read the file and store all lines in a list
	fread = open(fichier,'r')
	allLines = fread.readlines()
	fread.close()

	# Sometimes a calculation may time out or be terminated before it finishes running.  #TEST #FILTER
	# This will determine if the file formatted correctly or if it was interrupted.
	chaine = '*  NUMBERS OF CALLS TO SUBROUTINES                                            *\n'
	position_terminate = [i for i, x in enumerate(allLines) if x == chaine]
	size = len(position_terminate)
	if size < 1:
		dico_fichier[fichier] = 0
		print fichier, 'was terminated prematurely.'

	# Get total multipole moments at convergence. Use the information to determine if the  #TEST #FILTER
	# calculation ran into problems: if there is no such table or only 1, the calculation
	# did not converge and this file should be disregarded
	chaine = '*  MULTIPOLE MOMENTS [UNITS:  (10 FERMI)^LAMBDA]                       TOTAL  *\n'
	position_multipole = [i for i, x in enumerate(allLines) if x == chaine]
	size = len(position_multipole)
	if size < 2:
		dico_fichier[fichier] = 0
		if verbose:
			print fichier, 'did not converge.'
	else:
		actual_line_max = line_max[lambda_max]
		qlm = []
		for i in range(0,actual_line_max+2,2):
			element = allLines[position_multipole[size-1]+4+i]
			sequence = dict_qlm[i]
			beg = sequence[0]
			end = sequence[1]
			q_temp =[ element[b:e] for b,e in zip(beg,end) ]
			qlm.append(map(removeZEROS, q_temp))
		append_qlm_q( [ item for sublist in qlm for item in sublist ])

	# Only look for meaningful numbers if the file is converged
	
	if dico_fichier[fichier] > 0:  #TEST #FILTER
		
		# Get the basis deformation
		chaine = '*  CLASSICAL NUCLEAR SURFACE DEFINED FOR:'
		position_s = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		size = len(position_s)
		lines = [ allLines[i+6] for i in position_s]
		bet2 = map(breakLine, lines)
		append_beta2(bet2[0][3])

		# Get the nucleus
		chaine = '* NUCLIDE:'
		position_Z = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		size = len(position_Z)
		lines = [ allLines[i] for i in position_Z]
		noyau = map(breakLine, lines)
		append_nucleus( (noyau[0][4], noyau[0][7]) )

		# Get the value of the Skyrme functional
		chaine = '* PARAMETER SET'
		position_F = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		size = len(position_F)
		lines = [ allLines[i] for i in position_F]
		skyrme = map(breakLine, lines)
		append_force(re.split(':',skyrme[0][3])[0])

		# Get the characteristics of the basis
		chaine = '*  OSCILLATOR FREQUENCIES: X='
		position_b = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		size = len(position_b)
		deque((list.pop(allLines, i) for i in sorted(position_b[0:size-1], reverse=True)), maxlen=0)
		position_b = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		if size > 0:
			i = position_b[0]
			# basis frequency
			omg = breakLine(allLines[i])
			append_omega( (omg[4], omg[6], omg[8]) )
			# number of shells
			i = i + 4
			Nsh = breakLine(allLines[i])
			append_shells( (Nsh[7], Nsh[10], Nsh[13]) )
			# Gauss-Hermite integration points
			i = i + 2
			Ngh = breakLine(allLines[i])
			append_Gauss( (Ngh[3], Ngh[6], Ngh[9]) )
			# Number of states
			i = i + 2
			Nst = re.split('=',breakLine(allLines[i])[2])
			append_states(Nst[1])
			
		chaine = '*                                           HOMEGA='
		position_b = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		size = len(position_b)
		deque((list.pop(allLines, i) for i in sorted(position_b[0:size-1], reverse=True)), maxlen=0)
		position_b = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		if size > 0:
			# HFODD characteristics
			i = position_b[0]
			FCHOM0 = breakLine(allLines[i])
			append_basis_HFODD( (FCHOM0[2], FCHOM0[4]) )

		# Get the characteristics of the pairing force
		chaine = '* CONTACT PAIRING INTERACTION:'
		position_P = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		size = len(position_P)
		deque((list.pop(allLines, i) for i in sorted(position_P[0:size-1], reverse=True)), maxlen=0)
		position_P = [ i for i, x in enumerate(allLines) if x.find(chaine) > -1 ]
		if size > 0:
			# neutron pairing
			i = position_P[0] + 1
			lines = allLines[i]
			Vn = breakLine(lines)
			append_Vn_pair( (Vn[2], Vn[3], Vn[4], Vn[5]) )
			# proton pairing
			i = i + 1
			lines = allLines[i]
			Vp = breakLine(lines)
			append_Vp_pair( (Vp[2], Vp[3], Vp[4], Vp[5]) )
			# energy cut-off
			i = i + 4
			lines = allLines[i]
			Ecut = breakLine(lines)
			append_cut_off( Ecut[9] )

		# Get the collective inertia
		chaine = "*  MASS TENSOR M_{ij}/HbarC**2 WITH i=(L,M) AND j=(LP,MP)                     *\n"
		position_collective = [i for i, x in enumerate(allLines) if x == chaine ]
		size = len(position_collective)
		if size == 1 and dico_fichier[fichier] > 0:
			collectiveInertia(position_collective[0], append_col_mass, append_metric, append_zpe)
		else:
			append_col_mass( {} )
			append_metric( {} )
			append_zpe( (0.0, 0.0) ) 

		# Get the table of energies
		chaine = '*                                ENERGIES (MEV)                               *\n'
		position_energies = [i for i, x in enumerate(allLines) if x == chaine]
		size = len(position_energies)
		energies = { 4: kineticEnergy, 5: spEnergy, 6: pairingEnergy, 7: pairingRearrangementEnergy, \
			9+lipkin: pairingGap, 10+lipkin: fermiEnergy, 12+2*lipkin: CoulombEnergy, \
			18+2*lipkin+1: rearrangementEnergy, 21+2*lipkin+1: soEnergy, \
			22+2*lipkin+1: skyrmeEnergy, 24+2*lipkin+1: stability }
#			18+2*lipkin: rearrangementEnergy, 21+2*lipkin: soEnergy, \
#			22+2*lipkin: skyrmeEnergy, 24+2*lipkin: stability }
		for indexEnergy in [4, 5, 6, 7, 9+lipkin, 10+lipkin, 12+2*lipkin, 18+2*lipkin+1, 21+2*lipkin+1, 22+2*lipkin+1, 24+2*lipkin+1]:
#		for indexEnergy in [4, 5, 6, 7, 9+lipkin, 10+lipkin, 12+2*lipkin, 18+2*lipkin, 21+2*lipkin, 22+2*lipkin, 24+2*lipkin]:
			debut          = position_energies[size-1]
			position       = debut + indexEnergy
			elementEnergy  = allLines[position]
			ligneFormattee = breakLine(elementEnergy)
			energies.get(indexEnergy)()

		# Get fission fragment properties: energies, interaction energy, deformations, etc.
		chaine = "*            FISSION FRAGMENT PROPERTIES (SHARP ADIABATIC SCISSION)           *\n"
		position_fragments = [i for i, x in enumerate(allLines) if x == chaine ]
		size = len(position_fragments)

		if size == 1:

			debut = position_fragments[0] + 2

			# Get neck characteristics
			position    = debut
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_couP, 10)

			# Neck
			position    = debut + 1
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_couS, 10)

			position    = debut + 2
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_couZ, 9)

			position    = debut + 3
			ligneBuffer = allLines[position]
			CM1 = extractValues(ligneBuffer, 9)
			CM2 = extractValues(ligneBuffer,10)
			append_frag_CM( ("{0:> 9.3e}".format(CM1), "{0:> 9.3e}".format(CM2)) )

			position    = debut + 4
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_couD, 8)

			# Interaction energy
			position    = debut + 5
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_intS, 5)

			position    = debut + 6
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_intC, 8)

			# Exact Coulomb interaction energy
			position    = debut + 7
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_intCDex, 7)

			position    = debut + 8
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_intCXex, 7)

			# Get fission fragment properties: energies, interaction energy, deformations, etc.
			chaine = "*             |   LEFT  FRAGMENT (z < zN)   |   RIGHT FRAGMENT (z > zN)       *\n"
			position_energies = [i for i, x in enumerate(allLines) if x == chaine ]
			
			debut = position_energies[0] + 2

			# Get fragment characteristics (newer versions)
			position    = debut
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefA, 3)
			formatValues(ligneBuffer, append_frag_rigA, 5)

			position    = debut + 1
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefZ, 3)
			formatValues(ligneBuffer, append_frag_rigZ, 5)

			position    = debut + 2
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefEtot, 3)
			formatValues(ligneBuffer, append_frag_rigEtot, 5)

			position    = debut + 3
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefEkin, 3)
			formatValues(ligneBuffer, append_frag_rigEkin, 5)

			position    = debut + 4
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefVnuc, 3)
			formatValues(ligneBuffer, append_frag_rigVnuc, 5)

			position    = debut + 5
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefVpai, 3)
			formatValues(ligneBuffer, append_frag_rigVpai, 5)

			position    = debut + 6
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefVcoD, 3)
			formatValues(ligneBuffer, append_frag_rigVcoD, 5)

			position    = debut + 7
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefVcoE, 3)
			formatValues(ligneBuffer, append_frag_rigVcoE, 5)

			position    = debut + 8
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lefCOM, 3)
			formatValues(ligneBuffer, append_frag_rigCOM, 5)
			
			# Get fission fragment multipole moments (in fragment intrinsic frame)
			chaine = "*                 MULTIPOLE MOMENTS IN FRAGMENT INTRINSIC FRAME               *\n"
			position_multipole = [i for i, x in enumerate(allLines) if x == chaine ]
			
			debut = position_multipole[0] + 4

			position    = debut
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lQ20, 3)
			formatValues(ligneBuffer, append_frag_rQ20, 5)

			position    = debut + 1
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lQ22, 3)
			formatValues(ligneBuffer, append_frag_rQ22, 5)

			position    = debut + 2
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lQ30, 3)
			formatValues(ligneBuffer, append_frag_rQ30, 5)

			position    = debut + 3
			ligneBuffer = allLines[position]
			formatValues(ligneBuffer, append_frag_lQ40, 3)
			formatValues(ligneBuffer, append_frag_rQ40, 5)

# OPTION:
# These high-order multipole moments only matter if you go that high in the rest of the code.  #TEST #FILTER
#			position    = debut + 4
#			ligneBuffer = allLines[position]
#			formatValues(ligneBuffer, append_frag_lQ50, 3)
#			formatValues(ligneBuffer, append_frag_rQ50, 5)
#
#			position    = debut + 5
#			ligneBuffer = allLines[position]
#			formatValues(ligneBuffer, append_frag_lQ60, 3)
#			formatValues(ligneBuffer, append_frag_rQ60, 5)
#
#			position    = debut + 6
#			ligneBuffer = allLines[position]
#			formatValues(ligneBuffer, append_frag_lQ70, 3)
#			formatValues(ligneBuffer, append_frag_rQ70, 5)
#
#			position    = debut + 7
#			ligneBuffer = allLines[position]
#			formatValues(ligneBuffer, append_frag_lQ80, 3)
#			formatValues(ligneBuffer, append_frag_rQ80, 5)
#

		else:

			append_frag_couP(0.0), append_frag_couS(0.0), append_frag_couD(0.0), append_frag_couZ(0.0)
			append_frag_intS(0.0), append_frag_intC(0.0)
			append_frag_intCDex(0.0), append_frag_intCXex(0.0)
			append_frag_lefA(0.0), append_frag_lefZ(0.0),
			append_frag_rigA(0.0), append_frag_rigZ(0.0)
			append_frag_lefEtot(0.0), append_frag_rigEtot(0.0)
			append_frag_lefEkin(0.0), append_frag_rigEkin(0.0)
			append_frag_lefVnuc(0.0), append_frag_rigVnuc(0.0)
			append_frag_lefVpai(0.0), append_frag_rigVpai(0.0)
			append_frag_lefVcoD(0.0), append_frag_rigVcoD(0.0)
			append_frag_lefVcoE(0.0), append_frag_rigVcoE(0.0)
			append_frag_lefCOM(0.0), append_frag_rigCOM(0.0)
			append_frag_lQ20(0.0), append_frag_lQ22(0.0)
			append_frag_lQ30(0.0), append_frag_lQ40(0.0)
			append_frag_lQ50(0.0), append_frag_lQ60(0.0)
			append_frag_lQ70(0.0), append_frag_lQ80(0.0)
			append_frag_rQ20(0.0), append_frag_rQ22(0.0)
			append_frag_rQ30(0.0), append_frag_rQ40(0.0)
			append_frag_rQ50(0.0), append_frag_rQ60(0.0)
			append_frag_rQ70(0.0), append_frag_rQ80(0.0)

		# Get temperature and entropy at convergence
		chaine = '*  FINITE-TEMPERATURE HFB CALCULATIONS AT'
		position_entropy = [i for i, x in enumerate(allLines) if x.find(chaine) > -1]
		size = len(position_entropy)
		if size == 1:
			debut = position_entropy[size-1]
			# Get temperature
			formatValues(allLines[debut], append_fthfb_temp, 7)
			# Get total entropy (sum of neutrons and protons)
			position     = debut + 2
			ligneEntropy = allLines[position]
			temperatureValues(ligneEntropy, append_fthfb_entr, 3, 6)
			# Get quantum fluctuations of particle number
			position     = debut + 3
			ligneQuantum = allLines[position]
			temperatureValues(ligneQuantum, append_fthfb_quan, 3, 5)
			# Get statistical fluctuations of particle number
			position         = debut + 4
			ligneStatistical = allLines[position]
			temperatureValues(ligneStatistical, append_fthfb_stat, 3, 5)
			# Get quantum and statistical fluctuations of multipole moment constraints
			position         = debut + 8
			ligneStatistical = [ allLines[position+n] for n in range(0,number_constraints) ]
			pos = [ 2, 3, 4, 5 ]
# OPTION (not actually sure what this does, but it's breaking the thing!)
#			dispersionQ(ligneStatistical, append_dispersion, pos, number_constraints)  #TEST #FILTER
		else:
			append_fthfb_temp(0.0), append_fthfb_entr(0.0)
			append_fthfb_quan(0.0), append_fthfb_stat(0.0)
			zero_liste = [ '0' for i in range(0,number_constraints)]
#			append_dispersion( (zero_liste, zero_liste, zero_liste, zero_liste) )

elapsed_total = (time.time() - start_total)
print 'Time elapsed for total ....: ', elapsed_total

#-------------------------------------------------------------------------------------------------------------------#
#    Printing the listing of converged results: multipole moments, energy plus various other relevant quantities    #
#-------------------------------------------------------------------------------------------------------------------#

start_post = time.time()

listeFichier_good = [ fichier for fichier in listeFichier if dico_fichier[fichier]==1 ]

if verbose:
	print "Total number of files...........: ", len(listeFichier)
	print "Total number of complete files..: ", len(listeFichier_good)

root = ET.Element("root")

liste_i, liste_j, liste_value = [], [], []
liste_l, liste_m, liste_QF, liste_SF = [], [], [], []
n10, n11, n20, n22, n30, n40, n50, n60, n70, n80 = 1, 2, 3, 5, 6, 10, 15, 21, 28, 36

dico = { "id": "0", "neighborsID": " 0 1 2 3", "nom": "1", "dir": "repertoire/", "dE": "0.0 MeV", \
       "beta2": "  0.000", "omega0": "  0.000", "FCHOM0": "  0.000", \
       "omega_x": " 0.000", "omega_y": " 0.000", "omega_z": " 0.000", \
       "Nx": "  0", "Ny": "  0", "Nz": "  0", "Ng_x": "  0", "Ng_y": "  0", "Ng_z": "  0", "LDBASE": "  0",\
       "q20": "0.0 b", "q22": "0.0 b", "q30": "0.0 b^3/2", "q40": "0.0 b^2", \
       "q50": "0.0 b^5/2", "q60": "0.0 b^3", "q70": "0.0 b^7/2", "q80": "0.0 b^4", \
       "EHFB": "0.0 MeV", "E0_GCM": "0.0 MeV", "E0_ATDHF": "0.0 MeV", \
       "deltaN": "0.0 MeV", "deltaP": "0.0 MeV", "EpairN": "0.0 MeV", "EpairP": "0.0 MeV", \
       "lambdaN": "-1.0 MeV", "lambdaP": "-1.0 MeV", \
       "T": "0.0 MeV", "S": "0.0 MeV", \
       "N_QF": "    0.000", "N_SF": "    0.000", "lambda": liste_l, "mu": liste_m, "Q_QF": liste_QF, "Q_SF": liste_SF, \
       "zN": "0.0 fm", "D": "0.0 fm", "qN": "0.0", "Nz": "0.0", \
       "Z1": "0.0", "A1": "0.0", "Z2": "0.0", "A2": "0.0", \
       "q20_1": "0.0 b", "q22_1": "0.0 b", "q30_1": "0.0 b^3/2", "q40_1": "0.0 b^2", \
       "q50_1": "0.0 b^5/2", "q60_1": "0.0 b^3", "q70_1": "0.0 b^7/2", "q80_1": "0.0 b^4", \
       "q20_2": "0.0 b", "q22_2": "0.0 b", "q30_2": "0.0 b^3/2", "q40_2": "0.0 b^2", \
       "q50_2": "0.0 b^5/2", "q60_2": "0.0 b^3", "q70_2": "0.0 b^7/2", "q80_2": "0.0 b^4", \
       "Enuc": "0.0 MeV", "ECou": "0.0 MeV", "ECouDir_exact": "0.0 MeV", "ECouExc_exact": "0.0 MeV", \
       "Ekin_1": "0.0 MeV", "Enuc_1": "0.0 MeV", "Epair_1": "0.0 MeV", \
       "ECouD_1": "0.0 MeV", "ECouE_1": "0.0 MeV", "ECM_1": "0.0 MeV", \
       "Ekin_2": "0.0 MeV", "Enuc_2": "0.0 MeV", "Epair_2": "0.0 MeV", \
       "ECouD_2": "0.0 MeV", "ECouE_2": "0.0 MeV", "ECM_2": "0.0 MeV", \
       "i": liste_i, "j": liste_j, "value": liste_value }

Nprot, Nneut = 0, 0
EDF = 'toto'
temperature = ' 0.000'
pair_n = ('    0.000', '    0.000', '    0.000', '    0.000', '    0.000')
pair_p = ('    0.000', '    0.000', '    0.000', '    0.000', '    0.000')
cut =  '   0.000'

for fichier,i in zip(listeFichier_good,range(0,len(listeFichier_good))):

	skyrme = getStringFromList_safe(force, i)
	noyau = getTupleFromList_safe(nucleus, i, "{0:> 3d}")
	temp = getNumberFromList_safe(Temperature, i, "{0:> 6.3f}")
	Vp_n = getTupleFromList_safe(Vn_pair, i, "{0:> 9.3f}")
	Vp_p = getTupleFromList_safe(Vp_pair, i, "{0:> 9.3f}")
	Ecut = getNumberFromList_safe(cut_off, i, "{0:> 8.3f}")

	same_PES = ( Nneut == noyau[0] ) and ( Nprot == noyau[1] ) and ( EDF == skyrme) \
	                                 and ( temp == temperature ) \
	          and ( Vp_n == pair_n ) and ( Vp_p == pair_p ) and ( Ecut == cut )

	# Header
	if not same_PES:
		PES = ET.SubElement(root, "PES")
		PES.attrib["name"] = "the big test"
		Global = ET.SubElement(PES, "Global")
		nucl = ET.SubElement(Global, "nucleus")
		nucl.attrib["Z"] = noyau[1]
		nucl.attrib["N"] = noyau[0]
		f = ET.SubElement(Global, "force")
		f.attrib["name"] = skyrme
		T = ET.SubElement(Global, "temperature")
		T.attrib["T"] = temp
		VpairN = ET.SubElement(Global, "pairingForceN")
		VpairN.attrib["V0"] = Vp_n[0]
		VpairN.attrib["V1"] = Vp_n[1]
		VpairN.attrib["rho"] = Vp_n[2]
		VpairN.attrib["alpha"] = Vp_n[3]
		VpairP = ET.SubElement(Global, "pairingForceP")
		VpairP.attrib["V0"] = Vp_p[0]
		VpairP.attrib["V1"] = Vp_p[1]
		VpairP.attrib["rho"] = Vp_p[2]
		VpairP.attrib["alpha"] = Vp_p[3]
		PairingCutoff = ET.SubElement(Global, "pairingCutoff")
		PairingCutoff.attrib["Ecut"] = Ecut
		comment = ET.SubElement(Global, "comment")
		comment.text = "Blabla"

		Nprot, Nneut = noyau[1], noyau[0]
		EDF = skyrme
		temperature = temp
		pair_n, pair_p, cut = Vp_n, Vp_p, Ecut

	# Characteristics of the basis
	basis_deform = getNumberFromList_safe(beta2, i, "{0:> 6.3f}")
	basis_frequencies = getTupleFromList_safe(omega, i, "{0:> 7.4f}")
	omega_x, omega_y, omega_z = basis_frequencies
	basis_shells = getTupleFromList_safe(shells, i, "{0:> 3d}")
	N_x, N_y, N_z = basis_shells
	basis_Gauss = getTupleFromList_safe(Gauss, i, "{0:> 3d}")
	Ng_x, Ng_y, Ng_z = basis_Gauss
	LDBASE = getNumberFromList_safe(states, i, "{0:> 6d}")
	base_HFODD = getTupleFromList_safe(basis_HFODD, i, "{0:> 7.4f}")
	omega0, FCHOM0 = base_HFODD

	# Global properties of the compound nucleus
	Etot = getNumberFromList_safe(Etotal, i, "{0:> 13.6f}")
	EpaN = getNumberFromList_safe(Epai_n, i, "{0:> 8.3e}")
	EpaP = getNumberFromList_safe(Epai_p, i, "{0:> 8.3e}")
	DelN = getNumberFromList_safe(delta_n, i, "{0:> 7.3e}")
	DelP = getNumberFromList_safe(delta_p, i, "{0:> 7.3e}")
	lamN = getNumberFromList_safe(Efer_n, i, "{0:> 7.3e}")
	lamP = getNumberFromList_safe(Efer_p, i, "{0:> 7.3e}")
	Stab = getNumberFromList_safe(Estability, i, "{0:> 10.6e}")
	Q_10 = getNumberFromList_1_safe(q_value, i, n10, "{0:> 10.6f}")
	Q_11 = getNumberFromList_1_safe(q_value, i, n11, "{0:> 10.6f}")
	Q_20 = getNumberFromList_1_safe(q_value, i, n20, "{0:> 10.6f}")
	Q_22 = getNumberFromList_1_safe(q_value, i, n22, "{0:> 10.6f}")
	Q_30, Q_40, Q_50, Q_60, Q_70, Q_80 = '  0.0000', '  0.0000', '  0.0000', '  0.0000', '  0.0000', '  0.0000'
	if lambda_max >=3:
		Q_30 = getNumberFromList_1_safe(q_value, i, n30, "{0:> 10.6f}")
	if lambda_max >=4:
		Q_40 = getNumberFromList_1_safe(q_value, i, n40, "{0:> 10.6f}")
	if lambda_max >=5:
		Q_50 = getNumberFromList_1_safe(q_value, i, n50, "{0:> 10.6f}")
	if lambda_max >=6:
		Q_60 = getNumberFromList_1_safe(q_value, i, n60, "{0:> 10.6f}")
	if lambda_max >=7:
		Q_70 = getNumberFromList_1_safe(q_value, i, n70, "{0:> 10.6f}")
	if lambda_max >=8:
		Q_80 = getNumberFromList_1_safe(q_value, i, n80, "{0:> 10.6f}")

	# Neck and fragment properties
	zN, qN, dN, Nz   = '  0.0000', '  0.0000', '  0.0000', '  0.0000'
	Esky, ECou, ECouD, ECouX = '-0000.000',' +000.000','+000.0000', '-000.0000'
	dNQF, dNSF = '   0.0000', '   0.0000'
	ZZ_1, AA_1, ZZ_2, AA_2 = '  0.0000', '  0.0000', '  0.0000', '  0.0000'
	Q20__1, Q22__1, Q30__1, Q40__1 = '   0.0000', '   0.0000', '   0.0000', '   0.0000'
	Q20__2, Q22__2, Q30__2, Q40__2 = '   0.0000', '   0.0000', '   0.0000', '   0.0000'
	Q50__1, Q60__1, Q70__1, Q80__1 = '   0.0000', '   0.0000', '   0.0000', '   0.0000'
	Q50__2, Q60__2, Q70__2, Q80__2 = '   0.0000', '   0.0000', '   0.0000', '   0.0000'
	V0_ATDHF, V0_GCM = '    0.000', '    0.000'
	zN   = getNumberFromList_safe(neck_position, i, "{0:> 8.4f}")
	qN   = getNumberFromList_safe(neck_size, i, "{0:> 8.4f}")
	Nz   = getNumberFromList_safe(neck_protons, i, "{0:> 8.4f}")
	dN   = getNumberFromList_safe(neck_distance, i, "{0:> 8.4f}")
	Esky = getNumberFromList_safe(interaction_skyrme, i, "{0:> 9.3f}")
	ECou = getNumberFromList_safe(interaction_Coulomb, i, "{0:> 9.3f}")
	ECouD  = getNumberFromList_safe(interaction_CoulDirExact, i, "{0:> 9.4f}")
	ECouX  = getNumberFromList_safe(interaction_CoulExcExact, i, "{0:> 9.4f}")
	V0_ATDHF, V0_GCM = getTupleFromList_safe(liste_zpe, i, "{0:> 8.3f}")
	dNQF = getNumberFromList_safe(fluctuations_quantum, i, "{0:> 9.4f}")
	dNSF = getNumberFromList_safe(fluctuations_statistical, i, "{0:> 9.4f}")
	ZZ_1 = getNumberFromList_safe(Z_1, i, "{0:> 8.4f}")
	AA_1 = getNumberFromList_safe(A_1, i, "{0:> 8.4f}")
	ZZ_2 = getNumberFromList_safe(Z_2, i, "{0:> 8.4f}")
	AA_2 = getNumberFromList_safe(A_2, i, "{0:> 8.4f}")
	Q20__1 = getNumberFromList_safe(Q20_1, i, "{0:> 9.4f}")
	Q20__2 = getNumberFromList_safe(Q20_2, i, "{0:> 9.4f}")
	Q22__1 = getNumberFromList_safe(Q22_1, i, "{0:> 9.4f}")
	Q22__2 = getNumberFromList_safe(Q22_2, i, "{0:> 9.4f}")
	Q30__1 = getNumberFromList_safe(Q30_1, i, "{0:> 9.4f}")
	Q30__2 = getNumberFromList_safe(Q30_2, i, "{0:> 9.4f}")
	Q40__1 = getNumberFromList_safe(Q40_1, i, "{0:> 9.4f}")
	Q40__2 = getNumberFromList_safe(Q40_2, i, "{0:> 9.4f}")

	Ekin_1, Enuc_1, Epair_1, ECouD_1, ECouE_1 = '+0000.000', '-0000.000', '-0000.000', '+0000.000', '-0000.000'
	Ekin_2, Enuc_2, Epair_2, ECouD_2, ECouE_2 = '+0000.000', '-0000.000', '-0000.000', '+0000.000', '-0000.000'
	Ekin_1  = getNumberFromList_safe(Tkin_1, i, "{0:> 9.3f}")
	Enuc_1  = getNumberFromList_safe(Vnuc_1, i, "{0:> 9.3f}")
	Epair_1 = getNumberFromList_safe(Vpai_1, i, "{0:> 9.3f}")
	ECouD_1 = getNumberFromList_safe(CouD_1, i, "{0:> 9.3f}")
	ECouE_1 = getNumberFromList_safe(CouE_1, i, "{0:> 9.3f}")
	Ekin_2  = getNumberFromList_safe(Tkin_2, i, "{0:> 9.3f}")
	Enuc_2  = getNumberFromList_safe(Vnuc_2, i, "{0:> 9.3f}")
	Epair_2 = getNumberFromList_safe(Vpai_2, i, "{0:> 9.3f}")
	ECouD_2 = getNumberFromList_safe(CouD_2, i, "{0:> 9.3f}")
	ECouE_2 = getNumberFromList_safe(CouE_2, i, "{0:> 9.3f}")
	Q50__1 = getNumberFromList_safe(Q50_1, i, "{0:> 9.4f}")
	Q50__2 = getNumberFromList_safe(Q50_2, i, "{0:> 9.4f}")
	Q60__1 = getNumberFromList_safe(Q60_1, i, "{0:> 9.4f}")
	Q60__2 = getNumberFromList_safe(Q60_2, i, "{0:> 9.4f}")
	Q70__1 = getNumberFromList_safe(Q70_1, i, "{0:> 9.4f}")
	Q70__2 = getNumberFromList_safe(Q70_2, i, "{0:> 9.4f}")
	Q80__1 = getNumberFromList_safe(Q80_1, i, "{0:> 9.4f}")
	Q80__2 = getNumberFromList_safe(Q80_2, i, "{0:> 9.4f}")

	ECM_1, ECM_2 = '-0000.000', '-0000.000'
	ECM_1 = getNumberFromList_safe(PCM_1, i, "{0:> 9.3f}")
	ECM_2 = getNumberFromList_safe(PCM_2, i, "{0:> 9.3f}")

	# Finite-temperature T and entropy S
	temp, entr = '  0.000000', '  0.000000'
	value_T, value_S = 0.0, 0.0
	if len(Temperature) > 0:
		try:
			value_T = Temperature[i]
			value_S = Entropy[i]
		except IndexError:
			value_T, value_S = 0.0, 0.0
	temp = "{0:> 10.6f}".format(float(value_T))
	entr = "{0:> 10.6f}".format(float(value_S))

	# Fluctuations
	if len(fluctuations_quantum) > 0:
		dis_N_quantum = "{0:> 8.3f}".format(fluctuations_quantum[i])
	if len(fluctuations_statistical) > 0:
		dis_N_statistical = "{0:> 8.3f}".format(fluctuations_statistical[i])
#	if len(dispersion) > 0:
#		dis_Q_all = dispersion[i]

	# Recording results in the XML tree
	if abs(float(Estability[i])) < convergenceCriterion:  #TEST #FILTER
		dico["id"]       = str(i)
		dico["nom"]      = fichier
		dico["dir"]      = current_directory
		# Characteristics of the basis
		dico["beta2"]    = basis_deform
		dico["omega0"]   = omega0
		dico["FCHOM0"]   = FCHOM0
		dico["omega_x"]  = omega_x
		dico["omega_y"]  = omega_y
		dico["omega_z"]  = omega_z
		dico["Nx_HO"]    = N_x
		dico["Ny_HO"]    = N_y
		dico["Nz_HO"]    = N_z
		dico["Ng_x"]     = Ng_x
		dico["Ng_y"]     = Ng_y
		dico["Ng_z"]     = Ng_z
		dico["LDBASE"]   = LDBASE
		# Global nuclear properties
		dico["dE"]       = Stab + " MeV"
		dico["q20"]      = Q_20 + " b"
		dico["q22"]      = Q_22 + " b"
		dico["q30"]      = Q_30 + " b^3/2"
		dico["q40"]      = Q_40 + " b^2"
		dico["q50"]      = Q_50 + " b^5/2"
		dico["q60"]      = Q_60 + " b^3"
		dico["q70"]      = Q_70 + " b^7/2"
		dico["q80"]      = Q_80 + " b^4"
		dico["xi"]       = "{0:> 10.6f}".format((float(AA_2)-float(AA_1))/(float(AA_2)+float(AA_1)))
		dico["EHFB"]     = Etot + " MeV"
		dico["T"]        = temp + " MeV"
		dico["S"]        = entr + " MeV"
		# fluctuations (quantum and statistical)
		dico["N_QF"]     = dis_N_quantum
		dico["N_SF"]     = dis_N_statistical
#		dico["lambda"]   = dis_Q_all[0]
#		dico["mu"]       = dis_Q_all[1]
#		dico["Q_QF"]     = dis_Q_all[2]
#		dico["Q_SF"]     = dis_Q_all[3]
		dico["deltaN"]   = DelN + " MeV"
		dico["deltaP"]   = DelP + " MeV"
		dico["EpairN"]   = EpaN + " MeV"
		dico["EpairP"]   = EpaP + " MeV"
		dico["lambdaN"]  = lamN + " MeV"
		dico["lambdaP"]  = lamP + " MeV"
		dico["zN"]       = zN + " fm"
		dico["D"]        = dN + " fm"
		dico["qN"]       = qN
		dico["Nz"]       = Nz
		# Fission fragment properties
		dico["Z1"]       = ZZ_1
		dico["A1"]       = AA_1
		dico["Z2"]       = ZZ_2
		dico["A2"]       = AA_2
		dico["q20_1"]    = Q20__1 + " b"
		dico["q22_1"]    = Q22__1 + " b"
		dico["q30_1"]    = Q30__1 + " b^3/2"
		dico["q40_1"]    = Q40__1 + " b^2"
		dico["q50_1"]    = Q50__1 + " b^5/2"
		dico["q60_1"]    = Q60__1 + " b^3"
		dico["q70_1"]    = Q70__1 + " b^7/2"
		dico["q80_1"]    = Q80__1 + " b^4"
		dico["q20_2"]    = Q20__2 + " b"
		dico["q22_2"]    = Q22__2 + " b"
		dico["q30_2"]    = Q30__2 + " b^3/2"
		dico["q40_2"]    = Q40__2 + " b^2"
		dico["q50_2"]    = Q50__2 + " b^5/2"
		dico["q60_2"]    = Q60__2 + " b^3"
		dico["q70_2"]    = Q70__2 + " b^7/2"
		dico["q80_2"]    = Q80__2 + " b^4"
		dico["Enuc"]     = Esky + " MeV"
		dico["ECou"]     = ECou + " MeV"
		dico["Ekin_1"]   = Ekin_1 + " MeV"
		dico["Enuc_1"]   = Enuc_1 + " MeV"
		dico["Epair_1"]  = Epair_1 + " MeV"
		dico["ECouD_1"]  = ECouD_1 + " MeV"
		dico["ECouE_1"]  = ECouE_1 + " MeV"
		dico["ECouDir_exact"] = ECouD + " MeV"
		dico["ECouExc_exact"] = ECouX + " MeV"
		dico["ECM_1"]    = ECM_1 + " MeV"
		dico["Ekin_2"]   = Ekin_2 + " MeV"
		dico["Enuc_2"]   = Enuc_2 + " MeV"
		dico["Epair_2"]  = Epair_2 + " MeV"
		dico["ECouD_2"]  = ECouD_2 + " MeV"
		dico["ECouE_2"]  = ECouE_2 + " MeV"
		dico["ECM_2"]    = ECM_2 + " MeV"
		# Collective inertia
# OPTION #TEST #FILTER
#		 Should be commented out if inertia package not used
#		tenseur = liste_Bij[i]
#		l = len(tenseur)
#		liste_value = zip(*[ tenseur[j]['mass'] for j in range(0,l) ])
#		dico["type_bra"]  = [ tenseur[j]['type_bra'] for j in range(0,l) ]
#		dico["type_ket"]  = [ tenseur[j]['type_ket'] for j in range(0,l) ]
#		dico["units_bra"] = [ tenseur[j]['units_bra'] for j in range(0,l) ]
#		dico["units_ket"] = [ tenseur[j]['units_ket'] for j in range(0,l) ]
#		dico["bra"]       = [ tenseur[j]['bra'] for j in range(0,l) ]
#		dico["ket"]       = [ tenseur[j]['ket'] for j in range(0,l) ]
#		dico["M_ATDHF"]   = liste_value[0]
#		dico["M_GCM"]     = liste_value[1]
#		dico["E0_ATDHF"]  = V0_ATDHF
#		dico["E0_GCM"]    = V0_GCM
		# GCM metric
		tenseur = liste_Gij[i]
		l = len(tenseur)
		liste_value = [ tenseur[j]['G'] for j in range(0,l) ]
		dico["type_bra"]  = [ tenseur[j]['type_bra'] for j in range(0,l) ]
		dico["type_ket"]  = [ tenseur[j]['type_ket'] for j in range(0,l) ]
		dico["units_bra"] = [ tenseur[j]['units_bra'] for j in range(0,l) ]
		dico["units_ket"] = [ tenseur[j]['units_ket'] for j in range(0,l) ]
		dico["bra"]       = [ tenseur[j]['bra'] for j in range(0,l) ]
		dico["ket"]       = [ tenseur[j]['ket'] for j in range(0,l) ]
		dico["G"]         = liste_value

		error_flag = point_xml(dico,number_constraints)


# Writing the results in the XML file
tree = ET.ElementTree(root)
tree.write(fichier_PES, pretty_print=True)


elapsed_post = (time.time() - start_post)
print 'Time elapsed for postprocessing ..........: ', elapsed_post

os.system('mv summary/* %s' % current_directory)

timestamp = time.strftime("%m-%d-%Y")
print timestamp

os.system('OUTDIR="$HOME/outputs/%s"; mkdir $OUTDIR' %timestamp )
os.system('OUTDIR="$HOME/outputs/%s/176Pt-fission"; mkdir $OUTDIR' %timestamp )

os.system('cp %s/out/*.xml $HOME/outputs/%s/176Pt-fission' %(current_directory,timestamp))
os.system('cp %s/hfodd.d $HOME/outputs/%s/176Pt-fission' %(current_directory,timestamp))
os.system('cp %s/hfodd_mpiio.d $HOME/outputs/%s/176Pt-fission' %(current_directory,timestamp))
os.system('cp %s/hfodd_path_new.d $HOME/outputs/%s/176Pt-fission' %(current_directory,timestamp))
os.system('cp %s/hfodd_path.d $HOME/outputs/%s/176Pt-fission' %(current_directory,timestamp))

