import os, glob, datetime, operator
from optparse import OptionParser
from shutil import copyfile
from PIL import Image

# get date taken from an image and convert string to be a valid date string
def get_date_taken(path):
    date_taken = list(Image.open(path)._getexif()[36867])
    date_taken[4] = '-'
    date_taken[7] = '-'
    date_taken[10] = '-'
    return "".join(date_taken)


def main():
    diff_dir = True
    file_dict = {}
    parser = OptionParser()
    parser.add_option("-s", "--source", action="store", dest="source",
                      help="source directory of images to index", type="string", default="")
    parser.add_option("-d", "--destination", action="store", dest="destination",
                      help="destination directory for indexed images", type="string", default="")
    parser.add_option("-t", "--type", action="store", dest="type",
                      help="file extension for images to index", choices=['jpg', 'png'], default="jpg")
    (options, args) = parser.parse_args()

    # check if source and destination directory exists and change working directory
    if os.path.isdir(options.source):
        os.chdir(options.source)
    else:
        print("Source directory could not be found.")
        exit()

    if options.destination == options.source:
        diff_dir = False

    if not options.destination:
        choice = input("Destination directory not specified. Rename files in source directory? (y/n) ")
        if choice.lower() == 'y':
            options.destination = options.source
            diff_dir = False

    if not os.path.isdir(options.destination):
        print("Destination directory could not be found.")
        exit()

    for file in glob.glob("*." + options.type):
        if not diff_dir:
            old_file = file
            file = old_file[:-4]+"_old.jpg"
            os.rename(old_file, file)
        date = datetime.datetime.fromisoformat(get_date_taken(options.source+"\\"+file))
        milliseconds = int(round(date.timestamp() * 1000))
        file_dict[file] = milliseconds

    file_dict = sorted(file_dict.items(), key=operator.itemgetter(1))

    i = 0
    for k, v in file_dict:
        if diff_dir:
            copyfile(k, options.destination + "\\" + str(i) + ".JPG")
        else:
            os.rename(k, str(i) + ".JPG")
        i += 1

    print("We've reached the end!")


if __name__ == '__main__':
    main()