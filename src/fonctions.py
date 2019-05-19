import cv2
import os
from time import time


def timer_decorator(func):
    def f(*args, **kwargs):
        before = time()
        rv = func(*args, **kwargs)
        after = time()
        print("{:05.2f}ms elapsed in {}".format(1000*(after - before), func.__name__))
        return rv

    return f


# @timer_decorator
def my_resize(image, width=None, height=None, inter=cv2.INTER_LINEAR):  # INTER_AREA
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        if height is None:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))
        else:
            if w < h:
                r = width / float(w)
                dim = (width, int(h * r))
            else:
                r = height / float(h)
                dim = (int(w * r), height)
    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


width_target = 640


def get_video_save_size(h, w):
    r = width_target / float(w)
    dim = (width_target, int(h * r))

    return dim


def create_gif(video_path, o_folder, fps=5, width=320):
    gif_file_name = o_folder + "video_solve_0.gif"
    ind_save = 0
    while os.path.isfile(gif_file_name):
        ind_save += 1
        gif_file_name = o_folder + "video_solve_{}.gif".format(ind_save)

    cmd = ["ffmpeg",
           "-i", video_path,
           "-vf scale={}:-1".format(width),
           "-r", str(fps),
           "-f image2pipe",
           "-loglevel fatal",
           "-vcodec ppm - |",
           "convert",
           "-delay", str(20),
           "-loop 0",
           "-", gif_file_name
           ]
    cmd = " ".join(cmd)
    os.system(cmd)


if __name__ == '__main__':
    # video_path_ = "/home/remi/PycharmProjects/sudoku-solver/videos_result/out_process_0.mp4"
    # o_folder_ = "/home/remi/PycharmProjects/sudoku-solver/videos_result/"
    # create_gif(video_path_, o_folder_, width=480)
    im = cv2.imread("images_test/sudoku2.jpg")
    my_resize(im, height=900)
    my_resize(im, height=900, inter=cv2.INTER_AREA)
