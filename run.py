import os
import sys

# Add current directory to Python path to import backend correctly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app, seed_database

if __name__ == '__main__':
    # Set USE_SQLITE=true by default for local execution if MySQL environment is not configured
    if not os.environ.get('MYSQL_HOST'):
        os.environ['USE_SQLITE'] = 'true'
        
    app = create_app()
    seed_database(app)
    
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting local Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
