#!/usr/bin/env python
"""Create 3-Layers BEM model from Flash MRI images

This program assumes that both Freesurfer/FSL, and MNE, including MNE's
Matlab Toolbox, are installed properly.

This function extracts the BEM surfaces (outer skull, inner skull, and
outer skin) from multiecho FLASH MRI data with spin angles of 5 and 30
degrees. The multiecho FLASH data are inputted in DICOM format.
This function assumes that the Freesurfer segmentation of the subject
has been completed. In particular, the T1.mgz and brain.mgz MRI volumes
should be, as usual, in the subject's mri directory.

Before running this script do the following:
(unless the --noconvert option is specified)

    1. Copy all of your FLASH images in a single directory <source> and
       create a directory <dest> to hold the output of mne_organize_dicom
    2. cd to <dest> and run
       $ mne_organize_dicom <source>
       to create an appropriate directory structure
    3. Create symbolic links to make flash05 and flash30 point to the
       appropriate series:
       $ ln -s <FLASH 5 series dir> flash05
       $ ln -s <FLASH 30 series dir> flash30
    4. cd to the directory where flash05 and flash30 links are
    5. Set SUBJECTS_DIR and SUBJECT environment variables appropriately
    6. Run this script

Example usage:

$ mne flash_bem --subject sample

"""
from __future__ import print_function

# Authors: Lorenzo De Santis

from mne.bem import make_flash_bem


def run():
    from mne.commands.utils import get_optparser

    parser = get_optparser(__file__)

    parser.add_option("-s", "--subject", dest="subject",
                      help="Subject name", default=None)
    parser.add_option("-d", "--subjects-dir", dest="subjects_dir",
                      help="Subjects directory", default=None)
    parser.add_option("-3", "--noflash30", dest="noflash30",
                      action="store_true", default=False,
                      help=("Skip the 30-degree flip angle data"),)
    parser.add_option("-n", "--noconvert", dest="noconvert",
                      action="store_true", default=False,
                      help=("Assume that the Flash MRI images have already "
                            "been converted to mgz files"))
    parser.add_option("-u", "--unwarp", dest="unwarp",
                      action="store_true", default=False,
                      help=("Run grad_unwarp with -unwarp <type> option on "
                            "each of the converted data sets"))
    parser.add_option("-v", "--view", dest="show", action="store_true",
                      help="Show BEM model in 3D for visual inspection",
                      default=False)

    options, args = parser.parse_args()

    if options.subject is None:
        parser.print_help()
        raise RuntimeError('The subject argument must be set')

    subject = options.subject
    subjects_dir = options.subjects_dir
    noflash30 = options.noflash30
    noconvert = options.noconvert
    unwarp = options.unwarp
    show = options.show

    make_flash_bem(subject=subject, subjects_dir=subjects_dir,
                   noflash30=noflash30, noconvert=noconvert, unwarp=unwarp,
                   show=show)

is_main = (__name__ == '__main__')
if is_main:
    run()