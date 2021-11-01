import os
import getopt
import sys
import csv
import PySimpleGUI as sg
import cv2 as cv
import numpy as np
import argparse

valueInSeparator = 0

class event_info:
    def __init__(self):
        self.event_header = []
        self.timestamp = 0
        self.x = 0
        self.y = 0
        self.polarity = 0
    
    def check_header(self, csv_header):
        if (csv_header[0] == "timestamp" and
            csv_header[1] == "x" and
            csv_header[2] == "y" and
            csv_header[3] == "polarity"):
            self.event_header = csv_header
        else:
            print('Header is corrupted')

    def get_next_line(self, csv):
        try:
            temp_csv = next(csv)
        except StopIteration:
            return 0
        self.timestamp = temp_csv[0]
        self.x = temp_csv[1]
        self.y = temp_csv[2]
        self.polarity = temp_csv[3]
        return temp_csv

    def get_event_chunk (self, csv, img):
        read_ok = 0
        value = 0
        first_ts = 0
        curr_ts = 0
        while True:
            new_event = self.get_next_line(csv)
            if new_event != 0:
                curr_ts = int(self.timestamp)
                if first_ts == 0:
                    first_ts = int(self.timestamp)
                if (curr_ts - first_ts) < 2000:
                    if int(self.polarity) == 1:
                        value = 255
                    else:
                        value = 0
                    self.fix_screen_res(img)
                    self.fix_pixel_pol(img,value)
                    read_ok = 1
                else:
                    break
            else:
                break
        return read_ok

    def fix_screen_res (self, img):
        if img.shape != (320,240):
            self.x = (int(self.x) / 320) * img.shape[0]
            self.y = (int(self.y) / 240) * img.shape[1]

    def fix_pixel_pol (self, img, value):
        if (int(self.x) < img.shape[0]-2):
            img[int(self.x)+1,int(self.y)] = value
        if int(self.y) > 0:
            img[int(self.x),int(self.y)-1] = value
        img[int(self.x),int(self.y)] = value
        if (int(self.y) < img.shape[1]-2):
            img[int(self.x),int(self.y)+1] = value
        if int(self.x) > 0:
            img[int(self.x)-1,int(self.y)] = value


def PrepareArguments():
    parser = argparse.ArgumentParser(description='Event Camera Raw File Visualizer')
    parser.add_argument('-i', '--input_file', required=True, type=str,
                        help='Define CSV INPUT_FILE, where raw event data is to be found')
    parser.add_argument('-s', '--window_size', default='320x240', type=str,
                        help='Define WINDOW_SIZE of output window')
    return parser

def main():
    parser = PrepareArguments()
    args = parser.parse_args()
    fileName = args.input_file
    size = tuple(map(int, args.window_size.split('x')))
    print('Input file -', fileName)
    print('Image size -', size)
    return fileName, size

if __name__ == "__main__":
    fileName, size = main()
    FullFileName = os.path.join(sys.path[0], fileName)

    img = np.zeros(size,dtype=np.uint8)
    img.fill(136)
    next_read = []
    read_ok = 0

    if os.path.isfile(FullFileName):
        with open(FullFileName, 'r') as file:
            print('Starting visualize process, press q to exit')
            csvreader = csv.reader(file)
            events = event_info()
            header = events.get_next_line(csvreader)
            events.check_header(header)
            print('Header content:')
            print(events.event_header)
            next_read = events.get_next_line(csvreader)
            # vid_out = cv.VideoWriter('video.avi', cv.VideoWriter_fourcc('M','J','P','G'), 15, size)
            while True:
                read_ok = events.get_event_chunk(csvreader, img)
                if read_ok != 0:
                    # vid_out.write(img)
                    cv.imshow('Single Channel Window', img)
                    img.fill(136)
                    if (cv.waitKey(1) & 0xFF == ord('q')):
                        break
                else:
                    print('End of read!')
                    break
    else:
        print('File does not exist -', FullFileName)

    cv.destroyAllWindows()