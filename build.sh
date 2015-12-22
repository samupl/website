#!/usr/bin/env bash

# Compile sass files
scss media/sass/style.scss media/css/style.css

# Compress and minify JS (order matters)
uglifyjs \
    media/js/jquery.js \
    media/js/bootstrap.js \
    media/js/samu.js \
    > media/minified.js

# Compress and minify css
uglifycss media/css/* > media/minified.css

# Collect static files
python manage.py collectstatic --noinput