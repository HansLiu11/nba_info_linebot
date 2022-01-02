from typing import Text
from numpy import trunc
from transitions.extensions import GraphMachine
import time
from datetime import datetime, timedelta

from utils import push_text_message, send_img_carousel, send_sticker, send_text_message, send_menu_carousel, send_button, show_Games, show_boxscore, show_standings, show_tmw_schedule, showStatleader, shownews, showteamsch


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_lobby(self, event):
        text = event.message.text
        return True
    
    def is_going_to_gameScores(self, event):
        text = event.message.text
        return text.lower() == "game scores"
    
    def is_going_to_todayGame(self, event):
        text = event.message.text
        return text.lower() == "today game"
    
    def is_going_to_yesterdayGame(self, event):
        text = event.message.text
        return text.lower() == "yesterday game"
    
    def is_going_to_otherGame(self, event):
        text = event.message.text
        return text.lower() == "other game"
    
    def is_going_to_showotherGame(self, event):
        return True

    def is_going_to_gameSchedule(self, event):
        text = event.message.text
        return text.lower() == "game schedules"
    
    def is_going_to_showSchedule(self, event):
        text = event.message.text
        return text.lower() == "show game schedule"
    
    def is_going_to_boxScores(self, event):
        text = event.message.text
        return text.lower() == "game box scores"
    
    def is_going_to_boxfromgame(self,event):
        text = event.message.text
        return text.lower() == "watch game result"

    def is_going_to_showBoxscores(self, event):
        text = event.message.text
        return True
    
    def is_going_to_showStanding(self, event):
        text = event.message.text
        return text.lower() == "show standing"
    
    def is_going_to_statLeader(self, event):
        text = event.message.text
        return text.lower() == "show season leader"
    
    def is_going_to_showNews(self, event):
        text = event.message.text
        return text.lower() == "t86"
    
    def is_going_to_searchTeamsch(self, event):
        text = event.message.text
        return text.lower() == "search team schedule" 
    
    def is_going_to_showTeamsch(self, event):
        text = event.message.text
        return True
    
    def is_going_to_backLobby(self, event):
        text = event.message.text
        return text.lower() == "go back to menu"
    
    def is_going_to_backotherGame(self, event):
        text = event.message.text
        return text.lower() == "go back"

    def on_enter_lobby(self, event):
        print("I'm entering lobby")
        uid = event.source.user_id
        send_menu_carousel(uid)
        
    def on_enter_gameScores(self, event):
        print("I'm entering gameScores")

        uid = event.source.user_id
        img = "https://images-na.ssl-images-amazon.com/images/I/61G5S99JAAL.jpg"
        labels = ["今日比賽", "昨日比賽","其他比賽"]
        texts = ["today game", "yesterday game", "other game"]
        discription = "請選擇想要看的比分日期"
        send_button(uid, img, "Game Scores", discription, texts, labels)
        
    
    def on_enter_todayGame(self, event):
        print("I'm entering todayGame")

        today = datetime.today().strftime('%Y-%m-%d')
        uid = event.source.user_id
        reply_token = event.reply_token
        show_Games(reply_token, today)
        
        img = "https://cdn.nba.com/manage/2021/08/Web_Schedule_Announcement_Covers16x9-1-784x441.jpg"
        labels = ["比賽數據統計","回主選單"]
        texts = ["watch game result", "go back to menu"]
        discription = "看更多或回主選單"
        send_button(uid, img, "Watch more", discription, texts, labels)

        
    def on_enter_yesterdayGame(self, event):
        print("I'm entering yesterdayGame")

        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
        reply_token = event.reply_token
        uid = event.source.user_id
        show_Games(reply_token, yesterday)
        
        img = "https://cdn.nba.com/manage/2021/08/Web_Schedule_Announcement_Covers16x9-1-784x441.jpg"
        labels = ["比賽數據統計","回主選單"]
        texts = ["watch game result", "go back to menu"]
        discription = "看更多或回主選單"
        send_button(uid, img, "Watch more", discription, texts, labels)
    
    def on_enter_otherGame(self, event):
        print("I'm entering otherGame")
        userid = event.source.user_id

        msg = "請輸入想知道的比賽日期, Ex: 2021-12-22"
        push_text_message(userid, msg)

    def on_enter_showotherGame(self, event):
        print("I'm entering showotherGame")
        
        reply_token = event.reply_token
        uid = event.source.user_id
        text = event.message.text
        try:
            show_Games(reply_token, text)
            
            img = "https://cdn.nba.com/manage/2021/08/Web_Schedule_Announcement_Covers16x9-1-784x441.jpg"
            labels = ["比賽數據統計","回主選單"]
            texts = ["watch game result", "go back to menu"]
            discription = "看更多或回主選單"
            send_button(uid, img, "Watch more", discription, texts, labels)
        except:
            send_text_message(reply_token, "格式錯誤，請重新再試")
            self.go_back(event)
        
    def on_enter_boxScores(self, event):
        print("I'm entering boxScores")
        reply_token = event.reply_token
        uid = event.source.user_id
        # send_text_message(reply_token, "Trigger boxScores") 
        send_text_message(reply_token, text="請輸入比賽日期和隊伍, Ex:2021-12-22 Magic")
        
    def on_enter_showBoxscores(self, event):
        print("I'm entering showBoxscores")
        reply_token = event.reply_token
        uid = event.source.user_id
        msg = event.message.text
        
        try:
            show_boxscore(uid,msg)
            img = 'https://clutchpoints.com/wp-content/uploads/2020/10/Ranking-the-top-25-NBA-Players-going-into-2021-Thumbnail-1200x900.jpg'
            labels = ["回主選單"]
            texts = ["go back to menu"]
            discription = "看更多或回主選單"
            send_button(uid, img, "Back to menu", discription, texts, labels)
            
        except:
            send_text_message(reply_token, "格式錯誤，請重新再試")
            self.go_back(event)

    def on_enter_showStanding(self, event):
        print("I'm entering showStanding")

        # reply_token = event.reply_token
        uid = event.source.user_id
        show_standings(uid)
        
        img = "https://boundtoball.com/wp-content/uploads/2021/07/NBA-TEAM-LOGOS.jpg"
        labels = ["回主選單"]
        texts = ["go back to menu"]
        discription = "看更多或回主選單"
        send_button(uid, img, "Back to menu", discription, texts, labels)
        
    def on_enter_gameSchedule(self, event):
        print("I'm entering gameSchedule") 
        
        uid = event.source.user_id
        img = "https://cdn.nba.com/manage/2020/11/nba-basketball-iso-784x441.jpg"
        labels = ["今明兩天賽程", "球隊賽程", "回主選單"]
        texts = ["show game schedule", "search team schedule", "go back to menu"]
        discription = "請選擇想要查看的賽程"
        send_button(uid, img, "Schedule", discription, texts, labels)
        
    def on_enter_showSchedule(self, event):
        print("I'm entering showSchedule")

        uid = event.source.user_id
        reply_token = event.reply_token
        show_tmw_schedule(reply_token)
        
        img = "https://brasilturis.com.br/wp-content/uploads/2020/06/nba-define-volta-dos-jogos-para-31-de-julho-em-complexo-da-disney-1.jpg"
        labels = ["回主選單"]
        texts = ["go back to menu"]
        discription = "回主選單"
        send_button(uid, img, "Back to menu", discription, texts, labels)
    
    def on_enter_statLeader(self, event):
        print("I'm entering statLeader")

        reply_token = event.reply_token
        uid = event.source.user_id
        showStatleader(reply_token)
        
        img = "https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2021/10/24/0/14396126.jpeg&x=0&y=0&sw=0&sh=0&sl=W&fw=1050&exp=3600"
        labels = ["回主選單"]
        texts = ["go back to menu"]
        discription = "回主選單"
        send_button(uid, img, "Back to menu", discription, texts, labels)
    def on_enter_showNews(self, event):
        print("I'm entering showNews")
        uid = event.source.user_id
        reply_token= event.reply_token
        shownews(reply_token)
        
        img = "https://i1.wp.com/www.nbaanalysis.net/wp-content/uploads/2021/11/Key-Questions-Facing-Top-Title-Contenders-Early-In-NBA-Season-1.jpeg?resize=678%2C381&ssl=1"
        labels = ["回主選單"]
        texts = ["go back to menu"]
        discription = "回主選單"
        send_button(uid, img, "Back to menu", discription, texts, labels)
    
    def on_enter_searchTeamsch(self, event):
        print("I'm entering searchTeamsch")
        uid = event.source.user_id
        
        netsimg = "https://adayimg.com/wp-content/uploads/2012/05/brooklyn-nets-unveil-new-nba-logo-1.jpg"
        bullsimg = "https://sportando.basketball/wp-content/uploads/2021/03/bulls-logo-e1604871991247.jpeg"
        warriorimg = "https://static-wp-tor15-prd.torcedores.com/wp-content/uploads/2019/10/warriors-521x338.png"
        mavericksimg = "https://net-storage.tcccdn.com/storage/pianetabasket.com/img_notizie/thumb3/10/109469221348e5f23f8474e72b89f815-84391-49bae5367b7dae9344cf35bd3f0f7758.jpg"
        lakersimg = "https://wallpaperaccess.com/full/1126209.jpg"
        bucksimg = "https://images6.alphacoders.com/105/thumb-1920-1055946.jpg"
        sunimg = "https://c4.wallpaperflare.com/wallpaper/884/795/632/basketball-phoenix-suns-logo-nba-hd-wallpaper-thumb.jpg"
        clipimg = "https://image-cdn.essentiallysports.com/wp-content/uploads/20200922131406/Clippers-Logo-e1472074589881-1.jpg" 
        
        urls = [netsimg, bullsimg,warriorimg, mavericksimg, lakersimg, bucksimg, sunimg, clipimg]
        labels = ["Nets","Bulls","Warriors","Mavericks","Lakers","Bucks","Suns","Clippers"]
        texts = ["Nets","Bulls","Warriors","Mavericks","Lakers","Bucks","Suns","Clippers"]
        
        send_img_carousel(uid, urls, labels, texts)
        push_text_message(uid, message="請選擇上面隊伍和或輸入其他隊伍, Ex:Magic")
    
    def on_enter_showTeamsch(self, event):
        print("I'm entering showTeam")
        uid = event.source.user_id
        reply_token = event.reply_token
        text = event.message.text 
        try:
            showteamsch(reply_token, text)
            img = "https://img.sportsv.net/img/article/cover/3/79623/fit-LV7Ph7Arzu-945x495.png"
            labels = ["回主選單"]
            texts = ["go back to menu"]
            discription = "回主選單"
            send_button(uid, img, "Back to menu", discription, texts, labels)
        except:
            send_text_message(reply_token, "格式錯誤，請重新再試")
            self.go_back(event)
    # def on_exit_state2(self):
    #     print("Leaving state2")
