#!/usr/bin/env python3
import os
# import xml.etree.ElementTree as ET
from lxml import etree as ET
import sys
import re

re_tape = re.compile(r'tape(\d+)')
re_video = re.compile(r'(tape\d+-(\d+)).avi$')
re_srt = re.compile(r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})')


def input_multiline(txt):
    print(txt)
    lines = []
    while True:
        line = input()
        if line == '':
            break
        lines.append(line)
    return '\n'.join(lines)


def move_srt(video: str):
    srt = video.rsplit('.', 1)[0] + '.srt'
    if os.path.exists(srt):
        return
    os.rename(srt + '0', srt)
    os.remove(srt + '1')


def get_recording_date(video: str):
    srt = video.rsplit('.', 1)[0] + '.srt'
    with open(srt) as f:
        for line in f:
            match = re_srt.search(line)
            if match:
                return match


basefolder = sys.argv[-1]
folders = [os.path.join(basefolder, dir)
           for dir in os.listdir(basefolder)
           if os.path.isdir(os.path.join(basefolder, dir)) and re_tape.search(dir)]

for folder in folders:
    tmatch = re_tape.search(folder)
    tapenum = tmatch.group(1)

    videos = [os.path.join(folder, file) for file in os.listdir(folder)
              if re_video.search(file)]

    tape_description = input_multiline('Enter multi-line description for tape "{}"'.format(tapenum))
    for video in videos:
        vmatch = re_video.search(video)
        videoname = vmatch.group(1)
        videonum = vmatch.group(2)

        move_srt(video)
        recording_date = get_recording_date(video)

        videoinfo = ET.Element('episodedetails')
        ET.SubElement(videoinfo, 'title').text=os.path.basename(video).rsplit('.', 1)[0]
        ET.SubElement(videoinfo, 'showtitle').text='dv'
        ET.SubElement(videoinfo, 'plot').text=recording_date.group(0) + '\n' + tape_description
        ET.SubElement(videoinfo, 'aired').text=recording_date.group(1)
        ET.SubElement(videoinfo, 'dateadded').text=recording_date.group(0) + ':00'
        ET.SubElement(videoinfo, 'year').text=recording_date.group(0).split('-')[0]

        ET.SubElement(videoinfo, 'path').text=video
        ET.SubElement(videoinfo, 'filenameandpath').text=os.path.abspath(video)
        ET.SubElement(videoinfo, 'basepath').text=os.path.split(os.path.abspath(video))[0]

        ET.SubElement(videoinfo, 'season').text=tapenum
        ET.SubElement(videoinfo, 'episode').text=str(int(videonum))
        with open(video.split('.')[0] + '.nfo', 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
            f.write(ET.tostring(videoinfo, pretty_print=True).decode())
