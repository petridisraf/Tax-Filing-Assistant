from flask import Blueprint, request, jsonify, current_app, render_template
from .models import db, TaxInfo
import openai


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/submit', methods=['POST'])
def submit():
    income = request.form.get('income')
    expenses = request.form.get('expenses')

    if not income or not expenses:
        return jsonify({"error": "Invalid input"}), 400

    tax_info = TaxInfo(income=income, expenses=expenses)
    db.session.add(tax_info)
    db.session.commit()

    # Call OpenAI API for tax advice
    openai.api_key = current_app.config['OPENAI_API_KEY']
    prompt = f"Provide tax advice for an income of {income} and expenses of {expenses}."
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=150)
    tax_advice = response.choices[0].text.strip()

    return jsonify({"message": "Data submitted successfully!", "tax_advice": tax_advice}), 201

@main.route('/api/get_tax_advice', methods=['POST'])
def get_tax_advice():
    data = request.get_json()

    income = data.get('income')
    expenses = data.get('expenses')

    if not income or not expenses:
        return jsonify({"error": "Income and expenses are required."}), 400

    try:
        income = float(income)
        expenses = float(expenses)
    except ValueError:
        return jsonify({"error": "Invalid input. Please enter numeric values for income and expenses."}), 400

    openai.api_key = current_app.config['OPENAI_API_KEY']
    
    prompt = f"Provide tax advice for an individual with an income of {income} and expenses of {expenses}."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a tax advisor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    advice = response.choices[0].message['content'].strip()

    return jsonify({"advice": advice})