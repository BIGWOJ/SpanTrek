from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates test users to database'

    def handle(self, *args, **options):
        User = get_user_model()
        
        usernames = [
            'alexsmith', 'mariagarcia', 'johndoe', 'sarahjohnson', 'mikewilson',
            'emmabrown', 'davidjones', 'lisadavis', 'chrismiller', 'annawilson',
            'tomanderson', 'jennytaylor', 'stevethomas', 'katejackson', 'paulwhite',
            'lucyharris', 'markmartin', 'sophiethompson', 'ryangarcia', 'amyrobinson',
            'jakeclark', 'ninarodriguez', 'benlewis', 'zoelee', 'maxwalker'
        ]
        
        password = 'testpassword'
        
        created_count = 0
        skipped_count = 0
        
        for username in usernames:
            # Skip if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(f'User {username} already exists - skipped')
                skipped_count += 1
                continue
            
            # Otherwise, create the user
            try:
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@email.com',
                    password=password
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created user: {username}')
                )
                created_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating user {username}: {str(e)}')
                )
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Test users creation summary:')
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
        self.stdout.write(f'Skipped: {skipped_count}')
        self.stdout.write(f'Total processed: {created_count + skipped_count}')
        self.stdout.write('='*50)