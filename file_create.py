import sys
import io

source_file = sys.argv[1]
target_file = sys.argv[2]
bytes_to_read = int(sys.argv[3]) * 1024 * 1024





def usage():
    print "file_create.py src_file_name <dest_file_name_prefix> <dest_file_size> <count>"

def main():
    source_file = sys.argv[1]
    dest_file_name_prefix = sys.argv[2]
    dest_file_size = int(sys.argv[3]) * 1024 * 1024
    dest_file_count = int(sys.argv[4])
    dest_file_format = ""


    for i in range (0,dest_file_count):
        dest_file_name = dest_file_name_prefix + "_{}".format(i)+dest_file_format
        with open(source_file, 'rb') as src, open(dest_file_name,'wb') as trg:
            #file_buffer = io.BufferedReader(src)
            data = src.read(dest_file_size)
            trg.write(data)

if __name__ == "__main__":
    main()




