import requests
import os

def getAvailableServer(serverList):
    availableList = []
    for i in serverList:
        ret = os.system('ping {} -w 1'.format(i))
        if ret == 0:
            availableList.append(i)

    return availableList

def getRequestsSession(UA=''):
    if UA == '':
        UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

    headers = {
        'Connection': 'close',
        'User-Agent': UA,
        'Host': 'cbiz.yanhekt.cn',
        'Origin': 'https://www.yanhekt.cn',
        'Referer': 'https://www.yanhekt.cn/',
        'Xdomain-Client': 'web_user',
    }

    session = requests.Session()
    session.headers.update(headers)
    session.trust_env = False

    return session

def getLessonInfo(course_id, session):
    url = 'https://cbiz.yanhekt.cn/v1/course?id={}&with_professor_badges=true'.format(course_id)

    res = session.get(url)
    if res.status_code != 200:
        print('[getClassInfo] GET error: {}'.format(res.status_code))
        return None

    res_json = res.json()
    
    data = res_json['data']

    lessonInfo = {
        'id': data['id'],
        'name_zh': data['name_zh'],
        'name_en': data['name_en'],
        'code': data['code'],
        'type_name': data['type_name'],
        'school_year': data['school_year'],
        'semester': data['semester'],
        'college_name': data['college_name'],
        'professors': [i['name'] for i in data['professors']],
    }

    return lessonInfo

def getVideoList(course_id, session):
    url = 'https://cbiz.yanhekt.cn/v2/course/session/list?course_id={}'.format(course_id)

    res = session.get(url)
    if res.status_code != 200:
        print('[getVideoList] GET error: {}'.format(res.status_code))
        return None

    res_json = res.json()

    videoList = {}
    
    for i in res_json['data']:
        main_url = i['videos'][0]['main'].replace('https://cvideo.yanhekt.cn','')
        vga_url = i['videos'][0]['vga'].replace('https://cvideo.yanhekt.cn','')
        date_split = i['title'].split(' ')
        date = date_split[0] + ' ' + date_split[1]
        if not videoList.get(date + ' main') or videoList[date + ' main'] == '':
            videoList[date + ' main'] = main_url
        if not videoList.get(date + ' vga') or videoList[date + ' vga'] == '':
            videoList[date + ' vga'] = vga_url

    return videoList

def main(course_id, corePath, workDir):
    session = getRequestsSession()
    if session is None:
        print('Cant get requests session!')
        return

    serverList = getAvailableServer(['yanhe{}.bit.edu.cn'.format(i) for i in range(2,13)])
    if len(serverList) == 0:
        print('Cant download video by server list!')
        return
    else:
        print('Available Server List: ' + serverList)

    lessonInfo = getLessonInfo(course_id, session)
    if len(lessonInfo) == 0:
        print('Cant download lesson information!')
        return
    else:
        print(lessonInfo)
    
    if lessonInfo['name_en'] != '':
        workDir = workDir + lessonInfo['name_en']
    else:
        print('Cant get English name, but the process is going on!')
        workDir = workDir + str(course_id)
    
    os.makedirs(workDir, exist_ok=True)

    videoList = getVideoList(course_id, session)
    if len(videoList) == 0:
        print('Cant get video list!')
        return
    videoKeyList = list(videoList.keys())

    os.system('pause')

    failedList = []
    for idx in videoKeyList:
        videoInfo = videoList[idx]
        if videoInfo != '':
            ret = 1
            for server in serverList:
                url = 'http://' + server + videoInfo
                cmd = '{} "{}" --workDir "{}" --saveName "{}" '.format(
                    corePath,
                    url,
                    workDir,
                    idx
                )
                cmd += '--retryCount "3" --enableDelAfterDone --disableDateInfo --noProxy'
                ret = os.system(cmd)
            if ret != 0:
                failedList.append(idx)
    
    if len(failedList) != 0:
        print('Failed to download videos as follows:')
        pprint(failedList)
    

if __name__ == '__main__':
    course_id = 20854
    corePath = 'N_m3u8DL-CLI_v2.9.9.exe'
    workDir = os.path.join('D:/Downloads/')

    main(course_id, corePath, workDir)

    print('======================== Task Finish ========================')