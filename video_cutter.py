import os
from os import listdir
from os.path import isfile, join


def video_cutter(input_path, output_path, start_time, end_time, vcodec="copy", acodec="copy",
                 preset="slow", crf=0):
    cmd = "ffmpeg -i " + input_path + " -ss " + start_time + " -to " + end_time + " -c:v " + vcodec + " -preset " + preset + " -crf " + str(
        crf) + " -x264-params keyint=123:min-keyint=20 -c:a " + acodec + " " + output_path
    result = os.system(cmd)
    return result


def get_cut_times(times):
    times = times.replace(".", ":")
    segments = times.split("_")
    segments = [(item.split("-")) for item in segments]

    for i in range(0, len(segments)):  # increase end time by 1 sec
        end_time = segments[i][1]
        second=end_time.rfind(":")
        if int(end_time[second+1:])!=59:
            segments[i][1] = end_time[:second+1] + str(int(end_time[second+1:]) + 1)

    for segment in segments:
        try:
            for indx in range(0, 2):
                if segment[indx].count(":") == 0:
                    segment[indx] = "0:0:" + segment[indx]
                elif segment[indx].count(":") == 1:
                    segment[indx] = "0:" + segment[indx]
                elif segment[indx].count(":") == 2:
                    pass
                else:
                    print("error in filename:" + times)
                    return -1
        except IndexError:
            print("error in filename:" + times)
            return -1

    return segments


def unedited():
    ipath = input("Enter Source video's directory: ")
    edited=ipath+"/output"
    if not os.path.exists(ipath+"/unedited"):
        os.mkdir(ipath+"/unedited")

    result=[file for file in listdir(edited) if isfile(join(edited, file))]
    result=[file[:-7]+file[-4:] for file in result]
    source=[file for file in listdir(ipath) if isfile(join(ipath, file))]

    for item in set(source):
        if item not in result:
            os.system("cp " + ipath + "/" + item + " " + ipath + "/unedited/")


def nameCorrection(cwd):
    files = [file for file in listdir(cwd) if isfile(join(cwd, file))]
    if not os.path.exists(cwd+"/correctedName"):
        os.mkdir(cwd+"/correctedName")
    for file in files:
        name=file.replace(" ","")
        name=name[1:name.rfind(".")-1]+name[name.rfind("."):]
        name=name.replace(")(","_")
        originalname=file.replace(")","\)")
        originalname=originalname.replace("(","\(")
        print(name)
        os.system("cp "+join(cwd,originalname)+" "+join(cwd+"/correctedName",name))
        



if __name__ == "__main__":

    cwd = input("Enter video's directory: ")
    while not os.path.exists(cwd):
        cwd = input("This directory does not exist! Enter video's directory: ")

    output_path = cwd + "/output"
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    files = [file for file in listdir(cwd) if isfile(join(cwd, file))]
    
    format_list = ["mov", "avi", "3gp", "mpg", "mkv", "mp4", ]
    video_files = list(filter(lambda x: x[x.rfind(".") + 1:].lower() in format_list, files))
    unprocessed_files = [video for video in files if video not in video_files]

    for video in video_files:
        index = video.rfind(".")
        name = video[:index]
        video_format = video[index + 1:]
        times = get_cut_times(name)

        output_index = 0
        if times != -1:
            for time in times:
                start_time = time[0]
                end_time = time[1]
                print("cutting " + video)
                output_index += 1
                output_name = name + "\(" + str(output_index) + "\)." + video_format
                exit_code = video_cutter(input_path=join(cwd, video), output_path=output_path + "/" + output_name,
                                         start_time=start_time, end_time=end_time, vcodec="libx264", crf=10)
                if exit_code != 0:
                    unprocessed_files.append(output_name)
                    print(output_name + ": unsuccessful!")
                else:
                    print(output_name + ":  successful")
        else:
            unprocessed_files.append(video)

    print("==================================================")
    print(unprocessed_files)
