#!/usr/bin/env python
## category Conversion
## desc Convert BAM reads to FASTA sequences
'''
Convert BAM reads to FASTA sequences
'''
import sys
import os
from support.eta import ETA
import pysam


def bam_tofasta(sam_fname, colorspace=False, only_mapped=False, only_unmapped=False):
    if only_mapped == False and only_unmapped == False:
        return
    if sam_fname[-4:].lower() == '.bam':
        samfile = pysam.Samfile(sam_fname, 'rb')
    else:
        samfile = pysam.Samfile(sam_fname, 'r')

    eta = ETA(0, bamfile=samfile)

    for read in samfile:
        eta.print_status(extra=read.qname, bam_pos=(read.rname, read.pos))
        if only_mapped and read.is_unmapped:
            continue
        if only_unmapped and not read.is_unmapped:
            continue

        if colorspace:
            seq = read.opt('CS')
        else:
            seq = read.seq

        sys.stdout.write('>%s\n%s\n' % (read.qname, seq))

    eta.done()
    samfile.close()


def usage():
    print __doc__
    print """\
Usage: bamutils tofasta [-cs] {-mapped} {-unmapped} file.bam

Outputs the sequences of all mapped reads to FASTA format.
"""
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()

    cs = False
    samf = None
    mapped = False
    unmapped = False

    for arg in sys.argv[1:]:
        if arg == '-cs':
            cs = True
        elif arg == '-unmapped':
            unmapped = True
        elif arg == '-mapped':
            mapped = True
        elif os.path.exists(arg):
            samf = arg

    if not samf:
        usage()

    if not unmapped and not mapped:
        mapped = True
        unmapped = True

    bam_tofasta(samf, cs, mapped, unmapped)
