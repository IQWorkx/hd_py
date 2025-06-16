from flask import Blueprint, request, jsonify, current_app
import uuid
from db import get_db_connection
from jwt_utils import create_jwt_token, decode_jwt_token
from functools import wraps

# JWT authentication decorator
def require_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'status': 'error', 'message': 'Missing or invalid Authorization header'}), 401
        token = auth_header.split(' ')[1]
        identity = decode_jwt_token(token)
        if not identity:
            return jsonify({'status': 'error', 'message': 'Invalid or expired token'}), 401
        request.identity = identity
        return f(*args, **kwargs)
    return decorated

api = Blueprint('api', __name__)

@api.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing credentials'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if not user:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        token = create_jwt_token({'username': username, 'role': user['role']})
        return jsonify({'status': 'success', 'token': token})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api.route('/api/register', methods=['POST'])
@require_jwt
def api_register():
    data = request.json
    required = ['name', 'email', 'phone', 'company', 'purpose', 'whom_to_meet']
    if not all(k in data for k in required):
        return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
    temp_id = str(uuid.uuid4())[:8]
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO visitors (name, email, phone, company, purpose, whom_to_meet, temp_id, status, checkin_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (data['name'], data['email'], data['phone'], data['company'], data['purpose'], data['whom_to_meet'], temp_id, 'IN'))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'temp_id': temp_id})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api.route('/api/checkin', methods=['POST'])
@require_jwt
def api_checkin():
    data = request.json
    temp_id = data.get('temp_id')
    if not temp_id:
        return jsonify({'status': 'error', 'message': 'Missing temp_id'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM visitors WHERE temp_id=%s", (temp_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'status': 'error', 'message': 'Invalid Temp ID'}), 404
        elif row[0] == 'IN':
            return jsonify({'status': 'error', 'message': 'Already checked in'}), 400
        else:
            cursor.execute("UPDATE visitors SET status='IN', checkin_time=NOW(), checkout_time=NULL WHERE temp_id=%s", (temp_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'status': 'success', 'message': 'Check-in successful'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api.route('/api/checkout', methods=['POST'])
@require_jwt
def api_checkout():
    data = request.json
    temp_id = data.get('temp_id')
    if not temp_id:
        return jsonify({'status': 'error', 'message': 'Missing temp_id'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM visitors WHERE temp_id=%s", (temp_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'status': 'error', 'message': 'Invalid Temp ID'}), 404
        elif row[0] == 'OUT':
            return jsonify({'status': 'error', 'message': 'Already checked out'}), 400
        else:
            cursor.execute("UPDATE visitors SET status='OUT', checkout_time=NOW() WHERE temp_id=%s", (temp_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'status': 'success', 'message': 'Checkout successful'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api.route('/api/visitors', methods=['GET'])
@require_jwt
def api_visitors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, phone, company, purpose, whom_to_meet, temp_id, status, checkin_time, checkout_time FROM visitors ORDER BY created_at DESC")
        visitors = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'visitors': visitors})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
