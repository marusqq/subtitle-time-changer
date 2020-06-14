#change subtitles
import datetime
import json
from sys import argv
from os import listdir, getcwd

def split_time_to_sets(line, time_count):
    '''splits line and returns [hours, minutes, seconds, milliseconds]'''

    if time_count == 1:
        #take endspace char from the first one      
        line = line.replace(' ', '')

    elif time_count == 2:
        #take \n from the last one
        line = line.lstrip()
        line = line.rstrip()

    time1 = line.split(':')
    secs_milisecs = time1[2].split(',')

    hours = time1[0]
    minutes = time1[1]
    seconds = secs_milisecs[0]
    milliseconds = secs_milisecs[1]
    return [hours, minutes, seconds, milliseconds]

def check_for_time_miscalculation(time_type, value):
    '''returns true if there is more value than possible
    false if everything is legal'''
    if time_type in ['h', 'm', 's']:
        return value >= 60

    elif time_type in ['ms']:
        return value >= 1000

def add_zeroes(type, number):
    '''takes int/str, returns str with leading zeroes'''
    if type.lower() in ['h', 'm', 's']:
        return str(number).zfill(2)
        
    elif type.lower() in ['ms']:
        return str(number).zfill(3)

def set_time(time, time_type, time_value):
    '''sets time from time_type to time_value while still adding zeroes'''
    if time_type == 'h':
        time[0] = add_zeroes(time_type, str(time_value))
    elif time_type == 'm':
        time[1] = add_zeroes(time_type, str(time_value))
    elif time_type == 's':
        time[2] = add_zeroes(time_type, str(time_value))
    elif time_type == 'ms':
        time[3] = add_zeroes(time_type, str(time_value))
    return time

def add_time(time_to_add_to, time_type, time_to_add):
    '''adds time with basic int addition and going over 60/1000 limits
    returns time_to_add_to'''

    if time_type.lower() == 'h':
        time_to_add_to[0] = add_zeroes('h', int(time_to_add_to[0]) + int(time_to_add))
    
    elif time_type.lower() == 'm':

        if check_for_time_miscalculation(time_type.lower(), int(time_to_add_to[1]) + int(time_to_add)):
            
            minutes = (int(time_to_add_to[1]) + int(time_to_add)) % 60
            hours = (int(time_to_add_to[1]) + int(time_to_add)) // 60

            #if adding 128 to 0, minutes would get 8, and hours would get 2
            set_time(time_to_add_to, 'm', minutes)
            add_time(time_to_add_to, 'h', hours)
        else:
            time_to_add_to[1] = add_zeroes('m', int(time_to_add_to[1]) + int(time_to_add))

    elif time_type.lower() == 's':

        if check_for_time_miscalculation(time_type.lower(), int(time_to_add_to[2]) + int(time_to_add)):
            
            seconds = (int(time_to_add_to[2]) + int(time_to_add)) % 60
            minutes = (int(time_to_add_to[2]) + int(time_to_add)) // 60
            
            #if adding 18 to 42, seconds would get 0, and minutes would get 1
            set_time(time_to_add_to, 's', seconds)
            add_time(time_to_add_to, 'm', minutes)
        else:
            time_to_add_to[2] = add_zeroes('s', int(time_to_add_to[2]) + int(time_to_add))

    elif time_type.lower() == 'ms':
        if check_for_time_miscalculation(time_type.lower(), int(time_to_add_to[3]) + int(time_to_add)):
            
            milliseconds = (int(time_to_add_to[3]) + int(time_to_add)) % 1000
            seconds = (int(time_to_add_to[3]) + int(time_to_add)) // 1000

            #if adding 1001 to 0001, seconds would get 1, and minutes would get 2
            set_time(time_to_add_to, 'ms', milliseconds)
            add_time(time_to_add_to, 's', seconds)
        else:
            time_to_add_to[3] = add_zeroes('ms', int(time_to_add_to[3]) + int(time_to_add))

    return

def print_dash_line():
    print('---------------------------------')
    return

def print_time(time, freetext_front = None, freetext_end = None):
    '''prints time in four different rows'''
    print(str(freetext_front) + time[0] + ':' + time[1] + ':' + time[2] + ',' + time[3] + str(freetext_end))
    print_dash_line()
    return

def print_start_info(filename, thing_to_add, value_to_add):
    '''prints filename, type_of_time adding and adding value'''
    
    print_dash_line()
    if value_to_add < 0:
        print('Removing', str(value_to_add) + thing_to_add, 'to [', filename, ']')

    else:
        print('Adding', str(value_to_add) + thing_to_add, 'to [', filename, ']')
    
    print('Change type or value in add_settings.json')
    print_dash_line()

    return

def format_time_for_output(time1, time2):
    time = (time1[0] + ':' + time1[1] + ':' + time1[2] + ',' + time1[3]
          + ' --> ' +
          time2[0] + ':' + time2[1] + ':' + time2[2] + ',' + time2[3]
          + '\n')
    return time

def get_file_name():
    files_in_loc = listdir(getcwd())
    for file in reversed(files_in_loc):
        if not '.srt' in file or 'converted' in file:
            files_in_loc.remove(file)
    if len(files_in_loc) == 1:
        return files_in_loc[0]
    else:
        print('Choose what subtitle to convert:')
        print_dash_line()
        for i in range(len(files_in_loc)):
            print(int(i) + 1, '---> for', files_in_loc[i])
        print_dash_line()
        
        file_choose = int(input('Enter number and press enter:\n'))
        try:
            return files_in_loc[file_choose]
        except IndexError:
            quit('Wrong choice!')

if __name__ == "__main__":

    filename = get_file_name()
    if filename is None:
        quit('No .srt file found! Exiting')

    with open('add_settings.json') as f:
        data = json.load(f)

    thing_to_add = str(data['time_type_to_add'])
    value_to_add = int(data['time_to_add'])

    out_file = open('converted_' + filename, 'w+')

    try:
        print_start_info(filename, thing_to_add, value_to_add)
        with open(filename) as fp:
            line = 'first_time'
            while line:
                line = fp.readline()
                
                #if this is not a time line
                if '-->' not in line:
                    out_file.write(line)
                
                #if time line, let's try to calculate
                else:
                    
                    #split two times
                    times = line.split('-->')

                    #split hours, minutes, seconds, milliseconds
                    time1 = split_time_to_sets(times[0], 1)
                    time2 = split_time_to_sets(times[1], 2)

                    #add desired time                             
                    add_time(time1, thing_to_add, value_to_add)
                    add_time(time2, thing_to_add, value_to_add)

                    #combine and write to file
                    out_file.write(format_time_for_output(time1, time2))
        
        out_file.close()
        print('Done!')

    except FileNotFoundError:
        quit('Add ' + filename + ' file to the directory this script is in.')


           

       