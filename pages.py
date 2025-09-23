from otree.api import *
from .models import C, Subsession, Group, Player


# ====== NUEVO ======
class Intro(Page):
    """Pantalla de bienvenida e instrucciones."""
    pass
# ====== FIN NUEVO ======

# =========================
# DATOS SOCIODEMOGRÁFICOS
# =========================
class Demographics(Page):
    form_model = 'player'
    form_fields = ['estrato', 'edad', 'sexo']

# ===============
# JUEGO: ULTIMÁTUM
# ===============
class UltimatumOffer(Page):
    form_model = 'group'
    form_fields = ['offer']
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

class WaitForOffer(WaitPage):
    pass

class UltimatumResponse(Page):
    form_model = 'group'
    form_fields = ['accepted']
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

class UltimatumResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs()

class UltimatumResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        return dict(offer=g.offer, accepted=g.accepted, payoff=player.payoff, endowment=C.ENDOWMENT)

# ===============
# JUEGO: DICTADOR
# ===============
class Dictador(Page):
    form_model = 'player'
    form_fields = ['dictador_oferta']
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

class DictadorResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs_dictador()

class DictadorResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        g = player.group
        dictator = g.get_player_by_id(1)
        oferta = dictator.dictador_oferta or cu(0)
        return dict(oferta=oferta, payoff=player.payoff, endowment=C.ENDOWMENT)

# ====== NUEVO ======
class Gracias(Page):
    """Pantalla de cierre/agradecimiento."""
    pass
# ====== FIN NUEVO ======

# =================
# SECUENCIA DE PÁGINAS
# =================
page_sequence = [
    Intro,           # <- NUEVO: primero
    Demographics,
    # Ultimátum
    UltimatumOffer, WaitForOffer, UltimatumResponse, UltimatumResultsWaitPage, UltimatumResults,
    # Dictador
    Dictador, DictadorResultsWaitPage, DictadorResults,
    Gracias,         # <- NUEVO: último
]