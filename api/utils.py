import os
import qrcode
from io import BytesIO
from django.conf import settings
import re


def safe_filename(value: str) -> str:
    return re.sub(r'\W+', '_', value)


def create_qr_code_for_tables(organization_name: str, number: str):
    if settings.DEBUG:
        qr_data = f"http://localhost:8000/{organization_name}?t={number}/"
    else:
        qr_data = f"https://foodlistback.pythonanywhere.com/{organization_name}?t={number}/"

    qr_img = qrcode.make(qr_data)

    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)

    filename = f"qr_{organization_name}_{number}.png"
    relative_path = f"qr_codes/{filename}"
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Fayl mavjud bo'lmasa, saqlaymiz
    if not os.path.exists(full_path):
        with open(full_path, 'wb') as f:
            f.write(buffer.read())

    return relative_path
