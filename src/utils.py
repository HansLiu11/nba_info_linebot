import os
from linebot.models.messages import StickerMessage
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date, timedelta, timezone

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
                            "text": "2021/01/01",
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
                            label='Game Scores',
                            text='game scores',
                        ),
                        MessageTemplateAction(
                            label='Game BoxScores',
                            text='game box scores',
                        ),
                        MessageTemplateAction(
                            label='Game Schedule',
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
                            label='Standing',
                            text='show standing',
                        ),
                        MessageTemplateAction(
                            label='Stats Leader',
                            text='show season leader',
                        ),
                        MessageTemplateAction(
                            label='NBA News',
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
     
     
def show_todayGame(reply_token):
    url = "https://tw.global.nba.com/stats2/scores/daily.json?countryCode=TW&locale=zh_TW&tz=%2B8"
    
    session = requests.Session()
    response = session.get(url=url, headers=headers).json()
    games = response["payload"]["date"]["games"]
    today = date.today().strftime("%Y/%m/%d")
    result = ""
    result += (f"\U0001f4c6 {today} \n\n")
    if len(games) == 0:
        result += "\U0000274c No games today"
    
    for game in games :
        gstatus = game['boxscore']['statusDesc']
        if gstatus == "結束":
            homeScore = game['boxscore']['homeScore']
            awayScore = game['boxscore']['awayScore']
            if homeScore > awayScore:
                winteam = game['homeTeam']['profile']["nameEn"]
                loseteam = game['awayTeam']['profile']["nameEn"]
                result += ("\U0001f3c6 {} \U0001f3c0 {}\n".format(winteam,homeScore))
                result += ("\U0001f62d {} \U0001f3c0 {}\n\n".format(loseteam,awayScore))
            else:
                loseteam = game['homeTeam']['profile']["nameEn"]
                winteam = game['awayTeam']['profile']["nameEn"]
                result += ("\U0001f3c6 {} \U0001f3c0 {}\n".format(winteam,awayScore))
                result += ("\U0001f62d {} \U0001f3c0 {}\n\n".format(loseteam,homeScore))
        elif "ET" in gstatus:
            tm = game['profile']["dateTimeEt"]
            tm = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
            # convert ET time to Taipei time
            tm1 = tm.replace(tzinfo=timezone.utc)
            gametime = tm1.astimezone(timezone(timedelta(hours=13))).strftime("%I:%M %p")
            hometeam = game['homeTeam']['profile']["nameEn"]
            awayteam = game['awayTeam']['profile']["nameEn"]
            result += (f"\U00002694 {hometeam} vs {awayteam}\n")
            result += (f"\U000023f0 {gametime}\n\n")
            
        else:
            homeScore = game['boxscore']['homeScore']
            awayScore = game['boxscore']['awayScore']
            hometeam = game['homeTeam']['profile']["nameEn"]
            awayteam = game['awayTeam']['profile']["nameEn"]
            retime = game['boxscore']['periodClock']
            result += (f"\U0001f525 {gstatus} {retime}\n")
            result += ("{} \U0001f3c0 {}\n".format(hometeam,homeScore))
            result += ("{} \U0001f3c0 {}\n\n".format(awayteam,awayScore))
            

    result += "Pospond: "         
    for game in games:
        gstatus = game['boxscore']['statusDesc']
        if gstatus == "延期":
            hometeam = game['homeTeam']['profile']["nameEn"]
            awayteam = game['awayTeam']['profile']["nameEn"]
            result += (f"\n\U00002694 {hometeam} V.S. {awayteam}")
            
        
    # gamescore = scoreboard.ScoreBoard().games.get_dict()
    send_text_message(reply_token,result)
    return "OK"

def show_Games(reply_token, date:str):
    # gamedate = datetime.strptime(date,"%Y-%m-%d")
    # gamedate = (gamedate - timedelta(1)).strftime('%Y-%m-%d')
    url = f"https://tw.global.nba.com/stats2/scores/daily.json?countryCode=TW&gameDate={date}&locale=zh_TW&tz=%2B8"
    session = requests.Session()
    response = session.get(url=url, headers=headers).json()
    games = response["payload"]["date"]["games"]
    date = date.replace("-","/")
    result = ""
    result += (f"\U0001f4c6 {date} \n\n")
    if len(games) == 0:
        result += "\U0000274c No scheduled games"
    
    for game in games :
        gstatus = game['boxscore']['statusDesc']
        if gstatus == "結束":
            homeScore = game['boxscore']['homeScore']
            awayScore = game['boxscore']['awayScore']
            if homeScore > awayScore:
                winteam = game['homeTeam']['profile']["nameEn"]
                loseteam = game['awayTeam']['profile']["nameEn"]
                result += ("\U0001f3c6 {} \U0001f3c0 {}\n".format(winteam,homeScore))
                result += ("\U0001f62d {} \U0001f3c0 {}\n".format(loseteam,awayScore))
            else:
                loseteam = game['homeTeam']['profile']["nameEn"]
                winteam = game['awayTeam']['profile']["nameEn"]
                result += ("\U0001f3c6 {} \U0001f3c0 {}\n".format(winteam,awayScore))
                result += ("\U0001f62d {} \U0001f3c0 {}\n".format(loseteam,homeScore))
            if len(game['urls']) > 0:
                url = game['urls'][0]["value"]
                result += "Highlights : " + url + "\n\n"
            else:
                result += "\n"
    
    result += "Pospond: "         
    for game in games:
        gstatus = game['boxscore']['statusDesc']
        if gstatus == "延期":
            hometeam = game['homeTeam']['profile']["nameEn"]
            awayteam = game['awayTeam']['profile']["nameEn"]
            result += (f"\n\U00002694 {hometeam} V.S. {awayteam}")
    
    send_text_message(reply_token,result)
    return "OK"

def show_tmw_schedule(uid):
    
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
        
        push_text_message(uid,result)
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
    
def showStatleader(uid):
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
        
    push_text_message(uid, result)
    
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
