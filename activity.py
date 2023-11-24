import discord
import random
import math


class BoltActivity():
    def __init__(self) -> None:
        pass

    def choose(self, options: list):
        return options[math.floor(random.random() * len(options))]
       
    def game(self):
        playing_list = ['Genshin Impact']
        return discord.Game(self.choose(playing_list))
        
    def activity(self):
        activities = ['game']
        activity = self.choose(activities)
        
        match activity:
            case 'game':
                return self.game()