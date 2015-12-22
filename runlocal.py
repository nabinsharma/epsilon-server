import argparse
import json
import os
import logging

DEJAVU_CONFIG_FILE = 'dejavu.cnf'


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    # It's bad and there might be better solution. I just wanted to NOT
    # run __init__ stuff while running this script.
    from dejavu.dejavu_main import Dejavu
    import dejavu.database as database
    from dejavu.recognize import MicrophoneRecognizer, FileRecognizer

    db_cls = database.get_database()
    with open(DEJAVU_CONFIG_FILE) as f:
        db_config_dict = json.load(f)
    db = db_cls(**db_config_dict.get("database", {}))

    # Create a Dejavu instance.
    djv = Dejavu(db)

    if args.subparser_name == 'f':
        print("Fingerprinting %s songs in %s directory" %
              (args.ext, args.dir))
        djv.fingerprint_directory(args.dir, args.ext)
    elif args.subparser_name == 'r':
        song = None
        if args.src.lower() == "mic":
            # Recognize using mic
            song = djv.recognize(MicrophoneRecognizer, seconds=5)
            print "We recognized: %s \n" % song
        else:
            file = args.src
            if not os.path.isfile(file):
                raise IOError, "File %s does not exist" % file
            # Recognize audio from a file
            song = djv.recognize(FileRecognizer, file)
        print "We recognized: %s\n" % song['song_name']
    else:
        raise ValueError, "Invalid subparser. See help"


if __name__ == '__main__':
    parser = argparse.ArgumentParser( 
        description = "Developer usage of Dejavu for Epsilon",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(dest='subparser_name',
                                       help="fingerprint or recognize")
    
    parser_f = subparsers.add_parser("f", help="Fingerprint songs")
    parser_f.add_argument('--dir', help="Directory of songs")
    parser_f.add_argument('--ext', nargs='+',
                          help="File extension of songs (audio files)")

    parser_r = subparsers.add_parser('r', help="Recognize a song")
    parser_r.add_argument('--src', help="Audio source - mic or path to a audio file")

    parser.add_argument(
        "-v",
        "--verbose",
        "--fingerprint",
        default=None,
        help="Fingerprint a directory of audio files.")
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
