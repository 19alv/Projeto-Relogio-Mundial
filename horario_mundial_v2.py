"""
Consultor de horários mundiais (versão 2).

- Saudação inicial (Bom dia / Boa tarde / Boa noite) conforme o horário local.
- Todos os continentes, com os principais países.
- Permite adicionar novos países ao continente correto; as adições são
  salvas em "paises_personalizados.json" e aparecem nas próximas consultas.
- Saída em linhas curtas, para não quebrar em telas/painéis estreitos.

Requer Python 3.9+. No Windows, instale também: pip install tzdata
"""

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, available_timezones

# Pasta do script (se __file__ não existir, como em alguns compiladores online,
# usa a pasta atual)
try:
    PASTA = Path(__file__).resolve().parent
except NameError:
    PASTA = Path.cwd()

ARQUIVO_PERSONALIZADO = PASTA / "paises_personalizados.json"

# Estrutura: continente -> { país: fuso horário IANA (geralmente da capital) }
PAISES_BASE = {
    "América do Sul": {
        "Brasil": "America/Sao_Paulo",
        "Argentina": "America/Argentina/Buenos_Aires",
        "Chile": "America/Santiago",
        "Colômbia": "America/Bogota",
        "Peru": "America/Lima",
        "Venezuela": "America/Caracas",
        "Uruguai": "America/Montevideo",
        "Paraguai": "America/Asuncion",
        "Bolívia": "America/La_Paz",
        "Equador": "America/Guayaquil",
    },
    "América do Norte": {
        "Estados Unidos (Nova York)": "America/New_York",
        "Estados Unidos (Los Angeles)": "America/Los_Angeles",
        "Canadá (Toronto)": "America/Toronto",
        "México": "America/Mexico_City",
    },
    "América Central e Caribe": {
        "Cuba": "America/Havana",
        "Panamá": "America/Panama",
        "Costa Rica": "America/Costa_Rica",
        "Jamaica": "America/Jamaica",
        "República Dominicana": "America/Santo_Domingo",
        "Guatemala": "America/Guatemala",
    },
    "Europa": {
        "Reino Unido": "Europe/London",
        "França": "Europe/Paris",
        "Alemanha": "Europe/Berlin",
        "Espanha": "Europe/Madrid",
        "Portugal": "Europe/Lisbon",
        "Itália": "Europe/Rome",
        "Países Baixos": "Europe/Amsterdam",
        "Suíça": "Europe/Zurich",
        "Suécia": "Europe/Stockholm",
        "Grécia": "Europe/Athens",
        "Turquia": "Europe/Istanbul",
        "Rússia (Moscou)": "Europe/Moscow",
    },
    "África": {
        "Egito": "Africa/Cairo",
        "África do Sul": "Africa/Johannesburg",
        "Nigéria": "Africa/Lagos",
        "Quênia": "Africa/Nairobi",
        "Marrocos": "Africa/Casablanca",
        "Etiópia": "Africa/Addis_Ababa",
        "Argélia": "Africa/Algiers",
        "Gana": "Africa/Accra",
        "Angola": "Africa/Luanda",
        "Moçambique": "Africa/Maputo",
    },
    "Ásia": {
        "Japão": "Asia/Tokyo",
        "China": "Asia/Shanghai",
        "Coreia do Sul": "Asia/Seoul",
        "Índia": "Asia/Kolkata",
        "Emirados Árabes Unidos": "Asia/Dubai",
        "Arábia Saudita": "Asia/Riyadh",
        "Israel": "Asia/Jerusalem",
        "Tailândia": "Asia/Bangkok",
        "Singapura": "Asia/Singapore",
        "Indonésia": "Asia/Jakarta",
        "Filipinas": "Asia/Manila",
        "Paquistão": "Asia/Karachi",
        "Irã": "Asia/Tehran",
    },
    "Oceania": {
        "Austrália (Sydney)": "Australia/Sydney",
        "Austrália (Perth)": "Australia/Perth",
        "Nova Zelândia": "Pacific/Auckland",
        "Fiji": "Pacific/Fiji",
        "Papua-Nova Guiné": "Pacific/Port_Moresby",
        "Samoa": "Pacific/Apia",
    },
    "Antártida": {
        "Base McMurdo (EUA/Nova Zelândia)": "Antarctica/McMurdo",
        "Base Palmer (EUA)": "Antarctica/Palmer",
        "Base Casey (Austrália)": "Antarctica/Casey",
    },
}


# ----------------------------------------------------------------------------
# Persistência
# ----------------------------------------------------------------------------
def carregar_dados() -> dict:
    """Junta a base padrão com os países adicionados pelo usuário."""
    dados = {continente: dict(paises) for continente, paises in PAISES_BASE.items()}

    if ARQUIVO_PERSONALIZADO.exists():
        try:
            extras = json.loads(ARQUIVO_PERSONALIZADO.read_text(encoding="utf-8"))
            for continente, paises in extras.items():
                if continente in dados:
                    dados[continente].update(paises)
        except (json.JSONDecodeError, OSError):
            print("Aviso: não foi possível ler o arquivo de países personalizados.")
    return dados


def salvar_pais(continente: str, pais: str, fuso: str) -> None:
    """Grava o novo país no arquivo JSON, no continente correto."""
    extras = {}
    if ARQUIVO_PERSONALIZADO.exists():
        try:
            extras = json.loads(ARQUIVO_PERSONALIZADO.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            extras = {}
    extras.setdefault(continente, {})[pais] = fuso
    try:
        ARQUIVO_PERSONALIZADO.write_text(
            json.dumps(extras, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError:
        print("Aviso: não foi possível salvar o arquivo. O país vale só nesta sessão.")


# ----------------------------------------------------------------------------
# Lógica de horário
# ----------------------------------------------------------------------------
def saudacao(hora: int) -> str:
    if 5 <= hora < 12:
        return "Bom dia"
    if 12 <= hora < 18:
        return "Boa tarde"
    return "Boa noite"


def agora_em(fuso: str) -> datetime:
    return datetime.now(ZoneInfo(fuso))


def mostrar_horario(pais: str, fuso: str) -> None:
    """Mostra o horário em duas linhas curtas para não quebrar a linha."""
    agora = agora_em(fuso)
    print(f"\n{pais}")
    print(f"  {agora:%d/%m/%Y %H:%M} - {saudacao(agora.hour)} lá")


# ----------------------------------------------------------------------------
# Interface de texto
# ----------------------------------------------------------------------------
def escolher_continente(dados: dict, titulo: str = "Escolha o continente"):
    continentes = list(dados.keys())
    print(f"\n{titulo}:")
    for i, nome in enumerate(continentes, 1):
        print(f"  {i} - {nome} ({len(dados[nome])})")
    print("  0 - Voltar")

    escolha = input("Opção: ").strip()
    if escolha.isdigit() and 1 <= int(escolha) <= len(continentes):
        return continentes[int(escolha) - 1]
    return None


def consultar(dados: dict) -> None:
    continente = escolher_continente(dados)
    if not continente:
        return

    paises = list(dados[continente].items())
    print(f"\n{continente}:")
    for i, (pais, _) in enumerate(paises, 1):
        print(f"  {i:>2} - {pais}")
    print("   t - Ver todos deste continente")
    print("   0 - Voltar")

    escolha = input("Opção: ").strip().lower()
    if escolha == "t":
        for pais, fuso in paises:
            mostrar_horario(pais, fuso)
    elif escolha.isdigit() and 1 <= int(escolha) <= len(paises):
        pais, fuso = paises[int(escolha) - 1]
        mostrar_horario(pais, fuso)


def consultar_todos(dados: dict) -> None:
    for continente, paises in dados.items():
        print(f"\n===== {continente} =====")
        for pais, fuso in paises.items():
            mostrar_horario(pais, fuso)


def pedir_fuso():
    """Pede um fuso IANA válido; permite buscar por parte do nome."""
    todos = sorted(available_timezones())
    while True:
        entrada = input(
            "Fuso (ex.: Asia/Kolkata) ou parte do nome\n"
            "para buscar (vazio cancela): "
        ).strip()
        if not entrada:
            return None
        if entrada in todos:
            return entrada

        achados = [z for z in todos if entrada.lower().replace(" ", "_") in z.lower()]
        if not achados:
            print("Nenhum fuso encontrado. Tente outro termo.")
            continue
        print("Fusos encontrados:")
        for i, z in enumerate(achados[:15], 1):
            print(f"  {i:>2} - {z}")
        if len(achados) > 15:
            print(f"  ... e mais {len(achados) - 15}. Refine a busca.")
        escolha = input("Número do fuso (Enter busca de novo): ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= min(15, len(achados)):
            return achados[int(escolha) - 1]


def adicionar(dados: dict) -> None:
    continente = escolher_continente(dados, "Adicionar em qual continente")
    if not continente:
        return

    pais = input("Nome do país (ou país/cidade): ").strip()
    if not pais:
        print("Nome vazio, operação cancelada.")
        return
    if pais in dados[continente]:
        print(f"'{pais}' já existe em {continente}.")
        return

    fuso = pedir_fuso()
    if not fuso:
        print("Operação cancelada.")
        return

    salvar_pais(continente, pais, fuso)
    dados[continente][pais] = fuso  # já disponível na próxima consulta
    print(f"\n'{pais}' adicionado em {continente}!")


def main() -> None:
    dados = carregar_dados()

    local = datetime.now().astimezone()
    print(f"{saudacao(local.hour)}! Bem-vindo ao")
    print("consultor de horários mundiais.")
    print(f"Seu horário local: {local:%d/%m/%Y %H:%M}")

    while True:
        print("\n===== MENU =====")
        print("  1 - Consultar por continente/país")
        print("  2 - Ver todos os países")
        print("  3 - Adicionar um país")
        print("  0 - Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            consultar(dados)
        elif opcao == "2":
            consultar_todos(dados)
        elif opcao == "3":
            adicionar(dados)
        elif opcao == "0":
            print(f"\n{saudacao(datetime.now().astimezone().hour)}! Até a próxima.")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
