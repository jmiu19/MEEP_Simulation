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

    ## settings   ######################################################################################
    resolution = args.Resol               # pixels/um
                                          # (start with ~50 nanometer mesh for testing)
                                          # (~10 nanometer mesh is a typical value for testing)
                                          # (~2 nanometer mesh is a typical value for publication)
    ## variable parameters #############################################################################
    sep = args.Sep                        # separation distance between cavities
    lambda_min = args.Lam_s               # source minimum wavelength
    lambda_max = args.Lam_u               # source maximum wavelength
    sim_time = args.Time                  # simulation time after source
    animate = (args.Animate == 'True')    # bool value, if true, generate animation of the simulation

    NULL = (args.NULL=='True')            # bool value, if false, then simulate with no holes
                                            # (for the purpose of normalizing the flux plot)

    a_0 = 0.33                            # lattice constant      (try 0.330 um)
    r_inc = 0.02                          # increment of r/a      (try 0.02 um)
    r_0 = 0.35                            # hole radius in unit of periodicity (try 0.35)
    h = 0.14                              # waveguide height      (try 0.140 um)
    w = 1.4                               # waveguide width       (try 1.4 in unit of a)

    dair = 1.00                           # air padding   # can try to reduce,
                                                          # should be longer than half-wavelength,
                                                          # one-wavelength or longer is desired
    dpml = 1.00                           # PML thickness (Do not touch)
    Ndef = 4                              # number of defect periods   (try 4)
    Nwvg = 10                             # number of waveguide periods
    
    
    ## geometry of the device ##########################################################################    
    a_taper = []    # distance between the holes in taper
    r_taper = []    # radius of the holes in the taper
    x_taper = []    # x-position of the center of the holes in the tpaer
    for i in range(Ndef+1):
        r_i = (r_0 - r_inc * (Ndef-i)) * a_0
        a_i = r_i / r_0
        a_taper.append(a_i)
        r_taper.append(r_i)
        x_taper.append(sum(a_taper)-(a_taper[i]/2))

    ## Old Design ############################
    # for i in range(Ndef+1):
    #     if i == 0:
    #         a_i = a_0
    #     else:
    #         a_i =  r_taper[-1] / 0.35
    #     r_i = (r-r_inc*i) * a_i
    #     r_taper.append(r_i)
    #     a_taper.append(a_i)
    #########################################


    
    ## size of the computation cell 
    sx = 2*sum(a_taper) + 2*(Nwvg-1)*a_0 + a_0       # length of the crystal cavity
    sy = dpml+dair+2*(w*a_0)+sep+dair+dpml           # width of the simulation cell
    sz = dpml+dair+h+dair+dpml                       # height of the simulation cell
    cell_size = mp.Vector3(sx,sy,sz)
    boundary_layers = [mp.PML(dpml)]

    ## material used
    nSiN = 2      # refraction index of the material, use n=2 for SiN
    SiN = mp.Medium(index=nSiN)

    ## create the band
    geometry = [mp.Block(material=SiN, center=mp.Vector3(0, +(w*a_0+sep)/2, 0), size=mp.Vector3(mp.inf,w*a_0,h)),
                mp.Block(material=SiN, center=mp.Vector3(0, -(w*a_0+sep)/2, 0), size=mp.Vector3(mp.inf,w*a_0,h))]

    ## defines holes in the device #####################################################################
    if (NULL):
        for i in [0,1]:
            ## add holes (waveguide) to the band
            for mm in range(Nwvg):
                geometry.append(mp.Cylinder(material=mp.air, radius=r_0*a_0, height=mp.inf,
                                            center=mp.Vector3(+sum(a_taper)-a_taper[-1]/2+mm*a_0, ((-1)**i)*(w*a_0+sep)/2, 0)))
                geometry.append(mp.Cylinder(material=mp.air, radius=r_0*a_0, height=mp.inf,
                                            center=mp.Vector3(-sum(a_taper)+a_taper[-1]/2-mm*a_0, ((-1)**i)*(w*a_0+sep)/2, 0)))
            ## add holes (taper) to the band
            for mm in range(Ndef):
                geometry.append(mp.Cylinder(material=mp.air, radius=r_taper[mm], height=mp.inf,
                                            center=mp.Vector3(+x_taper[mm], ((-1)**i)*(w*a_0+sep)/2, 0)))
                geometry.append(mp.Cylinder(material=mp.air, radius=r_taper[mm], height=mp.inf,
                                            center=mp.Vector3(-x_taper[mm], ((-1)**i)*(w*a_0+sep)/2, 0)))

    ## define the source ###############################################################################
    fmin = 1/lambda_max
    fmax = 1/lambda_min
    fcen = 0.5*(fmin+fmax)
    df = fmax-fmin

    sources = [# source at upper cavity
               mp.Source(mp.GaussianSource(fcen, fwidth=df),
               component=mp.Ey, center=mp.Vector3(0, +(w*a_0+sep)/2, 0)),
               #size=mp.Vector3(0,3*(w*a_0),0)),
               # source at lower cavity
               mp.Source(mp.GaussianSource(fcen, fwidth=df),
               component=-mp.Ey, center=mp.Vector3(0, -(w*a_0+sep)/2, 0))]# ,
               #size=mp.Vector3(0,3*(w*a_0),0)),]

    ## symmetry of the system ##########################################################################
    symmetries = [mp.Mirror(mp.X,+1),             ## try symmetry in x direction    
                  #mp.Mirror(mp.Y,-1), 
                  mp.Mirror(mp.Z,+1)]             ## only put symmetry in z direction

    ## define the simulation and detector objects ######################################################
    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=boundary_layers,
                        geometry=geometry,
                        sources=sources,
                        dimensions=3,
                        symmetries=symmetries)

    ## for flux diagram
    freg_upper_cavity = mp.FluxRegion(center=mp.Vector3(+sum(a_taper)+6*a_0, +(w*a_0+sep)/2, 0), 
                                      size=mp.Vector3(0, (w*a_0), h))
    freg_lower_cavity = mp.FluxRegion(center=mp.Vector3(+sum(a_taper)+6*a_0, -(w*a_0+sep)/2, 0), 
                                      size=mp.Vector3(0, (w*a_0), h))
    nfreq = 500 # number of frequencies at which to compute flux
    trans_upper_cavity = sim.add_flux(fcen, df, nfreq, freg_upper_cavity) 
    trans_lower_cavity = sim.add_flux(fcen, df, nfreq, freg_lower_cavity) 

    ## for animation
    if (animate):
        figure = plt.figure(dpi=100)
        Animate = mp.Animate2D(fields=mp.Ey, f=figure, realtime=False, normalize=False,
                               output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(sx, sy, 0)))

        ## run the simulation and save the data #######################################################
        sim.run(mp.in_volume(mp.Volume(center=mp.Vector3(), size=mp.Vector3(sx,sy,0)), 
                             mp.at_end(mp.output_epsilon, mp.output_efield_y)),
                mp.at_every(1, Animate), 
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, -(w*a_0+sep)/2, 0), fcen, df)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, +(w*a_0+sep)/2, 0), fcen, df)),
                until_after_sources=sim_time) # mp.stop_when_fields_decayed(50, mp.Ey, mp.Vector3(+sum(a_taper)+6*a_0), 1e-3))
    
        # save the animation
        filename = ("output/animation["+str(lambda_max)+','
                                       +str(lambda_min)+'.'
                                       +str(sep)+','
                                       +str(NULL)+"].mp4")
        Animate.to_mp4(10, filename)
    else:
        ## run the simulation and save the data #######################################################
        sim.run(mp.in_volume(mp.Volume(center=mp.Vector3(), size=mp.Vector3(sx,sy,0)), 
                             mp.at_end(mp.output_epsilon, mp.output_efield_y)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, -(w*a_0+sep)/2, 0), fcen, df)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, +(w*a_0+sep)/2, 0), fcen, df)),
                until_after_sources=sim_time) # mp.stop_when_fields_decayed(50, mp.Ey, mp.Vector3(+sum(a_taper)+6*a_0,0,0), 1e-3))
        
    # for flux plot
    sim.display_fluxes(trans_upper_cavity, trans_lower_cavity)  # print out the flux spectrum


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-Lam_u', type=float, default=0.77, help='source maximal wavelength (default: 0.77)')
    parser.add_argument('-Lam_s', type=float, default=0.72, help='source minimal wavelength (default: 0.72)')
    parser.add_argument('-Sep', type=float, default=0.075, help='edge to edge separation of bands (default: 0.1)')
    parser.add_argument('-Resol', type=float, default=30, help='resolution limit (default: 30 pixels/um)')
    parser.add_argument('-NULL', type=str, default='True', 
                        help=('run the simulation with no holes for normalization of the flux plot, '+
                              'true with holes, false with no holes (default: True)'))
    parser.add_argument('-Animate', type=str, default='Fase',
                        help='generate animation of the simulation or not, True - generate (default: True)')
    parser.add_argument('-Time', type=float, default=100,
                        help='simulation time after the source has been removed (default: 100)')
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
75 nanometers as minimum for practical purpose
100 nanometers should have some coupling effect
"""
