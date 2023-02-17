from website import app # because of the __init__ file making website a package



if __name__ == '__main__':
    app.run(debug=True, port=8000)
    