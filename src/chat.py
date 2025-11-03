from .search import search_prompt

def main():
  print("Bem-vindo ao chat! Digite sua pergunta ou 'sair, exit ou quit' para encerrar.")
  while True:
    user_input = input("Você: ")
    if user_input.lower() in {"sair", "exit", "quit"}:
      print("Encerrando o chat. Até mais!")
      break
    try:
      if not user_input.strip():
          print("Por favor, insira uma pergunta válida.")
          continue
      response = search_prompt(user_input)

      print(f"Assistente: {response}")
    except Exception as e:
      print(f"Erro ao processar a entrada: {e}")
      continue

if __name__ == "__main__":
    main()