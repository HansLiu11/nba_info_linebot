from fsm import TocMachine

def creat_machine():
    machine = TocMachine(
        states=["user", "lobby", "gameScores","todayGame","yesterdayGame","otherGame","showotherGame","boxScores", "showBoxscores","showStanding","gameSchedule", "statLeader","searchTeam","showTeam"],
        transitions=[
            {
                "trigger": "advance",
                "source": "user",
                "dest": "lobby",
                "conditions": "is_going_to_lobby",
            },
            {
                "trigger": "advance",
                "source": "lobby",
                "dest": "gameScores",
                "conditions": "is_going_to_gameScores",
            },
            {
                "trigger": "advance",
                "source": "gameScores",
                "dest": "todayGame",
                "conditions": "is_going_to_todayGame",
            },
            {
                "trigger": "advance",
                "source": "gameScores",
                "dest": "yesterdayGame",
                "conditions": "is_going_to_yesterdayGame",
            },
            {
                "trigger": "advance",
                "source": "gameScores",
                "dest": "otherGame",
                "conditions": "is_going_to_otherGame",
            },
            {
                "trigger": "advance",
                "source": "otherGame",
                "dest": "showotherGame",
                "conditions": "is_going_to_showotherGame",
            },
            {
                "trigger": "advance",
                "source": "lobby",
                "dest": "boxScores",
                "conditions": "is_going_to_boxScores",
            },
            {
                "trigger": "advance",
                "source": ["todayGame", "yesterdayGame", "showotherGame"],
                "dest": "boxScores",
                "conditions": "is_going_to_boxfromgame",
            },
            {
                "trigger": "advance",
                "source": "boxScores",
                "dest": "showBoxscores",
                "conditions": "is_going_to_showBoxscores",
            },
            {
                "trigger": "advance",
                "source": "lobby",
                "dest": "showStanding",
                "conditions": "is_going_to_showStanding",
            },
            {
                "trigger": "advance",
                "source": "lobby",
                "dest": "gameSchedule",
                "conditions": "is_going_to_gameSchedule",
            },
            {
                "trigger": "advance",
                "source": "lobby",
                "dest": "statLeader",
                "conditions": "is_going_to_statLeader",
            },
            {
                "trigger": "advance",
                "source": "lobby",
                "dest": "searchTeam",
                "conditions": "is_going_to_searchTeam",
            },
            {
                "trigger": "advance",
                "source": "searchTeam",
                "dest": "showTeam",
                "conditions": "is_going_to_showTeam",
            },
            {
                "trigger": "advance", 
                "source": ["gameScores", "yesterdayGame","todayGame", "boxScores", "showotherGame","showBoxscores" , "showStanding", "gameSchedule","statLeader","showTeam"],
                "dest": "lobby",
                "conditions": "is_going_to_backLobby",
             },
            {"trigger": "go_back", "source": ["gameScores", "yesterdayGame","todayGame","showotherGame", "boxScores", "showBoxscores", "showStanding", "gameSchedule","statLeader","showTeam"], "dest": "lobby"},
        ],
        initial="user",
        auto_transitions=False,
        show_conditions=True,
    )
    
    return machine