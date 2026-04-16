"""
Django shell script for creating sample data for testing.
"""
import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from requests.models import BloodRequest

User = get_user_model()

def create_sample_donors():
    """Create sample donors for testing."""
    
    donors_data = [
        {
            'username': 'donor_aplus_1',
            'email': 'donor1@example.com',
            'password': 'testpass123',
            'first_name': 'John',
            'phone': '1001000001',
            'blood_group': 'A+',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'location_name': 'Manhattan, NYC',
            'is_available': True,
        },
        {
            'username': 'donor_oplus_1',
            'email': 'donor2@example.com',
            'password': 'testpass123',
            'first_name': 'Jane',
            'phone': '1001000002',
            'blood_group': 'O+',
            'latitude': 40.7589,
            'longitude': -73.9851,
            'location_name': 'Times Square, NYC',
            'is_available': True,
            'last_donation_date': (datetime.now() - timedelta(days=45)).date(),
        },
        {
            'username': 'donor_ominus_1',
            'email': 'donor3@example.com',
            'password': 'testpass123',
            'first_name': 'Bob',
            'phone': '1001000003',
            'blood_group': 'O-',
            'latitude': 40.7505,
            'longitude': -73.9972,
            'location_name': 'Central Park, NYC',
            'is_available': True,
            'last_donation_date': (datetime.now() - timedelta(days=120)).date(),
        },
        {
            'username': 'donor_bplus_1',
            'email': 'donor4@example.com',
            'password': 'testpass123',
            'first_name': 'Alice',
            'phone': '1001000004',
            'blood_group': 'B+',
            'latitude': 40.6892,
            'longitude': -74.0445,
            'location_name': 'Brooklyn, NYC',
            'is_available': False,
        },
    ]
    
    created = 0
    for donor_data in donors_data:
        if not User.objects.filter(username=donor_data['username']).exists():
            user = User.objects.create_user(**donor_data)
            created += 1
            print(f"✓ Created donor: {user.username} ({user.blood_group})")
        else:
            print(f"✗ Donor already exists: {donor_data['username']}")
    
    return created


def create_sample_requests():
    """Create sample blood requests."""
    
    try:
        requester = User.objects.get(username='donor_aplus_1')
    except User.DoesNotExist:
        print("✗ Requester user not found. Create donors first.")
        return 0
    
    requests_data = [
        {
            'blood_group': 'O+',
            'latitude': 40.7480,
            'longitude': -73.9862,
            'location_name': 'Midtown, NYC',
            'urgency': 'High',
            'message': 'Need blood urgently for surgery',
        },
        {
            'blood_group': 'A+',
            'latitude': 40.6501,
            'longitude': -73.9496,
            'location_name': 'Jamaica, Queens',
            'urgency': 'Medium',
            'message': 'Regular blood donation needed',
        },
    ]
    
    created = 0
    for request_data in requests_data:
        request_data['user'] = requester
        blood_req = BloodRequest.objects.create(**request_data)
        created += 1
        print(f"✓ Created blood request: {blood_req.id} ({blood_req.blood_group}) - {blood_req.urgency}")
    
    return created


if __name__ == '__main__':
    print("=" * 50)
    print("Creating sample data for Bloodlink...")
    print("=" * 50)
    
    donors = create_sample_donors()
    print(f"\nCreated {donors} sample donors")
    
    requests = create_sample_requests()
    print(f"Created {requests} sample blood requests")
    
    print("\n" + "=" * 50)
    print("Sample data creation complete!")
    print("=" * 50)
    print("\nLogin credentials:")
    print("- Username: donor_oplus_1")
    print("- Password: testpass123")
