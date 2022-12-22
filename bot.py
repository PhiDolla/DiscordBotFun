import discord
import responses
import time
import os
from mutagen.mp3 import MP3
from dotenv import load_dotenv

load_dotenv()


class DiscordUser:
  def __init__(self, Name, DiscID, PlayIntro):
    self.Name = Name
    self.DiscID = DiscID
    self.PlayIntro = PlayIntro

discordUsers = []

Kevin = DiscordUser("Kevin", 99631509811531776, False)
Jordan = DiscordUser("Jordan", 118580050458181632, False)
Ash = DiscordUser("Ash", 379371489830371328, False)
Joseph = DiscordUser("Joseph", 96755714260754432, False)
Gem = DiscordUser("Gem", 128770452116996096, False)
Arevalo = DiscordUser("Arevalo", 423785008545923075, False)
Derrick = DiscordUser("Derrick", 96813438143045632, False)
Kristian = DiscordUser("Kristian", 118563421980590084, False)
Phil = DiscordUser("Phil", 132963280351264768, False)

discordUsers.append(Kevin)
discordUsers.append(Jordan)
discordUsers.append(Ash)
discordUsers.append(Joseph)
discordUsers.append(Gem)
discordUsers.append(Arevalo)
discordUsers.append(Kristian)
discordUsers.append(Phil)

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)

        for DiscUser in discordUsers:
            if DiscUser.DiscID == message.author.id:
                if response == 'Your intro was turned on.':
                    DiscUser.PlayIntro = True
                elif response == 'Your intro was turned off.':
                    DiscUser.PlayIntro = False

        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = os.getenv('discordToken')
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    
    client = discord.Client(intents = intents)

    async def playSoundOnEnter(path_mp3, member, before, after):

        voice_client = discord.utils.get(client.voice_clients, guild=member.guild)
        path_ffmpeg = r"D:\\PythonFiles\\ffmpeg\\bin\\ffmpeg.exe"
        
        if voice_client:
            print('Already connected to voice channel')
            return

        vc_before = before.channel
        vc_after = after.channel

        channel = client.get_channel(1055363530662084619)

        if vc_before == vc_after:
            return

        if vc_before is None:
            channel = member.voice.channel
            vc = await channel.connect()
            time.sleep(.5)
            vc.play(discord.FFmpegPCMAudio(executable=path_ffmpeg, source=path_mp3))

            time.sleep(MP3(path_mp3).info.length)

            await vc.disconnect()

        elif vc_after is None:
            return

        else:
            channel = member.voice.channel
            vc = await channel.connect()
            time.sleep(.5)
            vc.play(discord.FFmpegPCMAudio(executable=path_ffmpeg, source=path_mp3))

            time.sleep(MP3(path_mp3).info.length)

            await vc.disconnect()

    @client.event
    async def on_ready():
        print(f'{client.user} is now running.')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
            
        user_message = str(message.content)

        #if message.author.id == Kevin:
        #    await message.channel.send(f'Shut the fuck up CRACKER!')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    @client.event
    async def on_voice_state_update(member, before, after):

        if member.id == Kevin.DiscID and Kevin.PlayIntro:
            await playSoundOnEnter("DonnieThornberry.mp3", member, before, after)

        elif member.id == Jordan.DiscID and Jordan.PlayIntro:
            await playSoundOnEnter("RoundOfApplause.mp3", member, before, after)

        elif member.id == Ash.DiscID and Ash.PlayIntro:
            await playSoundOnEnter("GiantRatMakesTheRules.mp3", member, before, after)

        elif member.id == Arevalo.DiscID and Arevalo.PlayIntro:
            await playSoundOnEnter("AvocadosFromMexico.mp3", member, before, after)
        
        elif member.id == Derrick.DiscID and Derrick.PlayIntro:
            await playSoundOnEnter("ArmyStrong.mp3", member, before, after)

        elif member.id == Kristian.DiscID and Kristian.PlayIntro:
            await playSoundOnEnter("Trapanese.mp3", member, before, after)

        elif member.id == Phil.DiscID and Phil.PlayIntro:
            await playSoundOnEnter("PutMyArmorOn.mp3", member, before, after)

    client.run(TOKEN)