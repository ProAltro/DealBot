import re
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

    def clear(self):
        super().clear()
        data = None
        with open("details.json", "r") as file:
            data = json.load(file)
        with open("details.json", "w") as file:
            data["lottery"] = []
            json.dump(data, file)


class Duel:
    def __init__(self, host, p, amt, casino):
        self.host = host
        self.p = p
        self.amt = amt
        self.stage = "inv"
        self.casino = casino

    def accepted(self):
        self.stage = "guess"
        self.guesses = {self.host: [], self.p: []}
        schedule(
            30,
            self.casino.delete_duel,
            self,
            init_stage="guess",
            dm="Duel timed out. Players took too long to guess.",
        )

    async def check(self):
        if self.guesses[self.host] and self.guesses[self.p]:
            self.stage = "compl"
            win = random.randint(1, 30)
            guess = dict(self.guesses)
            for i in self.guesses:
                self.guesses[i] = [abs(j - win) for j in self.guesses[i]]
            host = min(self.guesses[self.host])
            p = min(self.guesses[self.p])
            prompt = f"""**Number**: `{win}`\n
{self.casino.users[self.host].name}'s guesses: `{guess[self.host]}`
{self.casino.users[self.p].name}'s guesses: `{guess[self.p]}`\n"""
            if p < host:
                self.casino.money[self.host] -= self.amt
                self.casino.money[self.p] += self.amt
                prompt += f"""Closest Guess: `{guess[self.p][self.guesses[self.p].index(p)]}`\n
**Winner:** {self.casino.users[self.p].name}\n\n"""
            elif p > host:
                self.casino.money[self.host] += self.amt
                self.casino.money[self.p] -= self.amt
                prompt += f"""Closest Guess: `{guess[self.host][self.guesses[self.host].index(host)]}`\n
**Winner:** {self.casino.users[self.host].name}\n\n"""
            else:
                prompt += f"""Closest Guess: `{guess[self.host][self.guesses[self.host].index(host)]}`\n
**Tie**\n\n"""

            prompt += f"""{self.casino.users[self.host].name}'s Balance: `{self.casino.money[self.host]}c`\n"""
            prompt += f"""{self.casino.users[self.p].name}'s Balance: `{self.casino.money[self.p]}c`"""
            await self.casino.users[self.host].send(prompt)
            await self.casino.users[self.p].send(prompt)

            await self.casino.delete_duel(self, duel_over=True)

            return True
        return False


class Casino:
    def __init__(self, client):
        if not os.path.exists("details.json"):
            with open("details.json", "w") as file:
                json.dump({"money": {}, "lottery": []}, file)

        with open("details.json", "r") as file:
            data = json.load(file)
            self.money = Money(data["money"])
            self.lottery_tracker = Lottery(data["lottery"])
            self.users = {}
            self.duels = {}
            self.client = client

    async def register(self, msg, id):
        if id in self.money:
            await msg.reply("You are Already Registered!")
            return
        self.money[id] = 50000
        self.users[id] = await client.fetch_user(id)
        await msg.reply("You have been registered!\nYou have **50000c**")

    async def lottery(self, msg: discord.Message, id):
        if id in self.lottery_tracker:
            await msg.reply("You have already spun the wheel!")
            return

        lottery = msg.content.split()
        if len(lottery) != 3 or lottery[1] not in ("high", "low", "mid"):
            await msg.reply(
                """Please enter in the format `?lottery <type> <guess>`
```Type:
'low' - Guess Between 1 and 10
'mid' - Guess Between 1 and 20
'high' - Guess Between 1 and 50```"""
            )
            return
        limits = {"high": 50, "low": 10, "mid": 20}
        pool = {
            "high": [
                (40, None),
                (5, 16000),
                (3, 32000),
                (2, 50000),
                (1, 250000),
            ],
            "low": [(4, 250), (2, 2000), (2, 4000), (1, 10000)],
            "mid": [(15, 500), (3, 4000), (2, 8000), (1, 50000)],
        }
        t = lottery[1]

        if str(lottery[2]).isnumeric() and 0 < int(lottery[2]) <= limits[t]:
            prizes = []
            for i in pool[t]:
                prizes.extend(i[0] * [i[1]])
            random.shuffle(prizes)
            prize = prizes[int(lottery[2])]
            self.lottery_tracker.append(id)
            if prize:
                self.money[id] += prize
                await msg.reply(
                    f"You won {prize} coins!\nCurrent balance: **{self.money[id]}c**"
                )
            else:
                await msg.reply("You won nothing! Try again later.")
        else:
            await msg.reply(f"Please enter a **number** from **1** to **{limits[t]}**")

    async def gamble(self, msg, id):
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
            await msg.reply("Player not registered")
            return
        await msg.reply(f"Balance: **{self.money[id]}c**")

    def set(self, id, amt):
        self.money[id] = amt

    def rich(self):
        money = list(self.money.items())
        money = sorted(money, key=lambda x: x[1])
        return money[::-1][:10]

    async def donate(self, msg, gid, rid, amt):
        if rid not in self.money:
            await msg.reply("Receiver is not playing the game!")
            return
        if amt > self.money[gid]:
            await msg.reply(f"You dont have **{amt}c** to donate!")
            return
        self.money[gid] -= amt
        self.money[rid] += amt
        await msg.reply(
            f"{self.users[gid]} gave {amt}c to {self.users[rid]}!\n{self.users[gid]}: {self.money[gid]}c\n{self.users[rid]}: {self.money[rid]}c"
        )

    async def duel(self, msg, host, person, amt):
        if person not in self.money:
            await msg.reply("The person you challenged isnt registered!")
        elif amt > self.money[host]:
            await msg.reply(f"You dont have **{amt}c** to donate!")
        elif amt > self.money[person]:
            await msg.reply(
                f"The person you challenged doesnt have enough money to cover the bet"
            )
        elif host in self.duels:
            await msg.reply(f"You are already in a duel!")
        elif person in self.duels:
            await msg.reply("The person you challenged is already in a duel")
        elif person == host:
            await msg.reply("You can't duel yourself.")
        else:
            self.duels[host] = Duel(host, person, amt, self)
            schedule(
                30,
                self.delete_duel,
                self.duels[host],
                dm="Duel timed out.",
                init_stage="inv",
            )
            # t = threading.Thread(
            #     target=self.delete_duel,
            #     args=(self.duels[host], [host, person], 30, True),
            # )
            # t.start()
            await msg.reply(f"{self.users[person].name} has been invited to duel.")
            await self.users[person].send(
                f"{self.users[host].name} has invited you to a duel with the bet of {amt}c.\nAccept or not? Enter yes/no"
            )
            self.duels[person] = self.duels[host]

    async def delete_duel(self, duel, init_stage=None, dm=None, duel_over=False):
        if (duel.stage == init_stage) or duel_over:
            for i in [duel.host, duel.p]:
                if i in self.duels:
                    del self.duels[i]
                if dm != None:
                    await duel.casino.users[i].send(dm)

    async def data(self, msg):
        with open("details.json", "r") as f:
            await msg.reply(f"```{json.load(f)}```")

    def reset(self):
        for i in self.money:
            self.money[i] = 50000

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
        self.casino = Casino(self)
        self.casino.users = {}
        for i in self.casino.money:
            user: discord.User = await self.fetch_user(i)
            self.casino.users[i] = user
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
        elif str(message.author.id) in self.casino.money.keys():
            if message.content.startswith("?lottery"):
                await self.casino.lottery(message, str(message.author.id))
            elif message.content.startswith("?gamble"):
                await self.casino.gamble(message, str(message.author.id))
            elif message.content.startswith("?info"):
                det = message.content.split()
                mentioned_id = parse_mention(det[1])
                if len(det) == 1:
                    await self.casino.info(message, str(message.author.id))
                elif len(det) == 2 and mentioned_id != None:
                    await self.casino.info(message, mentioned_id)
                else:
                    await message.send("Enter in the format `?info (optional:<user>)`")
            elif message.content.startswith("?donate"):
                det = message.content.split()
                mentioned_id = parse_mention(det[1])

                if len(det) == 3 and det[2].isnumeric() and mentioned_id != None:
                    await self.casino.donate(
                        message, str(message.author.id), mentioned_id, int(det[2])
                    )
                else:
                    await message.reply("Enter in the format `?donate <player> <amt>`")

            elif message.content.startswith("?rich"):
                det = self.casino.rich()
                s = ""
                for i in det:
                    user = self.casino.users[i[0]]
                    s += f"{user.name} - **{i[1]}c**\n"
                await message.reply(s)

            elif message.content.startswith("?duel"):
                det = message.content.split()
                mentioned_id = parse_mention(det[1])
                if len(det) == 3 and det[2].isnumeric() and mentioned_id != None:
                    await self.casino.duel(
                        message, str(message.author.id), mentioned_id, int(det[2])
                    )
                else:
                    await message.reply("Enter in the format `?duel <player> <amt>`")

            if message.author.id == 621638677612855306:
                if message.content.startswith("?set"):
                    msg = message.content.split()
                    mentioned_id = parse_mention(msg[1])
                    if mentioned_id != None:
                        self.casino.set(mentioned_id, msg[2])
                        await message.reply("Done.")
                    else:
                        await message.reply("Mention someone.")
                elif message.content.startswith("?reset"):
                    self.casino.reset()
                    await message.reply("Done.")
                elif message.content.startswith("?data"):
                    await self.casino.data(message)

            if isinstance(message.channel, discord.DMChannel):
                did = str(message.author.id)
                if did in self.casino.duels:
                    duel = self.casino.duels[did]
                    if duel.stage == "inv" and duel.p == did:
                        m = message.content.split()
                        if "y" in m[0]:
                            duel.accepted()
                            prompt = "Duel Accepted\nGuess 3 numbers between 1 to 30 and send them seperated by space"
                            await message.reply(prompt)
                            await self.casino.users[duel.host].send(prompt)
                        elif "n" in m[0]:
                            h = duel.host
                            await self.casino.users[h].send("Duel Rejected")
                            await message.reply("Duel Rejected")
                            duel.stage = "rejected"

                            await self.casino.delete_duel(duel, duel_over=True)
                        else:
                            await message.reply("Enter yes or no")
                    elif duel.stage == "guess":
                        if len(duel.guesses[did]) == 0:
                            m = message.content.split()
                            if (
                                len(m) == 3
                                and m[0].isnumeric()
                                and m[1].isnumeric()
                                and m[2].isnumeric()
                            ):
                                duel.guesses[did] = [
                                    int(m[1]),
                                    int(m[2]),
                                    int(m[0]),
                                ]
                                await duel.check()

                            else:
                                await message.reply(
                                    "Please enter 3 numbers like `<num1> <num2> <num3>`"
                                )
                        else:
                            await message.reply("You have already guessed!")

        elif message.content.startswith("?"):
            m = message.content.split()
            if m[0][1:] in [
                "info",
                "gamble",
                "rich",
                "donate",
                "lottery",
                "reset",
                "set",
                "data",
                "duel",
            ]:
                await message.reply("Register First!")
        if isinstance(message.channel, discord.TextChannel):
            try:
                gid = message.guild.id
                await guilds[gid].action(message)
            except KeyError:
                print("Error")

    @tasks.loop(hours=1)
    async def stuff(self):
        self.casino.lottery_reset()
        await botchannel.send("Lottery Reset")


def schedule(time, callback, *args, **kwargs):
    async def e():
        await asyncio.sleep(time)

        if asyncio.iscoroutinefunction(callback):
            await callback(*args, **kwargs)
        else:
            callback(*args, **kwargs)

    asyncio.ensure_future(e())


def parse_mention(string):
    matches = re.findall(r"<@!?(\d+)>", string)

    if len(matches) > 0:
        return matches[0]


client = MyClient(intents=discord.Intents.all())
try:
    client.run(token)
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system("kill 1")
