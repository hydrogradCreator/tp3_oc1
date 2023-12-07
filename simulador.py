import sys

OUTPUT = "output.txt"


class CacheLine:
    def __init__(self):
        self.valid = 0
        self.block_address = None
        self.insertion_order = 0  # Adicionado para FIFO

    def update(self, block_address, insertion_order):
        self.valid = 1
        self.block_address = block_address
        self.insertion_order = insertion_order

    def __str__(self):
        addr_str = (
            f"{self.valid} 0x{self.block_address:08X}"
            if self.valid
            else f"{self.valid}"
        )

        return addr_str
        # return f"{self.valid}{addr_str}"


class CacheSimulator:
    def __init__(self, cache_size, line_size, group_size):
        self.line_size = line_size
        self.group_size = group_size
        self.line_count = cache_size // line_size
        self.lines = [CacheLine() for _ in range(self.line_count)]
        self.hits = 0
        self.misses = 0
        self.access_count = 0  # Contador de acessos para controle de FIFO

    def access_memory(self, address):
        block_address = address // self.line_size
        group_index = block_address % (self.line_count // self.group_size)

        start_index = group_index * self.group_size
        end_index = start_index + self.group_size

        for i in range(start_index, end_index):
            line = self.lines[i]
            if line.valid and line.block_address == block_address:
                cont = 0
                self.hits += 1
                cont = cont + 1
                return cont  # Hit found

        # Miss: Replace the oldest line in the group
        self.misses += 1
        oldest_line_index = None
        oldest_insertion_order = float("inf")

        for i in range(start_index, end_index):
            line = self.lines[i]
            if not line.valid:
                oldest_line_index = i
                break
            elif line.insertion_order < oldest_insertion_order:
                oldest_insertion_order = line.insertion_order
                oldest_line_index = i

        self.lines[oldest_line_index].update(block_address, self.access_count)
        self.access_count += 1

    def print_stats(self, file):
        file.write("================\n")
        file.write("IDX V ** ADDR **\n")
        for idx, line in enumerate(self.lines):
            file.write(f"{idx:03} {line}\n")

    def print_hits_miss(self, file):
        file.write(f"#hits: {self.hits}\n#miss: {self.misses}")


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python simulador.py <cache_size> <line_size> <group_size> <access_file>"
        )
        sys.exit(1)

    cache_size = int(sys.argv[1])
    line_size = int(sys.argv[2])
    group_size = int(sys.argv[3])
    access_file = sys.argv[4]

    simulator = CacheSimulator(cache_size, line_size, group_size)

    with open(OUTPUT, "w") as file_out:
        with open(access_file, "r") as file:
            for line in file:
                address = int(line.strip(), 16)
                cont = simulator.access_memory(address)
                print(f"{cont}")

                # Remova a próxima linha se não quiser imprimir as estatísticas após cada acesso

                # Processar a linha aqui
                if (
                    file.readline() == "" and cont == 1
                ):  # Checagem se a próxima linha é o final do arquivo
                    print("Estou na última linha.")
                    break

                else:
                    simulator.print_stats(file_out)

            simulator.print_hits_miss(file_out)


if __name__ == "__main__":
    main()


# with open(access_file, 'r') as file:
#             lines = file.readlines()  # Lê todas as linhas do arquivo de uma vez

#         for i, line in enumerate(lines):
#             address = int(line.strip(), 16)
#             hit = simulator.access_memory(address)  # Retorna 1 se for um HIT, caso contrário 0

#             # Se estiver na última linha E for um HIT, não escreva no arquivo
#             if i == len(lines) - 1 and hit:
#                 break
#             else:
#                 simulator.print_stats(file_out)

#         simulator.print_hits_miss(file_out)
