#!/usr/bin/env pyython3

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
		published_at = ruling.get("publihed_at", "N/A")
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

		print("=" * 60)
		print(f"Nome: {carta.get('name')}")
		print(f"Custo de Mana: {carta.get('mana_cost')}")
		print(f"Tipo: {carta.get('type_line')}")
		print(f"Raridade: {carta.get('rarity')}")
		print(f"Coleção: {carta.get('set_name')}")
		
		oracle_text = carta.get("oracle_text")

		if oracle_text:
			print("\nDescrição:")
			print(oracle_text)

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

























































































