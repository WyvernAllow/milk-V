import asyncio
import random

import nextcord
from nextcord.ext import commands, tasks

from enum import Enum, auto

class MilkVState(Enum):
    OFFLINE = auto()
    ONLINE = auto()
    READING = auto()
    WORKING = auto()
    GAMING = auto()
    TYPING = auto()

class MilkV(commands.Bot):
    def __init__(self):
        super().__init__(intents=nextcord.Intents.all(), status=nextcord.Status.offline)

        self.state = MilkVState.OFFLINE
        
        self.transitions = {
            (MilkVState.OFFLINE, MilkVState.ONLINE):  self.on_enter_online,
            (MilkVState.ONLINE,  MilkVState.OFFLINE): self.on_enter_offline,
            (MilkVState.ONLINE,  MilkVState.READING): self.on_enter_reading,
            (MilkVState.READING, MilkVState.WORKING): self.on_enter_working,
            (MilkVState.WORKING, MilkVState.ONLINE):  self.on_exit_working,
            (MilkVState.READING, MilkVState.GAMING):  self.on_enter_gaming,
            (MilkVState.GAMING,  MilkVState.ONLINE):  self.on_exit_gaming,
            (MilkVState.READING, MilkVState.TYPING):  self.on_enter_typing,
            (MilkVState.TYPING,  MilkVState.READING): self.on_exit_typing
        }

        self.on_update.start()

    async def change_state(self, new_state):
        old_state = self.state
        self.state = new_state

        transition = (old_state, new_state)
        if transition in self.transitions:
            await self.transitions[transition]()

    async def on_enter_online(self):
        print('going online')
        await self.change_presence(status=nextcord.Status.online)

    async def on_enter_offline(self):
        print('going offline')
        await self.change_presence(status=nextcord.Status.offline)

    async def on_enter_reading(self):
        print('starting to read messages')

    async def on_enter_working(self):
        print('starting to work')

    async def on_exit_working(self):
        print('stopping work')

    async def on_enter_gaming(self):
        print('starting to game')

    async def on_exit_gaming(self):
        print('stopping gaming')

    async def on_enter_typing(self):
        print('starting to type')

    async def on_exit_typing(self):
        print('stopping typing')

    @tasks.loop(minutes=1)
    async def on_update(self):
        print('updating...')

        if random.random() < 0.5:
            await self.change_state(MilkVState.ONLINE)
        else:
            await self.change_state(MilkVState.OFFLINE)

    async def on_start(self):
        print('starting...')

    @on_update.before_loop
    async def before_update_loop(self):
        await self.wait_until_ready()
        await self.on_start()