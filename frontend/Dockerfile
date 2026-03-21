# QuantDinger Frontend — static runtime image
# Build context: repository root (see docker-compose.yml)
# The open-source repo ships prebuilt static assets in `frontend/dist`,
# so no Node.js build stage is required.
ARG RUNTIME_IMAGE=nginx:1.25-alpine
FROM ${RUNTIME_IMAGE}

RUN apk add --no-cache curl

COPY frontend/dist/ /usr/share/nginx/html/
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
