from elections.elec_data import candidate_by_code, candidates_by_city_and_role
from elections.view import gen_statistics_html, open_file

def main():
  while True:
    display_menu()
    
    res = input("")
    
    if res == "1":
      option_1()
      
    elif res == "2":
      option_2()    
      
    elif res == "3":
      option_3()          
      
    elif res == "0":
      print("Encerrando...")
      break
    else:
      clear()
      print("Opção inválida, tente de novo...")
      
    if not proceed(): break
      
def clear():
  import os
  os.system('cls' if os.name == 'nt' else 'clear')
      
def proceed() -> bool:
  cont = input("Continuar (S ou N)? ").strip().upper()
  if cont == "N": 
    return False
  elif cont not in "SN":
    print("Resposta inválida!")
    proceed()
  return True

def display_menu():
  clear()
  print(
    '''
  Bem vindo(a) ao ElectionsAPE\n
  Opções:
  1 - Listar candidato por município e cargo
  2 - Exibir detalhes de um candidato a partir do código
  3 - Gerar página com estatísticas interessantes sobre os candidatos
  0 - Fechar aplicação\n
  O que você deseja fazer?''', end=" "
  )
  
def option_1():
  clear()
  cityCode = int(input("Código numérico da cidade desejada: "))
  roleCode = int(input("Código numérico do cargo desejado: "))
  print(candidates_by_city_and_role(cityCode, roleCode).to_string(index=False))

def option_2():
  clear()
  code = int(input("Código sequencial numérico do candidato desejado: "))
  print(candidate_by_code(code).to_string(index=False))

def option_3():
  clear()
  res = input("Deseja abrir a página com as estatísticas (S ou N)? ").upper()
  if res == "S":
    open_file(gen_statistics_html())    
  elif res not in "SN":
    print("Opção inválida...")
    option_3()
    

if __name__ == "__main__":
  main()