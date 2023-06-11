from app import app

match __name__:
    case "__main__":
        app.run(debug=True)

