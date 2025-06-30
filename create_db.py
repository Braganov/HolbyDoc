from holbydoc.app import db, app
import os

# S'assurer que le dossier holbydoc existe
os.makedirs('holbydoc', exist_ok=True)

# Changer l'URI de la base de données pour la placer dans le dossier holbydoc
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///holbydoc/site.db"

with app.app_context():
    db.create_all()
    print("Base de données et tables créées dans le dossier holbydoc.")
