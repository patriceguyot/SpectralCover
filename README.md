# SpectralCover

This python code intend to illustrate a scientific paper: 

\[1\] Guyot, P., Pinquier, J., & André-Obrecht, R. (2012, June). *Water flow detection from a wearable device with a new feature, the spectral cover*. In Content-Based Multimedia Indexing (CBMI), 2012 10th International Workshop on (pp. 1-6). IEEE. 

This code shows a version of a tool in development. 
It uses a audio low-level feature, the spectral cover, to detect water flow sounds in audio recordings of daily activities. This feature can also be used to detect vacuum cleaner sounds.

It can either output:
 * a text file containing the values of the spectral cover,
 * a text file containing the values of the minimum of the spectral cover.


From this outputs, simple thresholds can be used to segment the audio files in different classes: water, vacuum cleaner, other sounds.


 

## Prerequisites

This code is based on python (tested with python 2.7.12).

The following python package is required:

 * [Numpy](http://www.numpy.org/)

Other required packages are normally included in python: 
 * [wave](https://docs.python.org/2/library/wave.html) (to read audio)
 * array
 * optparse
 
## Usage

The following command provides some help on the usage of the code: 

$python computeSC.py -h

The following command run the code with same parameters than in the article \[1\]:

$python computeSC.py 10-10-06.wav -o sc.out -w 1024 -s 512 -m -d 2 -f min.out -g 1.5 -v


## Licence

GPL V 3 - see [LICENSE.txt](https://github.com/patriceguyot/SpectralCover/blob/master/LICENSE.txt) for more info


## Authors

Patrice Guyot
    
Questions, comments and remarks (by emails) would be appreciated.   
    
Credits: If you use this code, please cite the paper \[1\].
