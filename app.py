import pickle
import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the trained linear regression model from linear.pkl
with open('linear.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML Template with an attractive, responsive UI using Tailwind CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>House Price Prediction Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 min-h-screen text-slate-100 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-2xl shadow-2xl overflow-hidden p-8">
        
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-indigo-400">
                House Price Predictor
            </h1>
            <p class="text-slate-400 text-sm mt-2">Enter the property details below to estimate its market value</p>
        </div>

        <!-- Result Box -->
        {% if prediction_text %}
        <div class="mb-8 p-4 bg-teal-950/50 border border-teal-500/30 rounded-xl text-center animate-fade-in">
            <span class="text-xs uppercase tracking-wider text-teal-400 font-semibold">Estimated Valuation</span>
            <div class="text-3xl font-black text-teal-300 mt-1">{{ prediction_text }}</div>
        </div>
        {% endif %}

        <!-- Form -->
        <form action="/" method="POST" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Square Footage</label>
                <input type="number" step="any" name="Square_Footage" required 
                    value="{{ form_data.Square_Footage if form_data else '' }}"
                    class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-teal-500 transition" placeholder="e.g., 2000">
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Number of Bedrooms</label>
                <input type="number" name="Num_Bedrooms" required 
                    value="{{ form_data.Num_Bedrooms if form_data else '' }}"
                    class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-teal-500 transition" placeholder="e.g., 3">
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Number of Bathrooms</label>
                <input type="number" step="any" name="Num_Bathrooms" required 
                    value="{{ form_data.Num_Bathrooms if form_data else '' }}"
                    class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-teal-500 transition" placeholder="e.g., 2">
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Year Built</label>
                <input type="number" name="Year_Built" required 
                    value="{{ form_data.Year_Built if form_data else '' }}"
                    class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-teal-500 transition" placeholder="e.g., 2010">
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Lot Size</label>
                <input type="number" step="any" name="Lot_Size" required 
                    value="{{ form_data.Lot_Size if form_data else '' }}"
                    class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-teal-500 transition" placeholder="e.g., 5000">
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-300 mb-1">Garage Size (Cars)</label>
                <input type="number" name="Garage_Size" required 
                    value="{{ form_data.Garage_Size if form_data else '' }}"
                    class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-teal-500 transition" placeholder="e.g., 2">
            </div>

            <div class="md:col-span-2">
                <label class="block text-sm font-medium text-slate-300 mb-1">Neighborhood Quality (1-10)</label>
                <input type="number" step="any" name="Neighborhood_Quality" required 
                    value="{{ form_data.Neighborhood_Quality if form_data else '' }}"
                    class="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-slate-100 focus:outline-none focus:border-teal-500 transition" placeholder="e.g., 8">
            </div>

            <div class="md:col-span-2 mt-4">
                <button type="submit" class="w-full bg-gradient-to-r from-teal-500 to-indigo-600 text-white font-semibold py-3 rounded-lg shadow-lg hover:from-teal-400 hover:to-indigo-500 transition duration-200 cursor-pointer">
                    Calculate Price
                </button>
            </div>
        </form>
        
        <div class="text-center mt-6 text-xs text-slate-500">
            Powered by Flask & Scikit-Learn
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    form_data = None
    
    if request.method == 'POST':
        try:
            # Extract features in the exact order expected by the model
            form_data = request.form
            features = [
                float(form_data['Square_Footage']),
                float(form_data['Num_Bedrooms']),
                float(form_data['Num_Bathrooms']),
                float(form_data['Year_Built']),
                float(form_data['Lot_Size']),
                float(form_data['Garage_Size']),
                float(form_data['Neighborhood_Quality'])
            ]
            
            # Predict using the loaded model
            final_features = np.array([features])
            prediction = model.predict(final_features)[0]
            
            # Format output as currency
            prediction_text = f"${prediction:,.2f}"
        except Exception as e:
            prediction_text = f"Error in calculation: {str(e)}"
            
    return render_template_string(HTML_TEMPLATE, prediction_text=prediction_text, form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
