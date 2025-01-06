###############################################################################
# Copyright 2024 Tim Stephenson and contributors
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License.  You may obtain a copy
#  of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under
#  the License.
#
# Command line client for managing an image library.
#
###############################################################################
import logging
from hmac import compare_digest
import os
import shutil

from PIL import Image

from imagectl.__main__ import get_hash
from imagectl.api import ImageCommand, ImageCommandOptions

VERBOSE = False
# Set list of valid file extensions
valid_extensions = [".JPG", ".jpg", ".jpeg", ".png"]
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class OrganiserCommand(ImageCommand):
    """Command to organise an image library"""
    NAME = 'organise'
    def __init__(self, subparsers):
        super().__init__(self)
        self.cmd = subparsers.add_parser(self.NAME,
                   help='organise images in a standard structure')
        self.cmd.add_argument("-i", "--input", help="base image directory")
        self.cmd.add_argument("-o", "--output", help="output directory")
        self.cmd.add_argument("-m", "--move", action="store_true", help="move the file (default is to copy)")
        self.cmd.add_argument("-r", "--recurse", action="store_true", help="process child directories as well")
        self.cmd.add_argument("-v", "--verbose", action="store_true", help="increase the progess messages")

    def execute(self, options: ImageCommandOptions):
        # print(f'command {self.NAME} not yet implemented')
        in_dir = options.input
        out_dir = options.output
        move = options.move
        print('processing dir: ' + in_dir)

        # list files in dir
        file_names = os.listdir(in_dir)

        # for each file
        for file_name in file_names:
            if (VERBOSE):
                print('  processing: ' + file_name)

            # get file extension
            file_ext = os.path.splitext(file_name)[1]

            # process image / dir / other
            if (file_ext in valid_extensions):
                self.process_image(os.path.join(in_dir, file_name), out_dir, move=move)
            elif (os.path.isdir(os.path.join(in_dir, file_name))):
                self.process_dir(os.path.join(in_dir, file_name))
            else:
                if (VERBOSE):
                    print('    skipping unsupported extension: ' + file_ext)
                continue

    @staticmethod
    def get_new_file_name(in_file: str, year: str, month: str, day: str) -> str:
        """returns the new date prefixed file name"""
        file_base = os.path.basename(os.path.splitext(in_file)[0])
        file_ext = os.path.splitext(in_file)[1]
        if file_base.startswith(f"{year}-{month}-{day}"):
            return f"{file_base}{file_ext.lower()}"
        else:
            return f"{year}-{month}-{day}-{file_base}{file_ext.lower()}"

    @staticmethod
    def is_writable(in_file, out_file):
        """returns true if out_file does not exist or has the same hash"""
        if not os.path.exists(out_file):
            return True
        else:
            in_hash = get_hash(in_file)
            out_hash = get_hash(out_file)
            return compare_digest(in_hash.strip(), out_hash.strip())

    def process_image(self, in_file: str, out_dir: str, move: bool = False):
        print('    process image: ' + in_file)
        old_file_path = in_file

        # open the image
        if (VERBOSE):
            print('    opening: ' + old_file_path)
        try:
            image = Image.open(old_file_path)
        except:
            if (VERBOSE):
                print('    cannot open ' + in_file)
            return

        # get EXIF metadata
        if (image._getexif() == None):
            if (VERBOSE):
                print('    skipping ' + in_file + ' because no EXIF data available')
            return

        # get date taken from metadata
        try:
            print(image._getexif()[36867])
            date_taken = image._getexif()[36867]
        except:
            if (VERBOSE):
                print('    skipping ' + in_file + ' because no EXIF data available')
            return

        # close the image
        image.close()

        # extract parts of date and format
        year = date_taken[0:4]
        month = date_taken[5:7]
        day = date_taken[8:10]
        date_time = date_taken \
            .replace(":", "-") \
            .replace(" ", "-")

        out_file = self.get_new_file_name(in_file, year, month, day)

        # make target dir
        if not (os.path.exists(out_dir)):
            os.mkdir(out_dir)
        trgt_path = os.path.join(out_dir, year)
        if not (os.path.exists(trgt_path)):
            os.mkdir(trgt_path)
        trgt_path = os.path.join(trgt_path, month)
        if not (os.path.exists(trgt_path)):
            os.mkdir(trgt_path)

        # create the new dir path
        new_file_path = os.path.join(trgt_path, out_file)

        if self.is_writable(in_file, out_file):
            # copy / move the file
            if (move):
                if (VERBOSE):
                    print('    moving from ' + old_file_path + ' to ' + new_file_path)
                shutil.move(old_file_path, new_file_path)
            else:
                if (VERBOSE):
                    print('    copying from ' + old_file_path + ' to ' + new_file_path)
                shutil.copy2(old_file_path, new_file_path)
