from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pathlib import Path
# Sample product data (would come from your database in production)

BASE_DIR = Path(__file__).resolve().parent.parent

def load_products():
    file_path = BASE_DIR / "app/static/app/data/products.json"
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

# In-memory cart storage (replace with database in production)
user_carts = {}

@csrf_exempt
def get_products(request):
    products = load_products()
    return JsonResponse({"products": products})

@csrf_exempt
def cart(request, user_id):
    products = load_products()
    """Endpoint to handle cart operations"""
    if request.method == 'GET':
        # Get user's cart
        cart_items = user_carts.get(user_id, [])
        return JsonResponse({"cart": cart_items})
    
    elif request.method == 'POST':
        # Add item to cart
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)
        
        if user_id not in user_carts:
            user_carts[user_id] = []
            
        # Check if product already in cart
        cart_item = next((item for item in user_carts[user_id] if item['id'] == product_id), None)
        
        if cart_item:
            cart_item['quantity'] += quantity
        else:
            user_carts[user_id].append({
                "id": product['id'],
                "name": product['name'],
                "price": product['price'],
                "quantity": quantity,
                "image": product['image']
            })
            
        return JsonResponse({"success": True, "cart": user_carts[user_id]})
    
    elif request.method == 'DELETE':
        # Remove item from cart
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        if user_id in user_carts:
            user_carts[user_id] = [item for item in user_carts[user_id] if item['id'] != product_id]
            
        return JsonResponse({"success": True, "cart": user_carts.get(user_id, [])})

orders = []  # lista de pedidos (substituir por DB depois)

@csrf_exempt
def checkout(request, user_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        required_fields = ['name', 'email', 'address', 'payment_method']
        if not all(field in data for field in required_fields):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        cart_items = user_carts.get(user_id, [])
        if not cart_items:
            return JsonResponse({"error": "Cart is empty"}, status=400)

        total = sum(item['price'] * item['quantity'] for item in cart_items)

        # Gera número do pedido
        import random
        order_number = random.randint(10000, 99999)

        # Cria pedido
        order = {
            "order_number": order_number,
            "user_id": user_id,
            "customer": {
                "name": data['name'],
                "email": data['email'],
                "address": data['address'],
                "payment_method": data['payment_method'],
            },
            "items": cart_items,
            "total": total,
        }
        orders.append(order)

        # Limpa carrinho
        user_carts[user_id] = []

        # ======================================================================
        print("-----------------------------------------")
        print(f"✅ Pedido #{order_number} recebido com sucesso!")
        print(f"Cliente: {data['name']}")
        print(f"Total de pedidos na memória agora: {len(orders)}")
        print("Lista de todos os pedidos:")
        # O import json e o indent=2 servem para imprimir o dicionário de forma bonita
        print(json.dumps(orders, indent=2, ensure_ascii=False))
        print("-----------------------------------------")
        # ======================================================================
        return JsonResponse({
            "success": True,
            "order_number": order_number,
            "total": total,
            "items": cart_items,
            "message": "Pedido confirmado com sucesso!"
        })
    return JsonResponse({"error": "Invalid request method"}, status=405)