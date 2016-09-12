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

    # Returns ffmpeg command in list to create video from image
    def create_background_video(self, background, length):
        background_video_command = ['-loop', '1',
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
    parser.add_argument('-v', '--video', action='append',
                        help='Add one or more video.')
    print(parser.parse_args())

def main():
    parse_arguments()

    video_editor = Editor('ffmpeg')
    video_editor.editor_info()

    #lecture = Lecture()

    background_cmd = [video_editor.ffmpeg] + video_editor.create_background_video(
        '/home/john/Workspace/fflecture/resources/stats-background.jpg', 30)
    video_editor.commands.append(background_cmd)
    #video_editor.run()

if __name__ == "__main__":
    main()
