from elections.elec_data import candidate_by_code, candidates_by_city_and_role, goods_by_code, social_medias_by_code
from elections.view import gen_statistics_html, open_file, create_html_dir, open_url
from elections.cities_html import start_flask
from pandas import DataFrame
import os
import time
import threading


def main():
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
    
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

            case "4":
                clear()
                print("Webserver iniciado no ip: http://127.0.0.1:5000/ abra o navegador para acessar o site.")
                open_url("http://127.0.0.1:5000/")
                input("\nPressione qualquer tecla para voltar ao menu...")
                
            case "0":
                print("Encerrando...")
                if flask_thread:
                    os._exit(0)  # Encerra o Flask
                break
            
            case _:
                print("Opcao invalida, tente de novo...")
                time.sleep(0.8)

      
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
1 - Listar candidato por municipio e cargo
2 - Exibir detalhes de um candidato a partir do codigo
3 - Gerar pagina com estatisticas interessantes sobre os candidatos
4 - Abrir pagina dos municipios
0 - Fechar aplicacao\n
O que voce deseja fazer?'''
    )


def option_by_city_and_role() -> None:
    """
    Opção do menu que lista os candidatos por município e cargo.
    """
    clear()
    print("Digite 'q' para voltar ao menu anterior.")
    
    city_code = input("Codigo numerico da cidade desejada: ").lower()
    if city_code == "q":
        return
    
    if not validate_number(city_code):
        return option_by_city_and_role()
        
    role_code = input("Codigo numerico do cargo desejado: ").lower()
    if role_code == "q": 
        return
    
    if not validate_number(role_code):
        return option_by_city_and_role()
    
    print()
    print(treat_empty_df(candidates_by_city_and_role(int(city_code), int(role_code)), "Municipio ou cargo nao encontrado!"))

    input("\nPressione qualquer tecla para voltar ao menu...")


def option_by_code() -> None:
    """
    Opção do menu que exibe detalhes de um candidato a partir do código.
    """
    clear()
    print("Digite 'q' para voltar ao menu anterior.")
    
    candidate_code = input("Codigo sequencial numerico do candidato desejado: ").lower()
    if candidate_code == "q":
        return
    
    if not validate_number(candidate_code):
        return option_by_code()
    
    print()
    print(treat_empty_df(candidate_by_code(int(candidate_code)), "Candidato nao encontrado!"))
    print("\nBens do candidato(a):")
    print(treat_empty_df(goods_by_code(int(candidate_code)), "Nem um bem encontrado!"))
    print("\nRedes sociais do candidato(a):")
    print(treat_empty_df(social_medias_by_code(int(candidate_code)), "Nem uma rede social encontrada!"))

    input("\nPressione qualquer tecla para voltar ao menu...")


def option_gen_statistics() -> None:
    """
    Opção do menu que gera uma página HTML com estatísticas sobre os candidatos.
    """
    clear()
    user_confirm = input("Deseja abrir a pagina com as estatisticas (S ou N)? ").lower()
    if user_confirm == "s":
        create_html_dir()
        open_file(gen_statistics_html())    
    elif user_confirm == "n":
        return
    elif user_confirm != "n":
        print("Opcao invalida...")
        time.sleep(0.8)
        option_gen_statistics()
    
    input("\nPressione qualquer tecla para voltar ao menu...")
    
def treat_empty_df(df: DataFrame, message: str):
    return df.to_string(index=False) if not df.empty else message 


if __name__ == "__main__":
    main()
