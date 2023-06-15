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
    animate = (args.Animate == 'True')    # bool value, if true, generate animation of the simulation
    sim_time = args.Time                  # simulation time after source 
    
    NULL = (args.NULL=='True')            # bool value, if false, then simulate with no holes
                                            # (for the purpose of normalizing the flux plot)

    ## fixed parameters ################################################################################
    a_start = 0.43                        # starting periodicity  
    a_end = 0.33                          # ending periodicity    
    s_cav = 0.146                         # cavity length
    r = 0.28                              # hole radius  (units of a)
    h = 0.22                              # waveguide height     
    w = 0.50                              # waveguide width
    dair = 1.00                           # air padding   #should be longer than half-wavelength,
                                                          #one-wavelength is desired
    dpml = 1.00                           # PML thickness (Do not touch)
    Ndef = 3                              # number of defect periods   
    Nwvg = 9                              # number of waveguide periods    

    ## geometry of the device ##########################################################################    
    a_taper = mp.interpolate(Ndef, [a_start,a_end])
    dgap = a_end-2*r*a_end

    ## size of the computation cell 
    sx = 2*(Nwvg*a_start+sum(a_taper))-dgap+s_cav
    sy = dpml+dair+w+dair+dpml
    sz = dpml+dair+h+dair+dpml
    cell_size = mp.Vector3(sx,sy,sz)
    boundary_layers = [mp.PML(dpml)]

    ## material used
    nSi = 3.45   ## use n=2 for SiN
    Si = mp.Medium(index=nSi)

    geometry = [mp.Block(material=Si, center=mp.Vector3(0, +(w+sep)/2, 0), size=mp.Vector3(mp.inf,w,h)),
                mp.Block(material=Si, center=mp.Vector3(0, -(w+sep)/2, 0), size=mp.Vector3(mp.inf,w,h))]
    
    
    
    ## defines holes in the device #####################################################################
    if (NULL):
        for y_pos in [-(w+sep)/2, +(w+sep)/2]:
            ## waveguide holes
            for mm in range(Nwvg):
                geometry.append(mp.Cylinder(material=mp.air, radius=r*a_start, height=mp.inf,
                                            center=mp.Vector3(-0.5*sx+0.5*a_start+mm*a_start,y_pos,0)))
                geometry.append(mp.Cylinder(material=mp.air, radius=r*a_start, height=mp.inf,
                                            center=mp.Vector3(+0.5*sx-0.5*a_start-mm*a_start,y_pos,0)))
            ## taper holes
            for mm in range(Ndef+2):
                geometry.append(mp.Cylinder(material=mp.air, radius=r*a_taper[mm], height=mp.inf,
                                            center=mp.Vector3(-0.5*sx+Nwvg*a_start
                                                              +(sum(a_taper[:mm]) if mm>0 else 0)
                                                              +0.5*a_taper[mm],y_pos,0)))
                geometry.append(mp.Cylinder(material=mp.air, radius=r*a_taper[mm], height=mp.inf,
                                            center=mp.Vector3(+0.5*sx-Nwvg*a_start
                                                              -(sum(a_taper[:mm]) if mm>0 else 0)
                                                              -0.5*a_taper[mm],y_pos,0)))


    ## define the source ###############################################################################
    fmin = 1/lambda_max
    fmax = 1/lambda_min
    fcen = 0.5*(fmin+fmax)
    df = fmax-fmin

    sources = [# first source at the upper cavity
               mp.Source(mp.GaussianSource(fcen, fwidth=df), 
               component=mp.Ey, 
               center=mp.Vector3(0, (w+sep)/2 ,0)),
               #size=mp.Vector3(0,w,0)),
               # second source at the lower cavity
               mp.Source(mp.GaussianSource(fcen, fwidth=df), 
               component=-mp.Ey, 
               center=mp.Vector3(0,-(w+sep)/2,0))]#,
               #size=mp.Vector3(0,w,0))]

    ## symmetry of the system ##########################################################################
    symmetries = [#mp.Mirror(mp.X,+1)] 
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


    # for flux diagram 
    flux_detect_size = mp.Vector3(0, w, h) 
    flux_detect_center_upper_cavity = mp.Vector3(sx/2-dpml-a_end, +(w+sep)/2, 0)
    flux_detect_center_lower_cavity = mp.Vector3(sx/2-dpml-a_end, -(w+sep)/2, 0) 
    freg_upper_cavity = mp.FluxRegion(center=flux_detect_center_upper_cavity, size=flux_detect_size)
    freg_lower_cavity = mp.FluxRegion(center=flux_detect_center_lower_cavity, size=flux_detect_size)
    nfreq = 500 # number of frequencies at which to compute flux
    trans_upper_cavity = sim.add_flux(fcen, df, nfreq, freg_upper_cavity) # transmitted flux
    trans_lower_cavity = sim.add_flux(fcen, df, nfreq, freg_lower_cavity) # transmitted flux

    ## for animation
    if (animate):
        figure = plt.figure(dpi=100)
        Animate = mp.Animate2D(fields=mp.Ey, f=figure, realtime=False, normalize=False,
                               output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(sx, sy, 0)))

        ## run the simulation and save the data #######################################################
        sim.run(mp.in_volume(mp.Volume(center=mp.Vector3(), size=mp.Vector3(sx,sy,0)), 
                             mp.at_end(mp.output_epsilon, mp.output_efield_y)),
                mp.at_every(1, Animate), 
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, -(w+sep)/2, 0), fcen, df)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, +(w+sep)/2, 0), fcen, df)),
                until_after_sources=sim_time) # mp.stop_when_fields_decayed(50, mp.Ey, mp.Vector3(sx-dpml-a_end,0,0), 1e-5))
    
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
                until_after_sources=sim_time) # mp.stop_when_fields_decayed(50, mp.Ey, mp.Vector3(0.5*sx-dpml-0.5), 1e-5))
        
    # for flux plot
    sim.display_fluxes(trans_upper_cavity, trans_lower_cavity)  # print out the flux spectrum


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-Lam_u', type=float, default=1.66, help='maximum source wavelength (default: 1.66)')
    parser.add_argument('-Lam_s', type=float, default=1.46, help='minimum source wavelength (default: 1.46)')
    parser.add_argument('-Sep', type=float, default=0.075, help='edge to edge separation of bands (default: 0.075)')
    parser.add_argument('-Resol', type=float, default=30, help='resolution limit (default: 30 pixels/um)')
    parser.add_argument('-Animate', type=str, default='True',
                        help='generate animation of the simulation or not, True - generate (default: True)')
    parser.add_argument('-NULL', type=str, default='False', 
                        help='run the simulation with no holes for normalization of the flux plot (default: False)')
    parser.add_argument('-Time', type=float, default=100, 
                        help='simulation time after the source is turned off (default: 100)')
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
