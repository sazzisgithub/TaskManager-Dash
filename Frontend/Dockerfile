FROM nginx:alpine

# Install envsubst (comes with gettext package)
RUN apk add --no-cache gettext

# Copy all frontend files into nginx's HTML directory
COPY . /usr/share/nginx/html

# Copy nginx config template
COPY nginx.conf /etc/nginx/templates/default.conf.template

EXPOSE 80

CMD ["/bin/sh", "-c", "envsubst '${PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
