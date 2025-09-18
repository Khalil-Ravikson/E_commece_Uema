from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse

# Importa o modelo Product do models.py
from .models import Product,Customer, Order, OrderItem
import datetime

# Importa nossos novos modelos e formulários
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ShippingForm


from django.conf import settings # <- ADICIONE ESTA LINHA
import os # <- ADICIONE ESTA LINHA

def _get_cart_context(session):
    """
    Função de ajuda para obter o contexto do carrinho.
    Esta versão é mais robusta: ela ignora itens inválidos
    e limpa a sessão de "lixo" para evitar erros.
    """
 
    cart = session.get('cart', {})
    
    cart_items = []
    total_price = 0
    
    keys_to_remove_from_cart = []

    for product_id_str, item_data in cart.items():
        try:
            # Tenta converter o ID para um número. Se falhar (ex: ID vazio ''),
            # vai pular para o bloco 'except'.
            product_id_int = int(product_id_str)
            
            # Tenta encontrar o produto no banco. Se não encontrar,
            # vai pular para o bloco 'except'.
            product = Product.objects.get(id=product_id_int)
            
            # Se chegou até aqui, o item é válido.
            quantity = item_data.get('quantity', 1) # Usar .get() é mais seguro
            total_item_price = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_item_price
            })
            total_price += total_item_price

        # Captura os dois erros possíveis: ID inválido ou produto não existente
        except (ValueError, Product.DoesNotExist):
            # Se o item é inválido, marcamos ele para remoção do carrinho
            keys_to_remove_from_cart.append(product_id_str)
            continue
    
    # Se encontramos alguma chave inválida, limpamos o carrinho na sessão
    if keys_to_remove_from_cart:
        for key in keys_to_remove_from_cart:
            if key in cart:
                del cart[key]
        session['cart'] = cart # Salva o carrinho "limpo" de volta na sessão
    
    return {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_item_count': sum(item.get('quantity', 1) for item in cart.values())
    }

def product_list(request):
    """View da página principal."""
    products = Product.objects.all().order_by('-created_at')
    context = _get_cart_context(request.session)
    context['products'] = products
    return render(request, 'app/index.html', context)

def checkout_view(request):
    """View da página de checkout."""
    context = _get_cart_context(request.session)
    # Adicione aqui a lógica do formulário de checkout no futuro
    return render(request, 'app/checkout.html', context)

def add_to_cart(request, product_id):
    """Adiciona um produto ao carrinho ou incrementa sua quantidade."""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {'quantity': 1}
    
    messages.success(request, f'"{product.name}" foi adicionado ao carrinho!')
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

def remove_from_cart(request, product_id):
    """Remove um item completamente do carrinho."""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        messages.success(request, 'Item removido do carrinho.')
    
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

def update_cart(request, product_id, action):
    """Aumenta ou diminui a quantidade de um item no carrinho."""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if action == 'increase':
            cart[product_id_str]['quantity'] += 1
        elif action == 'decrease':
            cart[product_id_str]['quantity'] -= 1
            if cart[product_id_str]['quantity'] <= 0:
                del cart[product_id_str]
    
    messages.success(request, "Carrinho atualizado!")
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

def clear_session(request):
    """
    Uma view de utilidade para limpar completamente a sessão.
    Muito útil para debug durante o desenvolvimento.
    """
    request.session.flush()
    return HttpResponse("<h1>Sessão limpa com sucesso!</h1><a href='/'>Voltar para a loja</a>")

# ==========================================================
# NOVAS VIEWS DE AUTENTICAÇÃO
# ==========================================================

def register_view(request):
    """
    Processa a página de cadastro.
    """
    # Se o usuário já estiver logado, redireciona para a página principal
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        # Se o formulário foi enviado, processa os dados
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 1. Salva o novo usuário no banco
            user = form.save()
            
            # 2. Cria um 'Customer' associado a esse novo 'User'
            # Usamos o username como nome padrão, o usuário pode alterar depois
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email
            )

            # 3. Loga o usuário automaticamente
            login(request, user)
            
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('product_list')
        else:
            # Se o formulário for inválido, exibe os erros
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # Se for a primeira vez na página, mostra um formulário em branco
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'app/register.html', context)


def login_view(request):
    """
    Processa a página de login.
    """
    if request.user.is_authenticated:
        return redirect('product_list')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Pega o usuário do formulário
            user = form.get_user()
            # Loga o usuário na sessão
            login(request, user)
            # ===============================================
            # NOVA LÓGICA PARA O "LEMBRAR-ME"
            # ===============================================
            remember_me = form.cleaned_data.get('remember_me')
            if not remember_me:
                # Se "Lembrar-me" NÃO estiver marcado, a sessão expira quando o navegador fechar.
                request.session.set_expiry(0)
            else:
                # Se ESTIVER marcado, a sessão usará o tempo padrão do Django (geralmente 2 semanas).
                request.session.set_expiry(1209600) # Opcional: define 2 semanas em segundos
            # ===============================================
            messages.info(request, f'Bem-vindo de volta, {user.username}!')
            return redirect('product_list')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = CustomAuthenticationForm()

    context = {'form': form}
    return render(request, 'app/login.html', context)


def logout_view(request):
    """
    Desconecta o usuário.
    """
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('product_list')

def checkout_view(request):
    """
    Processa a página e a lógica de finalização de compra.
    """
    cart_context = _get_cart_context(request.session)
    cart_items = cart_context['cart_items']

    # Se o carrinho estiver vazio, redireciona para a loja
    if not cart_items:
        messages.info(request, "Seu carrinho está vazio.")
        return redirect('product_list')

    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            # 1. Obter ou Criar o Cliente
            if request.user.is_authenticated:
                customer = request.user.customer
            else:
                # Para convidados, usamos o email para identificar ou criar um cliente
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                customer, created = Customer.objects.get_or_create(email=email)
                if created:
                    customer.name = name
                    customer.save()

            # 2. Criar o Pedido (Order)
            order = Order.objects.create(
                customer=customer,
                complete=False # Marcamos como incompleto inicialmente
            )
            
            # 3. Criar os Itens do Pedido (OrderItem)
            for item in cart_items:
                OrderItem.objects.create(
                    product=item['product'],
                    order=order,
                    quantity=item['quantity']
                )

            # 4. Finalizar o Pedido
            order.transaction_id = datetime.datetime.now().timestamp() # ID de transação simples
            order.complete = True
            order.save()

            # 5. Limpar o carrinho da sessão
            if 'cart' in request.session:
                del request.session['cart']

            messages.success(request, 'Seu pedido foi finalizado com sucesso!')
            return redirect('product_list') # Idealmente, redirecionar para uma pág de "Obrigado"
            
    else:
        # Se for um GET, apenas exibe o formulário
        form = ShippingForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': cart_context['total_price']
    }
    return render(request, 'app/checkout.html', context)


def about(request):
    return render(request, "app/about.html")
def contact(request):
    return render(request, "app/contact.html")
def services(request):
    return render(request, "app/services.html")
def team(request):
    return render(request, "app/team.html")

