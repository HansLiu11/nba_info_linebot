import json
import os
from linebot.models.messages import StickerMessage
from linebot.models.send_messages import ImageSendMessage
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date, timedelta, timezone
import pytz

from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, MessageTemplateAction, ButtonsTemplate, URITemplateAction, FlexSendMessage
from linebot.models.template import CarouselColumn, ImageCarouselColumn, ImageCarouselTemplate

load_dotenv()
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
print(channel_access_token)
line_bot_api = LineBotApi(channel_access_token)
headers  = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
}

def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def push_text_message(uid, message):
    line_bot_api.push_message(uid, TextSendMessage(text=message))
    
    return "OK"

def send_sticker(uid, pid, sid):
    line_bot_api.push_message(uid, StickerMessage(package_id=pid, sticker_id=sid))
    
    return "OK"

def send_img(reply_token, url):
    message = ImageSendMessage(
        original_content_url=url,
        preview_image_url= url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_img_carousel(uid, urls, labels, texts):
    cols = []
    for i , url in enumerate(urls):
        col = ImageCarouselColumn(
            image_url=url,
            action=MessageTemplateAction(
                label= labels[i],
                text = texts[i]
            )      
        )
        cols.append(col)
        
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=ImageCarouselTemplate(
            columns=cols
        )
    )
    line_bot_api.push_message(uid, message)  # bot 主動送訊息

def send_urlimg_carousel(uid, dicts):
    cols = []
    for i , dict in enumerate(dicts):
        col = ImageCarouselColumn(
            image_url=dict['img'],
            action=URITemplateAction(
                uri = dict['link'],
                label = dict['title'][0:11]
            )      
        )
        cols.append(col)
        
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=ImageCarouselTemplate(
            columns=cols
        )
    )
    line_bot_api.push_message(uid, message)

def send_flex_msg(reply_token,dicts):
    bubbles = []
    for dict in dicts:
        bubbles.append({
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": dict['img'],
                    "size": "5xl",
                    "aspectMode": "cover",
                    "aspectRatio": "2:3",
                    "gravity": "top"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": date.today().strftime('%Y-%m-%d'),
                            "size": "xl",
                            "color": "#ffffff",
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": dict['title'],
                            "color": "#ebebeb",
                            "size": "sm",
                            "flex": 0,
                            "wrap": True
                        }
                        ],
                        "spacing": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "filler"
                                },
                                {
                                    "type": "text",
                                    "text": "More Details",
                                    "color": "#ffffff",
                                    "flex": 0,
                                    "offsetTop": "-2px"
                                },
                                {
                                    "type": "filler"
                                }
                            ],
                            "spacing": "sm",
                            "action": {
                                "type": "uri",
                                "label": "新聞",
                                "uri": dict['link']
                            }
                        },
                        {
                            "type": "filler"
                        }
                        ],
                        "borderWidth": "1px",
                        "cornerRadius": "4px",
                        "spacing": "sm",
                        "borderColor": "#ffffff",
                        "margin": "xxl",
                        "height": "40px"
                    }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303Acc",
                    "paddingAll": "20px",
                    "paddingTop": "18px"
                },
            ],
            "paddingAll": "0px"
        }
    })
    msg = {
        "type": "carousel",
        "contents": bubbles
    }
    reply_msg = FlexSendMessage(
        alt_text='News',
        contents=msg
    )
    
    line_bot_api.reply_message(reply_token, reply_msg)


def send_menu_carousel(uid):
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://cdn.udn.com/img/480/photo/web/video/321526_78296dec11f7e28b_o.jpg',
                    title='NBA Menu1',
                    text='which would you like to watch?',
                    actions=[
                        MessageTemplateAction(
                            label='查看比分',
                            text='game scores',
                        ),
                        MessageTemplateAction(
                            label='比賽數據',
                            text='game box scores',
                        ),
                        MessageTemplateAction(
                            label='查看賽程',
                            text='game schedules',
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://cdn.udn.com/img/480/photo/web/video/321526_78296dec11f7e28b_o.jpg',
                    title='NBA Menu2',
                    text='which would you like to watch?',
                    actions=[
                        MessageTemplateAction(
                            label='戰績排名',
                            text='show standing',
                        ),
                        MessageTemplateAction(
                            label='數據排行',
                            text='show season leader',
                        ),
                        MessageTemplateAction(
                            label='NBA 新聞',
                            text='show news',
                        )
                    ]
                ),
            ]
        )
    )
    line_bot_api.push_message(uid, message)  # bot 主動送訊息

def send_button(uid, imgurl, title, discrip, texts, labels):
    acts = []
    for i, lab in enumerate(labels):
        acts.append(
            MessageTemplateAction(
                label=lab,
                text=texts[i]
            )
        )
    
    message = TemplateSendMessage(
        alt_text='Buttons Template',
        template=ButtonsTemplate(
            title=title,
            text=discrip,
            thumbnail_image_url=imgurl,
            actions=acts
        )
    )
    line_bot_api.push_message(uid, message)
     
     
def show_Games(reply_token, date:str):
    url = f"https://tw.global.nba.com/stats2/scores/daily.json?countryCode=TW&gameDate={date}&locale=zh_TW&tz=%2B8"
    
    session = requests.Session()
    response = session.get(url=url, headers=headers).json()
    date_info = response["payload"]["date"]
    nxtgamemillis = float(response["payload"]['nextAvailableDateMillis'])
    nxtgamedate = datetime.utcfromtimestamp(nxtgamemillis / 1000.)
    nxtgamedate = nxtgamedate.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Asia/Taipei'))
    
    if date_info == None:
        board = json.load(open('json/NoGame.json','r',encoding='utf-8'))
        board['body']['contents'][2]['text'] = str(nxtgamedate)[:-6]
        board['footer']['contents'][0]['action']['data'] = 'Get{}'.format(str(nxtgamedate)[:-6])
        line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果~', board))
        return
    
    bubbles = [] 
    games = date_info["games"]
    for game in games :
        board = json.load(open('json/Bubble.json','r',encoding='utf-8'))
        gstatus = game['boxscore']['statusDesc']
        
        # Get Game profile
        gameId = game['profile']['gameId']

        # Home/Away Team
        NBA_homeTeam = game['homeTeam']
        NBA_awayTeam = game['awayTeam']

        # HomeTeam - Profile
        Home_profile = NBA_homeTeam['profile']
        Home_name = Home_profile['displayAbbr']
        Home_abbr = Home_profile['abbr']
        Home_logo_url = 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Home_abbr)

        # AwayTeam - Profile
        Away_profile = NBA_awayTeam['profile']
        Away_name = Away_profile['displayAbbr']
        Away_abbr = Away_profile['abbr']
        Away_logo_url = 'https://tw.global.nba.com/media/img/teams/00/logos/{}_logo.png'.format(Away_abbr)

        # HomeTeam - matchup
        Home_matchup = NBA_homeTeam['matchup']
        Home_losses = Home_matchup['losses']
        Home_wins = Home_matchup['wins']

        # AwayTeam - matchup
        Away_matchup = NBA_awayTeam['matchup']
        Away_losses = Away_matchup['losses']
        Away_wins = Away_matchup['wins']

        
        if gstatus == "延期":
            response = json.load(open('json/Pospond.json','r',encoding='utf-8'))
            
            tm = game['profile']["dateTimeEt"]
            tm = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
            # convert ET time to Taipei time
            tm1 = tm.replace(tzinfo=timezone.utc)
            gametime = tm1.astimezone(timezone(timedelta(hours=13))).strftime("%I:%M %p")
            
            response['body']['contents'][0]['contents'][0]['contents'][1]['url'] = str(Home_logo_url)
            response['body']['contents'][0]['contents'][0]['contents'][2]['text'] = f'{Home_wins} - {Home_losses}'
            
            response['body']['contents'][0]['contents'][1]['contents'][2]['text'] = gametime

            response['body']['contents'][0]['contents'][2]['contents'][0]['contents'][1]['url'] = str(Away_logo_url)
            response['body']['contents'][0]['contents'][2]['contents'][0]['contents'][2]['text'] = f'{Away_wins} - {Away_losses}'
            
            response['footer']['contents'][0]['contents'][0]['action']['uri'] = 'https://tw.global.nba.com/preview/#!/'.format(gameId)

            bubbles.append(response)
            continue
        
        elif "ET" in gstatus:
            tm = game['profile']["dateTimeEt"]
            tm = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
            # convert ET time to Taipei time
            tm1 = tm.replace(tzinfo=timezone.utc)
            gametime = tm1.astimezone(timezone(timedelta(hours=13))).strftime("%I:%M %p")
            
            response = json.load(open('json/NotStarted.json','r',encoding='utf-8'))

            response['body']['contents'][0]['contents'][0]['contents'][1]['url'] = str(Home_logo_url)
            response['body']['contents'][0]['contents'][0]['contents'][2]['text'] = f'{Home_wins} - {Home_losses}'
            
            response['body']['contents'][0]['contents'][1]['contents'][2]['text'] = gametime

            response['body']['contents'][0]['contents'][2]['contents'][0]['contents'][1]['url'] = str(Away_logo_url)
            response['body']['contents'][0]['contents'][2]['contents'][0]['contents'][2]['text'] = f'{Away_wins} - {Away_losses}'
            
            response['footer']['contents'][0]['contents'][0]['action']['uri'] = f'https://tw.global.nba.com/preview/#!/{gameId}'

            bubbles.append(response)
            continue
        
        
        # URLs
        NBA_Hightlight = None
        NBA_Live = None
        if(len(game['urls']) > 0):
            NBA_Hightlight = game['urls'][0]['value']
            # NBA_Live = game['urls'][1]['value']

        # HomeTeam - score
        Home_score = NBA_homeTeam['score']
        Home_main_score = []
        for i in range(4):
            Home_main_score.append(Home_score['q{}Score'.format(i+1)])
        for i in range(10):
            Home_main_score.append(Home_score['ot{}Score'.format(i+1)])
        
        Home_totScore = Home_score['score']

        # Home - pointGameLeader
        Home_pointGameLeader = NBA_homeTeam['pointGameLeader']
        Home_pointGameLeader_Name = Home_pointGameLeader['profile']['displayName']
        Home_pointGameLeader_Points = Home_pointGameLeader['statTotal']['points']

        # Home - assistGameLeader
        Home_assistGameLeader = NBA_homeTeam['assistGameLeader']
        Home_assistGameLeader_Name = Home_assistGameLeader['profile']['displayName']
        Home_assistGameLeader_Assists = Home_assistGameLeader['statTotal']['assists']

        # Home - reboundGameLeader
        Home_reboundGameLeader = NBA_homeTeam['reboundGameLeader']
        Home_reboundGameLeader_Name = Home_reboundGameLeader['profile']['displayName']
        Home_reboundGameLeader_Rebs = Home_reboundGameLeader['statTotal']['rebs']

        # AwayTeam - score
        Away_score = NBA_awayTeam['score']
        Away_main_score = []
        for i in range(4):
            Away_main_score.append(Away_score['q{}Score'.format(i+1)])
        for i in range(10):
            Away_main_score.append(Away_score['ot{}Score'.format(i+1)])
        Away_totScore = Away_score['score']

        # Away - pointGameLeader
        Away_pointGameLeader = NBA_awayTeam['pointGameLeader']
        Away_pointGameLeader_Name = Away_pointGameLeader['profile']['displayName']
        Away_pointGameLeader_Points = Away_pointGameLeader['statTotal']['points']

        # Away - assistGameLeader
        Away_assistGameLeader = NBA_awayTeam['assistGameLeader']
        Away_assistGameLeader_Name = Away_assistGameLeader['profile']['displayName']
        Away_assistGameLeader_Assists = Away_assistGameLeader['statTotal']['assists']

        # Away - reboundGameLeader
        Away_reboundGameLeader = NBA_awayTeam['reboundGameLeader']
        Away_reboundGameLeader_Name = Away_reboundGameLeader['profile']['displayName']
        Away_reboundGameLeader_Rebs = Away_reboundGameLeader['statTotal']['rebs']

        # Set HomeTeam Bubble
        board['body']['contents'][0]['contents'][0]['contents'][1]['url'] = str(Home_logo_url)
        board['body']['contents'][0]['contents'][0]['contents'][2]['text'] = f'{Home_wins} - {Home_losses}'

        # Set Total Score
        board['body']['contents'][0]['contents'][1]['contents'][2]['text'] = str(Home_totScore)
        board['body']['contents'][0]['contents'][2]['contents'][2]['text'] = str(Away_totScore)

        # Set AwayTeam board
        board['body']['contents'][0]['contents'][3]['contents'][0]['contents'][1]['url'] = str(Away_logo_url)
        board['body']['contents'][0]['contents'][3]['contents'][0]['contents'][2]['text'] = f'{Away_wins} - {Away_losses}'

        # Set Name
        board['body']['contents'][2]['contents'][0]['contents'][1]['text'] = Home_name
        board['body']['contents'][2]['contents'][0]['contents'][2]['text'] = Away_name

        # Set Scores
        for i in range(4):
            Score = json.load(open('json/Score.json','r',encoding='utf-8'))
            Score['contents'][0]['text'] = '第{}局'.format(i+1)
            Score['contents'][1]['text'] = str(Home_main_score[i])
            Score['contents'][2]['text'] = str(Away_main_score[i])
            board['body']['contents'][2]['contents'].append(Score)
        for i in range(4,14):
            if(Home_main_score[i] == 0 and Away_main_score[i] == 0):
                break
            else:
                Score = json.load(open('json/Score.json','r',encoding='utf-8'))
                Score['contents'][0]['text'] = 'OT{}'.format(i-4)
                Score['contents'][1]['text'] = str(Home_main_score[i])
                Score['contents'][2]['text'] = str(Away_main_score[i])
                board['body']['contents'][2]['contents'].append(Score)

        # Set URLs
        if(NBA_Live is not None):
            Buttom = json.load(open('json/Buttom.json','r',encoding='utf-8'))
            Buttom['contents'][0]['action']['label'] = '收看直播'
            Buttom['contents'][0]['action']['uri'] = str(NBA_Live)
            board['footer']['contents'].append(Buttom)
        if(gameId is not None):
            Buttom = json.load(open('json/Buttom.json','r',encoding='utf-8'))
            Buttom['contents'][0]['action']['label'] = '數據統計'
            Buttom['contents'][0]['action']['uri'] = f'https://tw.global.nba.com/boxscore/#!/{gameId}'
            board['footer']['contents'].append(Buttom)
        if(NBA_Hightlight is not None):
            Buttom = json.load(open('json/Buttom.json','r',encoding='utf-8'))
            Buttom['contents'][0]['action']['label'] = 'Hightlights'
            Buttom['contents'][0]['action']['uri'] = str(NBA_Hightlight)
            board['footer']['contents'].append(Buttom)
        
        bubbles.append(board)
        # break
    # print (bubbles)
            
    msg = {
        "type": "carousel",
        "contents": bubbles
    }
    reply_msg = FlexSendMessage(
        alt_text='查詢結果~',
        contents=msg
    )
    
    line_bot_api.reply_message(reply_token, reply_msg)
    return "OK"

def show_tmw_schedule(reply_token):
    
    url = "https://tw.global.nba.com/stats2/season/schedule.json?countryCode=TW&days=2&locale=zh_TW&tz=%2B8"
    
    session = requests.Session()
    response = session.get(url=url, headers=headers).json()
        
    dates = response["payload"]["dates"]
    for i in range(len(dates)):
        games = dates[i]["games"]
        tomorrow = games[0]['profile']["dateTimeEt"].split("T")[0]
        gamedate = datetime.strptime(tomorrow,"%Y-%m-%d")
        gamedate = (gamedate + timedelta(1)).strftime('%Y-%m-%d')
        # tomorrow = tomorrow.replace("-","/")
        result = ""
        result += (f"\U0001f4c6 {gamedate} \n\n")
        if len(games) == 0:
            result += "\U0000274c No scheduled games"
        else:
            for game in games :
                gstatus = game['boxscore']['statusDesc']
                if gstatus != "延期":
                    tm = game['profile']["dateTimeEt"]
                    tm = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
                    # convert ET time to Taipei time
                    tm1 = tm.replace(tzinfo=timezone.utc)
                    gametime = tm1.astimezone(timezone(timedelta(hours=13))).strftime("%I:%M %p")
                    
                    hometeam = game['homeTeam']['profile']["nameEn"]
                    
                    awayteam = game['awayTeam']['profile']["nameEn"]
                    
                    result += (f"\U000023f0 {gametime}\n")
                    result += (f"\U00002694 {hometeam} vs {awayteam}\n\n")
            
            result += "Pospond: "         
            for game in games:
                gstatus = game['boxscore']['statusDesc']
                if gstatus == "延期":
                    hometeam = game['homeTeam']['teamName']
                    awayteam = game['awayTeam']['teamName']
                    result += (f"\n\U00002694 {hometeam} V.S. {awayteam}")
        
        send_text_message(reply_token,result)
    return "OK"

def show_standings(uid):
    url = "https://tw.global.nba.com/stats2/season/conferencestanding.json?locale=zh_TW"
    
    session = requests.Session()
    # response = requests.get(url=url, headers=headers).json()
    response = session.get(url=url, headers=headers).json()
    Eteams = response["payload"]["standingGroups"][0]["teams"]
    Wteams = response["payload"]["standingGroups"][1]["teams"]
    Eteams_rank = {}
    Wteams_rank = {}
    resultE = '\U0001F4E2\U0001F4E2\U0001F4E2 Eastern Conference\n\n'
    resultW = '\U0001F4E2\U0001F4E2\U0001F4E2 Western Conference\n\n'
    for team in Eteams:
        conf = response["payload"]["standingGroups"][0]["displayConference"]
        tname = team["profile"]["cityEn"] + " " + team["profile"]["nameEn"]
        wins = team["standings"]["wins"]
        losses = team["standings"]["losses"]
        winp = team["standings"]["winPct"]
        rank = team["standings"]["confRank"]
        gb = team["standings"]["confGamesBehind"]

        Eteams_rank[rank] = [conf, tname, wins, losses, winp, gb]
        
    for team in Wteams:
        conf = response["payload"]["standingGroups"][0]["displayConference"]
        tname = team["profile"]["cityEn"] + " " + team["profile"]["nameEn"]
        wins = team["standings"]["wins"]
        losses = team["standings"]["losses"]
        winp = team["standings"]["winPct"]
        rank = team["standings"]["confRank"]
        gb = team["standings"]["confGamesBehind"]

        Wteams_rank[rank] = [conf, tname, wins, losses, winp, gb]
        
    for rank in range(1,len(Eteams_rank)+1):
        team = Eteams_rank[rank]
        if(rank == 1):
            resultE += ("\U0001F947 {}({})\n" .format(team[1],rank))
        elif(rank == 2):
            resultE += ("\U0001F948 {}({})\n" .format(team[1],rank))
        elif(rank == 3):
            resultE += ("\U0001F949 {}({})\n" .format(team[1],rank))
        elif(rank > 3 and rank < 9):
            resultE += ("\U0001f3c5 {}({})\n" .format(team[1],rank))
        else:
            resultE += ("\U00002716 {}({})\n" .format(team[1],rank))

        resultE += (f"{team[2]} W, {team[3]} L, {team[4]} W/L%, {team[5]} GB\n")
    
    for rank in range(1,len(Eteams_rank)+1):
        team = Wteams_rank[rank]
        if(rank == 1):
            resultW += ("\U0001F947 {}({})\n" .format(team[1],rank))
        elif(rank == 2):
            resultW += ("\U0001F948 {}({})\n" .format(team[1],rank))
        elif(rank == 3):
            resultW += ("\U0001F949 {}({})\n" .format(team[1],rank))
        elif(rank > 3 and rank < 9):
            resultW += ("\U0001f3c5 {}({})\n" .format(team[1],rank))
        else:
            resultW += ("\U00002716 {}({})\n" .format(team[1],rank))

        resultW += (f"{team[2]} W, {team[3]} L, {team[4]} W/L%, {team[5]} GB\n")
            
    push_text_message(uid,resultE)
    push_text_message(uid,resultW)
    
def show_boxscore(uid, dateteam):
    list = dateteam.split(" ")
    Date = datetime.strptime(list[0], "%Y-%m-%d")
    url = f"https://tw.global.nba.com/stats2/scores/daily.json?countryCode=TW&gameDate={Date}&locale=zh_TW&tz=%2B8"
    session = requests.Session()
    response = session.get(url=url, headers=headers).json()
    games = response["payload"]["date"]["games"]
    searchteam = list[1]
    for game in games:
        if game['homeTeam']['profile']["nameEn"] == searchteam or game['awayTeam']['profile']["nameEn"] == searchteam:
            gid = game['profile']['gameId']
    
    print(gid)
    
    staturl = f"https://tw.global.nba.com/stats2/game/snapshot.json?countryCode=TW&gameId={gid}&locale=zh_TW&tz=%2B"
    session = requests.Session()
    response = session.get(url=staturl, headers=headers).json()
    hm_player_stats = response["payload"]["homeTeam"]
    ay_plater_stats = response["payload"]["awayTeam"]
    if hm_player_stats['profile']["nameEn"] == searchteam:
        searchteam = hm_player_stats['profile']['cityEn'] + searchteam
        opp_team = ay_plater_stats['profile']['cityEn'] + ay_plater_stats['profile']["nameEn"]
    else:
        searchteam = ay_plater_stats['profile']['cityEn'] + searchteam
        opp_team = hm_player_stats['profile']['cityEn'] + hm_player_stats['profile']["nameEn"]
    result = ("\U0001f3c0\U0001f3c0\U0001f3c0 {}\n\n" .format(searchteam))
    result_opp = ("\U0001f3c0\U0001f3c0\U0001f3c0 {}\n\n" .format(opp_team))
    for p in hm_player_stats["gamePlayers"]:
        player = p["profile"]
        player_stat = p["statTotal"]
        result += (f"\U0001F525\U000026f9\U0001F525 {player['displayNameEn']} {player['position']} {player_stat['mins']}:{player_stat['secs']}\n")
        result += (f"{player_stat['points']} PTS, {player_stat['assists']} AST, {player_stat['rebs']} REB, {player_stat['steals']} STL, {player_stat['blocks']} BLK, {player_stat['turnovers']} TOV\n\n")
    for p in ay_plater_stats["gamePlayers"]:
        player = p["profile"]
        player_stat = p["statTotal"]
        result_opp += (f"\U0001F525\U000026f9\U0001F525 {player['displayNameEn']} {player['position']} {player_stat['mins']}:{player_stat['secs']}\n")
        result_opp += (f"{player_stat['points']} PTS, {player_stat['assists']} AST, {player_stat['rebs']} REB, {player_stat['steals']} STL, {player_stat['blocks']} BLK, {player_stat['turnovers']} TOV\n")
    push_text_message(uid, result)
    push_text_message(uid, result_opp)
    
def showStatleader(reply_token):
    url = "https://stats.nba.com/js/data/widgets/home_season.json"
    response = requests.get(url=url, headers=headers).json()
    seasonLeaders = response["items"][0]["items"]
    result = "Season Leaders\n\n"
    
    pointleaders = seasonLeaders[0]
    title = pointleaders["title"]
    result += f"\U0001f525 {title} \U0001f525\n\U0001f451 "
    for i in range(3):
        player = pointleaders["playerstats"][i]
        result += "{}  {} PTS\n".format(player['PLAYER_NAME'], player['PTS'])
    
    reboundleaders = seasonLeaders[1]
    result += f"\n\U0001f3c0 {reboundleaders['title']} \U0001f3c0\n\U0001f451 "
    for i in range(3):
        player = reboundleaders["playerstats"][i]
        result += "{}  {} REB\n".format(player['PLAYER_NAME'], player['REB'])
      
    assistleaders = seasonLeaders[2]
    result += f"\n\U0001f64c {assistleaders['title']} \U0001f64c\n\U0001f451 "
    for i in range(3):
        player = assistleaders["playerstats"][i]
        result += "{}  {} AST\n".format(player['PLAYER_NAME'], player['AST'])
        
    blockleaders = seasonLeaders[3]    
    result += f"\n\U0001f932 {blockleaders['title']} \U0001f932\n\U0001f451 "
    for i in range(3):
        player = blockleaders["playerstats"][i]
        result += "{}  {} BLK\n".format(player['PLAYER_NAME'], player['BLK']) 
        
    stealleaders = seasonLeaders[4]    
    result += f"\n\U000026f9 {stealleaders['title']} \U000026f9\n\U0001f451 "
    for i in range(3):
        player = stealleaders["playerstats"][i]
        result += "{}  {} STL\n".format(player['PLAYER_NAME'], player['STL'])
        
    threeptsleader = seasonLeaders[6]    
    result += f"\n\U0001f44c {threeptsleader['title']} \U0001f44c\n\U0001f451 "
    for i in range(3):
        player = threeptsleader["playerstats"][i]
        result += "{}  {} 3PM\n".format(player['PLAYER_NAME'], player['FG3M'])
        
    send_text_message(reply_token, result)
    
def showteamsch(reply_token, team):
    team_lw = team.lower()
    url = f"https://tw.global.nba.com/stats2/team/schedule.json?countryCode=TW&locale=zh_TW&teamCode={team_lw}"
    session = requests.Session()
    response = session.get(url=url, headers=headers).json()
    d = date.today()
    months = response["payload"]["monthGroups"]
    for m in months:
        if m["number"] == d.month:
            games = m['games']
    result = ""
    games = list(filter(lambda g:{d <= datetime.strptime(g['profile']['dateTimeEt'], '%Y-%m-%dT%H:%M').date()}, games))
    for g in games[:5] :
        gamedate = datetime.strptime(g['profile']['dateTimeEt'], '%Y-%m-%dT%H:%M').date()
        gamedate = (gamedate + timedelta(1)).strftime('%Y-%m-%d')
        result += (f"\U0001f4c6 {gamedate} \n")
        gstatus = g['boxscore']['statusDesc']
        if gstatus != "延期":
            tm = g['profile']["dateTimeEt"]
            tm = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
            # convert ET time to Taipei time
            tm1 = tm.replace(tzinfo=timezone.utc)
            gametime = tm1.astimezone(timezone(timedelta(hours=13))).strftime("%I:%M %p")
            
            hometeam = g['homeTeam']['profile']["nameEn"]
            awayteam = g['awayTeam']['profile']["nameEn"]
            
            result += (f"\U000023f0 {gametime}\n")
            if hometeam == team: 
                result += (f"\U00002694 {team} vs {awayteam}\n\n")
            else:
                result += (f"\U00002694 {team} vs {hometeam}\n\n")

    send_text_message(reply_token,result)
    return "OK"
    
def shownews(reply_token):
    nba_news = []
    url = "https://nba.udn.com/nba/news/"
    session = requests.Session()
    response = session.get(url=url)
    sp = BeautifulSoup(response.text, 'html.parser')   
    out = sp.find(id="news_list_body").find('dl')
    newses = out.find_all('a')
    for news in newses:
        link = "https://nba.udn.com" + news.get("href")
        title = news.find("h3").text
        img = news.find('img')['data-src']
        x=['title','link','img']
        dictionary = dict(zip(x,[title,link,img]))
        nba_news.append(dictionary)
    
    send_flex_msg(reply_token,nba_news)
    # print(nba_news)
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
