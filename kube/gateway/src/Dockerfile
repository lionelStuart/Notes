# syntax=docker/dockerfile:1

FROM golang:1.21

# Set destination for COPY
WORKDIR /app

ENV GOPROXY='https://goproxy.cn,direct'


# Download Go modules
COPY . ./
RUN go mod download

# Copy the source code. Note the slash at the end, as explained in
# https://docs.docker.com/engine/reference/builder/#copy


# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o=main  cmd/main.go

# Optional:
# To bind to a TCP port, runtime parameters must be supplied to the docker command.
# But we can document in the Dockerfile what ports
# the application is going to listen on by default.
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE 8090

# Run
CMD ["bash", "./start.sh"]
