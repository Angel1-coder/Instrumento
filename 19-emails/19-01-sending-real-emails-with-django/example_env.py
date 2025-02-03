""" 
This is an example file of the environment variables you should 
have set in the env.py file of your project to run it locally.
"""
import os

os.environ.setdefault('STRIPE_PUBLIC_KEY', 'your stripe publishable key, get this from your stripe developers dashboard')
os.environ.setdefault('STRIPE_SECRET_KEY', 'your stripe secret key, get this from your stripe developers dashboard')
os.environ.setdefault('STRIPE_WH_SECRET', 'your stripe webhook secret, get this from the Stripe CLI after opening the stripe portal')
os.environ.setdefault('DEVELOPMENT', '1')