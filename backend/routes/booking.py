from flask import Blueprint, request, jsonify
from models import db, Client, Artisan, Booking
from email_service import send_email # I'll create this later

# Create the Blueprint
booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

@booking_bp.route('/book', methods=['POST'])
def book_artisan():
    data = request.json
    client_id = data.get('client_id')
    artisan_id = data.get('artisan_id')
    details = data.get('details', '')

    # Validating client and artisan existence
    client = Client.query.get(client_id)
    artisan = Artisan.query.get(artisan_id)

    if not client or not artisan:
        return jsonify({"error": "Client or Artisan not found"}), 404

    # Creat booking
    booking = Booking(client_id=client_id, artisan_id=artisan_id, details=details)
    db.session.add(booking)
    db.session.commit()

    # Sending notification email to the artisan
    subject = f"New Booking from {client.name}"
    body = f"""
    Hello {artisan.name},

    You have received a new booking from {client.name} ({client.email}).

    Booking Details:
    {details}

    Date: {booking.booking_date.strftime('%Y-%m-%d %H:%M:%S')}
    """
    send_email(artisan.email, subject, body)

    return jsonify({"message": "Booking created and email sent successfully!"}), 201
