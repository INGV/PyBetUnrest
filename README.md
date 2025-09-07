# PyBetUnrest

PyBetUnrest is an open and cross-platform implementation of BET_UNREST model. BET_UNREST is an extension of BET_EF including non-magmatic volcanic unrest and its relating hazardous phenomena, by adding a specific branch to the event tree ([Rouwet et al., 2014](https://appliedvolc.biomedcentral.com/articles/10.1186/s13617-014-0017-3)). It has been designed and developed as one of the final products of the EU VUELCO project and tested during the last volcanic crisis simulation organized in Dominica (West Indies) in the frame of VUELCO ([Sandri et al., 2017](https://link.springer.com/chapter/10.1007/11157_2017_9[](url))).

More details on PyBetUnrest tool can be found in [Tonini et al. (2016)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016GC006327), where the use of the tool is illustrated through an application to available knowledge and datasets of the Kawah Ijen stratovolcano, Indonesia. In particular, the tool is set on the basis of monitoring data for the learning period 2000–2010, and is then blindly applied to the test period 2010–2012, during which significant unrest phases occurred. 

An on-line running (stable but currently not in development) version of PyBetUnrest is hosted on the [VHub platform](https://vhub.org/resources/betunrest) 

## Requirements
This version of PyBetUnrest requires Python 3 and the following Python modules/libraries:
 - wxpython
 - numpy
 - matplotlib
 - pillow (formerly known as PIL)


## Installation
Download this repository by clicking the button placed on the top-right of this page, under the project title (the one with the small cloud icon with a downward arrow) and unzip the archive wherever you prefer in your local computer (referred as `/path_to_pybetunrest/` from hereafter).

Alternatively, you can make a clone of the project:
```
git clone git@github.com:INGV/PyBetUnrest.git
```

Now, in order to run the tool, you need a Python interpreter (3.x version) and the packages listed above (compatible with your Python interpreter version).
Different approaches can be adopted to satisfy these requierments, depending on the experience of the user with Python programming and on the used operating system.

NOTE: The software is developed and tested mainly on Debian-based Linux distribution, meaning that software issues due to different operating systems could be missed by developers.   


#### Using a Conda environment
A suggested (and cross-platform) way to run PyBetUnrest is to use a [Conda](https://conda.io/en/latest/) environment, in particular [Miniconda](https://conda.io/en/latest/miniconda.html). This will allow to build a specific Python environment separated from your system libraries.
Moreover, Conda is a package manager, so it will take care for you of check the correct dependencies among packages.

NOTE: Users that are working with the much more complete [Anaconda distribution](https://www.anaconda.com/), should be able to run the PyBetUnrest tool without installing Miniconda. However, it could be more comfortable to create a dedicated environment with the packages listed above. 

After having downloaded the last Miniconda (if you do not have particoular needs, the Miniconda Python3 version is suggested) for your own platform from [here](https://conda.io/en/latest/miniconda.html), install it, by accepting the licence and following the default options suggested by the installer. The installer will create a miniconda3/ folder in a given default path (hereafter, I'll refer to it with `/path_to_miniconda/`), depending on your operating system.
Linux (and OSX) users can run the following command lines to download and install last Miniconda version: 

```
wget -c http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

 - **Linux and Mac/OSX users**
The installer should add the Miniconda environment to your PATH variable. 
You can check it opening the terminal and running `echo $PATH`
If Miniconda is not in your PATH variable, you can temporary add it by running:
`export PATH="path_to_miniconda/bin:$PATH" `
or adding the previous line to the .profile or .bash_profile.

 - **Windows users**
In Windows the installer suggests to not add the PATH since they can use directly the Anaconda Prompt from the Windows menu, which load the Conda environment. 


Then you have to create the specific environment to run PyBetUnrest. To do this, open a terminal (Windows users have to do it from the Miniconda Prompt) and type:
```
conda env create -f /path_to_pybetunrest/pybet.yml
```

If this command returns an error, you can manually create the environment as follows (here python 3.8 is used, but any 3.x version considered stable should work):
```
conda create --name pybet python=3.8
conda activate pybet
conda install numpy pillow matplotlib wxpython
```

If `conda activate pybet` returns an error, try `source activate pybet`, depending on versions of conda itself.

In order to run PyBetUnrest, the user have to activate the pybet environment. When the environment is activate, the prompt displays its name between brackets:
```
(pybet) prompt: 
```
The shell will continue to work regularly but using the Python interpreter and the libraries of the activated environment. 
To deactivate it just type:
 - `conda deactivate`
or
 - `source deactivate`
or close the shell and open another one.
  
Once you have the pybet environment activated, you can run the tool:
```
(pybet) prompt: python /path_to_pybetunrest/src/betunrest.py
```

