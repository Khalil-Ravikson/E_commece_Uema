# Projeto E-commerce ShopNova (Uema Website)

Bem-vindo ao repositório do ShopNova, um projeto de e-commerce desenvolvido com Django como parte de um estudo acadêmico. A aplicação simula uma loja virtual completa, desde a listagem de produtos até o checkout final, com um sistema de autenticação de usuários.

---

## Funcionalidades Atuais

* **Listagem de Produtos:** Exibição de produtos com imagem, nome, descrição e preço a partir de um banco de dados.
* **Carrinho de Compras:**
    * Adição de produtos ao carrinho.
    * Carrinho persistente via Sessão do Django (modal flutuante).
    * Ajuste de quantidade (+/-) e remoção de itens diretamente no modal.
* **Sistema de Usuários:**
    * Cadastro de novas contas de cliente.
    * Login e Logout de usuários.
    * Barra de navegação dinâmica que se adapta ao status de login do usuário.
* **Checkout:**
    * Formulário para coleta de dados de entrega.
    * Criação de Pedidos (`Order`) e Itens de Pedido (`OrderItem`) no banco de dados após a finalização da compra.
    * Lógica para lidar com clientes registrados e convidados.
* **Painel de Administração:** Uso do Admin nativo do Django para gerenciar Produtos, Clientes e Pedidos.

---

## Tecnologias Utilizadas

* **Backend:** Python 3.10.12, Django 5.2.6
* **Banco de Dados:** PostgreSQL (desenvolvido com Docker, compatível com Supabase)
* **Frontend:** HTML5, Tailwind CSS, JavaScript (mínimo, para interatividade da UI)
* **Containerização:** Docker, Docker Compose

---

## Como Rodar o Projeto

Existem duas maneiras de rodar o projeto: usando Docker (recomendado) ou um ambiente virtual Python tradicional.

### Método 1: Usando Docker (Recomendado)

Este método é mais simples e garante que o ambiente seja idêntico em qualquer máquina.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Khalil-Ravikson/E_commece_Uema.git
    cd Uema_webSite
    ```

2.  **Crie o arquivo `.env`:**
    Copie o conteúdo do arquivo `.env.example` (se você criar um) ou crie um arquivo `.env` na raiz e adicione as seguintes variáveis (use as mesmas credenciais do `docker-compose.yml` para o banco local):
    ```ini
    SECRET_KEY=sua_chave_secreta_super_segura_aqui
    DEBUG=True
    DB_NAME=shopnova_db
    DB_USER=shopnova_user
    DB_PASSWORD=shopnova_password
    DB_HOST=db
    DB_PORT=5432
    ```

3.  **Construa e inicie os containers:**
    ```bash
    docker-compose up --build
    ```

4.  **Acesse o site** no seu navegador em `http://127.0.0.1:8000/`.

5.  Para criar um superusuário (para acessar o `/admin/`), abra outro terminal e rode:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

### Método 2: Ambiente Virtual Python (Tradicional)

1.  **Clone o repositório** e entre na pasta.

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o arquivo `.env`** como no método Docker. Certifique-se que `DB_HOST` seja `localhost` se estiver usando um banco de dados local não-dockerizado.

5.  **Aplique as migrações e inicie o servidor:**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    ```

---

## Atualizações Futuras (Roadmap Profissional)

Este projeto tem uma base sólida. Os próximos passos para torná-lo uma aplicação de nível profissional incluem:

* **Tarefas em Segundo Plano com Celery:**
    * Implementar o envio de e-mails de confirmação de pedido de forma assíncrona para não atrasar a resposta ao usuário.
    * Usar um Message Broker como o Redis.

* **Integração com APIs Externas:**
    * **Pagamentos:** Integrar um gateway de pagamento (Mercado Pago, PagSeguro, Stripe) para processar transações reais.
    * **Frete:** Conectar com a API dos Correios para cálculo de frete em tempo real.
    * **Endereços:** Usar uma API como a ViaCEP para autocompletar o endereço a partir do CEP.

* **Testes Automatizados:**
    * Escrever testes unitários e de integração com o framework de testes do Django para garantir a estabilidade do código e evitar regressões.

* **Deploy em Produção:**
    * Configurar a aplicação para rodar em um servidor de produção com Gunicorn e Nginx.
    * Usar um serviço de nuvem (Heroku, Render, DigitalOcean) para a hospedagem.

* **Performance e Otimização:**
    * Implementar cache com Redis para consultas frequentes.
    * Otimizar queries do banco de dados com `select_related` e `prefetch_related`.
    * Servir arquivos estáticos e de mídia através de um serviço de CDN (como AWS S3).