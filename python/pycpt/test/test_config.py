from cpt.configuration import Configuration

if __name__ == '__main__':
    p = Configuration(test_env='paas_ci')
    i = 0
    for key in sorted(p.properties.keys()):
        i += 1
        print(f"{i}. {key}={p.properties[key]}")
