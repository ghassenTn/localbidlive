# LocalBidLive

A real-time auction platform connecting local businesses with consumers for time-sensitive deals and surplus inventory.

## Features

- Real-time bidding system powered by Centrifugo
- Geolocation-based auction filtering
- Push notifications for auction updates
- Multi-language support
- Responsive design
- Secure payment processing
- Business analytics dashboard

## Technical Stack

- Backend: Django
- Real-time Updates: Centrifugo
- Frontend: Django templates with Bootstrap
- Database: PostgreSQL
- Cache: Redis
- Task Queue: Celery

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file and set your environment variables
4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
