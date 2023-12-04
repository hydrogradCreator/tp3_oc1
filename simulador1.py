import sys

class CacheLine:
    def __init__(self):
        self.valid = 0
        self.block_address = None

    def update(self, block_address):
        self.valid = 1
        self.block_address = block_address

    def __str__(self):
        addr_str = f"0x{self.block_address:08X}" if self.valid else "       "
        return f"{self.valid} {addr_str}"

class CacheSimulator:
    def __init__(self, cache_size, line_size, group_size):
        self.line_size = line_size
        self.group_size = group_size
        self.group_count = cache_size // (line_size * group_size)
        self.lines = [CacheLine() for _ in range(self.group_count * group_size)]
        self.hits = 0
        self.misses = 0

    def access_memory(self, address):


        #simula a associatividade
        # calcula qual bloco de memoria ta sendo acessado e determina qual grupo esse bloco pertence
        # ou seja, determina de qual bloco de memoria o endereço acessado é.
        # self.line é o tamanho de uma linha da cache (bytes)
        block_address = address // self.line_size
        group_index = (block_address % self.group_count) * self.group_size

        # Check for hit within the group
        # verifica se a linha atual é válida (self.lines[i].valid == 1) e se o endereço do bloco nessa linha 
        # (self.lines[i].block_address) corresponde ao bloco que está sendo acessado (block_address).
        # Hit: Se ambas as condições forem verdadeiras, incrementa o contador de hits (self.hits) e retorna, 
        # indicando que um hit foi encontrado e o acesso à memória foi bem-sucedido.

        for i in range(group_index, group_index + self.group_size):
            if self.lines[i].valid and self.lines[i].block_address == block_address:
                self.hits += 1
                return  # Hit found
        self.misses += 1
        
        # Miss: Replace using FIFO within the group
        # Percorre novamente todas as linhas dentro do grupo para encontrar uma linha inválida (não utilizada).
        # Atualização da Linha Inválida: Se uma linha inválida for encontrada, atualiza essa linha com o endereço do bloco atual (block_address) e retorna.
        # Substituição FIFO: Se não houver linhas inválidas (todas as linhas no grupo estão em uso), substitui a primeira linha do grupo pelo bloco atual. 
        # Isso segue a política FIFO, onde a linha mais antiga é substituída pela nova.
        # Rotação das Linhas: Depois de substituir a primeira linha, as linhas dentro do grupo são reordenadas para manter a ordem FIFO.
        # A linha que acabou de ser atualizada é movida para o final do grupo, mantendo a ordem de chegada das linhas.
        
        for i in range(group_index, group_index + self.group_size):
            if not self.lines[i].valid:
                self.lines[i].update(block_address)
                return
        # Replace the first line in the group
        self.lines[group_index].update(block_address)
        # Rotate lines within the group to maintain FIFO order
        self.lines[group_index:group_index + self.group_size] = \
            self.lines[group_index + 1:group_index + self.group_size] + [self.lines[group_index]]

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

    simulator = CacheSimulator(cache_size, line_size, group_size)

    with open(access_file, 'r') as file:
        for line in file:
            address = int(line.strip(), 16)
            simulator.access_memory(address)
            simulator.print_stats()
    print("\n")
    simulator.print_hits_miss()

if __name__ == "__main__":
    main()
