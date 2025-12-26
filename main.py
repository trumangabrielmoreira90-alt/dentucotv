import discord
from discord.ext import commands
from discord import app_commands

TOKEN = "MTQ1MzgxMTQ1MjE0OTQ5ODAzOA.GTUjl7.GpjH1Om6SMxJQP4W48lh5qfjDBj3Mb8OfbFM90"

STAFF_ROLE_ID = 1448078922905293022
SUPORTE_CATEGORY_ID = 1452827497879306261
DENUNCIA_CATEGORY_ID = 1452827497879306261
FINANCEIRO_CATEGORY_ID = 1452827497879306261

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)


# ======================
# VIEW DO PAINEL
# ======================
class TicketPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def criar_ticket(self, interaction, categoria_id, nome, emoji):
        guild = interaction.guild
        user = interaction.user
        category = guild.get_channel(categoria_id)

        for channel in category.channels:
            if channel.topic == str(user.id):
                await interaction.response.send_message(
                    "❌ Você já tem um ticket aberto nesta categoria.",
                    ephemeral=True
                )
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True),
            guild.get_role(STAFF_ROLE_ID): discord.PermissionOverwrite(view_channel=True)
        }

        channel = await guild.create_text_channel(
            name=f"{nome}-{user.name}".lower(),
            category=category,
            overwrites=overwrites,
            topic=str(user.id)
        )

        embed = discord.Embed(
            title=f"{emoji} Ticket de {nome.capitalize()}",
            description="Explique sua solicitação.",
            color=discord.Color.blurple()
        )

        await channel.send(
            content=f"{user.mention} | <@&{STAFF_ROLE_ID}>",
            embed=embed,
            view=FecharTicket()
        )

        await interaction.response.send_message(
            f"✅ Ticket criado: {channel.mention}",
            ephemeral=True
        )

    @discord.ui.button(label="Suporte", emoji="🎧", style=discord.ButtonStyle.primary)
    async def suporte(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_ticket(interaction, SUPORTE_CATEGORY_ID, "suporte", "🎧")

    @discord.ui.button(label="Denúncias", emoji="⚠️", style=discord.ButtonStyle.danger)
    async def denuncias(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_ticket(interaction, DENUNCIA_CATEGORY_ID, "denuncia", "⚠️")

    @discord.ui.button(label="Financeiro", emoji="💰", style=discord.ButtonStyle.success)
    async def financeiro(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_ticket(interaction, FINANCEIRO_CATEGORY_ID, "financeiro", "💰")


# ======================
# VIEW FECHAR TICKET
# ======================
class FecharTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fechar Ticket", emoji="🔒", style=discord.ButtonStyle.red)
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if STAFF_ROLE_ID not in [r.id for r in interaction.user.roles]:
            await interaction.response.send_message(
                "❌ Apenas a staff pode fechar este ticket.",
                ephemeral=True
            )
            return

        await interaction.channel.delete()


# ======================
# SLASH COMMAND
# ======================
@bot.tree.command(name="tickets", description="Enviar painel de tickets")
@app_commands.checks.has_role(STAFF_ROLE_ID)
async def tickets(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Central de Atendimento",
        description=(
            "🎧 Suporte\n"
            "⚠️ Denúncias\n"
            "💰 Financeiro"
        ),
        color=discord.Color.dark_blue()
    )

    await interaction.channel.send(embed=embed, view=TicketPanel())
    await interaction.response.send_message("✅ Painel enviado.", ephemeral=True)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"🤖 Bot online como {bot.user}")


# ========================
# START BOT
# ========================
print("✅ Token carregado com sucesso")
TOKEN = "MTQ1MzgxMTQ1MjE0OTQ5ODAzOA.GTUjl7.GpjH1Om6SMxJQP4W48lh5qfjDBj3Mb8OfbFM90"
bot.run(TOKEN)
