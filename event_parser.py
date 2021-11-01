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
            raise NameError('CSV is corrupted -> need to have [timestamp, x, y, polarity] header')

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
