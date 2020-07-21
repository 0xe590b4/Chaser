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
from demo.tools import ShortVideo


movie_cut = "/Users/0xe590b4/Downloads/3d"
movie_data = "/Users/0xe590b4/Downloads/3d/done/demo/data"
movie_head = "/Users/0xe590b4/Downloads/3d/done/demo/head"
movie_filename1 = "/Users/0xe590b4/Downloads/demo.mp4"





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

# m.cut_audio("/Users/0xe590b4/Downloads/demo.mp3", m.t2s("00:02:15"), m.t2s("00:03:45"), "/Users/0xe590b4/Downloads/bgm.mp3")
#
# clear(movie_data+"/3")
# m.cut_video(movie_filename1, m.t2s("00:42:11"), m.t2s("00:42:16"), movie_data + "/3/1.mp4",0)
#m.cut_video(movie_filename1, m.t2s("00:42:18"), m.t2s("00:42:35"), movie_data + "/3/2.mp4",0)
# m.cut_video(movie_filename1, m.t2s("00:55:31"), m.t2s("00:55:45"), movie_data + "/3/3.mp4",0)
# m.cut_video(movie_filename1, m.t2s("01:28:27"), m.t2s("01:28:45"), movie_data + "/3/4.mp4",0)
# m.cut_video(movie_filename1, m.t2s("01:38:45"), m.t2s("01:38:50"), movie_data + "/3/5.mp4",0)
#m.cut_video(movie_filename1, m.t2s("01:41:19"), m.t2s("01:41:28"), movie_data + "/3/6.mp4",0)
#m.cut_video(movie_filename1, m.t2s("01:42:15"), m.t2s("01:42:30"), movie_data + "/3/7.mp4",0)
# m.merge_movies(movie_data+"/3",movie_data+"/3.mp4")

#
# clear(movie_data+"/2")
# m.cut_video(movie_filename1, m.t2s("00:12:55"), m.t2s("00:13:03"), movie_data + "/2/1.mp4")
# m.cut_video(movie_filename1, m.t2s("00:08:25"), m.t2s("00:08:35"), movie_data + "/2/2.mp4")
# m.merge_movies(movie_data+"/2",movie_data+"/2.mp4")

#
#
# clear(movie_data+"/1")
#m.cut_video(movie_filename1, m.t2s("00:53:12"), m.t2s("00:53:22"), movie_data + "/1/1.mp4")
# m.cut_video(movie_filename1, m.t2s("00:53:30"), m.t2s("00:53:45"), movie_data + "/1/2.mp4")
# m.cut_video(movie_filename1, m.t2s("01:39:20"), m.t2s("01:39:27"), movie_data + "/1/3.mp4")
#m.cut_video(movie_filename1, m.t2s("01:39:30"), m.t2s("01:39:42"), movie_data + "/1/4.mp4")
# m.cut_video(movie_filename1, m.t2s("01:44:40"), m.t2s("01:45:00"), movie_data + "/1/5.mp4")
#m.cut_video(movie_filename1, m.t2s("00:28:40"), m.t2s("00:28:50"), movie_data + "/1/6.mp4")
#m.merge_movies(movie_data+"/1",movie_data+"/1.mp4")
#
#
# m.get_movie_frames(
#     movie_filename1,
#     m.t2s("01:26:36"),  # 将第120秒内容当封皮
#     movie_head + "/cover.png",
#     ""
# )
#
# m.rows_for_cover(
#     movie_head + "/cover.png",
#     movie_head
# )


