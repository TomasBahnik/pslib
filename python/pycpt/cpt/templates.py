from jinja2 import Template


def fe_transaction_html_template(test_env='test_env', log_dir='log_dir', script_name='script_name') -> Template:
    return Template('''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {
        border: 1px solid black;
    }
    </style>
    </head>
    <body>
    <h2>FE transactions</h2>
    <table border="1">
        <tr><th>Iteration</th><th>Name</th><th>Trx time</th><th>Wasted time</th><th>Error</th></tr>
        {% for trx in trxs %}
        <tr><td>{{ trx['iteration'] }}</td> <td>{{ trx['trx_name'] }}</td> <td>{{ trx['trx_time'] }}</td>
         <td>{{ trx['wasted_time'] }}</td><td>{{ trx['error'] }}</td></tr>
        {% endfor %}
    </table>
    <p>'Trx time' = duration - wasted_time. Wasted time is the time spent by the tool to capture and process data during test run</p>
    <a href=../../../log/''' + test_env + '/' + log_dir + '/' + script_name + '>Log dir of the FE test</a>' +
                    '''
    </body>
    </html> 
    ''')
