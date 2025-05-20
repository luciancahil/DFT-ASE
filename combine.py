
from ase.build import bulk, surface
from ase.io import read


name = "NaCl"

rocksalt = bulk('NaCl', crystalstructure='rocksalt', a=6.0)

atoms = read("TaAgO3.poscar")

# Define the Miller indices (h, k, l) for the surface
miller_indices = (1, 0, 0)  # Change this to (1,1,1) or any other plane

layers = 1
vacuum = 100.0  
slab = surface(atoms, miller_indices, layers, vacuum)

breakpoint()

#TODO: Allow selection of pseudo potentials
pseudopotentials = {'Na': 'Na.pbe-spn-kjpaw_psl.1.0.0.UPF', 'Cl': 'Cl.pbe-n-kjpaw_psl.1.0.0.UPF'}

masses = {"H": 1.0, "O":16.0, "Na":22.99, "Cl":35.453 }
# Optionally create profile to override paths in ASE configuration:
profile = {'command':'/home/roy/anaconda3/envs/qe/bin/pw.x', 'pseudo_dir':'./psudos'}

#TODO: Change the total number of atoms
boilerplate = open("Dummy.in", mode='r')

output = open("{}.in".format(name), mode='w')

for line in boilerplate:
    output.write(line)


for atom in rocksalt:
    symbol = atom.symbol
    output.write(" {} {:.3f} {}\n".format(symbol, masses[symbol], pseudopotentials[symbol]))



output.write("ATOMIC_POSITIONS (angstrom)\n")

for atom in rocksalt:
    symbol = atom.symbol
    pos = atom.position
    output.write(" {} {:.2f} {:.2f} {:.2f}\n".format(symbol, pos[0], pos[1], pos[2]))

output.write("K_POINTS (gamma)\n")