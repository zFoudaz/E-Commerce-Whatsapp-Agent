"""Seed script to populate initial categories and products in the ecommerce database."""

from database import engine, SessionLocal
import models

def seed():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(models.Category).count() > 0:
        print("Database already contains data. Skipping seed.")
        db.close()
        return

    print("Seeding initial store categories and products...")

    electronics = models.Category(
        name="Electronics",
        description="Laptops, gaming accessories, and smart devices."
    )
    accessories = models.Category(
        name="Accessories",
        description="Cables, chargers, and laptop stands."
    )
    audio = models.Category(
        name="Audio",
        description="Headphones, earphones, and Bluetooth speakers."
    )

    db.add_all([electronics, accessories, audio])
    db.commit()

    products = [
        models.Product(name="Mechanical Keyboard", description="RGB mechanical keyboard with blue switches", price=89.99, stock=12, category_id=electronics.id),
        models.Product(name="Wireless Gaming Mouse", description="Ergonomic rechargeable mouse with 16000 DPI", price=49.99, stock=25, category_id=electronics.id),
        models.Product(name="Gaming Monitor 27-inch", description="144Hz IPS gaming monitor QHD", price=279.99, stock=4, category_id=electronics.id),
        models.Product(name="USB-C Fast Charging Cable", description="Braided 2-meter 100W PD charging cable", price=14.99, stock=50, category_id=accessories.id),
        models.Product(name="Aluminum Laptop Stand", description="Foldable ergonomic laptop riser", price=34.99, stock=15, category_id=accessories.id),
        models.Product(name="Noise Cancelling Headphones", description="Over-ear wireless headphones with ANC", price=149.99, stock=8, category_id=audio.id),
        models.Product(name="Waterproof Bluetooth Speaker", description="Portable 20W stereo outdoor speaker", price=59.99, stock=0, category_id=audio.id),
    ]

    db.add_all(products)
    db.commit()
    db.close()
    print("Seeding complete! 3 Categories and 7 Products added.")

if __name__ == "__main__":
    seed()
