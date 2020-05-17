import yaml

from encoders.encoder_factory import EncoderFactory


class Main:

    def __init__(self):
        with open("./encoder_config.yml") as file:
            encoder_conf_dict = yaml.safe_load(file)
        self.encoder_factory = EncoderFactory(encoder_conf_dict)

    def run(self):
        encoder = self.encoder_factory.get_encoder("bert_embedded")

        while True:
            text = input(">")
            result = encoder.encode([text])
            print(result)


if __name__ == "__main__":
    main = Main()
    main.run()
