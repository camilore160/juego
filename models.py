from otree.api import *
from otree.api import widgets  # para usar RadioSelect


class C(BaseConstants):
    NAME_IN_URL = 'juegos'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)  # dotación inicial en puntos/fichas
    # range() requiere enteros, por eso usamos int(ENDOWMENT)
    OFFER_CHOICES = list(range(0, int(ENDOWMENT) + 1, 10))  # 0..100 de 10 en 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # -------------------
    # ULTIMÁTUM
    # -------------------
    offer = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto ofreces al otro jugador?"
    )
    accepted = models.BooleanField(
        label="¿Aceptas la oferta?",
        choices=[[True, 'Aceptar'], [False, 'Rechazar']],
        widget=widgets.RadioSelect
    )

    def set_payoffs(self):
        # p1 = proponente (id 1), p2 = receptor (id 2)
        p1, p2 = self.get_players()
        if self.accepted:
            p1.payoff = C.ENDOWMENT - self.offer
            p2.payoff = self.offer
        else:
            p1.payoff = cu(0)
            p2.payoff = cu(0)

    # -------------------
    # DICTADOR
    # -------------------
    def set_payoffs_dictador(self):
        p1, p2 = self.get_players()  # p1 es el dictador (id 1)
        p1.payoff = C.ENDOWMENT - p1.dictador_oferta
        p2.payoff = p1.dictador_oferta


class Player(BasePlayer):
    # Sociodemográficos
    estrato = models.IntegerField(
        label="¿Cuál es tu estrato socioeconómico?",
        choices=[1, 2, 3, 4, 5, 6],
        widget=widgets.RadioSelect
    )
    edad = models.IntegerField(
        label="¿Cuál es tu edad?",
        min=16, max=100
    )
    sexo = models.StringField(
        label="Sexo",
        choices=["Hombre", "Mujer", "Otro", "Prefiero no decir"],
        widget=widgets.RadioSelect
    )

    # Decisión del dictador
    dictador_oferta = models.CurrencyField(
        choices=C.OFFER_CHOICES,
        label="¿Cuánto darías al otro jugador?"
    )