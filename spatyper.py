#!/usr/bin/env python3

"""
spaTyper main script

Contributors:
K. Therkelsen

"""
version_numb = "v2.0.0"

# imports
import os, sys, shutil, subprocess, gzip
from argparse import ArgumentParser

# for help
if len(sys.argv) == 1:
    print("")
    print("spaTyper " + version_numb)
    print("")
    print("spaTyper - predicts the Staphylococcus aureus spa type from genome sequences")
    print("Spa type sequences are used as queries to blast against a database from the genome sequences")
    print("Subsequently, it matches the 5' and 3' ends of the spa type sequences that have 100% identity starting at position 1.")
    print("")
    print("")
    print("Usage: spatyper.py <options> ")
    print("Ex: spatyper.py -i /path/to/isolate.fa.gz -db /path/to/spatyper_db/ -o /path/to/outdir")
    print("")
    print("")
    print("For help, type: spatyper.py -h")
    print("")
    sys.exit(1)
    
    ##########################################################################
    # CLASSES AND FUNCTIONS                                                  #   
    ##########################################################################

class spatype():

    def __init__(self, spa_seq_file, blast_path):
        self.spa_file = spa_seq_file
        self.blast = blast_path
        
    def spa_database(self, fasta_file):
        """Builds BLAST database from genome sequences names seq_db."""
        if is_gzipped(fasta_file):
            # Unzip file
            cmd = "gzip -d " + fasta_file
            subprocess.run(cmd, shell=True)
            cmd = self.blast + "makeblastdb -in " + fasta_file.replace(".gz", "") + " -out seq_db -dbtype nucl"
        else:
            cmd = self.blast + "makeblastdb -in " + fasta_file + " -out seq_db -dbtype nucl"
        print("# Building sequence database")
        print("#")
        print("# BLAST call: " + cmd)
        print("#")
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL).wait() 
        print("BLAST call ended")
    
    def find_spatype(self):
        """
        BLAST spa sequences against genome sequences database (seq_db).
        Outputs a temporary tabular blastn_out.tab with all all spatype alignments.
        """
        cmd = self.blast + "blastn -query " + self.spa_file + " -db seq_db -out " + outdir + "/blastn_out.tab -outfmt 7 -dust no -evalue 0.0001 -num_alignments 10000"

        print("# Blasting query against sequence database")
        print("#")
        print("# BLAST call: " + cmd)
        print("#")
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL).wait()
        print("BLAST call ended")
        print("#")
        
    def filter_spatype(self):
        """
        Filter and save spatype alignments fulfilling:
        % identity == 100
        alignment length >= 20
        q. start == 1 and q. end == 1
        Outputs a temporary tab-separated file with hits.
        """
        print("# Filtering BLAST hits")
        print("#")
        with open(outdir + "/hits.tab", "w") as out:
            with open(outdir + "/blastn_out.tab", "r") as f:
                
                for line in f:
                    if line[0] == "#":
                        continue
                    line = line.split("\t")
                    if float(line[2]) < 100.000 or int(line[3]) < 20 or (int(line[6]) != 1 and int(line[7]) != 1):
                        continue
                    out.write("\t".join(line))
        
    
    def saco_convert(self, fasta_file):
        """
        Change format of genome sequences to use as input for match_spa_ends func.
        Outputs a temporary file saco.tab.
        """
        with open(outdir + "/saco.tab", "w") as out:
            with open(fasta_file) as f:
                header = f.readline()[1:-1]
                seq = ""
                for line in f:
                    if line.startswith(">"):
                        out.write(header + "\t" + seq + "\t\t\n")
                        header = line[1:-1]
                        seq = ""
                        continue
                    seq += line[:-1]
                out.write(header + "\t" + seq + "\t\t\n")

    def get_repeats(self):
        """Extract spa type repeats and store in dict"""
        spa_type_repeats = {}
        with open(db_path +'/spa_types.txt') as f:
            for l in f:
                tmp = l.split(',')
                type = tmp[0]
                spa_type_repeats[type] = tmp[1].strip()
        return spa_type_repeats

    def match_spa_ends(self):
        """
        Executes spa_type.find.gawk machting the the 5' and 3' ends of the reads.
        Returns a dict with all values for outfile with results.
        """
        cmd = "./spa_type.find.gawk {o}/hits.tab {o}/saco.tab > {o}/res.tab".format(o=outdir)
        print("# Matching spa ends")
        print("#")
        print("# Call: " + cmd)
        print("#")
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print("Call ended")
    
def is_gzipped(file_path):
    """ Returns True if file is gzipped and False otherwise.

    The result is inferred from the first two bits in the file read
    from the input path.
    On unix systems this should be: 1f 8b
    Theoretically there could be exceptions to this test but it is
    unlikely and impossible if the input files are otherwise expected
    to be encoded in utf-8.
    """
    with open(file_path, mode="rb") as fh:
        bit_start = fh.read(2)
    if(bit_start == b"\x1f\x8b"):
        return True
    else:
        return False

def file_format(input_files):
    """
    Takes all input files and checks their first character to assess
    the file format. 3 lists are return 1 list containing all fasta files
    1 containing all fastq files and 1 containing all invalid files
    """
    fasta_files = []
    fastq_files = []
    invalid_files = []
    for infile in input_files:
        # Check valid input path
        if not os.path.exists(infile):
            sys.exit("Input Error: Input file does not exist!\n")    
        # Open input file and get the first character
        try:
            f =  gzip.open(infile, "rb")
            fst_char = f.read(1)
        except OSError:
            f = open(infile, "rb")
            fst_char = f.read(1)
        f.close()
        # Return file format based in first char
        if fst_char == b"@":
            fastq_files.append(infile)
        elif fst_char == b">":
            fasta_files.append(infile)
        else:
            invalid_files.append(infile)
    return (fasta_files, fastq_files, invalid_files)


if __name__ == "__main__":
    
    ##########################################################################
    # PARSE COMMAND LINE OPTIONS                                             #
    ##########################################################################
    
    parser = ArgumentParser()
    
    parser.add_argument("-i", "--inputfile",
                        help="FASTA files are accepted. Can be whole genome or contigs.",
                        required=True,
                        default=None)
    # Optional arguments
    parser.add_argument("-db", "--databases",
                        help="Path to the directory containing the database with\
                              the spa sequences.",
                        default="spatyper_db/")
    parser.add_argument("-b", "--blastPath",
                        help="Path to blast directory",
                        default="")
    parser.add_argument("-o", "--outdir",
                        help="Output directory.",
                        default="")
    parser.add_argument("-no_tmp", "--remove_tmp",
                        help="Remove temporary files after run. Default=True.",
                        choices=["True", "False"],
                        default="True")
    parser.add_argument("-v", "--version", action="version", version=version_numb)
    args = parser.parse_args()
    
    
    ##########################################################################
    # MAIN                                                                   #   
    ##########################################################################
    
    ##### Validate arguments

    # Check if valid output directory is provided
    if args.outdir:
        outdir = os.path.abspath(args.outdir)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
    else:
       outdir = os.getcwd()

    # Check if valid blast path is provided
    if args.blastPath:
        if not os.path.isdir(args.blastPath) and args.blastPath != "":
            sys.exit("No valid path to blast directory was provided. Use the -b flag to provide the path.")
        if not os.path.join(args.blastPath, "blastn"):
            sys.exit("No valid path to blast directory was provided. Use the -b flag to provide the path.")
    elif shutil.which("blastn") is None or shutil.which("makeblastdb") is None:
        sys.exit("Blast tool does not exist. Use the -b flag to provide the path to the tools.")
    else:
        pass
    blast_path = args.blastPath
    
    # Check if valid database is provided
    if args.databases:
        db_path = os.path.abspath(args.databases)
        if not os.path.exists(args.databases):
            sys.exit("Input Error: The specified database directory does not "
                 "exist:" + db_path + "\n")  
    
    # Check existence of the spa files in database
    spa_seq_file = "%sspa_sequences.fna" % (args.databases)
    if(not os.path.isfile(spa_seq_file)):
        sys.exit("spa sequence file not found at expected location: %s"%(spa_seq_file))
    spa_types_file = "%s/spa_types.txt" % (args.databases)
    if(not os.path.isfile(spa_types_file)):
        sys.exit("spa types file not found at expected location: %s"%(spa_types_file))
    
    # Load and check input file(s)
    if args.inputfile is None:
        sys.exit("Input Error: No inputfile was provided!\n")
    inputfile_lst = args.inputfile.split(",")
    for file in inputfile_lst:
        if not os.path.exists(file):
            sys.exit("Input Error: Input file not found at expected location: %s"%(file))
    # Check file format of input files (fasta or fastq, gz or not gz)
    (fasta_files, fastq_files, invalid_files) = file_format(inputfile_lst)
    
    if len(fasta_files) == 0 or len(fastq_files) >= 1:
        sys.exit("Input file must be fasta format.")
    
    # If input is an assembly
    if len(fasta_files) == 1:
    
        # Initiate spa typing
        spa = spatype(spa_seq_file, blast_path)
        fasta = fasta_files[0]
        # Do spatyping
        spa.spa_database(fasta)
        spa.find_spatype()
        spa.filter_spatype()
        spa.saco_convert(fasta)
        spa.match_spa_ends()
        

        # Fetch the results from the spaTyper
        results = {
            'spa_type':    'unknown',
            'repeats':     '',
            'contig':      'N/A',
            'position':    '',
            'orientation': 'N/A'
            }
        # Load spa repeat db
        spa_type_repeats_dict = spa.get_repeats()
        with open(outdir +"/res.tab") as f:
            for l in f:
                if l[:5] == 'Bingo':
                    tmp = l.split('\t')
                    results['spa_type']    = tmp[1].split('_')[1].strip()
                    results['repeats'] = spa_type_repeats_dict.get(tmp[1].split('_')[1].strip())
                    results['contig']      = tmp[2].strip()
                    results['position']    = tmp[3].split(':')[1].strip()
                    results['orientation'] = tmp[4].strip()

        # Create results file
        tsv = os.path.join(outdir + "/spaType_results.tsv")
        with open(tsv, "w") as f:
            f.write("#spa Typing\n")
            f.write("#spa Type\tRepeats\tContig\tPosition\tOrientation\n")
            f.write("%s\t%s\t%s\t%s\t%s\n"%(results['spa_type'], results['repeats'],
                                            results['contig'], results['position'],
                                            results['orientation']))

        # Cleaning tmp files
        if args.remove_tmp == "True":
            cmd = "rm " + outdir + "/*.tab"
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL).wait()
            cmd = "rm seq_db.*"
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL).wait()
        print("spaTyper: Done")
