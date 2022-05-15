import discord
import random, json
import asyncio, os
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import tasks

load_dotenv()

token = os.getenv("token")
allen = None


class Command:
    @staticmethod
    async def action(msg):
        pass


class AresPing(Command):
    @staticmethod
    async def action(msg: discord.Message):
        if "arnav" in msg.content.lower():
            await msg.reply(f"<@{688719979713003520}>")


class XyreoIsGay(Command):
    @staticmethod
    async def action(msg: discord.Message):
        if "xyreo" in msg.content.lower() or msg.content.lower().startswith(
            "who is gay"
        ):
            await msg.reply("Xyreo is Gay")


class Pop(Command):
    async def action(msg: discord.Message):
        if "pop" in msg.content.lower():
            await msg.add_reaction("🖕")


class Guild:
    def __init__(self, commands):
        self.commands: list[Command] = commands

    async def action(self, msg):
        for command in self.commands:
            await command.action(msg)


names = {
    "RU": 763660200674459658,
    "Allen": 844921090237005864,
    "VOT": 938050114201714688,
    "Test": 742671327143395439,
}
mapping = {
    "RU": [XyreoIsGay, Pop],
    "VOT": [XyreoIsGay],
    "Allen": [XyreoIsGay, AresPing],
    "Test": [XyreoIsGay, Pop],
}
guilds = {names[i]: Guild(mapping[i]) for i in names.keys()}


class Game:
    awards = [
        "Ternion :Ternion",
        "Argentium :Argentium:",
        "2 months nitro :nitro: :nitro:",
        "1 month nitro :nitro:",
        "4x poc :PotOCoins: :PotOCoins: :PotOCoins: :PotOCoins: ",
        "3x poc :PotOCoins: :PotOCoins: :PotOCoins: ",
        "2x poc :PotOCoins: :PotOCoins: ",
        "Poc :PotOCoins:",
        "Platinum :Platinum: ",
        "2x coin gift :CoinGift: :CoinGift: ",
        "Gold :Gold: ",
        "Coin gift :CoinGift:",
        "Timeless beauty :timelessbeauty:",
        "2020 vet :coinscoins:",
        "Silver :Silver:",
        "Press F :CH_PressFButton:",
    ]

    def __init__(self, channel):
        self.awards = Game.awards[:]
        random.shuffle(self.awards)
        self.cases = {i: self.awards[i] for i in range(len(self.awards))}
        self.state = ("PICK", 1)
        self.channel: discord.TextChannel = channel

        self.chosen = None
        self.round = 1

    async def start(self):
        await self.channel.send("Game Started\n")
        await self.channel.send(self.available_cases())

    def events(self, e):
        pass

    async def is_proper(self, m):
        if self.state[0] == "PICK":
            try:
                if "," in m:
                    m = m.split(",")
                else:
                    m = m.split()
                m: list[str]

                for i in m:
                    if not (i.isdigit() and 0 < int(i) <= 16):
                        await self.channel.send("Please enter valid case numbers")
                        return False
                m = [int(i) for i in m]

                if len(m) != self.state[1]:
                    await self.channel.send(
                        f"Please enter **{self.state[1]}** case{'' if self.state[1] == 1 else 's seperated either by commas or spaces**'}"
                    )
                    return False
                else:
                    for i in m:
                        if i - 1 not in self.cases.keys():
                            await self.channel.send(
                                "Please pick from the available cases"
                            )
                            return False
                    else:
                        return True
            except:
                await self.channel.send(
                    "Some error occured. Please check your input and try again"
                )
                return False

        elif self.state[0] == "DND":
            try:
                if m in ["deal", "no deal", "nodeal", "no", "no_deal"]:
                    return True
                else:
                    await self.channel.send(
                        "Please enter either **Deal** or **No Deal** "
                    )
                    return False
            except:
                self.channel.send(
                    "Some Error occurred. Check your input and try again."
                )
                return False

    async def proceed(self, m):
        if self.state[0] == "PICK":
            if self.round != 1:
                picked = [(int(i) - 1) for i in m.split()]
                eliminated_text = "Eliminated:\n\n"
                for i in picked:
                    eliminated_text += f"Case: {i+1} - {self.cases[i]}\n"
                    del self.cases[i]
                await self.channel.send(eliminated_text)
                await self.channel.send("Offered 5000, Deal or No Deal ? ")
                self.state = ("DND",)

            else:
                chosen = int(m) - 1
                self.chosen = {chosen: self.cases[chosen]}
                self.round += 1
                self.state = ("PICK", 4)
                del self.cases[chosen]
                await self.channel.send(f"You picked case {chosen+1}")
                await self.channel.send(self.available_cases())

        elif self.state[0] == "DND":
            if m in ["deal", "d"]:
                await self.channel.send("Deal Accepted")
            else:
                await self.channel.send("Deal Refused")
                self.state = ("PICK", 3)
                await self.channel.send(self.available_cases())

    def available_cases(self):
        cases_msg = "Available Cases:\n"
        for i in self.cases:
            cases_msg += f"Case: {i+1}\n"
        cases_msg += (
            f"\nPick **{self.state[1]}** case{'s' if self.state[1] != 1 else ''}"
        )

        return cases_msg


class Money(dict):
    def __init__(self, d):
        super().__init__(d)

    def __setitem__(self, key, value):
        super().__setitem__(key, int(value))
        data = None
        with open("details.json", "r") as file:
            data = json.load(file)
        with open("details.json", "w") as file:
            data["money"] = self
            json.dump(data, file)

    def __getitem__(self, key):
        return super().__getitem__(key)


class Lottery(list):
    def __init__(self, l):
        super().__init__(l)

    def append(self, value):
        super().append(value)
        data = None
        with open("details.json", "r") as file:
            data = json.load(file)
        with open("details.json", "w") as file:
            data["lottery"] = self
            json.dump(data, file)


class Casino:
    def __init__(self):
        with open("details.json", "r") as file:
            data = json.load(file)
            self.money = Money(data["money"])
            self.lottery_tracker = Lottery(data["lottery"])

    async def register(self, msg, id):
        if id in self.money:
            await msg.reply("You are Already Registered!")
            return
        self.money[id] = 5000
        await msg.reply("You have been registered!\nYou have 5000c")

    async def lottery(self, msg: discord.Message, id):
        if id not in self.money:
            await msg.reply("Register First!")
            return
        if id in self.lottery_tracker:
            await msg.reply("You have already spun the wheel!")
            return
        prizes = [None, None, None, 100, 50, 200, 50, 50, 50, 100]
        random.shuffle(prizes)

        lottery = msg.content.split()
        if len(lottery) != 2:
            await msg.reply("Please enter in the format `?lottery <guess>`")
            return

        if str(lottery[1]).isnumeric() and 0 < int(lottery[1]) <= 10:
            prize = prizes[int(lottery[1])]
            self.lottery_tracker.append(id)
            if prize:
                self.money[id] += prize
                await msg.reply(
                    f"You won {prize} coins!\nCurrent balance: **{self.money[id]}**c"
                )
            else:
                await msg.reply("You won nothing! Try again later.")
        else:
            await msg.reply("Please enter a **number** from **1** to **20**")

    async def gamble(self, msg, id):
        if id not in self.money:
            await msg.reply("Register First!")
            return
        g = msg.content.split()
        g = g[1:]
        if (
            len(g) == 2
            and g[0].isnumeric()
            and g[1].isnumeric()
            and 1 <= int(g[1]) <= 3
        ):
            if int(g[0]) > self.money[id]:
                await msg.reply(
                    f"You have only {self.money[id]}!\nYou can only place bets less than your money"
                )
            else:
                guess = random.randint(1, 3)
                if guess == int(g[1]):
                    self.money[id] += int(g[0])
                    await msg.reply(
                        f"You guessed correctly!\nYou won {g[0]}c.\nCurrent Balance: **{self.money[id]}**c"
                    )
                else:
                    self.money[id] -= int(g[0])
                    await msg.reply(
                        f"You guessed wrong\nCurrent Balance: **{self.money[id]}**c"
                    )
        else:
            await msg.reply(
                f"Please enter in the format: `?gamble <amt> <guess>`.\nMake sure the guess is between 1 and 3"
            )

    async def info(self, msg, id):
        if id not in self.money:
            await msg.reply("Register First!")
            return
        await msg.reply(f"Your Current Balance: **{self.money[id]}c**")

    async def set(self, id, amt):
        self.money[id] = amt

    def rich(self, msg):
        money = list(self.money.items())
        money = sorted(money, key=lambda x: x[1])
        return money[-1]

    def lottery_reset(self):
        self.lottery_tracker.clear()


class MyClient(discord.Client):
    async def on_ready(self):
        global allen, botchannel
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")
        self.games: dict[int, Game] = {}
        allen = self.get_guild(names["Allen"])
        botchannel = self.get_channel(975318526351003678)
        print("Allen: ", allen)
        self.casino = Casino()
        self.stuff.start()

    async def on_member_update(self, before, after):
        bact = list(before.activities)
        aact = list(after.activities)
        if len(bact) == len(aact):
            return

        role = get(allen.roles, name="Music")

        waslisten = False
        islisten = False
        for i in bact:
            if isinstance(i, discord.activity.Spotify):
                waslisten = True

        for i in aact:
            if isinstance(i, discord.activity.Spotify):
                islisten = True

        if not waslisten and islisten:
            await before.add_roles(role)
        elif waslisten and not islisten:
            await before.remove_roles(role)

    async def on_message(self, message: discord.Message):
        # region Deal Bot
        if message.author.id == self.user.id:
            return
        cid = message.channel.id
        if message.content.startswith("!dnd start"):
            self.games[cid] = Game(message.channel)
            await self.games[cid].start()
            return
        elif message.content.startswith("!dnd end"):
            del self.games[cid]
            await message.channel.send("Game Ended")
            return
        elif cid in self.games:
            game = self.games[cid]
            m = message.content.lower()
            if await game.is_proper(m):
                await game.proceed(m)
            else:
                return

        # endregion
        # region Gamble Bot
        if message.content.startswith("?register"):
            await self.casino.register(message, str(message.author.id))
        elif message.content.startswith("?lottery"):
            await self.casino.lottery(message, str(message.author.id))
        elif message.content.startswith("?gamble"):
            await self.casino.gamble(message, str(message.author.id))
        elif message.content.startswith("?info"):
            await self.casino.info(message, str(message.author.id))
        elif message.author.id == 621638677612855306 and message.content.startswith(
            "?set"
        ):
            msg = message.content.split()
            await self.casino.set(msg[1][2:-1], msg[2])
        elif message.content.startswith("?rich"):
            det = self.casino.rich(message)
            user: discord.User = await self.fetch_user(det[0])
            await message.reply(f"{user.name}: **{det[1]}c**")

        gid = message.guild.id
        await guilds[gid].action(message)

    @tasks.loop(hours=1)
    async def stuff(self):
        self.casino.lottery_reset()
        await botchannel.send("Lottery Reset")


client = MyClient(intents=discord.Intents.all())
try:
    client.run(token)
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system("kill 1")
