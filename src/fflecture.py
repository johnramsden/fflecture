#!/usr/bin/env python

import subprocess as sp
import argparse
import os.path


class Lecture:
    def __init__(self, lecture_title, class_title,
                 background, video_sequence: list):
        self.lecture_title = lecture_title
        self.class_title = class_title
        self.background = background
        self.video_sequence = video_sequence

    def describe_lecture(self):
        print(self.class_title, " ", self.lecture_title)
        print("Using intro background ", self.background)
        print("Video sequence: ", *self.video_sequence)


class Editor:
    def __init__(self,
                 ffmpeg: str="ffmpeg",
                 font_file=None,
                 font_size: int=148,
                 font_color: str="white",
                 title_length: int=5,
                 title_x: str="(w-text_w)/2",
                 title_y: str="(h-text_h)/2",
                 box: int=1,
                 box_color: str="black",
                 box_opacity: int=0.5,
                 box_border_width: int=25):
        self.ffmpeg = ffmpeg
        self.commands = {'help': [self.ffmpeg, '-h']}
        self.command_sequence = []
        self.titles= {"font": {"file": font_file,
                               "size": font_size,
                               "color": font_color},
                      "length": title_length,
                      "box": {"status": box,
                              "color": box_color,
                              "opacity": box_opacity,
                              "borderw": box_border_width},
                      "coordinates": {"x": title_x,
                                      "y": title_y}}

    def editor_info(self):
        print("## Editor information ##")
        print("Binary: ", self.ffmpeg)

    def image_video_command(self, background: str, output_stream: str="temp.ts"):
        """
        ffmpeg command in list to create video from image
        :param background:
        :param output_stream:
        :return:
        """
        return {"command": [self.ffmpeg, '-loop', '1', '-i', background,
                            '-c:v', 'libx264', '-t', str(self.titles['length']),
                            '-pix_fmt', 'yuvj444p',
                            '-f', 'mpegts', output_stream],
                "stream": output_stream}

    """ A Full title:

    ffmpeg -i intermediate1.ts -filter_complex

    "drawtext=enable='between(t,1,9)':
    fontfile=/usr/share/fonts/TTF/WorkSans-Bold.ttf:
    text='STAT302': fontcolor=white: fontsize=148: box=1:
    boxcolor=black@0.5: boxborderw=25: x=(w-text_w)/2: y=(h-text_h)/2
    [firsttitle];[firsttitle]drawtext=enable='between(t,11,19)':
    fontfile=/usr/share/fonts/TTF/WorkSans-Bold.ttf:
    text='Lecture 01': fontcolor=white: fontsize=148: box=1:
    boxcolor=black@0.5: boxborderw=25: x=(w-text_w)/2: y=(h-text_h)/2"

    -codec:a copy output.mp4
    """

    def intro_titles_command(self, background: str, titles: list, output_video: str):
        """
        drawtext=enable='between(t,1,9)':
        fontfile=/usr/share/fonts/TTF/WorkSans-Bold.ttf:
        text='STAT302': fontcolor=white: fontsize=148:
        box=1: boxcolor=black@0.5: boxborderw=25: x=(w-text_w)/2: y=(h-text_h)/2 [v]
        """
        image_video = self.image_video_command(background)
        intro_titles_command = image_video['command']

        print("Added {}".format(intro_titles_command))

        # Setup filter for intro titles
        intro_titles_filter = []
        for index in range(len(titles)):
            filter_section = []
            if index == 0:
                filter_section.append("drawtext=enable='between(t,{0},{1})'"
                                           .format(str(index * self.titles['length'] + 1),
                                                   str((index + 1) * self.titles['length'] - 1)))
            else:
                filter_section.append("[firsttitle];[firsttitle]drawtext=enable='between(t,{0},{1})'"
                                           .format(str(index * self.titles['length'] + 1),
                                               str((index + 1) * self.titles['length'] - 1)))

            filter_section.extend(["fontfile={}".format(self.titles['font']['file']),
                                    "fontcolor={}".format(self.titles['font']['color']),
                                    "fontsize={}".format(str(self.titles['font']['size'])),
                                    "box={}".format(str(self.titles['box']['status'])),
                                    "boxcolor={0}@{1}".format(self.titles['box']['color'],
                                                              str(self.titles['box']['opacity'])),
                                    "boxborderw={}".format(str(self.titles['box']['borderw'])),
                                    "x={}".format(self.titles['coordinates']['x']),
                                    "y={}".format(self.titles['coordinates']['y'])])

            intro_titles_filter.append(":".join(filter_section))
        print(intro_titles_filter)

        self.commands.update({"intro": [intro_titles_command,
                                            [self.ffmpeg, '-i', image_video['stream'],
                                             '-filter_complex', "{}".format(":".join(intro_titles_filter)),
                                             '-codec:a', 'copy', output_video]
                                            ]})

    # ffmpeg -loop 1 -i stats-background.jpg -i MATH220-E01-part1.MTS -i MATH220-E01-part2.MTS -filter_complex
    # "[0:v:0]duration=10[begin];[begin]drawtext=enable='between(t,1,5)':fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf:text='MATH220'[halfintro];drawtext=enable='between(t,6,10)':fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf:text='Lecture 01'[intro];[intro][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[v][a]" -map "[v]" -map "[a]" o.mp4

    def concat_video_command(self, videos: list, concat_video: str):
        """
        Setup the ffmpeg command used to concatenate videos.
        :return:
        """
        video_command = [self.ffmpeg]
        for video in videos:
            video_command.extend(['-i', video])

        """
        Setup the filter to concatenate videos. e.g. With n=2:
        "[0:v:0] [0:a:0] [1:v:0] [1:a:0] concat=n=2:v=1:a=1 [v] [a]"
        """
        concat_filter = []
        for video in range(len(videos)):
            concat_filter.extend(["[{0}:v:0]".format(video), "[{}:a:0]".format(video)])
        concat_filter.extend(["concat=n={}:v=1:a=1".format(len(videos)), "[v]", "[a]"])

        # Add the filter items in a string, surrounded by quotes
        video_command.extend(['"{}"'.format(" ".join(concat_filter)),
                              '-map', '"[v]"', '-map', '"[a]"', concat_video])
        return video_command

    def run(self, command: str):
        if command in self.commands:
            print("running command: {}".format(command))
            for ffmpeg_commands in self.commands[command]:
                print(ffmpeg_commands)
                sp.call(ffmpeg_commands)
        else:
            print("No command {} found".format(command))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Create lecture with ffmpeg.')
    parser.add_argument('-b', '--binary',
                        help='Specify ffmpeg binary, default is "ffmpeg"')
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
                      arguments.picture, arguments.video)
    #lecture.describe_lecture()

    # Create video editor
    video_editor = Editor('ffmpeg', font_file=arguments.font, title_length=int(arguments.titlelength))
    # print(video_editor.concat_video_command(lecture.video_sequence))
    # print(video_editor.image_video_command(arguments.picture, arguments.titlelength))

    title_video = 'intro_title.mp4'

    video_editor.intro_titles_command(
            lecture.background, [lecture.class_title, lecture.lecture_title], title_video)

    #print(video_editor.commands['intro'])

    video_editor.run("intro")
    #sp.call(video_editor.image_video_command(lecture.background)["command"])


if __name__ == "__main__":
    main()