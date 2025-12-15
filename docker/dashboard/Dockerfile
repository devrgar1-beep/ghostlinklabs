FROM nginx:stable-alpine

# Remove default nginx config
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy site static files from repo root (with build context set in compose)
COPY ui/dashboard /usr/share/nginx/html
COPY docker/dashboard/nginx.conf /etc/nginx/conf.d/ghostlink.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
