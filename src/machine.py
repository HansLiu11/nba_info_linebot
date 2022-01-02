from fsm import TocMachine

def create_machine():
    machine = TocMachine(
        states=["user", "init", "showFsm","lobby", "gameScores","todayGame","yesterdayGame","otherGame","showotherGame","boxScores", "showBoxscores","showStanding","showSchedule", "gameSchedule","searchTeamsch" ,"showTeamsch", "statLeader", "showNews"],
        transitions=[
            {
                "trigger": "advance",
                "source": "user",
                "dest": "init",
                "conditions": "is_going_to_init",
            },
            {
                "trigger": "advance",
                "source": "init",
                "dest": "lobby",
                "conditions": "is_going_to_lobby",
            },
            {
                "trigger": "advance",
                "source": "init",
                "dest": "showFsm",
                "conditions": "is_going_to_showFsm",
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
                "source": "gameSchedule",
                "dest": "showSchedule",
                "conditions": "is_going_to_showSchedule",
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
                "dest": "showNews",
                "conditions": "is_going_to_showNews",
            },
            {
                "trigger": "advance",
                "source": "gameSchedule",
                "dest": "searchTeamsch",
                "conditions": "is_going_to_searchTeamsch",
            },
            {
                "trigger": "advance",
                "source": "searchTeamsch",
                "dest": "showTeamsch",
                "conditions": "is_going_to_showTeamsch",
            },
            {
                "trigger": "advance", 
                "source": ["gameScores", "yesterdayGame","todayGame", "boxScores", "showotherGame","showBoxscores" , "showStanding", "gameSchedule","statLeader", "showNews", "showSchedule", "showTeamsch"],
                "dest": "lobby",
                "conditions": "is_going_to_backLobby",
             },
            {
                "trigger": "advance",
                "source": "showotherGame",
                "dest": "otherGame",
                "conditions": "is_going_to_backotherGame",
            },
            {
                "trigger": "go_back",
                "source": ["showFsm"],
                "dest": "init",
            },
            {"trigger": "go_back", "source": ["gameScores", "yesterdayGame","todayGame","showotherGame","showTeamsch" ,"boxScores", "showBoxscores", "showStanding", "showSchedule","gameSchedule","statLeader", "showNews", "searchTeamsch"], "dest": "lobby"},
        ],
        initial="user",
        auto_transitions=False,
        show_conditions=True,
    )
    
    return machine