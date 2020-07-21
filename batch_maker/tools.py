#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
# @Time    : 2020-05-25  21:00
# @Author  : 行颠
# @Email   : 0xe590b4@gmail.com
# @File    : demo.py
# @Software: demo.py
# @DATA    : 2020-05-25
"""



import numpy as np
import pandas as pd

from moviepy.editor import *
from moviepy.video.tools.drawing import circle
from moviepy.video.tools.credits import credits1
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

import moviepy.audio.fx.all as afx
import moviepy.video.fx.all as vfx

from demo.config import *


class ShortVideo():

    def __init__(self):
        pass

    def makedirs(self, file_path):

        import os

        if os.path.isdir(file_path) == False:

            parent_path = os.path.dirname(file_path)

            if not os.path.exists(parent_path):

                os.makedirs(parent_path)
        else:

            os.makedirs(file_path)

    def clear(self,path):
        import shutil

        try:
            shutil.rmtree("{}/".format(path))
        except:
            pass

    def get_video_duration(self, video_path):
        video = VideoFileClip(video_path)
        return video.duration

    def get_video_time(self, video_path):

        video = VideoFileClip(video_path)
        second = video.duration
        video.close()

        duration = '{0}:{1}:{2}'
        if second > 0:
            hour = int(second / 3600)
            if hour > 0:
                mm = int(second % 3600 / 60)
                ss = int(second % 3600 % 60)
                duration = duration.format('{:0>2d}'.format(hour), '{:0>2d}'.format(mm), '{:0>2d}'.format(ss))
            else:
                mm = int(second / 60)
                ss = int(second % 60)
                duration = duration.format('{:0>2d}'.format(0), '{:0>2d}'.format(mm), '{:0>2d}'.format(ss))
        else:
            duration = '00:00:00'
        return duration

    def t2s(self, time_str):
        h, m, s = time_str.strip().split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)

    def s2t(self, second):

        duration = '{0}:{1}:{2}'
        if second > 0:
            hour = int(second / 3600)
            if hour > 0:
                mm = int(second % 3600 / 60)
                ss = int(second % 3600 % 60)
                duration = duration.format('{:0>2d}'.format(hour), '{:0>2d}'.format(mm), '{:0>2d}'.format(ss))
            else:
                mm = int(second / 60)
                ss = int(second % 60)
                duration = duration.format('{:0>2d}'.format(0), '{:0>2d}'.format(mm), '{:0>2d}'.format(ss))
        else:
            duration = '00:00:00'
        return duration


    def get_audio_high_part(self, input_audio_filename, output_audio_filename, seconds=15):
        """
        找音乐中最精彩的部分
        :param input_audio_filename:
        :param output_audio_filename:
        :param title:
        :return:
        """

        # from pychorus import find_and_output_chorus
        #
        # self.makedirs(output_audio_filename)
        #
        # find_and_output_chorus(
        #     input_audio_filename,
        #     output_audio_filename,
        #     seconds)

        pass

    def custom_resize(self, input_image_path, output_image_path, size=(720, 1080), end_with=".jpeg",
                      resize_send_with=".png"):
        """
        图片重新设置大小
        :param input_image_path 图片列表（图片大小需要一致）
        :param output_image_path  图片输出位置及文件名
        :param size 宽高
        :param end_with 以什么结尾
        :param resize_send_with 重新设置大小后设置的格式
        """

        from skimage.io import imread, imsave

        from skimage.transform import resize

        image_list = os.listdir(input_image_path)

        for image in image_list:

            # 指定结尾的图片再缩放大小
            if image.endswith('{}'.format(end_with)):
                img = imread('{}/{}'.format(input_image_path, image))

                img_resized = resize(img, size)

                sava_file = '{}/resize_{}{}'.format(output_image_path, image, resize_send_with)

                self.makedirs(sava_file)

                img_uint8 = img_resized.astype(np.uint8)

                imsave(sava_file, img_uint8)

    def image_to_video(self, input_image_path, output_video_filename, end_with=".png", fps=10):
        """
        图片合成视频
        :param input_image_path 图片列表（图片大小需要一致）
        :param output_video_filename 视频输出位置及文件名
        :param end_with
        :param fps
        """

        from natsort import natsorted

        self.makedirs(output_video_filename)

        filelist = os.listdir(input_image_path)

        image_list = []

        for item in natsorted(filelist):
            if item.endswith('{}'.format(end_with)):
                image_list.append('{}/{}'.format(input_image_path, item))

        clip = ImageSequenceClip(image_list, fps=fps)
        clip.write_videofile(output_video_filename)
        clip.close()

    def get_audio_from_video(self, video_filename):
        """
        从视频中提取音频，如果是无声音视频需要加空白声音
        :param video_filename:
        return:
        """

        from pydub import AudioSegment

        audio_filename = '{}.wav'.format(video_filename)

        # if os.path.exists(audio_filename):
        #     return audio_filename

        video = VideoFileClip(video_filename)
        audio = video.audio
        duration_video = video.duration

        if audio:

            audio.write_audiofile(audio_filename)
            audio.close()
        else:
            silence = AudioSegment.silent(duration=duration_video * 1000)
            silence.export(audio_filename, format="wav")

        return audio_filename


    def head(self, input_images_filename, output_video_filename,times=1):
        """

        :param input_images_path:
        :param output_video_filename:
        :param resize_path:
        :return:
        """

        self.makedirs(output_video_filename )

        if input_images_filename.lower().endswith(".gif",4):

            video_clip = VideoFileClip(input_images_filename).resize((720,1280)).set_duration(times)
            video_clip.write_videofile(output_video_filename)

            return  output_video_filename

        if input_images_filename.lower().endswith(".png", 4):
            image_list = [input_images_filename]
            clip = ImageSequenceClip(image_list, fps=1).resize((720,1280))
            clip.write_videofile(output_video_filename)
            clip.close()

            return output_video_filename


    def end(self, input_images_path, output_video_filename, resize_path, size=(800, 800), end_with='.png',
            resize_send_with=".png", fps=5):
        """

        :param input_images_path:
        :param output_video_filename:
        :param resize_path:
        :return:
        """
        self.custom_resize(input_images_path, resize_path, size=size, end_with=end_with,
                           resize_send_with=resize_send_with)
        self.image_to_video(resize_path, output_video_filename, end_with=resize_send_with, fps=fps)

        return output_video_filename

    def end_add_circle(self, input_video_filename, output_video_filename, title="燕南赵北 \n 视频教程", cut_time=5):
        """
         以圆关闭为结尾的视频片尾
        :param input_video_filename:
        :param output_video_filename:
        :param title:
        :param cut_time:
        :return:
        """
        # 获取视频时长
        video_clip = VideoFileClip(input_video_filename)
        video_duration  = int(video_clip.duration)

        # 获取视频音频
        audio_filename = self.get_audio_from_video(input_video_filename)
        audio_clip = AudioFileClip(audio_filename)
        audio_duration = int(audio_clip.duration)


        clip = VideoFileClip(input_video_filename). \
            subclip(video_duration - cut_time, video_duration). \
            add_mask()


        clip.mask.get_frame = lambda t: circle(screensize=(clip.w, clip.h),
                                               center=(clip.w / 2, clip.h / 4),
                                               radius=max(0, int(800 - 200 * t)),
                                               col1=1, col2=0, blur=4)

        the_end = TextClip(title, font=TITLE_FONT, color="white",
                           fontsize=70).set_duration(clip.duration)

        final = CompositeVideoClip([the_end.set_pos('center'), clip],
                                   size=clip.size)

        # 合并音频
        result_audio = CompositeAudioClip([audio_clip])

        # 视频设置音频文件
        final_clip = final.set_audio(result_audio.subclip(audio_duration - cut_time, audio_duration))

        self.makedirs(output_video_filename)
        # 要这样设置 否则无声
        final_clip.write_videofile(output_video_filename,
                                   codec='libx264',
                                   audio_codec='aac',
                                   temp_audiofile=output_video_filename + '_temp-audio.m4a',
                                   remove_temp=True,
                                   threads=4
                                   )

    def end_add_credits(self, input_video_filename, output_video_filename, credits_filename="credits.txt",
                        keep_times=2):
        """
        生成最后的演员表的视频片尾
        :param input_video_filename:
        :param output_video_filename:
        :param credits_filename 演员表
        :return:
        """

        clip = (VideoFileClip(input_video_filename)
                .speedx(0.4)
                .fx(vfx.colorx, 0.7))

        # mountainmask = ImageClip('./end/4.png', ismask=True)

        credits = credits1(credits_filename, 3 * clip.w / 4, font=TITLE_FONT)
        scrolling_credits = credits.set_pos(lambda t: ('center', -10 * t))

        # final = CompositeVideoClip([clip, scrolling_credits, clip.set_mask(mountainmask)])

        final = CompositeVideoClip([clip,
                                    scrolling_credits
                                    ])

        final.set_duration(keep_times).write_videofile(output_video_filename,
                                                       codec='libx264',
                                                       audio_codec='aac',
                                                       temp_audiofile=output_video_filename + '_temp-audio.m4a',
                                                       remove_temp=True
                                                       )
        final.close()

    def head_body_end(self, head_filename, body_filename, end_filename, output_video_filename):
        """

        :param head_filename:
        :param body_filename:
        :param end_filename:
        :param output_file_name:
        :return:
        """

        # 获取视频时长
        clip_video1 = VideoFileClip(head_filename)
        clip_video2 = VideoFileClip(body_filename)
        clip_video3 = VideoFileClip(end_filename)
        duration_video1 = clip_video1.duration
        duration_video2 = clip_video2.duration
        duration_video3 = clip_video3.duration

        # 获取视频音频
        path_audio1 = self.get_audio_from_video(head_filename)
        path_audio2 = self.get_audio_from_video(body_filename)
        path_audio3 = self.get_audio_from_video(end_filename)

        audio_video1 = AudioFileClip(path_audio1)
        audio_video2 = AudioFileClip(path_audio2).subclip(0,duration_video2-duration_video3)
        audio_video3 = AudioFileClip(path_audio3)


        # 统一视频分辨率
        w1, h1, fps1 = clip_video1.w, clip_video1.h, clip_video1.fps
        w2, h2, fps2 = clip_video2.w, clip_video2.h, clip_video2.fps


        clip_video1_new = clip_video1

        if w2 == w1 and h2 == h2:
            clip_video2_new = clip_video2.subclip(0,duration_video2-duration_video3)
        else:
            clip_video2_new = clip_video2.resize((w1, int(h1*(0.65)))).subclip(0, duration_video2 - duration_video3)

        clip_video3_new = clip_video3.resize((w1, h1))


        result_video = CompositeVideoClip([
            clip_video1_new,

            clip_video2_new.set_start(duration_video1).crossfadein(1).set_pos("center"),

            clip_video3_new.set_start(duration_video1 + duration_video2 - duration_video3 ).crossfadein(1)])

        # 合并音频
        result_audio = CompositeAudioClip([
            audio_video1,
            audio_video2.set_start(duration_video1),
            audio_video3.set_start(duration_video1 + duration_video2 - duration_video3)
        ])

        # 视频设置音频文件
        final_clip = result_video.set_audio(result_audio)

        self.makedirs(output_video_filename)
        # 要这样设置 否则无声
        final_clip.write_videofile(output_video_filename,
                                   codec='libx264',
                                   audio_codec='aac',
                                   temp_audiofile=output_video_filename + '_temp-audio.m4a',
                                   remove_temp=True
                                   )

    def get_video_high_part(self, input_video_filename, output_video_path):
        """

        :param input_video_path:
        :param output_video_path:
        :return:
        """

        from scipy.io import wavfile

        audio_output_path = "{}.wav".format(input_video_filename)

        if os.path.exists(audio_output_path) == False:
            audio_output_path = self.get_audio_from_video(input_video_filename)

        sr, x = wavfile.read(audio_output_path)
        x = x[:, 0]

        # 性能低下 用上面的快
        # import  librosa
        # x, sr = librosa.load(audio_output_path)

        max_slice = 5
        cut_slice = 5
        window_length = max_slice * sr

        # 计算短时能量最费时间
        energy = np.array([sum(abs(x[i:i+window_length]**2)) for i in range(0, len(x), window_length)])

        #energy = np.array([sum(abs(x[i:i + window_length])) for i in range(0, len(x), window_length)])

        df = pd.DataFrame(columns=['energy', 'start', 'end'])

        nums = []
        for i in range(len(energy)):
            nums.append(energy[i])

        # 利用四分位的方法 取85%以上的内容
        t = np.percentile(nums, 85, interpolation='midpoint')
        thresh = int(t)
        print("85%位", thresh)

        row_index = 0
        for i in range(len(energy)):

            value = energy[i]
            if value >= thresh:
                i = np.where(energy == value)[0]
                df.loc[row_index, 'energy'] = value
                df.loc[row_index, 'start'] = i[0] * cut_slice
                df.loc[row_index, 'end'] = (i[0] + 1) * cut_slice -1
                row_index = row_index + 1

        temp = []
        i = 0
        j = 0
        n = len(df) - 2
        m = len(df) - 1
        while (i <= n):
            j = i + 1
            while (j <= m):
                if (df['end'][i] == df['start'][j]):
                    df.loc[i, 'end'] = df.loc[j, 'end']
                    temp.append(j)
                    j = j + 1
                else:
                    i = j
                    break

        df.drop(temp, axis=0, inplace=True)

        start = np.array(df['start'])
        end = np.array(df['end'])

        video_list = []
        for i in range(len(df)):
            if (i != 0):
                start_lim = start[i] - cut_slice
            else:
                start_lim = start[i]
            end_lim = end[i]


            filename = "{}/cut_{}.mp4".format(output_video_path, (i + 1))

            self.makedirs(filename)
            video_list.append(filename)

            # self.cut_video(input_video_path, start_lim, end_lim, filename)

            ffmpeg_extract_subclip(input_video_filename, start_lim, end_lim, targetname=filename)

        return video_list

    def merge_movies(self, video_dir, output_video_filename):
        """

        :param video_dir:
        :param output_video_filename:
        :return:
        """

        from natsort import natsorted

        # 定义一个数组
        L = []
        A = []

        temp = []
        # 访问 video 文件夹 (假设视频都放在这里面)
        for root, dirs, files in os.walk(video_dir):

            # 遍历所有文件
            for file in natsorted(files):
                # 如果后缀名为 .mp4
                if os.path.splitext(file)[1] == '.mp4':
                    # 拼接成完整路径
                    filePath = os.path.join(root, file)
                    # 载入视频
                    video = VideoFileClip(filePath).fx(vfx.fadein,3,(0,0,0)).fx(vfx.fadein,3,(0,0,0)).fx(vfx.colorx, 1.5)
                    video = video.resize((1280, 720))

                    # 添加到数组
                    L.append(video)

                    # 获取视频音频
                    path_audio = self.get_audio_from_video(filePath)
                    audio = AudioFileClip(path_audio)
                    A.append(audio)
                    temp.append(path_audio)

        # 合并4段视频
        result_video = concatenate_videoclips(L)

        # 合并音频
        result_audio = concatenate_audioclips(A)

        # 视频设置音频文件
        final_clip = result_video.set_audio(result_audio)

        # 要这样设置 否则无声
        final_clip.write_videofile(output_video_filename,
                                   codec='libx264',
                                   audio_codec='aac',
                                   temp_audiofile=output_video_filename + '_temp-audio.m4a',
                                   threads=4,
                                   remove_temp=True
                                   )
        #删除音频文件
        for i in temp:
            self.clear(i)

    def get_movie_frames(self, cover_video_filename, time, output_cover_filename, title =None,color='white'):
        """
        获取某一帧保存为图片
        :param cover_video_filename:
        :param seconds:  '00:00:03'
        :param output_image_filename:
        :return:
        """

        self.makedirs(output_cover_filename)

        video = VideoFileClip(cover_video_filename)

        w, h = 1280, 720
        ww, hh = 16, 9

        # if ratio == 1:
        #     w, h = 720, 1280
        #     ww, hh = 9, 16

        crop_size = 2

        bc_args = {'height': h}
        clip_args = {'width': w}
        center = {'x_center': w / 2}

        if video.w / video.h < ww / hh:
            bc_args, clip_args = clip_args, bc_args
            center = {'y_center': h / 2}


        # 比例
        sub_video_clip = video.resize(**clip_args).crop(x1=crop_size, width=w - crop_size * 2,
                                                                 y1=crop_size, height=h - crop_size * 2).margin(
            crop_size,
            color=(0, 0, 0))


        v_list = [video]

        if title:
            txt_clip = TextClip(title, font=TITLE_FONT, fontsize=100, color='white')
            title = txt_clip.set_position(('center', int(video.h/8))).set_duration(video.duration)
            v_list.append(title)

        fina = CompositeVideoClip(v_list)

        fina.save_frame(output_cover_filename, t=time)

        return output_cover_filename

    def rows_for_cover(self, input_cover_filename, output_cover_dir, image_style ="png", count=3):
        """
        将一个图片分割为3份 一行三份的样式视频用此方法 九宫格另写吧
        :param output_cover_filename:
        :param count:
        :return:
        """

        print(image_style)
        from PIL import Image

        image = Image.open(input_cover_filename)
        width, height = image.size
        item_width = int(width / count)
        item_height = height

        output_cover_dir_data = []
        for i in range(0, count):
            box = (i * item_width, 0, (i + 1) * item_width, item_height)

            print(image_style)
            image_filename = '{}/{}.{}'.format(output_cover_dir, (i + 1),image_style)
            print(image_filename)
            self.makedirs(image_filename)
            output_cover_dir_data.append(image_filename)

            image.crop(box).save(image_filename)


        return  output_cover_dir_data


    def cut_audio(self, input_video_filename, start, end, output_video_filename):

        audio = AudioFileClip(input_video_filename).subclip(start, end)

        audio.write_audiofile(output_video_filename)
        audio.close()


    def cut_video(self, input_video_filename, start, end, output_video_filename,crop_size = 0):

        """
        长视频 切成短 视频
        :param input_video_path:
        :param output_video_path:
        :param title:
        :return:
        """

        video_clip = VideoFileClip(input_video_filename).subclip(start, end)
        # duration_video_clip = video_clip.duration
        video_audio = video_clip.audio

        # 获取视频音频
        # path_audio1 = self.get_audio_from_video(input_video_filename)
        # audio_video1 = AudioFileClip(path_audio1)

        video = CompositeVideoClip([video_clip])


        video = video.fx(vfx.crop,  x2=video.w,  width=video.w,
                        y2=video.h-850, height=video.h-crop_size)



        final_clip = video.set_audio(video_audio)

        self.makedirs(output_video_filename)

        # 要这样设置 否则无声
        final_clip.write_videofile(output_video_filename,
                                   codec='libx264',
                                   audio_codec='aac',
                                   temp_audiofile=input_video_filename + '_temp-audio.m4a',
                                   remove_temp=True
                                   )
        final_clip.close()

        return output_video_filename

    def make_new_video(self, data,callback=None):

        print(data)
        input_video_filename = data.get("input_video_filename", None)
        output_video_filename = "{}/{}".format(data.get("output_video_filename", None), data.get("video_name", None))

        start = int(data.get("start", 0))
        end = int(data.get("end", None))
        title = data.get("title", None)
        subtitle = data.get("subtitle", None)
        background = data.get("background", None)
        cover = data.get("cover", None)

        colorx = data.get("colorx", 1.2)
        blackwhite = data.get("blackwhite", None)
        speedx = data.get("speedx", 1.1)

        src_volume = data.get("src_volume", None)
        dst_volume = data.get("dst_volume", None)/10
        bgm_filename = data.get("bgm_filename", None)

        pos = data.get("pos", 0)
        ratio = data.get("ratio", 0)

        opacity = data.get("opacity", 0.5)
        watermark = data.get("watermark", None)

        pos_list = [("left", "top"), ("left", "bottom"), ("right", "top"), ("right", "bottom")]



        video_clip = VideoFileClip(input_video_filename) #.fx(vfx.speedx, speedx)


        # 获取视频音频 视频可能没声音 需要特殊处理
        audio_filename = self.get_audio_from_video(input_video_filename)
        audio_clip = AudioFileClip(audio_filename)


        # 如果时间不够就循环
        times_duration = end - start + 1
        # video_clip = video_clip.fx(vfx.loop, duration=times_duration)
        audio_clip = audio_clip.fx(afx.audio_loop, duration=times_duration)
        #


        # 截取视频和音频
        if end != None:
            sub_video_clip = video_clip.subclip(start, end)
            sub_audio_clip = audio_clip.subclip(start, end)

        duration_audio_clip = sub_audio_clip.duration
        duration_video_clip = sub_video_clip.duration

        #print(duration_audio_clip,duration_video_clip)

        w, h = 1280, 720
        ww,hh = 16,9

        if ratio == 1:
            w, h =  720,1280
            ww, hh = 9, 16

        crop_size = 2

        bc_args = {'height': h}
        clip_args = {'width': w}
        center = {'x_center': w / 2}

        if sub_video_clip.w / sub_video_clip.h < ww / hh:
            bc_args, clip_args = clip_args, bc_args
            center = {'y_center': h / 2}

        # 黑色背景
        bgVideo = ColorClip((w, h), color=(220, 20, 60)).resize(**bc_args).crop(**center, **clip_args).set_duration(
            duration_video_clip).set_fps(10)

        # 比例
        # sub_video_clip = sub_video_clip.resize(**clip_args).crop(x1=crop_size, width=w - crop_size * 2,
        #                                                          y1=crop_size, height=h - crop_size * 2).margin(
        #     crop_size,
        #     color=(0, 0, 0))

        # 背景音乐
        if bgm_filename:

            bgm = AudioFileClip(bgm_filename)  # .fx(vfx.speedx, speedx)
            sub_bgm_clip = bgm.subclip(start, end)

            # 背景音乐 混合原声
            sub_audio_clip = CompositeAudioClip([
                sub_audio_clip.volumex(src_volume),
                sub_bgm_clip.volumex(dst_volume)
            ])



        # 正文视频根据背景视频大小缩放
        # it can hangs when resize movie
        video_clip_resize = sub_video_clip.resize(newsize=(int(bgVideo.w), int(bgVideo.h * (bgVideo.w/sub_video_clip.w))))

        # video_clip_resize = VideoFileClip(input_video_filename,
        #                                   verbose=True,
        #                                   target_resolution=[int(bgVideo.h * 0.75), int(bgVideo.w)])


        clip_list = [bgVideo,video_clip_resize.set_pos("center")]
        if title :
            txt_clip = TextClip(title, font=TITLE_FONT, fontsize=70, color='white')
            title = txt_clip.set_position(('center', 'top')).set_duration(duration_video_clip)
            #title = txt_clip.set_position(lambda t: ('center', 50 + t)).set_duration(duration_video_clip)
            #title = txt_clip.set_position((0.1,0.2), relative=True).set_duration(duration_video_clip)
            clip_list.append(title)

        # 如果有字幕
        if subtitle :
            generator = lambda txt: TextClip(txt, font=SUBTITLE_FONT, fontsize=36, color='white')
            subtitles = (SubtitlesClip(subtitle, generator).set_position(('center', 'bottom')))
            #subtitles = (SubtitlesClip(subtitle, generator).set_position((0.1,0.7), relative=True))
            clip_list.append(subtitles)

        # 如果有logo
        if watermark:
            logo = (ImageClip(watermark)
                    .set_duration(duration_video_clip)  # 水印持续时间
                    .resize(height=200)  # 水印的高度，会等比缩放
                    #.margin(left=8, right=8, top=8, bottom=8, opacity=opacity)  # 水印边距和透明度
                    .set_position((0.35,0.05), relative=True))  # 水印的位置
            clip_list.append(logo)


        video = CompositeVideoClip(clip_list)

        final_clip = video.set_audio(sub_audio_clip)

        final_clip = final_clip.fx(vfx.colorx, colorx)

        if blackwhite == 2:  # 选中
            final_clip = final_clip.fx(vfx.blackwhite)

        temp_audiofile = "{}_{}".format(output_video_filename, 'temp-audio.m4a')

        self.makedirs(output_video_filename)

        if callback:
            final_clip.write_videofile(output_video_filename,
                                       codec='libx264',
                                       audio_codec='aac',
                                       temp_audiofile=temp_audiofile,
                                       threads=4,
                                       remove_temp=True,
                                       verbose = False,
                                       logger=callback
                                       )
        else:
            final_clip.write_videofile(output_video_filename,
                                       codec='libx264',
                                       audio_codec='aac',
                                       temp_audiofile=temp_audiofile,
                                       threads=4,
                                       remove_temp=True
                                       )
        self.clear(audio_filename)
        final_clip.close()



    def subtitle(self,input_movie_filename, srt_filename,text):

        self.makedirs(srt_filename)
        inx = 0
        f = open(srt_filename, 'w')
        f.write('{}'.format(inx))
        f.write('\n')

        end = self.get_video_time(input_movie_filename)

        f.write("00:00:00,000" + " --> " +  end + ",000")

        f.write('\n')
        f.write(text)
        f.write('\n\n')


