#!/usr/bin/env python

import subprocess as sp
import argparse


class Lecture:
    def __init__(self, lecture_title, class_title,
                 background, sequence: list, intro_length: int):
        self.lecture_title = lecture_title
        self.class_title = class_title
        self.background = background
        self.sequence = sequence
        self.intro_length = intro_length

    def describe_lecture(self):
        print(self.class_title, " ", self.lecture_title)
        print("Using intro background ", self.background,
              " for ", self.intro_length, "seconds.")
        print("Video sequence: ", *self.sequence)


class Editor:
    def __init__(self, ffmpeg):
        self.ffmpeg = ffmpeg
        self.commands = [[self.ffmpeg, '-h']]

    def editor_info(self):
        print("## Editor information ##")
        print("Binary: ", self.ffmpeg)

    # Returns ffmpeg command in list to create video from image
    def create_background_video(self, background, length):
        return  ['-loop', '1',
                 '-i', background,
                 '-c:v', 'libx264',
                 '-t', str(length),
                 '-pix_fmt', 'yuvj444p',
                 'background.mp4']

    def create_intro_filter(self):

    # ffmpeg -loop 1 -i stats-background.jpg -i MATH220-E01-part1.MTS -i MATH220-E01-part2.MTS -filter_complex "[0:v:0]duration=10[begin];[begin]drawtext=enable='between(t,1,5)':fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf:text='MATH220'[halfintro];drawtext=enable='between(t,6,10)':fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf:text='Lecture 01'[intro];[intro][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[v][a]" -map "[v]" -map "[a]" o.mp4


    # FFMPEG Command:
    # ffmpeg -i MATH220-E01-part1.MTS -i MATH220-E01-part2.MTS -filter_complex
    # "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]"
    # -map "[v]" -map "[a]" o.mp4
    def video_filter(self, number_video):
        return '"[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n={}:v=1:a=1 [v] [a]"'.format(number_video)

    # def setup_commands(self):


    def run(self):
        for cmd in self.commands:
            sp.call(cmd)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Create lecture with ffmpeg.')
    parser.add_argument('-b', '--binary',
                        help='Specify ffmpeg binary, default is ffmpeg')
    parser.add_argument('-v', '--video', action='append',
                        help='Add one or more video.')
    parser.add_argument('-c', '--coursetitle', default='Course',
                        help='Add course title.')
    parser.add_argument('-t', '--lecturetitle', default='Lecture 00',
                        help='Add lecture title.')
    parser.add_argument('-p', '--picture',
                        help='Specify picture to use as background')
    parser.add_argument('-l', '--titlelength',
                        help='Set length of each title', default=5)
    parser.add_argument('-f', '--font',
                        help=("Specify font for introduction titles,"
                              "e.g. /usr/share/fonts/TTF/AnonymousPro-Bold.ttf"))
    parser.add_argument('-n', help="Run in test mode, will not output anything.")
    return parser.parse_args()

def main():
    # Get commandline input
    arguments = parse_arguments()

    # Create Lecture
    lecture = Lecture(arguments.lecturetitle, arguments.coursetitle,
                      arguments.picture, arguments.video, arguments.titlelength)
    lecture.describe_lecture()

    # Create video editor
    video_editor = Editor('ffmpeg')


    # background_cmd = [video_editor.ffmpeg] + video_editor.create_background_video(
    #     '/home/john/Workspace/fflecture/resources/stats-background.jpg', 30)
    # video_editor.commands.append(background_cmd)
    #video_editor.run()

if __name__ == "__main__":
    main()
