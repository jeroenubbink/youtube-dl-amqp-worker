# youtube-dl-amqp-worker

A very basic AMQP worker that listens to events on RabbitMQ and downloads
the requested youtube URL

## Getting Started

Just clone the thing.

Configure RabbitMQ and download location in `config.yml`
Check the `config.yml.example` for an example configuration.
Configuration can also be exposed through environment variables. They will
Take precedence over `config.yml`.

For ease of use you can run RabbitMQ in docker by running: `docker-compose up`.

### Prerequisites

Docker (optional)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Jeroen Ubbink** - [jeroenubbink](https://github.com/jeroenubbink)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
