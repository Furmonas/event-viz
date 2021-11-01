import numpy as np
import csv
import cv2 as cv

from event_parser import event_info

class viz_events:
    def __init__(self,window_size,fill_content=136):
        self.img = np.zeros(window_size, dtype=np.uint8)
        self.img.fill(fill_content)

    def start(self,raw_event_file_name):
        with open(raw_event_file_name, 'r') as file:
            print('Starting visualize process, press q to exit')
            csvreader = csv.reader(file)
            events = event_info()
            header = events.get_next_line(csvreader)
            events.check_header(header)
            print('Header content:')
            print(events.event_header)
            events.get_next_line(csvreader)
            while True:
                read_ok = events.get_event_chunk(csvreader, self.img)
                if read_ok != 0:
                    cv.imshow('Single Channel Window', self.img)
                    self.img.fill(136)
                    if (cv.waitKey(1) & 0xFF == ord('q')):
                        break
                else:
                    print('End of read!')
                    break
        cv.destroyAllWindows()
