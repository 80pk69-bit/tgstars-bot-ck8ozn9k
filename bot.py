from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.types import ContentType
import asyncio
import logging

BOT_TOKEN = "8722217381:AAEdSCNK7GwgcChvfBi0ZcAyEi3-U6EJfEs"
YOUR_CHAT_ID = 1371848407

PRODUCTS = {
    'IVKtUbmPC4mP': {'name': 'Минимальный (10GB)', 'price': 100},
    'IV8jvyldWANN': {'name': 'Стандарт (25GB)', 'price': 100},
    'IV10yvyfLy3e': {'name': 'Премиум (100+GB)', 'price': 100}
}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    args = message.text.split()
    if len(args) > 1 and args[1].startswith('stars_'):
        parts = args[1].replace('stars_', '').split('_')
        if len(parts) >= 2:
            order_id = parts[0]
            unique = parts[1]
            if order_id in PRODUCTS:
                product = PRODUCTS[order_id]
                prices = [LabeledPrice(label=f"Доступ к {product['name']}", amount=product['price'])]
                await bot.send_invoice(
                    chat_id=message.chat.id,
                    title=f"Premium Archive - {product['name']}",
                    description=f"Эксклюзивный контент ({product['name']})",
                    payload=f"{order_id}_{unique}",
                    provider_token="",
                    currency="XTR",
                    prices=prices,
                    start_parameter="stars_pay"
                )
            else:
                await message.answer("❌ Неверный заказ. Обратитесь в поддержку.")
        else:
            await message.answer("❌ Неверный формат ссылки.")
    else:
        await message.answer("👋 Используйте кнопки на сайте для оплаты.")

@dp.pre_checkout_query()
async def pre_checkout_query_handler(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(lambda msg: msg.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment_handler(message: types.Message):
    payment = message.successful_payment
    order_id = payment.payload.split('_')[0] if payment.payload else 'unknown'
    product_name = PRODUCTS.get(order_id, {}).get('name', 'Неизвестный товар')
    
    await bot.send_message(
        chat_id=YOUR_CHAT_ID,
        text=f"✅ ОПЛАТА STARS ПОЛУЧЕНА!\n"
             f"Товар: {product_name}\n"
             f"Сумма: {payment.total_amount} Stars\n"
             f"От: @{message.from_user.username or 'без username'}"
    )
    
    await message.answer(
        "✅ Оплата принята! Ссылка на архив будет отправлена в течение 24 часов.\n"
        "Пожалуйста, проверьте спам и напишите @support, если не получите."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
