#!/usr/bin/env python

import subprocess as sp
import argparse


class Lecture:
    def __init__(self, titles: list, background, sequence: list):
        self.titles = titles
        self.background = background
        self.sequence = sequence




class Editor:
    def __init__(self, ffmpeg):
        self.ffmpeg = ffmpeg
        self.commands = [[self.ffmpeg, '-h']]

    def editor_info(self):
        print("## Editor information ##")
        print("Binary: ", self.ffmpeg)

    def create_background_video(self, background, length):
        background_video_command = [self.ffmpeg, '-loop', '1',
                                    '-i', background,
                                    '-c:v', 'libx264',
                                    '-t', str(length),
                                    '-pix_fmt', 'yuvj444p',
                                    'background.mp4']
        return background_video_command

    #def create_intro_filter(self):


    # def create_video_sequence(self):
    #
    # def setup_commands(self):


    def run(self):
        for cmd in self.commands:
            sp.call(cmd)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Create lecture with ffmpeg.')
    args = parser.parse_args()


def main():
    parse_arguments()
    video_editor = Editor('ffmpeg')
    video_editor.editor_info()
    video_editor.create_background_video('/home/john/Workspace/fflecture/resources/stats-background.jpg', 30)

if __name__ == "__main__":
    main()
