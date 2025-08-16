from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Product, Category, InstrumentType
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate products with realistic rental prices for different durations'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate rental prices...')
        
        with transaction.atomic():
            # Get or create categories
            strings_category, _ = Category.objects.get_or_create(
                name='strings',
                defaults={'friendly_name': 'String Instruments', 'description': 'Guitars, Basses, Violins'}
            )
            
            percussion_category, _ = Category.objects.get_or_create(
                name='percussion',
                defaults={'friendly_name': 'Percussion Instruments', 'description': 'Drums, Cajón, Handpan'}
            )
            
            wind_category, _ = Category.objects.get_or_create(
                name='wind',
                defaults={'friendly_name': 'Wind Instruments', 'description': 'Trumpets, Saxophones, Flutes'}
            )
            
            keyboards_category, _ = Category.objects.get_or_create(
                name='keyboards',
                defaults={'friendly_name': 'Keyboards & Pianos', 'description': 'Digital Pianos, MIDI Keyboards'}
            )
            
            # Get or create instrument types
            acoustic_guitar_type, _ = InstrumentType.objects.get_or_create(
                name='acoustic_guitar',
                category=strings_category,
                defaults={'description': 'Acoustic guitars for various styles'}
            )
            
            electric_guitar_type, _ = InstrumentType.objects.get_or_create(
                name='electric_guitar',
                category=strings_category,
                defaults={'description': 'Electric guitars for rock, jazz, and blues'}
            )
            
            electric_bass_type, _ = InstrumentType.objects.get_or_create(
                name='electric_bass',
                category=strings_category,
                defaults={'description': 'Electric bass guitars'}
            )
            
            drum_kit_type, _ = InstrumentType.objects.get_or_create(
                name='drum_kit',
                category=percussion_category,
                defaults={'description': 'Complete drum kits'}
            )
            
            cajon_type, _ = InstrumentType.objects.get_or_create(
                name='cajon',
                category=percussion_category,
                defaults={'description': 'Cajón percussion instruments'}
            )
            
            trumpet_type, _ = InstrumentType.objects.get_or_create(
                name='trumpet',
                category=wind_category,
                defaults={'description': 'Brass trumpets'}
            )
            
            saxophone_type, _ = InstrumentType.objects.get_or_create(
                name='saxophone',
                category=wind_category,
                defaults={'description': 'Saxophones in various keys'}
            )
            
            flute_type, _ = InstrumentType.objects.get_or_create(
                name='flute',
                category=wind_category,
                defaults={'description': 'Woodwind flutes'}
            )
            
            digital_piano_type, _ = InstrumentType.objects.get_or_create(
                name='digital_piano',
                category=keyboards_category,
                defaults={'description': 'Digital pianos with weighted keys'}
            )
            
            midi_keyboard_type, _ = InstrumentType.objects.get_or_create(
                name='midi_keyboard',
                category=keyboards_category,
                defaults={'description': 'MIDI keyboards for production'}
            )
            
            # Create products with realistic rental prices
            products_data = [
                # String Instruments
                {
                    'name': 'Yamaha FG800',
                    'category': strings_category,
                    'instrument_type': acoustic_guitar_type,
                    'description': 'Classic acoustic guitar perfect for beginners',
                    'brand': 'Yamaha',
                    'model': 'FG800',
                    'rental_price_3months': Decimal('39.99'),
                    'rental_price_6months': Decimal('34.99'),
                    'rental_price_12months': Decimal('29.99'),
                    'rental_price_24months': Decimal('24.99'),
                    'purchase_price': Decimal('199.99'),
                },
                {
                    'name': 'Fender CD-60S',
                    'category': strings_category,
                    'instrument_type': acoustic_guitar_type,
                    'description': 'Fender acoustic guitar with rich sound',
                    'brand': 'Fender',
                    'model': 'CD-60S',
                    'rental_price_3months': Decimal('44.99'),
                    'rental_price_6months': Decimal('39.99'),
                    'rental_price_12months': Decimal('34.99'),
                    'rental_price_24months': Decimal('29.99'),
                    'purchase_price': Decimal('249.99'),
                },
                {
                    'name': 'Squier Stratocaster',
                    'category': strings_category,
                    'instrument_type': electric_guitar_type,
                    'description': 'Classic electric guitar for rock and blues',
                    'brand': 'Squier',
                    'model': 'Stratocaster',
                    'rental_price_3months': Decimal('49.99'),
                    'rental_price_6months': Decimal('44.99'),
                    'rental_price_12months': Decimal('39.99'),
                    'rental_price_24months': Decimal('34.99'),
                    'purchase_price': Decimal('299.99'),
                },
                {
                    'name': 'Epiphone Les Paul',
                    'category': strings_category,
                    'instrument_type': electric_guitar_type,
                    'description': 'Epiphone Les Paul with classic rock sound',
                    'brand': 'Epiphone',
                    'model': 'Les Paul Standard',
                    'rental_price_3months': Decimal('54.99'),
                    'rental_price_6months': Decimal('49.99'),
                    'rental_price_12months': Decimal('44.99'),
                    'rental_price_24months': Decimal('39.99'),
                    'purchase_price': Decimal('349.99'),
                },
                {
                    'name': 'Squier Precision Bass',
                    'category': strings_category,
                    'instrument_type': electric_bass_type,
                    'description': 'Classic P-Bass sound for any genre',
                    'brand': 'Squier',
                    'model': 'Precision Bass',
                    'rental_price_3months': Decimal('49.99'),
                    'rental_price_6months': Decimal('44.99'),
                    'rental_price_12months': Decimal('39.99'),
                    'rental_price_24months': Decimal('34.99'),
                    'purchase_price': Decimal('299.99'),
                },
                
                # Percussion Instruments
                {
                    'name': 'Pearl Export Drum Kit',
                    'category': percussion_category,
                    'instrument_type': drum_kit_type,
                    'description': 'Complete drum kit with cymbals and hardware',
                    'brand': 'Pearl',
                    'model': 'Export',
                    'rental_price_3months': Decimal('89.99'),
                    'rental_price_6months': Decimal('79.99'),
                    'rental_price_12months': Decimal('69.99'),
                    'rental_price_24months': Decimal('59.99'),
                    'purchase_price': Decimal('599.99'),
                },
                {
                    'name': 'Meinl Cajón',
                    'category': percussion_category,
                    'instrument_type': cajon_type,
                    'description': 'Professional cajón for flamenco and acoustic',
                    'brand': 'Meinl',
                    'model': 'Headliner',
                    'rental_price_3months': Decimal('24.99'),
                    'rental_price_6months': Decimal('19.99'),
                    'rental_price_12months': Decimal('14.99'),
                    'rental_price_24months': Decimal('9.99'),
                    'purchase_price': Decimal('149.99'),
                },
                
                # Wind Instruments
                {
                    'name': 'Yamaha YTR-2330 Trumpet',
                    'category': wind_category,
                    'instrument_type': trumpet_type,
                    'description': 'Student trumpet perfect for beginners',
                    'brand': 'Yamaha',
                    'model': 'YTR-2330',
                    'rental_price_3months': Decimal('59.99'),
                    'rental_price_6months': Decimal('54.99'),
                    'rental_price_12months': Decimal('49.99'),
                    'rental_price_24months': Decimal('44.99'),
                    'purchase_price': Decimal('399.99'),
                },
                {
                    'name': 'Yamaha YAS-280 Saxophone',
                    'category': wind_category,
                    'instrument_type': saxophone_type,
                    'description': 'Alto saxophone with rich jazz sound',
                    'brand': 'Yamaha',
                    'model': 'YAS-280',
                    'rental_price_3months': Decimal('79.99'),
                    'rental_price_6months': Decimal('74.99'),
                    'rental_price_12months': Decimal('69.99'),
                    'rental_price_24months': Decimal('64.99'),
                    'purchase_price': Decimal('599.99'),
                },
                {
                    'name': 'Yamaha YFL-222 Flute',
                    'category': wind_category,
                    'instrument_type': flute_type,
                    'description': 'Student flute with clear tone',
                    'brand': 'Yamaha',
                    'model': 'YFL-222',
                    'rental_price_3months': Decimal('69.99'),
                    'rental_price_6months': Decimal('64.99'),
                    'rental_price_12months': Decimal('59.99'),
                    'rental_price_24months': Decimal('54.99'),
                    'purchase_price': Decimal('499.99'),
                },
                
                # Keyboards
                {
                    'name': 'Yamaha P-45 Digital Piano',
                    'category': keyboards_category,
                    'instrument_type': digital_piano_type,
                    'description': '88-key digital piano with weighted keys',
                    'brand': 'Yamaha',
                    'model': 'P-45',
                    'rental_price_3months': Decimal('89.99'),
                    'rental_price_6months': Decimal('79.99'),
                    'rental_price_12months': Decimal('69.99'),
                    'rental_price_24months': Decimal('59.99'),
                    'purchase_price': Decimal('599.99'),
                },
                {
                    'name': 'Alesis V49 MIDI Keyboard',
                    'category': keyboards_category,
                    'instrument_type': midi_keyboard_type,
                    'description': '49-key MIDI keyboard for music production',
                    'brand': 'Alesis',
                    'model': 'V49',
                    'rental_price_3months': Decimal('39.99'),
                    'rental_price_6months': Decimal('34.99'),
                    'rental_price_12months': Decimal('29.99'),
                    'rental_price_24months': Decimal('24.99'),
                    'purchase_price': Decimal('199.99'),
                },
            ]
            
            # Create or update products
            for product_data in products_data:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults=product_data
                )
                
                if created:
                    self.stdout.write(f'Created: {product.name}')
                else:
                    # Update existing product with new rental prices
                    for key, value in product_data.items():
                        setattr(product, key, value)
                    product.save()
                    self.stdout.write(f'Updated: {product.name}')
            
            self.stdout.write(
                self.style.SUCCESS('Successfully populated rental prices for all products!')
            )











