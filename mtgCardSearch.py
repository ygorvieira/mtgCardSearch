#!/usr/bin/env python3

import sys
import requests
from urllib.parse import quote

API_URI = "https://api.scryfall.com/cards/named?fuzzy={}"


def buscar_regras(rulings_uri):
	headers = {
		"User-Agent": "mtg-cli-app/1.0"
	}

	try:
		response = requests.get(
			rulings_uri,
			headers=headers,
			timeout=10
		)

		if response.status_code != 200:
			return[]

		data = response.json()
	
		return data.get("data", [])

	except requests.RequestException:
		return []


def buscar_impressoes(prints_search_uri):
	headers = {
		"User-Agent": "mtg-cli-app/1.0"
	}

	try:
		response = requests.get(
			prints_search_uri,
			headers=headers,
			timeout=10
		)

		if response.status_code != 200:
			return []

		data = response.json()

		return data.get("data", [])

	except requests.RequestException:
		return []


def mostrar_impressoes(impressoes):
	print("\nColeções:")

	sets_exibidos = set()

	for carta in impressoes:
		set_name = carta.get("set_name")
		set_code = carta.get("set")

		chave = (set_name, set_code)

		if chave not in sets_exibidos:
			print(f" - {set_name} ({set_code.upper()})")
			sets_exibidos.add(chave)


def mostrar_formatos(legalities):
	print("\nFormatos válidos:")

	possui_formato = False

	for formato, status in legalities.items():
		if status == 'legal':
			print(f" - {formato}")
			possui_formato = True

	if not possui_formato:
		print(" Nenhum formato válido.")


def mostrar_regras(rulings):
	print("\nRegras:")

	if not rulings:
		print(" Nenhuma regra adicional encontrada.")
		return

	for ruling in rulings[:5]:
		published_at = ruling.get("published_at", "N/A")
		comment = ruling.get("comment", "")

		print(f"\n[{published_at}]")
		print(comment)


def buscar_carta(nome_carta):
	uri = API_URI.format(quote(nome_carta))

	headers = {
		"User-Agent": "mtg-cli-app/1.0"
	}

	try:
		response = requests.get(
			uri,
			headers=headers,
			timeout=10
		)

		if response.status_code != 200:
			print(f"Erro HTTP: {response.status_code}")
			print(response.text)
			return

		carta = response.json()

		oracle_id = carta.get("oracle_id")
		pt_carta = None
		if oracle_id:
			pt_search_uri = f"https://api.scryfall.com/cards/search?q=oracle_id%3A{oracle_id}+lang%3Apt&unique=cards"
			try:
				pt_resp = requests.get(pt_search_uri, headers=headers, timeout=10)
				if pt_resp.status_code == 200:
					pt_data = pt_resp.json()
					if pt_data.get("total_cards", 0) > 0:
						pt_card = pt_data["data"][0]
						if pt_card.get("lang") == "pt":
							pt_carta = pt_card
			except requests.RequestException:
				pass

		nome = (pt_carta.get("printed_name") or pt_carta.get("name")) if pt_carta else carta.get("name")
		descricao = (pt_carta.get("printed_text") or pt_carta.get("oracle_text")) if pt_carta else carta.get("oracle_text")

		print("=" * 60)
		print(f"Nome: {nome}")
		print(f"Custo de Mana: {carta.get('mana_cost')}")
		print(f"Tipo: {carta.get('type_line')}")
		print(f"Raridade: {carta.get('rarity')}")

		prints_search_uri = carta.get("prints_search_uri")

		if prints_search_uri:
			impressoes = buscar_impressoes(prints_search_uri)
			mostrar_impressoes(impressoes)
		
		if descricao:
			print("\nDescrição:")
			print(descricao)

		poder = carta.get("power")
		resistencia = carta.get("toughness")

		if poder and resistencia:
			print(f"\nPoder / Resistência: {poder}/{resistencia}")

		legalities = carta.get("legalities", {})
		mostrar_formatos(legalities)

		rulings_uri = carta.get("rulings_uri")

		if rulings_uri:
			rulings = buscar_regras(rulings_uri)
			mostrar_regras(rulings)

		print("\n" + "=" * 60)

	except requests.RequestException as e:
		print(f"Erro ao acessar API: {e}")


def main():
	if len(sys.argv) < 2:
		print("Uso:")
		print(f" python {sys.argv[0]} \"Nome da Carta\"")
		sys.exit(1)

	nome_carta = " ".join(sys.argv[1:])
	buscar_carta(nome_carta)


if __name__ == "__main__":
	main()
