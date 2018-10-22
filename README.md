# dv-metadata
Copy video files from a DV (DigitalVideo) tape, and import them into Kodi.

Run the capture script to capture the video files (using dvgrab). The video files are saved as dv/tapeX/tapeX-YYY.avi, were X is the tape number (automatically incremented) and YYY is the video number on the tape.

When all tapes are copied, run the postprocessor to create the .nfo files for kodi to import the tapes as a TV show (each tape is a season, each video on a tape is an episode).
The post-processor will, for each tape, ask for a description of the tape, on multiple lines. Input an empty line to stop.
