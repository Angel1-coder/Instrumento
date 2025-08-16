"""
Example environment variables for local development.
Copy this file to env.py and fill in your actual values.
"""
import os

# Stripe Keys (placeholder values - replace with your actual keys)
os.environ.setdefault('STRIPE_PUBLIC_KEY', 'pk_test_your_stripe_public_key_here')
os.environ.setdefault('STRIPE_SECRET_KEY', 'sk_test_your_stripe_secret_key_here')
os.environ.setdefault('STRIPE_WH_SECRET', 'whsec_your_stripe_webhook_secret_here')

# Development mode
os.environ.setdefault('DEVELOPMENT', '1')

# Database (SQLite for development)
os.environ.setdefault('DATABASE_URL', '')

# Email (console backend for development)
os.environ.setdefault('EMAIL_HOST_USER', '')
os.environ.setdefault('EMAIL_HOST_PASS', '')
os.environ.setdefault('DEFAULT_FROM_EMAIL', 'noreply@instrumento.com')
