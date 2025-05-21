
from ase.build import bulk, surface
from ase.io import read
from decimal import Decimal

'%.2E' % Decimal('40800000000.00000000000000')

def write_boiler(output, a, b, c, natoms, ntype):
    output.write("&CONTROL\n")
    output.write("    calculation = \"relax\"\n")
    output.write("    max_seconds =  8.64000e+04\n")
    output.write("    pseudo_dir  = \".\"\n")
    output.write("/\n")
    output.write("\n")
    output.write("&SYSTEM\n")
    output.write("    a           =  %.5E\n" % Decimal(a))
    output.write("    b           =  %.5E\n" % Decimal(b))
    output.write("    c           =  %.5E\n" % Decimal(c))
    output.write("    degauss     =  1.00000e-02\n")
    output.write("    ecutrho     =  5.00000e+02\n")
    output.write("    ecutwfc     =  5.00000e+01\n")
    output.write("    ibrav       = 6\n")
    output.write("    nat         = {}\n".format(natoms))
    output.write("    ntyp        = {}\n".format(ntype))
    output.write("    occupations = \"fixed\"\n")
    output.write("    smearing    = \"gaussian\"\n")
    output.write("/\n")
    output.write("\n")
    output.write("&ELECTRONS\n")
    output.write("    conv_thr         =  1.00000e-06\n")
    output.write("    electron_maxstep = 200\n")
    output.write("    mixing_beta      =  7.00000e-01\n")
    output.write("    startingpot      = \"atomic\"\n")
    output.write("    startingwfc      = \"atomic+random\"\n")
    output.write("/\n")
    output.write("\n")
    output.write("K_POINTS {gamma}\n")
    output.write("\n")
    output.write("ATOMIC_SPECIES\n")


name = "TaAgO3"

rocksalt = bulk('NaCl', crystalstructure='rocksalt', a=6.0)

atoms = read("TaAgO3.poscar")

# Define the Miller indices (h, k, l) for the surface
miller_indices = (1, 0, 0)  # Change this to (1,1,1) or any other plane

layers = 1
vacuum = 100.0  
slab = surface(atoms, miller_indices, layers, vacuum)


# coordinates

a = slab.cell[0][0].item()
b = slab.cell[1][1].item()
c = (a + b) * 2.5
output = open("{}.in".format(name), mode='w')
natoms = len(slab)
ntype = len(set(atoms.get_atomic_numbers()))

write_boiler(output, a, b, c, natoms, ntype)


#TODO: Allow selection of pseudo potentials
pseudopotentials = {'Na': 'Na.pbe-spn-kjpaw_psl.1.0.0.UPF', 'Cl': 'Cl.pbe-n-kjpaw_psl.1.0.0.UPF'}

masses = {"H": 1.0, "O":16.0, "Na":22.99, "Cl":35.453 }
# Optionally create profile to override paths in ASE configuration:
profile = {'command':'/home/roy/anaconda3/envs/qe/bin/pw.x', 'pseudo_dir':'./psudos'}

#TODO: Change the total number of atoms
boilerplate = open("Dummy.in", mode='r')





for atom in rocksalt:
    symbol = atom.symbol
    output.write(" {} {:.3f} {}\n".format(symbol, masses[symbol], pseudopotentials[symbol]))



output.write("ATOMIC_POSITIONS (angstrom)\n")

for atom in rocksalt:
    symbol = atom.symbol
    pos = atom.position
    output.write(" {} {:.2f} {:.2f} {:.2f}\n".format(symbol, pos[0], pos[1], pos[2]))

output.write("K_POINTS (gamma)\n")