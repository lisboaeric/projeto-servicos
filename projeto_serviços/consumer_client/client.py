import requests

def create_user(username, password):
    url = "http://user-service:8001/create_user_rpc/"
    user_data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, data=user_data)
        response.raise_for_status()
        print("Usuário criado com sucesso")
    except requests.exceptions.RequestException as e:
        print(f"Falha ao criar usuário: {e}")

def create_product(name, description, price):
    url = "http://product-service:8002/create_product_rpc/"
    product_data = {
        "name": name,
        "description": description,
        "price": price
    }
    try:
        response = requests.post(url, data=product_data)
        response.raise_for_status()
        print("Produto criado com sucesso")
    except requests.exceptions.RequestException as e:
        print(f"Falha ao criar produto: {e}")

if __name__ == "__main__":
    while True:
        print("\nEscolha a operação desejada:")
        print("1. Criar novo usuário")
        print("2. Criar novo produto")
        print("3. Sair")

        choice = input("Opção: ")

        if choice == "1":
            username = input("Digite o username do novo usuário: ")
            password = input("Digite a senha do novo usuário: ")
            create_user(username, password)
        elif choice == "2":
            name = input("Digite o nome do novo produto: ")
            description = input("Digite a descrição do novo produto: ")
            price = float(input("Digite o preço do novo produto: "))
            create_product(name, description, price)
        elif choice == "3":
            print("Encerrando cliente.")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")