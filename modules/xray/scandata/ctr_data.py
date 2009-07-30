##############################################################################
"""
T. Trainor (fftpt@uaf.edu)
Frank Heberling (Frank.Heberling@ine.fzk.de)
Functions for extracting ctr data from ScanData objects

Modifications:
--------------
"""
##############################################################################
"""
Todo
- Test!
- sorting and specify HK for plots
- averaging/merging and merge statistics
- corrections for rocking scans
"""
#############################################################################

import types
import pylab
import numpy as Num
from xtal.active_area import active_area

##############################################################################
def append_ctr(scans,ctr=None,I_lbl='I_c',Ierr_lbl='Ierr_c',AAparams=[]):
    if ctr == None:
        return CtrData(scans=scans,I_lbl=I_lbl,Ierr_lbl=Ierr_lbl,AAparams=AAparams)
    else:
        return ctr.append_data(scans)

##############################################################################
class CtrData:
    def __init__(self,scans=[],I_lbl='I_c',Ierr_lbl='Ierr_c',AAparams=[]):
        #
        self.I_lbl    = I_lbl
        self.Ierr_lbl = Ierr_lbl
        self.AAparams = AAparams
        #
        self.H    = Num.array([],float)
        self.K    = Num.array([],float)
        self.L    = Num.array([],float)
        self.I0   = Num.array([],float)
        self.I    = Num.array([],float)
        self.Ierr = Num.array([],float)
        self.corr = Num.array([],float)
        self.F    = Num.array([],float)
        self.Ferr = Num.array([],float)
        #
        self.append_data(scans)

    ##########################################################################
    def append_data(self,scans):
        """
        scans is a list of scan data objects
        """
        if type(scans) != types.ListType:
            scans = [scans]

        for scan in scans:
            #fill dictionary with data from all scans
            self.H    = Num.append(self.H,scan.scalers['H'])
            self.K    = Num.append(self.K,scan.scalers['K'])
            self.L    = Num.append(self.L,scan.scalers['L'])
            self.I0   = Num.append(self.I0,scan.scalers['io'])
            self.I    = Num.append(self.I,scan.image_peaks[self.I_lbl])
            self.Ierr = Num.append(self.Ierr,scan.image_peaks[self.Ierr_lbl])
            # the correction Factor is multiplied by 17000 to rescale to Counts/sec
            corr = self.calc_correction(scan)*17000 
            F    = (corr*scan.image_peaks[self.I_lbl])**0.5
            Ferr = (corr*scan.image_peaks[self.Ierr_lbl])**0.5
            #
            self.corr = Num.append(self.corr,corr)
            self.F    = Num.append(self.F,F)
            self.Ferr = Num.append(self.Ferr,Ferr)

    ##########################################################################
    def calc_correction(self,scan):
        """
        correction factors for pilatus
        """
        #calculate correction factors for specular rods
        if (Num.abs(scan.scalers['H'][0]) < 0.01 and \
            Num.abs(scan.scalers['K'][0]) < 0.01) :
            Cp = 1 - Num.sin(Num.radians(scan.scalers['nu']))**2
            Ci = Num.sin(Num.radians(scan.scalers['nu']/2))
        #or calculate correction factors for off-specular rods
        else:
            Cp = 1 - Num.cos(Num.radians(scan.scalers['del']))**2 * \
                 Num.sin(Num.radians(scan.scalers['nu']))**2
            Ci = Num.cos(Num.radians(scan.scalers['del'])) * \
                 Num.sin(Num.radians(scan.scalers['Beta']))

        if self.AAparams != [] and len(self.AAparams) == 7:
            d1 = self.AAparams[0]
            d2 = self.AAparams[1]
            phi_d1 = self.AAparams[2]
            phi_d2 = self.AAparams[3]
            Bwidth = self.AAparams[4]
            Bheight = self.AAparams[5]
            Debug = self.AAparams[6]

            footprint, spilloff = active_area(scan,d1,d2,phi_d1,phi_d2,Bwidth,Bheight,Debug)
        else:
            footprint = Num.ones((scan.dims[0]))
            spilloff  = Num.ones((scan.dims[0]))

        corr = Ci/(Cp*scan.scalers['io']*spilloff*footprint)
        
        return corr

    ##########################################################################
    def plot(self):
        """
        plot the rod
        """
        pylab.figure()
        pylab.plot(self.L, self.F,'b')
        pylab.errorbar(self.L,self.F,self.Ferr, fmt ='o')
        pylab.semilogy()
        pylab.show()

    ##########################################################################
    def write_HKL(self,fname = 'ctr.hkl'):
        #write data file for row data
        f = open(fname, 'w')
        f.write('#idx        H            K            L            F           F_err \n')
        for i in range(len(self.L)):
            if self.I[i] > 0:
                line = "%i    %i    %i    %6.3f    %6.6g    %6.6g\n" % (i,
                                                                  self.H[i],
                                                                  self.K[i],
                                                                  self.L[i],
                                                                  self.F[i],
                                                                  self.Ferr[i])
                f.write(line)
        f.close()
