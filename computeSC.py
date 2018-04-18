import wave
import numpy as np
from optparse import OptionParser
import array



def wavread(file_name,verbose=False):
    '''
    Read a wave file and convert in samples scales to -1.0 -- 1.0
    Only read wave files of 16 bits and 1 channel.
    
    Args:
        file_name: File name to read
        verbose: Print features if set at true
    Returns:
        samples: The samples scales to -1.0 -- 1.0 extracts from the file
        sample_rate: Sample rate of the original signal      
        
    P. Guyot - January 2014 - Last update April 2018    
    '''
    
    stream = wave.open(file_name,"rb")

    num_channels = stream.getnchannels()
    sample_rate = stream.getframerate()
    sample_width = stream.getsampwidth() # sample width in bites
    num_frames = stream.getnframes()
    
    nb_bits=sample_width*8 # number of samples in bit
    
    if verbose:
        print "Reading file : ", file_name
        print "\t Number of channels : ", num_channels
        print "\t Sample rate : ", sample_rate
        print "\t Number of bits : : ", nb_bits
        print "\t Number of frames : ", num_frames
    
    if (nb_bits!=16):
        raise Exception('Error : Bit quantification differs from 16. Bit quantification = ', nb_bits)   
      
    if (num_channels!=1):
        raise Exception('Error : More than one channel. Number of channels = ',num_channels)          
    
    signal_bin=stream.readframes(num_frames)    # signal (string of bytes)
    signal_int=np.array(array.array('H',signal_bin),'int16')    # signal (int 16)
    
    # scale to -1.0 -- 1.0
    max_nb_bit = float(2**(nb_bits-1))  
    samples = signal_int / (max_nb_bit + 1.0)
    
    if verbose:
        print ""
    return samples,sample_rate
    

def spectro(x, n_win, n_step):  
    '''
    Spectrogram of a signal.
    Hamming window.
    
    Args:
        signal: The signal
        n_win: Number of samples for one frame
        n_step : step = hop = number of samples of one step
        
    Returns:    
        X : spectrogram of the signal  
    '''
    n_fft=n_win
    
    window=np.hamming(n_win) # Hamming window
    
    n_x_fft=range(n_win, len(x), n_step) # vecteur contenant les indices (fin de fenetre) de chaque fft   
    X = np.zeros( (n_fft/2, len(n_x_fft)) )
    
    for i,n in enumerate(n_x_fft) :
        xseg=x[n-n_win:n]
        z = np.fft.fft(window * xseg)    
        X[:,i]=np.abs(z[:n_fft/2])
    return X






def spectralcover(X,sr,gamma):
    '''
    Spectral cover of a spectrogram X
    
    Args:
        X : spectrogram of an audio signal
        sr : sampling rate of the audio signal
        gamma : tunning of the spectral cover (default = 1;5)
    Returns: 
        sp
    '''    
    
    n_fft=len(X[:,1])
    f_max=sr/2;
    vect_freq=np.linspace(f_max/n_fft,f_max,n_fft) 
    return np.array([sum((trame*vect_freq)**2) / (sum(trame)) ** gamma for trame in X.T])
        
        
                   
              
    
def parse_options():
    usage = "usage: %prog filename [-o fileout] [-w winsize] [-s hopsize] [-m] [-d minimumduration] [-f minimum_file_out] [-g gamma] [-v]"
    description = "Compute the spectral cover values from a wave sound file. Output syntax is: time_in \\t time_out \\t value  "
    epilog = "See the article \"Water flow detection from a wearable device with a new feature, the spectral cover. Proceedings of the International Workshop on Content-Based Multimedia Indexing (CBMI 2012), IEEE\" for more informations about the spectral cover."
    parser = OptionParser(usage=usage, description=description, epilog=epilog)
    parser.add_option("-o", dest="file_out", default="out.txt", help="Output file. Default:%default", metavar="file_name")
    parser.add_option("-w", type="int", dest="n_win", metavar="window_size", default=512, help="Window size (samples). Default:%default")
    parser.add_option("-s", type="int", dest="n_step", metavar="hop_size", default=256, help="Hop size (samples). Default:%default")
    parser.add_option("-v", action="store_true", dest="verbose", default=False, help="Verbose. Default:%default")
    parser.add_option("-m", action="store_true", dest="minimum", default=False, help="Compute the spectral cover minimum. Default:%default")
    parser.add_option("-d", type="float", dest="s_minimum", metavar="minimum_window", default=2, help="Minimum window duration (seconds). Default:%default")
    parser.add_option("-f", dest="minimum_file_out", default="minimum.out.txt", help="Minimum output file. Default:%default", metavar="minimum_file_out")
    parser.add_option("-g", type="float", dest="gamma", default="1.5", help="Gamma parameter. Default:%default", metavar="gamma")
    
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        
    return (options, args) 
    

##########################################################################################
#SCRIPT
##########################################################################################
if __name__=="__main__":
    
    # Features computation
    
    
    (options, args)=parse_options()
    filename=args[0]
    n_win=options.n_win
    n_step=options.n_step
    file_out=options.file_out
    verbose=options.verbose
    minimum=options.minimum
    s_minimum=options.s_minimum
    minimum_file_out=options.minimum_file_out
    gamma=options.gamma
   
   
  
    signal,sr= wavread(filename,verbose=verbose)
    #sr,signal=scipy_wavread(file_name)
    if verbose: 
        print 'Spectral cover computation...'
        print 'Window size: ', n_win
        print 'Hop size: ', n_step
        print 'Gamma: ', gamma
        
        
    duration=np.shape(signal)[0]/sr
     
    
     
    X=spectro(signal, n_win, n_step)
    
   
    sp=spectralcover(X, sr, gamma)
      

    sr_sp=len(sp)/float(duration)
    
    
    f=open(file_out,'w')
    for i in range(len(sp)):
        time_in=i/ float(sr_sp)
        time_out= (i+1)/ float(sr_sp)
        f.write(str(time_in) + '\t' + str(time_out) + '\t' + str(sp[i]) + '\n')
    f.close()
     
    if verbose: 
        print 'Spectral cover values printed in the file: ', file_out 
    
    
    # Compute the minimum
    if minimum:    
        if verbose:     
           print 'Compute the spectral cover minimum...'
        
    
        n_min_length=int(np.floor(s_minimum*sr_sp))
        
      
        min_sp=np.array([np.min(sp[i:i+n_min_length]) for i in range(0,len(sp)-n_min_length)])  
        f=open(minimum_file_out,'w')
        

        sr_file_min=len(min_sp)/float(duration)
        
        for i in range(len(min_sp)):
            time_in=i/ float(sr_file_min)
            time_out= (i+1)/ float(sr_file_min)
            f.write(str(time_in) + '\t' + str(time_out) + '\t' + str(min_sp[i]) + '\n')
        f.close()

        if verbose: 
            print 'Spectral cover minimum values printed in the file: ', minimum_file_out
