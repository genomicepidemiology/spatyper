spaTyper documentation
=============

The spaTyper service predicts the _Staphylococcus aureus_ spa type from genome sequences.

## Installation

Setting up spaTyper
```bash
# Go to wanted location for spatyper
cd /path/to/some/dir

# Clone the latest version and enter the spatyper directory
git clone https://git@bitbucket.org/genomicepidemiology/spatyper.git
cd spatyper

```

Download the spaTyper database

```bash
# Go to the directory where you want to store the spaTyperr database
cd /path/to/some/dir
# Clone database from git repository
git clone https://bitbucket.org/genomicepidemiology/spatyper_db.git
```
### Dependencies:

#### Python modules: CGECore
To install the needed python modules you can use pip. 
```bash
pip3 install cgecore
```
For more information visit the respective website:
```url
https://bitbucket.org/genomicepidemiology/cge_core_module
```

#### Gawk
To install gawk with Linux/Unix Homebrew can be used.
```bash
brew install gawk
```
For Windows users please see:
```url
http://gnuwin32.sourceforge.net/packages/gawk.htm
```

#### BLAST
spaTyper requires blastn. 
Note, if you don't want to specify the path of blastn every time you run
spaTyper, make sure that blastn is in you PATH.

Blastn can be obtained from:
```url
ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
```

## Usage

You can run spaTyper command line using python3.

```bash

# Example of running spaTyper
python3 spatyper.py -i /path/to/isolate.fa.gz -db /path/to/spatyper_db/ -o /path/to/outdir

# The program can be invoked with the -h option
usage: spatyper.py [-h] [-i INPUTFILE] [-db DATABASES] [-o OUTDIR] [-b BLASTPATH] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        FASTA files are accepted. Can be whole genome or contigs.
  -db DATABASES, --databases DATABASES
                        Path to the directory containing the database with the spa sequences.
  -o OUTDIR, --outdir OUTDIR
                        Output directory.
  -b BLASTPATH, --blastPath BLASTPATH
                        Path to blastn
  -no_tmp {T,F}, --remove_tmp {T,F}
                        Remove temporary files after run. Default=True.
  -v, --version         show program's version number and exit
```

## Web-server
A webserver implementing the method is available at the [link](http://www.genomicepidemiology.org/ "CGE website") and can be found here: <https://cge.cbs.dtu.dk/services/spatyper/>

## Citation
When using the method and spaTyper database please cite:

Comparing whole-genome sequencing with Sanger sequencing for spa typing of methicillin-resistant Staphylococcus aureus.
Bartels MD, Petersen A, Worning P, Nielsen JB, Larner-Svensson H, Johansen HK, Andersen LP, Jarløv JO, Boye K, Larsen AR, Westh H.
J. Clin. Microbiol. 2014. 52(12): 4305-8.
PMID: [link](https://pubmed.ncbi.nlm.nih.gov/25297335/ "25297335")

Typing of methicillin-resistant Staphylococcus aureus in a university hospital setting using a novel software for spa-repeat determination and database management.
Harmsen D., Claus H., Witte W., Rothgänger J., Claus H., Turnwald D., & Vogel U.
J. Clin. Microbiol. 2003. 41: 5442-5448.
PMID: [link](https://pubmed.ncbi.nlm.nih.gov/14662923/ "14662923")

Please also add the following acknowledgement: 
_"This publication made use of the spa typing website (http://www.spaserver.ridom.de/) that is developed by Ridom GmbH and curated by SeqNet.org (http://www.SeqNet.org/)."_

## References

1. Camacho C, Coulouris G, Avagyan V, Ma N, Papadopoulos J, Bealer K, Madden TL. BLAST+: architecture and applications. BMC Bioinformatics 2009; 10:421. 

License
=======

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.