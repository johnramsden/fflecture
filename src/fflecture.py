#!/usr/bin/env python

import subprocess as sp
import argparse


class Lecture:
    def __init__(self, titles: list, background, sequence: list):
        self.__titles = titles
        self.__background = background
        self.__sequence = sequence



class Editor:
    commands = [[__FFMPEG_BIN, '-h']]

    def set_ffmpeg_bin(self, ffmpeg_bin=None):
        # Default to linux binary
        if ffmpeg_bin is None:
            self.__FFMPEG_BIN = "ffmpeg"
        else:
            self.__FFMPEG_BIN = ffmpeg_bin

    def editor_info(self):
        print("## Editor information ##")
        print("Binary: ", self.__FFMPEG_BIN)

    def create_intro(self):

    def create_video_sequence(self):

    def setup_commands(self):


    def run(self):
        for cmd in self.commands:
            sp.call(cmd)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Create lecture with ffmpeg.')
    args = parser.parse_args()


def main():
    parse_arguments()
    video_editor = Editor()
    video_editor.editor_info()
    video_editor.run()

if __name__ == "__main__":
    main()
