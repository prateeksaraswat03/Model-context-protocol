from database.db import init_db, seed_db

def start_app():
    print("Initializing Spendly Application...")

    # Initialize and seed the database
    try:
        init_db()
        seed_db()
        print("Database initialized and seeded successfully.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        return

    print("Application is now running!")

if __name__ == "__main__":
    start_app()
