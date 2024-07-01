import nextcord
from nextcord.ext import commands, tasks

class MilkV(commands.Bot):
    def __init__(self):
        super().__init__(intents=nextcord.Intents.all(), status=nextcord.Status.offline)

        self.on_update.start()

    @tasks.loop(minutes=1)
    async def on_update(self):
        print('updating...')

    async def on_start(self):
        print('starting...')

    @on_update.before_loop
    async def before_update_loop(self):
        await self.wait_until_ready()
        await self.on_start()