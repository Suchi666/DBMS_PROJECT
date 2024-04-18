from flask import Flask, render_template,request,redirect
import requests

app = Flask(__name__)

# Replace 'YOUR_NGROK_URL' with the public URL generated by ngrok
ngrok_url = 'https://899f-34-133-227-191.ngrok-free.app/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getresult', methods=['GET'])
def get_result():
    # Get the query string from the form submission
    query_string = request.args.get('query_string')
    print(query_string)
    response = requests.get(f'{ngrok_url}', params={'item_id':19,'query_string': query_string}).json()
    print(response['response'])
    result=response['response']
    # Extract the relevant information from the response JSON
    # result = data.get('response', 'No result found')
    
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)