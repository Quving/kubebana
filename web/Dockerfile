FROM node:14.1.0

LABEL maintainer="Vinh Ngu"

# Build assets
WORKDIR /build
ADD . .

RUN npm install
RUN npm run build

# Serve assets
FROM nginx:alpine

EXPOSE 80
COPY --from=0 /build/dist /usr/share/nginx/html
COPY --from=0 /build/nginx.conf /etc/nginx/conf.d/default.conf
