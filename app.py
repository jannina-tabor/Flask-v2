from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from Linked_list import LinkedList

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

Linked_list = LinkedList()

@app.route('/')
def index():
    # Render the initiaila page with the linked list*
    return render_template('Linked_list.html', linked_list=Linked_list.print_list())

@app.route('/update', methods=['POST'])
def update():
    operation = request.form.get('operation')
    data = request.form.get('data', None)  # Using .get() to avoid KeyError

    # Validate the data when required
    if operation in ["remove_at", "insert_beginning", "insert_end"] and not data:
        flash("Please provide data for the operation.")
        return redirect(url_for('index'))  # Prevent further execution

    try:
        if operation == "insert_beginning" and data:
            Linked_list.insert_at_beginning(data)
            flash(f"Inserted '{data}' at the beginning.")
        elif operation == "insert_end" and data:
            Linked_list.insert_at_end(data)
            flash(f"Inserted '{data}' at the end.")
        elif operation == "remove_beginning":
            if Linked_list.head:  # If the list isn't empty
                removed_data = Linked_list.remove_beginning()
                flash(f"Removed element '{removed_data}' from the beginning.")
            else:
                flash("The list is empty. No element to remove.")
        elif operation == "remove_end":
            if Linked_list.head:  # If the list isn't empty
                removed_data = Linked_list.remove_end()
                flash(f"Removed element '{removed_data}' from the end.")
            else:
                flash("The list is empty. No element to remove.")
        elif operation == "remove_at" and data:
            found = Linked_list.search(data)
            if found:
                Linked_list.remove_at(data)
                flash(f"Removed element '{data}' from the list.")
            else:
                flash(f"Data '{data}' not found in the list. Cannot remove.")
        elif operation == "search" and data:
            found = Linked_list.search(data)
            if found:
                flash(f"Data '{data}' found in the list.")
            else:
                flash(f"Data '{data}' not found in the list.")
        else:
            flash("Invalid operation or missing data.")

    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        print(f"Error occurred: {e}")  # Log error for debugging

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
