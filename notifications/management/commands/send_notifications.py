from django.core.management.base import BaseCommand
from notifications.utils import process_pending_notifications
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Process pending notifications and send them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose output',
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        
        if verbose:
            self.stdout.write(self.style.SUCCESS('Processing pending notifications...'))
        
        sent_count, failed_count = process_pending_notifications()
        
        if verbose:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully sent {sent_count} notifications, {failed_count} failed'
                )
            )
        
        logger.info(f'Notification processing completed: {sent_count} sent, {failed_count} failed')
