 #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Skywalker Run-Archiving Script

Script that saves a copy of the inputted template file in a run directory which
is indexed by date and time saved. 
"""
############
# Standard #
############
import time
import shutil
import logging
import argparse
from pathlib import Path
from logging.handlers import RotatingFileHandler

def get_logger(name, stream_level=logging.warn, log_file=True, 
               log_dir=Path("."), max_bytes=1024*1024):
    """
    Returns a properly configured logger that has a stream handler and a file
    handler.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # One format to display the user and another for debugging
    format_stream = "%(levelname)-2s: %(message)4s"
    format_debug = "%(asctime)s:%(filename)s:%(lineno)4s - " \
      "%(funcName)s():    %(levelname)-8s %(message)4s"
    # Prevent logging from propagating to the root logger
    logger.propagate = 0

    # Setup the stream logger
    console = logging.StreamHandler()
    console.setLevel(stream_level)
    # Print log messages nicely if we arent in debug mode
    if stream_level >= logging.INFO:
        stream_formatter = logging.Formatter(format_stream)
    else:
        stream_formatter = logging.Formatter(format_debug)
    console.setFormatter(stream_formatter)
    logger.addHandler(console)
    
    if log_file:
        log_file = log_dir / "log.txt"
        # Create the file if it doesnt already exist
        if not log_file.exists():
            log_file.touch()
        # Setup the file handler
        file_handler = RotatingFileHandler(
            str(log_file), mode='a', maxBytes=max_bytes, backupCount=2,
            encoding=None, delay=0)
        file_formatter = logging.Formatter(format_debug)
        file_handler.setFormatter(file_formatter)
        # Always save everything
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    return logger

def check_args(args):
    """
    Checks to make sure the inputted arguments are valid.
    """
    # # Check the various paths and files exist
    # Template file
    if not args.template.exists():
        err_str = "Inputted template file '{0}' does not exist!.".format(
            str(args.template))
        logger.error(err_str)
        raise FileNotFoundError(err_str)
    
    # Save directory
    if str(args.save_path) != "":
        if not args.save_path.exists():
            logger.info("Path to save location does not exist. Creating "
                        "directories.")
            args.save_path.mkdir(parents=True)
            
    # Log dir
    if not args.log_dir.exists():
        args.log_dir.mkdir(parents=True)
    return args

def setup_parser_and_logging(description=""):
    """
    Sets up the parser, by adding the arguments, parsing the inputs and then
    returning the args and parser.
    """
    # Setup the parser
    if not description:
        description = __doc__
    parser = argparse.ArgumentParser(description=description)

    # Add all the arguments
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Run in debug mode.",)        
    parser.add_argument("--log_dir", metavar="P", type=str,  
                        default=str(Path.cwd() / "logs"), action="store",
                        help="Path to save the logs in.")
    parser.add_argument("-t", "--template", metavar="P", type=str,
                        default=str(Path.cwd() / "run_skywalker_template.ipynb"),
                        action="store", help="Template file path to be copied.")
    parser.add_argument("-s", "--save_path", metavar="P", type=str,
                        default="", action="store",
                        help="Save path for copied file.")
    
    # Parse the inputted arguments
    args = parser.parse_args()

    # Convert path strs to Path objects
    args.log_dir = Path(args.log_dir)
    args.save_path = Path(args.save_path)
    args.template = Path(args.template)
    
    # Perform any argument checks
    args = check_args(args)

    # Set the amount of logging
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
        
    # Get the logger
    logger = get_logger(__name__, stream_level=log_level, 
                        log_dir=args.log_dir)
    logger.debug("Logging level set to {0}.".format(log_level))

    return args, logger

def archive(template, save_path):
    """
    Create a copy of the template folder and then save it in the save location.
    By default it will create the files in a directory named after the the date
    it was saved, with a name that includes the date and the time.

    Parameters
    ----------
    template : Path
    	Path object of the template file that will be copied

    save_path : Path
    	Path object of the target path. If it is '.', the path will be
    	substituted with a dir with runs + date / template_name + date
    	+ time + .ext.
    """
    # Make a copy using the save path if it was provided
    if str(save_path) != ".":
        shutil.copy(str(template), str(save_path))

    # Interpolate save file and dir based on the template name
    else:
        # Get the current date and time
        date_current = time.strftime("%Y_%m_%d")
        time_current = time.strftime("%H_%M_%S")

        # Directory path
        save_dir = Path("runs_{0}".format(date_current))
        # Create it if it doesnt exist
        if not save_dir.exists():
            save_dir.mkdir(parents=True)

        # Get the template stem
        template_stem = template.stem
        # Add the date and time, replacing 'template' if it exists
        template_name = template_stem.replace("template", "")
        if template_name[-1] != "_":
            template_name += "_"
        template_name += date_current + "_" + time_current + template.suffix
        # Create the save path
        save_path = save_dir / template_name

        # Perform the copy
        ret_path = shutil.copy(str(template), str(save_path))
        if ret_path == str(save_path):
            logger.info("Created copy '{0}'".format(str(save_path)))
        else:
            logger.error("Copy returned path '{0}' for save path '{1}'".format(
                ret_path, str(save_path)))
        
if __name__ == "__main__":
    # Parse arguments
    args, logger = setup_parser_and_logging()
    # Run the script
    archive(args.template, args.save_path)
