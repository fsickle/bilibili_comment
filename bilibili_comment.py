# -*- coding: utf-8 -*-
import requests, time, numpy

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def get_videos_nums(mid):
    # 获取视频数
    videos_url = "https://space.bilibili.com/ajax/member/"\
        "getSubmitVideos?mid={}&page=1&pagesize=1".format(mid)
    response = requests.get(videos_url, headers=headers)
    
    try:
        resp_json = response.json()
    except ValueError:
        print("json 解析失败：{}".format(response.text))
    else:
        return resp_json['data']['count']
    return None
    
def get_video_aid_title(mid):
    # 获取视频的av号和标题
    videos_url = "https://space.bilibili.com/ajax/member/"\
        "getSubmitVideos?mid={}&page=1&pagesize=1".format(mid)
    response = requests.get(videos_url, headers=headers)
    response.raise_for_status()
    response.encoding = 'utf-8'
    
    try:
        resp_json = response.json()
    except ValueError:
        print("json 解析失败：{}".format(response.text))
    else:
        aid = resp_json['data']['vlist'][0]['aid']
        title = resp_json['data']['vlist'][0]['title']
        return aid, title
    return None
    
def get_video_reply(aid):
    # reply numbers
    reply_url = "https://api.bilibili.com/x/web-interface/"\
        "archive/stat?aid={}".format(aid)
    response = requests.get(reply_url, headers=headers)
    
    try:
        resp_json = response.json()
    except ValueError:
        print("json 解析失败：{}".format(response.text))
    else:
        return resp_json['data']['reply']
    return None
    
       
def post_comment(aid, message):
    # 提交评论
    reply_url = "https://api.bilibili.com/x/v2/reply/add"
    cookie = {
        "DedeUserID":a,#用户ID
        "DedeUserID__ckMd5":b,#用户ID_MD5值
        "SESSDATA":c,#会话cookie
        "bili_jct":d,#crsf cookie
    }
    request_headers = {
        "Cookie": "DedeUserID={a}; "
                  "DedeUserID__ckMd5={b}; "
                  "SESSDATA={c}; "
                  "bili_jct={d}; ".format(a=cookie["DedeUserID"],
                                          b=cookie["DedeUserID__ckMd5"],
                                          c=cookie["SESSDATA"],
                                          d=cookie['bili_jct']),
        "User-Agent": "Mozilla/5.0",
    }
    form_data = {
        "csrf":	cookie['bili_jct'],
        "jsonp": "jsonp",
        "message": message,
        "oid": aid,
        "plat":	1,
        "type":	1,
    }
    
    try:
        response = requests.post(reply_url, headers=request_headers,
            data=form_data)
        resp_json = response.json()
    except ValueError:
        print("json 解析失败")
    else:
        if resp_json.get('code', None) is not None:
            if resp_json['code'] == 0:
                print("评论成功：{}".format(message))
                return True
            else:
                print("评论失败：{}".format(message))
        else:
            print("json 格式错误")
    return False
    
if __name__ == '__main__':
    a = input('DedeUserID:(include "")')
    b = input('DedeUserID__ckMd5:(include "")')
    c = input('SESSDATA:(include "")')
    d = input('bili_jct:(include "")')
    mid = input('Up ID:')
    message = input('评论内容(在3到1000字符内)：')
    reply_where = input('期望的评论层数:')
    
    print('running')
    try:
        current_videos_num = get_videos_nums(mid)
        target_num = current_videos_num + 1
        while target_num != get_videos_nums(mid):
            time.sleep(numpy.random.rand())  # 访问时间间隔（秒）
        aid, title = get_video_aid_title(mid)
        print('title: %s' % title)
        reply_num = get_video_reply(aid)
        if reply_num == str(int(reply_where)-1):
            post_comment(aid, message)
        if post_comment(aid, message):
            print("视频{}评论成功".format(title))
        else:
            print("视频{}评论失败".format(title))
    except requests.HTTPError:
        print("网络错误")
        
        
        
