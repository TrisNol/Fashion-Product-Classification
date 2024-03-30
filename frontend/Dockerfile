FROM node:20.12.0-alpine3.19 AS build
WORKDIR /app
COPY . .
RUN npm ci && npm run build --prod

FROM nginx:1.25.4-alpine3.18-slim
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist/frontend /usr/share/nginx/html
EXPOSE 80

CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/assets/env.template.js > /usr/share/nginx/html/assets/env.js && exec nginx -g 'daemon off;'"]