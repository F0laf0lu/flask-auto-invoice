from flask import Flask, render_template, request, send_file
from datetime import datetime
import pdfkit
import io
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def invoice():
    posted_data = request.get_json() or {}
    today = datetime.today().strftime("%B %d, %Y")
    default_data = {
        'details' : {
        'date': today,
        'invoice_number' : 123,
        'due_date': today },
        
        'recipient' : {
        'name': 'Acme Corp',
        'email': 'john@example.com',
        'addr_1': '12345 Sunny Road',
        'addr_2' : 'Sunnyville, CA 12345'
        },

    'items' : [{
                'charge': 300.0,
                'title': 'website design'
            },
            {
                'charge': 75.0,
                'title': 'Hosting (3 months)'
            },
            {
                'charge': 10.0,
                'title': 'Domain name (1 year)'
            }
        ]
    }

    details= posted_data.get('details', default_data['details'])
    recipient = posted_data.get('recipient', default_data['recipient'])
    items = posted_data.get('items', default_data['items'])
    
    total = sum([i['charge'] for i in items])

    rendered =  render_template('invoice.html', 
                        details=details,
                        recipient=recipient,
                        items = items,
                        total = total,
                        )
    
    # Set the path to wkhtmltopdf executable file
    path_wkthmltopdf = b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    return send_file(
                io.BytesIO(pdf),
                download_name= f'{recipient["name"]} invoice.pdf'
            )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

