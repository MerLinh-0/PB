# from datasets import datasets
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datasets.db"

db = SQLAlchemy(app)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(50), nullable=False)
    rows = db.Column(db.Integer, nullable=False)
    cols = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "topic": self.topic,
            "rows": self.rows,
            "cols": self.cols,
            "description": self.description
        }


with app.app_context():
    db.create_all()  
    
    if Dataset.query.count() == 0:
        starting_sets = [
            {
                "name": "Iris Species",
                "topic": "Biologia / Klasyfikacja",
                "rows": 150,
                "cols": 4,
                "description": "Klasyczny zbiór danych zawierający pomiary płatków i działek kielicha trzech gatunków irysów. Idealny do nauki podstawowych algorytmów klasyfikacji."
            },
            {
                "name": "Boston Housing",
                "topic": "Nieruchomości / Regresja",
                "rows": 506,
                "cols": 13,
                "description": "Zbiór danych o cenach nieruchomości w okolicach Bostonu wraz z informacjami o przestępczości, zagospodarowaniu terenu i wskaźnikach demograficznych. Wykorzystywany do zadań regresji."
            },
            {
                "name": "Credit Card Fraud Detection",
                "topic": "Finanse / Wykrywanie anomalii",
                "rows": 284807,
                "cols": 30,
                "description": "Zanonimizowane transakcje europejskich kart kredytowych z września 2013 roku. Zbiór wysoce niezbalansowany, przeznaczony do testowania metod wykrywania oszustw i anomalii."
            },
            {
                "name": "Titanic Passenger Survival",
                "topic": "Historia / Klasyfikacja binarna",
                "rows": 891,
                "cols": 11,
                "description": "Dane demograficzne i informacje o biletach pasażerów Titanica. Popularny zbiór służący do budowania modeli przewidujących szanse na przeżycie katastrofy."
            }
        ]

        for set in starting_sets:
            new_set = Dataset(
                name=set["name"],
                topic=set["topic"],
                rows=set["rows"],   
                cols=set["cols"],   
                description=set["description"]
            )
            db.session.add(new_set)
        db.session.commit()


def check_json(set):
    if not set:
        return "Brak danych JSON"

    needed = ['name', 'topic', 'rows', 'cols', 'description']
    
    for pole in needed:
        if pole not in set:
            return f"Brakujące pole: {pole}"

    if not isinstance(set['rows'], int) or set['rows'] < 0:
        return "Pole rows musi być nieujemną liczbą całkowitą."
        
    if not isinstance(set['cols'], int) or set['cols'] < 0:
        return "Pole cols musi być nieujemną liczbą całkowitą."

    return None

@app.route("/")
def index():
    return render_template('index.html', title='Katalog')

@app.route("/datasets")
def sets():
    return render_template('datasets.html', title='Lista zbiorów', sets=Dataset.query.all())

@app.route("/datasets/<int:id>")
def details(id):
    return render_template('details.html', set=Dataset.query.get_or_404(id))

@app.route("/api/datasets")
def api_sets():
    datasets = Dataset.query.all()
    return jsonify([ds.to_dict() for ds in datasets]), 200

@app.route("/api/datasets/<int:id>")
def api_details(id):
    dataset = Dataset.query.get(id)
    if not dataset:
        return jsonify({"error": "Nie znaleziono zbioru"}), 404
    return jsonify(dataset.to_dict()), 200

@app.route("/api/datasets", methods=["POST"])
def api_sets_add():
    set_json = request.get_json()
    error_msg = check_json(set_json)
    if error_msg is not None:
        return jsonify({"error":error_msg}), 400

    new_set = Dataset(
        name=set_json["name"],
        topic=set_json["topic"],
        rows=set_json["rows"],
        cols=set_json["cols"],
        description=set_json["description"]
    )
    db.session.add(new_set)
    db.session.commit()

    return jsonify(new_set.to_dict()), 201

@app.route("/api/datasets/<int:id>", methods=["PUT"])
def api_set_update(id):
    dataset = Dataset.query.get(id)
    if not dataset:
        return jsonify({"error": "Nie znaleziono zbioru o podanym ID."}), 404
        
    set_json = request.get_json()

    error_msg = check_json(set_json)
    if error_msg is not None:
        return jsonify({"error": error_msg}), 400
        
    dataset.name = set_json["name"]
    dataset.topic = set_json["topic"]
    dataset.rows = set_json["rows"]
    dataset.cols = set_json["cols"]
    dataset.description = set_json["description"]
    
    db.session.commit()
    return jsonify(dataset.to_dict()), 200

@app.route("/api/datasets/<int:id>", methods=["DELETE"])
def api_set_delete(id):
    dataset = Dataset.query.get(id)
    if not dataset:
        return jsonify({"error": "Nie znaleziono zbioru"}), 404
        
    db.session.delete(dataset)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
