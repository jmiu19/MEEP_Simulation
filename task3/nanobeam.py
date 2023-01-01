import meep as mp
import argparse
import os
import sys
from matplotlib import pyplot as plt

def main(args):
    """
    define the geometry of the photonic crystal cavity and parameters for Simulation
    then run the simulation   [[!!  units in microns (um) !!]]
    """

    resolution = 40                       # pixels/um
                                          #(start with ~50 nanometer mesh for testing)
                                          #(~10 nanometer mesh is a typical value for testing)
                                          #(~2 nanometer mesh is a typical value for publication)

    a_start = args.a_start                # starting periodicity  (lattice constant, try 0.410 um)
    a_end = args.a_end                    # ending periodicity    (try 0.330 um)
    s_cav = args.s_cav                    # cavity length
    r = args.r                            # hole radius           (in unit of periodicity)
    h = args.hh                           # waveguide height      (try 0.140 um)
    w = args.w                            # waveguide width       (try 0.500 um)

    dair = 1.00                           # air padding   # can try to reduce,
                                                          # should be longer than half-wavelength,
                                                          # one-wavelength or longer is desired
    dpml = 1.00                           # PML thickness (Do not touch)

    Ndef = args.Ndef                      # number of defect periods   (try 4)
    a_taper = mp.interpolate(Ndef-1, [a_start,a_end])[1:]

    Nwvg = args.Nwvg                      # number of waveguide periods
                                          # (can try smaller number to reduce simulation time)
    sx = 2*(Nwvg*a_start+sum(a_taper))-a_end+s_cav+2*r*a_end     # length of the crystal cavity
    sy = dpml+dair+w+dair+dpml                                   # width of the simulation cell
    sz = dpml+dair+h+dair+dpml                                   # height of the simulation cell

    cell_size = mp.Vector3(sx,sy,sz)
    boundary_layers = [mp.PML(dpml)]

    nSiN = 2      # index of refraction of the material of the photonic crystal cavity, use n=2 for SiN
    SiN = mp.Medium(index=nSiN)

    ## create the band
    geometry = [mp.Block(material=SiN, center=mp.Vector3(), size=mp.Vector3(mp.inf,w,h))]

    ## add holes (waveguide) to the band
    for mm in range(Nwvg):
        geometry.append(mp.Cylinder(material=mp.air, radius=r*a_start, height=mp.inf,
                                    center=mp.Vector3(-0.5*sx+0.5*a_start+mm*a_start,0,0)))
        geometry.append(mp.Cylinder(material=mp.air, radius=r*a_start, height=mp.inf,
                                    center=mp.Vector3(+0.5*sx-0.5*a_start-mm*a_start,0,0)))
    ## add holes (taper) to the band
    for mm in range(Ndef):
        geometry.append(mp.Cylinder(material=mp.air, radius=r*a_taper[mm], height=mp.inf,
                                    center=mp.Vector3(-0.5*sx+Nwvg*a_start+(sum(a_taper[:mm]) if mm>0 else 0)+0.5*a_taper[mm],0,0)))
        geometry.append(mp.Cylinder(material=mp.air, radius=r*a_taper[mm], height=mp.inf,
                                    center=mp.Vector3(+0.5*sx-Nwvg*a_start-(sum(a_taper[:mm]) if mm>0 else 0)-0.5*a_taper[mm],0,0)))

    ## define the source
    lambda_min = 0.72        # minimum source wavelength  (do 0.72 um)
    lambda_max = 0.77        # maximum source wavelength  (do 0.77 um)
    fmin = 1/lambda_max
    fmax = 1/lambda_min
    fcen = 0.5*(fmin+fmax)
    df = fmax-fmin

    sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df), component=mp.Ey, center=mp.Vector3())]

    symmetries = [mp.Mirror(mp.X,+1), mp.Mirror(mp.Y,-1), mp.Mirror(mp.Z,+1)]

    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=boundary_layers,
                        geometry=geometry,
                        sources=sources,
                        dimensions=3,
                        symmetries=symmetries)

    ## For animation
    sim.reset_meep()
    figure = plt.figure(dpi=100)
    Animate = mp.Animate2D(fields=mp.Ey, f=figure, realtime=False, normalize=True,
                           output_plane=mp.Volume(center=mp.Vector3(0,0,0),size=mp.Vector3(sx, sy, 0)))
    plt.close()

    # run the simulation
    sim.run(mp.in_volume(mp.Volume(center=mp.Vector3(), size=mp.Vector3(sx,sy,0)), mp.at_end(mp.output_epsilon, mp.output_efield_y)),
            mp.at_every(1, Animate), mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(), fcen, df)),
            until_after_sources=500)

    # save the animation
    filename = "output/animation.mp4"
    Animate.to_mp4(10, filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a_start', type=float, default=0.41, help='starting periodicity (default: 0.41 um)')
    parser.add_argument('-a_end', type=float, default=0.33, help='ending periodicity (default: 0.33 um)')
    parser.add_argument('-s_cav', type=float, default=0.146, help='cavity length (default: 0.146 um)')
    parser.add_argument('-r', type=float, default=0.35, help='hole radius (default: 0.35 in unit of a)')
    parser.add_argument('-hh', type=float, default=0.14, help='waveguide height (default: 0.14 um)')
    parser.add_argument('-w', type=float, default=0.50, help='waveguide width (default: 0.50 um)')
    parser.add_argument('-Ndef', type=int, default=4, help='number of defect periods (default: 4)')
    parser.add_argument('-Nwvg', type=int, default=8, help='number of waveguide periods (default: 8)')
    args = parser.parse_args()
    main(args)



"""
lattice constant a = 330 nm

width = 1.4a
radius = 0.35a
increment of 0.02 for the taper
update a for the taper to maintain the ratio of r/a=0.35

edge to edge distance between two bands:
50 nanometers as minimum for practical purpose
100 nanometers should have some coupling effect
"""
