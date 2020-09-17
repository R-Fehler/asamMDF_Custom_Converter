from pathlib import Path
from asammdf import MDF
import sys, os

def main():
    # set variables
    mdf_extension=".MF4"
    input_folder="input"
    output_folder="output"



    # Set paths
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        path = Path(sys._MEIPASS).parent.absolute()
    else:
        path = Path(__file__).parent.parent.absolute()
    print("Path is:", path)
    path_in = Path(path, input_folder)
    path_out = Path(path, output_folder)
    os.mkdir(path_out)
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
        filename=Path(path_out, "dbc_converted_mf"),
        time_as_date=True,
        time_from_zero=False,
        single_time_base=True,
        raster=0.5,
    )
    print("DBC Converting finished and exported to .mat file")

if __name__ == "__main__":
    main()