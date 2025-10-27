from django.core.management.base import BaseCommand
from base.models import User

class Command(BaseCommand):
    help = 'Create daily challenges for all users'

    def handle(self, *args, **options):
        """Create daily challenges for all users - runs daily at specified time."""
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found'))
            return
        
        success_count = 0
        for user in users:
            try:
                user.create_daily_challenges()
                success_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error for user {user.username}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Created daily challenges for {success_count} users')
        )