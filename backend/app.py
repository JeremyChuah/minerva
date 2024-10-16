from flask import Flask, jsonify, request

# Initialize the Flask app
app = Flask(__name__)

#Ping
@app.get('/ping')
def ping():
    return 'ping'
# Run the server
if __name__ == '__main__':
    app.run(debug=True)
