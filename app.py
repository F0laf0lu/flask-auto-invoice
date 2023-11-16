from flask import Flask, render_template, Response, send_file
from datetime import datetime
import pdfkit
import io
import os

app = Flask(__name__)

@app.route('/')
def invoice():
    today = datetime.today().strftime("%B %d, %Y")
    details = {
        'date': today,
        'invoice_number' : 123,
        'due_date': today
    }
    recipient = {
    'name': 'Acme Corp',
    'email': 'john@example.com',
    'addr_1': '12345 Sunny Road',
    'addr_2' : 'Sunnyville, CA 12345'
    }

    items = [{
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


# @app.route("/download")
# def generate_pdf():

#     # Set the path to wkhtmltopdf executable file
#     path_wkthmltopdf = b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
#     config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

#     # PDF Content
#     name = 'Folafolu'
#     email = 'ofolafolu@gmail.com'

#     html = f"<html><body><h1>Hi {name}</h1><h2>Your email is {email}</h2></body></html>"
#     pdf = pdfkit.from_string(html, False, configuration=config)

#     headers = {
#         'Content-Type': 'application/pdf',
#         'Content-Disposition': f"attachment;filename={name}.pdf"
#     }

#     response = Response(pdf, headers=headers)
#     return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

