import argparse
import random
import shutil
from pathlib import Path
import ffmpeg


def main(source_dir, destination):
    """
    Find MP3s in the source directory and find enough duration to fill a 74-minute MD set to LP4

    :param source_dir: Path - directory housing MP3 files to be searched recursively
    :param destination: Path - directory to copy files to
    """
    file_list = list()
    tracks_already_included = list()
    for file in source_dir.glob('**/*.mp3'):
        file_list.append(file)

    # 74 minute disc, LP4
    available_seconds = (74 * 60 * 4)
    # tweak to try to overcome the error margin
    available_seconds *= 1.013

    while available_seconds > 30:
        # Grab a random file and remove it from the list
        current_file = file_list[random.randint(0, (len(file_list)) - 1)]

        try:
            title_artist = f"{ffmpeg.probe(current_file)['format']['tags']['title']} " \
                           f"- {ffmpeg.probe(current_file)['format']['tags']['artist']}"
        except ffmpeg.Error:
            print(f"\n{current_file} looks weird, skipping it.\n")
            continue

        if title_artist in tracks_already_included:
            print("\nTrack already included, skipping\n")
            continue
        else:
            try:
                duration = float(ffmpeg.probe(current_file)['format']['duration'])
                print(f"File: {current_file}\n"
                      f"Time remaining: {available_seconds}\n"
                      f"File duration: {duration}")

                if available_seconds > duration:
                    # copy the file to the output dir
                    available_seconds -= duration

                    randomise_filename = True
                    if randomise_filename:
                        output_filename = Path(str(destination) + f"/{str(random.randint(0, 99))} " + current_file.name)
                    else:
                        output_filename = Path(str(destination) + f"/" + current_file.name)
                    # copy the file to the output directory
                    shutil.copyfile(current_file, output_filename)

                    # add it to the list of tracks included to avoid duplicates
                    tracks_already_included.append(title_artist)
            except ffmpeg.Error:
                continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='MD Disc Randomisation Filler',
        description='''Takes a directory as input
        and copies a random selection of audio files to a directory - to fill an MD using the LP4 encoder.''')
    parser.add_argument('--input-dir')
    parser.add_argument('--output-dir')
    args = parser.parse_args()

    main(Path(args.input_dir), args.output_dir)
