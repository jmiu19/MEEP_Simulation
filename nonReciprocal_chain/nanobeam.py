import meep as mp
import cmath
import random
import argparse
import os
import sys
from matplotlib import pyplot as plt
import pandas as pd

def simulation(params):
    """
    define the geometry of the photonic crystal cavity and parameters for Simulation
    then run the simulation   [[!!  units in microns (um) !!]]
    """

    ## settings   ############################################################
    resolution = int(params['Resolution']) # pixels/um
                   # (start with ~50 nanometer mesh for testing)
                   # (~10 nanometer mesh is a typical value for testing)
                   # (~2 nanometer mesh is a typical value for publication)
    ## variable parameters ###################################################
    a_0 = params['a']              # lattice constant (try 0.330 um)
    lambda_min = params['Lam_ss']  # source minimum wavelength
    lambda_max = params['Lam_us']  # source maximum wavelength
    sim_time = params['Times']     # simulation time after source
    animate = params['Animate']    # bool value, true generates animation
    nwvg_up = params['Nwvg_ups']   # number of waveguide holes in upper cavity
    nwvg_lo = params['Nwvg_los']   # number of waveguide holes in lower cavity
    v = params['v']                # separation between nanobeams in a pair
    w = params['w']                # separation between pairs
    x_offset = params['x_offsets']
    numPairs = params['numPairs']  # number of pairs of nanobeams


    NULL = params['NULL']   # bool value, false simulates with no holes
                              # (for the purpose of normalizing the flux plot)

    width = 1.4       # nanobeam width (try 1.4) (exp 1.5)
    r_inc = 0.02      # increment of r/a      (try 0.02 um)
    r_0 = 0.35        # hole radius in unit of periodicity (try 0.35)
    h = 0.14          # waveguide height      (try 0.140 um) (exp 0.130 um)


    dair = 1.00       # air padding   # can try to reduce,
                       # should be longer than half-wavelength,
                       # one-wavelength or longer is desired
    dpml = 1.00       # PML thickness (should fix at 1 um)
    Ndef = 4          # number of defect periods   (try 4)


    ## geometry of the device ################################################
    a_taper = []    # distance between the holes in taper
    r_taper = []    # radius of the holes in the taper
    x_taper = []    # x-position of the center of the holes in the tpaer
    for i in range(Ndef+1):
        r_i = (r_0 - r_inc * (Ndef-i)) * a_0
        a_i = r_i / r_0
        a_taper.append(a_i)
        r_taper.append(r_i)
        x_taper.append(sum(a_taper)-(a_taper[i]/2))

    ## size of the computation cell
    sx = 2*sum(a_taper)+2*max(nwvg_up,nwvg_lo)*a_0+a_0+2.5*dpml+x_offset
    sy = dpml+dair+numPairs*(2*width*a_0+v)+(numPairs-1)*w+dair+dpml # width
    sz = dpml+dair+2*h+dair+dpml              # height of the simulation cell
    cell_size = mp.Vector3(sx,sy,sz)
    boundary_layers = [mp.PML(dpml)]

    ## material used
    nSiN = 2      # refraction index of the material, use n=2 for SiN
    SiN = mp.Medium(index=nSiN)

    ## create the nanobeams
    geometry = []
    halfWidth = width*a_0/2
    for i in range(numPairs):
        y_ctr_lo = -(sy/2)+dpml+dair+(4*i+1)*halfWidth+i*v+i*w
        y_ctr_up = -(sy/2)+dpml+dair+(4*i+3)*halfWidth+(i+1)*v+i*w
        geometry.append(mp.Block(material=SiN,
                                 center=mp.Vector3(0, y_ctr_lo, 0),
                                 size=mp.Vector3(mp.inf,width*a_0,h)))
        geometry.append(mp.Block(material=SiN,
                                 center=mp.Vector3(0, y_ctr_up, 0),
                                 size=mp.Vector3(mp.inf,width*a_0,h)))

    ## define holes in the device ############################################
        if (NULL):
            for j in [0,1]:
                if j==0: # i=0 is the upper nanobeam
                    Nwvg = nwvg_up
                    y_ctr = y_ctr_up
                if j==1: # i=1 is the lower nanobeam
                    Nwvg = nwvg_lo
                    y_ctr = y_ctr_lo
                ## add waveguide holes to the nanobeam
                for mm in range(Nwvg):
                    x_ctr_r = +sum(a_taper)-a_taper[-1]/2+mm*a_0+x_offset/2*(-1)**i
                    x_ctr_l = -sum(a_taper)+a_taper[-1]/2-mm*a_0+x_offset/2*(-1)**i
                    ctr_r = mp.Vector3(x_ctr_r, y_ctr, 0)
                    ctr_l = mp.Vector3(x_ctr_r, y_ctr, 0)
                    geometry.append(mp.Cylinder(material=mp.air,
                                                radius=r_0*a_0,
                                                height=mp.inf,
                                                center=ctr_r))
                    geometry.append(mp.Cylinder(material=mp.air,
                                                radius=r_0*a_0,
                                                height=mp.inf,
                                                center=ctr_l))
                ## add taper holes to the nanobeam
                for mm in range(Ndef):
                    ctr_r = mp.Vector3(+x_taper[mm]+x_offset/2*(-1)**i, y_ctr, 0)
                    ctr_l = mp.Vector3(-x_taper[mm]+x_offset/2*(-1)**i, y_ctr, 0)
                    geometry.append(mp.Cylinder(material=mp.air,
                                                radius=r_taper[mm],
                                                height=mp.inf,
                                                center=ctr_r))
                    geometry.append(mp.Cylinder(material=mp.air,
                                                radius=r_taper[mm],
                                                height=mp.inf,
                                                center=ctr_l))

    ## define the source ####################################################
    fmin = 1/lambda_max
    fmax = 1/lambda_min
    fcen = 0.5*(fmin+fmax)
    df = fmax-fmin

    sources = []
    for i in range(numPairs):
        y_ctr_lo = -(sy/2)+dpml+dair+(4*i+1)*halfWidth+i*v+i*w
        y_ctr_up = -(sy/2)+dpml+dair+(4*i+3)*halfWidth+(i+1)*v+i*w
        aplitude_up = cmath.exp(2*cmath.pi*random.random()*1j)
        amplitude_lo = cmath.exp(2*cmath.pi*random.random()*1j)
        sources.append(mp.Source(mp.GaussianSource(fcen, fwidth=df),
                                 amplitude=aplitude_lo,
                                 component=mp.Ey,
                                 center=mp.Vector3(0, y_ctr_lo, h)))
        sources.append(mp.Source(mp.GaussianSource(fcen, fwidth=df),
                                 amplitude=amplitude_up,
                                 component=mp.Ey,
                                 center=mp.Vector3(0, y_ctr_up, h)))

    ## symmetry of the system ###############################################
    symmetries = [#mp.Mirror(mp.X,+1),
                  #mp.Mirror(mp.Y,-1),
                  mp.Mirror(mp.Z,+1)]   ## put symmetry in z direction

    ## define the simulation and detector objects ###########################
    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=boundary_layers,
                        geometry=geometry,
                        sources=sources,
                        dimensions=3,
                        symmetries=symmetries)

    ## for flux diagram
    flux_detectors = []
    for i in range(numPairs):
        y_pos = -(sy/2)+dpml+dair+(4*i+2)*halfWidth+(i+1/2)*v+i*w
        freg_between = mp.FluxRegion(center=mp.Vector3(0, y_pos, 0),
                         size=mp.Vector3(0.8*(sx-2*dpml), 0, 0.8*(sz-2*dpml)))
        nfreq = 500 # number of frequencies at which to compute flux
        flux_detectors.append(sim.add_flux(fcen, df, nfreq, freg_between))


    ## for animation
    if (animate):
        figure = plt.figure(dpi=100)
        Animate = mp.Animate2D(fields=mp.Ey, f=figure,
                               realtime=False, normalize=False,
                               output_plane=mp.Volume(center=mp.Vector3(),
                                                      size=mp.Vector3(sx,sy,0)))

        ## run the simulation and save the data #############################
        sim.run(mp.in_volume(mp.Volume(center=mp.Vector3(),
                             size=mp.Vector3(sx,sy,0)),
                             mp.at_end(mp.output_epsilon, mp.output_efield_y)),
                mp.at_every(1, Animate),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, 0, 0), fcen, df)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, sy/2, 0), fcen, df)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, -sy/2, 0), fcen, df)),
                until_after_sources=sim_time)

        # save the animation
        filename = ("output/animation/animation[w"+str(w)+'-v'+str(v)+"].mp4")
        Animate.to_mp4(10, filename)
    else:
        ## run the simulation and save the data ##############################
        sim.run(mp.in_volume(mp.Volume(center=mp.Vector3(),
                             size=mp.Vector3(sx,sy,0)),
                             mp.at_end(mp.output_epsilon, mp.output_efield_y)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, 0, 0), fcen, df)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, sy/2, 0), fcen, df)),
                mp.after_sources(mp.Harminv(mp.Ey, mp.Vector3(0, -sy/2, 0), fcen, df)),
                until_after_sources=sim_time)

    # for flux plot
    # print out the flux spectrum
    n_detector = 0
    for detector in flux_detectors:
        meep.display_csv("flux"+str(n_detector), meep.get_flux_freqs(detector))
        n_detector += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-params', type=str,
                        default='[60,0.05,0.6,0.85,True,300,3,10]',
                        help='a python string that contains the parameters')
    args = parser.parse_args()
    params_csv = pd.read_csv('parameters.csv', index_col=0)
    params = params_csv.loc[args.params]
    simulation(params)
