from flask import Flask, render_template, request, redirect, url_for, flash, send_file, after_this_request
import os
import tempfile
from src.utils.load_utils import load_scheduler

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(24)

scheduler = None

@app.route('/')
def index():
    """Home page with options to generate, view, and save schedules"""
    return render_template('index.html')

@app.route('/load', methods=['POST'])
def load():
    """Load a custom input file"""
    global scheduler

    if 'input_file' not in request.files:
        flash("No file selected", "error")
        return redirect(url_for('index'))

    file = request.files['input_file']

    if file.filename == '':
        flash("No file selected", "error")
        return redirect(url_for('index'))

    if not file.filename.endswith('.json'):
        flash("Only JSON files are supported", "error")
        return redirect(url_for('index'))

    try:
        temp_path = os.path.join('data', 'tmp.json')
        file.save(temp_path)

        scheduler = load_scheduler(temp_path)
        flash(f"Data loaded successfully from {file.filename}", "success")
    except Exception as e:
        flash(f"Error loading data: {str(e)}", "error")

    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    """Generate a schedule"""
    global scheduler

    if scheduler is None:
        flash("Error: No data loaded", "error")
        return redirect(url_for('index'))

    try:
        result = scheduler.solve()
        if result == "Optimal":
            flash("Schedule generated!", "success")
        else:
            flash(f"Schedule not generated: {result}", "error")
    except Exception as e:
        flash(f"Error generating schedule: {str(e)}", "error")

    return redirect(url_for('index'))

@app.route('/view')
def view():
    """View the generated schedule"""
    global scheduler

    if scheduler is None:
        flash("Error: No data loaded", "error")
        return redirect(url_for('index'))

    schedule_data = scheduler.get_output_data()

    time_slots = sorted({entry["time_slot"].split(' ')[1] for entry in schedule_data})
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    schedule_table = []
    for slot in time_slots:
        row = {"time": slot}
        for day in days:
            entry = next(
                (f"{c['course']} ({c['instructor']})"
                 for c in schedule_data
                 if c['time_slot'] == f"{day} {slot}"),
                "Free"
            )
            row[day.lower()] = entry
        schedule_table.append(row)

    return render_template('view.html', schedule=schedule_table, days=days)

@app.route('/save', methods=['POST'])
def save():
    """Save the schedule to a JSON file and download it"""
    global scheduler

    if scheduler is None:
        flash("Error: No data loaded", "error")
        return redirect(url_for('index'))

    elif not scheduler.schedule:
        flash("Error: Generate the schedule first.", "error")
        return redirect(url_for('index'))

    try:
        output_filename = request.form.get('output_filename', default='schedule.json')

        if not output_filename.endswith('.json'):
            output_filename += '.json'

        temp_fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(temp_fd)

        scheduler.save_schedule(temp_path)

        @after_this_request
        def remove_file(response):
            try:
                os.remove(temp_path)
            except Exception as e:
                app.logger.error(f"Error removing temporary file: {e}")
            return response

        return send_file(
            temp_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/json'
        )
    except Exception as e:
        flash(f"Error saving schedule: {str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
