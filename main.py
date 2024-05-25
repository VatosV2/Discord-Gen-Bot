from Helper import *


activity = discord.Activity(type=discord.ActivityType.playing, name=status)
intents=discord.Intents.default()
intents.members = True
intents.presences = True
bot = discord.Bot(command_prefix="*", activity=activity, status=discord.Status.online, intents=intents)


for folder in folder_list:
    stock = gen_get_stock(folder)
    for service in stock:
        remove_empty(f"{folder}/{service}" )


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    channel_ids = [free_gen_channel_id, boost_gen_channel_id, premium_gen_channel_id]  
    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)

        messages = await channel.history(limit=100).flatten()
        for message in messages:
            try:
                await message.delete()
            except:
                pass
    free_channel = bot.get_channel(free_gen_channel_id)
    booster_channel = bot.get_channel(boost_gen_channel_id)
    premium_channel = bot.get_channel(premium_gen_channel_id)
    free_channel_embed = discord.Embed(
        title="How to use Free gen:",
        description=f"**Commands**:\n```\n/gen [service]\n/stock\n```\n**Settings**:\n```\nYou need to allow Direct Messages from server members to use this bot.\n```\n**Cooldown:**\n```\nThe cooldown is {free_gen_cooldown} seconds.\n```",
        color=0xf43f5e
    )
    free_channel_embed.set_footer(text="Made by github.com/vatosv2 & discord.gg/nexustools")
    booster_channel_embed = discord.Embed(
        title="How to use Booster gen:",
        description=f"**Commands**:\n```\n/booster_gen [service]\n/booster_stock\n```\n**Settings**:\n```\nYou need to allow Direct Messages from server members to use this bot.\n```\n**Cooldown:**\n```\nThe cooldown is {boost_gen_cooldown} seconds.\n```",
        color=0xf43f5e
    )
    booster_channel_embed.set_footer(text="Made by github.com/vatosv2 & discord.gg/nexustools")
    premium_channel_embed = discord.Embed(
        title="How to use Premium gen:",
        description=f"**Commands**:\n```\n/premium_gen [service]\n/premium_stock\n```\n**Settings**:\n```\nYou need to allow Direct Messages from server members to use this bot.\n```\n**Cooldown:**\n```\nThe cooldown is {premium_gen_cooldown} seconds.\n```",
        color=0xf43f5e
    )
    premium_channel_embed.set_footer(text="Made by github.com/vatosv2 & discord.gg/nexustools")
    await free_channel.send(embed=free_channel_embed)
    await booster_channel.send(embed=booster_channel_embed)
    await premium_channel.send(embed=premium_channel_embed)

@bot.event
async def on_presence_update(before, after):
    role = discord.utils.get(before.guild.roles, id=free_gen_role)
    channel = bot.get_channel(status_logs)

    if after.bot:
        return

    had_free_gen_status = any(isinstance(activity, discord.CustomActivity) and str(activity) == free_gen_status for activity in before.activities)

    has_free_gen_status = any(isinstance(activity, discord.CustomActivity) and str(activity) == free_gen_status for activity in after.activities)

    if had_free_gen_status and not has_free_gen_status:
        await after.remove_roles(role)
        embed = discord.Embed(title="Removed Free Gen", description=f"{after.mention} has been removed from the Free Gen.", color=discord.Color.red())
        await channel.send(embed=embed)

    elif not had_free_gen_status and has_free_gen_status:
        await after.add_roles(role)
        embed = discord.Embed(title="Added Free Gen", description=f"{after.mention} has been added to the Free Gen.", color=discord.Color.green())
        await channel.send(embed=embed)

    elif had_free_gen_status and not after.activities:
        await after.remove_roles(role)
        embed = discord.Embed(title="Removed Free Gen", description=f"{after.mention} has been removed from the Free Gen.", color=discord.Color.red())
        await channel.send(embed=embed)
        
@bot.slash_command(name="whitelist", description="Whitelist a user.", guild_ids=[guild_id])
async def whitelist(
    ctx, user: discord.Option(discord.Member, "Member to whitelist", required=True)
):
    if str(ctx.author.id) != str(owner_id):
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Contact {await bot.fetch_user(owner_id)}",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ),
            ephemeral=True
        )

    if (
        not (str(user.id) in open("assets/whitelist.txt", "r").read().splitlines())
        and str(user.id) != str(owner_id)
    ):
        with open("assets/whitelist.txt", "a") as whitelist:
            whitelist.write(str(user.id) + "\n")

        embed = discord.Embed(
            title="Success",
            description=f"Successfully Whitelisted {user}",
            color=0xba67f6
        )
        log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Whitelisted <@{user.id}>", "Admin")
        log_action_file(f"{ctx.author.name} Whitelisted {user.name}")
        return await ctx.respond(embed=embed, ephemeral=True)

    elif str(user.id) == str(owner_id):
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Already Owner!",
                description=f"You cant run this command you are owner on this bot!",
                color=0xf667c6
            ),
            ephemeral=True
        )

    else:
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Already whitelisted!",
                description=f"{user} is already whitelisted!",
                color=0xf667c6
            ),
            ephemeral=True
        )
    
@bot.slash_command(name="unwhitelist", desciption="unwhitelist a user with ease.", guild_ids=[guild_id])
async def unwhitelist(
    ctx, user: discord.Option(discord.Member, "Member to unwhitelist", required=True)
):
    if str(ctx.author.id) != str(owner_id):
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Contact {await bot.fetch_user(owner_id)}",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ),
            ephemeral=True
        )

    if (
        not (str(user.id) in open("assets/whitelist.txt", "r").read().splitlines())
        and str(user.id) != str(owner_id)
    ):
        embed = discord.Embed(
            title="User Not Whitelisted!",
            description=f"{user} is currently not whitelisted.",
            color=0xf667c6
        )

        return await ctx.respond(embed=embed, ephemeral=True)

    elif str(user.id) == str(owner_id):
        return await ctx.respond(
            embed=discord.Embed(
                title=f"Already Owner!",
                description=f"You are currently the owner! You cannot unwhitelist yourself.",
                color=0xf667c6
            ),
            ephemeral=True
        )

    else:
        with open("assets/whitelist.txt", "r+") as whitelist:
            whitelisted = whitelist.readlines()
            whitelist.seek(0)
            for line in whitelisted:
                if not (str(user.id) in line):
                    whitelist.write(line)
            whitelist.truncate()

        embed = discord.Embed(
            title="Success",
            description=f"Successfully Removed {user}",
            color=0xba67f6
        )
        log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Unwhitelisted <@{user.id}>", "Admin")
        log_action_file(f"{ctx.author.name} Unwhitelisted {user.name}")

        return await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="add_service", description="Add a service.", guild_ids=[guild_id])
async def add_service(
    ctx: discord.ApplicationContext,
    gen: discord.Option(str, "Select the generator type.", choices=['Free_gen', 'Booster_gen', 'Premium_gen']),
    service: discord.Option(str, "Name of the service."),
    attachment: discord.Option(discord.Attachment, "Upload your file to fill the stock here.", required=False)
):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Added {service} in {gen}", "Admin")
    log_action_file(f"{ctx.author.name} Added {service} in {gen}")
    if gen == "Free_gen":
        folder = free_gen_folder
    if gen == "Booster_gen":
        folder = boost_gen_folder
    if gen == "Premium_gen":
        folder = premium_gen_folder
    if Path(f'{folder}/{service}.txt').is_file():
        await ctx.respond(f"Service: `{service}` Already exists!", ephemeral=True)
    else:
        if attachment:
            content = await attachment.read()
            content = content.decode()
            with open(f"{folder}/{service}.txt", "w", encoding="utf-8") as nexus:
                for stock in content.splitlines():
                    nexus.write(stock + "\n")
        else:
            with open(f"{folder}/{service}.txt", "w", encoding="utf-8") as nexus:
                nexus.close()
        await ctx.respond(f"Added Service: `{service}`!", ephemeral=True)

@bot.slash_command(name="get_log_file", descriptiom="get the log file", guild_ids=[guild_id])
async def get_log_file(ctx):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> requested log file", "Admin")
    log_action_file(f"{ctx.author.name} requested log file")
    await ctx.respond(file=discord.File("assets/logs.txt", "logs.txt"), ephemeral=True)

##########################################################################################################################################################################

@bot.slash_command(name="stock", description="get the current stock of free gen.", guild_ids=[guild_id])
async def stock(ctx):
    if ctx.channel.id == free_gen_channel_id:
        log_action_webhook(freegenhook, f"<@{ctx.author.id}> used /stock", "Free Gen")
        log_action_file(f"{ctx.author.name} used /stock")
        stock = gen_get_stock(free_gen_folder)
        stock1 = ""
        for service in stock:
            count = count_stock(free_gen_folder, service)
            service = service[:-4]
            stock1 += f"**{service}** `{count}` \n"
        embed = discord.Embed(
            title="Nexus Gen Stock",
            description=(
                stock1
            ),
            color=discord.Color.from_rgb(250, 10, 214)
        )
        embed.set_footer(text="Made by github.com/vatosv2 & discord.gg/nexustools")
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await ctx.respond("Wrong channel buddy.", ephemeral=True)


@bot.slash_command(name="remove_free_service", description="Remove A free service.", guild_ids=[guild_id])
async def remove_free_service(
  ctx, 
  service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_free_service_options))
): 
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    os.remove(f"{free_gen_folder}/{service}.txt")
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Removed {service} from free Gen", "Admin")
    log_action_file(f"{ctx.author.name} Removed {service} from free Gen")
    await ctx.respond(f"Deleted `{service}`!", ephemeral=True)

@bot.slash_command(name="restock_free_gen", description="Restock A free gen service.", guild_ids=[guild_id])
async def restock(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_free_service_options)),
    attachment: discord.Option(
        discord.Attachment, "Drag your file to fill the stock here.", required=True
    ),
):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Restocked {service} in free Gen", "Admin")
    log_action_file(f"{ctx.author.name} Restocked {service} in free Gen")
    content = await attachment.read()
    content = content.decode()
    with open(f"{free_gen_folder}/{service}.txt", "a", encoding="utf-8") as nexus:
        for stock in content.splitlines():
            nexus.write(stock + "\n")
    await ctx.respond(f"Restocked `{service}`!", ephemeral=True)

@bot.slash_command(name="clear_free_stock", description="Clears A free service Stock.", guild_ids=[guild_id])
async def clear_free_stock(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_free_service_options)),
):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Cleared {service} in free Gen", "Admin")
    log_action_file(f"{ctx.author.name} Cleared {service} in free Gen")
    with open(f"{free_gen_folder}/{service}.txt", "w", encoding="utf-8") as nexus:
        nexus.write("")
    await ctx.respond(f"Cleared Stock of `{service}`!", ephemeral=True)


@bot.slash_command(name="gen", description="Gens From Free Stock.", guild_ids=[guild_id])
@commands.cooldown(1, free_gen_cooldown, commands.BucketType.user)
async def gen(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_free_service_options)),
):
    if ctx.channel.id == free_gen_channel_id:
        role = discord.utils.get(ctx.guild.roles, id=free_gen_role)
        if role in ctx.author.roles:
            log_action_webhook(freegenhook, f"<@{ctx.author.id}> generated {service} from free Gen", "Free Gen")
            log_action_file(f"{ctx.author.name} generated {service} from free Gen")
            with open(f"{free_gen_folder}/{service}.txt", 'r', encoding="utf-8") as file:
                lines = file.readlines()

            if not lines:
                await ctx.respond(f"`{service}` Got no Stock left :(", ephemeral=True)
            else:
                non_empty_lines = [line for line in lines if line.strip() != ""]

                account = random.choice(non_empty_lines).strip()
                remaining_lines = [line for line in lines if line.strip() != account]

                with open(f"{free_gen_folder}/{service}.txt", 'w', encoding="utf-8") as file:
                    file.writelines(remaining_lines)

                await ctx.respond(f"Account generated! If you didn't receive a DM, please unlock it from settings.", ephemeral=True)
                embed = discord.Embed(
                    title="Account Generated",
                    description=(
                    f"""**Account: **
                    ```{account}```
                    """
                    
                    ),
                    color=discord.Color.from_rgb(250, 10, 214)
                )
                try:
                    await ctx.author.send(embed=embed)
                except discord.Forbidden:
                    await ctx.respond("I couldn't send you a DM. Please check your DM settings.", ephemeral=True)
        else:
            await ctx.respond("You dont have permission for Free Gen.", ephemeral=True)
    else:
        await ctx.respond("Wrong channel buddy.", ephemeral=True)

@gen.error
async def gen_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            embed=discord.Embed(
                title="Cooldown",
                description=f" Try again in {round(error.retry_after, 2)} seconds.",
                color=0xf667c6
            ), ephemeral=True
        )

#######################################################################################################################################################

@bot.slash_command(name="booster_stock", description="get the current booster gen stock.", guild_ids=[guild_id])
async def booster_stock(ctx):
    if ctx.channel.id == boost_gen_channel_id:
        log_action_webhook(boostgenhook, f"<@{ctx.author.id}> Used /booster_stock", "Booster Gen")
        log_action_file(f"{ctx.author.name} Used /booster_stock")
        stock = gen_get_stock(boost_gen_folder)
        stock1 = ""
        for service in stock:
            count = count_stock(boost_gen_folder, service)
            service = service[:-4]
            stock1 += f"**{service}** `{count}` \n"
        embed = discord.Embed(
            title="Nexus Gen Stock",
            description=(
                stock1
            ),
            color=discord.Color.from_rgb(250, 10, 214)
        )
        embed.set_footer(text="Made by github.com/vatosv2 & discord.gg/nexustools")
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await ctx.respond("Wrong channel buddy.", ephemeral=True)

@bot.slash_command(name="remove_booster_service", description="Remove A booster service.", guild_ids=[guild_id])
async def remove_booster_service(
  ctx, 
  service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_booster_service_options))
): 
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Deleted {service} in booster Gen", "Admin")
    log_action_file(f"{ctx.author.name} Deleted {service} in booster Gen")
    os.remove(f"{boost_gen_folder}/{service}.txt")
    await ctx.respond(f"Deleted `{service}`!", ephemeral=True)

@bot.slash_command(name="restock_booster_gen", description="Restock A booster gen service.", guild_ids=[guild_id])
async def booster_restock(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_booster_service_options)),
    attachment: discord.Option(
        discord.Attachment, "Drag your file to fill the stock here.", required=True
    ),
):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Restocked {service} in booster Gen", "Admin")
    log_action_file(f"{ctx.author.name} Restocked {service} in booster Gen")
    content = await attachment.read()
    content = content.decode()
    with open(f"{boost_gen_folder}/{service}.txt", "a", encoding="utf-8") as nexus:
        for stock in content.splitlines():
            nexus.write(stock + "\n")
    await ctx.respond(f"Restocked `{service}`!", ephemeral=True)

@bot.slash_command(name="clear_booster_stock", description="Clears A booster service Stock.", guild_ids=[guild_id])
async def clear_booster_stock(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_booster_service_options)),
):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Cleared {service} in booster Gen", "Admin")
    log_action_file(f"{ctx.author.name} Cleared {service} in booster Gen")
    with open(f"{boost_gen_folder}/{service}.txt", "w", encoding="utf-8") as nexus:
        nexus.write("")
    await ctx.respond(f"Cleared Stock of `{service}`!", ephemeral=True)

@bot.slash_command(name="booster_gen", description="Gens From Booster Stock.", guild_ids=[guild_id])
@commands.cooldown(1, boost_gen_cooldown, commands.BucketType.user)
async def booster_gen(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_booster_service_options)),
):
    if ctx.channel.id == boost_gen_channel_id:
        role = discord.utils.get(ctx.guild.roles, id=boost_gen_role)
        if role in ctx.author.roles:
            log_action_webhook(boostgenhook, f"<@{ctx.author.id}> generated {service} in booster Gen", "Booster Gen")
            log_action_file(f"{ctx.author.name} generated {service} in booster Gen")
            with open(f"{boost_gen_folder}/{service}.txt", 'r', encoding="utf-8") as file:
                lines = file.readlines()

            if not lines:
                await ctx.respond(f"`{service}` Got no Stock left :(", ephemeral=True)
            else:
                non_empty_lines = [line for line in lines if line.strip() != ""]

                account = random.choice(non_empty_lines).strip()
                remaining_lines = [line for line in lines if line.strip() != account]

                with open(f"{boost_gen_folder}/{service}.txt", 'w', encoding="utf-8") as file:
                    file.writelines(remaining_lines)

                await ctx.respond(f"Account generated! If you didn't receive a DM, please unlock it from settings.", ephemeral=True)
                embed = discord.Embed(
                    title="Account Generated",
                    description=(
                    f"""**Account: **
                    ```{account}```
                    """
                    
                    ),
                    color=discord.Color.from_rgb(250, 10, 214)
                )
                try:
                    await ctx.author.send(embed=embed)
                except discord.Forbidden:
                    await ctx.respond("I couldn't send you a DM. Please check your DM settings.", ephemeral=True)
        else:
            await ctx.respond("You dont have permission for booster gen.", ephemeral=True)
    else:
        await ctx.respond("Wrong channel buddy.", ephemeral=True)

@booster_gen.error
async def boost_gen(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            embed=discord.Embed(
                title="Cooldown",
                description=f" Try again in {round(error.retry_after, 2)} seconds.",
                color=0xf667c6
            ), ephemeral=True
        )
#########################################################################################################################################################################


@bot.slash_command(name="premium_stock", description="get the current premium gen stock.", guild_ids=[guild_id])
async def premium_stock(ctx):
    if ctx.channel.id == premium_gen_channel_id:
        log_action_webhook(premiumgenhook, f"<@{ctx.author.id}> Used /premium_stock", "Premium Gen")
        log_action_file(f"{ctx.author.name} Used /premium_stock")
        stock = gen_get_stock(premium_gen_folder)
        stock1 = ""
        for service in stock:
            count = count_stock(premium_gen_folder, service)
            service = service[:-4]
            stock1 += f"**{service}** `{count}` \n"
        embed = discord.Embed(
            title="Nexus Gen Stock",
            description=(
                stock1
            ),
            color=discord.Color.from_rgb(250, 10, 214)
        )
        embed.set_footer(text="Made by github.com/vatosv2 & discord.gg/nexustools")
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await ctx.respond("Wrong channel buddy.", ephemeral=True)

@bot.slash_command(name="remove_premium_service", description="Remove A premium service.", guild_ids=[guild_id])
async def remove_premium_service(
  ctx, 
  service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_premium_service_options))
): 
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> removed {service} in premium Gen", "Admin")
    log_action_file(f"{ctx.author.name} removed {service} in premium Gen")
    os.remove(f"{premium_gen_folder}/{service}.txt")
    await ctx.respond(f"Deleted `{service}`!", ephemeral=True)

@bot.slash_command(name="restock_premium_gen", description="Restock A premium gen service.", guild_ids=[guild_id])
async def restock_premium(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_premium_service_options)),
    attachment: discord.Option(
        discord.Attachment, "Drag your file to fill the stock here.", required=True
    ),
):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> Restocked {service} in premium Gen", "Admin")
    log_action_file(f"{ctx.author.name} Restocked {service} in premium Gen")
    content = await attachment.read()
    content = content.decode()
    with open(f"{premium_gen_folder}/{service}.txt", "a", encoding="utf-8") as nexus:
        for stock in content.splitlines():
            nexus.write(stock + "\n")
    await ctx.respond(f"Restocked `{service}`!", ephemeral=True)

@bot.slash_command(name="clear_premium_stock", description="Clears A premium service Stock.", guild_ids=[guild_id])
async def clear_premium_stock(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_premium_service_options)),
):
    if not await Utils.isWhitelisted(ctx):
        return await ctx.respond(
            embed=discord.Embed(
                title="Not Whitelisted",
                description="You need to be added as owner to run this command!",
                color=0xf667c6
            ), ephemeral=True
        )
    log_action_webhook(admincommandshook, f"<@{ctx.author.id}> cleared {service} in premium Gen", "Admin")
    log_action_file(f"{ctx.author.name} cleared {service} in premium Gen")
    with open(f"{premium_gen_folder}/{service}.txt", "w", encoding="utf-8") as nexus:
        nexus.write("")
    await ctx.respond(f"Cleared Stock of `{service}`!", ephemeral=True)

@bot.slash_command(name="premium_gen", description="Gens From premium Stock.", guild_ids=[guild_id])
@commands.cooldown(1, premium_gen_cooldown, commands.BucketType.user)
async def premium_gen(
    ctx,
    service: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_premium_service_options)),
):
    if ctx.channel.id == premium_gen_channel_id:
        role = discord.utils.get(ctx.guild.roles, id=premium_gen_role)
        if role in ctx.author.roles:
            log_action_webhook(premiumgenhook, f"<@{ctx.author.id}> Generated {service} in premium Gen", "Premium Gen")
            log_action_file(f"{ctx.author.name} Generated {service} in premium Gen")
            with open(f"{premium_gen_folder}/{service}.txt", 'r', encoding="utf-8") as file:
                lines = file.readlines()

            if not lines:
                await ctx.respond(f"`{service}` Got no Stock left :(", ephemeral=True)
            else:
                non_empty_lines = [line for line in lines if line.strip() != ""]

                account = random.choice(non_empty_lines).strip()
                remaining_lines = [line for line in lines if line.strip() != account]

                with open(f"{premium_gen_folder}/{service}.txt", 'w', encoding="utf-8") as file:
                    file.writelines(remaining_lines)

                await ctx.respond(f"Account generated! If you didn't receive a DM, please unlock it from settings.", ephemeral=True)
                embed = discord.Embed(
                    title="Account Generated",
                    description=(
                    f"""**Account: **
                    ```{account}```
                    """
                    
                    ),
                    color=discord.Color.from_rgb(250, 10, 214)
                )
                try:
                    await ctx.author.send(embed=embed)
                except discord.Forbidden:
                    await ctx.respond("I couldn't send you a DM. Please check your DM settings.", ephemeral=True)
        else:
            await ctx.respond("You dont have permission for Premium gen.", ephemeral=True)
    else:
        await ctx.respond("Wrong channel buddy.", ephemeral=True)

@premium_gen.error
async def premium_gen(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            embed=discord.Embed(
                title="Cooldown",
                description=f" Try again in {round(error.retry_after, 2)} seconds.",
                color=0xf667c6
            ), ephemeral=True
        )

#################################################################################################################################################################
os.system('cls' if os.name == 'nt' else 'clear')
print(f'''{Fore.LIGHTMAGENTA_EX}
                    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗   ████████╗ ██████╗  ██████╗ ██╗     ███████╗  
                    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝      
                    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗█████╗██║   ██║   ██║██║   ██║██║     ███████╗       
                    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║╚════╝██║   ██║   ██║██║   ██║██║     ╚════██║       
                    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║      ██║   ╚██████╔╝╚██████╔╝███████╗███████║   
                    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                                discord.gg/nexustools
    ''')
bot.run(bot_token)