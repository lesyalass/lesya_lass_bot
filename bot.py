import os

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    TOKEN = "7544393183:AAFbLdQ8F1A4JKOZtFgs9P43WzblcBa0bJE"
print(TOKEN)