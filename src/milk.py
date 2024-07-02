import asyncio
import random
from enum import Enum, auto
from datetime import datetime, timedelta

import nextcord
from nextcord.ext import commands

class MilkVState(Enum):
    OFFLINE = auto()
    IDLE = auto()
    WORKING = auto()
    GAMING = auto()
    CHECKING_MESSAGES = auto()

def select_random_state(states: list[MilkVState], weights: list[float]) -> MilkVState:
    assert len(states) == len(weights)
    return random.choices(population=states, weights=weights, k=1)[0]

class MilkV(commands.Bot):
    def __init__(self):
        super().__init__(intents=nextcord.Intents.all(), status=nextcord.Status.offline)

        self.state = MilkVState.OFFLINE

        self.transitions = {
            (MilkVState.OFFLINE, MilkVState.IDLE):  self.on_enter_idle,
            (MilkVState.IDLE,  MilkVState.OFFLINE): self.on_enter_offline,
        }

        self.last_state_change = datetime.now()

        self.total_time_per_state = {
            MilkVState.OFFLINE: timedelta(0),
            MilkVState.IDLE: timedelta(0),
            MilkVState.WORKING: timedelta(0),
            MilkVState.GAMING: timedelta(0),
            MilkVState.CHECKING_MESSAGES: timedelta(0),
        }

        self.total_time_online = timedelta(0)

    async def change_state(self, new_state):
        now = datetime.now()

        old_state = self.state
        self.state = new_state

        duration = now - self.last_state_change
        self.total_time_per_state[old_state] += duration
        self.last_state_change = now

        if self.state != MilkVState.OFFLINE:
            self.total_time_online += duration

        transition = (old_state, new_state)
        if transition in self.transitions:
            await self.transitions[transition]()

    async def on_enter_offline(self):
        print('Going offline')
        await self.change_presence(status=nextcord.Status.offline)

    async def on_enter_idle(self):
        print('Going idle...')
        await self.change_presence(status=nextcord.Status.online)

        sleep_time = random.randint(5, 10)
        print(f'Idling for {sleep_time} minutes')
        await asyncio.sleep(sleep_time * 60)

        next_state = select_random_state(
            [MilkVState.OFFLINE, MilkVState.IDLE, MilkVState.GAMING, MilkVState.WORKING, MilkVState.CHECKING_MESSAGES],
            [2, 2, 4, 4, 6]
        )

        await self.change_state(next_state)

    async def on_enter_offline(self):
        print('going offline')
        await self.change_presence(status=nextcord.Status.offline)

    async def on_message(self, message: nextcord.Message):
        print(f'Content: {message.content}')

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('----------------------------------------------------')

        await self.change_state(MilkVState.IDLE)