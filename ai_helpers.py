import openai
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

# Configure OpenAI API (in production, use environment variables)
# openai.api_key = "your-api-key-here"

def generate_purpose_suggestions(company_name):
    """
    Generate smart suggestions for visit purpose based on company name
    """
    common_purposes = {
        "tech": ["Software Demo", "IT Support", "System Integration", "Technical Consultation"],
        "consulting": ["Business Meeting", "Strategy Session", "Project Review", "Consultation"],
        "healthcare": ["Medical Consultation", "Healthcare Partnership", "Medical Supply Delivery"],
        "education": ["Training Session", "Educational Workshop", "Academic Collaboration"],
        "finance": ["Financial Review", "Investment Discussion", "Banking Services"],
        "default": ["Business Meeting", "Interview", "Delivery", "Consultation", "Site Visit"]
    }

    # Simple keyword matching for demo purposes
    # In production, use more sophisticated NLP or ML techniques
    company_lower = company_name.lower()
    if any(word in company_lower for word in ["tech", "software", "digital", "it", "computer"]):
        return common_purposes["tech"]
    elif any(word in company_lower for word in ["consult", "advisor", "partner"]):
        return common_purposes["consulting"]
    elif any(word in company_lower for word in ["health", "medical", "hospital", "care"]):
        return common_purposes["healthcare"]
    elif any(word in company_lower for word in ["school", "college", "university", "education"]):
        return common_purposes["education"]
    elif any(word in company_lower for word in ["bank", "finance", "invest", "capital"]):
        return common_purposes["finance"]
    else:
        return common_purposes["default"]

def get_chatbot_response(user_query, visitor_name=None):
    """
    Generate a response to user queries using OpenAI API
    """
    try:
        # For demo purposes, use a rule-based approach
        # In production, use OpenAI API
        user_query = user_query.lower()

        if "check in" in user_query or "checkin" in user_query:
            return "To check in, please scan your QR code or enter your temporary ID in the check-in form."

        elif "check out" in user_query or "checkout" in user_query:
            return "To check out, please scan your QR code or enter your temporary ID in the check-out form."

        elif "register" in user_query or "sign up" in user_query:
            return "To register as a visitor, please fill out the visitor entry form with your details."

        elif "qr code" in user_query:
            return "After registration, you'll receive a QR code that you can use for check-in and check-out."

        elif "contact" in user_query:
            return "For assistance, please contact the reception desk or ask for help through this chat."

        elif "hello" in user_query or "hi" in user_query:
            greeting = f"Hello{' ' + visitor_name if visitor_name else ''}! How can I assist you today?"
            return greeting

        else:
            # Fallback response
            return "I'm Ashley. I can help with visitor registration, check-in, and check-out. What do you need help with?"

        # When implementing OpenAI API:
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant for a visitor management system."},
        #         {"role": "user", "content": user_query}
        #     ]
        # )
        # return response.choices[0].message.content

    except Exception as e:
        return f"I'm having trouble processing your request. Please try again later. Error: {str(e)}"

def analyze_visitor_patterns(visitors_data):
    """
    Analyze visitor patterns and generate insights
    Input: List of visitor dictionaries with check-in times
    Output: Dictionary with analysis results and visualizations
    """
    try:
        # Convert to pandas DataFrame for easier analysis
        df = pd.DataFrame(visitors_data)

        # Ensure datetime format
        df['checkin_time'] = pd.to_datetime(df['checkin_time'])

        # Basic statistics
        total_visitors = len(df)
        if total_visitors == 0:
            return {
                "total_visitors": 0,
                "insights": ["No visitor data available for analysis."],
                "charts": {}
            }

        # Visitors per day of week
        df['day_of_week'] = df['checkin_time'].dt.day_name()
        day_counts = df['day_of_week'].value_counts()

        # Visitors per hour of day
        df['hour_of_day'] = df['checkin_time'].dt.hour
        hour_counts = df['hour_of_day'].value_counts().sort_index()

        # Most common companies
        company_counts = df['company'].value_counts().head(5)

        # Most common purposes
        purpose_counts = df['purpose'].value_counts().head(5)

        # Generate insights
        insights = []

        # Busiest day
        if not day_counts.empty:
            busiest_day = day_counts.idxmax()
            busiest_day_count = day_counts.max()
            insights.append(f"Busiest day is {busiest_day} with {busiest_day_count} visitors.")

        # Busiest hour
        if not hour_counts.empty:
            busiest_hour = hour_counts.idxmax()
            busiest_hour_count = hour_counts.max()
            insights.append(f"Busiest hour is {busiest_hour}:00 with {busiest_hour_count} visitors.")

        # Most common company
        if not company_counts.empty:
            most_common_company = company_counts.index[0]
            company_visit_count = company_counts.iloc[0]
            insights.append(f"Most frequent visitor company is {most_common_company} with {company_visit_count} visits.")

        # Most common purpose
        if not purpose_counts.empty:
            most_common_purpose = purpose_counts.index[0]
            purpose_count = purpose_counts.iloc[0]
            insights.append(f"Most common visit purpose is '{most_common_purpose}' with {purpose_count} occurrences.")

        # Generate charts as base64 encoded images
        charts = {}

        # Visitors per day chart
        plt.figure(figsize=(10, 6))
        day_counts.plot(kind='bar', color='skyblue')
        plt.title('Visitors per Day of Week')
        plt.ylabel('Number of Visitors')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        charts['day_chart'] = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        # Visitors per hour chart
        plt.figure(figsize=(10, 6))
        hour_counts.plot(kind='bar', color='lightgreen')
        plt.title('Visitors per Hour of Day')
        plt.xlabel('Hour')
        plt.ylabel('Number of Visitors')
        plt.xticks(range(24))
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        charts['hour_chart'] = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        return {
            "total_visitors": total_visitors,
            "insights": insights,
            "charts": charts,
            "day_counts": day_counts.to_dict(),
            "hour_counts": hour_counts.to_dict(),
            "company_counts": company_counts.to_dict(),
            "purpose_counts": purpose_counts.to_dict()
        }

    except Exception as e:
        return {
            "error": str(e),
            "insights": [f"Error analyzing visitor data: {str(e)}"],
            "charts": {}
        }

def predict_visitor_traffic(visitors_data, days_to_predict=7):
    """
    Predict visitor traffic for the next few days
    Input: List of visitor dictionaries with check-in times
    Output: Dictionary with predictions
    """
    try:
        # Convert to pandas DataFrame
        df = pd.DataFrame(visitors_data)

        # Ensure datetime format
        df['checkin_time'] = pd.to_datetime(df['checkin_time'])

        # Group by date and count visitors
        df['date'] = df['checkin_time'].dt.date
        daily_counts = df.groupby('date').size()

        # If we don't have enough data, return a simple average
        if len(daily_counts) < 3:
            avg_visitors = daily_counts.mean() if not daily_counts.empty else 0
            predictions = {
                (datetime.now().date() + timedelta(days=i)).isoformat(): avg_visitors 
                for i in range(1, days_to_predict + 1)
            }
            return {
                "predictions": predictions,
                "method": "average",
                "confidence": "low"
            }

        # Simple moving average prediction
        # In a real application, use more sophisticated time series models
        window = min(7, len(daily_counts))
        recent_avg = daily_counts.tail(window).mean()

        # Get day of week patterns
        df['day_of_week'] = df['checkin_time'].dt.dayofweek
        day_patterns = df.groupby('day_of_week').size()
        day_patterns = day_patterns / day_patterns.sum() * recent_avg * 7

        # Generate predictions
        predictions = {}
        today = datetime.now().date()

        for i in range(1, days_to_predict + 1):
            future_date = today + timedelta(days=i)
            day_of_week = future_date.weekday()

            # Use day pattern if available, otherwise use recent average
            if day_of_week in day_patterns:
                predicted_visitors = day_patterns[day_of_week]
            else:
                predicted_visitors = recent_avg

            predictions[future_date.isoformat()] = round(predicted_visitors, 1)

        return {
            "predictions": predictions,
            "method": "day_pattern",
            "confidence": "medium"
        }

    except Exception as e:
        return {
            "error": str(e),
            "predictions": {},
            "method": "failed",
            "confidence": "none"
        }
