import os
import django
from pymongo import MongoClient

# Налаштування Django
print("Setting up Django...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()
print("Django setup complete.")

from quotes.models import Author, Quote, Tag

# Підключення до MongoDB
print("Connecting to MongoDB...")
client = MongoClient("mongodb+srv://goitlearn:WAdWzy6PycdDlgm7@cluster0.utwip5n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo_db = client['myDB1']
print("MongoDB connection established.")
print("Available collections:", mongo_db.list_collection_names())

# Перевірка даних у колекціях
print("Checking if authors collection exists...")
if 'author' in mongo_db.list_collection_names():
    print("Authors collection exists.")
else:
    print("Authors collection does NOT exist.")

print("Checking if quotes collection exists...")
if 'quote' in mongo_db.list_collection_names():
    print("Quotes collection exists.")
else:
    print("Quotes collection does NOT exist.")

mongo_authors = mongo_db['author']
mongo_quotes = mongo_db['quote']

# Перевірка кількості записів
print(f"Number of authors in MongoDB: {mongo_authors.count_documents({})}")
print(f"Number of quotes in MongoDB: {mongo_quotes.count_documents({})}")

# Створюємо словник для відображення ідентифікаторів авторів MongoDB на Django
author_id_map = {}

# Міграція авторів
print("Starting authors migration...")
for mongo_author in mongo_authors.find():
    print(f"Processing author: {mongo_author}")
    author, created = Author.objects.get_or_create(
        fullname=mongo_author['fullname'],
        defaults={
            'born_date': mongo_author['born_date'],
            'born_location': mongo_author['born_location'],
            'description': mongo_author['description']
        }
    )
    author_id_map[str(mongo_author['_id'])] = author.id  # Зберігаємо відображення ідентифікаторів авторів

# Міграція цитат
print("Starting quotes migration...")
for mongo_quote in mongo_quotes.find():
    print(f"Processing quote: {mongo_quote}")
    author_id = author_id_map.get(str(mongo_quote['author']))  # Отримуємо відповідний ідентифікатор автора зі словника
    if author_id:
        author = Author.objects.get(id=author_id)
        quote_text = f'"{mongo_quote["quote"]}" - {author.fullname}'
    else:
        quote_text = f'"{mongo_quote["quote"]}" - Author unknown'
    
    quote, created = Quote.objects.get_or_create(
        quote=quote_text,
        author_id=author_id
    )

    # Міграція тегів
    if 'tags' in mongo_quote:
        for tag_name in mongo_quote['tags']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

    if created:
        print(f"Quote created: {quote.quote}")
    else:
        print(f"Quote already exists: {quote.quote}")

print("Migration completed.")