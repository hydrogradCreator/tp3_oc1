import sys

class CacheLine:
    #inicializa cada linha da cache com o bit de validade. 0 ou 1
    def __init__(self):
        self.valid = 0
        self.block_address = None

    def update(self, block_address):
        self.valid = 1
        self.block_address = block_address

    # aqui é onde imprime formatado o endereço
    def __str__(self):
        addr_str = f"0x{self.block_address:08X}" if self.valid else "       "
        return f"{self.valid} {addr_str}"

class CacheSimulator:
    # inicializa o objeto, recebendo os parametros por linha de comando
    def __init__(self, cache_size, line_size, group_size):
        self.line_size = line_size
        self.group_size = group_size
        self.line_count = cache_size // line_size
        self.lines = [CacheLine() for _ in range(self.line_count)]
        self.hits = 0
        self.misses = 0

    def access_memory(self, address):
        #simula a associatividade
        # calcula qual bloco de memoria ta sendo acessado e determina qual grupo esse bloco pertence
        # ou seja, determina de qual bloco de memoria o endereço acessado é.
        # self.line é o tamanho de uma linha da cache (bytes)
        block_address = address // self.line_size

        #calcula o indice para qual grupo o bloco de memoria deve ser mapeado
        # self.group_size é o número de linhas em cada grupo (ou conjunto) na cache.
        group_index = block_address % (self.line_count // self.group_size)

        # recalcula os indíces como se fosse o LRU
        start_index = group_index * self.group_size
        end_index = start_index + self.group_size

        for i in range(start_index, end_index):
            line = self.lines[i]
            if line.valid and line.block_address == block_address:
                self.hits += 1
                return  # Hit found

        # Miss: find the first invalid line or replace the oldest line in the group (LRU)
        self.misses += 1
        for i in range(start_index, end_index):
            line = self.lines[i]
            if not line.valid:
                line.update(block_address)
                return

        # Replace the first line in the group
        self.lines[start_index].update(block_address)

    def print_stats(self):
        print("================")
        print("IDX V ** ADDR **")
        for idx, line in enumerate(self.lines):
            print(f"{idx:03} {line}")

    def print_hits_miss(self): 
        print(f"#hits: {self.hits} \n#miss: {self.misses}")

def main():
    if len(sys.argv) != 5:
        print("Usage: python simulador.py <cache_size> <line_size> <group_size> <access_file>")
        sys.exit(1)

    cache_size = int(sys.argv[1])
    line_size = int(sys.argv[2])
    group_size = int(sys.argv[3])
    access_file = sys.argv[4]

    #instancia da cache
    simulator = CacheSimulator(cache_size, line_size, group_size)

    with open(access_file, 'r') as file:
        for line in file:
            address = int(line.strip(), 16)
            simulator.access_memory(address)
            simulator.print_stats()
    print(f"\n")
    simulator.print_hits_miss()

if __name__ == "__main__":
    main()
