from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from Linked_list import LinkedList

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

linked_list = LinkedList()

@app.route('/')
def index():
    # Render the initiaila page with the linked list*
    return render_template('Linked_list.html', linked_list=linked_list.print_list())

@app.route('/update', methods=['POST'])
def update():
    operation = request.form.get('operation')
    data = request.form.get('data', None)  # Using .get() to avoid KeyError
    
    # Debugging print statements
    print(f"Received operation: {operation}")
    print(f"Received data: {data}")

    if operation is None:
        flash("No operation selected.")
        return render_template('index.html', linked_list=linked_list)
    
    # Validate the data when required
    if operation in ["remove_at", "insert_beginning", "insert_end"] and not data:
        flash("Please provide data for the operation.")
        return redirect(url_for('index'))  # Prevent further execution

    try:
        # Operations based on the button clicked
        if operation == "insert_beginning" and data:
            linked_list.insert_at_beginning(data)
            flash(f"Inserted '{data}' at the beginning.")
        elif operation == "insert_end" and data:
            linked_list.insert_at_end(data)
            flash(f"Inserted '{data}' at the end.")
        elif operation == "remove_beginning":
            if linked_list.head:  # If the list isn't empty
                removed_data = linked_list.remove_beginning()
                flash(f"Removed element '{removed_data}' from the beginning.")
            else:
                flash("The list is empty. No element to remove.")
        elif operation == "remove_end":
            if linked_list.head:  # If the list isn't empty
                removed_data = linked_list.remove_end()
                flash(f"Removed element '{removed_data}' from the end.")
            else:
                flash("The list is empty. No element to remove.")
        elif operation == "remove_at" and data:
            found = linked_list.search(data)
            if found:
                linked_list.remove_at(data)
                flash(f"Removed element '{data}' from the list.")
            else:
                flash(f"Data '{data}' not found in the list. Cannot remove.")
        elif operation == "search" and data:
            found = linked_list.search(data)
            if found:
                flash(f"Data '{data}' found in the list.")
            else:
                flash(f"Data '{data}' not found in the list.")
        else:
            flash("Invalid operation or missing data.")

        #Return the updated list as a JSON response for AJAX
        return jsonify(linked_list=linked_list)
    
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        print(f"Error occurred: {e}")  # Log error for debugging

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
