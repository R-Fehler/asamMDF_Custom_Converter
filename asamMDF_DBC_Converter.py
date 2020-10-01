import argparse
import sys
from pathlib import Path

from asammdf import MDF


def main():
    input_folder_default = 'input'
    output_folder_default = "output"
    filename_default = "dbc_converted_mf"
    mdf_extension = ".MF4"

    parser = argparse.ArgumentParser(description='DBC convert multiple MDF files'
                                                 ' with same structure to one large .mat file')

    parser.add_argument('--fileName', metavar='fn', type=str, default=filename_default,
                        help='name of the output .mat file, default=' + filename_default)
    parser.add_argument('--inputDir', metavar='in-dir', type=str, default=input_folder_default,
                        help='directory of your input folder containing MF4 and DBC Files,'
                             ' default=' + input_folder_default)
    parser.add_argument('--outputDir', metavar="out-dir", type=str, default=output_folder_default,
                        help='directory of your output folder,'
                             'default=' + output_folder_default)
    args = parser.parse_args()
    print(args)
    # set variables
    input_folder = args.inputDir
    output_folder = args.outputDir
    filename = args.fileName


    # Set paths
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        path = Path(sys._MEIPASS).parent.absolute()
    else:
        path = Path(__file__).parent.absolute()
    print("Path is:", path)
    path_in = Path(path, input_folder)
    path_out = Path(path, output_folder)
    Path(path_out).mkdir(exist_ok=True)
    # load MDF/DBC files from input folder

    logfiles = list(path_in.glob("*" + mdf_extension))
    dbc = list(path_in.glob("*" + ".DBC"))

    print("Log file(s): ", logfiles, "\nDBC(s): ", dbc)

    # concatenate MDF files from input folder
    mdf = MDF.concatenate(logfiles)
    print("mdf files are concatenated")

    # DBC convert the unfiltered MDF + save & export resampled data
    print("DBC Converting started")
    mdf_scaled = mdf.extract_can_logging(dbc, ignore_invalid_signals=True)
    mdf_scaled.export(
        "mat",
        filename=Path(path_out, filename),
        time_as_date=True,
        time_from_zero=False,
        single_time_base=True,
        raster=0.5,
    )
    print("DBC Converting finished and exported to .mat file")


if __name__ == "__main__":
    main()
