import discord
import random
import asyncio, os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("token")


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


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")
        self.games: dict[int, Game] = {}

    async def on_message(self, message: discord.Message):
        # we do not want the bot to reply to itself
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

        if "xyreo" in message.content.lower():
            await message.channel.send("Xyreo is gay")

        if "pop" in message.content.lower():
            await message.add_reaction("🖕")


client = MyClient()
client.run(token)
