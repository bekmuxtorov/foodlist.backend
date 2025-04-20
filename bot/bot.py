from telegram import ReplyKeyboardRemove
import random
import string
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup

from django.conf import settings

from eateries import models
from .utils import create_jwt_token

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    user_profile = models.UserProfile.objects.filter(
        telegram_id=chat_id).first()

    if user_profile:
        update.message.reply_text(
            f"🎉 Xush kelibsiz, {user.first_name} 🎉\n\n✅ Siz allaqachon ro'yxatdan o'tgansiz"
        )
        return

    update.message.reply_text(
        f"🎉 Xush kelibsiz, {user.first_name} 🎉 \n\nAvtorizatsiyani yakunlash va bot imkoniyatlaridan foydalanish uchun tugmani bosing\n\n👇 Kontaktni yuboring 👇\n\nAvtorizatsiya nima beradi:\n✅ Shaxsiylashtirilgan ma'lumotlar va sozlamalar\n✅ Ma'lumotlarni qayta kiritmasdan qulay o'zaro aloqa",
        reply_markup=ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(
                        "📞 Telefon raqamni jo'natish",
                        request_contact=True
                    )
                ]
            ],
            one_time_keyboard=True
        )
    )


def phone_number(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    phone_number = update.message.contact.phone_number

    user_profile = models.UserProfile.objects.filter(
        phone_number=phone_number).first()
    if user_profile:
        update.message.reply_text(
            f"🎉 Xush kelibsiz, {user.first_name} 🎉\n\n✅ Siz allaqachon ro'yxatdan o'tgansiz"
        )
        return

    try:
        TOKEN_VALIDITY_PERIOD = settings.TOKEN_VALIDITY_PERIOD
        new_user = models.UserProfile.objects.create(
            full_name=user.full_name,
            phone_number=phone_number,
            telegram_id=user.id,
            is_active=True
        )
        new_user.auth_token = create_jwt_token(
            user=new_user,
            hours=TOKEN_VALIDITY_PERIOD
        )
        new_user.set_token_expiry(hours=TOKEN_VALIDITY_PERIOD)
        new_user.save()
        update.message.reply_text(
            f"🎉 Tabriklaymiz, {user.first_name} 🎉\n\n✅ Siz roʻyxatdan oʻtdingiz!"
        )
    except Exception as e:
        print(f"Error creating user profile: {e}")
        update.message.reply_text(
            "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
        )
        return


def send_confirmation_message_to_user(user_id):
    try:
        message = "🔔 Tizimga kirishingizni tasdiqlang:"
        bot.send_message(
            chat_id=user_id,
            text=message,
            reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(
                            "✅Tasdiqlash",
                        ),
                        KeyboardButton(
                            "🚫Bekor qilish",
                        )
                    ]
                ],
                one_time_keyboard=True,
                resize_keyboard=True,
                row_width=2,

            )
        )
    except Exception as e:
        print(f"Error sending message: {e}")


def keyboards_handle_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_profile = models.UserProfile.objects.filter(
        telegram_id=user.id
    ).first()
    if not user_profile:
        return

    user_response = update.message.text
    if user_response == "✅Tasdiqlash":
        TOKEN_VALIDITY_PERIOD = settings.TOKEN_VALIDITY_PERIOD
        update.message.reply_text(
            "✅ Siz loginingizni muvaffaqiyatli tasdiqladingiz!\n\nEndi siz saytga kirishingiz va ishlashni davom ettirishingiz mumkin.\nXizmatimizdan foydalanganingiz uchun tashakkur!",
            reply_markup=ReplyKeyboardRemove()
        )
        if not user_profile.is_token_valid():
            user_profile.is_active = True
            user_profile.auth_token = create_jwt_token(
                user=user_profile,
                hours=TOKEN_VALIDITY_PERIOD
            )
            user_profile.set_token_expiry(TOKEN_VALIDITY_PERIOD)
            user_profile.save()

    elif user_response == "🚫Bekor qilish":
        update.message.reply_text(
            "🚫 Siz tizimga kirishni rad etdingiz!",
            reply_markup=ReplyKeyboardRemove()
        )
        user_profile.is_active = False
        user_profile.save()

    else:
        update.message.reply_text(
            "Iltimos, tasdiqlash yoki bekor qilishni tanlang."
        )


phone_handler = MessageHandler(Filters.contact, phone_number)
keyboards_handler = MessageHandler(
    Filters.text & ~Filters.command,
    keyboards_handle_message
)


def run_bot():
    updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(phone_handler)
    dp.add_handler(keyboards_handler)

    updater.start_polling()
    updater.idle()
