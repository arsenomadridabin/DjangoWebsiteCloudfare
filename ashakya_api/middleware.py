import requests
import pytz
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Visitor
import logging

logger = logging.getLogger('__name__')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Define the local timezone
LOCAL_TZ = pytz.timezone('America/Chicago')  # Replace with your local time zone

class VisitorMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/':  # Only process for the root path
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            referer = request.META.get('HTTP_REFERER','No Referer')
            # Check if an entry with the same IP address exists within the last 10 minutes
            ten_minutes_ago = timezone.now() - timedelta(minutes=10)
            if not Visitor.objects.filter(
                ip_address=ip_address,
                timestamp__gte=ten_minutes_ago
            ).exists():
                # Make an API request to get geolocation data
                #ip_stack_access_key = '4959d4309ddf57c2de44f7dd9bcfbac7'
                #url = f'http://api.ipstack.com/{ip_address}?access_key={ip_stack_access_key}'
                
                ip_geo_access_key='254e7d78cc1f47ba8519473c18baabae'
                url = f'https://api.ipgeolocation.io/ipgeo?apiKey={ip_geo_access_key}&ip={ip_address}'
                logger.info("url:")
                logger.info(url)
                try:
                    response = requests.get(url)
                    logger.info(response)
                    geo_data = response.json()

                    # Get the current time in the local timezone
                    local_time = timezone.now().astimezone(LOCAL_TZ)

                    # Save visitor information to the database
                    Visitor.objects.create(
                        ip_address=ip_address,
                        user_agent=user_agent,
                        country_name=geo_data.get('country_name', ''),
                        region_name=geo_data.get('state_prov', ''),
                        zip_code=geo_data.get('zipcode', ''),
                        latitude=geo_data.get('latitude', 0.0),
                        longitude=geo_data.get('longitude', 0.0),
                        timestamp=local_time,  # Save the local time
                        city=geo_data.get('city',''),
                        referer=referer,
                        isp=geo_data.get('isp',''),
                        organization=geo_data.get('organization','')
                    )

                except Exception as e:
                    logger.info("Exception Visitor object creation:")
                    import traceback
                    logger.info(traceback.format_exc())
                    # Handle exceptions if needed
                    try:
                        Visitor.objects.create(referer=referer,user_agent=user_agent,ip_address=ip_address)
                    except:
                        pass
        else:
            if request.path == "/static/files/Abin_CV.pdf":
                Visitor.objects.create(ip_address=ip_address,user_agent=user_agent,download=True)
            else:
                pass
