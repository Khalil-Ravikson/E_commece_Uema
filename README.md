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
---

## Roadmap Profissional e Próximos Passos

Este projeto possui uma base sólida. Os próximos passos para transformá-lo em uma aplicação de nível profissional incluem:

### 1. Tarefas em Segundo Plano com Celery
- **Objetivo:** Melhorar a performance e a experiência do usuário em tarefas lentas.
- **Ações:**
  - Implementar o envio de e-mails de confirmação de pedido de forma assíncrona (em segundo plano) usando **Celery** e um Message Broker como o **Redis**. Isso faz com que o usuário não precise esperar o envio do e-mail para ver a página de confirmação.
  - Usar para outras tarefas demoradas, como processamento de imagens ou geração de relatórios.

### 2. Integração com APIs Externas
- **Objetivo:** Adicionar funcionalidades do mundo real que dependem de serviços de terceiros.
- **Ações:**
  - **Pagamentos:** Integrar um gateway de pagamento (ex: **Mercado Pago, PagSeguro, Stripe**) para processar transações com Cartão de Crédito e PIX.
  - **Frete:** Conectar com a API dos **Correios** para cálculo de frete em tempo real baseado no CEP.
  - **Endereços:** Usar uma API como a **ViaCEP** no formulário de checkout para autocompletar o endereço a partir do CEP digitado pelo usuário.

### 3. Melhorias na Experiência do Usuário (UX)
- **Objetivo:** Tornar o site mais dinâmico e fácil de usar.
- **Ações:**
  - **Atualizações sem Recarregar a Página (AJAX):** Reintroduzir a lógica de atualizar o carrinho sem recarregar a página, usando uma biblioteca como **HTMX** (para manter a lógica no backend) ou **JavaScript com a API Fetch** (para mais controle no frontend).
  - **Busca de Produtos:** Implementar uma barra de busca funcional.
  - **Filtros e Paginação:** Adicionar filtros para produtos (por categoria, preço) e paginação na página de produtos.

### 4. Deploy em Produção
- **Objetivo:** Colocar a aplicação no ar de forma segura e escalável.
- **Ações:**
  - Configurar a aplicação para rodar em um servidor de produção com **Gunicorn** (servidor de aplicação) e **Nginx** (servidor web).
  - Empacotar toda a aplicação em containers **Docker** para garantir consistência entre os ambientes.
  - Hospedar em um serviço de nuvem como **Render.com, Heroku, ou DigitalOcean**.

### 5. Ferramentas de Desenvolvimento e Testes
- **Objetivo:** Aumentar a qualidade e a confiabilidade do código.
- **Ações:**
  - **Testes Automatizados:** Escrever testes unitários e de integração com o framework de testes do Django para validar as funcionalidades do carrinho e do checkout.
  - **Tunelamento com Ngrok:** Usar o **Ngrok** para criar um túnel seguro para o seu servidor de desenvolvimento local. Isso é essencial para testar serviços que precisam de um webhook (uma URL pública), como gateways de pagamento, que precisam notificar seu site de que um pagamento foi aprovado.
  - **Django Debug Toolbar:** Instalar e configurar esta ferramenta para analisar a performance, as queries do banco de dados e outras informações vitais durante o desenvolvimento.