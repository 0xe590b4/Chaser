#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
# @Time    : 2020-07-06  10:18
# @Author  : 行颠
# @Email   : 0xe590b4@gmail.com
# @File    : test
# @Software: Chaser
# @DATA    : 2020-07-06
"""

import  os
from batch_maker.tools import ShortVideo


movie_cut = "/Users/0xe590b4/Downloads/3d"
movie_data = "/Users/0xe590b4/Downloads/3d/done/demo/data"
movie_head = "/Users/0xe590b4/Downloads/3d/done/demo/head"
movie_filename1 = "/Users/0xe590b4/Downloads/3d/demo1.mp4"




def clear(path):
    import shutil

    try:
        shutil.rmtree("{}/".format(path))
    except:
        pass





m = ShortVideo()


# m.get_video_high_part(
#         movie_filename1,
#         movie_cut
# )

#
# clear(movie_data+"/3")
# m.cut_video(movie_filename1, m.t2s("01:12:04"), m.t2s("01:12:20"), movie_data + "/3/1.mp4")
# m.cut_video(movie_filename1, m.t2s("00:06:10"), m.t2s("00:06:18"), movie_data + "/3/2.mp4")
# m.cut_video(movie_filename1, m.t2s("00:26:12"), m.t2s("00:26:27"), movie_data + "/3/3.mp4")
# m.cut_video(movie_filename1, m.t2s("01:14:41"), m.t2s("01:15:04"), movie_data + "/3/4.mp4")
# m.merge_movies(movie_data+"/3",movie_data+"/3.mp4")
#
#
# clear(movie_data+"/2")
# m.cut_video(movie_filename1, m.t2s("01:25:03"), m.t2s("01:25:21"), movie_data + "/2/1.mp4")
# m.cut_video(movie_filename1, m.t2s("01:25:40"), m.t2s("01:25:44"), movie_data + "/2/2.mp4")
# m.cut_video(movie_filename1, m.t2s("01:25:45"), m.t2s("01:25:50"), movie_data + "/2/3.mp4")
# m.cut_video(movie_filename1, m.t2s("01:25:52"), m.t2s("01:26:15"), movie_data + "/2/4.mp4")
# m.merge_movies(movie_data+"/2",movie_data+"/2.mp4")
#
#
# clear(movie_data+"/1")
# m.cut_video(movie_filename1, m.t2s("00:46:42"), m.t2s("00:46:45"), movie_data + "/1/1.mp4",100)
# m.cut_video(movie_filename1, m.t2s("00:24:57"), m.t2s("00:25:03"), movie_data + "/1/2.mp4",100)
# m.cut_video(movie_filename1, m.t2s("00:48:15"), m.t2s("00:48:22"), movie_data + "/1/3.mp4",100)
# m.cut_video(movie_filename1, m.t2s("01:21:48"), m.t2s("01:22:17"), movie_data + "/1/4.mp4",100)
# m.cut_video(movie_filename1, m.t2s("01:26:22"), m.t2s("01:26:42"), movie_data + "/1/5.mp4",100)
# m.merge_movies(movie_data+"/1",movie_data+"/1.mp4")


# m.get_movie_frames(
#     movie_filename1,
#     m.t2s("00:46:57"),  # 将第120秒内容当封皮
#     movie_head + "/cover.png",
#     "机械.画皮"
# )

# m.rows_for_cover(
#     movie_head + "/cover.png",
#     movie_head
# )


