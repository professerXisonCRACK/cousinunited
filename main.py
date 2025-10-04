import discord
from discord.ext import commands
import json
import os
import random
import string
import asyncio
from discord.ui import View, Button
import secrets

def generate_token():
    return secrets.token_urlsafe(16)  # secure random token

# ---------------- SETTINGS ----------------
OWNER_IDS = [845482960441835560, 805747807641534484, 1349784493434736722, 1267842225727869032, 1336880287979667556]
DATA_FILE = "cousins.json"
SPARKHOST_URL = "http://v-dtx-05.sparkedhost.us:8080"
# ---------------- DATA ----------------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        cousins = json.load(f)
        cousins = {str(k): v for k, v in cousins.items()}
else:
    cousins = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(cousins, f)

# ---------------- DISCORD SETUP ----------------
intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- HELPERS ----------------
def generate_cousin_id():
    return "#" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# ---------------- EVENTS ----------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ---------------- COMMANDS ----------------
@bot.command()
async def register(ctx, user_id: int, rep: int, rank: int):
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("❌ You don't have permission.")
    if rep < 1 or rep > 100:
        return await ctx.send("⚠️ Reputation must be between 1 and 100.")
    try:
        member = await bot.fetch_user(user_id)
    except:
        return await ctx.send("❌ User not found.")
    cousin_id = cousins.get(str(user_id), {}).get("cousin_id", generate_cousin_id())
    cousins[str(user_id)] = {
        "name": member.display_name,
        "rep": rep,
        "rank": rank,
        "cousin_id": cousin_id,
        "banner": cousins.get(str(user_id), {}).get("banner"),
        "password": cousins.get(str(user_id), {}).get("password")
    }
    save_data()
    embed = discord.Embed(
        title=f"{member.name} registered!",
        description=f"👨‍👩‍👧 Reputation: **{rep}/100**\n🏅 Ranking: #{rank}\n🆔 Cousin ID: {cousin_id}",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    if cousins[str(user_id)].get("banner"):
        embed.set_image(url=cousins[str(user_id)]["banner"])
    await ctx.send(embed=embed)

@bot.command()
async def update(ctx, user_id: int, rep: int, rank: int):
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("❌ You don't have permission.")
    if str(user_id) not in cousins:
        return await ctx.send("⚠️ User not registered.")
    try:
        member = await bot.fetch_user(user_id)
    except:
        return await ctx.send("❌ User not found.")
    if "cousin_id" not in cousins[str(user_id)]:
        cousins[str(user_id)]["cousin_id"] = generate_cousin_id()
    cousins[str(user_id)].update({
        "name": member.display_name,
        "rep": rep,
        "rank": rank
    })
    save_data()
    embed = discord.Embed(
        title=f"{member.name}'s info updated!",
        description=f"🔄 New Reputation: **{rep}/100**\n🏅 Ranking: #{rank}\n🆔 Cousin ID: {cousins[str(user_id)]['cousin_id']}",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    if cousins[str(user_id)].get("banner"):
        embed.set_image(url=cousins[str(user_id)]["banner"])
    await ctx.send(embed=embed)

@bot.command()
async def setpass(ctx, password: str):
    """Set a password for your Cousin profile."""
    user_id = str(ctx.author.id)
    if user_id not in cousins:
        return await ctx.send("❌ You are not registered.")

    token = generate_token()
    cousins[user_id]["token"] = token
    cousins[user_id]["password"] = password  # optional
    save_data()

    link = f"https://YOUR-RENDER-URL/cousin/{user_id}?token={token}"
    await ctx.send(f"✅ Password set! View your profile here:\n🔗 {link}")


@bot.command()
async def rep(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        user_id = str(ctx.author.id)
        data = cousins.get(user_id)
        if not data:
            return await ctx.send("❌ You are not registered.")

        token = data.get("token")
        if not token:
            return await ctx.send("⚠️ You need to set a password first with `!setpass <password>`")

        await ctx.send(f"🔗 View your Cousin profile here:\nhttps://your-app-name.onrender.com/cousin/{user_id}?token={token}")
    else:
        await ctx.send("❌ Use this command in DMs with me!")




# ---------------- LOOKUP ----------------
@bot.command()
async def lookup(ctx, user_id: int):
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("❌ You don't have permission.")
    data = cousins.get(str(user_id))
    if not data:
        return await ctx.send("❌ This user is not registered.")
    try:
        member = await bot.fetch_user(user_id)
    except discord.NotFound:
        return await ctx.send(f"❌ Could not find user with ID {user_id}.")
    embed = discord.Embed(
        title=f"{member.name}'s Cousin Information",
        description=(
            f"👀 Reputation: **{data['rep']}/100**\n"
            f"🏅 Ranking: #{data['rank']}\n"
            f"🆔 Cousin ID: {data['cousin_id']}"
        ),
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    if data.get("banner"):
        embed.set_image(url=data["banner"])
    await ctx.send(embed=embed)

# ---------------- LEADERBOARD ----------------
@bot.command()
async def leaderboard(ctx):
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("❌ You don't have permission.")
    sorted_cousins = sorted(cousins.items(), key=lambda x: x[1]["rep"], reverse=True)
    leaderboard = ""
    for idx, (user_id, data) in enumerate(sorted_cousins, start=1):
        try:
            user = await bot.fetch_user(int(user_id))
            leaderboard += f"**#{idx}** — {user.name} : **{data['rep']}/100** (Rank: #{data['rank']})\n"
        except:
            continue
    embed = discord.Embed(
        title="🏆 Cousins Leaderboard",
        description=leaderboard or "No cousins yet.",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

# ---------------- SET BANNER ----------------
@bot.command()
async def setbanner(ctx, user_id: int, image_url: str):
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("❌ You don't have permission.")
    if str(user_id) not in cousins:
        return await ctx.send("⚠️ User not registered.")
    cousins[str(user_id)]["banner"] = image_url
    save_data()
    await ctx.send(f"✅ Banner set for user {user_id}!")

# ---------------- REP STORM ----------------
@bot.command()
async def repstorm(ctx):
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("⚠️ Only a Cousin Overlord can summon a Rep Storm!")
    winners = []
    await ctx.send("🌩️ **REP STORM IS COMING!** 🌩️")
    await asyncio.sleep(1)
    for cousin_id, data in cousins.items():
        member = ctx.guild.get_member(int(cousin_id))
        if not member:
            continue
        if data["rep"] >= 100:
            await ctx.send(f"{member.display_name} is already at max rep ✅")
            await asyncio.sleep(0.5)
            continue
        roll = random.random()
        success = roll < 0.10
        if success:
            data["rep"] = min(100, data["rep"] + 1)
            if data["rank"] > 1:
                data["rank"] -= 1
            winners.append(member.display_name)
        await ctx.send(f"{member.display_name} rolled {roll:.2f} → {'✅ +1 rep, rank ↓1' if success else '❌ no rep'}")
        await asyncio.sleep(0.5)
    save_data()
    if winners:
        await ctx.send(
            f"🌩️ **REP STORM STRIKES!** 🌩️\n"
            f"{len(winners)} cousins gained **+1 rep** and moved up the ranks! ⚡\n"
            f"Winners: {', '.join(winners)}"
        )
    else:
        await ctx.send("🌩️ **REP STORM STRIKES!** 🌩️\nNo cousins in this server gained rep this time. ⚡")

# ---------------- REP RAID ----------------
class RaidView(View):
    def __init__(self, ctx):
        super().__init__(timeout=15)
        self.ctx = ctx
        self.joined = set()
    @discord.ui.button(label="⚔️ Join Raid", style=discord.ButtonStyle.red)
    async def join(self, interaction: discord.Interaction, button: Button):
        user_id = str(interaction.user.id)
        if user_id not in cousins:
            cousins[user_id] = {
                "name": interaction.user.display_name,
                "rep": 0,
                "rank": 9999,
                "cousin_id": generate_cousin_id()
            }
        cousins[user_id]["name"] = interaction.user.display_name
        if user_id in self.joined:
            await interaction.response.send_message("❌ You already joined!", ephemeral=True)
        else:
            self.joined.add(user_id)
            await interaction.response.send_message(f"✅ {interaction.user.display_name} joined the raid!", ephemeral=True)
    async def on_timeout(self):
        results = []
        for user_id in self.joined:
            data = cousins[user_id]
            roll = random.random()
            if roll < 0.10:
                if data["rep"] < 100:
                    data["rep"] = min(100, data["rep"] + 2)
                data["rank"] = max(1, data["rank"] - 2)
                results.append(f"🏆 {data['name']} WON → **+2 rep, rank up by 2!**")
            else:
                loss = random.randint(1, 3)
                data["rep"] = max(0, data["rep"] - loss)
                data["rank"] += loss
                results.append(f"💀 {data['name']} LOST → **-{loss} rep, rank down by {loss}!**")
        save_data()
        if results:
            embed = discord.Embed(
                title="🏰 The Raid is Over!",
                description="\n".join(results),
                color=discord.Color.dark_red()
            )
            await self.ctx.send(embed=embed)
        else:
            await self.ctx.send("⚔️ Nobody joined the raid... anticlimactic 😅")

@bot.command()
async def repraid(ctx):
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("❌ Only owners can start a Rep Raid!")
    view = RaidView(ctx)
    embed = discord.Embed(
        title="⚔️ Rep Raid Incoming!",
        description="Click **Join Raid** below to fight! You have 15 seconds!",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed, view=view)

# ---------------- HYPE REP HEIST ----------------
class HypeHeistView(View):
    def __init__(self, ctx, participants):
        super().__init__(timeout=10)
        self.ctx = ctx
        self.participants = participants
        self.joined = set()
    @discord.ui.button(label="💰 Join Heist!", style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction, button: Button):
        user_id = str(interaction.user.id)
        if user_id not in self.participants:
            return await interaction.response.send_message("❌ You can't join this heist.", ephemeral=True)
        if user_id in self.joined:
            await interaction.response.send_message("❌ You already joined!", ephemeral=True)
        else:
            self.joined.add(user_id)
            await interaction.response.send_message(f"✅ You joined the heist, {interaction.user.display_name}!", ephemeral=True)
    async def on_timeout(self):
        if not self.joined:
            await self.ctx.send("💨 The heist collapsed… nobody joined in time!")
            return
        suspense_msgs = ["💣 Loading vault…", "🔒 Cracking safe…", "💨 Sneaking past guards…", "👀 Eyes on the prize…", "⚡ Almost there…"]
        for msg in suspense_msgs:
            await self.ctx.send(msg)
            await asyncio.sleep(1.5)
        winner_id = random.choice(list(self.joined))
        winner_data = cousins.get(winner_id)
        if not winner_data:
            winner_data = {
                "name": self.ctx.guild.get_member(int(winner_id)).display_name,
                "rep": 0,
                "rank": 9999,
                "cousin_id": generate_cousin_id()
            }
            cousins[winner_id] = winner_data
        gain = random.randint(1, 2)
        winner_data["rep"] = min(100, winner_data.get("rep", 0) + gain)
        if winner_data.get("rank", 9999) > 1:
            winner_data["rank"] = max(1, winner_data["rank"] - gain)
        save_data()
        winner_user = self.ctx.guild.get_member(int(winner_id))
        losers_msg = []
        for loser_id in self.joined:
            if loser_id == winner_id:
                continue
            loser_data = cousins.get(loser_id)
            if not loser_data:
                continue
            loss = random.randint(1, 2)
            loser_data["rep"] = max(0, loser_data.get("rep", 0) - loss)
            loser_data["rank"] = loser_data.get("rank", 9999) + loss
            save_data()
            loser_user = self.ctx.guild.get_member(int(loser_id))
            losers_msg.append(f"💀 {loser_user.display_name} lost {loss} rep and dropped {loss} rank!")
        animation = ["🔑", "💎", "💰", "🪙", "💣", "🔒", "⚡"]
        msg = await self.ctx.send("💨 Cracking the vault...")
        for _ in range(6):
            await msg.edit(content=" ".join(random.choices(animation, k=10)))
            await asyncio.sleep(0.5)
        await self.ctx.send("ANDDDDD…")
        await asyncio.sleep(1.5)
        result_msg = f"🏆 **{winner_user.display_name}** snatched **{gain} rep** and improved their rank by {gain}!"
        if losers_msg:
            result_msg += "\n" + "\n".join(losers_msg)
        await self.ctx.send(result_msg)

@bot.command()
async def hypeheist(ctx):
    if ctx.author.id not in OWNER_IDS:
        return await ctx.send("❌ Only owners can start a Rep Heist!")
    if isinstance(ctx.channel, discord.TextChannel):
        participants = [str(m.id) for m in ctx.channel.members if str(m.id) in cousins]
        if not participants:
            return await ctx.send("⚠️ No registered cousins in this channel to join the heist.")
        view = HypeHeistView(ctx, participants)
        embed = discord.Embed(
            title="💰 Hype Rep Heist Incoming!",
            description="Click **Join Heist!** within 10 seconds to try your luck!\n**Winner:** +1–2 rep & rank ↑1–2\n**Losers:** -1–2 rep & rank ↓1–2",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("❌ This command can only be used in server text channels!")

# ---------------- BROADCAST ----------------
@bot.command()
@commands.is_owner()
async def broadcast(ctx, *, message: str = None):
    if not message and not ctx.message.attachments:
        return await ctx.send("❌ You need to provide a message or attach an image!")
    embed = discord.Embed(
        title="📢 Global Cousin Message 📢",
        description=message or "",
        color=discord.Color.blue()
    )
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        embed.set_image(url=attachment.url)
    sent = 0
    failed = 0
    for user_id in cousins.keys():
        user = bot.get_user(int(user_id))
        if user:
            try:
                await user.send(embed=embed)
                sent += 1
                await asyncio.sleep(1)
            except Exception:
                failed += 1
    await ctx.send(f"✅ Sent to {sent} cousins. ❌ Failed: {failed}")

# ---------------- RUN BOT ----------------
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN not found in environment variables!")
bot.run(TOKEN)
