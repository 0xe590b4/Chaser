#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
# @Time    : 2020-05-25  21:28
# @Author  : 行颠
# @Email   : 0xe590b4@gmail.com
# @File    : demo1.py
# @Software: test
# @DATA    : 2020-05-25
"""

import os
from batch_maker.tools import ShortVideo
from natsort import natsorted

from threading import Thread


class BatchMovie(Thread):

    def __init__(self):
        super(BatchMovie, self).__init__()

        self.sv = ShortVideo()

    def head(self, input_video_filename, output_video_filename, times=1):
        self.sv.head(
            input_video_filename,
            output_video_filename,
            times
        )

    def end(self, input_video_filename, output_video_filename, end_title="结束语", cut_time=5):
        self.sv.end_add_circle(
            input_video_filename,
            output_video_filename,
            end_title,
            cut_time
        )


    def body(self,
             input_movie_filename,
             bgm_audio_filename,
             title,
             subtitle,
             output_movie_filename
             ):
        data = {

            "start": 0,
            "end": int(self.sv.get_video_duration(input_movie_filename)),
            "ratio": 1,
            "title": title,
            "src_volume": 3,
            "dst_volume": 5,
            # "bgm_filename": bgm_audio_filename,
            #"watermark": "/Users/0xe590b4/Downloads/Chaser/demo/logo.png",
            "subtitle": subtitle,
            "output_video_filename": output_movie_filename,
            "video_name": os.path.basename(input_movie_filename),
            "input_video_filename": input_movie_filename

        }

        self.sv.make_new_video(data)

    def subtitle(self, input_movie_filename, srt_filename, text):
        self.sv.subtitle(input_movie_filename, srt_filename, text)

    def head_body_end(self, head_filename, body_filename, end_filename, output_video_filename):
        self.sv.head_body_end(head_filename, body_filename, end_filename, output_video_filename)

    def clear(self, path):
        import shutil

        try:
            shutil.rmtree("{}/".format(path))
        except:
            pass

if __name__ == '__main__':

    workspace = "/Users/0xe590b4/Downloads/3d/done/demo"


    end_title = "燕南赵北 \n 感谢您观看！"
    movie_data = workspace + "/data"
    movie_head = workspace + "/head"
    movie_body = workspace + "/body"
    movie_end = workspace + "/end"
    movie_subtitle = workspace + "/subtitle"
    movie_bgm = workspace + "/bgm"
    movie_result = workspace + "/result"

    title_list = [
        "第一集",
        "第二集",
        "第三集"
    ]

    subtitle_list = [
        "英雄的结局总让人唏嘘！",
        "没有点本事,怎么敢做辛弃疾的女人",
        "斩叛徒,收失地,真英雄！"
    ]

    m = BatchMovie()


    for i  in [1,2,3]:

        data_mp4 = "{}/{}.mp4".format(movie_data, i)
        haad_image = "{}/{}.png".format(movie_head, i)
        haad_mp4 = "{}/{}.mp4".format(movie_head, i)
        body_mp4 = "{}/{}.mp4".format(movie_body, i)
        end_mp4 = "{}/{}.mp4".format(movie_end, i)
        subtitle_filename = "{}/{}.srt".format(movie_subtitle, i)
        bgm_filename = "{}/{}.mp3".format(movie_bgm, i)


        #if not os.path.exists(haad_mp4):
        m.head(haad_image, haad_mp4, times=1)

        #if not os.path.exists(body_mp4):
        m.subtitle(data_mp4, subtitle_filename, subtitle_list[i - 1])

        m.body(data_mp4,
               bgm_filename,
               title_list[i - 1],
               subtitle_filename,
               movie_body,
               )

        #if not os.path.exists(end_mp4):
        m.end(body_mp4,
              end_mp4,
              end_title,
              5
              )

        m.head_body_end(
            "{}/{}.mp4".format(movie_head, i),
            "{}/{}.mp4".format(movie_body, i),
            "{}/{}.mp4".format(movie_end, i),
            "{}/{}.mp4".format(movie_result, i)
        )


