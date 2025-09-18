from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User # Importa o modelo de usuário padrão do Django


class Product(models.Model):
    """
    Representa um produto na loja. Cada atributo aqui
    será uma coluna na tabela do banco de dados.
    """
    
    # Campo para o nome do produto. `max_length` é obrigatório.
    name = models.CharField("Nome", max_length=120)

    # `TextField` é para textos longos. `blank=True` significa que não é obrigatório.
    description = models.TextField("Descrição", blank=True)

    # `DecimalField` é ESSENCIAL para dinheiro, pois evita erros de arredondamento.
    price = models.DecimalField(
        "Preço",
        max_digits=10,      # Número máximo de dígitos no total
        decimal_places=2,   # Quantos desses dígitos são casas decimais
        validators=[MinValueValidator(0.01)] # Impede preços negativos ou zero
    )

    # `ImageField` para o upload de imagens.
    # `upload_to='products/'` diz ao Django para salvar as imagens na pasta 'media/products/'.
    image = models.ImageField(
        "Imagem",
        upload_to='products/',
        default='products/default.png' # Uma imagem padrão, caso nenhuma seja enviada
    )

    # `PositiveIntegerField` garante que o estoque nunca será um número negativo.
    stock = models.PositiveIntegerField("Estoque", default=1)

    # `auto_now_add=True` salva a data e hora exatas de quando o produto foi criado.
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    def __str__(self):
        """
        Define como o objeto será exibido, por exemplo, no painel de administração.
        É muito útil para legibilidade.
        """
        return f"{self.name} (R$ {self.price})"

    class Meta:
        """
        Metadados do modelo. Usado para configurações como ordenação
        e nomes mais amigáveis no painel de administração.
        """
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-created_at'] # Ordena os produtos do mais novo para o mais antigo


# Nota: Para que o campo ImageField funcione corretamente, você precisa ter a biblioteca Pillow instalada.
# Você pode instalá-la via pip:
# pip install Pillow

# Além disso, certifique-se de configurar corretamente o MEDIA_URL e MEDIA_ROOT no seu settings.py
# para servir arquivos de mídia durante o desenvolvimento.


# ==========================================================
# NOVOS MODELOS ABAIXO
# ==========================================================

class Customer(models.Model):
    """
    Representa um cliente, que pode ou não ser um usuário registrado.
    """
    # Relação um-para-um com o usuário do Django.
    # `null=True` e `blank=True` permitem que clientes existam sem uma conta de usuário (convidados).
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Usuário")
    
    name = models.CharField("Nome", max_length=200, null=True)
    email = models.EmailField("E-mail", max_length=200, null=True)

    def __str__(self):
        if self.user:
            return self.user.username
        return self.email or "Cliente Convidado"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Order(models.Model):
    """
    Representa um pedido de compra no e-commerce.
    """
    # Chave estrangeira para o Cliente. Se um cliente for deletado, seus pedidos também serão.
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Cliente")
    
    date_ordered = models.DateTimeField("Data do Pedido", auto_now_add=True)
    complete = models.BooleanField("Finalizado", default=False)
    transaction_id = models.CharField("ID da Transação", max_length=200, null=True)

    def __str__(self):
        return f"Pedido #{self.id}"

    @property
    def get_cart_total(self):
        """Calcula o total do pedido somando os subtotais de todos os itens."""
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        """Calcula a quantidade total de itens no pedido."""
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class OrderItem(models.Model):
    """
    Representa um item específico dentro de um pedido.
    """
    # Chave estrangeira para o Produto. Se o produto for deletado, o item do pedido também será.
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Produto")
    
    # Chave estrangeira para o Pedido.
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Pedido")
    
    quantity = models.IntegerField("Quantidade", default=0, null=True, blank=True)
    date_added = models.DateTimeField("Data de Adição", auto_now_add=True)

    @property
    def get_total(self):
        """Calcula o subtotal do item (preço * quantidade)."""
        total = self.product.price * self.quantity
        return total

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"