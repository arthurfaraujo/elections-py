from elections.elec_data import getCandidatesByCityAndRole, getCandidateByCode

def main():
  while True:
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
    
    res = input("")
    
    if res == "1":
      clear()
      cityCode = int(input("Código numérico da cidade desejada: "))
      roleCode = int(input("Código numérico do cargo desejado: "))
      getCandidatesByCityAndRole(cityCode, roleCode)
      if not proceed(): break
      
    elif res == "2":
      clear()
      code = int(input("Código sequencial numérico do candidato desejado: "))
      getCandidateByCode(code)
      if not proceed(): break      
      
    elif res == "0":
      print("Encerrando...")
      break
    else:
      clear()
      print("Opção inválida, tente de novo...")
      
def clear():
  import os
  os.system('cls' if os.name == 'nt' else 'clear')
      
def proceed():
  cont = input("Continuar (S ou N)? ").strip().upper()
  if cont == "N": 
    return False
  elif cont not in "SN":
    print("Resposta inválida!")
    proceed()
  return True

if __name__ == "__main__":
  main()