from flask import Flask, render_template, request, abort
from setup_app import setUp
from mypkg import data_handler as dh

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")


@app.route('/')
def index():
    result = dh.get_daily_data()
    return render_template('index.html', result=result, title="Today total covid cases")

@app.route('/search')
def custom_filter_page():
    date_str = request.args.get('date')
    try:
        result = dh.get_data_from_date_to_today(date_str)
        return render_template('index.html', result=result, title=f"Total covid cases from {date_str} to today")
    except Exception:
            abort(400)



if __name__ == '__main__':
    setUp()
    app.run(host='127.0.0.1', port=8080, debug=True)