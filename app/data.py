"""Datos del dominio: clases de Baldur's Gate 3 y preguntas del cuestionario.

Cada clase tiene "rasgos" (0 a 3) que describen cómo se juega. Cada opción de
respuesta suma o resta puntos a esos mismos rasgos. El puntaje de una clase es
el producto de ambos (ver logic.py).
"""
from dataclasses import dataclass, field

HABILIDADES = {
    "FUE": "Fuerza",
    "DES": "Destreza",
    "CON": "Constitución",
    "INT": "Inteligencia",
    "SAB": "Sabiduría",
    "CAR": "Carisma",
}

DIFICULTADES = {1: "Fácil", 2: "Media", 3: "Difícil"}


@dataclass(frozen=True)
class Clase:
    slug: str
    nombre: str
    rol: str
    dificultad: int  # 1 = fácil, 2 = media, 3 = difícil
    dado_golpe: int
    armadura: str
    orden_habilidades: tuple
    rasgos: dict
    descripcion: str
    consejo: str

    @property
    def dificultad_texto(self) -> str:
        return DIFICULTADES[self.dificultad]


@dataclass(frozen=True)
class Opcion:
    texto: str
    rasgos: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Pregunta:
    id: int
    texto: str
    opciones: tuple


def _r(melee=0, distancia=0, magia=0, resistencia=0, sigilo=0,
       apoyo=0, social=0, naturaleza=0, simple=0):
    return dict(melee=melee, distancia=distancia, magia=magia,
                resistencia=resistencia, sigilo=sigilo, apoyo=apoyo,
                social=social, naturaleza=naturaleza, simple=simple)


CLASES = (
    Clase("barbaro", "Bárbaro", "Tanque de daño cuerpo a cuerpo", 1, 12,
          "Ligera y media, sin armadura pesada",
          ("FUE", "CON", "DES", "SAB", "CAR", "INT"),
          _r(melee=3, resistencia=3, naturaleza=1, simple=3),
          "Un guerrero furioso que entra en ira, resiste muchísimo daño y golpea fuerte.",
          "Activa la ira al inicio de cada combate y ataca al enemigo más cercano."),
    Clase("bardo", "Bardo", "Apoyo, carisma y habilidades", 3, 8,
          "Ligera",
          ("CAR", "DES", "CON", "SAB", "INT", "FUE"),
          _r(melee=1, distancia=1, magia=2, sigilo=1, apoyo=3, social=3),
          "Un artista con magia que inspira aliados, convence en los diálogos y sabe de todo un poco.",
          "Úsalo si disfrutas las conversaciones; tiene muchas opciones y requiere más planificación."),
    Clase("clerigo", "Clérigo", "Sanador y apoyo con fe", 2, 8,
          "Media y escudo (algunos dominios, pesada)",
          ("SAB", "CON", "FUE", "DES", "CAR", "INT"),
          _r(melee=2, magia=2, resistencia=2, apoyo=3, social=1, simple=1),
          "Un servidor divino que cura, protege al grupo y puede pelear de cerca con armadura.",
          "Mantén un par de hechizos de curación preparados y aprovecha la armadura."),
    Clase("druida", "Druida", "Mago de la naturaleza y transformaciones", 3, 8,
          "Media sin metal, escudo",
          ("SAB", "CON", "DES", "INT", "CAR", "FUE"),
          _r(melee=1, distancia=1, magia=3, resistencia=1, apoyo=2, naturaleza=3),
          "Un guardián de la naturaleza que lanza hechizos, invoca animales y se transforma en bestias.",
          "Empieza usando Forma salvaje para pelear de cerca antes de dominar los hechizos."),
    Clase("guerrero", "Guerrero", "Combatiente versátil y fiable", 1, 10,
          "Todas las armaduras y escudos",
          ("FUE", "CON", "DES", "SAB", "CAR", "INT"),
          _r(melee=3, distancia=2, resistencia=2, simple=3),
          "El especialista en armas: sencillo de jugar, resistente y con muchos ataques.",
          "La mejor opción para aprender las reglas sin preocuparte por los hechizos."),
    Clase("monje", "Monje", "Combatiente ágil sin armas", 2, 8,
          "Sin armadura",
          ("DES", "SAB", "CON", "FUE", "CAR", "INT"),
          _r(melee=3, magia=1, resistencia=1, sigilo=2, simple=1),
          "Un artista marcial veloz que golpea varias veces por turno y se mueve por el mapa con facilidad.",
          "Usa los puntos de ki para ataques extra y para escapar de situaciones peligrosas."),
    Clase("paladin", "Paladín", "Tanque con daño explosivo y apoyo", 1, 10,
          "Todas las armaduras y escudos",
          ("FUE", "CAR", "CON", "SAB", "DES", "INT"),
          _r(melee=3, magia=1, resistencia=3, apoyo=2, social=2, simple=3),
          "Un caballero sagrado con armadura pesada que castiga con daño radiante y protege a sus aliados.",
          "Guarda tus espacios de hechizo para Castigo divino: es lo que más daño aporta."),
    Clase("explorador", "Explorador", "Cazador a distancia y rastreador", 2, 10,
          "Ligera y media, escudo",
          ("DES", "SAB", "CON", "FUE", "INT", "CAR"),
          _r(melee=1, distancia=3, magia=1, sigilo=2, naturaleza=3, simple=1),
          "Un cazador con arco y un compañero animal, experto en terrenos salvajes.",
          "Elige un arco y mantén la distancia; tu compañero animal aguanta el daño."),
    Clase("picaro", "Pícaro", "Sigilo y daño por sorpresa", 2, 8,
          "Ligera",
          ("DES", "CON", "SAB", "INT", "CAR", "FUE"),
          _r(melee=2, distancia=2, sigilo=3, social=2, simple=1),
          "Un especialista en sigilo, trampas y cerraduras que hace mucho daño con el ataque furtivo.",
          "Busca siempre tener ventaja o un aliado junto al enemigo para activar el ataque furtivo."),
    Clase("hechicero", "Hechicero", "Lanzador de hechizos de gran poder", 2, 6,
          "Sin armadura",
          ("CAR", "CON", "DES", "SAB", "INT", "FUE"),
          _r(distancia=2, magia=3, social=2, simple=1),
          "Un lanzador con magia innata: pocos hechizos, pero muy potentes y modificables.",
          "Es frágil: mantente lejos de los enemigos y deja que tus aliados los frenen."),
    Clase("brujo", "Brujo", "Daño a distancia con pacto sobrenatural", 2, 8,
          "Ligera",
          ("CAR", "CON", "DES", "SAB", "INT", "FUE"),
          _r(melee=1, distancia=3, magia=3, social=2, simple=1),
          "Alguien que hizo un pacto con un ser poderoso a cambio de magia y habilidades especiales.",
          "Descansar recupera tus hechizos, así que usa Descarga sobrenatural sin miedo."),
    Clase("mago", "Mago", "Maestro de hechizos con más variedad", 3, 6,
          "Sin armadura",
          ("INT", "CON", "DES", "SAB", "CAR", "FUE"),
          _r(distancia=2, magia=3, apoyo=2),
          "El lanzador más versátil: aprende muchísimos hechizos y resuelve casi cualquier situación.",
          "Es la clase con más decisiones; recomendable cuando ya conoces los conceptos básicos."),
)

CLASES_POR_SLUG = {c.slug: c for c in CLASES}


PREGUNTAS = (
    Pregunta(1, "Cuando empieza una pelea, ¿qué prefieres hacer?", (
        Opcion("Meterme al frente y pegar de cerca", dict(melee=2, resistencia=1)),
        Opcion("Atacar desde lejos con un arco o hechizos", dict(distancia=2, magia=1)),
        Opcion("Pasar desapercibido y atacar por sorpresa", dict(sigilo=2, distancia=1)),
        Opcion("Ayudar y proteger a mis compañeros", dict(apoyo=2, magia=1)),
    )),
    Pregunta(2, "¿Qué te atrae más para tu personaje?", (
        Opcion("Armas y armaduras", dict(melee=2, magia=-1)),
        Opcion("Magia poderosa", dict(magia=2)),
        Opcion("Un poco de armas y un poco de magia", dict(melee=1, magia=1)),
        Opcion("Animales y poderes de la naturaleza", dict(naturaleza=2, magia=1)),
    )),
    Pregunta(3, "¿Qué tan resistente quieres que sea tu personaje?", (
        Opcion("Muy resistente, que aguante muchos golpes", dict(resistencia=2)),
        Opcion("Equilibrado", dict(resistencia=1)),
        Opcion("Frágil, pero que haga mucho daño desde lejos", dict(resistencia=-1, distancia=1)),
    )),
    Pregunta(4, "¿Cuánto quieres pensar durante los combates?", (
        Opcion("Lo mínimo: quiero algo simple y directo", dict(simple=3)),
        Opcion("Algunas decisiones, pero sin complicarme", dict(simple=1)),
        Opcion("Me gusta planificar y tener muchas opciones", dict(simple=-2)),
    )),
    Pregunta(5, "Un guardia te bloquea el paso. ¿Qué haces?", (
        Opcion("Hablo y trato de convencerlo", dict(social=2)),
        Opcion("Lo intimido para que se aparte", dict(melee=1, social=1, resistencia=1)),
        Opcion("Busco otra forma de entrar sin que me vea", dict(sigilo=2)),
        Opcion("Lo derroto por la fuerza", dict(melee=2)),
    )),
    Pregunta(6, "¿Qué papel te gustaría tener en el grupo?", (
        Opcion("Hacer el mayor daño posible", dict(melee=1, distancia=1, magia=1)),
        Opcion("Proteger al equipo en primera línea", dict(resistencia=2, apoyo=1)),
        Opcion("Curar, apoyar y dar ventajas", dict(apoyo=3)),
        Opcion("Explorar, abrir cerraduras y desactivar trampas", dict(sigilo=2)),
    )),
    Pregunta(7, "¿Qué fuente de poder te resulta más interesante?", (
        Opcion("Animales y la naturaleza", dict(naturaleza=3)),
        Opcion("La fe y un poder divino", dict(apoyo=1, resistencia=1, magia=1)),
        Opcion("Mi entrenamiento y mis habilidades", dict(melee=1, sigilo=1)),
        Opcion("Un pacto o un don misterioso", dict(magia=1, social=1)),
    )),
    Pregunta(8, "¿Qué personalidad describe mejor a tu héroe?", (
        Opcion("Valiente y honorable", dict(resistencia=1, melee=1, apoyo=1)),
        Opcion("Carismático y artista", dict(social=2, apoyo=1)),
        Opcion("Astuto y misterioso", dict(sigilo=2, social=1)),
        Opcion("Estudioso y curioso", dict(magia=2)),
    )),
)
