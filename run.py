#!/usr/bin/env python3
"""
Script de inicialização para produção (Railway, Render, etc.)
"""
import os
from app import app, init_database

# Inicializar banco de dados
init_database()

if __name__ == '__main__':
    # Railway e outras plataformas fornecem a variável PORT
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Usar gunicorn em produção, Flask dev server em desenvolvimento
    if os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RAILWAY_ENVIRONMENT'):
        # Se gunicorn estiver disponível, usar ele
        try:
            import gunicorn.app.wsgiapp as wsgi
            import sys
            sys.argv = [
                'gunicorn',
                '-w', '4',
                '-b', f'{host}:{port}',
                '--config', 'gunicorn.conf.py',
                'app:app'
            ]
            wsgi.run()
        except ImportError:
            # Fallback para Flask dev server
            print("Gunicorn não encontrado, usando Flask dev server")
            app.run(host=host, port=port, debug=False)
    else:
        # Modo desenvolvimento
        app.run(host=host, port=port, debug=True)
