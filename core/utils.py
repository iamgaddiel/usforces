from string import ascii_letters, digits
from  random import choices

from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model

def get_random_string(count: int) -> str:
    return ''.join(choices(ascii_letters + digits, k=count))


class ExtendedEncoder(DjangoJSONEncoder):

    def default(self, o):

        if isinstance(o, Model):
            return model_to_dict(o)

        return super().default(o)


if __name__ == '__main__':
    print(get_random_string(6))