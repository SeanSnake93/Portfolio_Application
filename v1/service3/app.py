#!/usr/bin/env python3
 
from application import app

__name__ = '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')