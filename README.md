# ChatBot NBA info

:basketball: **The NBA Line Bot with 6 features ! ** :basketball:
<p align="center">
  <img src="https://media.designrush.com/inspirations/129849/conversions/_1615382341_669_NBA-logo-preview.jpg" ,height="200" width="300"/>
</p>

Watch game results, boxscores, check the schedule, standings and serch for favorite Teams 

## QR code
<p align="center">
  <img src="https://qr-official.line.me/sid/L/366ndjdc.png" ,height="200" width="200"/>
</p>

## Setup

### Prerequisite
* Python 3.8
* Pipenv
* Line Bot API
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

## Finite State Machine
1. fsm example
![fsm_example](./img/show-fsm.png)
2. fsm of NBA info
![fsm](./img/fsm.png)

## Features

<p align="center">
  <img src="./img/4.jpg" ,height="330" width="190"/>
</p>

### Menu

<p align="center">
  <img src="./img/menu.jpg" ,height="350" width="190"/>
</p>

<p align="center">
  <img src="./img/5.jpg", height="350" width="190"/>
</p>

### Watch Games
Check the scores of the games on that day(Can choose **today**, **yesterday** or **enter other date** you want to know)

<p align="center">
  <img src="./img/6.jpg", height="350" width="190"/>
</p>

1. **Today game**

<p align="center">
  <img src="./img/7.jpg", height="350" width="190"/>
</p>

2. **other date with hightlight links**

<p align="center">
  <img src="./img/14.jpg", height="350" width="190"/>
</p>

### Check Schedule
<p align="center">
  <img src="./img/8.jpg", height="350" width="190"/>
</p>
1. **Tommorrow's schedule** - 
Showing the game schedule today and tomorrow 

<p align="center">
  <img src="./img/12.jpg", height="350" width="190"/>
</p>
<p align="center">
  <img src="./img/13.jpg", height="350" width="190"/>
</p>

2. **Team's schedule** - 
Can select one team to show their next 5 games' schedule

<p align="center">
  <img src="./img/9.jpg", height="350" width="190"/>
</p>

<p align="center">
  <img src="./img/10.jpg", height="350" width="190"/>
</p>

### Show Standings
Showing the team standings

<p align="center">
  <img src="./img/11.jpg", height="350" width="190"/>
</p>

### Show Stats Leader
Showing the stat leaders. (PPG / Assists / Rebounds / 3PM / Steals / Blocks)

<p align="center">
  <img src="./img/15.jpg", height="350" width="190"/>
</p>

### Show NBA news
Show the latest 10 NBA news and links to the news

<p align="center">
  <img src="./img/news1.jpg", height="350" width="190"/>
</p>

<p align="center">
  <img src="./img/news2.jpg", height="350" width="190"/>
</p>

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
