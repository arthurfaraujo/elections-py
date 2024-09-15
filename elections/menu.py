from elections.elec_data import candidate_by_code, candidates_by_city_and_role
from elections.view import gen_statistics_html, open_file
import os, time

def main():
  while True:
    display_menu()
    
    user_input = input("> ")
    match user_input:
      
      case "1":
        option_by_city_and_role()

      case "2":
        option_by_code()    

      case "3":
        option_gen_statistics()          

      case "0":
        print("Encerrando...")
        break
      
      case _:
        print("Opção inválida, tente de novo...")
        time.sleep(0.8)
        continue
      
      
def clear():
  os.system('clear||cls')
  
def validate_number(user_input: str) -> bool:
  """
  Valida se um input do usuário é um número.
  """
  if not user_input.isdecimal():
    print("Digite um número!")
    time.sleep(0.8)
    return False
  
  return True


def display_menu():
  clear()
  print(
'''Bem vindo(a) ao ElectionsAPE\n
1 - Listar candidato por município e cargo
2 - Exibir detalhes de um candidato a partir do código
3 - Gerar página com estatísticas interessantes sobre os candidatos
0 - Fechar aplicação\n
O que você deseja fazer?'''
  )
  

def option_by_city_and_role() -> None:
  """
  Opção do menu que lista os candidatos por município e cargo.
  """
  
  clear()
  print("Digite 'q' para voltar ao menu anterior.")
  
  city_code = input("Código numérico da cidade desejada: ")
  if city_code in "qQ":
    return
  
  if not validate_number(city_code):
    return option_by_city_and_role()
    
  role_code = input("Código numérico do cargo desejado: ")
  if role_code in "qQ": 
    return
  
  if not validate_number(role_code):
    return option_by_city_and_role()
  
  print(candidates_by_city_and_role(city_code, role_code).to_string(index=False))


def option_by_code() -> None:
  """
  Opção do menu que exibe detalhes de um candidato a partir do código.
  """
  clear()
  print("Digite 'q' para voltar ao menu anterior.")
  
  candidate_code = input("Código sequencial numérico do candidato desejado: ")
  if candidate_code in "qQ":
    return
  
  if not validate_number(candidate_code):
    return option_by_code()
  
  print(candidate_by_code(candidate_code).to_string(index=False))


def option_gen_statistics() -> None:
  """
  Opção do menu que gera uma página HTML com estatísticas sobre os candidatos.
  """
  clear()
  user_confirm = input("Deseja abrir a página com as estatísticas (S ou N)? ").upper()
  if user_confirm == "S":
    open_file(gen_statistics_html())    
  elif user_confirm not in "SN":
    print("Opção inválida...")
    time.sleep(0.8)
    option_gen_statistics()
    

if __name__ == "__main__":
  main()