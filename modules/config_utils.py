import os

# config.txt fica uma pasta acima deste arquivo
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'config.txt'
)

def load_config(section, config_path=CONFIG_PATH):
    """Retorna a lista de linhas da seção [section] do config.txt."""
    values = []
    current = None

    with open(config_path, encoding='utf-8') as f:
        for line in f:
            line = line.split('#', 1)[0].strip()  # remove comentários
            if not line:
                continue
            if line.startswith('[') and line.endswith(']'):
                current = line[1:-1].strip()
                continue
            if current == section:
                values.append(line)

    if not values:
        raise ValueError(f"Seção [{section}] não encontrada ou vazia em {config_path}")
    return values

def load_bool_config(section, config_path=CONFIG_PATH):
    """Como load_config, mas converte cada linha em bool (True/False/1/0)."""
    mapping = {'true': True, '1': True, 'false': False, '0': False}
    result = []
    for value in load_config(section, config_path):
        key = value.lower()
        if key not in mapping:
            raise ValueError(f"Valor inválido '{value}' na seção [{section}]. Use True ou False.")
        result.append(mapping[key])
    return result