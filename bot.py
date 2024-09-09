import discord
from discord.ext import commands
import smtplib
import random
import re
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD-TOKEN')
GUILD_ID = os.getenv('GUILD_ID')  # Remplacer par l'ID de votre serveur
EMAIL_DOMAIN = '@ynov.com'
VERIFICATION_CODES = {}  # Stocker les codes de vérification ici

# Configurer le bot
intents = discord.Intents.default()
intents.members = True  # Nécessaire pour manipuler les membres
bot = commands.Bot(command_prefix='>', intents=intents)

# Fonction pour envoyer un e-mail avec un code de vérification
def send_verification_email(email_address, verification_code):
    sender_email = "yapsonstudi@gmail.com"
    password = os.getenv('EMAIL_PASSWORD')

    message = f"Votre code de vérification est : {verification_code}"
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, email_address, message)
        server.quit()
        print(f"Code envoyé à {email_address}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")

# Commande pour débuter l'inscription
@bot.command(name='inscription')
async def inscription(ctx, email: str):
    """
    Démarre le processus d'inscription en envoyant un code de vérification par email.
    """
    # Vérifier que l'e-mail appartient à l'institution
    if not re.match(rf'^[\w\.-]+{EMAIL_DOMAIN}$', email):
        await ctx.send(f"Veuillez entrer une adresse e-mail valide se terminant par {EMAIL_DOMAIN}.")
        return

    # Générer et stocker un code de vérification
    verification_code = random.randint(100000, 999999)
    VERIFICATION_CODES[ctx.author.id] = (email, verification_code)

    # Envoyer le code à l'adresse e-mail
    send_verification_email(email, verification_code)
    await ctx.send(f"Un code de vérification a été envoyé à {email}. Veuillez l'entrer avec la commande `>verifier <code>`.")

# Commande pour vérifier le code
@bot.command(name='verifier')
async def verifier(ctx, code: int):
    """
    Vérifie le code de vérification et attribue un rôle si le code est correct.
    """
    if ctx.author.id not in VERIFICATION_CODES:
        await ctx.send("Vous n'avez pas encore initié le processus d'inscription.")
        return

    email, correct_code = VERIFICATION_CODES[ctx.author.id]

    if code == correct_code:
        # Ajouter un rôle après la vérification (le rôle "Étudiant")
        role = discord.utils.get(ctx.guild.roles, name="Étudiant")
        await ctx.author.add_roles(role)
        await ctx.send("Votre compte a été vérifié et vous avez reçu le rôle Étudiant.")
        del VERIFICATION_CODES[ctx.author.id]
    else:
        await ctx.send("Le code est incorrect. Veuillez réessayer.")

# Ajouter les rôles par réaction
@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté au serveur.')

    # Envoyer un message de bienvenue avec les réactions pour choisir les rôles
    guild = bot.get_guild(GUILD_ID)
    channel = discord.utils.get(guild.text_channels, name='👋┊roles-et-filières')  # Nom du canal à changer si besoin
    message = await channel.send(
        "Réagissez pour obtenir vos rôles:\n"
        "📱 pour B1 INFO\n💻 pour B3 INFO\n🖥️ pour M1/M2 INFO\n\n"
        "📈 pour B1 MARCOM\n📉 pour B3 MARCOM\n📊 pour M1/M2 MARCOM\n\n"
        "🏕️ pour B1 CREA\n🏜️ pour B3 CREA\n🏞️ pour M1/M2 CREA\n\n"
        "🎧 pour B1 AUDIO\n🎤 pour B3 AUDIO\n🎚️ pour M1/M2 AUDIO\n\n"
        "⛺ pour B1 ARCHI\n🏠 pour B3 ARCHI\n🏟️ pour M1/M2 ARCHI\n\n"
        "🗡️ pour B1 ANIM 3D\n⚔️ pour B3 ANIM 3D\n🔫 pour M1/M2 ANIM 3D\n\n"
        "👔 pour INTERVENANT(E)"
    )

    # Ajout des réactions au message
    reactions = ['📱', '💻', '🖥️', '📈', '📉', '📊', '🏕️', '🏜️', '🏞️', '🎧', '🎤', '🎚️', '⛺', '🏠', '🏟️', '🗡️', '⚔️', '🔫', '👔']
    for emoji in reactions:
        await message.add_reaction(emoji)

# Attribuer le rôle en fonction de la réaction
@bot.event
async def on_raw_reaction_add(payload):
    if payload.guild_id != int(GUILD_ID):
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    role = None

    if payload.emoji.name == '📱':
        role = discord.utils.get(guild.roles, name="B1 INFO")
    elif payload.emoji.name == '💻':
        role = discord.utils.get(guild.roles, name="B3 INFO")
    elif payload.emoji.name == '🖥️':
        role = discord.utils.get(guild.roles, name="M1/M2 INFO")
    elif payload.emoji.name == '📈':
        role = discord.utils.get(guild.roles, name="B1 MARCOM")
    elif payload.emoji.name == '📉':
        role = discord.utils.get(guild.roles, name="B3 MARCOM")
    elif payload.emoji.name == '📊':
        role = discord.utils.get(guild.roles, name="M1/M2 MARCOM")
    elif payload.emoji.name == '🏕️':
        role = discord.utils.get(guild.roles, name="B1 CREA")
    elif payload.emoji.name == '🏜️':
        role = discord.utils.get(guild.roles, name="B3 CREA")
    elif payload.emoji.name == '🏞️':
        role = discord.utils.get(guild.roles, name="M1/M2 CREA")
    elif payload.emoji.name == '🎧':
        role = discord.utils.get(guild.roles, name="B1 AUDIO")
    elif payload.emoji.name == '🎤':
        role = discord.utils.get(guild.roles, name="B3 AUDIO")
    elif payload.emoji.name == '🎚️':
        role = discord.utils.get(guild.roles, name="M1/M2 AUDIO")
    elif payload.emoji.name == '⛺':
        role = discord.utils.get(guild.roles, name="B1 ARCHI")
    elif payload.emoji.name == '🏠':
        role = discord.utils.get(guild.roles, name="B3 ARCHI")
    elif payload.emoji.name == '🏟️':
        role = discord.utils.get(guild.roles, name="M1/M2 ARCHI")
    elif payload.emoji.name == '🗡️':
        role = discord.utils.get(guild.roles, name="B1 ANIM 3D")
    elif payload.emoji.name == '⚔️':
        role = discord.utils.get(guild.roles, name="B3 ANIM 3D")
    elif payload.emoji.name == '🔫':
        role = discord.utils.get(guild.roles, name="M1/M2 ANIM 3D")
    elif payload.emoji.name == '👔':
        role = discord.utils.get(guild.roles, name="INTERVENANT(E)")

    if role:
        await member.add_roles(role)

# Retirer le rôle si la réaction est supprimée
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.guild_id != int(GUILD_ID):
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    role = None

    if payload.emoji.name == '📱':
        role = discord.utils.get(guild.roles, name="B1 INFO")
    elif payload.emoji.name == '💻':
        role = discord.utils.get(guild.roles, name="B3 INFO")
    elif payload.emoji.name == '🖥️':
        role = discord.utils.get(guild.roles, name="M1/M2 INFO")
    elif payload.emoji.name == '📈':
        role = discord.utils.get(guild.roles, name="B1 MARCOM")
    elif payload.emoji.name == '📉':
        role = discord.utils.get(guild.roles, name="B3 MARCOM")
    elif payload.emoji.name == '📊':
        role = discord.utils.get(guild.roles, name="M1/M2 MARCOM")
    elif payload.emoji.name == '🏕️':
        role = discord.utils.get(guild.roles, name="B1 CREA")
    elif payload.emoji.name == '🏜️':
        role = discord.utils.get(guild.roles, name="B3 CREA")
    elif payload.emoji.name == '🏞️':
        role = discord.utils.get(guild.roles, name="M1/M2 CREA")
    elif payload.emoji.name == '🎧':
        role = discord.utils.get(guild.roles, name="B1 AUDIO")
    elif payload.emoji.name == '🎤':
        role = discord.utils.get(guild.roles, name="B3 AUDIO")
    elif payload.emoji.name == '🎚️':
        role = discord.utils.get(guild.roles, name="M1/M2 AUDIO")
    elif payload.emoji.name == '⛺':
        role = discord.utils.get(guild.roles, name="B1 ARCHI")
    elif payload.emoji.name == '🏠':
        role = discord.utils.get(guild.roles, name="B3 ARCHI")
    elif payload.emoji.name == '🏟️':
        role = discord.utils.get(guild.roles, name="M1/M2 ARCHI")
    elif payload.emoji.name == '🗡️':
        role = discord.utils.get(guild.roles, name="B1 ANIM 3D")
    elif payload.emoji.name == '⚔️':
        role = discord.utils.get(guild.roles, name="B3 ANIM 3D")
    elif payload.emoji.name == '🔫':
        role = discord.utils.get(guild.roles, name="M1/M2 ANIM 3D")
    elif payload.emoji.name == '👔':
        role = discord.utils.get(guild.roles, name="INTERVENANT(E)")

    if role:
        await member.remove_roles(role)

# Lancer le bot
bot.run(TOKEN)
