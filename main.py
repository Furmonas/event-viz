# public inputs
import os
import sys
import cv2 as cv
import numpy as np
import pandas as pd

# personal inputs
from option_parser import PrepareArguments
from event_parser import event_info

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
            header = pd.read_csv(FullFileName, index_col=False, nrows=0).columns.tolist()
            events = event_info()
            events.check_header(header)
            print('Header content: {}'.format(events.event_header))
            # next_read = events.get_next_line(csvreader)
            # while True:
            #     read_ok = events.get_event_chunk(csvreader, img)
            #     if read_ok != 0:
            #         cv.imshow('Single Channel Window', img)
            #         img.fill(136)
            #         if (cv.waitKey(1) & 0xFF == ord('q')):
            #             break
            #     else:
            #         print('End of read!')
            #         break
    else:
        print('File does not exist -', FullFileName)

    cv.destroyAllWindows()
